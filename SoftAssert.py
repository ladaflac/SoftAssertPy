import inspect
import unittest
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement


class SoftAssert(unittest.TestCase):
    """
    Implementation of soft assertions for unittest and continuation of test run if a webdriver element was not found:
    1. Collect AssertionErrors and continue with test run
    2. Collect webdriver's NoSuchElementExceptions and continue with test run
    3. Fail the test after all the checks are done if there are collected failures
    """
    def __init__(self, methodName):
        super().__init__(methodName)
        self._failures_list = []

    def soft_assert(self, assert_method, *expressions, **keywordExpressions):
        """
        Calls the assert method, stores AssertionError to the test object
        :param assert_method:   unittest assert method
        :param expressions:     arguments to the assert method
        :param kwargs:          keyword arguments to the assert methods
        :return:
        """
        try:
            assert_method(*expressions, **keywordExpressions)
        except AssertionError as err:
            caller, lineno = self.report_stack()
            self._failures_list.append(
                {"caller": caller,
                 "ln": lineno,
                 "err": err})
            print(self._failures_list[-1])

    def soft_find_element(self, driver, By, value, command=None):
        """
        Searches for the element, stores NoSuchElementException to test object, executes a command on the found element
        :param driver:  webdriver object
        :param By:      locator strategy
        :param value:   Locator value
        :param command: (String) Name of the command to execute on found WebElement
        :return:    Found element
        """
        try:
            element = driver.find_element(By, value)
            if command:
                command_to_execute = getattr(WebElement, command)
                command_to_execute(element)
            return element
        except Exception as err:
            caller, lineno = self.report_stack()
            self._failures_list.append(
                {"caller": caller,
                 "ln": lineno,
                 "err": err.msg})
            print(self._failures_list[-1])

    def assert_all(self):
        """
        Fails the test if there is at least one failure from previously executed check stored in the test object
        :return:
        """
        if len(self._failures_list) > 0:
            self.fail(f"One or more checks failed:\n{self._failures_list}")

    @staticmethod
    def report_stack():
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
        return caller, lineno
