import json


class BotConfigs:
    def __init__(self):
        with open('./botcfg.json') as f:
            configs = json.load(f)
        self.region = configs['region']
        self.phone = configs['phone']
        self.password = configs['password']
        self.server_id = configs['server_id']
        self.channel_name = configs['channel_name']
        self.selenium_additional_args = configs['selenium_additional_args']


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
