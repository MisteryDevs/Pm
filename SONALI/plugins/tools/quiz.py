import random
import requests
import asyncio
from pyrogram import filters
from pyrogram.enums import PollType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from SONALI import app

quiz_loops = {}
active_polls = {}

async def fetch_quiz_question():
    """Fetch a quiz question from the API."""
    categories = [9, 17, 18, 20, 21, 27]
    url = f"https://opentdb.com/api.php?amount=1&category={random.choice(categories)}&type=multiple"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "results" in data and data["results"]:
            question_data = data["results"][0]
            question = question_data["question"]
            correct_answer = question_data["correct_answer"]
            incorrect_answers = question_data["incorrect_answers"]

            all_answers = incorrect_answers + [correct_answer]
            random.shuffle(all_answers)
            correct_index = all_answers.index(correct_answer)

            return question, all_answers, correct_index
        else:
            return None, None, None
    except Exception as e:
        print(f"Error fetching quiz question: {e}")
        return None, None, None

async def send_quiz_poll(client, chat_id, user_id, interval):
    """Send a quiz poll with an open period."""
    question, all_answers, correct_index = await fetch_quiz_question()

    if not question or not all_answers:
        await client.send_message(chat_id, "⚠️ Failed to fetch a quiz question. Please try again later.")
        return

    # Delete previous poll if exists
    if user_id in active_polls:
        try:
            await client.delete_messages(chat_id=chat_id, message_ids=active_polls[user_id])
        except Exception as e:
            print(f"Failed to delete previous poll: {e}")

    poll_message = await client.send_poll(
        chat_id=chat_id,
        question=question,
        options=all_answers,
        is_anonymous=False,
        type=PollType.QUIZ,
        correct_option_id=correct_index,
        open_period=interval  
    )

    if poll_message:
        active_polls[user_id] = poll_message.id

@app.on_message(filters.command("quizon"))
async def quiz_on(client, message):
    user_id = message.from_user.id
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("30s", callback_data="30_sec"), InlineKeyboardButton("1min", callback_data="1_min")],
        [InlineKeyboardButton("5min", callback_data="5_min"), InlineKeyboardButton("10min", callback_data="10_min")],
    ])
    await message.reply_text("Choose your quiz interval:", reply_markup=keyboard)

@app.on_callback_query(filters.regex(r"^\d+_sec$|^\d+_min$"))
async def start_quiz_loop(client, callback_query):
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id

    if user_id in quiz_loops:
        await callback_query.answer("❌ Quiz already running!", show_alert=True)
        return

    intervals = {
        "30_sec": 30,
        "1_min": 60,
        "5_min": 300,
        "10_min": 600
    }
    interval = intervals.get(callback_query.data, 60)
    await callback_query.message.delete()
    await callback_query.message.reply_text(f"✅ Quiz started! New question every {interval} seconds.")

    quiz_loops[user_id] = True
    while quiz_loops.get(user_id, False):
        await send_quiz_poll(client, chat_id, user_id, interval)
        await asyncio.sleep(interval)

@app.on_message(filters.command("quizoff"))
async def stop_quiz(client, message):
    user_id = message.from_user.id
    if user_id not in quiz_loops:
        await message.reply_text("❌ No quiz is currently running.")
        return

    quiz_loops.pop(user_id)
    await message.reply_text("⛔ Quiz stopped.")

    if user_id in active_polls:
        try:
            await client.delete_messages(chat_id=message.chat.id, message_ids=active_polls[user_id])
            active_polls.pop(user_id)
        except Exception as e:
            print(f"Failed to delete active poll: {e}")
