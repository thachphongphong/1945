from appium.webdriver.common.touch_action import TouchAction
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
import base64
from selenium.common.exceptions import NoSuchElementException
from threading import active_count
from time import sleep
import schedule
import threading
import json

with open('settings.json') as f:
    desired_caps = json.load(f)

map_53 = {"x" : 91, "y": 335}
play_7 = {"x" : 180, "y": 766}
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

with open(r"play_7.png", "rb") as image_file:
    play = base64.b64encode(image_file.read()).decode("utf-8")

with open(r"next.png", "rb") as image_file:
    next = base64.b64encode(image_file.read()).decode("utf-8")

with open(r"rocket2.png", "rb") as image_file:
    rocket = base64.b64encode(image_file.read()).decode("utf-8")

with open(r"53.png", "rb") as image_file:
    i53 = base64.b64encode(image_file.read()).decode("utf-8")

with open(r"map53.png", "rb") as image_file:
    m53 = base64.b64encode(image_file.read()).decode("utf-8")

# Add a threading Lock
# lock = threading.Lock()
next_time = 1
next_clicked = True
skill_i = 1

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

def click_i53():
    global next_clicked
    try:
        sleep(15)
        ei53 = driver.find_element(by=AppiumBy.IMAGE, value=i53)
        if(ei53.is_displayed()):  
            print('I53 found !!!')
            # ei53.click()
            TouchAction(driver).tap(None, map_53["x"], map_53["y"], 1).perform()
            sleep(5)
            click_play7_coord()
    except NoSuchElementException:
        print('I53 not found !!!')

def click_play7_coord():
    global next_clicked
    try:
        if next_clicked == True:
            sleep(1)
            # ep7 = driver.find_element(by=AppiumBy.IMAGE, value=play)
            # if(ep7.is_displayed()):
            print('Play click !!!')
            TouchAction(driver).tap(None, play_7["x"], play_7["y"], 1).perform()
            next_clicked = False
            sleep(3)
        else:
            click_i53()
    except NoSuchElementException:
        print('Play7 not found !!!')


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
    # Put the app into background for an indefinite amount of time:
    driver.background_app(-1)
    # and activate it once you need it again:
    # driver.activate_app("app.id")
    print(ex)
except KeyboardInterrupt:
    # driver.quit()
    print('You pressed Ctrl+C!')
    exit()
finally:
    print('Finally event')
    driver.quit()
