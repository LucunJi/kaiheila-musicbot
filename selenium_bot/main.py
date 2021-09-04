import json
import time

from selenium.webdriver import Chrome, ChromeOptions, Remote
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located as can_find
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException

def main():
    # read configs
    with open('./botcfg.json') as f:
        configs = json.load(f)
    assert configs.get('region') is not None  # TODO: actually make use of this prameter
    assert configs.get('phone') is not None
    assert configs.get('password') is not None
    assert configs.get('server_id') is not None
    assert configs.get('channel_name') is not None
    configs['selenium_additional_args'] = configs.get('selenium_additional_args') or []

    # launch Chrome
    options = ChromeOptions()
    for arg in configs.get('selenium_additional_args'):
        options.add_argument(arg)
    # browser = Chrome(options=options)
    browser = Remote(command_executor='http://localhost:4444', options=options)
    browser.get('https://www.kaiheila.cn/app/channels/' + configs['server_id'])

    # login
    WebDriverWait(browser, 10).until(lambda x: x.find_element_by_class_name('register-login-box'))
    phone_field = browser.find_element_by_xpath('//input[@placeholder="请输入你的手机号"][1]')
    ActionChains(browser).send_keys_to_element(phone_field, configs['phone']).perform()
    switch_login = browser.find_element_by_xpath('//div[text()="切换到密码登录"][1]')
    ActionChains(browser).click(switch_login).perform()
    password_field = browser.find_element_by_xpath('//input[@placeholder="请输入你的密码"][1]')
    ActionChains(browser).send_keys_to_element(password_field, configs['password']).perform()
    login_button = browser.find_element_by_xpath('//span[text()="登录"]/parent::button')
    ActionChains(browser).click(login_button).perform()

    # join channel
    channel_label_xpath = '//span[@title="{0}" and text()="{0}"]'.format(configs['channel_name'])
    channel_label = WebDriverWait(browser, 10).until(lambda x: x.find_element_by_xpath(channel_label_xpath))
    ActionChains(browser).double_click(channel_label).perform()

    # test sending text message -- for text channel only
#    message_editor = WebDriverWait(browser, 10).until(lambda x: x.find_element_by_class_name('richeditor-placeholders'))
#    test_msg = 'test message from selenium_bot' + Keys.ENTER
#    ActionChains(browser).click(message_editor).send_keys(test_msg).perform()

    # start to play music
    WebDriverWait(browser, 10).until(lambda x: x.find_element_by_xpath('//span[contains(@class, "connect-status")]/child::span'))
    confirm_btn = WebDriverWait(browser, 3).until(lambda x: x.find_element_by_xpath('//span[@title="需要按键说话" and text()="需要按键说话"]/parent::*/parent::*/descendant::button'))
    time.sleep(1)  # wait 1 sec for animation
    ActionChains(browser).click(confirm_btn).perform()
    ActionChains(browser).key_down(Keys.F2).perform()

    return browser  # return browser instance for console debugging

if __name__ == '__main__':
    browser = main()
    input('press any key to quit...')
    browser.quit()
