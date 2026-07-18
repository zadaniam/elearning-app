import flet as ft
from api_service import CatalogService  # 🌟 Menggunakan API Service eksternal


def CatalogScreen(page: ft.Page):

    # -------------------------------------------------------------
    # 1. INITIALIZATION & DATA FETCHING (Sangat Singkat & Bersih)
    # -------------------------------------------------------------
    
    # Siapkan penampung data kosong agar aplikasi tidak crash di awal
    materi_list = []
    config_live = {"formatted_amount": "Rp 150.000", "amount": 150000, "whatsapp_admin": "62895614609191"}
    daftar_kategori = ["Semua"]
    selected_category = "Semua"
    search_query = ""
    user_is_premium = page.data.get("is_premium", False) if page.data else False
    user_name = page.data.get("nama_lengkap", "Sobat") if page.data else "Sobat"

    # UI Containers Component
    video_list_container = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    category_row_container = ft.Row(scroll=ft.ScrollMode.AUTO, spacing=10)

    # --- 2. BUNGKUS DENGAN CONTAINER PUTIH ---
    materi_section_white = ft.Container(
        bgcolor=ft.Colors.WHITE,
        border_radius=ft.BorderRadius(25, 25, 0, 0), # Pojok atas melengkung mulus
        padding=ft.Padding(20, 15, 20, 0),
        expand=True,
        content=ft.Column([
            ft.Row([ft.Text("Daftar Video Materi", size=15, weight=ft.FontWeight.BOLD, color="#1F2937")]),
            video_list_container  # Kolom daftar materi Anda dimasukkan ke sini
        ])
    )

    # 🌟 INDIKATOR LOADING: Buat roda berputar di tengah layar
    loading_indicator = ft.Container(
        content=ft.ProgressRing(width=30, height=30, stroke_width=3, color="#1E3A8A"),
        alignment="CENTER",
        expand=True
    )
    # Masukkan loading sebagai konten awal daftar video
    video_list_container.controls.append(loading_indicator)

    async def muat_data_dari_backend():
        nonlocal materi_list, config_live, daftar_kategori
        
        # 🌟 Jalankan request API di latar belakang (Gunakan run_task agar UI tidak beku)
        # Catatan: Jika ingin performa maksimal, library 'requests' bisa diganti 'httpx' nantinya
        materi_list = CatalogService.get_all_materi()
        config_live = CatalogService.get_live_config()
        
        # Ekstraksi ulang kategori setelah data masuk
        daftar_kategori = ["Semua"] + list(set(m.get("kategori") for m in materi_list if m.get("kategori")))
        
        # Gambar ulang komponen setelah data backend siap
        render_categories()
        render_materi()

        # 🌟 PENTING: Karena ini dijalankan di dalam async task, gunakan update_async()
        await page.update_async() 


    # -------------------------------------------------------------
    # 2. SUB-LOGIC FUNCTIONS (Event Handlers)
    # -------------------------------------------------------------
    def go_back(e):
        page.go("/")

    def select_category_click(e, nama_kategori):
        nonlocal selected_category
        selected_category = nama_kategori
        render_categories()
        render_materi()

    def on_search_change(e):
        """🌟 AKTIF REALTIME: Dipicu setiap kali pengguna mengetik"""
        nonlocal search_query
        search_query = e.control.value.lower().strip()
        render_materi()

    # -------------------------------------------------------------
    # 3. RE-RENDER LOGIC (Penyaringan & Penggambaran Konten)
    # -------------------------------------------------------------
    def render_categories():
        category_row_container.controls.clear()
        for kat in daftar_kategori:
            is_active = (kat == selected_category)
            category_chip = ft.Container(
                content=ft.Text(
                    kat.capitalize(), 
                    color=ft.Colors.WHITE if is_active else "#4B5563", 
                    weight=ft.FontWeight.BOLD if is_active else ft.FontWeight.NORMAL, 
                    size=13
                ),
                bgcolor="#1E3A8A" if is_active else "#E5E7EB",
                padding=ft.Padding(16, 8, 16, 8),
                border_radius=20,
                on_click=lambda e, k=kat: select_category_click(e, k),
                animate=ft.Animation(200, "ease")
            )
            category_row_container.controls.append(category_chip)

    def render_materi():
        video_list_container.controls.clear()
        
        for m in materi_list:
            # Kombinasi Filter Kategori + Search Kata Kunci
            match_cat = (selected_category == "Semua" or m.get("kategori") == selected_category)
            match_src = search_query in m.get("title", "").lower()
            
            if match_cat and match_src:
                # Membuat komponen kartu materi
                card_item = create_materi_card(m, user_is_premium)
                video_list_container.controls.append(card_item)

        if len(video_list_container.controls) == 0:
            video_list_container.controls.append(
                ft.Column([
                    ft.Icon(ft.Icons.SEARCH_OFF_ROUNDED, size=50, color="#9CA3AF"),
                    ft.Text("Materi tidak ditemukan. Coba kata kunci lain!", color="#9CA3AF", size=13)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
        page.update()

    # -------------------------------------------------------------
    # 4. REUSABLE WIDGETS (Fungsi Pembuat Komponen UI)
    # -------------------------------------------------------------
    def create_materi_card(m, is_premium_user):
        """Sub-fungsi khusus untuk merakit kontainer kartu modul"""
        badge = "GRATIS" if not m.get("is_premium", False) else "PREMIUM"
        badge_color = "#10B981" if not m.get("is_premium", False) else "#EF4444"
        
        if is_premium_user and m.get("is_premium", False):
            badge = "TERBUKA ✅"
            badge_color = "#3B82F6"

        url_gambar = m.get("thumbnail") or m.get("thumbnail_url") or "https://unsplash.com"

        return ft.Container(
            padding=12, border_radius=16, bgcolor="#FFFFFF",
            margin=ft.Margin(0, 0, 0, 12),
            on_click=lambda e: video_click(m.get("is_premium", False), m.get("title", "")),
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.05, "#000000"), offset=ft.Offset(0, 4)),
            content=ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=12,
                controls=[
                    ft.Container(width=90, height=70, border_radius=12, clip_behavior=ft.ClipBehavior.ANTI_ALIAS, content=ft.Image(src=url_gambar, fit="cover")),
                    ft.Column(
                        expand=True, spacing=6,
                        controls=[
                            ft.Text(m.get("title", "Tanpa Judul"), weight=ft.FontWeight.W_600, size=14, color="#1F2937", max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                            ft.Row([
                                ft.Container(content=ft.Text(badge, size=9, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD), bgcolor=badge_color, padding=ft.Padding(8, 3, 8, 3), border_radius=6),
                                ft.Text(m.get("kategori", "Umum").upper(), size=10, color="#9CA3AF", weight=ft.FontWeight.W_500)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                        ]
                    )
                ]
            )
        )

    def create_premium_banner():
        """Membuat Banner Promosi Premium yang otomatis sembunyi jika user sudah premium"""
        
        # Fungsi aksi saat tombol di banner diklik
        def banner_upgrade_klik(e):
            # Memicu dialog premium tiruan dengan mengambil judul materi pertama sebagai contoh
            contoh_judul = materi_list[0].get("title", "Semua Modul") if materi_list else "Semua Modul"
            video_click(materi_is_premium=True, video_title=contoh_judul)

        return ft.Container(
            # 🌟 PINTAR: Otomatis SEMBUNYI (False) jika user_is_premium bernilai True
            visible=not user_is_premium, 
            
            padding=ft.Padding(20, 16, 20, 16),
            margin=ft.Margin(20, 15, 20, 5),
            border_radius=16,
            # Menggunakan warna gradasi gelap mewah khas aplikasi premium
            gradient=ft.LinearGradient(
                begin=ft.Alignment(-1, -1),
                end=ft.Alignment(1, 1),      
                colors=["#1E3A8A", "#1D4ED8", "#3B82F6"]
            ),
            shadow=ft.BoxShadow(blur_radius=12, color=ft.Colors.with_opacity(0.15, "#1E3A8A"), offset=ft.Offset(0, 6)),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    # Bagian Teks Kiri
                    ft.Column(
                        expand=True,
                        spacing=4,
                        controls=[
                            ft.Row([
                                ft.Icon(ft.Icons.STAR_ROUNDED, color="#FBBF24", size=18),
                                ft.Text("AKSES TANPA BATAS", size=11, color="#93C5FD", weight=ft.FontWeight.BOLD,  style=ft.TextStyle(letter_spacing=1.2))
                            ], spacing=4),
                            ft.Text(
                                "Buka Semua Modul Premium", 
                                size=15, 
                                color=ft.Colors.WHITE, 
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Text(
                                f"Hanya dengan {config_live['formatted_amount']} sekali bayar", 
                                size=12, 
                                color="#E0F2FE"
                            )
                        ]
                    ),
                    # Bagian Tombol Kanan
                    ft.ElevatedButton(
                        content=ft.Text("Gabung", color="#1E3A8A", weight=ft.FontWeight.BOLD),
                        color="#1E3A8A",
                        bgcolor=ft.Colors.WHITE,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            padding=ft.Padding(12, 8, 12, 8)
                        ),
                        on_click=banner_upgrade_klik
                    )
                ]
            )
        )

    def video_click(materi_is_premium, video_title):
        """Logika klik video premium/gratis dan penanganan dialog"""
        async def buka_whatsapp(e_wa):
            message = f"Halo Admin, saya ingin mengaktifkan Materi Premium untuk modul: *{video_title}*."
            whatsapp_url = f"https://wa.me/{config_live['whatsapp_admin']}?text={message.replace(' ', '%20')}"
            dialog.open = False
            page.update()
            await page.launch_url(whatsapp_url)

        def bayar_otomatis_klik(e_pay):
            dialog.open = False
            page.update()
            user_email = page.data.get("user_email", "user_elearning@email.com") if page.data else "user_elearning@email.com"
            page.session.store.set("item_name", f"Premium: {video_title}")
            page.session.store.set("amount", config_live['amount'])
            page.session.store.set("user_email", user_email)
            page.go("/payment")

        if materi_is_premium and not user_is_premium:
            dialog = ft.AlertDialog(
                title=ft.Text("Materi Premium 🔒"),
                content=ft.Text(f"Akses materi ini dengan aktivasi akun premium ({config_live['formatted_amount']}). Pilih metode aktivasi di bawah:"),
                open=True,
                actions=[
                    ft.ElevatedButton("Bayar Instan (QRIS/E-Wallet/VA)", bgcolor="#1E3A8A", color=ft.Colors.WHITE, on_click=bayar_otomatis_klik),
                    ft.TextButton("Hubungi Admin (WhatsApp)", on_click=lambda _: page.run_task(buka_whatsapp, None)),
                    ft.TextButton("Nanti Saja", on_click=lambda _: setattr(dialog, 'open', False) or page.update()),
                ],
                actions_alignment=ft.MainAxisAlignment.END
            )
            page.overlay.append(dialog)
            page.update()
        else:
            if page.data: page.data["current_video"] = video_title
            page.go("/player")

    # -------------------------------------------------------------
    # 5. HEADER DESIGN & MASTER VIEW RENDER
    # -------------------------------------------------------------
    custom_header = ft.Container(
        padding=ft.Padding(20, 20, 20, 25), bgcolor="#1E3A8A", border_radius=ft.BorderRadius(30, 30, 0, 0),
        content=ft.Column(
            spacing=15,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.IconButton(ft.Icons.ARROW_BACK_IOS_NEW, icon_color=ft.Colors.WHITE, icon_size=18, on_click=go_back),
                        ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2, controls=[ft.Text(f"Halo, {user_name}!", size=12, color="#93C5FD")]),
                        ft.Container(content=ft.Icon(ft.Icons.ACCOUNT_CIRCLE_ROUNDED, color=ft.Colors.WHITE, size=32), on_click=lambda e: page.go("/profile"))
                    ]
                ),
                ft.Container(
                    bgcolor=ft.Colors.WHITE, border_radius=12, padding=ft.Padding(12, 4, 12, 4),
                    content=ft.Row([
                        ft.Icon(ft.Icons.SEARCH_ROUNDED, color="#9CA3AF", size=20),
                        ft.TextField(
                            hint_text="Cari materi pembelajaran bisnis...", content_padding=ft.Padding(10, 0, 10, 0), border=ft.InputBorder.NONE,
                            text_size=13, height=40, hint_style=ft.TextStyle(color="#9CA3AF"), expand=True,
                            on_change=on_search_change # 🌟 Menghubungkan fungsi search realtime
                        )
                    ])
                )
            ]
        )
    )

    page.run_task(muat_data_dari_backend)

    return ft.View(
        route="/catalog", bgcolor="#F3F4F6", padding=0,
        controls=[
            custom_header,
            create_premium_banner(),
            ft.Container(
                padding=ft.Padding(20, 15, 20, 10),
                content=ft.Column([
                    ft.Text("Kategori", size=14, weight=ft.FontWeight.BOLD, color="#1F2937"),
                    category_row_container
                ], spacing=8)
            ),
            # 4. SATU-SATUNYA BAGIAN DAFTAR MATERI (Gunakan Container Putih)
            ft.Container(
                expand=True,
                bgcolor=ft.Colors.WHITE,
                border_radius=ft.BorderRadius(25, 25, 0, 0), # Melengkung atas estetik
                padding=ft.Padding(20, 20, 20, 0),
                content=ft.Column([
                    ft.Text("Daftar Video Materi", size=15, weight=ft.FontWeight.BOLD, color="#1F2937"),
                    video_list_container # Masukkan KOLOM UTAMA Anda di sini
                ], spacing=10)
            )
        ]
    )
