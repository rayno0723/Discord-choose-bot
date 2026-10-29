import random
import discord
from discord.ext import commands

intents = discord.Intents.default()
# 註：這裡不需要開啟 message_content intent，因為 @Mention 訊息 Discord 會自動放行內容

# 設定前綴為「標記機器人」加 !choose，或是標記機器人後接任何前綴
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)


@bot.event
async def on_ready():
    print(f"機器人已上線：{bot.user.name}")


# 使用 *options 接收所有空格分隔的選項
@bot.command(name="choose")
async def choose(ctx, *options: str):
    # 防呆機制：如果沒有提供選項或只給了一個選項
    if len(options) < 2:
        await ctx.send("請至少提供兩個選項！範例：`@機器人 !choose 紅茶 綠茶 奶茶`")
        return

    # 隨機抽取一個選項
    selected = random.choice(options)
    await ctx.send(f"🎲 隨機選擇結果：**{selected}**")


# 請替換為你的 Bot Token
bot.run("YOUR_BOT_TOKEN")
