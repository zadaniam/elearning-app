import flet as ft

def ProfileScreen(page: ft.Page):
    # 1. AMBIL DATA DINAMIS DARI MEMORI PAGE.DATA
    user_email = page.data.get("email", "user@email.com") if page.data else "user@email.com"
    user_whatsapp = page.data.get("whatsapp", "-") if page.data else "-"
    is_premium = page.data.get("is_premium", False) if page.data else False
    
    nama_lengkap = page.data.get("nama_lengkap", "-") if page.data else "-"
    asal_daerah = page.data.get("asal_daerah", "-") if page.data else "-"
    nama_bisnis = page.data.get("nama_bisnis", "-") if page.data else "-"
    bidang_bisnis = page.data.get("bidang_bisnis", "-") if page.data else "-"
    
    # Penyesuaian tema warna status badge
    status_text = "MEMBER PREMIUM 🌟" if is_premium else "AKUN GRATIS 🆓"
    status_color = "#3B82F6" if is_premium else "#9CA3AF" # Blue premium vs Grey netral

    def go_to_catalog(e):
        page.go("/catalog")

    def log_out(e):
        if page.data:
            page.data.clear()
        page.go("/")

    # --- CUSTOM PROFILE HEADER (Setema dengan Catalog Screen Navy) ---
    custom_header = ft.Container(
        padding=ft.Padding(left=20, top=20, right=20, bottom=25),
        bgcolor="#1E3A8A", # Warna Navy Premium yang sinkron
        border_radius=ft.BorderRadius(0, 0, 30, 30),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            controls=[
                # Baris Atas: Tombol Back & Judul Halaman
                ft.Row(
                    alignment=ft.MainAxisAlignment.START,
                    controls=[
                        ft.IconButton(ft.Icons.ARROW_BACK_IOS_NEW, icon_color=ft.Colors.WHITE, icon_size=18, on_click=go_to_catalog),
                        ft.Container(width=10),
                        ft.Text("Profil Pengguna", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                    ]
                ),
                ft.Container(height=5),
                # Avatar Lingkaran Profil Modern
                ft.Container(
                    width=85,
                    height=85,
                    shape=ft.BoxShape.CIRCLE,
                    bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
                    alignment=ft.Alignment(0, 0),
                    content=ft.Icon(ft.Icons.PERSON_ROUNDED, size=50, color=ft.Colors.WHITE)
                ),
                ft.Text(nama_lengkap if nama_lengkap != "-" else "Pelajar Bisnis", size=18, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                ft.Text(user_email, size=13, color="#93C5FD")
            ]
        )
    )

    # --- CUSTOM ROW ITEM UNTUK DETAIL INFORMASI ---
    def detail_item(label, value):
        return ft.Container(
            padding=ft.Padding(left=0, top=8, right=0, bottom=8),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(label, size=13, color="#6B7280", weight=ft.FontWeight.W_500),
                    ft.Text(value, size=13, color="#1F2937", weight=ft.FontWeight.BOLD)
                ]
            )
        )

    # --- RENDER MASTER VIEW ---
    return ft.View(
        route="/profile",
        bgcolor="#F3F4F6", # Background abu-abu terang super bersih khas mobile app
        padding=0,         # Menempel penuh ke atas layar
        controls=[
            custom_header,
            
            ft.ListView(
                expand=True,
                spacing=15,
                padding=ft.Padding(left=20, top=15, right=20, bottom=20),
                controls=[
                    
                    # 🟢 BAGIAN 1: PUSAT AKUN (Gaya Card Minimalis Modern)
                    ft.Container(
                        padding=ft.Padding(left=16, top=16, right=16, bottom=16),
                        border_radius=16,
                        bgcolor="#FFFFFF",
                        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.05, "#000000"), offset=ft.Offset(0, 4)),
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.START, 
                            spacing=5,
                            controls=[
                                ft.Row([
                                    ft.Icon(ft.Icons.SHIELD_ROUNDED, color="#1E3A8A", size=18),
                                    ft.Text("Pusat Akun", weight=ft.FontWeight.BOLD, size=14, color="#1E3A8A"),
                                ], spacing=6),
                                ft.Divider(height=15, color="#E5E7EB"),
                                detail_item("No. WhatsApp", user_whatsapp),
                                ft.Container(height=5),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.Text("Status Akun", size=13, color="#6B7280", weight=ft.FontWeight.W_500),
                                        ft.Container(
                                            content=ft.Text(status_text, color=ft.Colors.WHITE, size=10, weight=ft.FontWeight.BOLD),
                                            bgcolor=status_color,
                                            padding=ft.Padding(left=10, top=5, right=10, bottom=5),
                                            border_radius=8
                                        )
                                    ]
                                )
                            ]
                        )
                    ),
                    
                    # 🔵 BAGIAN 2: IDENTITAS DIRI (Gaya Card Minimalis Modern)
                    ft.Container(
                        padding=ft.Padding(left=16, top=16, right=16, bottom=16),
                        border_radius=16,
                        bgcolor="#FFFFFF",
                        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.05, "#000000"), offset=ft.Offset(0, 4)),
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                            spacing=5,
                            controls=[
                                ft.Row([
                                    ft.Icon(ft.Icons.BADGE_ROUNDED, color="#1E3A8A", size=18),
                                    ft.Text("Identitas Diri", weight=ft.FontWeight.BOLD, size=14, color="#1E3A8A"),
                                ], spacing=6),
                                ft.Divider(height=15, color="#E5E7EB"),
                                detail_item("Asal Daerah", asal_daerah),
                                detail_item("Nama Bisnis", nama_bisnis),
                                detail_item("Bidang Bisnis", bidang_bisnis),
                            ]
                        )
                    ),

                    ft.Container(height=15),
                    
                    # 🔴 TOMBOL KELUAR AKUN (Desain Tombol Outline/Clean)
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.ElevatedButton(
                                "Keluar dari Akun",
                                icon=ft.Icons.LOGOUT_ROUNDED,
                                color="#EF4444",
                                bgcolor=ft.Colors.WHITE,
                                on_click=log_out,
                                width=220,
                                height=45,
                                # Memberikan aksen border merah tipis yang estetik
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=12),
                                )
                            )
                        ]
                    ),
                ]
            )
        ]
    )

