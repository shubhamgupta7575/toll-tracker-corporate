from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import mysql.connector
import dbInfo
import time

def tollScrapperCorporate():
    db = mysql.connector.connect(
                    host=dbInfo.host,
                    user=dbInfo.user,
                    password=dbInfo.password,
                    database=dbInfo.database
                )

    cursor = db.cursor()
    process_count = 0
    inserted_count = 0
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    chrome_path = "../toll_scrapper/driver/chromedriver.exe"
    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"
    urlName = "https://fastaglogin.icicibank.com/CUSTLOGIN/Default.aspx"
    driver = webdriver.Chrome(chrome_path,desired_capabilities=capa)
    driver.get(urlName)

    try:
        download_link = WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_xpath('//*[@id="rdCorporateLogin"]')).click()

    except TimeoutException:
        print("Loading take too much time on step 1")


    try:
        userID = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "txtUserId1"))
        )

        driver.execute_script("document.getElementById('txtUserId1').value='chetakmotors'")
        driver.execute_script("document.getElementById('txtPassword1').value='Cmpl@2020'")
        login = WebDriverWait(driver, 3).until(
            lambda x: x.find_element_by_xpath('//*[@id="btnLoginCorporate"]').click())

    except TimeoutException:
        print("Loading take too much time on step 3")

    time.sleep(2)
    driver.get('https://fastaglogin.icicibank.com/CUSTLOGIN/Pages/Documents/AdHocStatements.aspx')

    # try:
    #     link = WebDriverWait(driver, 10).until(
    #         lambda x: x.find_element_by_xpath('//*[@id="hyplnkView"]').click())
    # except TimeoutException:
    #     print("Loading take too much time on step 4")

    # try:
    #     link = WebDriverWait(driver, 10).until(
    #         lambda x: x.find_element_by_xpath('//*[@id="Menu_lnkbtnstatements"]').click())
    # except TimeoutException:
    #     print("Loading take too much time on step 4")
    #
    # try:
    #     link1 = WebDriverWait(driver, 10).until(
    #         lambda x: x.find_element_by_xpath('//*[@id="Body_Menu_rptSubDepartment_aMenuItem_1"]').click())
    # except TimeoutException:
    #     print("Loading take too much time on step 5")
    #
    try:
        link2 = WebDriverWait(driver, 5).until(
            lambda x: x.find_element_by_xpath('//*[@id="Body_Calendar_txtStartDates"]').click())
        # link3 = WebDriverWait(driver, 2).until(
        #     lambda x: x.find_element_by_xpath('//*[@id="Body_Calendar_lblMonthly"]').click())
        # link3 = driver.find_element_by_xpath('//*[@id="Body_Calendar_lblMonthly"]')
        # link3.click()
    except TimeoutException:
        print("Loading take too much time on step 6")

    try:
        link3 = WebDriverWait(driver, 3).until(
            lambda x: x.find_element_by_xpath('//*[@id="Body_Calendar_lblMonthly"]'))
        link3.click()
        time.sleep(2)
        # link3.send_keys( Keys.TAB, Keys.TAB, Keys.TAB, Keys.ENTER)
        download_link = driver.find_element_by_link_text('Export Transaction Summary to Excel')
        download_link.click()
        time.sleep(10)
    except TimeoutException:
        print("Loading take too much time on step 7")

    # try:
    #     link4 = WebDriverWait(driver, 5).until(
    #         lambda x: x.find_element_by_link_text("Export Transaction Summary to Excel").click())
    #     # download_link = driver.find_element_by_link_text('Export Transaction Summary to Excel')
    #     # download_link.click()
    # except TimeoutException:
    #     print("Loading take too much time on Download Online Statement")
    time.sleep(20)

    # try:
    #     table1 = driver.find_element_by_xpath('//*[@id="Menu_lnkbtnOnline"]')
    #     for row1 in table1.find_elements_by_css_selector('tr'):
    #         lst1 = []
    #         for cell1 in row1.find_elements_by_tag_name('td'):
    #             lst1.append(cell1.text)
    #             print(lst1)
    # except TimeoutException:
    #     print("Loading take too much time on step 4")

    driver.close()

if __name__  ==  "__main__":
    tollScrapperCorporate()
