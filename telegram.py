import requests

url = "https://api.telegram.org/bottoken/getMe"

headers = {
    "accept": "application/json",
    "User-Agent": "Telegram Bot SDK - (https://github.com/irazasyed/telegram-bot-sdk)"
}

response = requests.post(url, headers=headers)

print(response.text)