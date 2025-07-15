# 🧩 CAPTCHA Telegram Bot for Russian Embassy Queue Checker 🇷🇺📬

This project automates the process of checking your place in the queue for passport renewal at the Russian Embassy in the Czech Republic.

Once you apply, you receive a unique link via email. This script:
1. Opens that link daily in a headless browser.
2. Captures the CAPTCHA image.
3. Sends it to your Telegram account.
4. Waits for your input.
5. Submits the CAPTCHA and fetches your position in the queue.
6. Sends the result back via Telegram.

> ⚠️ IMPORTANT: If you check the link more than 20 times per day, **your application may be cancelled**. This script is optimized to run **once a day via cron**.

---

## 🧰 Requirements

- Docker installed (tested with Docker Desktop)
- A valid Telegram Bot Token
- Your Telegram user ID (to receive messages)

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
docker build -t embassy-queue-checker .
```

---

### 4. Run the Container Manually

```bash
docker run --rm embassy-queue-checker
```

---

### 5. Add Cron Job for Daily Check

To run once per day (e.g. at 09:00), add this line to your crontab (`crontab -e`):

```bash
0 9 * * * docker run --rm embassy-queue-checker
```

Make sure Docker is available in your cron session and paths are absolute.

---

## 🧪 What It Does

1. Launches a headless Chrome browser to open the embassy queue link.
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

This tool is provided for personal use only. Do not abuse the embassy system. The developers are not responsible for any misuse or consequences. Be sure not to check more than 20 times per 24 hours.

---
