import tkinter as tk
from tkinter import font
import random
from PIL import Image, ImageTk

class DisplayManager:
    def __init__(self, root, audio_manager):
        self.root = root
        self.audio = audio_manager
        
        # Ekran Özellikleri
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        
        # Konfigürasyon
        self.root.configure(bg='black', cursor="none")
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.protocol("WM_DELETE_WINDOW", lambda: None) # Alt+F4 engelle
        
        # Ana Konteyner
        self.main_frame = tk.Frame(self.root, bg="black")
        self.main_frame.pack(fill="both", expand=True)

        # Widgetlar
        self.lbl_main = tk.Label(self.main_frame, text="", font=("Consolas", 24, "bold"), fg="#00ff00", bg="black", wraplength=self.width - 100)
        self.lbl_main.place(relx=0.5, rely=0.4, anchor="center")
        
        self.lbl_sub = tk.Label(self.main_frame, text="", font=("Arial", 12), fg="white", bg="black")
        self.lbl_sub.place(relx=0.5, rely=0.6, anchor="center")
        
        self.entry = None

    def ask_language(self):
        """Oyun başlamadan önce dil seçimi penceresi (Statik/Blocking değil, kendi loop'u var)"""
        # Bu fonksiyon root'tan bağımsız çalışmalı, ama root zaten var.
        # Bu yüzden root'u geçici olarak küçük pencere yapalım.
        self.root.attributes('-fullscreen', False)
        self.root.geometry("400x200")
        self.root.title("TARTARUS SYSTEM BOOT")
        self.root.configure(cursor="arrow")
        
        lang_var = tk.StringVar(value="TR")
        
        def set_lang(l):
            lang_var.set(l)
            self.root.quit() # mainloop'u kır, ama pencereyi kapatma
            
        lbl = tk.Label(self.root, text="SELECT LANGUAGE / DİL SEÇİNİZ", bg="black", fg="white", font=("Arial", 14))
        lbl.pack(pady=20)
        
        btn_tr = tk.Button(self.root, text="TÜRKÇE", command=lambda: set_lang("TR"), width=15)
        btn_tr.pack(pady=5)
        
        btn_en = tk.Button(self.root, text="ENGLISH", command=lambda: set_lang("EN"), width=15)
        btn_en.pack(pady=5)
        
        self.root.mainloop() # Kullanıcı seçene kadar bekle
        
        # Seçim yapıldı, tam ekrana geç
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.__init__(self.root, self.audio) # Yeniden başlat
        return lang_var.get()

    def type_write(self, text, speed=50, color="#00ff00", callback=None):
        """
        Daktilo efektiyle yazı yazar. Blocking değildir (root.after kullanır).
        speed: milisaniye cinsinden karakter arası bekleme.
        """
        self.lbl_main.config(text="", fg=color)
        self._type_next_char(text, 0, speed, callback)

    def _type_next_char(self, text, index, speed, callback):
        if index < len(text):
            current_text = text[:index+1] + "█" # İmleç efekti
            self.lbl_main.config(text=current_text)
            
            # Rastgele ses efekti
            if index % 3 == 0:
                self.audio.play("beep")
            
            self.root.after(speed, lambda: self._type_next_char(text, index+1, speed, callback))
        else:
            self.lbl_main.config(text=text) # İmleci kaldır
            if callback:
                callback()

    def glitch_screen(self, duration=500):
        """Ekranı kısa süreliğine bozar."""
        original_bg = self.root.cget("bg")
        
        def toggle_invert(count):
            if count <= 0:
                self.root.configure(bg="black")
                self.lbl_main.configure(fg="#00ff00", bg="black")
                return
            
            # Renkleri ters çevir
            if count % 2 == 0:
                self.root.configure(bg="white")
                self.lbl_main.configure(fg="black", bg="white")
            else:
                self.root.configure(bg="black")
                self.lbl_main.configure(fg="red", bg="black") # Kırmızı glitch
                self.audio.play("static")
            
            self.root.after(50, lambda: toggle_invert(count-1))
            
        toggle_invert(duration // 50)

    def show_jumpscare(self, pil_image=None):
        """
        Jumpscare gösterir.
        pil_image: PIL Image objesi veya None.
        """
        # Thread-safe hale getir
        self.root.after(0, lambda: self._show_jumpscare_internal(pil_image))

    def _show_jumpscare_internal(self, pil_image):
        top = tk.Toplevel(self.root)
        top.attributes('-fullscreen', True)
        top.attributes('-topmost', True)
        top.configure(bg="red")
        
        if pil_image:
            try:
                img = pil_image.resize((self.width, self.height))
                img_tk = ImageTk.PhotoImage(img)
                lbl = tk.Label(top, image=img_tk)
                lbl.image = img_tk
                lbl.pack(fill="both", expand=True)
            except Exception as e:
                print(f"Jumpscare hatası: {e}")
        
        self.audio.play("screech")
        self.root.after(500, top.destroy)

    def start_fake_os_mode(self, screenshot):
        """Sahte Masaüstü modunu başlatır."""
        self.root.after(0, lambda: self._fake_os_internal(screenshot))
        
    def _fake_os_internal(self, screenshot):
        if not screenshot:
            return
            
        # Ekranı temizle
        self.main_frame.pack_forget()
        
        # Screenshot'ı bas
        img = screenshot.resize((self.width, self.height))
        img_tk = ImageTk.PhotoImage(img)
        
        lbl_bg = tk.Label(self.root, image=img_tk, borderwidth=0)
        lbl_bg.image = img_tk
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Fake crash
        self.root.config(cursor="arrow")
        
        # 5 saniye sonra "kanama" efekti veya glitch
        self.root.after(5000, lambda: self.glitch_screen(1000))
        self.root.after(6000, lambda: self.type_write("BURASI ARTIK YOK.", color="red"))

    def keep_focus(self):
        """Pencereyi sürekli üstte tutar."""
        self.root.focus_force()
        self.root.after(1000, self.keep_focus)

    def create_input(self, callback):
        """Kullanıcıdan veri almak için giriş kutusu oluşturur."""
        self.root.config(cursor="arrow")
        self.entry = tk.Entry(self.root, font=("Consolas", 20), bg="#111", fg="white", insertbackground="white", justify='center')
        self.entry.place(relx=0.5, rely=0.8, anchor="center", width=400)
        self.entry.focus_set()
        
        def on_submit(event=None):
            text = self.entry.get()
            self.entry.destroy()
            self.root.config(cursor="none")
            callback(text)
            
        self.entry.bind("<Return>", on_submit)

    def clear(self):
        self.lbl_main.config(text="")
        self.lbl_sub.config(text="")
