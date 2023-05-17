from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton(text='/help')
b2 = KeyboardButton(text='/description')
b3 = KeyboardButton(text='Random')
b4 = KeyboardButton(text='/location')
kb.add(b1, b2).add(b3).add(b4)


kb_photo = ReplyKeyboardMarkup(resize_keyboard=True)
bp1 = KeyboardButton(text='Random')
bp2 = KeyboardButton(text='Main')
kb_photo.add(bp1, bp2)


ikb = InlineKeyboardMarkup(row_width=2)
ib1 = InlineKeyboardButton(text='❤', callback_data='like')
ib2 = InlineKeyboardButton(text='👎', callback_data='dislike')
ib3 = InlineKeyboardButton(text='Next Photo', callback_data='next')
ib4 = InlineKeyboardButton(text='Main', callback_data='main')

ikb.add(ib1, ib2).add(ib3).add(ib4)

