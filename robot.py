import unittest
import desired_capabilities
from appium import webdriver


class Runner(unittest.TestCase):

    def setUp(self, host_address='127.0.0.2', host_port=4724):

        self.desired_capabilities = desired_capabilities.return_desired_capabilities()
        self.host_address = host_address
        self.host_port = host_port
        self.driver = webdriver.Remote('http://{}:{}/wd/hub'.format(
            self.host_address,
            self.host_port),
            self.desired_capabilities)

    def tearDown(self):

        try:
        self.assertAlmostEqual()
            self.driver.quit()

        except Exception as driver_err:

            raise driver_err

    def return_current_activity(self):

        print('Robot should return driver current activity')

        try:

            return self.driver.current_activity

        except Exception as err:

            raise err
