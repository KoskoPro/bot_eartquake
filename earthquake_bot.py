from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import config_bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
import requests
import re

API_TOKEN = config_bot.API_TOKEN
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    start_date = State()
    end_date = State()
    latitude = State()
    longitude = State()
    radius = State()
    magnitude = State()


@dp.message_handler(commands=['start', 'help', 'reset'])
async def send_welcome(msg: types.Message):
    await msg.reply("""Hey! I work with the USGS API.
    Send me the data: date, 
    end date, latitude, longitude, maximum 
    radius and minimum magnitude, and I will 
    show you a list of all earthquakes on these 
    dates in the specified radius""")
    await msg.answer("Please enter start date (YYYY-MM-DD)")
    await UserState.start_date.set()


@dp.message_handler(state=UserState.start_date)
async def get_start_date(message: types.Message, state: FSMContext):
    if not re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2}$', message.text):
        await message.reply('Invalid format date, please try again (YYYY-MM-DD)')
        return
    await state.update_data(start_date=message.text)
    await message.answer("Super. Next enter end date:")
    await UserState.end_date.set()


@dp.message_handler(state=UserState.end_date)
async def get_end_date(message: types.Message, state: FSMContext):
    if not re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2}$', message.text):
        await message.reply('Invalid format date, please try again (YYYY-MM-DD)')
        return
    await state.update_data(end_date=message.text)
    await message.answer("Good! Now enter latitude:")
    await UserState.latitude.set()


@dp.message_handler(state=UserState.latitude)
async def get_latitude(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        if 180 >= int(message.text) >= (-180):
            await state.update_data(latitude=message.text)
            await message.answer("Good! Now enter longitude:")
            await UserState.longitude.set()
        else:
            await message.reply('Latitude must be in range (-180; 180), please try again')
    else:
        await message.reply('Invalid latitude, please try again')
        return


@dp.message_handler(state=UserState.longitude)
async def get_longitude(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        if 90 >= int(message.text) >= (-90):
            await state.update_data(longitude=message.text)
            await message.answer("Good! Now enter max radius:")
            await UserState.radius.set()
        else:
            await message.reply('Longitude must be in range (-90; 90), please try again')
    else:
        await message.reply('Invalid longitude, please try again')
        return


@dp.message_handler(state=UserState.radius)
async def get_radius(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        if 20001 >= int(message.text) >= 0:
            await state.update_data(radius=message.text)
            await message.answer("Good! Now enter magnitude:")
            await UserState.magnitude.set()
        else:
            await message.reply('Radius must be in range (0; 20001), please try again')
    else:
        await message.reply('Invalid radius, please try again')
        return


@dp.message_handler(state=UserState.magnitude)
async def get_magnitude(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        if 10 >= int(message.text) >= 0:
            await state.update_data(magnitude=message.text)
            await message.answer("Super! Result: ")
            data = await state.get_data()
            result = request_url(data)
            if len(result) > 4096:
                for x in range(0, len(result), 4096):
                    await message.answer(f"{result[x:x + 4096]}")
            else:
                message.answer(result)

            await state.finish()
        else:
            await message.reply('Magnitude must be in range (0; 10), please try again')
    else:
        await message.reply('Invalid radius, please try again')
        return


def request_url(data):
    values = data.values()
    start_time, end_time, latitude, longitude, max_radius, magnitude = tuple(values)

    url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?'
    response = requests.get(url, headers={'Accept': 'Aplication/json'}, params={
        'format': 'geojson',
        'starttime': start_time,
        'endtime': end_time,
        'latitude': latitude,
        'longitude': longitude,
        'maxradiuskm': max_radius,
        'minmagnitude': magnitude
    })
    data = response.json()

    result = str()
    for i in range(len(data['features'])):
        result = result + f"{i + 1}. Place: {data['features'][i]['properties']['place']}.\
 Magnitude: {data['features'][i]['properties']['mag']}" + '\n'

    # answer to bot
    answer = f"{start_time} - {end_time}, Lt: {latitude},\
Lg: {longitude}, radius {max_radius}, minmagnitude {magnitude} \n\n{result}"

    return answer


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
