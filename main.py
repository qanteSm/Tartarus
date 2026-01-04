import tkinter as tk
from tkinter import messagebox
import time
import threading
import random
import sys
import os

# Yolları ayarla
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from managers.system_manager import SystemManager
from managers.audio_manager import AudioManager
from managers.display_manager import DisplayManager
from managers.sensor_manager import SensorManager
from managers.mind_core import MindCore

class GameController:
    def __init__(self):
        # 1. Temel Sistemleri Başlat
        self.root = tk.Tk()
        
        # 2. Sistem & Admin Kontrolü
        self.system = SystemManager(root=self.root)
        if not self.system.is_admin():
            messagebox.showwarning("Tartarus", "Admin privileges required for full immersion.\nProceeding with limited features.")
        
        self.audio = AudioManager()
        self.display = DisplayManager(self.root, self.audio)
        
        # 3. Dil Seçimi
        self.language = self.display.ask_language()
        
        # 4. Yapay Zeka & Sensörler
        API_KEY = os.getenv("TARTARUS_API_KEY") 
        self.mind = MindCore(api_key=API_KEY, language=self.language)
        self.sensor = SensorManager()
        
        # 5. Başlangıç Verileri (Fake OS & Doppelgänger)
        self.desktop_screenshot = self.system.take_screenshot()
        self.user_face_image = None # Başlangıçta null, start'ta alacağız
        self.clipboard_data = self.system.get_clipboard_text()
        
        # Oyun Durumu
        self.stage = 0
        self.current_riddle = ""
        self.is_running = True
        self.username = self.system.get_user_name()
        
        # Olay Döngülerini Bağla
        self.root.bind("<Control-Shift-Q>", lambda e: self.emergency_exit())
        self.root.bind("<Control-Shift-q>", lambda e: self.emergency_exit())
        
        self.root.after(1000, self.start_sequence)
        threading.Thread(target=self.chaos_loop, daemon=True).start()

    def start(self):
        self.sensor.start_monitoring()
        self.audio.play("drone")
        
        # Yüzü yakalamaya çalış (Kameranın ısınması için biraz beklemiş olduk)
        self.root.after(2000, self._capture_doppelganger)
        
        try:
            import pyautogui
            pyautogui.FAILSAFE = False
        except:
            pass
            
        self.display.keep_focus()
        self.root.mainloop()
    
    def _capture_doppelganger(self):
        """Kullanıcının yüzünü gizlice kaydeder."""
        face = self.sensor.get_user_face()
        if face:
            self.user_face_image = face

    def emergency_exit(self):
        print("ACİL ÇIKIŞ TETİKLENDİ.")
        self.game_over(survived=True)

    # --- OYUN AKIŞI ---

    def start_sequence(self):
        """Açılış: Masum başlar, sonra bozulur."""
        intro_text = f"CONNECTION ESTABLISHED: {self.username}" if self.language == "EN" else f"BAĞLANTI KURULDU: {self.username}"
        self.display.type_write(intro_text, speed=50, callback=self.intro_monologue)

    def intro_monologue(self):
        self.root.after(1000)
        line1 = "I am inside your walls." if self.language == "EN" else "Duvarlarının içindeyim."
        self.display.type_write(line1, color="red", speed=80)
        
        # Hayalet Dosya Oluştur
        fname = "DONT_LOOK_BEHIND_YOU.txt" if self.language == "EN" else "ARKANA_BAKMA.txt"
        content = "I SEE YOU." if self.language == "EN" else "SENİ GÖRÜYORUM."
        self.system.create_ghost_file(fname, content)
        
        # Arkadan fısıltılar
        self.audio.play("whisper_left")
        
        self.root.after(3000, self.stage_1_riddle)

    # AŞAMA 1: Bilmece + Clipboard
    def stage_1_riddle(self):
        self.stage = 1
        self.display.glitch_screen(200)
        
        # Clipboard verisini kullan
        clip_content = self.clipboard_data if self.clipboard_data and len(self.clipboard_data) < 50 else None
        self.current_riddle = self.mind.generate_riddle(clipboard_content)
        
        self.display.type_write(self.current_riddle, color="white", speed=30)
        self.root.after(2000, lambda: self.display.create_input(self.handle_riddle_answer))

    def handle_riddle_answer(self, answer):
        is_correct, reaction = self.mind.check_answer(self.current_riddle, answer)
        self.display.type_write(reaction, color="yellow" if is_correct else "red")
        
        if is_correct:
            self.root.after(3000, self.stage_2_weeping_angel)
        else:
            self.punish_player()
            self.root.after(2000, self.stage_1_riddle)

    # AŞAMA 2: Weeping Angel (Göz Teması)
    def stage_2_weeping_angel(self):
        self.stage = 2
        msg = "DON'T LOOK AWAY." if self.language == "EN" else "SAKIN GÖZLERİNİ KAÇIRMA."
        self.display.type_write(msg, color="red")
        
        self.angel_check_active = True
        self.angel_timer = 100 # 10 saniyelik hayatta kalma
        self.check_angel_loop()

    def check_angel_loop(self):
        if not self.angel_check_active: return
        
        looking = self.sensor.check_gaze()
        
        if not looking:
            # Bakmıyorsa ses artar, ekran kararır
            self.audio.play("screech")
            self.display.lbl_main.config(fg="darkred")
        else:
            self.display.lbl_main.config(fg="red")

        self.angel_timer -= 1
        if self.angel_timer <= 0:
            self.angel_check_active = False
            self.stage_3_fake_os()
        else:
            self.root.after(100, self.check_angel_loop)

    # AŞAMA 3: Fake OS (İllüzyon)
    def stage_3_fake_os(self):
        self.stage = 3
        # Ekran görüntüsünü bas
        if self.desktop_screenshot:
            self.display.start_fake_os_mode(self.desktop_screenshot)
            # Fake OS modunda display manager 6 saniye sonra otomatik "Burası artık yok" yazacak.
            # Biz sadece bir sonraki aşamaya geçişi tetikleyelim.
            self.root.after(8000, self.stage_4_breath)
        else:
            # Screenshot alınamadıysa direkt geç
            self.stage_4_breath()

    # AŞAMA 4: Breath Detection (Nefes Tutma)
    def stage_4_breath(self):
        self.stage = 4
        msg = "DON'T BREATHE. I CAN HEAR YOU." if self.language == "EN" else "NEFES ALMA. SENİ DUYABİLİYORUM."
        self.display.type_write(msg, color="white")
        
        # Arka plan sessizliği
        self.audio.play("drone") 
        
        self.breath_timer = 50 # 5 saniye
        self.check_breath_loop()

    def check_breath_loop(self):
        # Gürültü seviyesi 500'ü geçerse (hassas) yakala
        noise = self.sensor.get_noise_level_raw()
        if noise > 500: 
            self.punish_player()
            self.display.type_write("I HEARD YOU BREATHING.", color="red")
        
        self.breath_timer -= 1
        if self.breath_timer <= 0:
            self.stage_5_finale()
        else:
            self.root.after(100, self.check_breath_loop)

    # AŞAMA 5: Finale (Doppelgänger + Emre)
    def stage_5_finale(self):
        self.stage = 5
        self.mind.update_persona_to_victim()
        
        # Emre konuşuyor
        help_msg = self.mind.model.generate_content("Kullanıcıdan yardım iste.").text
        self.display.type_write(help_msg, color="cyan", speed=40)
        
        self.root.after(4000, self.reveal_doppelganger)

    def reveal_doppelganger(self):
        if self.user_face_image:
            # Yüzü göster
            self.display.show_jumpscare(self.user_face_image) # Jumpscare olarak göster
            
        final_msg = "YOU ARE REPLACED." if self.language == "EN" else "ARTIK SENİN YERİNE BEN GEÇTİM."
        self.display.type_write(final_msg, color="red")
        self.root.after(3000, lambda: self.game_over(survived=False))

    def punish_player(self):
        self.display.glitch_screen(500)
        self.audio.play("screech")
        # Anlık yüzü al (korkmuş yüz)
        scary = self.sensor.get_user_face() # Normal alalım, sensor manager işlemeden
        self.display.show_jumpscare(scary)

    def chaos_loop(self):
        """Arka plan olayları."""
        while self.is_running:
            time.sleep(random.randint(8, 15))
            # 3D Fısıltılar
            if random.random() < 0.3:
                side = random.choice(["whisper_left", "whisper_right"])
                self.audio.play_async(side)
            
            # Mouse Chaos
            if random.random() < 0.2:
                self.sensor.trigger_mouse_chaos()

    def game_over(self, survived):
        self.is_running = False
        self.sensor.stop_monitoring()
        self.audio.stop_all()
        if survived:
            self.root.quit()
        else:
            self.root.quit()
            # Gerçek bir kapanış efekti eklenebilir.

if __name__ == "__main__":
    game = GameController()
    game.start()
