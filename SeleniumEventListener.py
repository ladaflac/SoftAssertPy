import logging
from selenium.webdriver.support.events import AbstractEventListener


class SeleniumEventListener(AbstractEventListener):
    """
    Implementation of the event listener for Selenium.
    In this project applied to Selenium's find_element() methods.
    """
    def on_exception(self, exception, driver):
        """
        Logs the exception raised by Selenium
        :param exception:
        :param driver:
        :return:
        """
        logging.critical(exception)
