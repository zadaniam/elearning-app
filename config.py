# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Jika di .env tidak ada, maka otomatis default ke 'production' demi keamanan sistem rilis.
APP_ENV = os.getenv("APP_ENV", "production")

# SINGLE SOURCE OF TRUTH: Penentuan URL dasar API secara otomatis
if APP_ENV == "development":
    BASE_URL = "http://localhost:8000"
elif APP_ENV == "staging":
    BASE_URL = "https://elearning-backend-staging-8f81.up.railway.app"
else:
    BASE_URL = "https://elearning-backend-production-b5a4.up.railway.app"

# Kumpulan endpoint resmi agar penulisan di file screen menjadi rapi
API_URLS = {
    "login": f"{BASE_URL}/api/v1/auth/login",
    "register": f"{BASE_URL}/api/v1/auth/register",
    "katalog": f"{BASE_URL}/api/v1/materi/katalog",
    "chat_stream": f"{BASE_URL}/api/v1/chat/stream",
    "config": f"{BASE_URL}/api/v1/payment/config",
    "charge": f"{BASE_URL}/api/v1/payment/charge",
    "status": f"{BASE_URL}/api/v1/payment/status" # Nanti tinggal ditambah /order_id
}
