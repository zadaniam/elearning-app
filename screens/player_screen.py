import flet as ft
import flet_video as ftv  
import yt_dlp   
import requests
from config import API_URLS

def PlayerScreen(page: ft.Page):
    
    # 🟢 1. AMBIL DATA DINAMIS DARI HALAMAN KATALOG & DATABASE
    target_title = page.data.get("current_video", "1. Mindset Bisnis & Riset Pasar") if page.data else "1. Mindset Bisnis & Riset Pasar"
    

    # VARIABEL DEFAULT (Fallback jika server bermasalah atau kolom di DB kosong)
    video_url_target = "https://youtube.com"  
    live_deskripsi = "Selamat belajar! Simak materi video di atas dengan seksama untuk meningkatkan omset dan optimasi bisnis UMKM Anda."
    raw_silabus = [
        "Poin 1: Pengenalan dasar materi pembelajaran",
        "Poin 2: Strategi implementasi taktis dalam bisnis",
        "Poin 3: Kesimpulan dan langkah aksi (Action Plan)"
    ]

    try:
        r = requests.get(API_URLS["katalog"], timeout=5)
        if r.status_code == 200 and r.json():
            res_data = r.json()
            materi_list = res_data.get("data", [])
            
            for data in materi_list:
                if data.get("title") == target_title:
                    video_url_target = data.get("url", "https://youtube.com")

                # Ambil deskripsi dari database jika tersedia
                    if data.get("deskripsi"):
                        live_deskripsi = data.get("deskripsi")
                    
                    # Ambil silabus dari database jika tersedia
                    if data.get("silabus"):
                        db_silabus = data.get("silabus")
                        # Jika di database tipenya String panjang (misal dipisah koma atau baris baru)
                        if isinstance(db_silabus, str):
                            if "\n" in db_silabus:
                                raw_silabus = [p.strip() for p in db_silabus.split("\n") if p.strip()]
                            elif "+" in db_silabus:
                                raw_silabus = [p.strip() for p in db_silabus.split("+") if p.strip()]
                            else:
                                raw_silabus = [db_silabus]
                        # Jika di database tipenya sudah List array JSON
                        elif isinstance(db_silabus, list):
                            raw_silabus = db_silabus
                    break
            
    except Exception as e:
        print(f"Gagal mengambil URL video dari backend terpusat: {e}")

    def go_back(e):
        page.go("/catalog")

    def get_direct_youtube_url(url):
        if "youtube.com" not in url and "youtu.be" not in url:
            return url
            
        ydl_opts = {
            'format': 'best[ext=mp4]/best', 
            'quiet': True
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info.get('url', url)
        except Exception as e:
            print(f"Gagal ekstrak YouTube: {e}")
            return url

    # 🟢 2. EKSTRAK URL HASIL LIHAT DATABASE
    direct_url = get_direct_youtube_url(video_url_target)

    video_player = ftv.Video(
        expand=True,
        playlist=[
            ftv.VideoMedia(direct_url)
        ],
        playlist_mode=ftv.PlaylistMode.LOOP,
        fill_color=ft.Colors.BLACK,
        autoplay=True,
    )

    # PROSES GENERATE TAMPILAN SILABUS MENJADI WIDGET FLET (Kompatibel Flet 0.8.5)
    silabus_widgets = []
    for item in raw_silabus:
        silabus_widgets.append(
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED, color="#1E3A8A", size=18),
                    # Memperbaiki 'weight="medium"' menjadi FontWeight.W_500 agar tidak crash di Flet lama
                    ft.Text(item, size=13, color="#4B5563", weight=ft.FontWeight.W_500)
                ]),
                padding=ft.Padding(left=4, top=2, right=4, bottom=2)
            )
        )

    # --- 3. CUSTOM MOBILE BAR DESIGN (Ganti AppBar Kaku) ---
    custom_header = ft.Container(
        padding=ft.Padding(left=20, top=20, right=20, bottom=25),
        bgcolor="#1E3A8A", # Warna Navy Premium konsisten
        border_radius=ft.BorderRadius(0, 0, 30, 30),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.START,
            controls=[
                ft.IconButton(ft.Icons.ARROW_BACK_IOS_NEW, icon_color=ft.Colors.WHITE, icon_size=18, on_click=go_back),
                ft.Container(width=10),
                ft.Text("Video Materi", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
            ]
        )
    )

    # --- 4. RENDER MASTER VIEW ---
    return ft.View(
        route="/player",
        bgcolor="#F3F4F6", # Latar belakang abu-abu terang netral mobile app
        padding=0,         # Agar header melengkung menempel penuh ke atas layar
        controls=[
            custom_header,
            
            ft.ListView(
                expand=True,
                padding=ft.Padding(left=20, top=15, right=20, bottom=20),
                controls=[
                    # Area Video Player (Dengan bingkai melengkung halus)
                    ft.Container(
                        content=video_player, 
                        height=210, 
                        bgcolor=ft.Colors.BLACK, 
                        border_radius=16,
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, "#000000"), offset=ft.Offset(0, 4))
                    ),
                    ft.Divider(height=15, color=ft.Colors.TRANSPARENT),
                    
                    # Kartu Informasi Deskripsi Modul Video
                    ft.Container(
                        padding=ft.Padding(left=16, top=16, right=16, bottom=16),
                        border_radius=16,
                        bgcolor="#FFFFFF",
                        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.05, "#000000"), offset=ft.Offset(0, 4)),
                        content=ft.Column([
                            ft.Text(target_title, size=16, weight=ft.FontWeight.BOLD, color="#1F2937"),
                            ft.Text(
                                live_deskripsi,
                                size=13, 
                                color="#6B7280"
                            ),
                        ], spacing=6)
                    ),
                    
                    ft.Divider(height=15, color=ft.Colors.TRANSPARENT),
                    
                    # Kartu Area Rincian Silabus Pembelajaran
                    ft.Container(
                        padding=ft.Padding(left=16, top=16, right=16, bottom=16),
                        border_radius=16,
                        bgcolor="#FFFFFF",
                        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.05, "#000000"), offset=ft.Offset(0, 4)),
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(ft.Icons.MENU_BOOK_ROUNDED, color="#1E3A8A", size=18),
                                ft.Text("Rincian Silabus Materi", size=14, weight=ft.FontWeight.BOLD, color="#1E3A8A"),
                            ], spacing=6),
                            ft.Divider(height=15, color="#E5E7EB"),
                            ft.Column(controls=silabus_widgets, spacing=8)
                        ], spacing=5)
                    ),
                ]
            )
        ]
    )
