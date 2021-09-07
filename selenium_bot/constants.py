class Urls:
    SELENIUM_CMD_EXECUTOR = 'http://localhost:4444'
    KAIHEILA_HOME = 'https://www.kaiheila.cn'
    KAIHEILA_LOGIN = 'https://www.kaiheila.cn/api/v2/auth/login'
    KAIHEILA_SERVER_PATTERN = 'https://www.kaiheila.cn/app/channels/{}'


class XPaths:
    CHANNEL_LABEL_PATTERN = '//span[@title="{0}" and text()="{0}"]'
    VOICE_CONNECTED = '//span[contains(@class, "connect-status")]/child::span[text()="语音已连接"]'


class JScripts:
    SET_LOCALSTORAGE_PATTERN = "localStorage.setItem('KAIHEI_AUDIO_CONFIG', '{}');"
    GET_LOCALSTORAGE = 'return localStorage.getItem("KAIHEI_AUDIO_CONFIG");'
