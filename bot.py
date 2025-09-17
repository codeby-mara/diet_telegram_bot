import os
import asyncio
import telegram
import json

TOKEN = str(os.getenv("TELEGRAM_TOKEN"))
CHAT_ID = str(os.getenv("TELEGRAM_CHAT_ID"))

if TOKEN == "None" or TOKEN.strip() == "":
    raise ValueError("TELEGRAM_TOKEN environment variable is not set or is empty")

if CHAT_ID == "None" or CHAT_ID.strip() == "":
    raise ValueError("TELEGRAM_CHAT_ID environment variable is not set or is empty")

with open("frequenze.json", "r") as f:
    cibi = json.load(f)
    


#async def main():
#    bot = telegram.Bot(TOKEN)
#    async with bot:
#        await bot.send_message(chat_id=CHAT_ID, text="Prova")
#
#
#if __name__ == '__main__':
#    asyncio.run(main())