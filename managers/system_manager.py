import os
import sys
import ctypes
import platform
import pyautogui
import tkinter as tk
import random

class SystemManager:
    def __init__(self, root=None):
        self.os_type = platform.system()
        self.desktop_path = self._get_desktop_path()
        self.root = root

        # --- TEMİZLİK VE GÜVENLİK ---
        self.created_files = [] # Oyunun oluşturduğu dosyaları takip eder
        self.original_wallpaper = self._get_current_wallpaper() # Eski duvar kağıdını yedekler

    def _get_desktop_path(self):
        """Kullanıcının Masaüstü yolunu bulur."""
        try:
            return os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 
        except:
            return os.path.join(os.path.expanduser("~"), "Desktop")

    def is_admin(self):
        """Yönetici yetkilerini kontrol eder."""
        if self.os_type == "Windows":
            try:
                return ctypes.windll.shell32.IsUserAnAdmin()
            except:
                return False
        else:
            # Linux/Mac için (Bu proje Windows odaklı ama hata vermemeli)
            return os.geteuid() == 0

    # --- YENİ: DUVAR KAĞIDI YÖNETİMİ ---
    def _get_current_wallpaper(self):
        """Mevcut duvar kağıdını hafızaya alır (Sadece Windows)."""
        if self.os_type == "Windows":
            try:
                # SPI_GETDESKWALLPAPER = 0x0073
                ubuffer = ctypes.create_unicode_buffer(512)
                ctypes.windll.user32.SystemParametersInfoW(0x0073, 512, ubuffer, 0)
                return ubuffer.value
            except:
                return None
        return None

    def change_wallpaper(self, image_path):
        """Duvar kağıdını değiştirir."""
        if self.os_type == "Windows":
            try:
                # SPI_SETDESKWALLPAPER = 20
                ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
            except:
                pass

    def restore_wallpaper(self):
        """Orijinal duvar kağıdını geri yükler."""
        if self.original_wallpaper and os.path.exists(self.original_wallpaper):
            self.change_wallpaper(self.original_wallpaper)

    # --- YENİ: DOSYA VE MAREMİYET OKUMA ---
    def get_desktop_items(self, max_items=5):
        """Masaüstü dosya isimlerini okur."""
        try:
            items = os.listdir(self.desktop_path)
            # Sistem dosyalarını ve oyunun dosyalarını görmezden gel
            ignored = ["desktop.ini", "TARTARUS_LOGS", "DONT_LOOK_BEHIND_YOU.txt", "ini"]
            clean_items = [i for i in items if i not in ignored and not i.startswith(".")]

            if len(clean_items) > max_items:
                return random.sample(clean_items, max_items)
            return clean_items
        except:
            return []

    def get_location_info(self):
        """IP üzerinden şehir bilgisini çeker (requests kütüphanesi gerekir)."""
        try:
            import requests
            data = requests.get("http://ip-api.com/json/", timeout=2).json()
            return data.get("city"), data.get("isp")
        except:
            return None, None

    def get_active_window(self):
        """Aktif pencere başlığını döner (Alt-Tab takibi için)."""
        if self.os_type == "Windows":
            try:
                hwnd = ctypes.windll.user32.GetForegroundWindow()
                length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
                buff = ctypes.create_unicode_buffer(length + 1)
                ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
                return buff.value
            except:
                return ""
        return ""

    # --- DOSYA YÖNETİMİ VE TEMİZLİK ---
    def create_ghost_file(self, filename, content):
        """Masaüstünde bir dosya oluşturur."""
        full_path = os.path.join(self.desktop_path, filename)
        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            # Listeye ekle ki sonra silebilelim
            if full_path not in self.created_files:
                self.created_files.append(full_path)
            return full_path
        except Exception as e:
            print(f"HATA: Dosya oluşturulamadı - {e}")
            return None

    def delete_ghost_file(self, filename):
        """Masaüstündeki dosyayı siler."""
        full_path = os.path.join(self.desktop_path, filename)
        if os.path.exists(full_path):
            try:
                os.remove(full_path)
                # Listeden de çıkar
                if full_path in self.created_files:
                    self.created_files.remove(full_path)
                return True
            except Exception as e:
                print(f"HATA: Dosya silinemedi - {e}")
                return False
        return False

    def register_temp_file(self, filepath):
        """Dışarıdan oluşturulan (resim vb) dosyaları temizlik listesine ekler."""
        if filepath and filepath not in self.created_files:
            self.created_files.append(filepath)

    def cleanup_system(self):
        """ACİL DURUM PROSEDÜRÜ: Her şeyi eski haline getir."""
        print(">> TARTARUS TEMİZLİK PROTOKOLÜ DEVREDE <<")
        self.restore_wallpaper()

        for filepath in self.created_files:
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except:
                    pass
        self.created_files = []

    def get_user_name(self):
        """Bilgisayarın kullanıcı adını döndürür."""
        try:
            return os.getlogin()
        except:
            return "Human"

    def get_clipboard_text(self):
        """Panodaki metni okur."""
        if not self.root:
            return None
        try:
            return self.root.clipboard_get()
        except:
            return None

    def take_screenshot(self):
        """Ekran görüntüsü alır (Fake OS için)."""
        try:
            return pyautogui.screenshot()
        except:
            return None
