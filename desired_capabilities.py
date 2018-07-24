def _return_desired_capabilities(session_timeout=1000):

    desired_caps = {
        'platformName': 'Android',
        'platformVersion': '8.0.0',
        'deviceName': 'Nexus 5X',
        'app': 'c:\\selendroid-test-app.apk',
        'appActivity': '.HomeScreenActivity',
        'appPackage': 'io.selendroid.testapp',
        'noReset': True,
        'newCommandTimeout': session_timeout,
        'relaxedSecurity': True
    }

    return desired_caps


def list_desired_capabilities(key_value_to_return=None):

    if key_value_to_return is None:

        desired_caps_data = return_desired_capabilities()
        print('\nDesired Capabilities, Listing All Key=Value Structure')

        for key, value in zip(desired_caps_data.keys(), desired_caps_data.values()):

            print('Key: {}\nValue: {}\n'.format(key, value))

        return '\n'

    else:

        return return_desired_capabilities()


def caller_desired_capabilities(session_timeout=5000):

    desired_caps = {
        'platformName': 'Android',
        'platformVersion': '8.0.0',
        'deviceName': 'Nexus 5X',
        'app': 'c:\\selendroid-test-app.apk',
        'appActivity': '.HomeScreenActivity',
        'appPackage': 'io.selendroid.testapp',
        'noReset': True,
        'newCommandTimeout': session_timeout,
        'relaxedSecurity': True
    }

    return desired_caps


def return_desired_capabilities():

    desired_caps = {
        'platformName': 'Android',
        'platformVersion': '8.0.0',
        'deviceName': 'Nexus 5X',
        'browserName': 'Chrome',
        # 'app': 'c:\\nexar_app.apk',
        # 'appActivity': '.architecture.activities.MainActivity',
        # 'appPackage': 'mobi.nexar.dashcam',
        'noReset': True,
        'newCommandTimeout': 1000,
        'relaxedSecurity': True
    }

    return desired_caps
