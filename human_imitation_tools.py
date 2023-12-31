import math
import random
from time import sleep
from selenium.webdriver.remote.webelement import WebElement


class HumanImitationTools:
    @staticmethod
    def input(field: WebElement, text: str):
        field.click()
        HumanImitationTools.imitation_of_human_delay(2, 4)
        for char in text:
            field.send_keys(char)
            HumanImitationTools.imitation_of_human_delay()
        HumanImitationTools.imitation_of_human_delay(1, 3)

    @staticmethod
    def wait(seconds: float):
        print("Waiting for", f"{math.floor(seconds / 60.0)}m:{round(seconds % 60, 2)}s")
        sleep(seconds)

    @staticmethod
    def imitation_of_human_delay(t1=0.1, t2=0.3):
        if t1 > t2:
            t1 = t2
        delay = t1 + random.random() * (t2 - t1)
        HumanImitationTools.wait(round(delay, 2))