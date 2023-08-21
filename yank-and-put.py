from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
import time

# Configuration
GROUP_URL = 'https://www.facebook.com/groups/FBGID'
USERNAME = 'email@address'
PASSWORD = 'password'
TELEGRAM_TOKEN = "telgram_bot_token"
TELEGRAM_CHANNEL = "-100ID" # if the channel ID is for example 1192292378 then you should use -1001192292378\

# Initialize webdriver
service = Service(executable_path='/opt/homebrew/bin/chromedriver')
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 2  # 2: Block, 1: Allow, 0: Default
})
browser = webdriver.Chrome(service=service, options=options)

# Login to Facebook
browser.get('https://www.facebook.com')
username_elem = browser.find_element(By.ID, 'email')
username_elem.send_keys(USERNAME)
password_elem = browser.find_element(By.ID, 'pass')
password_elem.send_keys(PASSWORD)
login_btn = browser.find_element(By.NAME, 'login')
login_btn.click()
time.sleep(2)  # Wait for login to complete

# Go to Group and Scroll to load content
browser.get(GROUP_URL)
time.sleep(5)
for _ in range(10):  # Scroll 10 times (or as needed)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Allow content to load

# Extract images
img_elems = browser.find_elements(By.CSS_SELECTOR, 'img')
img_urls = [img.get_attribute('src') for img in img_elems]

# Close the browser
browser.close()

def post_image_to_telegram(img_url):
    base_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"
    send_photo_url = base_url + "sendPhoto"
    data = {
        "chat_id": TELEGRAM_CHANNEL,
        "photo": img_url,
        "caption": "From Facebook Group"
    }
    response = requests.post(send_photo_url, data=data)
    if response.status_code != 200:
        print(f"Failed to send image to Telegram. Error: {response.text}")

# Post to Telegram
for img_url in img_urls:
    post_image_to_telegram(img_url)
    time.sleep(5)  # Optional delay between posts