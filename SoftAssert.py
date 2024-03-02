import inspect
import unittest
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement


class SoftAssert(unittest.TestCase):
    """
    Implementation of soft assertions for unittest and continuation of test run if a webdriver element was not found:
    1. Collect AssertionErrors and continue with test run
    2. Collect webdriver's exception and continue with test run
    3. Fail the test after all the checks are done if there are collected failures
    """
    def __init__(self, methodName):
        super().__init__(methodName)
        self._failures_list = []

    def soft_assert(self, assert_method, *expressions, **keywordExpressions):
        """
        Calls the assert method, stores AssertionError to the test object
        Example usage:
            SoftFailuresCollector.soft_assert(unittest.TestCase.assertEqual, response.status_code, 200,
                f"Request failed with status {response.status_code}")
            SoftFailuresCollector.soft_assert(unittest.TestCase.assertTrue, len(flights) == 1,
                f"Found {len(flights)} flights, but 1 was expected")
        :param assert_method:   unittest assert method
        :param expressions:     arguments to the assert method
        :param kwargs:          keyword arguments to the assert methods
        :return:
        """
        try:
            # if assert_method is a function (added to special variables)
            if type(assert_method).__name__ == "function":
                assert_method(self, *expressions, **keywordExpressions)
            # if assert_method is a bound method (type(assert_method).__name__ = "method")
            else:
                assert_method(*expressions, **keywordExpressions)
        except AssertionError as err:
            caller, lineno, errMsg = self.report_stack(err)
            self._failures_list.append(
                {"caller": caller,
                 "ln": lineno,
                 "err": errMsg})
            print(self._failures_list[-1])

    def soft_find_element_or_attribute(self, driver, By, value, command=None, get_attribute=None):
        """
        Searches for the element, stores exception to test object, executes a command on the found element
        :param driver:  webdriver object
        :param By:      locator strategy
        :param value:   Locator value
        :param command: (String) Name of the command to execute on found WebElement
        :return:    Found element
        """
        element, attribute = None, None
        try:
            element = driver.find_element(By, value)
        except Exception as err:
            caller, lineno, errMsg = self.report_stack(err)
            self._failures_list.append(
                {"caller": caller,
                 "ln": lineno,
                 "err": errMsg})
            print(self._failures_list[-1])
            return

        # get_attribute goes before command
        # otherwise risk stale element reference exception
        if get_attribute:
            # Attribute will be None if it was not found, or "" if found but empty string, or a string
            attribute = self.get_element_attribute(element, get_attribute)

        if command:
            self.call_action_on_element(element, command)

        return attribute if get_attribute else element

    def call_action_on_element(self, element, action):
        try:
            command_to_execute = getattr(WebElement, action)
            command_to_execute(element)
        except Exception as err:
            caller, lineno, errMsg = self.report_stack(err)
            self._failures_list.append(
                {"caller": caller,
                 "ln": lineno,
                 "err": errMsg})
            print(self._failures_list[-1])

    def get_element_attribute(self, element, attribute):
        try:
            return element.get_attribute(attribute)
        except Exception as err:
            caller, lineno, errMsg = self.report_stack(err)
            self._failures_list.append(
                {"caller": caller,
                 "ln": lineno,
                 "err": errMsg})
            print(self._failures_list[-1])

    def soft_find_element_expect_not_found(self, driver, By, value):
        """
        Searches for the element, stores exception to test object if NoSuchElementException is NOT returned
        :param driver:  webdriver object
        :param by:      Locator strategy object, eg. By.XPATH
        :param value:   (String) Locator value, eg. "//div[@class='inbound']"
        :return:        Found element or attribute value
        """
        element = None
        try:
            # Expects NoSuchElementException on element search, otherwise raises AssertionError
            with self.assertRaises(NoSuchElementException, msg=f"Unexpected element found by {By} {value}") as exc:
                element = driver.find_element(By, value)
        except Exception as err:
            caller, lineno, errMsg = self.report_stack(err)
            self._failures_list.append(
                {"caller": caller,
                 "ln": lineno,
                 "err": errMsg})
            print(self._failures_list[-1])
        return element

    def assert_all(self):
        """
        Fails the test if there is at least one failure from previously executed check stored in the test object
        :return:
        """
        if len(self._failures_list) > 0:
            self.fail(f"One or more checks failed:\n{self._failures_list}")

    @staticmethod
    def report_stack(exception):
        """
        Returns the details about the line that didn't execute successfully in the caller method
        :return: caller - function name
        :return: lineno - line number
        """
        caller, lineno = None, None

        stack_list = inspect.stack()
        for stack in stack_list:
            func_name = getattr(stack, 'function', stack[3])
            if "test" in func_name:
                caller = func_name
                lineno = stack.lineno
                break

        # Some AssertionErrors don't return msg but 'standardMsg'
        exceptionMsg = exception.msg if hasattr(exception, "msg") else exception.args[0]

        return caller, lineno, exceptionMsg
