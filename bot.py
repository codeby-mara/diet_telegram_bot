import os
import asyncio
import telegram
import json
import random
from PIL import Image, ImageDraw, ImageFont
from datetime import date, timedelta 

def get_week():
    start = date.today()
    end = start + timedelta(days=6) 

    return start.strftime('%m/%d') + " - " + end.strftime('%m/%d')

def generate_diet(foods, filename="Dieta.png"):
    # settings
    headers = [get_week(), "Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
    cell_width = 200
    cell_height = 60
    font = ImageFont.truetype("Roboto-Medium.ttf", 30)
    
    # calculate size
    img_width = cell_width * len(headers)
    img_height = cell_height * (len(foods) + 1)
    
    # create image
    img = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(img)
    
    # draw header
    for i, header in enumerate(headers):
        x0, y0 = i * cell_width, 0
        x1, y1 = x0 + cell_width, cell_height
        draw.rectangle([x0, y0, x1, y1], outline="black", fill="#42aaf5")
        draw.text((x0 + 10, y0 + 20), header, fill="black", font=font)
    
    for row_i, row in enumerate(foods):
        for col_i, cell in enumerate(row):
            x0, y0 = col_i * cell_width, (row_i + 1) * cell_height
            x1, y1 = x0 + cell_width, y0 + cell_height
            fill_color = "#36abba" if col_i == 0 else "white"
            draw.rectangle([x0, y0, x1, y1], outline="black", fill=fill_color)
            draw.text((x0 + 10, y0 + 20), str(cell), fill="black", font=font)
    
    img.save(filename)

def get_foods(json_path):
    with open("frequenze.json", "r") as f:
        cibi = json.load(f)
        foods = [["Pranzo"] + [""] * 7, ["Cena"] + [""] * 7]
        old_food = ""
        
        for i in range(7):
            for j in range(2):
                food = None
                
                while food is None or (old_food == food and len(cibi) > 1):
                    food, num = random.choice(list(cibi.items()))

                cibi[food] -= 1
                foods[j][i+1] = food
                old_food = food
                if cibi[food] == 0:
                    cibi.pop(food)

    #check redudacy last day
    if(foods[0][7] == foods[1][7]):
        for i in range(1,len(foods[0])-1):
            if foods[0][i] != foods[1][7]:
                foods[0][i], foods[1][7] = foods[1][7], foods[0][i]
                break   
    return foods
   
TOKEN = str(os.getenv("TELEGRAM_TOKEN"))
CHAT_ID = str(os.getenv("TELEGRAM_CHAT_ID"))

if TOKEN == "None" or TOKEN.strip() == "":
    raise ValueError("TELEGRAM_TOKEN environment variable is not set or is empty")

if CHAT_ID == "None" or CHAT_ID.strip() == "":
    raise ValueError("TELEGRAM_CHAT_ID environment variable is not set or is empty")

async def main():
    bot = telegram.Bot(TOKEN)
    generate_diet(get_foods("frequenze.json"))
    async with bot:
        with open("Dieta.png", "rb") as img_file:
            await bot.send_photo(chat_id=CHAT_ID, photo=img_file, caption="Ecco la dieta di questa settimana")

    try:
        os.remove("Dieta.png")
    except Exception as e:
        print(f"Errore nella cancellazione dell'immagine: {e}")

if __name__ == '__main__':
    asyncio.run(main())

