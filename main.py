import asyncio
import logging
import sqlite3
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from mistralai import Mistral

# Загружаем токен из .env файла
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

if not BOT_TOKEN:
    raise ValueError("Пожалуйста, укажите токен вашего бота в .env файле.")
if not MISTRAL_API_KEY:
    raise ValueError("Пожалуйста, укажите API ключ Mistral AI в .env файле.")

# Инициализация бота и диспетчера
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()

# Инициализация Mistral AI
client = Mistral(api_key=MISTRAL_API_KEY)
model = "mistral-small-latest"

# Настройка базы данных
conn = sqlite3.connect("bot_users.db")
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    balance INTEGER DEFAULT 1,
    invited_by INTEGER,
    current_question TEXT DEFAULT NULL
)
''')
conn.commit()
cursor.execute("PRAGMA table_info(users)")
columns = [col[1] for col in cursor.fetchall()]
if "current_question" not in columns:
    cursor.execute("ALTER TABLE users ADD COLUMN current_question TEXT DEFAULT NULL")
    conn.commit()

# Главное меню
menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Задать вопрос")],
        [KeyboardButton(text="Купить расклады")],
        [KeyboardButton(text="Как работает бот")],
        [KeyboardButton(text="Количество раскладов: 0")]
    ],
    resize_keyboard=True
)

def update_balance_button(user_id):
    """Обновляет кнопку с балансом."""
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    balance = cursor.fetchone()[0]
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Задать вопрос")],
            [KeyboardButton(text="Купить расклады")],
            [KeyboardButton(text="Как работает бот")],
            [KeyboardButton(text=f"Количество раскладов: {balance}")]
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
    updated_menu = update_balance_button(user_id)
    await message.answer(
        "Привет! Я уникальный Таро-бот-эзотерик.\n"
        "Я помогу тебе сделать расклад на любой вопрос.",
        reply_markup=updated_menu
    )

@router.message(lambda message: message.text == "Задать вопрос")
async def ask_question(message: Message):
    """Обработчик кнопки 'Задать вопрос'."""
    user_id = message.from_user.id
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    balance = cursor.fetchone()[0]
    if balance > 0:
        await message.answer("Напиши свой вопрос для расклада.")
        cursor.execute("UPDATE users SET current_question = NULL WHERE user_id = ?", (user_id,))
        conn.commit()
    else:
        buy_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Приобрести 3 расклада за 50⭐", callback_data="buy_3")],
            [InlineKeyboardButton(text="Приобрести 10 раскладов за 90⭐", callback_data="buy_10")],
            [InlineKeyboardButton(text="Безлимит на месяц за 199⭐", callback_data="buy_month")],
            [InlineKeyboardButton(text="Получить бесплатно", callback_data="get_free")]
        ])
        await message.answer(
            "У вас нет доступных раскладов. Вы можете приобрести их или пригласить друга, чтобы получить бесплатно.",
            reply_markup=buy_keyboard
        )

@router.message(lambda message: message.text == "Купить расклады")
async def buy_spreads(message: Message):
    """Обработчик кнопки 'Купить расклады'."""
    buy_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Приобрести 3 расклада за 50⭐", callback_data="buy_3")],
        [InlineKeyboardButton(text="Приобрести 10 раскладов за 90⭐", callback_data="buy_10")],
        [InlineKeyboardButton(text="Безлимит на месяц за 199⭐", callback_data="buy_month")],
        [InlineKeyboardButton(text="Получить бесплатно", callback_data="get_free")]
    ])
    await message.answer(
        "Выберите один из вариантов покупки или получите бесплатные расклады, пригласив друга:",
        reply_markup=buy_keyboard
    )

@router.message(lambda message: message.text == "Как работает бот")
async def how_bot_works(message: Message):
    """Обработчик кнопки 'Как работает бот'."""
    await message.answer(
        "Как пользоваться ботом:\n"
        "1. Нажмите на кнопку 'Задать вопрос'.\n"
        "2. Напишите ваш вопрос.\n"
        "3. Выберите карты в мини-приложении.\n"
        "4. Дождитесь трактовки расклада.\n\n"
        "Пример вопроса:\n"
        "Стоит ли мне идти на мероприятие?\n\n"
        "Пример выпавших карт:\n"
        "Влюбленные, справедливость, перевернутый паж кубков.\n"
        
    )

@router.message(lambda message: message.text.startswith("Количество раскладов"))
async def check_balance(message: Message):
    """Обработчик кнопки 'Количество раскладов'."""
    user_id = message.from_user.id
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    balance = cursor.fetchone()[0]
    updated_menu = update_balance_button(user_id)
    await message.answer(
        f"У вас осталось {balance} расклад(ов).",
        reply_markup=updated_menu
    )

@router.callback_query(lambda callback_query: callback_query.data.startswith("buy_"))
async def handle_buy(callback_query):
    """Обработчик покупки раскладов."""
    user_id = callback_query.from_user.id
    if callback_query.data == "buy_3":
        cursor.execute("UPDATE users SET balance = balance + 3 WHERE user_id = ?", (user_id,))
        await callback_query.message.answer("Вы успешно приобрели 3 расклада.")
    elif callback_query.data == "buy_10":
        cursor.execute("UPDATE users SET balance = balance + 10 WHERE user_id = ?", (user_id,))
        await callback_query.message.answer("Вы успешно приобрели 10 раскладов.")
    elif callback_query.data == "buy_month":
        await callback_query.message.answer("Безлимит на месяц пока в разработке.")
    conn.commit()

@router.callback_query(lambda callback_query: callback_query.data == "get_free")
async def handle_get_free(callback_query):
    """Обработчик получения бесплатных раскладов по приглашению друга."""
    user_id = callback_query.from_user.id
    invite_link = f"https://t.me/your_bot_username?start={user_id}"
    await callback_query.message.answer(
        f"Пригласите друга, используя эту ссылку: {invite_link}\n"
        "Как только друг присоединится, вы получите 3 бесплатных расклада!"
    )

@router.message(lambda message: True)
async def handle_question_input(message: Message):
    """Обработчик ввода вопроса."""
    user_id = message.from_user.id
    cursor.execute("SELECT current_question FROM users WHERE user_id = ?", (user_id,))
    current_question = cursor.fetchone()[0]

    # Если текущий вопрос не задан, то это новый вопрос
    if current_question is None:
        question = message.text
        cursor.execute("UPDATE users SET current_question = ? WHERE user_id = ?", (question, user_id))
        conn.commit()
        await message.answer("Теперь укажи три карты через запятую.")
    else:
        # Если текущий вопрос уже задан, передаем сообщение следующему обработчику
        await handle_cards_input(message)

@router.message(lambda message: True)
async def handle_cards_input(message: Message):
    """Обработчик ввода карт."""
    user_id = message.from_user.id
    cursor.execute("SELECT current_question FROM users WHERE user_id = ?", (user_id,))
    current_question = cursor.fetchone()[0]

    # Если текущий вопрос задан, то это ввод карт
    if current_question:
        cards_input = message.text.strip()  # Убираем лишние пробелы в начале и конце
        cards = [card.strip() for card in cards_input.split(",")]  # Разделяем по запятым и убираем пробелы

        # Проверяем, что введено ровно три карты
        if len(cards) != 3:
            await message.answer("Пожалуйста, укажите ровно три карты через запятую.")
            return

        # Проверяем, что каждая карта не пустая
        if any(card == "" for card in cards):
            await message.answer("Названия карт не могут быть пустыми. Пожалуйста, укажите три карты через запятую.")
            return

        # Формируем строку с картами для отправки в Mistral AI
        cards_str = ", ".join(cards)
        result = query_mistral_ai(current_question, cards_str)

        if "Ошибка API" not in result:
            cursor.execute("UPDATE users SET balance = balance - 1 WHERE user_id = ?", (user_id,))
            cursor.execute("UPDATE users SET current_question = NULL WHERE user_id = ?", (user_id,))
            conn.commit()
            updated_menu = update_balance_button(user_id)
            await message.answer(f"Ваш расклад:\n\n{result}", reply_markup=updated_menu)
        else:
            await message.answer("Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте еще раз.")

def query_mistral_ai(question, cards):
    """Функция для запроса к Mistral AI."""
    try:
        chat_response = client.chat.complete(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "Ты специалист по картам Таро. Тебе задают вопрос и выбирают три карты. "
                        "Дай прогноз в дружелюбном и поддерживающем стиле. Ответ должен быть кратким, но завершённым и вмещаться в 350 токенов. "
                        " В ответе не используй символы вроде # или *. "
                        " Кратко опиши расклад и общий настрой."
                        " Анализ каждой карты: объясни значение каждой карты в контексте вопроса (2–3 предложения на карту)."
                        " Вывод: дай общий прогноз и рекомендации, как действовать."
                },
                {
                    "role": "user",
                    "content": f"Вопрос: {question}\nКарты: {cards}",
                },
            ],
            max_tokens=450
        )
        return chat_response.choices[0].message.content
    except Exception as e:
        logging.error(f"Ошибка при запросе к Mistral AI: {e}")
        return f"Ошибка API: {e}"

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