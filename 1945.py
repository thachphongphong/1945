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

skill_1 = { "x" : 40, "y": 536}
skill_2 = {"x": 40, "y": 625}

driver = webdriver.Remote(
    command_executor="http://127.0.0.1:4723",
    desired_capabilities=desired_caps
)

driver.update_settings({"getMatchedImageResult": True})
driver.implicitly_wait(5)

with open(r"plane.png", "rb") as image_file:
    plane = base64.b64encode(image_file.read()).decode("utf-8")

with open(r"x.png", "rb") as image_file:
    x = base64.b64encode(image_file.read()).decode("utf-8")

with open(r"play.png", "rb") as image_file:
    play = base64.b64encode(image_file.read()).decode("utf-8")

with open(r"73.png", "rb") as image_file:
    i73 = base64.b64encode(image_file.read()).decode("utf-8")

with open(r"next.png", "rb") as image_file:
    next = base64.b64encode(image_file.read()).decode("utf-8")

with open(r"rocket2.png", "rb") as image_file:
    rocket = base64.b64encode(image_file.read()).decode("utf-8")

with open(r"53.png", "rb") as image_file:
    i53 = base64.b64encode(image_file.read()).decode("utf-8")


next_time = 1
def next_display():
    global next_time  # Declare skill_i as a global variable
    global next_clicked
    try:
        e_next = driver.find_element(by=AppiumBy.IMAGE, value=next)
        if(e_next.is_displayed()):    
            print('NEXT found !!!')
            next_clicked = True
            next_time = 1
            e_next.click()
            click_i53()
    except Exception:
        next_time = next_time + 1
        print('NEXT Not found !!!')

next_clicked = True
def click_i53():
    global next_clicked
    try:
        sleep(20)
        ei53 = driver.find_element(by=AppiumBy.IMAGE, value=i53)
        print('I53 found !!!')
        ei53.click()
        sleep(5)
        click_play7_coord()
    except NoSuchElementException:
        print('I53 not found !!!')

def click_play7_coord():
    global next_clicked
    try:
        if next_clicked == True:
            print('Play click !!!')
            TouchAction(driver).tap(None, 180, 766, 2).perform()
            next_clicked = False
            sleep(5)
    except NoSuchElementException:
        print('Play7 not found !!!')


skill_i = 1
def cast_skill_coord():
    global skill_i
    try:
        if next_clicked == False:
            if skill_i == 1:
                print('Cast Skill ' + str(skill_i))
                TouchAction(driver).tap(None, skill_1["x"], skill_1["y"], 1).perform()
                skill_i = skill_i + 1
            else:
                print('Cast Skill ' + str(skill_i))
                TouchAction(driver).tap(None, skill_2["x"], skill_2["y"], 1).perform()
                skill_i = skill_i - 1
    except NoSuchElementException:
        print('Play7 not found !!!')

# Function to run scheduled tasks in the background
def run_next_display():
    schedule_thread = threading.Thread(target=next_display)
    schedule_thread.start()

def run_cast_skill():
    schedule_thread = threading.Thread(target=cast_skill_coord)
    schedule_thread.start()

try:
    # in 53
    click_i53()

    # cast skill
    schedule.every(45).seconds.do(run_cast_skill)
    # next
    schedule.every(120).seconds.do(next_display)

    # Step 3 : Find the device width and height
    deviceSize = driver.get_window_size()
    print("Device Width and Height : ",deviceSize)
    screenWidth = deviceSize['width']
    screenHeight = deviceSize['height']
    # Step 4 : Find the x,y coordinate to swipe
    # *********** Left to Right ************* #
    startx = screenWidth*8/9
    endx = screenWidth/9
    starty = screenHeight/2
    endy = screenHeight/2
    # *********** Right to Left ************* #
    startx2 = screenWidth/9
    endx2 = screenWidth*8/9
    starty2 = screenHeight/2
    endy2 = screenHeight/2

    # # move to botton
    # TouchAction(driver).long_press(None,startx,starty).move_to(None,startx,starty-20).release().perform()

    # Swipe
    while 1:
        # schedule
        schedule.run_pending()
        # sleep(1)
        # swipe
        if next_clicked is False:
            actions = TouchAction(driver)
            # Step 5 : perform the action swiping from left to Right
            actions.long_press(None,startx,starty).move_to(None,endx,endy).release().perform()
            # Step 6 : perform the action swiping from Right to Left
            actions.long_press(None,startx2,starty2).move_to(None,endx2,endy2).release().perform()
            # exit if failed
            if next_time == 3: raise Exception("3 time not found next, exit")
        else:
            click_i53()
except Exception as ex:
    print('!!! xxxxx !!!')
    print(ex)
except KeyboardInterrupt:
    print('You pressed Ctrl+C!')
    exit()
finally:
    driver.quit()