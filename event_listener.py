import unittest
from appium import webdriver
from desired_capabilities import return_desired_capabilities
from selenium.webdriver.support.events import EventFiringWebDriver
from selenium.webdriver.support.events import AbstractEventListener

desired_caps = return_desired_capabilities()


class ScreenshotListener(AbstractEventListener):

    def on_exception(self, exception, driver):

        screenshot_name = 'exception.png'
        driver.get_screenshot_as_file(screenshot_name)
        print("Screenshot saved as '%s'" % screenshot_name)


class TestDemo(unittest.TestCase):

    def test_demo(self):

        appium_driver = webdriver.Remote('http://127.0.0.2:4724/wd/hub', desired_caps)
        d = EventFiringWebDriver(appium_driver, ScreenshotListener())

        d.get("http://www.google.com")
        d.find_element_by_css_selector("div.that-does-not-exist")


if __name__ == '__main__':

    unittest.main()
