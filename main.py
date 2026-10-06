import os
from random import choice
from aiohttp import web
import discord
from discord.ext import commands

# 1. HTTP 網頁伺服器（供 UptimeRobot 保活）
async def handle_ping(request):
    return web.Response(text="Bot is alive!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"網頁保活伺服器已啟動，監聽 Port: {port}")

# 2. Discord Bot 設定
prefix = '!'

intents = discord.Intents.default()
intents.message_content = True

class CustomBot(commands.Bot):
    async def setup_hook(self):
        await start_web_server()

bot = CustomBot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready():
    print(f'機器人已成功登入為 {bot.user}')
    
    # ------------------ 設定自訂「正在遊玩」狀態 ------------------
    # 這裡可以自由改成你想顯示的文字（例如：!choose 隨機選擇）
    custom_status = "!choose 隨機選擇"
    
    await bot.change_presence(
        activity=discord.Game(name=custom_status),
        status=discord.Status.online  # 保持線上綠燈
    )
    # -----------------------------------------------------------

@bot.command()
async def choose(ctx, *, names: str):
    normalized_names = names.replace('，', ' ').replace(',', ' ')
    options = [item for item in normalized_names.split() if item]

    if not options:
        await ctx.send("請提供至少一個選項！範例：`!choose 珍珠奶茶 炒飯 牛排`")
        return

    selection = choice(options)
    await ctx.send(selection)

# 3. 主程式啟動
if __name__ == "__main__":
    TOKEN = os.getenv("TOKEN")
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("錯誤：未在環境變數中填寫 TOKEN！")
