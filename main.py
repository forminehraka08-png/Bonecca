import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from plugin import PluginManager
from storage import StorageAPI

API_TOKEN = 'YOUR_BOT_TOKEN'  # <-- вставьте сюда ваш токен!

ADMIN_USER_ID = 7142531263  # Ваш Telegram user id

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

storage = StorageAPI('data/database.db')
plugins = PluginManager('plugins', storage)

RANKS = ["Member", "Moder", "Admin", "Stmin", "Zamcrea", "Crea"]

async def on_startup():
    await storage.init_db()
    plugins.load_plugins()

@dp.message(Command(commands=["start"]))
async def cmd_start(message: types.Message):
    await storage.register_user(message.from_user.id, message.from_user.first_name, message.chat.id)
    await message.answer("Добро пожаловать, {}!".format(message.from_user.first_name))

@dp.message(Command(commands=["i"]))
async def cmd_i(message: types.Message):
    rank = await storage.get_user_rank(message.from_user.id)
    await message.answer(f"Ваш ранг: {rank}")

@dp.message(Command(commands=["help"]))
async def cmd_help(message: types.Message):
    help_text = await storage.get_help_text()
    help_addons = plugins.get_help_addons()
    await message.answer(help_text + "\n" + "\n".join(help_addons))

@dp.message(Command(commands=["plugins"]))
async def cmd_plugins(message: types.Message):
    plist = plugins.get_plugins_list()
    await message.answer("Список плагинов:\n" + "\n".join(plist))

@dp.message(Command(commands=["admin"]))
async def cmd_admin(message: types.Message):
    if message.from_user.id != ADMIN_USER_ID:
        await message.reply("Нет доступа.")
        return
    webapp_url = "http://localhost:8080/webadmin/index.html"
    markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Открыть админку", web_app=WebAppInfo(url=webapp_url))]
    ], resize_keyboard=True)
    await message.answer("Нажмите кнопку для входа в админку.", reply_markup=markup)

@dp.message()
async def handler(message: types.Message):
    # Передача сообщения в плагины
    for plugin in plugins.plugins:
        try:
            await plugin.on_message(message, storage)
        except Exception as e:
            print(f"Ошибка в плагине {plugin.__class__.__name__}: {e}")

def start_bot():
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

if __name__ == "__main__":
    start_bot()