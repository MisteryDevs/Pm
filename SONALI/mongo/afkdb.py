from SONALI.utils.mongo import afkdb

async def is_afk(user_id: int):
    """Check if user is AFK"""
    user = await afkdb.find_one({"user_id": user_id})
    if not user:
        return False, None
    return True, user.get("reason", "")

async def add_afk(user_id: int, reason: str):
    """Set user as AFK with reason"""
    await afkdb.update_one(
        {"user_id": user_id}, {"$set": {"reason": reason}}, upsert=True
    )

async def remove_afk(user_id: int):
    """Remove user from AFK"""
    await afkdb.delete_one({"user_id": user_id})

async def get_afk_users():
    """Get all AFK users"""
    users = await afkdb.find({"user_id": {"$gt": 0}}).to_list(None)
    return users or []
