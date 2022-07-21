from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from os import environ as env
from dotenv import load_dotenv


load_dotenv()

driver = webdriver.Firefox()

driver.get("https://pmdice.com")


def page_has_loaded():
    return driver.execute_script('return document.readyState;') == 'complete'


def login():
    driver.find_element(by=By.XPATH, value="//u[contains(text(),'Login')]").click()
    driver.find_element(by=By.ID, value="loginname").send_keys(env.get("USERNAME"))
    driver.find_element(by=By.ID, value="loginpw").send_keys(env.get("PASSWORD"))
    driver.find_element(by=By.ID, value="btnlogin").click()


if __name__ == "__main__":
    while not page_has_loaded():
        sleep(0.5)
    login()
