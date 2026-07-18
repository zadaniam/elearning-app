import flet as ft
import requests

def RegisterScreen(page: ft.Page):

    # --- 1. DEKLARASI INPUT FIELD ---
    # Pusat Akun
    txt_email = ft.TextField(label="Email", icon=ft.Icons.EMAIL)
    txt_password = ft.TextField(label="Kata Sandi", password=True, can_reveal_password=True, icon=ft.Icons.LOCK)
    txt_whatsapp = ft.TextField(label="No. WhatsApp", icon=ft.Icons.PHONE)
    
    # Identitas Diri
    txt_nama = ft.TextField(label="Nama Lengkap", icon=ft.Icons.PERSON)
    txt_asal = ft.TextField(label="Asal Daerah/Kota", icon=ft.Icons.LOCATION_CITY)
    txt_nama_bisnis = ft.TextField(label="Nama Bisnis", icon=ft.Icons.STORE)
    txt_bidang_bisnis = ft.TextField(label="Bidang Bisnis (Contoh: Kuliner)", icon=ft.Icons.BUSINESS_CENTER)

    txt_error = ft.Text(value="", color=ft.Colors.RED_500, size=12, weight=ft.FontWeight.BOLD)

    # --- 2. LOGIKA TOMBOL DAFTAR ---
    def proses_daftar(e):
        txt_error.value = ""
        page.update()

        # Validasi sederhana agar tidak ada kolom yang kosong
        if not all([txt_email.value, txt_password.value, txt_whatsapp.value, txt_nama.value, txt_asal.value, txt_nama_bisnis.value, txt_bidang_bisnis.value]):
            txt_error.value = "⚠️ Semua kolom wajib diisi dengan lengkap!"
            page.update()
            return

        # Panggil fungsi background task agar aplikasi HP tidak hang/freeze saat kirim data ke Firebase
        async def kirim_data_firebase():
            # 🌟 JALUR BARU: Mengirim data pendaftaran melalui REST API FastAPI backend Anda
            try:
                payload = {
                    "email": txt_email.value,
                    "password": txt_password.value,
                    "whatsapp": txt_whatsapp.value,
                    "nama": txt_nama.value,
                    "asal": txt_asal.value,
                    "nama_bisnis": txt_nama_bisnis.value,
                    "bidang_bisnis": txt_bidang_bisnis.value
                }
                
                response = requests.post(
                    "http://localhost:8000/api/v1/auth/register",
                    json=payload,
                    timeout=10
                )
                
                if response.status_code == 200:
                    hasil = response.json()
                    print("--- DETEKTIF: Registrasi Berhasil via FastAPI! ---")
                    
                    # Titipkan data lengkap hasil kembalian dari FastAPI ke memori aplikasi
                    page.data = {
                        "uid": hasil.get("uid"),  # 🌟 Mencatat UID baru dari server
                        "email": txt_email.value,
                        "is_premium": False,
                        "whatsapp": txt_whatsapp.value,
                        "nama_lengkap": txt_nama.value,
                        "asal_daerah": txt_asal.value,
                        "nama_bisnis": txt_nama_bisnis.value,
                        "bidang_bisnis": txt_bidang_bisnis.value
                    }
                    page.go("/catalog")
                    
                else:
                    # Menangani pesan error detail dari FastAPI HTTPException
                    try:
                        err_msg = response.json().get("detail", "")
                    except:
                        err_msg = "Terjadi kesalahan internal pada server backend."
                        
                    # Terjemahkan error ramah pengguna
                    if "EMAIL_EXISTS" in err_msg:
                        txt_error.value = "❌ Email ini sudah terdaftar. Silakan gunakan email lain."
                    elif "WEAK_PASSWORD" in err_msg:
                        txt_error.value = "❌ Kata sandi terlalu lemah (Minimal 6 karakter)."
                    elif "INVALID_EMAIL" in err_msg:
                        txt_error.value = "❌ Format penulisan email salah."
                    else:
                        txt_error.value = f"❌ Gagal: {err_msg}"
                        
            except Exception as err:
                txt_error.value = f"❌ Gagal terhubung ke server backend: {err}"

            # Sesuai kode asli Anda, flet versi ini menggunakan page.update() biasa di dalam task
            await page.update()

        page.run_task(kirim_data_firebase)

    def ke_halaman_login(e):
        page.go("/")

    return ft.View(
        route="/register",
        controls=[
            ft.AppBar(
                title=ft.Text("Daftar Akun Baru"),
                bgcolor=ft.Colors.BLUE_500,
                color=ft.Colors.WHITE,
                leading=ft.IconButton(ft.Icons.ARROW_BACK, icon_color=ft.Colors.WHITE, on_click=ke_halaman_login)
            ),
            ft.Container(
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Text("Silakan lengkapi data diri Anda untuk memulai belajar bisnis", size=14, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER),
                        ft.Divider(height=15, color=ft.Colors.TRANSPARENT),
                        
                        # Sub-judul Kelompok 1
                        ft.Text("🔐 PUSAT AKUN", weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.BLUE_700),
                        txt_email,
                        txt_password,
                        txt_whatsapp,
                        
                        ft.Divider(height=15, color=ft.Colors.TRANSPARENT),
                        
                        # Sub-judul Kelompok 2
                        ft.Text("📋 IDENTITAS DIRI", weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.BLUE_700),
                        txt_nama,
                        txt_asal,
                        txt_nama_bisnis,
                        txt_bidang_bisnis,
                        
                        txt_error,
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        
                        # Tombol Eksekusi
                        ft.ElevatedButton(
                            "Daftar Sekarang",
                            icon=ft.Icons.PERSON_ADD,
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.BLUE_500,
                            on_click=proses_daftar,
                            width=250
                        ),
                        
                        ft.TextButton("Sudah punya akun? Login di sini", on_click=ke_halaman_login)
                    ]
                ),
                padding=20,
                expand=True
            )
        ]
    )
