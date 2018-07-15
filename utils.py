from time import sleep
from appium import webdriver


class Robot(object):

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

    def suicide(self):

        self.driver.stop_client()
        print('robot suicide')
        self.driver.quit()


class Network(Robot):

    def __init__(self):

        print('robot digging inside toolbox\n')
        super(Network, self).__init__()

    def get_network_type(self):

        print('robot getting network type\n')
        return self.driver.network_connection

    def set_network_wifi(self):

        print('robot change network to wifi\n')
        return self.driver.set_network_connection(2)

    def limit_network_data(self):

        print('robot limit network to data only\n'.format())
        return self.driver.set_network_connection(4)


class GPS(Robot):

    def __init__(self):

        super(GPS, self).__init__()

    def set_gps(self, alt, lat, lon):

        return self.driver.set_location(altitude=alt, latitude=lat, longitude=lon)

    def get_gps(self):

        return self.driver.close_app()


if __name__ == '__main__':

    robot = Network()
    # robot = GPS()

    # test_run = [robot.get_network_type(), robot.set_network_wifi(), robot.limit_network_data()]
    # test_run = [robot.set_gps(10, 10, 10), robot.get_gps()]

    try:

        robot.set_network_wifi()

    except Exception as e:

        raise e

    robot.suicide()
