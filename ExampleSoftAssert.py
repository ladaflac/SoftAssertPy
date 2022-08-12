import requests
from selenium.webdriver.common.by import By
from HelperMethods import openPageInChrome
from SoftAssert import SoftAssert


class ExampleSoftAssert(SoftAssert):

    def test_soft_assert_api(self):
        """
        Sample API test.
        Runs all the checks, saves the failures and
        prints the details of all failed assertions after all the checks are executed.
        Expected test result is "fail".
        :return:
        """
        response = requests.get("https://www.google.com/search?q=python")

        # success expected
        SoftAssert.soft_assert(self, self.assertEqual, response.status_code, 200, f"Request failed with status {response.status_code}")

        headerCount = response.content.decode().count("h1")
        # assertion error expected
        SoftAssert.soft_assert(self, self.assertGreater, headerCount, 10, f"Found {headerCount} headers, but expected 10")

        # success expected
        SoftAssert.soft_assert(self, self.assertTrue, "accounts.google.com/ServiceLogin" in response.content.decode())

        # test failure expected
        SoftAssert.assert_all(self)

    def test_soft_assert_webdriver(self):
        """
        Sample Selenium test.
        Runs all the checks, saves the failures and
        prints the details of all failed assertions after all the checks are executed.
        Expected test result is "fail".
        :return:
        """
        self.driver = openPageInChrome("https://www.google.com/search?q=python")

        # success expected
        SoftAssert.soft_find_element(self, self.driver, By.XPATH, "//button[2]", "click")

        # selenium exception expected
        SoftAssert.soft_find_element(self, self.driver, By.XPATH, "//a[text() = 'Log in']")

        headerCount = len(self.driver.find_elements(By.TAG_NAME, "h1"))
        # assertion failure expected
        SoftAssert.soft_assert(self, self.assertGreater, headerCount, 10, msg=f"Found {headerCount} headers, but expected 10")

        # test failure expected
        SoftAssert.assert_all(self)

    def tearDown(self):
        if "driver" in self.__dict__:
            self.driver.quit()
