import os


class BotConfigs:
    def __init__(self):
        self.phone_prefix = os.environ['BOT_PHONE_PREFIX']
        self.phone = os.environ['BOT_PHONE']
        self.password = os.environ['BOT_PASSWORD']
        self.server_id = os.environ['BOT_SERVER_ID']
        self.channel_name = os.environ['BOT_CHANNEL_NAME']
        self.selenium_additional_args = os.environ['BOT_SELENIUM_ADDITIONAL_ARGS']


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
