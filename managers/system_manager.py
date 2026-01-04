import os
import sys
import ctypes
import platform
import pyautogui
import tkinter as tk

class SystemManager:
    def __init__(self, root=None):
        self.os_type = platform.system()
        self.desktop_path = self._get_desktop_path()
        self.root = root

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

    def create_ghost_file(self, filename, content):
        """Masaüstünde bir dosya oluşturur."""
        full_path = os.path.join(self.desktop_path, filename)
        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
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
                return True
            except Exception as e:
                print(f"HATA: Dosya silinemedi - {e}")
                return False
        return False

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
