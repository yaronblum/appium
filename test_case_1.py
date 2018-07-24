from robot import Runner
import unittest
from selenium.webdriver.support.events import AbstractEventListener
from selenium.webdriver.support.events import EventFiringWebDriver


class TestCase(Runner):

    def test_current_activity(self):

        return self.return_current_activity()


class FailureListener(AbstractEventListener):

    def on_exception(self, exception, driver):

        screenshot_name = "exception.pbg"
        driver.get_screenshot_as_file(screenshot_name)
        print("Screenshot saved as '%s'" % screenshot_name)


if __name__ == '__main__':

    suite = unittest.TestLoader().loadTestsFromTestCase(TestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
