import os
import subprocess
import discord
import openai

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

# Thiết lập client cho Discord và OpenAI
client = discord.Client(intents=intents)
openai.api_key = OPENAI_API_KEY

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!chatgpt'):
        user_input = message.content[len('!chatgpt '):]

        # Gửi yêu cầu đến ChatGPT-4
        response = openai.Completion.create(
            model="gpt-4",
            prompt=user_input,
            max_tokens=150
        )
        response_text = response.choices[0].text.strip()

        # Trả lời trong Discord
        await message.channel.send(response_text)

# Chạy bot
client.run(DISCORD_TOKEN)
