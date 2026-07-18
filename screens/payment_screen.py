# screens/payment_screen.py
import asyncio
import flet as ft
import requests
import uuid
from config import API_URLS 

class PaymentScreen(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(
            route="/payment",
            scroll=ft.ScrollMode.AUTO,
            bgcolor="#F3F4F6", # Set tema latar belakang abu-abu bersih mobile app
            padding=0,         # Agar header melengkung menempel penuh ke atas layar
        )
        self.main_page = page
        
        user_info = getattr(self.main_page, "data", {}) or {}
        self.user_uid = user_info.get("uid") or "5rYwn3sHSqVAnqAZTyMcqMdjbUt2"
        self.user_email = user_info.get("email") or "murid@email.com"

        self.order_id = f"REQ-{uuid.uuid4().hex[:6].upper()}"
        
        # Mengambil nama item dinamis dari session jika dikirim dari katalog, fallback ke default
        self.item_name = self.main_page.session.store.get("item_name") if self.main_page.session else "Kelas Master Bisnis Digital"
        if not self.item_name:
            self.item_name = "Kelas Master Bisnis Digital"
        
        # --- KOMPONEN STATE UI (Kompatibel Flet 0.8.5) ---
        self.status_text = ft.Text("Menghubungkan ke server...", size=14, color="#4B5563", weight=ft.FontWeight.W_500)
        self.btn_text = ft.Text("Memuat Harga...", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=14)
        
        # Desain tombol bayar mengikuti tema navy premium
        self.pay_button = ft.ElevatedButton(
            content=self.btn_text, 
            disabled=True, 
            on_click=self.proses_pembayaran,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,                   
                bgcolor="#1E3A8A", # Navy theme               
                shape=ft.RoundedRectangleBorder(radius=12)
            ),
            width=280,
            height=48
        )

        def go_to_catalog(e):
            self.main_page.go("/catalog")

        # --- 1. CUSTOM APP BAR / HEADER DESIGN ---
        custom_header = ft.Container(
            padding=ft.Padding(left=20, top=20, right=20, bottom=25),
            bgcolor="#1E3A8A", # Konsisten warna Navy
            border_radius=ft.BorderRadius(0, 0, 30, 30),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    ft.IconButton(ft.Icons.ARROW_BACK_IOS_NEW, icon_color=ft.Colors.WHITE, icon_size=18, on_click=go_to_catalog),
                    ft.Container(width=10),
                    ft.Text("Pembayaran Akun Premium", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                ]
            )
        )

        # --- 2. KARTU DETAIL TRANSAKSI (INVOICE STYLE) ---
        invoice_card = ft.Container(
            padding=ft.Padding(left=18, top=20, right=18, bottom=20),
            border_radius=16,
            bgcolor="#FFFFFF",
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.05, "#000000"), offset=ft.Offset(0, 4)),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
                controls=[
                    ft.Container(
                        width=50,
                        height=50,
                        shape=ft.BoxShape.CIRCLE,
                        bgcolor=ft.Colors.with_opacity(0.1, "#1E3A8A"),
                        alignment=ft.Alignment(0, 0), # Pengganti alignment.center untuk Flet 0.8.5
                        content=ft.Icon(ft.Icons.RECEIPT_LONG_ROUNDED, color="#1E3A8A", size=26)
                    ),
                    ft.Text(self.item_name, size=16, weight=ft.FontWeight.BOLD, color="#1F2937", text_align=ft.TextAlign.CENTER),
                    ft.Text(f"ID Transaksi: {self.order_id}", size=12, color="#9CA3AF"),
                    ft.Divider(height=10, color="#E5E7EB"),
                    
                    # Status Box Informasi Realtime
                    ft.Container(
                        padding=ft.Padding(left=12, top=10, right=12, bottom=10),
                        border_radius=10,
                        bgcolor="#F3F4F6",
                        width=300,
                        alignment=ft.Alignment(0, 0),
                        content=self.status_text
                    ),
                    
                    ft.Container(height=10),
                    self.pay_button,
                    
                    # Tombol Batalkan / Kembali Bertekstur Bersih
                    ft.TextButton(
                        "Batalkan Pembayaran", 
                        style=ft.ButtonStyle(color="#EF4444"),
                        on_click=go_to_catalog
                    )
                ]
            )
        )

        # --- 3. RENDERING COMPONENT KE STRUKTUR VIEW ---
        self.controls = [
            custom_header,
            ft.Container(
                padding=ft.Padding(left=20, top=25, right=20, bottom=20),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[invoice_card]
                )
            )
        ]
        
        # Jalankan penarikan harga otomatis dari API server pusat
        self.main_page.run_task(self.ambil_harga_terpusat)

    async def ambil_harga_terpusat(self):
        """Fungsi yang sudah diperbaiki mutlak setelah interogasi memori"""
        try:
            print(f"\n🔎 [FLET DETEKTIF] Mengambil konfigurasi harga dari: {API_URLS['config']}")
            response = requests.get(API_URLS["config"], timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                harga_format = data.get('formatted_amount', 'Rp 150.000')
                
                self.btn_text.value = f"Bayar Sekarang ({harga_format})"
                self.pay_button.disabled = False
                self.status_text.value = (
                    "💡 INFORMASI PENTING:\n"
                    "1. Pembayaran mendukung QRIS, E-Wallet, & Virtual Account.\n"
                    "2. Setelah menekan tombol, selesaikan pembayaran di browser.\n"
                    "3. Setelah pembayaran sukses, video premium otomatis aktif langsung.\n"
                    "4. Jika video premium belum aktif, coba restart aplikasi atau login ulang."
                )
                self.status_text.size = 11 
                
                print("🟢 [FLET DETEKTIF] Teks tombol sukses diperbarui secara legal di memori!")
            else:
                self.status_text.value = "❌ Gagal memuat konfigurasi harga server."
        except Exception as err:
            print(f"💥 [FLET DETEKTIF CRASH]: {err}")
            self.status_text.value = "❌ Gagal terhubung ke server backend."
            
        # Perbarui tampilan halaman secara total
        self.main_page.update()


    async def proses_pembayaran(self, e):
        self.status_text.value = "Sedang menyiapkan halaman pembayaran..."
        self.pay_button.disabled = True
        self.main_page.update()
        
        try:
            # Mengirim parameter (kembalikan ke params dulu untuk tes detektif ini)
            payload_params = {
                "order_id": self.order_id,
                "item_name": self.item_name,
                "user_email": self.user_email,
                "uid": self.user_uid
            }
            
            # 🕵️‍♂️ DETEKTIF FLET 1: Cetak data sebelum dikirim
            print(f"\n🔎 [FLET DETEKTIF] Mengirim POST ke: {API_URLS['charge']}")
            print(f"   Payload data: {payload_params}")

            response = requests.post(
                API_URLS["charge"],
                json=payload_params
            )
            
            # 🕵️‍♂️ DETEKTIF FLET 2: Cetak status kode dan teks mentah dari server
            print(f"🔎 [FLET DETEKTIF] Status HTTP Server: {response.status_code}")
            print(f"   Respons mentah server: {response.text}")
            
            res_data = response.json()
            
            if res_data.get("status") == "success":
                redirect_url = res_data.get("redirect_url")
                self.status_text.value = "Silakan selesaikan pembayaran di browser Anda..."
                self.main_page.update()
                
                await self.main_page.launch_url(redirect_url)
                asyncio.create_task(self.cek_status_berkala())
            else:
                self.status_text.value = "Gagal membuat sesi pembayaran."
                self.pay_button.disabled = False
                self.main_page.update()
                
        except Exception as err:
            # 🕵️‍♂️ DETEKTIF FLET 3: Cetak jika ada crash jaringan/pustaka
            print(f"💥 [FLET DETEKTIF CRASH] Terjadi error: {err}")
            self.status_text.value = f"Koneksi backend gagal: {err}"
            self.pay_button.disabled = False
            self.main_page.update()

    async def cek_status_berkala(self):
        for _ in range(15): 
            await asyncio.sleep(4)
            try:
                res = requests.get(f"{API_URLS['status']}/{self.order_id}")
                status = res.json().get("status")
                
                if status == "success":
                    self.status_text.value = "🎉 Pembayaran Sukses! Kelas Anda telah aktif."
                    self.status_text.color = ft.Colors.GREEN_700
                    self.pay_button.visible = False
                    self.main_page.update()
                    return
                elif status == "failed":
                    self.status_text.value = "❌ Pembayaran Gagal atau Kedaluwarsa."
                    self.status_text.color = ft.Colors.RED_700
                    self.pay_button.disabled = False
                    self.main_page.update()
                    return
            except:
                pass
        
        self.status_text.value = "Waktu tunggu habis. Jika sudah bayar, cek berkala halaman profil Anda."
        self.pay_button.disabled = False
        self.main_page.update()
