import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
# from telegram.ext import updater

bot = telebot.TeleBot('5360620791:AAGQSfUeYBt56U1FhjNc6a_3iTpQdOB0HXU')
HEADERS = {'user-agent':
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    name = types.KeyboardButton('Search the plant by its name')
    cat = types.KeyboardButton('Search the plant by its category')
    markup.add(name, cat)
    mess = f'Hello, <b>{message.from_user.first_name}</b>'
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['search'])
def search(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("cat1", url="https://google.com"))
    markup.add(types.InlineKeyboardButton("cat2", url="https://google.com"))
    bot.send_message(message.chat.id, 'working...', parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=["text"])
def check_button_option(message):
    if message.text == 'Search the plant by its name':
        bot.send_message(message.chat.id, 'Enter the name of the plant', parse_mode='html')
    elif message.text == 'Search the plant by its category':
        bot.send_message(message.chat.id, 'This functional is not ready yet', parse_mode='html')
    else:
        check_text_message(message)


def check_text_message(message):
    bot.send_message(message.chat.id, 'You entered ' + message.text, parse_mode='html')
    message.text = message.text.replace(' ', '-')
    url = "https://bloomscape.com/plant-care-guides/"
    soup = BeautifulSoup(requests.get(url, headers=HEADERS).text, 'lxml')

    links = []
    tmp = url
    for link in soup.findAll('a', href=True):
        links.append(link['href'])
        if message.text.lower() in link.get('href'):
            tmp = link.get('href')
            break

    for img in soup.findAll('img'):
        if message.text.lower() in img.get('src'):
            image = img.get('src')
            break

    if tmp == url:
        bot.send_message(message.chat.id, 'Not found!', parse_mode='html')
    else:
        #bot.send_message(message.chat.id, tmp, parse_mode='html')
        soup1 = BeautifulSoup(requests.get(tmp, headers=HEADERS).text, 'lxml')
        bot.send_photo(message.chat.id, image)
        mess = soup1.find('article', 'guide-wrapper__flex plant-care__species').get_text()
        mess = mess.replace('\n\n\n\n', '\n')
        mess = mess.replace('\n\n', '\n')
        if len(mess) > 4095:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Show all", url=tmp))
            bot.send_message(message.chat.id, text=mess[0:2500],reply_markup=markup)
        else:
            bot.send_message(message.chat.id, text=mess)

        # plant - care - instruction


# updater.bot.setWebhook('https://plant-care-bot.herokuapp.com/' + '5360620791:AAGQSfUeYBt56U1FhjNc6a_3iTpQdOB0HXU')

bot.polling(none_stop=True)
