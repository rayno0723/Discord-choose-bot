import os
from random import choice
from aiohttp import web
import discord
from discord import app_commands
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

# 2. Discord Bot 設定與自訂類別
class CustomBot(commands.Bot):
    async def setup_hook(self):
        # 啟動背景網頁伺服器
        await start_web_server()
        
        # 同步斜線指令到 Discord（讓 Discord 後台抓到全新的 /choose 指令）
        print("正在同步斜線指令到 Discord...")
        synced = await self.tree.sync()
        print(f"成功同步了 {len(synced)} 個斜線指令！")

# 開啟基本權限（斜線指令不需要 Message Content Intent）
intents = discord.Intents.default()
bot = CustomBot(command_prefix="!", intents=intents)

# 3. 機器人上線事件與自訂動態狀態
@bot.event
async def on_ready():
    print(f'機器人已成功登入為 {bot.user}')
    
    # 設定自訂「正在遊玩」狀態
    await bot.change_presence(
        activity=discord.Game(name="/choose 隨機選擇"),
        status=discord.Status.online
    )

# 4. 新增斜線指令 (/choose)
@bot.tree.command(name="choose", description="隨機選擇一個選項（用空格或逗號隔開）")
@app_commands.describe(options="請輸入選項，例如：珍珠奶茶 炒飯 牛排")
async def choose(interaction: discord.Interaction, options: str):
    # 將中文與英文逗號均轉換為空格，並依空白切割選項
    normalized_names = options.replace('，', ' ').replace(',', ' ')
    choices_list = [item for item in normalized_names.split() if item]

    if not choices_list:
        await interaction.response.send_message("請提供至少一個選項！", ephemeral=True)
        return

    selection = choice(choices_list)
    
    # 直接發送隨機挑選出的內容
    # Discord 介面會自動在訊息上方標註「使用者使用了 /choose options: ...」
    await interaction.response.send_message(selection)

# 5. 主程式啟動
if __name__ == "__main__":
    TOKEN = os.getenv("TOKEN")
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("錯誤：未在環境變數中填寫 TOKEN！")
