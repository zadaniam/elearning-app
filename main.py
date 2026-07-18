# main.py

import flet as ft
from screens.login_screen import LoginScreen
from screens.register_screen import RegisterScreen
from screens.dashboard_screen import CatalogScreen
from screens.player_screen import PlayerScreen
from screens.profile_screen import ProfileScreen
from screens.aichat_screen import ChatScreen
from screens.payment_screen import PaymentScreen

def main(page: ft.Page):
    page.title = "E-Learning Bisnis"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    page.window_width = 390
    page.window_height = 844
    page.window_resizable = False

    # Mengaktifkan scroll global sejak awal aplikasi menyala
    page.scroll = ft.ScrollMode.AUTO 

    def route_change(e):
        print("--- DETEKTIF: route_change BERHASIL TERPANGGIL! ---")
        print(f"--- DETEKTIF: Alamat Rute Aktif = {page.route} ---")
        
        page.views.clear()
        
        if page.route == "/":
            page.views.append(LoginScreen(page))
        elif page.route == "/register":
            page.views.append(RegisterScreen(page))
        elif page.route == "/catalog":
            page.views.append(CatalogScreen(page))
        elif page.route == "/player":
            page.views.append(PlayerScreen(page))
        elif page.route == "/profile":
            page.views.append(ProfileScreen(page))
        elif page.route == "/chat":
            page.views.append(ChatScreen(page))
        elif page.route == "/payment":
            page.views.append(PaymentScreen(page)) 
            

        # 🌟 KODE BARU: CETAK ISI TUMPUKAN MEMORI SEBELUM UPDATE
        print(f" Jumlah Layar Aktif di Memori = {len(page.views)}")
        for i, v in enumerate(page.views):
            # Mengintip objek apa saja yang ada di dalam tumpukan
            print(f"   -> Lapisan [{i}]: {type(v).__name__} (Route: {getattr(v, 'route', 'Tidak Ada')})")
        print("===============================================\n")
            

        page.update()

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.route = top_view.route
        route_change(None)

    # Daftarkan fungsi ke sistem Flet
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # Muat halaman pertama saat aplikasi dinyalakan
    page.route = "/"
    route_change(None)

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
