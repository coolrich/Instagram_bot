import pprint
import random
import re
import sys
import time
from getpass import getpass
from time import sleep

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.common.exceptions import WebDriverException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth


def simulate_human_typing(element, text):
    for character in text:
        element.send_keys(character)
        time.sleep(random.uniform(0.1, 0.3))


def simulate_human_click(element):
    ActionChains(driver).move_to_element(element).perform()
    time.sleep(random.uniform(0.5, 1.5))
    element.click()
    time.sleep(random.uniform(0.5, 1.5))


def sign_in(login: str, password: str):
    global driver
    opts = Options()
    ua = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    opts.add_argument(f'--user-agent={ua}')
    opts.add_experimental_option("detach", True)
    opts.add_argument("start-maximized")
    opts.add_argument("disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option('useAutomationExtension', False)
    prefs = {"credentials_enable_service": False,
             "profile.password_manager_enabled": False}
    opts.add_experimental_option("prefs", prefs)
    try:
        driver = webdriver.Chrome(options=opts)
    except WebDriverException as we:
        print(we)
        sys.exit()
    stealth(driver,
            languages=["ua-UA", "uk"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    driver.get('https://www.instagram.com')

    insta_login = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//input[@name=\'username\']')))
    simulate_human_typing(insta_login, login)
    insta_pswd = driver.find_element(By.XPATH, '//input[@name=\'password\']')
    simulate_human_typing(insta_pswd, password)
    login_button = driver.find_element(By.XPATH, '//div[contains(text(), "Увійти")]')
    simulate_human_click(login_button)


def sign_in_through_FB(login: str, password: str):
    global driver
    opts = Options()
    ua = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    opts.add_argument(f'--user-agent={ua}')
    opts.add_experimental_option("detach", True)
    opts.add_argument("start-maximized")
    opts.add_argument("disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option('useAutomationExtension', False)
    prefs = {"credentials_enable_service": False,
             "profile.password_manager_enabled": False}
    opts.add_experimental_option("prefs", prefs)
    try:
        driver = webdriver.Chrome(options=opts)
    except WebDriverException as we:
        print(we)
        sys.exit()
    stealth(driver,
            languages=["ua-UA", "uk"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    driver.get('https://www.instagram.com')
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(),\"Увійти через Facebook\")]"))).click()
    insta_login = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//input[@name=\'email\']')))
    simulate_human_typing(insta_login, login)
    insta_pswd = driver.find_element(By.XPATH, '//input[@name=\'pass\']')
    simulate_human_typing(insta_pswd, password)
    login_button = driver.find_element(By.XPATH, '//button[@id="loginbutton"]')
    simulate_human_click(login_button)


# After sign in
def go_to_feed():
    feed_element = driver.find_element(by=By.XPATH, value="//span[contains(text(), \"Головна\")]")
    simulate_human_click(feed_element)


def turn_off_notifications():
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[contains(text(), \"Увімкнути сповіщення\")]')))
        driver.find_element(by=By.XPATH, value="//button[contains(text(), \"Не зараз\")]").click()
    except TimeoutException as te:
        print("There is no notification of turn on instagram notifications.")


height_position = None


def is_page_bottom_reached(current_page_height, page_height):
    return current_page_height + driver.execute_script("return window.pageYOffset") >= page_height


def scroll_window_down(length_in_pages: int = 0.5, delay: int = 1):
    inner_screen_height = driver.execute_script("return window.innerHeight")
    step = length_in_pages * inner_screen_height
    previous_page_height = driver.execute_script("return document.body.scrollHeight;")
    global height_position
    if height_position is None:
        height_position = driver.execute_script("return window.scrollY")
    is_dynamically_updated = False
    scroll_count = 0
    while True:
        current_page_height = driver.execute_script("return document.body.scrollHeight;")
        if not is_page_updated(previous_page_height, current_page_height):
            is_dynamically_updated = True
        if is_page_bottom_reached(inner_screen_height, previous_page_height):
            break
        scroll_page_down_to(height_position)
        scroll_count += 1
        print(f"Scrolling down: {scroll_count}")
        height_position += step
        time.sleep(delay)
    return is_dynamically_updated


def scroll_page_down_to(to_height_position):
    driver.execute_script(f"window.scrollTo({{ top: {to_height_position}, behavior: 'smooth' }});")


def is_page_updated(previous_page_height, current_page_height):
    return current_page_height > previous_page_height


def random_waiting(t1=0.5, t2=1.5):
    time.sleep(t1 + random.random() * (t2 - t1))


def looking_for_posts():
    global pattern
    # pattern = r'https://www.instagram.com/p/[A-Za-z0-9]+/\?next=.*'
    pattern = r'.*/p/'
    posts = set()
    for _ in range(3):
        is_dynamically_updated = False
        while not is_dynamically_updated:
            is_dynamically_updated = scroll_window_down()
        print("Scrolling is finished.")
        gather_post_elements(posts)
        random_waiting()


def gather_post_elements(posts):
    is_new_posts_added = False
    try:
        a_tags = []
        time_elems = driver.find_elements(by=By.TAG_NAME, value='time')
        pprint.pp(f"Count of \'time\' elements:{len(time_elems)}")
        for time_tag in time_elems:
            some_tag = time_tag
            while True:
                some_tag = some_tag.find_element(by=By.XPATH, value="..")
                if some_tag.tag_name == 'a':
                    a_tags.append(some_tag)
                    break
        print("Looking for elements with posts")
        hrefs = [tag.get_attribute('href') for tag in a_tags]
        new_posts = set()
        new_posts.update(filter(lambda tag: re.search(pattern, tag) is not None, hrefs))
        for p in new_posts:
            if p not in posts:
                is_new_posts_added = True
                break
        posts.update(new_posts)
        pprint.pp([p for p in posts])
    except StaleElementReferenceException as sere:
        print("Stale element reference exception during finding posts")
        print(sere)
    except NoSuchElementException as nsee:
        print(nsee)
    return is_new_posts_added


my_login = input('Enter your username: ')
my_password = getpass('Enter your password: ')

if __name__ == "__main__":
    # try:
    # sign_in(login, password)
    sign_in_through_FB(my_login, my_password)
    sleep(2)
    turn_off_notifications()
    sleep(2)
    go_to_feed()
    sleep(2)
    turn_off_notifications()
    sleep(2)
    looking_for_posts()
    # except Exception as e:
    #     print("Something way wrong...")
    #     print(e)
