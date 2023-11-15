from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
import base64
import json

with open('settings.json') as f:
    desired_caps = json.load(f)

driver = webdriver.Remote(
    command_executor="http://127.0.0.1:4723",
    desired_capabilities=desired_caps
)

driver.update_settings({"getMatchedImageResult": True})

driver.implicitly_wait(20)

with open(r"ac.png", "rb") as image_file:
    ac = base64.b64encode(image_file.read()).decode("utf-8")

with open(r"1.png", "rb") as image_file:
    one = base64.b64encode(image_file.read()).decode("utf-8")

with open(r"plus.png", "rb") as image_file:
    plus = base64.b64encode(image_file.read()).decode("utf-8")

with open(r"equal.png", "rb") as image_file:
    equal = base64.b64encode(image_file.read()).decode("utf-8")

try:
    driver.background_app(-1)
    # # Clear the calculator (AC button)
    # e_ac = driver.find_element(by=AppiumBy.IMAGE, value=ac)
    # e_ac.click()
    # e_one = driver.find_element(by=AppiumBy.IMAGE, value=one)
    # e_one.click()
    # e_plus = driver.find_element(by=AppiumBy.IMAGE, value=plus)
    # e_plus.click()
    # e_one.click()
    # e_equal = driver.find_element(by=AppiumBy.IMAGE, value=equal)
    # e_equal.click()
except Exception as ex:
    print('!!! xxxxx !!!')
    print(ex)
finally:
    driver.quit()
