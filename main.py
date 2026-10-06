import os
from random import choice
from aiohttp import web
import discord
from discord.ext import commands

# 1. 建立簡單的 HTTP 響應處理器 (供 UptimeRobot 與 Render 健檢使用)
async def handle_ping(request):
    return web.Response(text="Bot is alive!")


async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()

    # 取得 Render 自動指派的 PORT，預設 8080
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"網頁保活伺服器已啟動，監聽 Port: {port}")


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
        await ctx.send("請提供至少一個選項！範例：`!choose 珍珠奶茶 炒飯 牛排`"
                       )
        return

    selection = choice(options)
    # 直接發送選中的內容
    await ctx.send(selection)


# 3. 覆寫 Bot 啟動邏輯，在登入 Discord 前先啟動網頁伺服器
class CustomBot(commands.Bot):

    async def setup_hook(self):
        await start_web_server()


# 4. 主程式啟動
if __name__ == "__main__":
    TOKEN = os.getenv("TOKEN")

    bot = CustomBot(command_prefix=prefix, intents=intents)

    # 重新掛載指令與事件
    @bot.event
    async def on_ready():
        print(f'機器人已成功登入為 {bot.user}')

    @bot.command()
    async def choose(ctx, *, names: str):
        normalized_names = names.replace('，', ' ').replace(',', ' ')
        options = [item for item in normalized_names.split() if item]

        if not options:
            await ctx.send("請提供至少一個選項！範例：`!choose 珍珠奶茶 炒飯 牛排`"
                           )
            return

        selection = choice(options)
        await ctx.send(selection)

    if TOKEN:
        bot.run(TOKEN)
    else:
        print("錯誤：未在環境變數中填寫 TOKEN！")
