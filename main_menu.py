from aiogram import Dispatcher, types

async def set_main_menu(dp: Dispatcher) -> None:
    main_menu_commands = [
        types.BotCommand(command="/start", description="Начало работы с ботом"),
        types.BotCommand(command="/help", description="Рукводство"),
        types.BotCommand(command="/stat", description="Ваша статистика игр"),
        types.BotCommand(command="/cancel", description="Отменить текущую игру"),
        types.BotCommand(command="/global", description="Глобальная статистика"),
        types.BotCommand(command="/all", description="Информация всего сервера")
    ]
    await dp.bot.set_my_commands(main_menu_commands)