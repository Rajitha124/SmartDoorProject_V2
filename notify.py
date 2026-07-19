import requests

BOT_TOKEN = "8624810799:AAFiDMj9Wf4zfr6c42nLVHXLpx-dRs0ivxI"
CHAT_ID = "1272708969"

def send_alert(image_url):

    message = "🚨 Unknown visitor detected!\n\nPlease check your Smart Door Dashboard."

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    data = {
        "chat_id": CHAT_ID,
        "caption": message,
        "photo": image_url
    }

    requests.post(url, data=data)