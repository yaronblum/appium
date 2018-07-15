import unittest
from appium import webdriver


class ContactAppTestAppium(object):

    def __init__(self):

        desired_caps = {
            'platformName': 'Android',
            'platformVersion': '8.0.0',
            'deviceName': 'Nexus 5X',
            'app': 'c:\\selendroid-test-app.apk',
            'appActivity': '.HomeScreenActivity',
            'appPackage': 'io.selendroid.testapp',
            'noReset': True
        }

        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)

    def kill_robot(self):

        self.driver.quit()


class Network(ContactAppTestAppium):

    def __init__(self):

        # super(Network, self).setUp()
        super(Network, self).__init__()

    def get_network_type(self):

        return self.driver.network_connection

    def set_network_wifi(self):

        return self.driver.set_network_connection(2)

    def limit_network_data(self):

        return self.driver.set_network_connection(4)

if __name__ == '__main__':

    robot = Network()
    print(robot.get_network_type())