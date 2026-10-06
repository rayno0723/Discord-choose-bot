import os
from random import choice
from threading import Thread
import discord
from discord.ext import commands
from flask import Flask

# 1. 建立簡單的 Flask 網頁伺服器供保活檢查
app = Flask('')


@app.route('/')
def home():
    return "Bot is alive!"


def run_web():
    # Render 會自動提供 PORT 環境變數
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)


def keep_alive():
    t = Thread(target=run_web)
    t.start()


# 2. Discord Bot 設定
prefix = ']]'
list_separator = ','

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=prefix, intents=intents)


@bot.event
async def on_ready():
    print(f'機器人已成功登入為 {bot.user}')


@bot.command()
async def choose(ctx, *, names: str):
    selection = choice(names.split(list_separator))
    await ctx.send(selection.strip())


# 3. 啟動網頁伺服器與機器人
if __name__ == "__main__":
    keep_alive()  # 背景啟動 Flask
    TOKEN = os.getenv("TOKEN")
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("錯誤：未填寫 TOKEN 環境變數！")