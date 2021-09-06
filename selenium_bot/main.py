import json
import time
import logging
from signal import signal, SIGINT
from sys import exit

import requests

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

    # launch Chrome
    logging.info('launch Chrome browser')
    options = ChromeOptions()
    for a in bot_configs.selenium_additional_args.split(' '):
        options.add_argument(a)
    if general_configs.test_local_chrome_browser:
        driver = Chrome(options=options)
    else:
        while True:
            try:
                driver = Remote(command_executor='http://localhost:4444', options=options)
            except MaxRetryError:
                logging.debug('cannot connect to remote selenium server, maybe it is not ready yet, retrying...')
                time.sleep(3)
            else:
                break

    signal(SIGINT, lambda signal_received, frame: on_sigint(driver))

    try:
        start_stream(driver, bot_configs)
        while True:
            time.sleep(10)
            # a random command to prevent the session from deleted
            driver.find_element_by_tag_name('body')
    except Exception as e:
        driver.quit()
        raise e

    return driver


def start_stream(driver, configs):
    driver.get(Urls.KAIHEILA_HOME)

    # set audio configs, must be in some html web page
    logging.info('set audio configs')
    set_audio_configs(driver, configs)

    # login
    logging.info('login into kaiheila server')
    make_login_requests(driver, configs)  # a faster way of login

    # join channel
    logging.info('enter the sound channel')
    channel_label_xpath = XPaths.CHANNEL_LABEL_PATTERN.format(configs.channel_name)
    channel_label = WebDriverWait(driver, 30).until(
        lambda x: x.find_element_by_xpath(channel_label_xpath))
    ActionChains(driver).double_click(channel_label).perform()

    # start to play music
    logging.info('start to play music')
    WebDriverWait(driver, 30).until(lambda x: x.find_element_by_xpath(XPaths.VOICE_CONNECTED))
    time.sleep(3)  # wait few secs until it is ready to accept key input
    ActionChains(driver).key_down(Keys.F2).perform()

    return driver  # return driver instance for console debugging


def make_login_requests(driver, configs):
    response = requests.post(Urls.KAIHEILA_LOGIN, data={
        'mobile': configs.phone,
        'mobile_prefix': configs.phone_prefix,
        'password': configs.password,
        'remember': 'false'
    })
    if response.cookies.get('auth') is None:
        raise PermissionError(
            'LOGIN FAILED! '
            'PLEASE MANUALLY VERIFY IF YOUR ACCOUNT CAN BE USED NORMALLY WITHOUT CAPTCHA.')
    for cookie in response.cookies:
        driver.add_cookie({
            'name': cookie.name,
            'value': cookie.value,
            'path': cookie.path,
            'domain': cookie.domain
        })
    driver.get(Urls.KAIHEILA_SERVER_PATTERN.format(configs.server_id))


def set_audio_configs(driver, configs):
    audio_config_string = json.dumps(DEFAULT_AUDIO_CONFIGS)
    driver.execute_script(JScripts.SET_LOCALSTORAGE_PATTERN.format(audio_config_string))
    logging.debug('audio configs is set to\n' +
                  str(driver.execute_script(JScripts.GET_LOCALSTORAGE)))


def on_sigint(driver):
    logging.info('received signal SIGINT, exit...')
    driver.quit()
    exit(1)


if __name__ == '__main__':
    driver = main()
    input('press any key to quit...')
    driver.quit()
