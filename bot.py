import os
import subprocess
import discord
import openai
from discord.ext import commands

# Hạ cấp thư viện OpenAI xuống phiên bản 0.27.0 nếu cần
def install(package):
    subprocess.check_call([os.sys.executable, "-m", "pip", "install", package])

# Kiểm tra và cài đặt đúng phiên bản openai
def check_and_install_openai():
    try:
        import openai
        version = openai.__version__
        if version != '0.27.0':
            print(f"Hạ cấp openai từ phiên bản {version} xuống 0.27.0")
            install('openai==0.27.0')
            # Reload lại thư viện sau khi cài đặt phiên bản mới
            import importlib
            importlib.reload(openai)
    except ImportError:
        install('openai==0.27.0')

# Gọi hàm kiểm tra và cài đặt openai
check_and_install_openai()

# Đặt Token của bot và API Key của OpenAI
DISCORD_TOKEN = 'M TI3MjE2NDAyMTM0ODMzOTgzNA.GhgNuX.mbPt-vMaayNVmBP6HKU3y4hSMMEoWlHzO-38_E'
OPENAI_API_KEY = 's k-proj-juh_r2jUPSnLQ1i6zZQSKDlHl3argRxQYFrWbVqWKG4iBOvOxIARuvTUc4T3BlbkFJRmDQerb7YnCEcPe6SEte9NSTZZJW58wZFdQ9kubH-ADvCgE-dknFi3xeUA'

# Thiết lập intents cho bot
intents = discord.Intents.default()
intents.message_content = True  # Kích hoạt quyền truy cập nội dung tin nhắn

# Thiết lập bot với tiền tố lệnh là "!"
bot = commands.Bot(command_prefix="!", intents=intents)

# Khởi tạo OpenAI API key
openai.api_key = OPENAI_API_KEY

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# Đăng ký lệnh "!chatgpt"
@bot.command(name="chatgpt")
async def chatgpt(ctx, *, prompt: str):
    """Gửi yêu cầu đến ChatGPT và nhận phản hồi"""
    try:
        # Gửi yêu cầu đến ChatGPT-3.5 Turbo
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        response_text = response['choices'][0]['text'].strip()

        # Trả lời trong Discord
        await ctx.send(response_text)

    except Exception as e:
        await ctx.send(f"Đã xảy ra lỗi: {str(e)}")

# Chạy bot
bot.run(DISCORD_TOKEN)
