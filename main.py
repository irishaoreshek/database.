import asyncio
import logging
import pymysql

from aiogram import Bot, Dispatcher

from config_data.config import load_config, Config
from keyboards.main_menu import set_main_menu
from handlers.user import register_user_handlers


logger = logging.getLogger(__name__)

def register_all_handlesrs(dp: Dispatcher) -> None:
    register_user_handlers(dp)

def connection_database(config: Config):
    try:
        connection = pymysql.connect(
            host=config.database.host,
            port=int(config.database.port),
            user=config.database.user,
            password=config.database.password,
            database=config.database.database
        )
        print("Подключение прошло успено!")
    except Exception as ex:
        print("Ошибка работы бд")
        print(ex)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s'
    )
    logger.info("Starting bot")
    
    config: Config = load_config('.env')

    bot: Bot = Bot(token=config.tgBot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher(bot)

    await set_main_menu(dp)

    register_all_handlesrs(dp)
    connection_database(config)

    try:
        await dp.start_polling()
    finally:
        await bot.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemError):
        logger.error("Bot Stopped!")
