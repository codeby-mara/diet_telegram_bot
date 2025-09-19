import os
import asyncio
import telegram
import json
from PIL import Image, ImageDraw, ImageFont

def generate_chore_chart(headers, rows, filename="Dieta.png"):
    # settings
    cell_width = 200
    cell_height = 60
    font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/Ubuntu-C.ttf", (cell_width/cell_height) * 5)
    
    # calculate size
    img_width = cell_width * len(headers)
    img_height = cell_height * (len(rows) + 1)
    
    # create image
    img = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(img)
    
    # draw header
    for i, header in enumerate(headers):
        x0, y0 = i * cell_width, 0
        x1, y1 = x0 + cell_width, cell_height
        draw.rectangle([x0, y0, x1, y1], outline="black", fill="blue")
        draw.text((x0 + 10, y0 + 20), header, fill="black", font=font)
    
    # draw rows
    for row_i, row in enumerate(rows):
        for col_i, cell in enumerate(row):
            x0, y0 = col_i * cell_width, (row_i + 1) * cell_height
            x1, y1 = x0 + cell_width, y0 + cell_height
            draw.rectangle([x0, y0, x1, y1], outline="black", fill="white")
            draw.text((x0 + 10, y0 + 20), str(cell), fill="black", font=font)
    
    img.save(filename)
    return filename


# Example usage
headers = ["", "Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
with open("frequenze.json", "r") as f:
    cibi = json.load(f)
rows = [
    ["Pranzo", "temp", "temp","temp","temp","temp","temp","temp"],
    ["Cena", "temp", "temp","temp","temp","temp","temp","temp"]
]

generate_chore_chart(headers, rows)

TOKEN = str(os.getenv("TELEGRAM_TOKEN"))
CHAT_ID = str(os.getenv("TELEGRAM_CHAT_ID"))

if TOKEN == "None" or TOKEN.strip() == "":
    raise ValueError("TELEGRAM_TOKEN environment variable is not set or is empty")

if CHAT_ID == "None" or CHAT_ID.strip() == "":
    raise ValueError("TELEGRAM_CHAT_ID environment variable is not set or is empty")





#async def main():
#    bot = telegram.Bot(TOKEN)
#    async with bot:
#        await bot.send_message(chat_id=CHAT_ID, text="Prova")
#
#
#if __name__ == '__main__':
#    asyncio.run(main())