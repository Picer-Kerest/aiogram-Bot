import os
import random
from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove
from keyboards import kb, ikb
from dotenv import load_dotenv
load_dotenv()

bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot)

HELP_COMMANDS = """
/start - Запуск бота
/help - Список команд
/description - Описание бота
/location - Случайная локация
Main - Главное меню
Random - Почти случайное фото
"""

arr_photos = (
    'https://www.tripzaza.com/ru/destinations/wp-content/uploads/2018/06/1-Yosemite_Valley-e1528945436839.jpg',
    'https://www.tripzaza.com/ru/destinations/wp-content/uploads/2018/06/3-Sagano_bamboo_forest-e1528945736776.jpg',
    'https://www.tripzaza.com/ru/destinations/wp-content/uploads/2018/06/5-Salar_de_Uyuni-e1528946029666.jpg',
    'https://www.tripzaza.com/ru/destinations/wp-content/uploads/2018/06/6-Tianzi_Mountains-e1528946160313.jpg',
    'https://www.tripzaza.com/ru/destinations/wp-content/uploads/2018/06/14-Sea-cave_in_Algarve-e1528947255164.jpg',
    'https://www.tripzaza.com/ru/destinations/wp-content/uploads/2018/06/15-Great_Canyon-e1528947372785.jpg',
    'https://www.tripzaza.com/ru/destinations/wp-content/uploads/2018/06/30-Geiranger_Fjord-e1528957461850.jpg',
)

desc = (
    'Yosemite Valley, USA',
    'Bamboo Forest, Japan',
    'Salar de Uyuni, Bolivia',
    'Tianji Mountains, China',
    'Sea Cave in Algarve, Portugal',
    'Grand Canyon, USA',
    'Geiranger Fjord, Norway',
)

photos = dict(zip(arr_photos, desc))
random_photo = random.choice(arr_photos)
like_flag = False
dislike_flag = False


async def on_startup(_):
    print('The bot is running')


async def send_random_pic(message: types.Message):
    global random_photo
    random_photo = random.choice(arr_photos)
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=random_photo,
        caption=photos[random_photo],
        reply_markup=ikb
    )


@dp.message_handler(Text(equals='Random'))
async def open_photo_kb_command(message: types.Message):
    await message.answer(text='Random', reply_markup=ReplyKeyboardRemove())
    await send_random_pic(message)


@dp.message_handler(Text(equals='Main'))
async def main_command(message: types.Message):
    await message.answer(text='Welcome to the main menu', reply_markup=kb)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(text='Welcome', reply_markup=kb)


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer(text=HELP_COMMANDS)


@dp.message_handler(commands=['location'])
async def location_command(message: types.Message):
    await message.answer(text='Generating a random location')
    await bot.send_location(chat_id=message.chat.id, latitude=random.randint(0, 90), longitude=random.randint(0, 90))


@dp.message_handler(commands=['description'])
async def description_command(message: types.Message):
    await message.answer(text='The bot is able to send photos in random order')
    await bot.send_sticker(chat_id=message.from_user.id, sticker='CAACAgIAAxkBAAEI_4xkY6aqvXAXvPRpsUrSzXLHVE7GywAC1SIAAjrw-EuqVhe4O4uNEy8E')


@dp.callback_query_handler()
async def callback_random_photo(callback: types.CallbackQuery):
    # callback.answer() Обязательно для завершения
    global random_photo
    if callback.data == 'like':
        global like_flag
        if not like_flag:
            like_flag = True
            await callback.answer('Did you like it')
        else:
            await callback.answer('Have you already liked')
    elif callback.data == 'dislike':
        global dislike_flag
        if not dislike_flag:
            dislike_flag = True
            await callback.answer("You didn't like it")
        else:
            await callback.answer('You have already set a dislike, we understand')
    elif callback.data == 'main':
        await callback.message.answer(text='Welcome to the main menu', reply_markup=kb)
        await callback.answer()
    else:
        random_photo = random.choice(tuple(filter(lambda x: x != random_photo, arr_photos)))
        # Это работает потому что random.choice выбирает одну фотографию.
        # Следовательно можно сделать выборку без этой фотографии
        media = types.InputMediaPhoto(random_photo, caption=photos[random_photo])
        await callback.message.edit_media(media=media, reply_markup=ikb)
        # Редактируем ранее отправленное фото.

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)

