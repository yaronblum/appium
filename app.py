import unittest
from appium import webdriver
from time import sleep


class ContactAppTestAppium(unittest.TestCase):

    def setUp(self):

        desired_caps = {
            'platformName': 'Android',
            'platformVersion': '8.0.0',
            'deviceName': 'Nexus 5X',
            'app': 'c:\\selendroid-test-app.apk',
            'appActivity': '.HomeScreenActivity',
            'appPackage': 'io.selendroid.testapp',
            'noReset': True
        }

        print('robot connecting to device..\n')
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        print('\n robot executing {}\n'.format(self._testMethodName))

    def tearDown(self):

        print('\nrobot committed another suicide \n')
        self.driver.quit()

    def test_RobotAttemptListElements(self):

        elements = self.driver.find_elements_by_xpath("//*[not(*)]")
        for element in elements:

            print('robot => element id {}'.format(element.id))
            if element.id == '8':

                element.click()
                self.robot_should_wait_until_activity_shown('.RegisterUserActivity', 10)
                sleep(1)
                self.robot_should_hide_keyboard()
                self.driver.back()
            
            else:

                print('robot taking a look at element id {}..'.format(element.id))
                print('robot took a look & says no.. \n')
                sleep(1)

    def test_LaunchApp(self):

        print('robot is going to launch client..\n')
        self.driver.launch_app()

    def test_list_elements_robot_got_via_uiAutomator(self):

        elements = self.driver.find_elements_by_android_uiautomator('new UiSelector().clickable(true)')
        for element in elements:

            print('{}\n'.format(element.text))

    def test_network_connection(self):

        if self.return_current_network() == 6:

            return self.skipTest('robot connected via wifi.. skipping {}'.format(self._testMethodName))

        else:

            print('continue with test case {}'.format(self._testMethodName))

        self.robot_PING()

    def return_current_network(self):

        print('current network connection => {}\n'.format(self.driver.network_connection))
        return self.driver.network_connection

    def robot_should_wait_until_activity_shown(self, activity_for_robot, robot_timeout):

        print('robot should now wait until current activity is {} \n'.format(activity_for_robot))
        
        self.driver.wait_activity(activity_for_robot, timeout=robot_timeout)
        sleep(1)
        print('robot says current activity is {}'.format(
            self.driver.current_activity))

        if self.driver.current_activity == activity_for_robot:

            return True

        else:

            return False

    def robot_should_hide_keyboard(self):

        sleep(1)
        self.driver.hide_keyboard()

    def robot_should_get_network_type(self):

        try:

            return self.driver.network_connection

        except Exception as e:

            print('robot can\'t get network type..\n')
            raise e

    def robot_set_current_network_to_wifi(self):

        if self.robot_should_get_network_type() != 6:

            try:

                return self.driver.set_network_connection(2)

            except Exception as e:

                return e

    def list_elements_robots_see(self):

        return self.driver.find_elements_by_xpath("//*[not(*)]")

    def robot_PING(self):

        return self.driver.command_executor('adb shell ping www.google.com')


class ExternalToolBox(ContactAppTestAppium):

    def setUp(self):

        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '8.0.0'
        desired_caps['deviceName'] = 'Nexus 5X'
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)

    def robot_should_get_network_type(self):

        try:
            return self.driver.network_connection

        except Exception as e:

            print('robot can\'t get network type..\n')
            raise e

    def robot_should_enable_wifi_connection(self):

        try:
            self.driver.set_network_connection(2)
            print('robot successfully enabled the wifi as primary connection\n')

        except Exception as e:

            print('robot unable to enable to set wifi as primary connection\n')
            raise e

    def robot_should_restrict_network_to_data_only(self):

        try:

            self.driver.set_network_connection(4)
            print('robot successfully restricted connection to data only\n')

        except Exception as e:

            print('robot unable to restrict connection to data only')
            raise e


if __name__ == '__main__':

        suite = unittest.TestLoader().loadTestsFromTestCase(ContactAppTestAppium)
        unittest.TextTestRunner(verbosity=2).run(suite)
