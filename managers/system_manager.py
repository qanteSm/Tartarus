import os
import sys
import ctypes
import platform
import pyautogui
import tkinter as tk
import random
import psutil
import time
import requests

class SystemManager:
    def __init__(self, root=None):
        self.os_type = platform.system()
        self.desktop_path = self._get_desktop_path()
        self.root = root
        
        self.created_files = []
        self.original_wallpaper = self._get_current_wallpaper()

    def _get_desktop_path(self):
        try:
            return os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 
        except:
            return os.path.join(os.path.expanduser("~"), "Desktop")

    def is_admin(self):
        if self.os_type == "Windows":
            try:
                return ctypes.windll.shell32.IsUserAnAdmin()
            except:
                return False
        else:
            return os.geteuid() == 0

    def _get_current_wallpaper(self):
        if self.os_type == "Windows":
            try:
                ubuffer = ctypes.create_unicode_buffer(512)
                ctypes.windll.user32.SystemParametersInfoW(0x0073, 512, ubuffer, 0)
                return ubuffer.value
            except:
                return None
        return None

    def change_wallpaper(self, image_path):
        if self.os_type == "Windows":
            try:
                ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
            except:
                pass

    def restore_wallpaper(self):
        if self.original_wallpaper and os.path.exists(self.original_wallpaper):
            self.change_wallpaper(self.original_wallpaper)

    def get_desktop_items(self, max_items=5):
        try:
            items = os.listdir(self.desktop_path)
            ignored = ["desktop.ini", "TARTARUS_LOGS", "DONT_LOOK_BEHIND_YOU.txt", "ini", "BENI_SIL.txt", "RITUEL_KILAVUZU.txt"]
            clean_items = [i for i in items if i not in ignored and not i.startswith(".")]
            
            if len(clean_items) > max_items:
                return random.sample(clean_items, max_items)
            return clean_items
        except:
            return []

    def get_location_info(self):
        try:
            data = requests.get("http://ip-api.com/json/", timeout=2).json()
            return data.get("city"), data.get("isp")
        except:
            return None, None

    def get_active_window(self):
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

    def create_ghost_file(self, filename, content):
        full_path = os.path.join(self.desktop_path, filename)
        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            if full_path not in self.created_files:
                self.created_files.append(full_path)
            return full_path
        except Exception as e:
            print(f"HATA: Dosya oluşturulamadı - {e}")
            return None

    def delete_ghost_file(self, filename):
        full_path = os.path.join(self.desktop_path, filename)
        if os.path.exists(full_path):
            try:
                os.remove(full_path)
                if full_path in self.created_files:
                    self.created_files.remove(full_path)
                return True
            except Exception as e:
                print(f"HATA: Dosya silinemedi - {e}")
                return False
        return False

    def rename_file_on_desktop(self, old_name, new_name):
        old_path = os.path.join(self.desktop_path, old_name)
        new_path = os.path.join(self.desktop_path, new_name)
        if os.path.exists(old_path):
            try:
                os.rename(old_path, new_path)
                return True
            except:
                return False
        return False

    def register_temp_file(self, filepath):
        if filepath and filepath not in self.created_files:
            self.created_files.append(filepath)

    def cleanup_system(self):
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
        try:
            return os.getlogin()
        except:
            return "Human"

    def get_clipboard_text(self):
        if not self.root:
            return None
        try:
            return self.root.clipboard_get()
        except:
            return None

    def take_screenshot(self):
        try:
            return pyautogui.screenshot()
        except:
            return None

    # --- HARDWARE EXORCISM NEW METHODS ---

    def check_usb_drives(self):
        """Returns a list of removable drives (mount points)."""
        drives = []
        try:
            partitions = psutil.disk_partitions()
            for p in partitions:
                if 'removable' in p.opts or 'cdrom' in p.opts or 'usb' in p.opts:
                     drives.append(p.mountpoint)
                elif self.os_type == "Windows" and 'removable' in p.opts:
                     drives.append(p.mountpoint)
        except:
            pass
        return drives

    def check_internet(self):
        """Pings Google DNS to check connection."""
        try:
            requests.get("http://8.8.8.8", timeout=1)
            return True
        except:
            return False

    def set_volume_mute(self, mute=True):
        """Sets system volume to 0 or mute (Windows only stub)."""
        if self.os_type == "Windows":
             # In a real scenario we would use pycaw or ctypes sendinput for volume keys
             pass
    
    def toggle_caps_lock(self):
        """Toggles Caps Lock (Windows only stub)."""
        if self.os_type == "Windows":
             try:
                 import ctypes
                 VK_CAPITAL = 0x14
                 ctypes.windll.user32.keybd_event(VK_CAPITAL, 0x45, 1, 0)
                 ctypes.windll.user32.keybd_event(VK_CAPITAL, 0x45, 3, 0)
             except:
                 pass

    def write_blob_to_usb(self, drive_letter):
        """Writes a 1GB dummy file to the USB drive."""
        try:
            path = os.path.join(drive_letter, "TARTARUS_PARCA_1.blob")
            # For demo purposes, we write a small file, not 1GB, to avoid disk space issues in testing
            with open(path, "wb") as f:
                f.write(os.urandom(1024 * 1024)) # 1MB for safety in dev
            return True
        except:
            return False
    
    def rename_usb_label(self, drive_letter, label="IT_HURTS"):
        """Renames the USB drive label (Windows specific)."""
        if self.os_type == "Windows":
            try:
                drive_root = drive_letter.split("\\")[0] + "\\"
                ctypes.windll.kernel32.SetVolumeLabelW(drive_root, label)
                return True
            except:
                return False
        return False
