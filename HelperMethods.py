from selenium import webdriver
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver
from SeleniumEventListener import SeleniumEventListener


def openPageInChrome(url):
    """
    Creates an instance of chromedriver.
    Opens the url provided in the parameter.
    :param url:
    :return: driver object
    """
    chromedriver = webdriver.Chrome()
    driver = EventFiringWebDriver(chromedriver, SeleniumEventListener())
    driver.get(url)

    return driver
