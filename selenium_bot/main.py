import json

from selenium.webdriver import Chrome, ChromeOptions
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
    assert configs.get('phone') is not None
    assert configs.get('password') is not None

    # launch Chrome
    options = ChromeOptions()
    for arg in configs.get('selenium_additional_args') or []:
        options.add_argument(arg)
    browser = Chrome(options=options)
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

if __name__ == '__main__':
    main()
    input('press any key to quit...')
