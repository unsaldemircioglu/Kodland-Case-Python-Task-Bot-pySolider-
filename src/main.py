"""
Ünsal Demircioğlu
Kodland Case
2024-06-01
Github: unsaldemircioglu
"""
import discord
from discord.ext import commands
import sqlite3
import os
import requests
import logging
from dotenv import load_dotenv
from ascii import ascii_art   # ASCII art import


# -----------------------------
# Veri Tabanı Sınıfı
# -----------------------------
class BaseDatabase:
    def __init__(self, db_name="tasks.db"):
        try:
            self.conn = sqlite3.connect(db_name)
            self.c = self.conn.cursor()
            self.initialize()
        except Exception as e:
            logging.error(f"Veritabanı başlatma hatası: {e}")

    def initialize(self):
        pass

    def execute(self, query, params=()):
        try:
            self.c.execute(query, params)
            self.conn.commit()
        except Exception as e:
            logging.error(f"Sorgu hatası: {e}")

    def fetch(self, query, params=()):
        try:
            self.c.execute(query, params)
            return self.c.fetchall()
        except Exception as e:
            logging.error(f"Veri çekme hatası: {e}")
            return []


# -----------------------------
# Görev Veritabanı Sınıfı
# -----------------------------
class TaskDatabase(BaseDatabase):
    def initialize(self):
        self.execute('''CREATE TABLE IF NOT EXISTS tasks
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         description TEXT NOT NULL,
                         completed INTEGER DEFAULT 0)''')

    def add_task(self, description):
        self.execute("INSERT INTO tasks (description) VALUES (?)", (description,))

    def delete_task(self, task_id):
        self.execute("DELETE FROM tasks WHERE id=?", (task_id,))

    def show_tasks(self):
        return self.fetch("SELECT id, description, completed FROM tasks")

    def complete_task(self, task_id):
        self.execute("UPDATE tasks SET completed=1 WHERE id=?", (task_id,))

    def get_task(self, task_id):
        try:
            self.c.execute("SELECT description, completed FROM tasks WHERE id=?", (task_id,))
            return self.c.fetchone()
        except Exception as e:
            logging.error(f"Görev alma hatası: {e}")
            return None

    def stats(self):
        completed = self.fetch("SELECT COUNT(*) FROM tasks WHERE completed=1")[0][0]
        pending = self.fetch("SELECT COUNT(*) FROM tasks WHERE completed=0")[0][0]
        return completed, pending


# -----------------------------
# Kullanıcı Veritabanı Sınıfı
# -----------------------------
class BaseBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def on_ready(self):
        print(f"Bot {self.user.name} çalışıyor!")

    async def on_command_error(self, ctx, error):
        await ctx.send(f"Hata: {error}")
        logging.error(f"Komut hatası: {error}")


# -----------------------------
# Kullanıcı Veritabanı Sınıfı
# -----------------------------
class TaskManagerBot(BaseBot):
    def __init__(self, command_prefix, intents, db: TaskDatabase):
        super().__init__(command_prefix, intents)
        self.db = db

    @commands.command()
    async def add_task(self, ctx, *, description):
        try:
            self.db.add_task(description)
            await ctx.send(f"Görev eklendi: {description}")
        except Exception as e:
            await ctx.send(f"Görev eklenemedi: {e}")

    @commands.command()
    async def delete_task(self, ctx, task_id: int):
        try:
            self.db.delete_task(task_id)
            await ctx.send(f"Görev {task_id} silindi.")
        except Exception as e:
            await ctx.send(f"Görev silinemedi: {e}")

    @commands.command()
    async def show_tasks(self, ctx):
        try:
            tasks = self.db.show_tasks()
            if not tasks:
                await ctx.send("Hiç görev yok.")
            else:
                msg = "\n".join([f"{tid} - {desc} [{'Tamamlandı' if comp else 'Bekliyor'}]" for tid, desc, comp in tasks])
                await ctx.send(f"Görevler:\n{msg}")
        except Exception as e:
            await ctx.send(f"Görevler listelenemedi: {e}")

    @commands.command()
    async def complete_task(self, ctx, task_id: int):
        try:
            self.db.complete_task(task_id)
            await ctx.send(f"Görev {task_id} tamamlandı!")
        except Exception as e:
            await ctx.send(f"Görev tamamlanamadı: {e}")

    @commands.command()
    async def stats(self, ctx):
        try:
            completed, pending = self.db.stats()
            await ctx.send(f"Görev İstatistikleri:\nTamamlanan: {completed}\nBekleyen: {pending}")
        except Exception as e:
            await ctx.send(f"İstatistik alınamadı: {e}")

    @commands.command()
    async def help_tasks(self, ctx):
        await ctx.send("Komutlar:\n"
                       "!add_task <açıklama>\n"
                       "!delete_task <id>\n"
                       "!show_tasks\n"
                       "!complete_task <id>\n"
                       "!celebrate <id>\n"
                       "!stats\n"
                       "!ascii\n")

    @commands.command()
    async def celebrate(self, ctx, task_id: int):
        try:
            task = self.db.get_task(task_id)
            if task and task[1] == 1:
                desc = task[0]
                api_url = "https://reveapi.example.com/generate"
                payload = {"prompt": f"Görev kutlama posteri: {desc}"}
                headers = {"Authorization": f"Bearer {os.getenv('REVE_API_KEY')}"}
                response = requests.post(api_url, json=payload, headers=headers, timeout=10)
                data = response.json()
                image_url = data.get("image_url")
                if image_url:
                    await ctx.send(f"Kutlama posteri üretildi: {desc}\n{image_url}")
                else:
                    await ctx.send("Görsel üretilemedi.")
            else:
                await ctx.send("Görev bulunamadı veya tamamlanmamış.")
        except requests.exceptions.Timeout:
            await ctx.send("API isteği zaman aşımına uğradı.")
        except Exception as e:
            await ctx.send(f"API hatası: {e}")

    @commands.command()
    async def ascii(self, ctx):
        await ctx.send(f"```\n{ascii_art}\n```")


# -----------------------------
#   Ana Program
# -----------------------------
if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("DISCORD_TOKEN")

    logging.basicConfig(filename="discord.log", level=logging.DEBUG,
                        format="%(asctime)s %(levelname)s:%(message)s")

    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    db = TaskDatabase()
    bot = TaskManagerBot(command_prefix="!", intents=intents, db=db)

    try:
        bot.run(token) # TOKEN'ı .env dosyasından çekip botu başlatmak için
    except Exception as e:
        logging.error(f"Bot başlatılamadı: {e}") # Hata durumunda loglama yapmak için
        print(f"Bot başlatılamadı: {e}") # Hata durumunda kullanıcıya bilgi vermek için
