from bs4 import BeautifulSoup
from html import unescape
import re
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as firefox_option_driver

firefox_option = firefox_option_driver()
#firefox_option.add_argument("--headless")
firefox_option.add_argument("--no-sandbox")
firefox_option.add_argument("--disable-dev-shm-usage")
firefox_option.add_argument("--window-size=1280,720")
firefox_option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")


def wait_full_xpath(driver, xp):
    while True:
        try:
            driver.find_element(By.XPATH,xp)
            break
        except:
            sleep(3)



def extract_message(message_html):
    soup = BeautifulSoup(message_html, "html.parser")
    root = soup.find(attrs={"data-sid": True})

    message_id = None
    message_date = None
    if root:
        message_id = root.get("data-sid")
        message_date = root.get("data-date")

    texts = []
    for node in soup.select(".KTwPFW.YjkWXv"):
        for img in node.find_all("img"):
            img.replace_with(img.get("alt", ""))

        for br in node.find_all("br"):
            br.replace_with("\n")

        text = node.get_text("\n", strip=True)

        if text:
            texts.append(text)

    text = "\n\n".join(texts)

    text = unescape(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    return {
        "id": message_id,
        "date": message_date,
        "text": text.strip(),
    }



avg_sleep = 0.2
class BaleAccountApi:
    def start(hide=True):
        if hide == True:
            firefox_option.add_argument("--headless")
        driver = webdriver.Firefox(options=firefox_option)
        driver.get("https://web.bale.ai/login?redirectTo=/")
        sleep(avg_sleep)
        return driver

    def send_otp_code(driver, phone_number):
        wait_full_xpath(driver,'/html/body/div[1]/div/div/div/div/div[3]/div[2]/div/button')
        driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div[3]/div[2]/div/button').click()

        wait_full_xpath(driver, '//*[@id="Mobile number"]')
        driver.find_element(By.XPATH,'//*[@id="Mobile number"]').send_keys(phone_number)
        driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div/button').click()

        sleep(4.5)
        try:
            driver.find_element(By.XPATH,'//*[@id="Login Code"]')
            return True
        except:
            return False
    
    def login(driver, otp_code):
        wait_full_xpath(driver, '//*[@id="Login Code"]')
        driver.find_element(By.XPATH,'//*[@id="Login Code"]').clear()
        driver.find_element(By.XPATH,'//*[@id="Login Code"]').send_keys(str(otp_code))
        sleep(4.5)
        if 'Chat' in driver.page_source:
            return True
        else:
            return False
    
    def get_page_source(driver):
        return driver.page_source
    
    def open_chat(driver, chat_uid):
        driver.get(f"https://web.bale.ai/chat?uid={chat_uid}")
        sleep(avg_sleep)
        try:
            driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[4]/div[3]/div[3]/div').click()
            sleep(avg_sleep)
        except:
            pass
    
    def send_message(driver,message):
        try:
            driver.find_element(By.XPATH,'//*[@id="editable-message-text"]').send_keys(message)
            driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[4]/div[4]/div[1]/div[4]').click()
            sleep(avg_sleep)
            return True
        except:
            return False
        

    def convert_id_to_uid(driver, ID):
        driver.get(f"https://ble.ir/{ID}")
        sleep(avg_sleep)
        wait_full_xpath(driver, '/html/body/div/div[2]/div/div[4]/a[2]')
        driver.find_element(By.XPATH,'/html/body/div/div[2]/div/div[4]/a[2]').click()
        sleep(avg_sleep)
        r1 = driver.current_url
        while True:
            if r1 != driver.current_url and 'uid=' in driver.current_url:
                break
            sleep(1)
        return ((driver.current_url).split('uid=')[1])
  


    def readmessages(driver):
        sleep(1.5)
        wait_full_xpath(driver, "/html/body/div[1]/div/div/div/div[4]/div[3]")
        soup = BeautifulSoup(driver.page_source, "html.parser")

        result = []

        for msg in soup.select(".message-item"):
            data = extract_message(str(msg))

            if data["text"]:
                result.append(data)

        return {
            "number": len(result),
            "messages": result
        }
