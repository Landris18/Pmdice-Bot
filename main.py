from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()

driver.get("https://pmdice.com")

driver.find_element(by=By.XPATH, value="//u[contains(text(),'Login')]").click()

username_input = driver.find_element(by=By.ID, value="loginname")
password_input = driver.find_element(by=By.ID, value="loginpw")
button_login = driver.find_element(by=By.ID, value="btnlogin")

username_input.send_keys("")
password_input.send_keys("")
button_login.click()


