"""
Ünsal Demircioğlu
Kodland Case
2024-06-01
Github: unsaldemircioglu
"""
import sqlite3

# Veritabanına bağlanlantısı 
conn = sqlite3.connect("user.db")

# Cursor Objem
c = conn.cursor()

#Tablo oluşturmk için(id,açıklama ve tamamlama durumu(bollean))
try:
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    ''')
    print("Tablo başarıyla oluşturuldu.")
except Exception as e:
    print(f"Tablo oluşturulurken hata: {e}")

# Değişiklikleri kaydetmek için
conn.commit()

# Bağlantıyı kapatmak için
conn.close()
