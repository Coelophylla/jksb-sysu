import os, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from util import get_img
from retrying import retry
import ddddocr
import logging

# 失败后随机 1-3s 后重试，最多 10 次
@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=10)
def initDriver():
    profile = webdriver.FirefoxProfile()
    profile.set_preference('intl.accept_languages', 'zh-CN, zh') #'zh-CN, zh','en-US, en'
    ## replace desired_domain.com below with whitelisted domain. Separate domains by comma.
    profile.set_preference("network.proxy.no_proxies_on","localhost,127.0.0.1,*sysu.edu.cn")
    profile.set_preference("network.proxy.backup.ssl","0.0.0.0")
    profile.set_preference("network.proxy.backup.ssl_port",1)
    profile.set_preference("network.proxy.http","0.0.0.0")
    profile.set_preference("network.proxy.http_port",1)
    profile.set_preference("network.proxy.ssl","0.0.0.0")
    profile.set_preference("network.proxy.ssl_port",1)
    profile.set_preference("network.proxy.type",1)
    profile.set_preference("network.proxy.share_proxy_settings",True)

    try:
        driver = webdriver.Firefox(executable_path=f'{os.getcwd()}/geckodriver.exe', firefox_profile=profile, )
    except:
        logging.error("webdriver初始化失败")
        raise Exception('webdriver初始化失败')
    else:
        #设置超时时间为30s
        driver.set_script_timeout(30)
        logging.info("初始化selenium driver完成")

        return driver


# 失败后随机 1-3s 后重试，最多 10 次
@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=10)
def login(driver,ocr):
    logging.info("访问登录页面")
    driver.get("https://cas.sysu.edu.cn/cas/login")

    logging.info("读取用户名密码")
    try:
        netid = os.environ['NETID']
        password = os.environ['PASSWORD']
    except:
        logging.error("读取用户名密码失败，请检查Github Actions的secrets是否正确输入")
        raise Exception('读取用户名密码失败')

    logging.info("输入用户名密码")
    driver.find_element_by_xpath('//*[@id="username"]').send_keys(netid)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)

    # 识别验证码
    code = get_img(ocr,driver)
    logging.info("输入验证码")
    driver.find_element_by_xpath('//*[@id="captcha"]').send_keys(code)

    # 点击登录按钮
    logging.info("点击登录按钮")
    driver.find_element_by_xpath('//*[@id="fm1"]/section[2]/input[4]').click()
    try:
        logging.info(driver.find_element_by_xpath('//*[@id="cas"]/div/div[1]/div/div/h2').text)
    except:
        logging.error(driver.find_element_by_xpath('//*[@id="fm1"]/div[1]/span').text)
        raise Exception('登陆失败')

# 失败后随机 3-5s 后重试，最多 10 次
@retry(wait_random_min=3000, wait_random_max=5000, stop_max_attempt_number=10)
def jksb(driver):
    logging.info('访问健康申报页面')
    driver.get("http://jksb.sysu.edu.cn/infoplus/form/XNYQSB/start")
    wait = WebDriverWait(driver, 30) # timeout in seconds -> 30

    try:
        wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//*[@id='form_command_bar']/li[1]")) )
        logging.info('打开健康申报成功')
    except:
        logging.error('打开健康申报失败')
        raise Exception('打开健康申报失败')

    logging.info("点击下一步")
    driver.find_element_by_xpath('//*[@id="form_command_bar"]/li[1]').click()

    wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//*[@id='form_command_bar']/li[2]")) ) # 出现终止按钮

    logging.info("出现终止按钮，先睡一会")
    time.sleep(5)
    logging.info("醒了，看看下一步能不能点了")
    wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//*[@id='form_command_bar']/li[1]")) ) # 等下一步能点
    logging.info("可以咯，提交健康申报")

    driver.find_element_by_xpath('//*[@id="form_command_bar"]/li[1]').click()

    result=""
    try:
        wait.until(expected_conditions.text_to_be_present_in_element
                   ((By.XPATH, '//div[8]/div/div[1]/div[2]'), "办理成功!"))
        result = driver.find_element_by_xpath('//div[8]/div/div[1]/div[2]').text
        logging.info("完成健康申报")
    except:
        logging.error("办理健康申报失败")
        logging.error(driver.find_element_by_xpath('//div[8]').text)
        raise Exception('办理健康申报失败')

    return result

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,format='[%(levelname)s] %(asctime)s %(message)s')

    driver=initDriver()
    ocr = ddddocr.DdddOcr()
    logging.info("初始化ddddocr完成")

    login(driver,ocr)
    jksb(driver)
    driver.quit()

