from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import dbInfo
import time
import pandas as pd
from pathlib import Path

def dispute_transaction_upload():
    xls_file_path = dbInfo.xls_file_path
    # convert into xls format
    read_csv_file = pd.read_csv("dispute_transaction_temp.csv")
    xls_file = Path("dispute_transaction.xls")
    if not(xls_file.is_file()):
        # file not exists
        read_csv_file.to_html("dispute_transaction.xls", index=False)
        print("Dispute Transaction CSV converted into XLS File.")
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
    driver.get('https://fastaglogin.icicibank.com/CUSTLOGIN/Pages/Complaints/BulkDisputeComplaints.aspx')
    time.sleep(2)
    try:
        select_file = WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_xpath('//*[@id="Body_fudComplaint"]')).send_keys(xls_file_path)

    except TimeoutException:
        print("Loading take too much time on select files to upload")
    time.sleep(5)
    # driver.find_element_by_xpath('//*[@id="Body_btnUploadComplaint"]').click()

    driver.close()

if __name__  ==  "__main__":
    dispute_transaction_upload()
