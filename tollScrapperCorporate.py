from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time

def tollScrapperCorporate():
    chrome_path = "./driver/chromedriver.exe"
    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"
    urlName = "https://fastaglogin.icicibank.com/CUSTLOGIN/Default.aspx"
    driver = webdriver.Chrome(chrome_path,desired_capabilities=capa)
    driver.get(urlName)

    try:
        corporate_select = WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_xpath('//*[@id="rdCorporateLogin"]')).click()

    except TimeoutException:
        print("Loading take too much time on select corporate")

    try:
        userID = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "txtUserId1"))
        )

        driver.execute_script("document.getElementById('txtUserId1').value='chetakmotors'")
        driver.execute_script("document.getElementById('txtPassword1').value='Cmpl@2020'")
        login = WebDriverWait(driver, 3).until(
            lambda x: x.find_element_by_xpath('//*[@id="btnLoginCorporate"]').click())

    except TimeoutException:
        print("Loading take too much time on Login")

    time.sleep(2)
    driver.get('https://fastaglogin.icicibank.com/CUSTLOGIN/Pages/Documents/AdHocStatements.aspx')

    try:
        link2 = WebDriverWait(driver, 5).until(
            lambda x: x.find_element_by_xpath('//*[@id="Body_Calendar_txtStartDates"]').click())
    except TimeoutException:
        print("Loading take too much time on Select Date")

    try:
        link3 = WebDriverWait(driver, 3).until(
            lambda x: x.find_element_by_xpath('//*[@id="Body_Calendar_lblMonthly"]'))
        link3.click()
        time.sleep(2)
        download_link = driver.find_element_by_link_text('Export Transaction Summary to Excel')
        download_link.click()
        time.sleep(10)
    except TimeoutException:
        print("Loading take too much time on Export Transaction Summary to Excel")

    time.sleep(30)
    print("Download OnlineStatement.xls successfully!")
    driver.close()

if __name__  ==  "__main__":
    tollScrapperCorporate()
