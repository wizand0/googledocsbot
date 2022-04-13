import telebot
from telebot import types

from google_sheets import get_total_revenue, add_row
from settings import TG_TOKEN, SHEET_URL
from utils import create_button

bot = telebot.TeleBot(TG_TOKEN, parse_mode=None)


BTN_DOC = create_button('doc', '📝 Показать документ')
BTN_REV = create_button('rev', '💲 Общая выручка')
BTN_NEW_ITEM = create_button('new_item', '✅ Добавить продажу')
BTN_CANCEL = create_button('cancel', '❌ Отмена')


def add_new_item(message):
    new_item = [message.from_user.first_name]
    msg = bot.send_message(message.chat.id, 'Введите объект')
    bot.register_next_step_handler(msg, add_title, new_item=new_item)


def add_title(message, **kwargs):
    new_item = kwargs.get('new_item', [])
    new_item.append(message.text)
    msg = bot.send_message(message.chat.id, 'Введите сумму выручки')
    bot.register_next_step_handler(msg, add_revenue, new_item=new_item)


def add_revenue(message, **kwargs):
    new_item = kwargs.get('new_item', [])
    new_item.append(message.text)
    add_row(new_item)

    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(BTN_DOC['text'], callback_data=BTN_DOC['key'])
    btn2 = types.InlineKeyboardButton(BTN_REV['text'], callback_data=BTN_REV['key'])
    btn3 = types.InlineKeyboardButton(BTN_CANCEL['text'], callback_data=BTN_CANCEL['key'])
    markup.add(btn1, btn2, btn3)

    bot.send_message(message.chat.id, 'Спасибо 👍. Я добавил в отчет новую продажу.',
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == BTN_DOC['key']:
            bot.send_message(call.message.chat.id,
                             f'<a href="{SHEET_URL}">Отчет по продажам</a>',
                             parse_mode='html')
        elif call.data == BTN_REV['key']:
            bot.send_message(call.message.chat.id,
                             f'Общая выручка = <b>{get_total_revenue()}</b>',
                             parse_mode='html')
        elif call.data == BTN_CANCEL['key']:
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text="ОК 👌",
                                  reply_markup=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    img = open('hello.png', 'rb')
    bot.send_sticker(message.chat.id, img)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(BTN_DOC['text'])
    btn2 = types.KeyboardButton(BTN_REV['text'])
    btn3 = types.KeyboardButton(BTN_NEW_ITEM['text'])
    markup.add(btn1, btn2, btn3)

    bot.reply_to(message, 'Привет! Это твой личный помощник. Чего изволите?', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == BTN_DOC['text']:
        bot.send_message(message.chat.id,
                         f'<a href="{SHEET_URL}">Отчет по продажам</a>',
                         parse_mode='html')
    elif message.text == BTN_REV['text']:
        bot.send_message(message.chat.id,
                         f'Общая выручка = <b>{get_total_revenue()}</b>',
                         parse_mode='html')
    elif message.text == BTN_NEW_ITEM['text']:
        add_new_item(message)

