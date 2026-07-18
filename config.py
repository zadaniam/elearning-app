# config.py

import os

# STATUS DEVELOPMENT: Ubah ke True jika masih di laptop, ubah ke False jika sudah rilis/produksi
IS_DEVELOPMENT = True

# SINGLE SOURCE OF TRUTH: Pusatkan semua URL di satu tempat ini
if IS_DEVELOPMENT:
    # URL saat pengujian lokal di komputer/laptop Anda
    # TIPS: Jika running di Emulator Android, ganti ke "http://10.0.2.2:8000"
    BASE_URL = "http://localhost:8000"
else:
    # URL asli saat aplikasi Anda sudah online (Server Produksi/Live)
    BASE_URL = "https://bisnisanda.com"

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
