import aiosqlite

class StorageAPI:
    def __init__(self, db_path):
        self.db_path = db_path

    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                nickname TEXT,
                chat_id INTEGER,
                rank TEXT DEFAULT 'Member',
                blocked INTEGER DEFAULT 0
            )""")
            await db.execute("""
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY,
                title TEXT,
                blocked INTEGER DEFAULT 0
            )""")
            await db.execute("""
            CREATE TABLE IF NOT EXISTS help (
                id INTEGER PRIMARY KEY,
                text TEXT
            )""")
            await db.execute("""
            CREATE TABLE IF NOT EXISTS stats (
                key TEXT PRIMARY KEY,
                value INTEGER
            )""")
            await db.execute("""
            CREATE TABLE IF NOT EXISTS plugins (
                name TEXT PRIMARY KEY,
                enabled INTEGER DEFAULT 1
            )""")
            await db.commit()
            # Инициализация help
            await db.execute(
                "INSERT OR IGNORE INTO help (id, text) VALUES (1, 'Добро пожаловать!')"
            )
            await db.commit()

    async def register_user(self, user_id, nickname, chat_id):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT OR IGNORE INTO users (id, nickname, chat_id) VALUES (?, ?, ?)",
                (user_id, nickname, chat_id)
            )
            await db.commit()

    async def get_user_rank(self, user_id):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT rank FROM users WHERE id = ?", (user_id,)) as cursor:
                row = await cursor.fetchone()
                return row[0] if row else "Member"

    async def set_user_rank(self, user_id, rank):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("UPDATE users SET rank=? WHERE id=?", (rank, user_id))
            await db.commit()

    async def block_user(self, user_id):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("UPDATE users SET blocked=1 WHERE id=?", (user_id,))
            await db.commit()

    async def unblock_user(self, user_id):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("UPDATE users SET blocked=0 WHERE id=?", (user_id,))
            await db.commit()

    async def get_users(self):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT id, nickname, rank, blocked FROM users") as cursor:
                return await cursor.fetchall()

    async def block_group(self, group_id):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("UPDATE groups SET blocked=1 WHERE id=?", (group_id,))
            await db.commit()

    async def unblock_group(self, group_id):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("UPDATE groups SET blocked=0 WHERE id=?", (group_id,))
            await db.commit()

    async def get_groups(self):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT id, title, blocked FROM groups") as cursor:
                return await cursor.fetchall()

    async def get_help_text(self):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT text FROM help WHERE id=1") as cursor:
                row = await cursor.fetchone()
                return row[0] if row else "Добро пожаловать!"

    async def set_help_text(self, text):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("UPDATE help SET text=? WHERE id=1", (text,))
            await db.commit()

    async def update_stat(self, key, value):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT OR REPLACE INTO stats (key, value) VALUES (?, ?)",
                (key, value)
            )
            await db.commit()

    async def get_stat(self, key):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT value FROM stats WHERE key=?", (key,)) as cursor:
                row = await cursor.fetchone()
                return int(row[0]) if row else 0

    async def get_all_stats(self):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT key, value FROM stats") as cursor:
                return await cursor.fetchall()

    async def set_plugin_status(self, plugin_name, enabled):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT OR REPLACE INTO plugins (name, enabled) VALUES (?, ?)",
                (plugin_name, int(enabled))
            )
            await db.commit()

    async def get_plugins(self):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT name, enabled FROM plugins") as cursor:
                return await cursor.fetchall()