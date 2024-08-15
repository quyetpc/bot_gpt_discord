import os
import subprocess
from flask import Flask
import threading
import discord
import openai

# Cài đặt thư viện cần thiết nếu chưa được cài đặt
def install(package):
    subprocess.check_call([os.sys.executable, "-m", "pip", "install", package])

install('flask')
install('discord.py')
install('openai')

# Khởi tạo ứng dụng Flask
app = Flask(__name__)

# Đặt Token của bot và API Key của OpenAI
DISCORD_TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'

# Thiết lập client cho Discord và OpenAI
client = discord.Client()
openai.api_key = OPENAI_API_KEY

# Flask route để kiểm tra trạng thái server
@app.route('/')
def home():
    return "Bot is running!"

# Hàm để chạy Discord bot trong một luồng riêng biệt
def run_discord_bot():
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

    client.run(DISCORD_TOKEN)

# Tạo một luồng mới để chạy bot
discord_thread = threading.Thread(target=run_discord_bot)
discord_thread.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
