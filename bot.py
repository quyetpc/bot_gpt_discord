import os
import subprocess
import json
import discord
import openai
from discord.ext import commands

# Đường dẫn đến file JSON chứa token và API key
config_file = 'config.json'

# Hàm để kiểm tra và tạo file JSON nếu chưa tồn tại
def check_and_create_config():
    if not os.path.exists(config_file):
        print(f"File {config_file} không tồn tại. Đang tạo file...")
        default_config = {
            "DISCORD_TOKEN": "YOUR_DISCORD_BOT_TOKEN",
            "OPENAI_API_KEY": "YOUR_OPENAI_API_KEY"
        }
        with open(config_file, 'w') as f:
            json.dump(default_config, f, indent=4)
        print(f"Đã tạo file {config_file}. Hãy điền token và API key rồi chạy lại chương trình.")
        exit()

# Hàm để tải cấu hình từ file JSON
def load_config():
    with open(config_file, 'r') as f:
        return json.load(f)

# Kiểm tra và tạo file config nếu cần
check_and_create_config()

# Tải cấu hình từ file JSON
config = load_config()

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

# Đặt Token của bot và API Key của OpenAI từ file JSON
DISCORD_TOKEN = config['DISCORD_TOKEN']
OPENAI_API_KEY = config['OPENAI_API_KEY']

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
