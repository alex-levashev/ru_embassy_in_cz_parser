#!/usr/bin/env python3

import os
import time
import logging
import requests
import json
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# === CONFIG ===
BOT_TOKEN = "TOKEN"
CHAT_ID = 66666
CAPTCHA_INPUT_ID = "ctl00_MainContent_txtCode"
URL = "url_from_email"
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

# === LOGGING ===
logging.basicConfig(level=logging.INFO)

# === Step 1: Capture CAPTCHA ===
logging.info("📸 Starting Chrome to fetch CAPTCHA...")

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)
driver.set_window_size(1920, 1080)
driver.get(URL)
time.sleep(2)

os.makedirs("output", exist_ok=True)
screenshot_path = "output/page.png"
cropped_path = "output/captcha.png"

driver.save_screenshot(screenshot_path)
image = Image.open(screenshot_path)
crop_box = (840, 475, 1040, 675)
captcha = image.crop(crop_box)
captcha.save(cropped_path)


# === Step 2: Send CAPTCHA to Telegram ===
logging.info("📤 Sending CAPTCHA to Telegram...")

with open(cropped_path, "rb") as f:
    files = {"photo": f}
    data = {"chat_id": CHAT_ID, "caption": "🧩 Enter captcha:"}
    response = requests.post(f"{TELEGRAM_API}/sendPhoto", data=data, files=files)
    logging.info(f"Sent CAPTCHA: {response.status_code}")

# === Step 3: Wait for user input ===
logging.info("⏳ Waiting for user input...")

last_update_id = None
captcha_code = None
timeout_seconds = 5
start_time = time.time()

logging.info("🕵️ Starting polling loop to get CAPTCHA input from user...")

import json

# Get last update ID to skip old messages
res = requests.get(f"{TELEGRAM_API}/getUpdates")
updates = res.json().get("result", [])
last_update_id = updates[-1]["update_id"] if updates else None
logging.info(f"📌 Starting from update_id = {last_update_id}")

captcha_code = None
timeout_seconds = 60
start_time = time.time()

while time.time() - start_time < timeout_seconds:
    params = {"timeout": 5}
    if last_update_id is not None:
        params["offset"] = last_update_id + 1

    try:
        res = requests.get(f"{TELEGRAM_API}/getUpdates", params=params)
        res.raise_for_status()
        result = res.json()
        updates = result.get("result", [])

        logging.debug(f"Raw response: {json.dumps(result, indent=2, ensure_ascii=False)}")

        for update in updates:
            last_update_id = update["update_id"]  # Always move forward

            message = update.get("message", {})
            sender_id = message.get("chat", {}).get("id")
            text = message.get("text")

            if sender_id == CHAT_ID and text:
                captcha_code = text.strip()
                logging.info(f"✅ Received CAPTCHA code: {captcha_code}")
                break

        if captcha_code:
            break

    except Exception as e:
        logging.error(f"❌ Polling error: {e}")

    time.sleep(1)

if not captcha_code:
    logging.warning("⚠️ No CAPTCHA code received.")
else:
    requests.post(f"{TELEGRAM_API}/sendMessage", data={"chat_id": CHAT_ID, "text": f"You've entered: {captcha_code}"})
    
# Input the user-entered CAPTCHA text into the field
input_element = driver.find_element(By.ID, "ctl00_MainContent_txtCode")
input_element.clear()
input_element.send_keys(captcha_code)
time.sleep(1)

# Optionally click the Submit button (adjust ID or name accordingly)
submit_button = driver.find_element(By.ID, "ctl00_MainContent_ButtonA")
submit_button.click()
time.sleep(1)

submit_button_2 = driver.find_element(By.ID, "ctl00_MainContent_ButtonB")
submit_button_2.click()
time.sleep(1)

element_text = driver.find_element(By.ID, "center-panel").text
requests.post(f"{TELEGRAM_API}/sendMessage", data={"chat_id": CHAT_ID, "text": f"Text {element_text}"})
time.sleep(1)

driver.save_screenshot(screenshot_path)
driver.quit()