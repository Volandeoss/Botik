import aiogram
from aiogram import Bot, types, Dispatcher
from aiogram.utils import executor
from aiogram.types import (
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove,
)
from auth import spreadsheet_auth
from environs import Env

import os

env = Env()
env.read_env()


class Botik:
    def __init__(self, token: str):
        self.token = token
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher(self.bot)

        self.button_today = InlineKeyboardButton(
            "Сьогодні\Завтра", callback_data="tod/tom"
        )
        self.button_auth = KeyboardButton("Авторизуватись")
        self.button_schedule = InlineKeyboardButton("Розклад", callback_data="schedule")
        self.button_week = InlineKeyboardButton("Тиждень", callback_data="week")

        self.kb = ReplyKeyboardMarkup(resize_keyboard=True)
        self.kb.row(self.button_auth)
        self.kb1 = InlineKeyboardMarkup(resize_keyboard=True)
        self.kb1.row(self.button_schedule)
        self.kb2 = InlineKeyboardMarkup(resize_keyboard=True)
        self.kb2.row(self.button_today).row(self.button_week)

        @self.dp.message_handler(commands=["start"])
        async def startin(message):
            await message.answer("Стартуєм!!", reply_markup=self.kb)

        @self.dp.callback_query_handler(lambda c: c.data == "schedule")
        async def today(callback: types.CallbackQuery):
            await callback.message.answer("Виберіть опцію", reply_markup=self.kb2)

        # dlya inline knopok
        @self.dp.callback_query_handler(lambda c: c.data == "tod/tom")
        async def today(callback: types.CallbackQuery):
            await callback.message.answer("розклад на сьогодні просто бімба")

        email_waiting = False

        @self.dp.message_handler(text="Авторизуватись")
        async def repeat(message: types.Message):
            global email_waiting
            answerik = spreadsheet_auth()
            if type(answerik) == str:
                await message.answer("Ви авторизувались", reply_markup=self.kb1)
            elif answerik == 403:
                await message.answer("Будь-ласка перевірте пошту", reply_markup=self.kb)
            else:
                await message.answer("Щось пішло не так", reply_markup=self.kb)
            await message.answer(answerik)
            # await message.answer("<b>Вкажіть свою пошту</b>", parse_mode="HTML")
            email_waiting = False  #!!!!!!!!!

        @self.dp.message_handler()
        async def review_mail(message):
            global email_waiting
            if email_waiting:
                if message.text[-19:] == "@rcit.ukr.education":
                    await message.answer("да все круто", reply_markup=self.kb1)
                else:
                    await message.answer("перевірте пошту")
            email_waiting = False

        executor.start_polling(self.dp, skip_updates=True)


botik = Botik(env.str("TOKEN"))
# how
