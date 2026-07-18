# screens/chat_screen.py
import flet as ft
import httpx
import asyncio
from config import API_URLS 

class ChatScreen(ft.View):
    def __init__(self, page: ft.Page):
        # Inisialisasi service AI
        self.backend_url = API_URLS["chat_stream"]
        
        # Penampung riwayat chat visual (hanya selama aplikasi menyala)
        self.chat_history_view = ft.ListView(
            expand=True, 
            spacing=10, 
            auto_scroll=True,
            padding=15
        )
        
        # Input teks dari user
        self.input_text = ft.TextField(
            hint_text="Tanyakan sesuatu tentang bisnis...",
            expand=True,
            autofocus=True,
            on_submit=self.kirim_pesan
        )
        
        # Tombol kirim
        self.btn_kirim = ft.IconButton(
            icon=ft.Icons.SEND_ROUNDED,
            icon_color=ft.Colors.BLUE,
            on_click=self.kirim_pesan
        )

        # Buat tampilan UI utamanya
        super().__init__(
            route="/chat",
            controls=[
                # AppBar atas dengan tombol kembali manual
                ft.AppBar(
                    title=ft.Text("Tanya AI Mentor Bisnis", weight="bold"),
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                    
                    # 🌟 TAMBAHKAN KODE BARU INI DI DALAM APPBAR:
                    leading=ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color=ft.Colors.BLACK,
                        tooltip="Kembali ke Dashboard",
                        # Mengarahkan rute kembali ke katalog dashboard Anda
                        on_click=lambda e: self.page.go("/catalog") 
                    ),
                ),
                
                # Area Chat
                self.chat_history_view,
                
                # Input Area di bagian bawah
                ft.Container(
                    content=ft.Row([self.input_text, self.btn_kirim]),
                    padding=10,
                    bgcolor=ft.Colors.SURFACE_CONTAINER_LOW
                )
            ]
        )

    def kirim_pesan(self, e):
        user_prompt = self.input_text.value.strip()
        if not user_prompt:
            return

        # 1. Tampilkan pesan user ke layar terlebih dahulu
        self.chat_history_view.controls.append(
            ft.Container(
                content=ft.Text(f"Anda:\n{user_prompt}", color=ft.Colors.BLACK),
                padding=10,
                bgcolor=ft.Colors.GREY_200,
                border_radius=10,
            )
        )
        
        # 2. Tampilkan status loading "Sedang Berpikir..."
        self.loading_bubble = ft.Text("AI sedang berpikir...", italic=True, color=ft.Colors.GREY_500)
        self.chat_history_view.controls.append(self.loading_bubble)
        
        # Kosongkan kotak input teks dan matikan tombol kirim sementara
        self.input_text.value = ""
        self.btn_kirim.disabled = True
        self.page.update() # Kirim perubahan ke UI agar pesan langsung muncul

        # 3. KIRIM PROSES KE BACKGROUND TUGAS (Agar tidak membeku)
        # Kita lempar proses internet ini menggunakan run_task bawaan Flet
        self.page.run_task(self.proses_panggil_ai, user_prompt)


    # 🌟 FUNGSI BARU: Khusus berjalan di background untuk menunggu jawaban internet
    async def proses_panggil_ai(self, user_prompt):
        print("\n--- 🕵️‍♂️ DETEKTIF: Memulai proses_panggil_ai di Background ---")
        
        # Hapus tulisan "Sedang berpikir..."
        self.chat_history_view.controls.remove(self.loading_bubble)

        # 1. Buat wadah teks kosong terlebih dahulu di UI
        ai_text_control = ft.Text("", color=ft.Colors.WHITE)
        self.chat_history_view.controls.append(
            ft.Container(
                content=ai_text_control,
                padding=10,
                bgcolor=ft.Colors.BLUE_800,
                border_radius=10,
            )
        )
        self.page.update()
        print("--- 🕵️‍♂️ DETEKTIF: Wadah teks kosong berhasil dibuat di UI ---")

        teks_berjalan = ""
        counter_potongan = 0

        try:
            print(f"--- 🕵️‍♂️ DETEKTIF: Menembak API Stream ke -> {self.backend_url} ---")
            
            # Menggunakan AsyncClient dari httpx untuk membaca Server-Sent Events / Stream
            async with httpx.AsyncClient(timeout=60.0) as client:
                # Kirim data prompt dalam bentuk JSON ke backend FastAPI Anda
                async with client.stream("POST", self.backend_url, json={"prompt": user_prompt}) as response:
                    
                    if response.status_code != 200:
                        print(f"--- ❌ DETEKTIF: Backend merespon dengan kode eror {response.status_code} ---")
                        ai_text_control.value = "Maaf, gagal mendapatkan respons dari server."
                        ai_text_control.color = ft.Colors.RED
                        self.page.update()
                    else:
                        print("--- 🕵️‍♂️ DETEKTIF: Koneksi Stream Terbuka! Mulai mencicil kata... ---")
                        
                        # Iterasi teks yang dikirimkan oleh StreamingResponse FastAPI kata demi kata
                        async for chunk in response.aiter_text():
                            if chunk:
                                counter_potongan += 1
                                teks_berjalan += chunk
                                ai_text_control.value = teks_berjalan
                                
                                # Cetak ke terminal Flet untuk monitoring pencicilan teks
                                print(f"      [Potongan ke-{counter_potongan}]: '{chunk}'")
                                
                                # Paksa Flet menggambar huruf baru ke layar saat ini juga
                                self.page.update()
                                await asyncio.sleep(0.01)

            print(f"--- 🕵️‍♂️ DETEKTIF: Selesai! Total potongan teks yang masuk: {counter_potongan} ---")

        except Exception as err:
            print(f"--- 💥 DETEKTIF ERROR: Koneksi ke backend gagal/timeout = {err} ---")
            ai_text_control.value = f"Gagal terhubung ke server backend: {str(err)}"
            ai_text_control.color = ft.Colors.RED
            self.page.update()
        
        # 4. Aktifkan kembali tombol kirim setelah selesai streaming
        self.btn_kirim.disabled = False
        self.page.update()