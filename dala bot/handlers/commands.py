from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from config import WEB_APP_URL

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
  name = message.from_user.first_name or "Қолданушы"

  keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
      text="📝 УБТ Тестін бастау",
      web_app=WebAppInfo(url=WEB_APP_URL)
    )],
    [InlineKeyboardButton(
      text="📊 Нәтижелер",
      callback_data="results"
    )]
  ])

  await message.answer(
    f"👋 Сәлем, {name}!\n\n"
    f"🎓 *УБТ Дайындық Ботына қош келдіңіз!*\n\n"
    f"📚 Бұл бот УБТ-ға дайындалуға көмектеседі:\n"
    f"• Математика\n"
    f"• Физика\n"
    f"• Химия\n"
    f"• Биология\n"
    f"• Тарих\n\n"
    f"Тестті бастау үшін батырманы басыңыз 👇",
    reply_markup=keyboard,
    parse_mode="Markdown"
  )

@router.message(Command("help"))
async def cmd_help(message: Message):
  await message.answer(
    "❓ *Көмек*\n\n"
    "/start — Ботты бастау\n"
    "/quiz — Тест бастау (bot ішінде)\n"
    "/score — Менің нәтижем\n"
    "/help — Осы мәзір",
    parse_mode="Markdown"
  )
