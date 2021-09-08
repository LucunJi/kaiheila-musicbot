import json
import time
from logging import Logger, getLogger

import requests

from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from configs import BotConfigs, DEFAULT_AUDIO_CONFIGS, GeneralConfigs
from constants import Urls, XPaths, JScripts


logger: Logger = getLogger(__name__)


class SeleniumController:
    def __init__(self, botcfg: BotConfigs, gencfg: GeneralConfigs):
        """Creates a selenium session, set audio configurations and login."""
        self.config_bot: BotConfigs = botcfg
        self.config_general: GeneralConfigs = gencfg
        self.driver: WebDriver = self.launch_chrome()
        try:
            # audio configs and cookies must be set when it is in some http/https page
            self.driver.get(Urls.KAIHEILA_HOME)
            self.set_audio_configs()
            self.try_login()
        except Exception as e:
            self.driver.quit()
            raise e

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.quit()

    def launch_chrome(self) -> WebDriver:
        """Launches a Chrome session locally or remotely."""
        options = ChromeOptions()
        for a in self.config_general.selenium_additional_args.split(' '):
            options.add_argument(a)
        return Chrome(options=options)

    def set_audio_configs(self):
        """Sets bot's audio configs."""
        logger.info('set audio configs')
        audio_config_string = json.dumps(DEFAULT_AUDIO_CONFIGS)
        self.driver.execute_script(JScripts.SET_LOCALSTORAGE_PATTERN.format(audio_config_string))
        logger.debug('audio configs is set to\n' +
                     str(self.driver.execute_script(JScripts.GET_LOCALSTORAGE)))

    def try_login(self):
        """Tries to log into kaiheila, may fail and raise PermissionError."""
        logger.info('log into kaiheila server')
        response = requests.post(Urls.KAIHEILA_LOGIN, data={
            'mobile': self.config_bot.phone,
            'mobile_prefix': self.config_bot.phone_prefix,
            'password': self.config_bot.password,
            'remember': 'false'
        })
        if response.cookies.get('auth') is None:
            raise PermissionError(
                ('LOGIN FAILED! '
                 'PLEASE MANUALLY VERIFY IF YOUR ACCOUNT CAN BE USED NORMALLY WITHOUT CAPTCHA.'
                 '\nHeader: {}\nCookies: {}\nResponse: {}')
                .format(response.headers, response.cookies, response.text))
        for cookie in response.cookies:
            self.driver.add_cookie({
                'name': cookie.name,
                'value': cookie.value,
                'path': cookie.path,
                'domain': cookie.domain
            })

    def join_voice_channel(self):
        """Joins the voice channel and prepare for playing music."""
        logger.info('enter the server')
        self.driver.get(Urls.KAIHEILA_SERVER_PATTERN.format(self.config_bot.server_id))

        logger.info('wait for the page to finish loading...')
        channel_label_xpath = XPaths.CHANNEL_LABEL_PATTERN.format(self.config_bot.channel_name)
        channel_label = WebDriverWait(self.driver, 30).until(
            lambda x: x.find_element_by_xpath(channel_label_xpath))

        logger.info('join the voice channel')
        ActionChains(self.driver).double_click(channel_label).perform()

        logger.info('wait for the voice channel to finish loading...')
        WebDriverWait(self.driver, 30).until(
            lambda x: x.find_element_by_xpath(XPaths.VOICE_CONNECTED))
        time.sleep(3)  # wait few secs until it is ready to accept key input
        ActionChains(self.driver).key_down(Keys.F2).perform()
        logger.info('ready to play some music')

    def quit(self):
        """Quits and cleans up everything."""
        self.driver.quit()
