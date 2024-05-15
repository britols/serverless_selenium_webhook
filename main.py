import os
import requests
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from tempfile import mkdtemp
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

USER = os.environ['DEST_USER']
PWD = os.environ['DEST_PWD']
URL = os.environ['DEST_URL']
WEBHOOK = os.environ['DEST_WHOOK']
WEBHOOK_FILTER = os.environ['DEST_WHOOK_FILTER']

def handler(event=None, context=None):
    options = webdriver.ChromeOptions()
    service = webdriver.ChromeService("/opt/chromedriver")

    options.binary_location = '/opt/chrome/chrome'
    options.add_argument("--headless=new")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")

    driver = webdriver.Chrome(options=options, service=service)
    driver.get(URL)

    #Sign in
    driver.find_element(By.CSS_SELECTOR, "[name = 'user[email]']").send_keys(USER)
    driver.find_element(By.CSS_SELECTOR, "[name = 'user[password]']").send_keys(PWD)
    elem = driver.find_element(By.CSS_SELECTOR, "[name = 'policy_confirmed']")
    driver.execute_script("arguments[0].click();", elem)
    elem = driver.find_element(By.CSS_SELECTOR, "[name = 'commit']")
    driver.execute_script("arguments[0].click();", elem)

    time.sleep(5)

    elem = driver.find_element(By.CSS_SELECTOR, "[class = 'button primary small']")
    driver.execute_script("arguments[0].click();", elem)

    time.sleep(2)

    elem = driver.find_element(By.CSS_SELECTOR, "[class = 'fas fa-money-bill-alt fa-lg fa-fw']")
    driver.execute_script("arguments[0].click();", elem)

    time.sleep(5)

    elem = driver.find_element(By.CSS_SELECTOR, "[class = 'button small primary small-only-expanded']")
    driver.execute_script("arguments[0].click();", elem)

    tables = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, "table")))

    table = tables[1]

    df = pd.read_html(table.get_attribute('outerHTML'))

    df2 = df[0]
    df2.columns = ['Loc','Disp']
    df2['Disp'] = pd.to_datetime(df2['Disp'],errors='coerce',format='%d %B, %Y')
    df2['Update'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    df2 = df2.dropna(subset='Disp')
    
    if not(df2.empty):
        output_table2 = df2.to_json(orient="split")
        data2 = {
        "username" : "VISA good bot"
        }
        data2["embeds"] = [
            {
        "description" : output_table2,
        "title" : "new Appointments found"
            }
        ]
        result2 = requests.post(WEBHOOK_FILTER, json = data2)

    output_table=df[0].to_json(orient="split")

    update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 

    data = {
    "content" : update_time,
    "username" : "VISA bot"
    }

    data["embeds"] = [
        {
    "description" : output_table,
    "title" : "First Available Appointments"
        }
    ]

    result = requests.post(WEBHOOK, json = data)

    driver.close();
    driver.quit();
    #return driver.find_element(By.CSS_SELECTOR, value="[name = 'commit']").text
