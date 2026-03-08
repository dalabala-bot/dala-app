from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

# ==============================
# УБТ СҰРАҚТАР БАЗАСЫ
# ==============================
QUESTIONS = [
  {
    "subject": "🔢 Математика",
    "question": "2x + 5 = 15 болса, x = ?",
    "options": ["3", "5", "7", "10"],
    "answer": 1
  },
  {
    "subject": "⚡ Физика",
    "question": "Жарықтың вакуумдағы жылдамдығы қанша?",
    "options": ["3×10⁶ м/с", "3×10⁸ м/с", "3×10¹⁰ м/с", "3×10⁴ м/с"],
    "answer": 1
  },
  {
    "subject": "🧪 Химия",
    "question": "Судың химиялық формуласы қандай?",
    "options": ["CO₂", "H₂SO₄", "H₂O", "NaCl"],
    "answer": 2
  },
  {
    "subject": "🧬 Биология",
    "question": "Адам ағзасында қанша хромосома бар?",
    "options": ["23", "44", "46", "48"],
    "answer": 2
  },
  {
    "subject": "📜 Тарих",
    "question": "Қазақстан тәуелсіздігін қай жылы алды?",
    "options": ["1989", "1990", "1991", "1992"],
    "answer": 2
  },
  {
    "subject": "🔢 Математика",
    "question": "π (пи) санының шамамен мәні қанша?",
    "options": ["2.14", "3.14", "4.14", "3.41"],
    "answer": 1
  },
  {
    "subject": "🌍 География",
    "question": "Қазақстанның астанасы қай қала?",
    "options": ["Алматы", "Шымкент", "Астана", "Қарағанды"],
    "answer": 2
  },
  {
    "subject": "⚡ Физика",
    "question": "Ньютонның бірінші заңы нені сипаттайды?",
    "options": ["Инерция", "Үдеу", "Күш", "Энергия"],
    "answer": 0
  },
  {
    "subject": "🧪 Химия",
    "question": "Алтынның химиялық белгісі қандай?",
    "options": ["Ag", "Al", "Au", "At"],
    "answer": 2
  },
  {
    "subject": "🔢 Математика",
    "question": "√144 = ?",
    "options": ["10", "11", "12", "14"],
    "answer": 2
  },
]

# ==============================
# FSM КҮЙЛЕРІ
# ==============================
class QuizState(StatesGroup):
  answering = State()

# ==============================
# ХЕНДЛЕРЛЕР
# ==============================
def get_question_keyboard(q_index: int):
  q = QUESTIONS[q_index]
  letters = ["A", "B", "C", "D"]
  buttons = [
    [InlineKeyboardButton(
      text=f"{letters[i]}. {opt}",
      callback_data=f"ans_{q_index}_{i}"
    )]
    for i, opt in enumerate(q["options"])
  ]
  return InlineKeyboardMarkup(inline_keyboard=buttons)

@router.message(Command("quiz"))
async def start_quiz(message: Message, state: FSMContext):
  await state.set_state(QuizState.answering)
  await state.update_data(q_index=0, score=0)
  await send_question(message, state, is_new=True)

async def send_question(message: Message, state: FSMContext, is_new=False):
  data = await state.get_data()
  idx = data.get("q_index", 0)

  if idx >= len(QUESTIONS):
    await show_final_score(message, state)
    return

  q = QUESTIONS[idx]
  text = (
    f"{q['subject']} | Сұрақ {idx + 1}/{len(QUESTIONS)}\n\n"
    f"❓ {q['question']}"
  )

  if is_new:
    await message.answer(text, reply_markup=get_question_keyboard(idx))
  else:
    await message.answer(text, reply_markup=get_question_keyboard(idx))

@router.callback_query(F.data.startswith("ans_"))
async def handle_answer(callback: CallbackQuery, state: FSMContext):
  _, q_idx, user_ans = callback.data.split("_")
  q_idx = int(q_idx)
  user_ans = int(user_ans)

  data = await state.get_data()
  current_idx = data.get("q_index", 0)

  if q_idx != current_idx:
    await callback.answer("Бұл сұраққа жауап бердіңіз!", show_alert=True)
    return

  q = QUESTIONS[q_idx]
  score = data.get("score", 0)

  await callback.message.edit_reply_markup(reply_markup=None)

  if user_ans == q["answer"]:
    score += 1
    result = "✅ Дұрыс! +1 ұпай"
  else:
    correct = q["options"][q["answer"]]
    result = f"❌ Қате! Дұрыс жауап: *{correct}*"

  await callback.answer()
  await callback.message.answer(result, parse_mode="Markdown")

  new_idx = q_idx + 1
  await state.update_data(q_index=new_idx, score=score)

  if new_idx >= len(QUESTIONS):
    await show_final_score(callback.message, state)
  else:
    q_next = QUESTIONS[new_idx]
    text = (
      f"{q_next['subject']} | Сұрақ {new_idx + 1}/{len(QUESTIONS)}\n\n"
      f"❓ {q_next['question']}"
    )
    await callback.message.answer(text, reply_markup=get_question_keyboard(new_idx))

async def show_final_score(message: Message, state: FSMContext):
  data = await state.get_data()
  score = data.get("score", 0)
  total = len(QUESTIONS)
  percent = round((score / total) * 100)

  if percent >= 80:
    grade = "🏆 Өте жақсы! УБТ-ға дайынсыз!"
  elif percent >= 60:
    grade = "👍 Жақсы! Тағы жаттығыңыз!"
  elif percent >= 40:
    grade = "📚 Орташа. Оқуды жалғастырыңыз!"
  else:
    grade = "💪 Тырысыңыз, бәрі болады!"

  keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔄 Қайта тапсыру", callback_data="restart_quiz")]
  ])

  await message.answer(
    f"🎉 *Тест аяқталды!*\n\n"
    f"📊 Нәтиже: *{score}/{total}* ({percent}%)\n\n"
    f"{grade}",
    reply_markup=keyboard,
    parse_mode="Markdown"
  )
  await state.clear()

@router.callback_query(F.data == "restart_quiz")
async def restart_quiz(callback: CallbackQuery, state: FSMContext):
  await callback.answer()
  await state.set_state(QuizState.answering)
  await state.update_data(q_index=0, score=0)
  q = QUESTIONS[0]
  text = f"{q['subject']} | Сұрақ 1/{len(QUESTIONS)}\n\n❓ {q['question']}"
  await callback.message.answer(text, reply_markup=get_question_keyboard(0))
