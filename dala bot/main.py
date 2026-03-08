import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import commands, quiz
from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

async def main():
  bot = Bot(token=BOT_TOKEN)
  dp = Dispatcher(storage=MemoryStorage())

  dp.include_router(commands.router)
  dp.include_router(quiz.router)

  print("✅ Бот іске қосылды!")
  await dp.start_polling(bot)

if __name__ == "__main__":
  asyncio.run(main())
