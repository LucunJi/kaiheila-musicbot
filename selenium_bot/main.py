import json
import time
import logging
from signal import signal, SIGINT
from sys import exit

import requests
from selenium.webdriver.remote.webdriver import WebDriver

from urllib3.exceptions import MaxRetryError

from selenium.webdriver import ChromeOptions, Remote, Chrome
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from configs import BotConfigs, DEFAULT_AUDIO_CONFIGS, GeneralConfigs
from constants import Urls, XPaths, JScripts


def main():
    # read configs
    logging.info('read configs')
    general_configs = GeneralConfigs()
    logging.getLogger().setLevel(general_configs.log_level)
    bot_configs = BotConfigs()

    logging.info('launch Chrome browser')
    bot_driver = launch_chrome(general_configs)

    signal(SIGINT, lambda signal_received, frame: on_sigint(bot_driver))

    try:
        start_stream(bot_driver, bot_configs)
        while True:
            time.sleep(10)
            # a random command to prevent the session from deleted
            bot_driver.find_element_by_tag_name('body')
    except Exception as e:
        bot_driver.quit()
        raise e

    return bot_driver


def launch_chrome(configs: GeneralConfigs) -> WebDriver:
    options = ChromeOptions()
    for a in configs.selenium_additional_args.split(' '):
        options.add_argument(a)
    if configs.test_local_chrome_browser:
        bot_driver = Chrome(options=options)
    else:
        while True:
            try:
                bot_driver = Remote(command_executor=Urls.SELENIUM_CMD_EXECUTOR, options=options)
            except MaxRetryError:
                logging.debug(
                    'cannot connect to remote selenium server, maybe it is not ready yet, '
                    'retrying...')
                time.sleep(3)
            else:
                break
    return bot_driver


def start_stream(bot_driver: WebDriver, configs: BotConfigs):
    bot_driver.get(Urls.KAIHEILA_HOME)

    # set audio configs, must be in some html web page
    logging.info('set audio configs')
    set_audio_configs(bot_driver, configs)

    logging.info('login into kaiheila server')
    try_login(bot_driver, configs)

    logging.info('enter the sound channel')
    bot_driver.get(configs.voice_channel_link)

    logging.info('wait for page to finish loading...')
    WebDriverWait(bot_driver, 30).until(lambda x: x.find_element_by_xpath(XPaths.VOICE_CONNECTED))
    time.sleep(3)  # wait few secs until it is ready to accept key input
    ActionChains(bot_driver).key_down(Keys.F2).perform()
    logging.info('ready to play some music')

    return bot_driver  # return driver instance for console debugging


def try_login(bot_driver: WebDriver, configs: BotConfigs):
    response = requests.post(Urls.KAIHEILA_LOGIN, data={
        'mobile': configs.phone,
        'mobile_prefix': configs.phone_prefix,
        'password': configs.password,
        'remember': 'false'
    })
    if response.cookies.get('auth') is None:
        raise PermissionError(
            ('LOGIN FAILED! '
             'PLEASE MANUALLY VERIFY IF YOUR ACCOUNT CAN BE USED NORMALLY WITHOUT CAPTCHA.'
             '\nHeader: {}\nCookies: {}\nResponse: {}')
            .format(response.headers, response.cookies, response.text))
    for cookie in response.cookies:
        bot_driver.add_cookie({
            'name': cookie.name,
            'value': cookie.value,
            'path': cookie.path,
            'domain': cookie.domain
        })


def set_audio_configs(bot_driver: WebDriver, configs: BotConfigs):
    audio_config_string = json.dumps(DEFAULT_AUDIO_CONFIGS)
    bot_driver.execute_script(JScripts.SET_LOCALSTORAGE_PATTERN.format(audio_config_string))
    logging.debug('audio configs is set to\n' +
                  str(bot_driver.execute_script(JScripts.GET_LOCALSTORAGE)))


def on_sigint(bot_driver: WebDriver):
    logging.info('received signal SIGINT, exit...')
    bot_driver.quit()
    exit(1)


if __name__ == '__main__':
    driver = main()
    input('press any key to quit...')
    driver.quit()
