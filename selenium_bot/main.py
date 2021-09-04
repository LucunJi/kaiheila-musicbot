import json
import time

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
    print('read configs')
    with open('./botcfg.json') as f:
        configs = json.load(f)
    assert configs.get('region') is not None
    assert configs.get('phone') is not None
    assert configs.get('password') is not None
    assert configs.get('server_id') is not None
    assert configs.get('channel_name') is not None
    configs['selenium_additional_args'] = configs.get('selenium_additional_args') or []

    # launch Chrome
    print('launch Chrome browser')
    options = ChromeOptions()
    for arg in configs.get('selenium_additional_args'):
        options.add_argument(arg)
    driver = Chrome(options=options)
    # driver = Remote(command_executor='http://localhost:4444', options=options)

    # login
    print('log into kaiheila server')
    # selenium_login(driver, configs)
    requests_login(driver, configs)  # a faster way of login

    # join channel
    print('enter the sound channel')
    channel_label_xpath = '//span[@title="{0}" and text()="{0}"]'.format(configs['channel_name'])
    channel_label = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath(channel_label_xpath))
    ActionChains(driver).double_click(channel_label).perform()

    # test sending text message -- for text channel only
#    message_editor = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_class_name('richeditor-placeholders'))
#    test_msg = 'test message from selenium_bot' + Keys.ENTER
#    ActionChains(driver).click(message_editor).send_keys(test_msg).perform()

    # start to play music
    print('start to play music')
    WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('//span[contains(@class, "connect-status")]/child::span'))
    confirm_btn = WebDriverWait(driver, 3).until(lambda x: x.find_element_by_xpath('//span[@title="需要按键说话" and text()="需要按键说话"]/parent::*/parent::*/descendant::button'))
    time.sleep(1)  # wait 1 sec for animation
    ActionChains(driver).click(confirm_btn).perform()
    ActionChains(driver).key_down(Keys.F2).perform()

    return driver  # return driver instance for console debugging

def selenium_login(driver, configs):
    driver.get('https://www.kaiheila.cn/app/passwordlogin?redir=%2Fchannels%2F' + configs['server_id'])
    region_field = driver.find_element_by_xpath('//div[contains(@class, "select-country-container")]/preceding::a[1]')
    ActionChains(driver).click(region_field).perform()
    # WebDriverWait(driver, 10).until(lambda x: x.find_element_by_class_name('register-login-box'))
    WebDriverWait(driver, 10).until(lambda x: x.find_element_by_class_name('login-box'))
    plus_region = '+' + configs['region']
    region_button_xpath = '//div[contains(@class, "country-list")]/child::div[substring(text(), string-length(text())-{0})="{1}"][1]'.format(len(plus_region) - 1, plus_region)
    region_button = driver.find_element_by_xpath(region_button_xpath)
    ActionChains(driver).click(region_button).perform()
    phone_field = driver.find_element_by_xpath('//input[@placeholder="请输入你的手机号"][1]')
    ActionChains(driver).send_keys_to_element(phone_field, configs['phone']).perform()
    # switch_login = driver.find_element_by_xpath('//div[text()="切换到密码登录"][1]')
    # ActionChains(driver).click(switch_login).perform()
    password_field = driver.find_element_by_xpath('//input[@placeholder="请输入你的密码"][1]')
    ActionChains(driver).send_keys_to_element(password_field, configs['password']).perform()
    login_button = driver.find_element_by_xpath('//span[text()="登录"]/parent::button')
    ActionChains(driver).click(login_button).perform()

def requests_login(driver, configs):
    response = requests.post('https://www.kaiheila.cn/api/v2/auth/login', data={
        'mobile': configs['phone'],
        'mobile_prefix': configs['region'],
        'password': configs['password'],
        'remember': 'false'
    })
    driver.get('https://www.kaiheila.cn')
    for cookie in response.cookies:
        driver.add_cookie({
            'name': cookie.name,
            'value': cookie.value,
            'path': cookie.path,
            'domain': cookie.domain
        })
    driver.get('https://www.kaiheila.cn/app/channels/' + configs['server_id'])

if __name__ == '__main__':
    driver = main()
    input('press any key to quit...')
    driver.quit()
