from telebot.async_telebot import AsyncTeleBot
import asyncio
import requests
from bs4 import BeautifulSoup
import aiohttp
import time


bot = AsyncTeleBot('6883509812:AAHpXd-uR0gOfvKNGP-p2tmVT5Zzs-sg1bs')


@bot.message_handler(commands=['start'])
async def start_message(message):
    await bot.send_message(message.chat.id, """
Здарова. 
Криптой заинтересовался? 
у нас есть немного...
    """)


@bot.message_handler(commands=['course'])
async def course_parse(message):
    BTC = get_rates()
    await bot.send_message(message.chat.id, f"""
    Курс битка: {BTC}$
    """)


def get_rates():
    url = 'https://www.rbc.ru/crypto/currency/btcusd'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find('div', class_='chart__subtitle js-chart-value')
    btc_value = list(quotes)[0].replace('\n                ', '')
    return btc_value


@bot.message_handler(commands=['regular'])
async def regular_message(message):
    course_list: list[int] = [0, 0]
    while True:
        time.sleep(3)
        last_course: int = get_rates()
        course_list.append(last_course)
        if course_list[0] - last_course >= 3000:
            await bot.send_message(message.chat.id, f'''
            test {course_list}
            ''')
            course_list[0] = last_course
        else:
            await bot.send_message(message.chat.id, 'Курс BTC не поменялся')


if __name__ == '__main__':
    asyncio.run(bot.polling())
