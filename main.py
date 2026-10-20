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

# 2. Discord Bot 設定
class CustomBot(commands.Bot):
    async def setup_hook(self):
        # 啟動網頁保活伺服器
        await start_web_server()
        
        # 👈 關鍵：必須加上這行，斜線指令才會同步到 Discord！
        print("正在同步斜線指令到 Discord...")
        synced = await self.tree.sync()
        print(f"成功同步了 {len(synced)} 個斜線指令！")

intents = discord.Intents.default()
bot = CustomBot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'機器人已成功登入為 {bot.user}')
    
    # 設定自訂「正在遊玩」狀態
    custom_status = "!choose 隨機選擇"
    await bot.change_presence(
        activity=discord.Game(name=custom_status),
        status=discord.Status.online
    )

# 斜線指令 (/choose)
@bot.tree.command(name="choose", description="隨機選擇一個選項（用空格或逗號隔開）")
@app_commands.describe(options="請輸入選項，例如：1 2 3")
async def slash_choose(interaction: discord.Interaction, options: str):
    normalized_names = options.replace('，', ' ').replace(',', ' ')
    choices_list = [item for item in normalized_names.split() if item]

    if not choices_list:
        await interaction.response.send_message("請提供至少一個選項！", ephemeral=True)
        return

    selection = choice(choices_list)
    
    # 第一行顯示原始指令文字，第二行顯示選中的結果
    message_content = f"!choose {options}\n{selection}"
    await interaction.response.send_message(message_content)

# 3. 主程式啟動
if __name__ == "__main__":
    TOKEN = os.getenv("TOKEN")
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("錯誤：未在環境變數中填寫 TOKEN！")
