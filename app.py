import unittest
from appium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.android.webdriver import DesiredCapabilities


class ContactAppTestAppium(unittest.TestCase):

    teardowns_counter = 1

    def setUp(self):

        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '8.0.0'
        desired_caps['deviceName'] = 'Nexus 5X'
        desired_caps['app'] = 'c:\\selendroid-test-app.apk'
        desired_caps['appActivity'] = '.HomeScreenActivity'
        desired_caps['appPackage'] = 'io.selendroid.testapp'

        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        sleep(1)

    def tearDown(self):

        print('robot committed another suicide \n')
        self.driver.quit()
        sleep(1)

    def test_RobotAttemptListElements(self):

        elements = self.driver.find_elements_by_xpath("//*[not(*)]")

        for element in elements:

            print('robot says current element ID    = {} \n'.format(element.id))
            print('robot says current element text  = {} \n'.format(element.text))

            if element.id == '8':

                element.click()
                print('robot says it will wait until new activity is shown \n')
                self.robot_should_wait_until_activity_shown('.RegisterUserActivity', 10)
                sleep(1)
                self.driver.hide_keyboard()
                self.driver.back()
            
            else:

                print('robot taking a look at element id {}.. \n'.format(element.id))
                print('robot took a look & says no.. \n')
                sleep(1)

    def test_LaunchApp(self):

        print('robot is going to launch client..\n')
        self.driver.launch_app()

    def list_elements_robots_see(self):

        return self.driver.find_elements_by_xpath("//*[not(*)]")

    def test_list_elements_robot_got_via_uiAutomator(self):

        elements = self.driver.find_elements_by_android_uiautomator('new UiSelector().clickable(true)')
        for element in elements:

            print('{}\n'.format(element.text))

    def robot_should_wait_until_activity_shown(self, activity_for_robot, robot_timeout):

        print('robot should now wait until current activity is {} \n'.format(activity_for_robot))
        
        self.driver.wait_activity(activity_for_robot, timeout=robot_timeout)

        print('robot says current activity is {}'.format(
            self.driver.current_activity))

        if self.driver.current_activity == activity_for_robot:

            return True

        else:

            return False

    def robot_should_hide_keyboard(self):

        self.driver.hide_keyboard()


if __name__ == '__main__':

    suite = unittest.TestLoader().loadTestsFromTestCase(ContactAppTestAppium)
    unittest.TextTestRunner(verbosity=2).run(suite)
