import os
import logging


class BotConfigs:
    def __init__(self):
        self.phone_prefix = os.environ['BOT_PHONE_PREFIX']
        self.phone = os.environ['BOT_PHONE']
        self.password = os.environ['BOT_PASSWORD']
        self.server_id = os.environ['BOT_SERVER_ID']
        self.channel_name = os.environ['BOT_CHANNEL_NAME']


class GeneralConfigs:
    def __init__(self):
        self.test_local_chrome_browser = \
            (os.environ.get('TEST_LOCAL_CHROME_BROWSER') or 'False').lower() == 'true'
        self.selenium_additional_args = os.environ['SELENIUM_ADDITIONAL_ARGS']
        self.log_level = logging.getLevelName(os.environ.get('LOG_LEVEL') or 'INFO')


DEFAULT_AUDIO_CONFIGS = {
    'selectedMicrophoneId': 'default',
    'selectedHeadphoneId': 'default',
    'inputVolume': 100,
    'outputVolume': 0,  # set to 0 to prevent echo
    'inputMode': 'keypress',
    'keypressDelay': 0,
    'openInputKey': [113],  # F2
    'closeInputKey': [],
    'quickMuteKey': [],
    'autoSens': True,
    'sensitivity': -90,
    'echoCancellation': False,  # set this to False to improve sound quality
    'noiseCancellation': False,  # set this to False to improve sound quality
    'soundGain': False,  # set this to False to improve sound quality
    'isInputMuted': False,
    'isMuted': False,
    'usersVolume': {},  # uid - volume pair(int)
    'overlay': True,
    'autoSelectDeviceShow': False,  # set to False to auto detect the default devices of your OS
    'lastConnectAudioInfo': {}
}

DEFAULT_LOG_FORMAT = 'Selenium Bot: %(asctime)s %(levelname)s %(name)s: %(message)s'
DEFAULT_LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'
