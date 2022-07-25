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
import requests

load_dotenv()

FirefoxOptions = Options()
FirefoxOptions.headless = True

driver = webdriver.Firefox(options=FirefoxOptions)
driver.get(env.get("LINK"))

stop = False
WIN = 0
LOSE = 0


def pageHasLoaded():
    return driver.execute_script('return document.readyState;') == 'complete'


def isConnected():
    return requests.get(env.get("LINK")).status_code == 200


def showStat():
    print("-------Number of WIN-------- : ", WIN)
    print("-------Nomber of LOSS------- : ", LOSE)


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
    global WIN
    global LOSE
    res = "not_rolled"

    try:
        labelStatus = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mfplayresultout .label"))).text
        
        if ("Win" in labelStatus):
            WIN += 1
            res = "win"
        if ("Loss" in labelStatus):
            LOSE += 1
            res = "lose"
        if ("Timeout" in labelStatus):
            res = "timeout"
        if ("Insufficient" in labelStatus):
            res = "insufficient"

        return res

    except Exception:
        return res


def start1(betMinAmount1, i):
    status = checkStatus()

    if checkReadyButton():
        if (status == "win"):
            driver.find_element(by=By.ID, value="mfInputAmount").send_keys(Keys.BACKSPACE * 8)
            driver.find_element(by=By.ID, value="mfInputAmount").send_keys(betMinAmount1)

            driver.execute_script("arguments[0].click()", driver.find_element(by=By.ID, value="mfpayout_over"))
            
            i += 1

        if (status == "lose"):
            betAmount = driver.find_element(by=By.ID, value="mfInputAmount").text

            if len(betAmount) != 0:
                if ((float(betAmount) / betMinAmount1) >= 1024):
                    print("Condition verified")
                
                driver.find_element(by=By.ID, value="mfInputAmount").send_keys(Keys.BACKSPACE * 8)
                driver.find_element(by=By.ID, value="mfInputAmount").send_keys(float(betAmount) * 2)

        if (status == "timeout"):
            reconnect = 10
            for i in range (1,reconnect):
                if not isConnected():
                    sleep(4)
                i += 1
                if (i > reconnect -1):
                    print(status)
                    showStat()
                    driver.close()
                
        if (status == "insufficient"):
            print(status)
            showStat()
            driver.close()

        if (status == "not_rolled"):
            print(status)
        
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
        if (status == "win"):
            driver.find_element(by=By.ID, value="mfInputAmount").send_keys(Keys.BACKSPACE * 8)
            driver.find_element(by=By.ID, value="mfInputAmount").send_keys(betMinAmount2)

            isDouble = False
            i += 1
        if (status == "lose"):
            betAmount = driver.find_element(by=By.ID, value="mfInputAmount").text

            if len(betAmount) != 0:
                if ((float(betAmount) / betMinAmount1) >= 4096):
                    print("Condition verified")

                if isDouble:
                    driver.find_element(by=By.ID, value="mfInputAmount").send_keys(Keys.BACKSPACE * 8)
                    driver.find_element(by=By.ID, value="mfInputAmount").send_keys(float(betAmount) * 2)
                    isDouble = False
                else:
                    driver.find_element(by=By.ID, value="mfInputAmount").send_keys(Keys.BACKSPACE * 8)
                    driver.find_element(by=By.ID, value="mfInputAmount").send_keys(float(betAmount))
                    isDouble = True

        if (status == "timeout"):
            reconnect = 10
            for i in range (1,reconnect):
                if not isConnected():
                    sleep(4)
                i += 1
                if (i > reconnect -1):
                    print(status)
                    showStat()
                    driver.close()
                
        if (status == "insufficient"):
            print(status)
            showStat()
            driver.close()

        if (status == "not_rolled"):
            print(status)

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
        if (status == "win"):
            driver.find_element(by=By.ID, value="mfInputAmount").send_keys(Keys.BACKSPACE * 8)
            driver.find_element(by=By.ID, value="mfInputAmount").send_keys(0)

            isDouble = False
            numStart = 0
            i += 1

        if (status == "lose"):
            if (numStart <= 0):
                betAmount = driver.find_element(by=By.ID, value="mfInputAmount").text

                if len(betAmount) != 0:
                        
                    if (betAmount <= 0):
                        betAmount = betMinAmount3

                    if ((betAmount / betMinAmount3) >= 4096):
                        print("Condition verified")

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

        if (status == "timeout"):
            reconnect = 10
            for i in range (1,reconnect):
                if not isConnected():
                    sleep(4)
                i += 1
                if (i > reconnect -1):
                    print(status)
                    showStat()
                    driver.close()
                
        if (status == "insufficient"):
            print(status)
            showStat()
            driver.close()

        if (status == "not_rolled"):
            print(status)

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
    if isConnected():
        try:
            arg = sys.argv[1] 

            if (arg == "--start1" or arg == "--start2" or arg == "--start3"):
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
