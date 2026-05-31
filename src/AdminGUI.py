"""
Ünsal Demircioğlu
Kodland Case
2024-06-01
Github: unsaldemircioglu
"""
import sqlite3
import logging
import tkinter as tk
from tkinter import messagebox

# -----------------------------
# Veri Tabanamı Sınıfı
# -----------------------------
class BaseDatabase:
    def __init__(self, db_name):
        try:
            self.conn = sqlite3.connect(db_name)
            self.c = self.conn.cursor()
            self.initialize()
        except Exception as e:
            logging.error(f"Veritabanı başlatma hatası: {e}")

    def initialize(self):
        """Alt sınıflar tarafından özelleştirilebilir"""
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
    def __init__(self, db_name="tasks.db"):
        super().__init__(db_name)

    def initialize(self):
        self.execute('''CREATE TABLE IF NOT EXISTS tasks
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         description TEXT NOT NULL,
                         completed INTEGER DEFAULT 0,
                         level INTEGER DEFAULT 1)''')

    def add_task(self, description, level=1):
        self.execute("INSERT INTO tasks (description, level) VALUES (?, ?)", (description, level))

    def show_tasks(self):
        return self.fetch("SELECT id, description, completed, level FROM tasks")

    def complete_task(self, task_id):
        self.execute("UPDATE tasks SET completed=1 WHERE id=?", (task_id,))

    def stats(self):
        completed = self.fetch("SELECT COUNT(*) FROM tasks WHERE completed=1")[0][0]
        pending = self.fetch("SELECT COUNT(*) FROM tasks WHERE completed=0")[0][0]
        return completed, pending


# -----------------------------
# Kullanıcı Veritabanı Sınıfı
# -----------------------------
class UserDatabase(BaseDatabase):
    def __init__(self, db_name="user.db"):
        super().__init__(db_name)

    def initialize(self):
        self.execute('''CREATE TABLE IF NOT EXISTS users
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         username TEXT NOT NULL,
                         level INTEGER DEFAULT 1)''')

    def add_user(self, username, level=1):
        self.execute("INSERT INTO users (username, level) VALUES (?, ?)", (username, level))

    def get_users(self):
        return self.fetch("SELECT id, username, level FROM users")

    def update_level(self, user_id, level):
        self.execute("UPDATE users SET level=? WHERE id=?", (level, user_id))


# -----------------------------
# GUI Sınıfı(Arayüz için)
# -----------------------------
class TaskGUI:
    def __init__(self, db: TaskDatabase, user_db: UserDatabase):
        self.db = db
        self.user_db = user_db
        self.root = tk.Tk()
        self.root.title("Görev ve Kullanıcı Yönetimi")

        # Kullanıcı ekleme alanı
        tk.Label(self.root, text="Kullanıcı Adı:").pack()
        self.user_entry = tk.Entry(self.root, width=30)
        self.user_entry.pack(pady=5)

        self.user_level_var = tk.IntVar(value=1)
        tk.Label(self.root, text="Kullanıcı Level:").pack()
        self.user_level_entry = tk.Entry(self.root, textvariable=self.user_level_var)
        self.user_level_entry.pack(pady=5)

        add_user_btn = tk.Button(self.root, text="Kullanıcı Ekle", command=self.add_user)
        add_user_btn.pack(pady=5)

        show_users_btn = tk.Button(self.root, text="Kullanıcıları Göster", command=self.show_users)
        show_users_btn.pack(pady=5)

        # Görev ekleme alanı
        tk.Label(self.root, text="Görev Açıklaması:").pack()
        self.entry = tk.Entry(self.root, width=40)
        self.entry.pack(pady=5)

        self.level_var = tk.IntVar(value=1)
        tk.Label(self.root, text="Görev Level:").pack()
        self.level_entry = tk.Entry(self.root, textvariable=self.level_var)
        self.level_entry.pack(pady=5)

        add_btn = tk.Button(self.root, text="Görev Ekle", command=self.add_task)
        add_btn.pack(pady=5)

        show_btn = tk.Button(self.root, text="Görevleri Göster", command=self.show_tasks)
        show_btn.pack(pady=5)

        stats_btn = tk.Button(self.root, text="İstatistikler", command=self.show_stats)
        stats_btn.pack(pady=5)

        # Çıktı alanı
        self.output = tk.Text(self.root, height=20, width=60)
        self.output.pack(pady=5)

    def add_user(self):
        username = self.user_entry.get()
        level = self.user_level_var.get()
        if username:
            self.user_db.add_user(username, level)
            messagebox.showinfo("Başarılı", f"Kullanıcı eklendi: {username} (Level {level})")
            self.user_entry.delete(0, tk.END)

    def show_users(self):
        users = self.user_db.get_users()
        self.output.delete("1.0", tk.END)
        if not users:
            self.output.insert(tk.END, "👤 Hiç kullanıcı yok.\n")
        else:
            for uid, uname, lvl in users:
                self.output.insert(tk.END, f"{uid} - {uname} (Level {lvl})\n")

    def add_task(self):
        desc = self.entry.get()
        level = self.level_var.get()
        if desc:
            self.db.add_task(desc, level)
            messagebox.showinfo("Başarılı", f"Görev eklendi: {desc} (Level {level})")
            self.entry.delete(0, tk.END)

    def show_tasks(self):
        tasks = self.db.show_tasks()
        self.output.delete("1.0", tk.END)
        if not tasks:
            self.output.insert(tk.END, "📭 Hiç görev yok.\n")
        else:
            for tid, desc, comp, lvl in tasks:
                self.output.insert(tk.END, f"{tid} - {desc} (Level {lvl}) [{'✅' if comp else '❌'}]\n")

    def show_stats(self):
        completed, pending = self.db.stats()
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, f"📊 İstatistikler:\nTamamlanan: {completed}\nBekleyen: {pending}\n")

    def run(self):
        self.root.mainloop()


# -----------------------------
# Ana Program
# -----------------------------
if __name__ == "__main__":
    logging.basicConfig(filename="gui.log", level=logging.DEBUG,
                        format="%(asctime)s %(levelname)s:%(message)s")

    db = TaskDatabase() # Veritabanı nesnesi oluşturmak için
    user_db = UserDatabase() # Veritabanını Objeye çekme
    gui = TaskGUI(db, user_db) # GUI nesnesi oluşturmak için
    gui.run()  # GUI'yi çalıştırmak için
