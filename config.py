
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging

#ID of the telegram account to which questions and requests will be sent
ADMIN_ID_TG = ""
logging.basicConfig(filename='logging.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
storage = MemoryStorage()

#BOT TOKEN
bot = Bot(token=str(""))
dp = Dispatcher(bot, storage=storage)