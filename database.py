import aiosqlite
from config import DB_NAME, START_BALANCE, JACKPOT_BASE

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            wallet INTEGER DEFAULT 0,
            total_wager INTEGER DEFAULT 0,
            weekly_profit INTEGER DEFAULT 0
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS jackpot(
            amount INTEGER
        )
        """)

        cursor = await db.execute("SELECT * FROM jackpot")
        if not await cursor.fetchone():
            await db.execute("INSERT INTO jackpot VALUES (?)", (JACKPOT_BASE,))

        await db.commit()
