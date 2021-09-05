import json
import time
import logging

import requests

from selenium.webdriver import Chrome, ChromeOptions, Remote
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located as can_find
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException

def main():
    # read configs
    logging.info('read configs')
    with open('./botcfg.json') as f:
        configs = json.load(f)
    assert configs.get('region') is not None
    assert configs.get('phone') is not None
    assert configs.get('password') is not None
    assert configs.get('server_id') is not None
    assert configs.get('channel_name') is not None
    configs['selenium_additional_args'] = configs.get('selenium_additional_args') or []

    # launch Chrome
    logging.info('launch Chrome browser')
    options = ChromeOptions()
    for arg in configs.get('selenium_additional_args'):
        options.add_argument(arg)
    driver = Remote(command_executor='http://localhost:4444', options=options)

    try:
        start_stream(driver, configs)
    except Exception as e:
        raise e

    return driver

def start_stream(driver, configs):
    driver.get('https://www.kaiheila.cn')

    # set audio configs, must be in some html web page
    logging.info('set audio configs')
    set_audio_configs(driver, configs)

    # login
    logging.info('login into kaiheila server')
    make_login_requests(driver, configs)  # a faster way of login

    # join channel
    logging.info('enter the sound channel')
    channel_label_xpath = '//span[@title="{0}" and text()="{0}"]'.format(configs['channel_name'])
    channel_label = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath(channel_label_xpath))
    ActionChains(driver).double_click(channel_label).perform()

    # start to play music
    logging.info('start to play music')
    WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('//span[contains(@class, "connect-status")]/child::span[text()="语音已连接"]'))
    time.sleep(3)  # wait few secs until it is ready to accept key input
    ActionChains(driver).key_down(Keys.F2).perform()

    return driver  # return driver instance for console debugging

def make_login_requests(driver, configs):
    response = requests.post('https://www.kaiheila.cn/api/v2/auth/login', data={
        'mobile': configs['phone'],
        'mobile_prefix': configs['region'],
        'password': configs['password'],
        'remember': 'false'
    })
    for cookie in response.cookies:
        driver.add_cookie({
            'name': cookie.name,
            'value': cookie.value,
            'path': cookie.path,
            'domain': cookie.domain
        })
    driver.get('https://www.kaiheila.cn/app/channels/' + configs['server_id'])

def set_audio_configs(driver, configs):
    audio_configs = {
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
    driver.execute_script("localStorage.setItem('KAIHEI_AUDIO_CONFIG', '{}');".format(json.dumps(audio_configs)))
    logging.debug('audio configs is set to\n', driver.execute_script('return localStorage.getItem("KAIHEI_AUDIO_CONFIG");'))


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    driver = main()
    input('press any key to quit...')
    driver.quit()
