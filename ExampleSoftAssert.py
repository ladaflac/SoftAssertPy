import requests
import selenium as selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from SoftAssert import SoftAssert


class ExampleSoftAssert(SoftAssert):

    def test_soft_assert_api(self):
        response = requests.get("https://www.google.com/search?q=python")

        SoftAssert.soft_assert(self, self.assertEqual, response.status_code, 200, f"Request failed with status {response.status_code}")

        headerCount = response.content.decode().count("h1")
        SoftAssert.soft_assert(self, self.assertGreater, headerCount, 10, f"Found {headerCount} headers, but expected 10")

        SoftAssert.soft_assert(self, self.assertTrue, "accounts.google.com/ServiceLogin" in response.content.decode())

        SoftAssert.assert_all(self)

    def test_soft_assert_webdriver(self):
        driver = selenium.webdriver.Chrome()
        driver.get(url="https://www.google.com/search?q=python")

        SoftAssert.soft_find_element(self, driver, By.XPATH, "//button[2]", "click")

        SoftAssert.soft_find_element(self, driver, By.XPATH, "//a[text() = 'Log in']")

        headerCount = len(SoftAssert.soft_find_elements(self, driver, By.TAG_NAME, "h1"))
        SoftAssert.soft_assert(self, self.assertGreater, headerCount, 10, msg=f"Found {headerCount} headers, but expected 10")

        SoftAssert.assert_all(self)
