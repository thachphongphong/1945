import pytest
import base64
from time import sleep
import logging
import json
import schedule as schedule
from appium import webdriver
from appium.webdriver.appium_service import AppiumService
from appium.options.ios import XCUITestOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
from appium.webdriver.extensions.action_helpers import ActionHelpers

# Constants
APPIUM_PORT = 4723
APPIUM_HOST = '127.0.0.1'
NEXT_TIME_LIMIT = 3

# Global variables
next_time = 1
next_clicked = True
skill_i = 1

IMAGE_FILE_PATHS = {
    'plane': 'plane.png',
    'x': 'x.png',
    'play': 'play_7.png',
    'next': 'next.png',
    'rocket': 'rocket2.png',
    'i53': '53.png',
    'm53': 'map53.png',
}


def load_settings():
    with open('settings.json') as f:
        return json.load(f)


def load_images():
    images = {}
    for name, path in IMAGE_FILE_PATHS.items():
        with open(path, "rb") as image_file:
            images[name] = base64.b64encode(image_file.read()).decode("utf-8")
    return images


loaded_images = load_images()
load_settings = load_settings()
LOGGER = logging.getLogger(__name__)
i53 = loaded_images['i53']
map_53 = [(91, 335)]
play_7 = [(180, 766)]
skill_1 = [(40, 536)]
skill_2 = [(40, 625)]


# HINT: fixtures below could be extracted into conftest.py
# HINT: and shared across all tests in the suite
@pytest.fixture(scope='session')
def appium_service():
    service = AppiumService()
    service.start(
        # Check the output of `appium server --help` for the complete list of
        # server command line arguments
        args=['--address', APPIUM_HOST, '-p', str(APPIUM_PORT), '--use-plugins', 'images'],
        timeout_ms=20000,
    )
    yield service
    service.stop()


def create_ios_driver(custom_opts=None):
    options = XCUITestOptions()
    options.platformVersion = '16.7'
    options.udid = load_settings['udid']
    if custom_opts is not None:
        options.load_capabilities(custom_opts)
    # Appium1 points to http://127.0.0.1:4723/wd/hub by default
    return webdriver.Remote(f'http://{APPIUM_HOST}:{APPIUM_PORT}', options=options)


@pytest.fixture
def ios_driver_factory():
    return create_ios_driver


@pytest.fixture
def ios_driver():
    # prefer this fixture if there is no need to customize driver options in tests
    driver = create_ios_driver()
    yield driver
    driver.quit()


def next_display(driver):
    global next_time  # Declare skill_i as a global variable
    global next_clicked
    try:
        e_next = driver.find_element(by=AppiumBy.IMAGE, value=next)
        if e_next.is_displayed():
            LOGGER.info('NEXT found !!!')
            next_clicked = True
            next_time = 1
            e_next.click()
            click_i53()
    except NoSuchElementException:
        next_time = next_time + 1
        LOGGER.warning('NEXT Not found !!!')


def click_i53(driver):
    global next_clicked
    try:
        sleep(20)
        ei53 = driver.find_element(by=AppiumBy.IMAGE, value=i53)
        if ei53.is_displayed():
            LOGGER.info('I53 found !!!')
            ActionHelpers.tap(driver, map_53)
            sleep(5)
            click_play7_coord(driver)
    except NoSuchElementException:
        LOGGER.warning('I53 not found !!!')


def click_play7_coord(driver):
    global next_clicked
    try:
        if next_clicked:
            sleep(2)
            LOGGER.info('Play click !!!')
            ActionHelpers.tap(driver, play_7)
            next_clicked = False
            sleep(3)
        else:
            click_i53(driver)
    except NoSuchElementException:
        LOGGER.warning('Play7 not found !!!')


def cast_skill_coord(driver):
    global skill_i
    try:
        if not next_clicked:
            LOGGER.info('Cast Skill {}', skill_i)
            ActionHelpers.tap(driver, skill_1) if skill_i == 1 else ActionHelpers.tap(driver, skill_2)
            skill_i = skill_i + 1 if skill_i == 1 else skill_i - 1
    except NoSuchElementException:
        LOGGER.warning('Play7 not found !!!')


def play_game(driver, startx, starty, endx, endy, startx2, starty2, endx2, endy2):
    ActionHelpers.swipe(driver, startx, starty, endx, endy, 500)
    ActionHelpers.swipe(driver, startx2, starty2, endx2, endy2, 500)


def run_next_display(driver):
    global next_time
    global next_clicked
    try:
        e_next = driver.find_element(by=AppiumBy.IMAGE, value=loaded_images['next'])
        if e_next.is_displayed():
            LOGGER.info('NEXT found !!!')
            next_clicked = True
            next_time = 1
            e_next.click()
            click_i53(driver)
    except NoSuchElementException:
        next_time += 1
        LOGGER.warning('NEXT Not found !!!')
        if next_time >= NEXT_TIME_LIMIT:
            raise Exception("3 times not found next, exit")


def run_cast_skill_coord(driver):
    try:
        if not next_clicked:
            cast_skill_coord(driver)
    except Exception as ex:
        LOGGER.warning('Error in run_cast_skill_coord: {}', ex)


def test_play(appium_service, ios_driver_factory):
    with ios_driver_factory({
        'appium:app': 'com.os.airforce',
        'appium:noReset': 'true'
    }) as driver:
        try:
            click_i53(driver)
            # cast skill
            schedule.every(45).seconds.do(run_cast_skill_coord, driver)
            # next
            schedule.every(120).seconds.do(run_next_display, driver)

            device_size = driver.get_window_size()
            screen_width = device_size['width']
            screen_height = device_size['height']

            startx, endx, starty, endy = screen_width * 8 / 9, screen_width / 9, screen_height / 2, screen_height / 2
            startx2, endx2, starty2, endy2 = screen_width / 9, screen_width * 8 / 9, screen_height / 2, screen_height / 2

            while True:
                schedule.run_pending()
                if not next_clicked:
                    play_game(driver, startx, starty, endx, endy, startx2, starty2, endx2, endy2)
                else:
                    click_i53(driver)
        except Exception as ex:
            LOGGER.error('Error in test_play: {}', ex)
            driver.background_app(-1)
        except KeyboardInterrupt:
            LOGGER.warning('You pressed Ctrl+C!')
            exit()
