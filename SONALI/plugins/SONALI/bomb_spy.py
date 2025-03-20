import asyncio
import random
from pyrogram import filters
from SONALI import app

# 🧨 Time Bomb Game Variables
bomb_holder = None
game_active = False

# 🕵️ Spy Game Variables
players = {}
spy_game_active = False


# 🎭 Time Bomb Game
@app.on_message(filters.command("bomb"))
async def start_bomb_game(client, message):
    global bomb_holder, game_active
    if game_active:
        await message.reply_text("⚠️ Game already in progress!")
        return

    chat_id = message.chat.id
    members = [member.user.id async for member in client.get_chat_members(chat_id) if not member.user.is_bot]

    if len(members) < 2:
        await message.reply_text("❌ At least 2 players required!")
        return

    bomb_holder = random.choice(members)
    game_active = True
    await message.reply_text(f"💣 Bomb Game Started!\n🎭 {await client.get_users(bomb_holder)} has the bomb!\n⏳ Pass it within 10 sec using `/pass @username`")

    await countdown(client, message)

async def countdown(client, message):
    global bomb_holder, game_active
    for i in range(10, 0, -1):
        await message.reply_text(f"⏳ {i} sec left! {await client.get_users(bomb_holder)} has the bomb!")
        await asyncio.sleep(1)

    await message.reply_text(f"💥 BOOM! {await client.get_users(bomb_holder)} eliminated!")
    game_active = False

@app.on_message(filters.command("pass") & filters.reply)
async def pass_bomb(client, message):
    global bomb_holder, game_active
    if not game_active:
        await message.reply_text("⚠️ No active game!")
        return

    new_holder = message.reply_to_message.from_user.id
    if new_holder == bomb_holder:
        await message.reply_text("⚠️ You already have the bomb!")
        return

    bomb_holder = new_holder
    await message.reply_text(f"🎭 {await client.get_users(bomb_holder)} now has the bomb!")


# 🕵️ Spy Game
@app.on_message(filters.command("start_spy"))
async def start_spy_game(client, message):
    global players, spy_game_active
    if spy_game_active:
        await message.reply_text("⚠️ Game already in progress!")
        return

    chat_id = message.chat.id
    members = [member.user.id async for member in client.get_chat_members(chat_id) if not member.user.is_bot]

    if len(members) < 3:
        await message.reply_text("❌ At least 3 players required!")
        return

    players = {user: "Citizen" for user in members}
    spy = random.choice(members)
    detective = random.choice([m for m in members if m != spy])

    players[spy] = "Spy"
    players[detective] = "Detective"

    for user, role in players.items():
        await client.send_message(user, f"🎭 Your Role: {role}")

    spy_game_active = True
    await message.reply_text("🕵️ Spy Game Started!\nEveryone check your private messages for your role.\n🔎 Discuss & vote using `/vote @username`")

@app.on_message(filters.command("vote") & filters.reply)
async def vote_player(client, message):
    global players, spy_game_active
    if not spy_game_active:
        await message.reply_text("⚠️ No active game!")
        return

    voted_player = message.reply_to_message.from_user.id
    if voted_player not in players:
        await message.reply_text("❌ Invalid vote!")
        return

    eliminated_role = players.pop(voted_player)
    await message.reply_text(f"🚨 {await client.get_users(voted_player)} was eliminated! They were a {eliminated_role}")

    if "Spy" not in players.values():
        await message.reply_text("🎉 Citizens Win!")
        spy_game_active = False
    elif len(players) == 2:
        await message.reply_text("🕵️ Spy Wins!")
        spy_game_active = False