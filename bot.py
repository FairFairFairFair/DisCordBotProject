import discord
import requests
import os
from dotenv import load_dotenv
# กำหนด Token สำหรับ Discord bot

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
# สร้าง Intents เพื่อให้สามารถใช้งานฟีเจอร์บางอย่างของ Discord
intents = discord.Intents.default()
intents.message_content = True  # เปิดใช้งานการรับข้อความจาก Discord

client = discord.Client(intents=intents)

# เมื่อ bot พร้อมใช้งาน
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

# เมื่อได้รับข้อความจากผู้ใช้
@client.event
async def on_message(message):
    if message.author == client.user:  # ถ้าเป็นข้อความจาก bot เองไม่ต้องตอบกลับ
        return

    if message.content.startswith('!gen'):  # เช็คคำสั่งที่เริ่มต้นด้วย !gen
        prompt = message.content[len('!gen '):]  # เอาคำหลัง !gen มาเป็น prompt

        # ส่งคำขอไปที่ API
        try:
            response = requests.post(
                "http://localhost:8000/generate",  # URL ของ API
                json={"prompt": prompt}  # ส่ง prompt ในรูปแบบ JSON
            )

            # ตรวจสอบการตอบกลับจาก API
            if response.status_code == 200:
                result = response.json()
                await message.channel.send(result["response"])  # ส่งข้อความที่ได้รับจาก API ไปที่ช่อง Discord
            else:
                await message.channel.send("❌ ขอโทษครับ, ไม่สามารถตอบกลับได้ในขณะนี้.")
        except Exception as e:
            await message.channel.send(f"❌ เกิดข้อผิดพลาด: {e}")

# เริ่มต้น bot
client.run(TOKEN)
