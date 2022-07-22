import math
import random
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from os import environ as env
from dotenv import load_dotenv
import sys


load_dotenv()

FirefoxOptions = Options()
FirefoxOptions.headless = False

driver = webdriver.Firefox(options=FirefoxOptions)
driver.get(env.get("LINK"))

stop = False


def pageHasLoaded():
    return driver.execute_script('return document.readyState;') == 'complete'


def login():
    while not pageHasLoaded():
        sleep(0.5)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//u[contains(text(),'Login')]"))).click()

    driver.find_element(by=By.ID, value="loginname").send_keys(env.get("USERNAME"))
    driver.find_element(by=By.ID, value="loginpw").send_keys(env.get("PASSWORD"))
    driver.find_element(by=By.ID, value="btnlogin").click()


def setStrategy(strategy, chance):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mfpayoutmul"))).send_keys(Keys.BACKSPACE * 8)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mfpayoutmul"))).send_keys(strategy)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mfpayoutper"))).send_keys(Keys.BACKSPACE * 8)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mfpayoutper"))).send_keys(chance)


def checkReadyButton():
    buttonPlay = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "btnplaymb")))
    if ("DICE" in buttonPlay.text):
        return True
    return False


def checkStatus():
    res = 0

    try:
        labelStatus = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mfplayresultout .label"))).text

        if ("Win" in labelStatus):
            res = 1
        elif ("Loss" in labelStatus):
            res = -1

        return res

    except Exception:
        return res


def start1(betMinAmount1, i):
    status = checkStatus()

    if checkReadyButton():
        if (status > 0):
            driver.find_element(by=By.ID, value="mfInputAmount").send_keys(Keys.BACKSPACE * 8)
            driver.find_element(by=By.ID, value="mfInputAmount").send_keys(betMinAmount1)

            WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "mfpayout_over"))).click()
            i += 1
        elif (status < 0):
            betAmount = driver.find_element(by=By.ID, value="mfInputAmount").text

            if len(betAmount) != 0:
                if ((float(betAmount) / betMinAmount1) >= 1024):
                    # showAlertMessage();
                    pass
                
                driver.find_element(by=By.ID, value="mfInputAmount").send_keys(Keys.BACKSPACE * 8)
                driver.find_element(by=By.ID, value="mfInputAmount").send_keys(float(betAmount) * 2)
        else:
            print("Dice_not_rolled or not_enough_balance")
        
        sleep(0.5)
        driver.find_element(by=By.ID, value="btnplaymb").click()

    if not stop:
        if (i > 100):
            betMinAmount2 = 0.0001

            driver.find_element(by=By.ID, value="mfpayoutmul").send_keys(Keys.BACKSPACE * 8)
            driver.find_element(by=By.ID, value="mfpayoutmul").send_keys("4x")

            driver.find_element(by=By.ID, value="mfpayoutper").send_keys(Keys.BACKSPACE * 8)
            driver.find_element(by=By.ID, value="mfpayoutper").send_keys("24.01%")

            start2(betMinAmount2, False, 1)
        else:
            min = 1.5
            max = 4
            delay = math.floor(random.randint(int(min), int(max - min + 1)))
            sleep(delay)
            start1(betMinAmount1, i)


def start2(betMinAmount2, isDouble, i) :
    status = checkStatus()

    if checkReadyButton():
        if (status > 0):
            driver.find_element(by=By.ID, value="mfInputAmount").send_keys(Keys.BACKSPACE * 8)
            driver.find_element(by=By.ID, value="mfInputAmount").send_keys(betMinAmount2)

            isDouble = False
            i += 1
        elif (status < 0):
            betAmount = driver.find_element(by=By.ID, value="mfInputAmount").text

            if len(betAmount) != 0:
                if ((float(betAmount) / betMinAmount1) >= 4096):
                    # showAlertMessage();
                    pass

                if isDouble:
                    driver.find_element(by=By.ID, value="mfInputAmount").send_keys(Keys.BACKSPACE * 8)
                    driver.find_element(by=By.ID, value="mfInputAmount").send_keys(float(betAmount) * 2)
                    isDouble = False
                else:
                    driver.find_element(by=By.ID, value="mfInputAmount").send_keys(Keys.BACKSPACE * 8)
                    driver.find_element(by=By.ID, value="mfInputAmount").send_keys(float(betAmount))
                    isDouble = True
        else:
            print("Dice_not_rolled or not_enough_balance")

        sleep(0.5)
        driver.find_element(by=By.ID, value="btnplaymb").click()

    if not stop:
        if (i > 100):
            betMinAmount3 = 0.0001

            driver.find_element(by=By.ID, value="mfpayoutmul").send_keys(Keys.BACKSPACE * 8)
            driver.find_element(by=By.ID, value="mfpayoutmul").send_keys("4x")

            driver.find_element(by=By.ID, value="mfpayoutper").send_keys(Keys.BACKSPACE * 8)
            driver.find_element(by=By.ID, value="mfpayoutper").send_keys("24.01%")

            start3(betMinAmount3, False, 0, 1)

        else:
            min = 1.5
            max = 4
            delay = math.floor(random.randint(int(min), int(max - min + 1)))
            sleep(delay)
            start2(betMinAmount2, isDouble, i)


def start3(betMinAmount3, isDouble, numStart, i):
    status = checkStatus()

    if checkReadyButton():
        if (status > 0):
            driver.find_element(by=By.ID, value="mfInputAmount").send_keys(Keys.BACKSPACE * 8)
            driver.find_element(by=By.ID, value="mfInputAmount").send_keys(0)

            isDouble = False
            numStart = 0
            i += 1

        elif (status < 0):
            if (numStart <= 0):
                betAmount = driver.find_element(by=By.ID, value="mfInputAmount").text

                if len(betAmount) != 0:
                        
                    if (betAmount <= 0):
                        betAmount = betMinAmount3

                    if ((betAmount / betMinAmount3) >= 4096):
                        pass
                        # showAlertMessage();

                    if (isDouble and numStart <= -2):
                        driver.find_element(by=By.ID, value="mfInputAmount").send_keys(Keys.BACKSPACE * 8)
                        driver.find_element(by=By.ID, value="mfInputAmount").send_keys(float(betAmount)  * 2)
                        isDouble = False
                    else:
                        driver.find_element(by=By.ID, value="mfInputAmount").send_keys(Keys.BACKSPACE * 8)
                        driver.find_element(by=By.ID, value="mfInputAmount").send_keys(float(betAmount))
                        isDouble = True
            else:
                driver.find_element(by=By.ID, value="mfInputAmount").send_keys(Keys.BACKSPACE * 8)
                driver.find_element(by=By.ID, value="mfInputAmount").send_keys(0)
                isDouble = False

            numStart -= 1
        else:
            print("Dice_not_rolled or not_enough_balance")

        sleep(0.3)
        driver.find_element(by=By.ID, value="btnplaymb").click()

    if not stop:
        if (i > 100):
            betMinAmount1 = 0.01

            driver.find_element(by=By.ID, value="mfpayoutmul").send_keys(Keys.BACKSPACE * 8)
            driver.find_element(by=By.ID, value="mfpayoutmul").send_keys("2x")

            driver.find_element(by=By.ID, value="mfpayoutper").send_keys(Keys.BACKSPACE * 8)
            driver.find_element(by=By.ID, value="mfpayoutper").send_keys("48.02%")

            start1(betMinAmount1, 1)
        else:
            min = 1.5
            max = 4
            delay = math.floor(random.randint(int(min), int(max - min + 1)))
            sleep(delay)
            start3(betMinAmount3, isDouble, numStart, i)
          

if __name__ == "__main__":
    try:
        arg = sys.argv[1] 

        if (arg == "--start1" or arg == "--start1" or arg == "--start1"):
            login()

            if (arg == "--start1"):
                betMinAmount1 = 0.001
                setStrategy("2x", "48.02%")
                start1(betMinAmount1, 1)
            
            if (arg == "--start2"):
                betMinAmount2 = 0.0001
                setStrategy("4x", "24.01%")
                start2(betMinAmount2, False, 1)

            if (arg == "--start3"):
                betMinAmount3 = 0.0001
                setStrategy("4x", "24.01%")
                start3(betMinAmount3, False, 0, 1)
        else:
            driver.close()
            print("Argument " + arg + " not recognized")
            print("Expected argument are --start1 | --start2 | --start3")

    except IndexError:
        driver.close()
        print("Expected argument are --start1 | --start2 | --start3")
