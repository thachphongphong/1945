from appium.webdriver.common.touch_action import TouchAction
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
import base64
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from multiprocessing.pool import ThreadPool
from threading import active_count
from time import sleep
from concurrent.futures import ThreadPoolExecutor
import schedule
import threading
import json

with open('settings.json') as f:
    desired_caps = json.load(f)

driver = webdriver.Remote(
    command_executor="http://127.0.0.1:4723",
    desired_capabilities=desired_caps
)

driver.update_settings({"getMatchedImageResult": True})
# driver.implicitly_wait(10)

with open(r"ads.png", "rb") as image_file:
    ads = base64.b64encode(image_file.read()).decode("utf-8")

with open(r"ads_done.png", "rb") as image_file:
    ads_done = base64.b64encode(image_file.read()).decode("utf-8")

with open(r"x1.png", "rb") as image_file:
    x1 = base64.b64encode(image_file.read()).decode("utf-8")


def is_display(v):
    try:
        element = driver.find_element(by=AppiumBy.IMAGE, value=v)
        return element.is_displayed()
    except NoSuchElementException:
        print('Element Not found !!!')
        return False
    
def next_display():
    try:
        e_x = driver.find_element(by=AppiumBy.IMAGE, value=x1)
        if(e_x.is_displayed()):    
            e_x.click()
    except Exception:
        print('X Not found !!!')

x_i = 1
def close_ads():
    global x_i  # Declare skill_i as a global variable
    try:
        value = None  # Initialize value
        if x_i == 1:
            value = x1
        if value is not None:                                                                            
            e_x = driver.find_element(by=AppiumBy.IMAGE, value=value)
            e_x.click()
    except Exception:
        # Toggle between skill 1 and skill 4
        if x_i < 2: x_i = x_i + 1
        else: x_i = 1
        print('X Not found !!!')

def click_ads(v):
    try:
        print('Find ads ...')
        element = driver.find_element(by=AppiumBy.IMAGE, value=v)
        if element.is_display():
            print('Ads found...')
            element.click()
            driver.implicitly_wait(10)
    except Exception:
        driver.save_screenshot('ads_screen.png')
        print('Ads Not found !!!')

# Function to run scheduled tasks in the background
def run_next_display():
    schedule_thread = threading.Thread(target=next_display)
    schedule_thread.start()

try:
    click_ads(ads)
    # cast skill
    schedule.every(30).seconds.do(click_ads, ads)
    # next
    schedule.every(32).seconds.do(close_ads)

    # Swipe
    while 1:
        # schedule
        schedule.run_pending()
except Exception as ex:
    print('!!! xxxxx !!!')
    print(ex)
except KeyboardInterrupt:
    print('You pressed Ctrl+C!')
    exit()
finally:
    driver.quit()