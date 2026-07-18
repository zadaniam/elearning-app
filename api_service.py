import requests
from config import API_URLS 

class CatalogService:
    @staticmethod
    def get_all_materi() -> list:
        """
        Menarik data katalog materi dari backend FastAPI.
        Mengembalikan list of dict jika sukses, atau list kosong jika gagal.
        """
        print("--- [API SERVICE] Menarik data katalog materi dari FastAPI... ---")
        try:
            response = requests.get(API_URLS["katalog"], timeout=5)
            if response.status_code == 200:
                res_data = response.json()
                return res_data.get("data", [])
            
            print(f"--- ❌ [API SERVICE] Server merespon status: {response.status_code} ---")
            return []
            
        except requests.exceptions.Timeout:
            print("--- 💥 [API SERVICE] Batas waktu habis (Timeout) menghubung server ---")
            return []
        except requests.exceptions.RequestException as e:
            print(f"--- 💥 [API SERVICE] Gagal terhubung ke backend = {e} ---")
            return []

    @staticmethod
    def get_live_config() -> dict:
        """
        Menarik data harga premium dan nomor WhatsApp admin dari server pusat.
        Mengembalikan dict berisi konfigurasi live, atau data fallback jika gagal.
        """
        # Data cadangan (fallback) jika server mati
        fallback_data = {
            "formatted_amount": "Rp 150.000",
            "amount": 150000,
            "whatsapp_admin": "62895614609191"
        }
        
        try:
            response = requests.get(API_URLS["config"], timeout=5)
            if response.status_code == 200:
                config_data = response.json()
                return {
                    "formatted_amount": config_data.get("formatted_amount", fallback_data["formatted_amount"]),
                    "amount": config_data.get("amount", fallback_data["amount"]),
                    "whatsapp_admin": config_data.get("whatsapp_admin", fallback_data["whatsapp_admin"])
                }
            return fallback_data
            
        except Exception:
            print("--- ⚠️ [API SERVICE] Gagal memuat config live, menggunakan data lokal ---")
            return fallback_data
