import os
from random import choice
from threading import Thread
import discord
from discord.ext import commands
from flask import Flask

# 1. Flask 網頁伺服器（保活機制）
app = Flask('')


@app.route('/')
def home():
    return "Bot is alive!"


def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)


def keep_alive():
    t = Thread(target=run_web)
    t.start()


# 2. Discord Bot 設定
prefix = '!'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=prefix, intents=intents)


@bot.event
async def on_ready():
    print(f'機器人已成功登入為 {bot.user}')


@bot.command()
async def choose(ctx, *, names: str):
    # 將中文與英文逗號均轉換為空格，並依空白切割選項
    normalized_names = names.replace('，', ' ').replace(',', ' ')
    options = [item for item in normalized_names.split() if item]

    if not options:
        await ctx.send("請提供至少一個選項！範例：`!choose 珍珠奶茶 炒飯 牛排`")
        return

    selection = choice(options)
    # 直接發送選中的內容
    await ctx.send(selection)


# 3. 啟動服務
if __name__ == "__main__":
    keep_alive()
    TOKEN = os.getenv("TOKEN")
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("錯誤：未在環境變數中填寫 TOKEN！")
