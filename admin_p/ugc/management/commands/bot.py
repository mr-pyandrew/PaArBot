import datetime
import json
import os
import random
import re
import time
import pytz
import logging
from django.utils import timezone
from django.db.models import F
from django.core.management import BaseCommand

from telegram.ext.dispatcher import run_async
from telegram import ReplyKeyboardMarkup, Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, \
    InlineQueryResultArticle, InputTextMessageContent, InputMediaPhoto, KeyboardButton, LabeledPrice, InputMediaVideo
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, Job, \
    InlineQueryHandler, PreCheckoutQueryHandler

from . import constants
from ...models import Users, Bearing, Leaf, Tree

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


#  C:\Users\user\Desktop\Успех ЗДЕСЬ!\Проекты\RS_Parser_bot\admin_p


def start(update, context):
    message = update.message
    bot = context.bot
    p, flag = Users.objects.get_or_create(
        external_id=message.chat.id,
        defaults={
            'user_name': message.chat.username,
            'first_name': message.chat.first_name,
        }
    )
    if flag:
        bot.send_message(message.chat.id,
                         'Подши́пник (от «под шип») — сборочный узел, являющийся частью опоры или упора и поддерживающий вал, ось или иную подвижную конструкцию с заданной жёсткостью. Фиксирует положение в пространстве, обеспечивает вращение, качение с наименьшим сопротивлением, воспринимает и передаёт нагрузку от подвижного узла на другие части конструкции[1].')
        main_menu(update, context)
    else:
        main_menu(update, context)


def main_menu(update, context: CallbackContext):
    message = update.message
    bot = context.bot
    buttons = []
    button_m = []
    text = 'Главное меню🖥\n'
    leafs = Leaf.objects.filter(main_menu=True)
    for i in range(len(leafs)):
        button_m.append(
            InlineKeyboardButton(str(i+1), callback_data='menu_' + str(leafs[i].id))
        )
        if i % 2 == 0:
            buttons.append(button_m)
            button_m = []
        text += str(i+1) + ') ' + leafs[i].leaf + '\n'
    buttons.append(button_m)
    reply_markup = InlineKeyboardMarkup(buttons)
    bot.send_message(message.chat.id, text, reply_markup=reply_markup)


def answer_questions(update, context: CallbackContext):
    bot = context.bot
    message = update.message


def button(update, context):
    query = update.callback_query
    bot = context.bot
    if query.data == 'mainMenu':
        main_menu(query, context)
        bot.delete_message(message_id=query.message.message_id, chat_id=query.message.chat.id)
    elif query.data == 'delete':
        bot.delete_message(message_id=query.message.message_id, chat_id=query.message.chat.id)
    elif query.data == 'buy':
        try:
            bot.edit_message_caption(message_id=query.message.message_id,
                                     chat_id=query.message.chat.id,
                                     caption=query.message.caption + '\n\n<b>Телефон для связи:</b> +XXXXXXXXX\n\n<b>Email:</b> example@email.com',
                                     parse_mode=ParseMode.HTML
                                     )
        except:
            bot.edit_message_text(
                message_id=query.message.message_id,
                chat_id=query.message.chat.id,
                text=query.message.text + '\n\n<b>Телефон для связи:</b> +XXXXXXXXX\n\n<b>Email:</b> example@email.com',
                parse_mode=ParseMode.HTML
            )
        context.bot.answer_callback_query(
            callback_query_id=query.id,
            text='Спасибо, что подали заявку, в ближайшее время мы с вами свяжемся',
            show_alert=False,
            timeout=7,
        )
    elif query.data == 'Notificator':
        context.bot.answer_callback_query(
            callback_query_id=query.id,
            text='Мы Вас обязательно оповестим при появлении новых позиций в нашем каталоге✅',
            show_alert=True,
        )
    elif query.data.split('_')[0] == 'menu':
        buttons = []
        button_m = []
        text = ''
        try:
            leafs = Tree.objects.filter(branch=Leaf.objects.get(id=int(query.data.split('_')[1])))
            for i in range(len(leafs)):
                button_m.append(
                    InlineKeyboardButton(str(i+1), callback_data='menu_' + str(leafs[i].leaf.id))
                )
                text += str(i+1) + ') ' + leafs[i].leaf.leaf + '\n'
                if i % 9 == 0:
                    buttons.append(button_m)
                    button_m = []
            buttons.append(button_m)
        except:
            pass
        if buttons != [[]]:
            buttons.append([InlineKeyboardButton('Главное меню🖥', callback_data='mainMenu')])
            reply_markup = InlineKeyboardMarkup(buttons)
            bot.send_message(
                query.message.chat.id,
                Leaf.objects.get(id=int(query.data.split('_')[1])).leaf + '\n' + text,
                reply_markup=reply_markup
            )
            bot.delete_message(message_id=query.message.message_id, chat_id=query.message.chat.id)
        else:
            buttons = []
            try:
                tree = Tree.objects.get(leaf=Leaf.objects.get(id=int(query.data.split('_')[1])))
                items = Bearing.objects.filter(tree=tree)
                for i in range(len(items)):
                    button_m.append(
                        InlineKeyboardButton(items[i].title, callback_data='product_' + str(items[i].id))
                    )
                    if i % 4 == 0:
                        buttons.append(button_m)
                        button_m = []
                buttons.append(button_m)
            except:
                pass
            if buttons != [[]]:
                buttons.append([InlineKeyboardButton('Главное меню🖥', callback_data='mainMenu')])
                reply_markup = InlineKeyboardMarkup(buttons)
                bot.send_message(
                    query.message.chat.id,
                    Leaf.objects.get(id=int(query.data.split('_')[1])).leaf,
                    reply_markup=reply_markup
                )
                bot.delete_message(message_id=query.message.message_id, chat_id=query.message.chat.id)
            else:
                buttons.append([InlineKeyboardButton('Главное меню🖥', callback_data='mainMenu')])
                buttons.append([InlineKeyboardButton('Оповестить при поступлении📳', callback_data='Notificator')])
                reply_markup = InlineKeyboardMarkup(buttons)
                bot.send_message(
                    query.message.chat.id,
                    '❌На данный момент таких подшипников нет в каталоге🔜',
                    reply_markup=reply_markup
                )
                bot.delete_message(message_id=query.message.message_id, chat_id=query.message.chat.id)

    elif query.data.split('_')[0] == 'product':
        product = Bearing.objects.get(id=int(query.data.split('_')[1]))
        buttons = []
        buttons.append([InlineKeyboardButton('Купить', callback_data='buy')])
        buttons.append([InlineKeyboardButton('Назад', callback_data='delete')])
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            bot.send_photo(chat_id=query.message.chat.id,
                           photo=open(os.path.join(BASE_DIR, product.photo.url[1::]), 'rb'),
                           caption=f'⚙️<b>{product.title}</b>⚙️\n\n<b>Описание:</b>\n{product.description}',
                           parse_mode=ParseMode.HTML,
                           reply_markup=reply_markup)
        except:
            text_description = product.description\
                .replace("Параметр Обозначение Значение Единицы", "")\
                .replace("Характеристики подшипника", "<b>Характеристики подшипника</b>")
            text1 = text_description.split('<b>Характеристики подшипника</b>')[1].replace('\n\n', '')
            text2 = ''
            for i in text1.split('\n'):
                if i != '' and i != ' ' and i != '\n':
                    text2 += '<b>{}: </b><i>{}</i>\n\n'.format(' '.join(i.split()[0:-3]), ' '.join(i.split()[-3:]))
            text_description = text_description.split('<b>Характеристики подшипника</b>')[0] + '\n\n' + text2

            bot.send_message(query.message.chat.id,
                             text=f'⚙️<b>Подшипник {product.title}</b>⚙️\n\n<b>Характеристики подшипника:</b>\n\n{text_description}',
                             parse_mode=ParseMode.HTML,
                             reply_markup=reply_markup)


class Command(BaseCommand):
    help = 'Телеграм бот'

    def handle(self, *args, **options):
        updater = Updater(token=constants.TOKEN, use_context=True, workers=3)
        dispatcher = updater.dispatcher

        job_queue = updater.job_queue

        start_handler = CommandHandler('start', start)

        answer_handler = MessageHandler(Filters.all, answer_questions)
        updater.dispatcher.add_handler(CallbackQueryHandler(button))
        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(answer_handler)
        updater.start_polling(timeout=5)
