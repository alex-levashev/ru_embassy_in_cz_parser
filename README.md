# 🧩 CAPTCHA Telegram Bot (Headless Chrome + Telegram + OCR-ready)

This project automates the process of solving CAPTCHAs by:
1. Capturing the CAPTCHA image from a web page using Selenium and Chrome.
2. Sending the CAPTCHA image via Telegram.
3. Waiting for user input through Telegram.
4. Submitting the CAPTCHA and reporting the result back.

---

## 🧰 Requirements

- Docker installed (tested with Docker Desktop)
- A valid Telegram Bot Token
- Your Telegram user ID (to receive messages)

---

## 📁 Project Structure

```
.
├── Dockerfile          # Docker setup to run Python + Selenium + Chrome
├── script.py           # Main Python script
└── output/             # Folder for screenshots (auto-created)
```

---

## 🚀 Quick Start

### 1. Get Telegram Bot Token and Your Chat ID

- Create a bot with [@BotFather](https://t.me/BotFather) on Telegram
- Send a message to your bot
- Use this URL to get your `chat_id`:  
  ```
  https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
  ```

### 2. Update Configuration in `script.py`

Set the following at the top of the script:

```python
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = YOUR_TELEGRAM_USER_ID
URL = "URL_FROM_EMAIL"  # Web page with CAPTCHA
```

---

### 3. Build the Docker Image

```bash
docker build -t captcha-bot .
```

---

### 4. Run the Container

```bash
docker run --rm -v "$(pwd)/output:/app/output" captcha-bot
```

---

## 🧪 What It Does

1. Launches a headless Chrome browser to open the target web page.
2. Takes a screenshot and crops the CAPTCHA.
3. Sends the cropped image to you on Telegram.
4. Waits for you to reply with the CAPTCHA text.
5. Inputs the text, clicks submission buttons, and fetches results from the page.
6. Sends the result back to you on Telegram.

---

## 🛠 Notes

- Crop coordinates (`crop_box`) are hardcoded: `(840, 475, 1040, 675)`
- You may need to adjust them depending on the CAPTCHA position.
- Submission button IDs must be correct for the target website:
  ```python
  driver.find_element(By.ID, "ctl00_MainContent_ButtonA")
  driver.find_element(By.ID, "ctl00_MainContent_ButtonB")
  ```

---

## 🧼 Cleanup

You can stop the Docker container any time with `Ctrl+C`. Screenshots will be saved in the `output/` folder.

---

## 🛡 Disclaimer

This is a proof-of-concept project intended for educational or internal automation use only. Do not use this tool to violate website terms of service or bypass security measures.

---
