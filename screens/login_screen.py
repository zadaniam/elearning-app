import flet as ft
import requests
from config import API_URLS

def LoginScreen(page: ft.Page):
    
    def login_click(e):
        status_text.value = ""
        page.update()

        # Validasi inputan lokal
        if not txt_email.value:
            status_text.value = "Email tidak boleh kosong"
            status_text.color = ft.Colors.RED
            page.update()
            return
        if not txt_password.value:
            status_text.value = "Password tidak boleh kosong"
            status_text.color = ft.Colors.RED
            page.update()
            return

        # Tampilkan animasi loading
        loading_ring.visible = True
        btn_masuk.disabled = True
        page.update()

        print(f"Mencoba masuk untuk email: {txt_email.value}")

        # 1. COBA LOGIN KE FIREBASE melalui BACKEND FASTAPI
        try:
            response = requests.post(
                API_URLS["login"],
                json={"email": txt_email.value, "password": txt_password.value},
                timeout=5
            )
            
            # Matikan loading ring setelah mendapat respon server
            loading_ring.visible = False
            btn_masuk.disabled = False

            if response.status_code == 200:
                hasil = response.json()
                # Simpan data ke session page.data seperti biasa Anda lakukan
                page.data = {
                    "uid": hasil.get("uid"),
                    "email": txt_email.value,        
                    "is_premium": hasil.get("is_premium", False),
                    "whatsapp": hasil.get("whatsapp", ""),
                    "nama_lengkap": hasil.get("nama_lengkap", ""),
                    "asal_daerah": hasil.get("asal_daerah", ""),
                    "nama_bisnis": hasil.get("nama_bisnis", ""),
                    "bidang_bisnis": hasil.get("bidang_bisnis", "") 
                }
                page.go("/catalog")
                return
            
            else:
                # Menangani error pesan dari detail FastAPI HTTPException
                try:
                    error_msg = response.json().get("detail", "")
                except:
                    error_msg = "Terjadi kesalahan internal pada server backend."
                
                # Terjemahkan kode error Firebase Auth yang diteruskan oleh FastAPI
                if "EMAIL_NOT_FOUND" in error_msg or "INVALID_LOGIN_CREDENTIALS" in error_msg or "INVALID_PASSWORD" in error_msg:
                    status_text.value = "Email atau kata sandi salah."
                else:
                    status_text.value = f"Gagal masuk: {error_msg}"
                    
                status_text.color = ft.Colors.RED
                page.update()

        except Exception as e:
            loading_ring.visible = False
            btn_masuk.disabled = False
            status_text.value = f"Gagal terhubung ke server backend: {e}"
            status_text.color = ft.Colors.RED
            page.update()

    txt_email = ft.TextField(
        label="Alamat Email", 
        hint_text="Masukkan email Anda",
        value="zadaniammusthofa@gmail.com",
        border_radius=10,
        width=300
    )

    txt_password = ft.TextField(
        label="Kata Sandi (Password)", 
        hint_text="Minimal 6 karakter",
        value="Zada23032001",
        border_radius=10,
        width=300,
        password=True,
        can_reveal_password=True  
    )

    status_text = ft.Text(value="", size=14, weight=ft.FontWeight.BOLD)
    loading_ring = ft.ProgressRing(visible=False, width=20, height=20, stroke_width=2)

    btn_masuk = ft.ElevatedButton(
        "Log-in / Masuk",
        on_click=login_click,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        width=300,
        height=50,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE_500
    )

    return ft.View(
        route="/",
        controls=[
            ft.AppBar(
                title=ft.Text("Selamat Datang"), 
                bgcolor=ft.Colors.BLUE_500, 
                color=ft.Colors.WHITE
            ),
            ft.Column(
                controls=[
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    ft.Icon(ft.Icons.LIGHTBULB_CIRCLE, size=80, color=ft.Colors.BLUE_500),
                    ft.Text("E-Learning Bisnis", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    ft.Text("Belajar bisnis praktis untuk pemula.", size=14, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER),
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    txt_email,
                    txt_password,
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    
                    status_text,
                    
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    loading_ring,
                    ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                    btn_masuk,
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    
                    # 🌟 SEKARANG DI SINI: Tombol daftar sudah dimasukkan ke dalam susunan layar
                    ft.TextButton(
                        "Belum punya akun? Daftar di sini", 
                        on_click=lambda e: page.go("/register")
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.START,
                expand=True
            )
        ]
    )
