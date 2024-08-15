import os
import subprocess
import discord
import openai
from discord import app_commands
from discord.ext import commands

# Cài đặt thư viện cần thiết nếu chưa được cài đặt
def install(package):
    subprocess.check_call([os.sys.executable, "-m", "pip", "install", package])

install('discord.py')
install('openai')

# Đặt Token của bot và API Key của OpenAI
DISCORD_TOKEN = ''
OPENAI_API_KEY = ''

# Thiết lập intents cho bot
intents = discord.Intents.default()
intents.message_content = True  # Kích hoạt quyền truy cập nội dung tin nhắn

# Thiết lập bot
bot = commands.Bot(command_prefix="/", intents=intents)

# Khởi tạo OpenAI API key
openai.api_key = OPENAI_API_KEY

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

@bot.tree.command(name="chatgpt")
async def chatgpt(interaction: discord.Interaction, *, prompt: str):
    """Gửi yêu cầu đến ChatGPT và nhận phản hồi"""
    try:
        # Gửi yêu cầu đến ChatGPT-3.5 Turbo
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        response_text = response.choices[0].message['content'].strip()

        # Trả lời trong Discord
        await interaction.response.send_message(response_text)

    except Exception as e:
        await interaction.response.send_message(f"Đã xảy ra lỗi: {str(e)}", ephemeral=True)

# Chạy bot
bot.run(DISCORD_TOKEN)
