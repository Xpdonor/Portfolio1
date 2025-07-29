from flask import Flask, request
import json
import requests
from telegram import Bot

app = Flask(__name__)
BOT_TOKEN = 'bot token'
bot = Bot(token=BOT_TOKEN)

def get_unused_config():
    with open("configs.json", "r") as f:
        configs = json.load(f)
    for config in configs:
        if not config["used"]:
            config["used"] = True
            with open("configs.json", "w") as f:
                json.dump(configs, f, indent=2)
            return config["text"]
    return None

@app.route("/verify", methods=["POST"])
def verify():
    data = request.json
    if data["status"] == 100:
        chat_id = int(data["order_id"])
        config = get_unused_config()
        if config:
            bot.send_message(chat_id=chat_id, text=f"✅succesfull payment!\n\n📄 your config:\n{config}")
        else:
            bot.send_message(chat_id=chat_id, text="❌ No config avalable")
    return "OK"

if __name__ == "__main__":
    app.run(port=5000)
