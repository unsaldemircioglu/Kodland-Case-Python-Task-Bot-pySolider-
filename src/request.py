"""
Ünsal Demircioğlu
Kodland Case
2024-06-01
Github: unsaldemircioglu
"""

import requests
import os
from dotenv import load_dotenv

# Ortam değişkenlerini yüklemek için
load_dotenv()

# API anahtarını almak için
REVE_API_KEY = os.getenv("REVE_API_KEY")

# API URL'si 
api_url = "https://reveapi.example.com/generate"

# İstek için payload gönderilecek veri
payload = {
    "prompt": "Tamamlanan görev için kutlama posteri: Raporu yaz"
}

# kimlik doğrulama için
headers = {
    "Authorization": f"Bearer {REVE_API_KEY}",
    "Content-Type": "application/json"
}

try:
    # isteği göndermek için
    response = requests.post(api_url, json=payload, headers=headers, timeout=10)

    # Yanıtı kontrol etmek için
    if response.status_code == 200:
        data = response.json()
        print("✅ Görsel üretildi:", data.get("image_url"))
    else:
        print(f" API hatası: {response.status_code} - {response.text}")

except requests.exceptions.Timeout:
    print(" İstek zaman aşımına uğradı.")
except Exception as e:
    print(f" Beklenmeyen hata: {e}")
