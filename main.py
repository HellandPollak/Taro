from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.filters import Command
from urllib.parse import quote
import asyncio
import logging
import sqlite3
import json
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Пожалуйста, укажите токен вашего бота в .env файле.")

# Инициализация бота и диспетчера
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()

# Настройка базы данных
conn = sqlite3.connect("bot_users.db")
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    current_question TEXT DEFAULT NULL
)
''')
conn.commit()

# Главное меню
menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Задать вопрос")]
    ],
    resize_keyboard=True
)

@router.message(Command(commands=['start']))
async def send_welcome(message: Message):
    """Обработчик команды /start."""
    user_id = message.from_user.id
    # Добавляем пользователя в базу данных, если его там нет
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    await message.answer(
        "Привет! Я Таро-бот. Напиши свой вопрос, выбери три карты, и я дам предсказание.",
        reply_markup=menu_keyboard
    )

@router.message(lambda message: message.text == "Задать вопрос")
async def ask_question(message: Message):
    """Обработчик кнопки 'Задать вопрос'."""
    await message.answer("Напиши свой вопрос для расклада.")

@router.message()
async def handle_question_input(message: Message):
    """Обработчик ввода вопроса."""
    user_id = message.from_user.id
    question = message.text

    # Сохраняем вопрос в базе данных
    cursor.execute("UPDATE users SET current_question = ? WHERE user_id = ?", (question, user_id))
    conn.commit()

    # Открываем мини-приложение с передачей вопроса
    web_app_url = f"https://hellandpollak.github.io/Taro/?question={quote(question)}"
    web_app = WebAppInfo(url=web_app_url)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Выбрать карты", web_app=web_app)]],
        resize_keyboard=True
    )
    await message.answer("Нажмите кнопку ниже, чтобы выбрать карты.", reply_markup=keyboard)

@router.message(lambda message: message.web_app_data)
async def handle_web_app_data(message: Message):
    """Обработчик данных из мини-приложения."""
    user_id = message.from_user.id
    try:
        data = json.loads(message.web_app_data.data)  # Получаем данные
        cards = data.get("cards")

        if not cards:
            await message.answer("Ошибка: данные из мини-приложения неполные.")
            return

        # Получение вопроса пользователя
        cursor.execute("SELECT current_question FROM users WHERE user_id = ?", (user_id,))
        question = cursor.fetchone()[0]

        if not question:
            await message.answer("Ошибка: не найден вопрос пользователя.")
            return

        # Формируем ответ (здесь можно добавить логику обработки карт и вопроса)
        response = f"Ваш вопрос: {question}\nВыбранные карты: {', '.join(cards)}\n\nТрактовка пока не реализована."

        # Сбрасываем сохранённый вопрос
        cursor.execute("UPDATE users SET current_question = NULL WHERE user_id = ?", (user_id,))
        conn.commit()

        await message.answer(response, reply_markup=menu_keyboard)

    except Exception as e:
        logging.error(f"Ошибка при обработке данных из мини-приложения: {e}")
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте ещё раз.")

async def main():
    """Основная функция для запуска бота."""
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        conn.close()  # Закрываем соединение с базой данных при завершении работы бота
