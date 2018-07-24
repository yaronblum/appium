import json
import unittest
import subprocess
import uiautomator
from time import sleep
from requests import get
import desired_capabilities
from appium import webdriver
from msvcrt import getch as wait_key
from sys import argv as script_params
from appium.webdriver.common.touch_action import TouchAction


class Robot(object):

    def __init__(self, host_address='127.0.0.2', server_port='4724'):

        self.host_address = host_address
        self.server_port = server_port
        self.status_code = self.request_status_from_server
        self.server = self.appium_server()

        try:

            self.driver = self.init_session()

        except Exception as init_error:

            raise init_error

        print('\nrobot is now one with remote webdriver'
              '\n--------------------------------------')
        for i, j in zip(self.driver.desired_capabilities.keys(),
                        self.driver.desired_capabilities.values()):
            print('robot => {} = {}'.format(i, j))

        print('\n')

    def suicide(self):

        print('\nrobot suicide')
        self.driver.quit()

    def appium_server(self):

        status_code = self.status_code()
        if status_code is not 200:

            try:

                subprocess.run(["start", "appium",
                                "--address", self.host_address,
                                "--port", self.server_port,
                                "--relaxed-security", "--log-timestamp"],
                               shell=True, timeout=5)

            except Exception as process_err:

                raise process_err
        else:

            print('seems remote server is already running\nresume..')

    def init_session(self):

        status_code = self.status_code()
        timeout = 0

        print('\nrobot attempt to initiate session with device..')
        print('waiting until status code is 200..')
        print('robot says current server status code is {}'.format(status_code))

        if status_code is not 200:

            while status_code is not 200:

                if timeout < 60:
                    print('connection attempts: {} out 5\n'.format(timeout))
                    sleep(1.5)
                    status_code = self.status_code()

                else:
                    print('\nrobot reached timeout, error while initiating session\nterminate process')
                    exit(code=666)
                timeout += 1

        return webdriver.Remote('http://{}:{}/wd/hub'.format(self.host_address,
                                                             self.server_port),
                                desired_capabilities.return_desired_capabilities())

    def request_status_from_server(self):

        try:

            res = get("http://{}:{}/wd/hub/status".format(self.host_address, self.server_port))
            return int(res.status_code)

        except Exception as e:

            if e:
                pass
            return 400

    @staticmethod
    def hold_app():

        sleep(1000)


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

    def toggle_location(self):

        return self.driver.toggle_location_services()

    @property
    def get_gps(self):

        gps_results = self.driver.execute_script('mobile: shell', {
            'command': 'dumpsys',
            'args': ['location',
                     "| grep 'gps: Location'"],
            'includeStderr': True,
            'timeout': 5000
        })

        return gps_results['stdout']


class AppService(Robot):

    def __init__(self):

        print('initiating robot app service utils')
        super(AppService, self).__init__()

    def launch_self_app(self):

        print('robot should try launch the app')

        try:

            return self.driver.launch_app()

        except Exception as launch_err:

            raise launch_err

    def uninstall_app(self):

        try:

            self.driver.remove_app(desired_capabilities.list_desired_capabilities('appPackage'))

        except NameError as err:

            raise err

    @property
    def return_current_active(self):

        return self.driver.current_activity

    @property
    def return_current_package(self):

        return self.driver.current_package

    @property
    def return_current_window_handler(self):

        return self.driver.current_window_handle


class Device(Robot):

    def __init__(self):

        super(Device, self).__init__()

    def restart(self, timeout=40):

        print('robot is going to restart device')
        if timeout == 40:

            print('default timeout values detected\n'
                  'robot will wait {} till re-initiating driver-session')

        else:

            print('robot detected custom timeout values for restart,\n'
                  'robot will wait {} seconds'.format(timeout))

        self.driver.execute_script('mobile: shell', {
            'command': 'reboot',
            'includeStderr': True,
            'timeout': 5000
        })

        sleep(timeout)
        print('robot reached timeout, passed {} seconds\n'.format(timeout))
        self.__init__()

    def press_home_button(self):

        return self.driver.press_keycode(3)

    def press_menu_button(self):

        return self.driver.press_keycode(82)

    def press_recent_apps(self):

        return self.driver.press_keycode(182)

    def press_app_switch(self):

        return self.driver.press_keycode(187)

    @property
    def return_window_dimensions(self):

        return self.driver.get_window_size(windowHandle='current').values()

    def swipe_from_center(self, time_duration_milliseconds=2000):

        x, y = self.return_window_dimensions()
        y_start_point = int(y / 2)
        y_end_point = int(y / 2)
        x_start_point = int(x / 2)
        print('ystart:{} yend: {} xstart:{}'.format(y_start_point, y_end_point, x_start_point))
        print('let us swipe')
        return exit()

        # return self.driver.swipe(x_start_point, y_start_point, y_end_point, time_duration_milliseconds)

    def flick(self, start_x, start_y, end_x, end_y):
        """Flick from one point to another point.
        :Args:
         - start_x - x-coordinate at which to start
         - start_y - y-coordinate at which to start
         - end_x - x-coordinate at which to stop
         - end_y - y-coordinate at which to stop
        :Usage:
            driver.flick(100, 100, 100, 400)
        """
        action = TouchAction()
        action.press(x=start_x, y=start_y).move_to(x=end_x, y=end_y).release()
        action.perform()

        return self


class Visual(Robot):

    def __init__(self):

        print('robot trying to open visual toolbox, stay tuned..')
        super(Visual, self).__init__()
        print('robot successfully cracked the toolbox')

    def return_base64_printscreen(self):

        return self.driver.get_screenshot_as_base64()

    def get_current_screen_as_base64(self):

        print('\nrobot detected current activity as {}..\n'.format(self.driver.current_activity))
        subject_printscreen = self.driver.get_screenshot_as_base64()
        compare_printscreen = self.driver.get_screenshot_as_base64()

        if subject_printscreen and compare_printscreen is not None:
            try:

                return [subject_printscreen, compare_printscreen]

            except Exception as e:

                raise e

    def start_video_recording(self):

        try:
            print('robot start recording video')

            print(self.driver.current_package)
            return wait_key()

        except Exception as err:

            try:
                print('robot sense keyboard interrupt\n'
                      'attempting to stop video')
                # self.driver.stop_recording_screen()

            except Exception as video_err:

                print('robot unable to stop the video')
                raise video_err

            raise err


class Runner(unittest.TestCase):

    def setUp(self):

        self.driver = Visual()

    def tearDown(self):

        self.driver.suicide()

    def test_compare_pictures(self, subject, compare_to):

        self.skipTest('\n!!!no need to run test!!!\n')

        print('robot detected base64 encoded images')
        print('robot => subject image character length: {}'.format(len(subject)))
        print('robot => compare_to image character length: {}'.format(len(compare_to)))

        extract_items = [i for i in self.driver.get_current_screen_as_base64()]
        return self.assertEqual(first=extract_items[0], second=extract_items[0])

    # before each test case attempt to build function
    # should return all function name and set it in a loop
    def test_get_class_methods(self):

        print([method_name for method_name in dir(self.driver)
               if callable(getattr(self.driver, method_name))])

        # print(dir(self.driver))


class Caller(Robot):

    def __init__(self):

        super(Caller, self).__init__()
        self.u2 = uiautomator.Selector()
        self.gps = GPS().get_gps()

    def launch_phone_app(self):

        try:

            self.driver.start_activity(app_package='com.google.android.dialer',
                                       app_activity='.extensions.GoogleDialtactsActivity')

        except Exception as error:

            raise error

    def return_clickable_elements(self):

        elements = self.driver.find_elements_by_android_uiautomator('new UiSelector().clickable(true)')

        for element in elements:
            print('{}\n'.format(element))

        return None

    def return_all_elements_by_xpath(self):

        elements = self.driver.find_elements_by_xpath("//*[not(*)]")
        for element in elements:

            if element.id == 9:

                element.click()


class UI2(Robot):

    def __init__(self):

        super(UI2, self).__init__()
        self.u2 = uiautomator


class Nexar(Robot):

    def __init__(self):

        super(Nexar, self).__init__()
        self.return_elements()

    def return_elements(self):

        elements = self.driver.find_elements_by_xpath("//*[not(*)]")

        print(elements)

        return len(elements)


class WebDriver(webdriver.Remote):

    def __init__(self):

        pass

    def _addCommands(self):

        self.command_executor._commands[Command.CONTEXTS] = \
            ('GET', '/session/$sessionId/contexts')
        self.command_executor._commands[Command.GET_CURRENT_CONTEXT] = \
            ('GET', '/session/$sessionId/context')
        self.command_executor._commands[Command.SWITCH_TO_CONTEXT] = \
            ('POST', '/session/$sessionId/context')
        self.command_executor._commands[Command.TOUCH_ACTION] = \
            ('POST', '/session/$sessionId/touch/perform')
        self.command_executor._commands[Command.MULTI_ACTION] = \
            ('POST', '/session/$sessionId/touch/multi/perform')
        self.command_executor._commands[Command.GET_APP_STRINGS] = \
            ('POST', '/session/$sessionId/appium/app/strings')
        # Needed for Selendroid
        self.command_executor._commands[Command.KEY_EVENT] = \
            ('POST', '/session/$sessionId/appium/device/keyevent')
        self.command_executor._commands[Command.PRESS_KEYCODE] = \
            ('POST', '/session/$sessionId/appium/device/press_keycode')
        self.command_executor._commands[Command.LONG_PRESS_KEYCODE] = \
            ('POST', '/session/$sessionId/appium/device/long_press_keycode')
        self.command_executor._commands[Command.GET_CURRENT_ACTIVITY] = \
            ('GET', '/session/$sessionId/appium/device/current_activity')
        self.command_executor._commands[Command.GET_CURRENT_PACKAGE] = \
            ('GET', '/session/$sessionId/appium/device/current_package')
        self.command_executor._commands[Command.SET_IMMEDIATE_VALUE] = \
            ('POST', '/session/$sessionId/appium/element/$id/value')
        self.command_executor._commands[Command.PULL_FILE] = \
            ('POST', '/session/$sessionId/appium/device/pull_file')
        self.command_executor._commands[Command.PULL_FOLDER] = \
            ('POST', '/session/$sessionId/appium/device/pull_folder')
        self.command_executor._commands[Command.PUSH_FILE] = \
            ('POST', '/session/$sessionId/appium/device/push_file')
        self.command_executor._commands[Command.BACKGROUND] = \
            ('POST', '/session/$sessionId/appium/app/background')
        self.command_executor._commands[Command.IS_APP_INSTALLED] = \
            ('POST', '/session/$sessionId/appium/device/app_installed')
        self.command_executor._commands[Command.INSTALL_APP] = \
            ('POST', '/session/$sessionId/appium/device/install_app')
        self.command_executor._commands[Command.REMOVE_APP] = \
            ('POST', '/session/$sessionId/appium/device/remove_app')
        self.command_executor._commands[Command.TERMINATE_APP] = \
            ('POST', '/session/$sessionId/appium/device/terminate_app')
        self.command_executor._commands[Command.ACTIVATE_APP] = \
            ('POST', '/session/$sessionId/appium/device/activate_app')
        self.command_executor._commands[Command.QUERY_APP_STATE] = \
            ('POST', '/session/$sessionId/appium/device/app_state')
        self.command_executor._commands[Command.START_ACTIVITY] = \
            ('POST', '/session/$sessionId/appium/device/start_activity')
        self.command_executor._commands[Command.LAUNCH_APP] = \
            ('POST', '/session/$sessionId/appium/app/launch')
        self.command_executor._commands[Command.CLOSE_APP] = \
            ('POST', '/session/$sessionId/appium/app/close')
        self.command_executor._commands[Command.END_TEST_COVERAGE] = \
            ('POST', '/session/$sessionId/appium/app/end_test_coverage')
        self.command_executor._commands[Command.LOCK] = \
            ('POST', '/session/$sessionId/appium/device/lock')
        self.command_executor._commands[Command.UNLOCK] = \
            ('POST', '/session/$sessionId/appium/device/unlock')
        self.command_executor._commands[Command.IS_LOCKED] = \
            ('POST', '/session/$sessionId/appium/device/is_locked')
        self.command_executor._commands[Command.SHAKE] = \
            ('POST', '/session/$sessionId/appium/device/shake')
        self.command_executor._commands[Command.TOUCH_ID] = \
            ('POST', '/session/$sessionId/appium/simulator/touch_id')
        self.command_executor._commands[Command.TOGGLE_TOUCH_ID_ENROLLMENT] = \
            ('POST', '/session/$sessionId/appium/simulator/toggle_touch_id_enrollment')
        self.command_executor._commands[Command.RESET] = \
            ('POST', '/session/$sessionId/appium/app/reset')
        self.command_executor._commands[Command.HIDE_KEYBOARD] = \
            ('POST', '/session/$sessionId/appium/device/hide_keyboard')
        self.command_executor._commands[Command.IS_KEYBOARD_SHOWN] = \
            ('GET', '/session/$sessionId/appium/device/is_keyboard_shown')
        self.command_executor._commands[Command.OPEN_NOTIFICATIONS] = \
            ('POST', '/session/$sessionId/appium/device/open_notifications')
        self.command_executor._commands[Command.GET_NETWORK_CONNECTION] = \
            ('GET', '/session/$sessionId/network_connection')
        self.command_executor._commands[Command.SET_NETWORK_CONNECTION] = \
            ('POST', '/session/$sessionId/network_connection')
        self.command_executor._commands[Command.GET_AVAILABLE_IME_ENGINES] = \
            ('GET', '/session/$sessionId/ime/available_engines')
        self.command_executor._commands[Command.IS_IME_ACTIVE] = \
            ('GET', '/session/$sessionId/ime/activated')
        self.command_executor._commands[Command.ACTIVATE_IME_ENGINE] = \
            ('POST', '/session/$sessionId/ime/activate')
        self.command_executor._commands[Command.DEACTIVATE_IME_ENGINE] = \
            ('POST', '/session/$sessionId/ime/deactivate')
        self.command_executor._commands[Command.GET_ACTIVE_IME_ENGINE] = \
            ('GET', '/session/$sessionId/ime/active_engine')
        self.command_executor._commands[Command.REPLACE_KEYS] = \
            ('POST', '/session/$sessionId/appium/element/$id/replace_value')
        self.command_executor._commands[Command.GET_SETTINGS] = \
            ('GET', '/session/$sessionId/appium/settings')
        self.command_executor._commands[Command.UPDATE_SETTINGS] = \
            ('POST', '/session/$sessionId/appium/settings')
        self.command_executor._commands[Command.TOGGLE_LOCATION_SERVICES] = \
            ('POST', '/session/$sessionId/appium/device/toggle_location_services')
        self.command_executor._commands[Command.SET_LOCATION] = \
            ('POST', '/session/$sessionId/location')
        self.command_executor._commands[Command.LOCATION_IN_VIEW] = \
            ('GET', '/session/$sessionId/element/$id/location_in_view')
        self.command_executor._commands[Command.GET_DEVICE_TIME] = \
            ('GET', '/session/$sessionId/appium/device/system_time')
        self.command_executor._commands[Command.CLEAR] = \
            ('POST', '/session/$sessionId/element/$id/clear')
        self.command_executor._commands[Command.START_RECORDING_SCREEN] = \
            ('POST', '/session/$sessionId/appium/start_recording_screen')
        self.command_executor._commands[Command.STOP_RECORDING_SCREEN] = \
            ('POST', '/session/$sessionId/appium/stop_recording_screen')
        self.command_executor._commands[Command.SET_CLIPBOARD] = \
            ('POST', '/session/$sessionId/appium/device/set_clipboard')
        self.command_executor._commands[Command.GET_CLIPBOARD] = \
            ('POST', '/session/$sessionId/appium/device/get_clipboard')
        self.command_executor._commands[Command.COMPARE_IMAGES] = \
            ('POST', '/session/$sessionId/appium/compare_images')


if __name__ == '__main__':

    if len(script_params) > 1:

        print('robot will born with the following user params: \n{}'
              .format(str(script_params)))

    else:

        print('\n!!!robot is normal, no user params were provided!!!')
        pass

    robot = Robot()
    robot.hold_app()

    # test_run = [robot.get_network_type(), robot.set_network_wifi(), robot.limit_network_data()]
    # test_run = [robot.set_gps(10, 10, 10), robot.get_gps()]
    # test_run = [robotGps.set_gps(30, 6, 666), robotGps.get_gps()]
