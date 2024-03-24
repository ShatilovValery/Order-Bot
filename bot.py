from aiogram import executor


# Функция котора выполняется при запуске
#Function that is executed at startup
async def on_startup(_):
    print("************************")
    print("* BOT HAS BEEN STARTED *")
    print("************************")


if __name__ == '__main__':
    from user_handler import dp
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)