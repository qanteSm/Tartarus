import tkinter as tk
from tkinter import messagebox
import time
import threading
import random
import sys
import os
import atexit
import queue

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from managers.system_manager import SystemManager
from managers.audio_manager import AudioManager
from managers.display_manager import DisplayManager
from managers.sensor_manager import SensorManager
from managers.mind_core import MindCore

class GameController:
    def __init__(self):
        self.root = tk.Tk()
        self.audio = AudioManager()
        self.display = DisplayManager(self.root, self.audio)
        self.system = SystemManager(root=self.root)
        self.sensor = SensorManager()
        self.mind = MindCore(language="TR")

        self.phase = 1 
        self.is_running = True
        self.usb_stage = 0 
        self.last_usb_list = []
        self.darkness_compliant = False
        self.panic_mode = False
        
        self.message_queue = queue.Queue()

        atexit.register(self.cleanup)
        self.root.bind("<Control-Shift-Q>", lambda e: self.emergency_exit())
        
        self.sensor.start_monitoring()
        self.root.after(1000, self.game_loop)
        self.root.after(100, self.process_message_queue)
        
        threading.Thread(target=self.internet_monitoring_loop, daemon=True).start()
        
        self.root.bind("<u>", lambda e: self.simulate_usb_event())
        self.root.bind("<i>", lambda e: self.simulate_internet_toggle())
        self.debug_internet = True
        self.internet_status_safe = True

    def start(self):
        self.display.root.mainloop()

    def cleanup(self):
        self.system.cleanup_system()
        self.sensor.stop_monitoring()
        self.audio.stop_all()

    def emergency_exit(self):
        self.cleanup()
        self.root.quit()

    def simulate_usb_event(self):
        self.handle_usb_logic(simulated=True)

    def simulate_internet_toggle(self):
        self.debug_internet = not self.debug_internet

    def internet_monitoring_loop(self):
        while self.is_running:
            real_status = self.system.check_internet()
            status = real_status if self.debug_internet else False
            self.internet_status_safe = status
            
            if not status:
                if not self.panic_mode:
                    self.message_queue.put(("PANIC_START", None))
            else:
                if self.panic_mode:
                    self.message_queue.put(("PANIC_STOP", None))
            
            time.sleep(2)

    def process_message_queue(self):
        try:
            while True:
                msg_type, data = self.message_queue.get_nowait()
                if msg_type == "PANIC_START":
                    self.trigger_panic_mode()
                elif msg_type == "PANIC_STOP":
                    self.stop_panic_mode()
                elif msg_type == "SHOW_MSG":
                    self.display.show_ghost_message(data[0], **data[1])
                elif msg_type == "PLAY_SOUND":
                    self.audio.play(data)
                elif msg_type == "FLASHBANG":
                    self.display.trigger_flashbang()
                elif msg_type == "PURGE":
                    self.phase_4_purge()
        except queue.Empty:
            pass
        self.root.after(100, self.process_message_queue)

    def game_loop(self):
        if not self.is_running: return

        self.check_darkness()
        self.check_jealousy() 
        self.check_usb_real()

        if self.phase == 1:
            self.phase_1_infiltration()
        elif self.phase == 2:
            self.phase_2_manifestation()
        elif self.phase == 3:
            self.phase_3_ritual()
        
        self.root.after(1000, self.game_loop)

    def trigger_panic_mode(self):
        self.panic_mode = True
        self.audio.play("static")
        self.audio.play("screech")
        
        def async_gen():
            msg = self.mind.generate_panic_reaction()
            self.message_queue.put(("SHOW_MSG", (msg, {"duration": 5000, "color": "red", "font_size": 40})))
            self.message_queue.put(("FLASHBANG", None))
            
        threading.Thread(target=async_gen, daemon=True).start()

    def stop_panic_mode(self):
        self.panic_mode = False
        self.audio.stop_all()
        self.audio.play("drone")

    def check_darkness(self):
        brightness = self.sensor.get_brightness()
        self.darkness_compliant = brightness < 50

    def check_jealousy(self):
        looking = self.sensor.check_gaze()
        if not looking and random.random() < 0.1: 
            self.audio.play("whisper_left")
            self.display.show_ghost_message("BURAYA BAK.", duration=1000, color="gray", font_size=12)

    def check_usb_real(self):
        current_drives = self.system.check_usb_drives()
        if len(current_drives) > len(self.last_usb_list):
            self.handle_usb_logic(simulated=False, drive_letter=current_drives[-1])
        
        self.last_usb_list = current_drives

    def phase_1_infiltration(self):
        if random.random() < 0.05:
            self.sensor.trigger_mouse_chaos()
        
        if random.random() < 0.02:
            self.system.toggle_caps_lock()

        if random.random() < 0.01: 
            self.transition_to_phase_2()

    def transition_to_phase_2(self):
        self.phase = 2
        self.display.show_ghost_message("SENİ GÖRÜYORUM.", duration=4000, color="red")
        self.audio.play("drone")
        self.system.create_ghost_file("O_BURADA.txt", "Artık çok geç.")
        
        face = self.sensor.get_scary_face()
        if face:
            path = os.path.abspath("cache_face.png")
            face.save(path)
            self.system.register_temp_file(path)
            self.system.change_wallpaper(path)

    def phase_2_manifestation(self):
        if random.random() < 0.1:
             def async_gen():
                msg = self.mind.generate_idle_threat()
                self.message_queue.put(("SHOW_MSG", (msg, {"duration": 2000})))
             threading.Thread(target=async_gen, daemon=True).start()

        if random.random() < 0.05:
            self.transition_to_phase_3()

    def transition_to_phase_3(self):
        self.phase = 3
        self.system.create_ghost_file("RITUEL_KILAVUZU.txt", "1. Işıkları söndür.\n2. USB Bellek hazırla.\n3. Beni içinden söküp at.")
        self.display.show_ghost_message("RİTÜEL BAŞLADI.", font_size=30)

    def phase_3_ritual(self):
        if not self.darkness_compliant:
            if random.random() < 0.1:
                def async_gen():
                    msg = self.mind.generate_darkness_demand()
                    self.message_queue.put(("SHOW_MSG", (msg, {"color": "white"})))
                threading.Thread(target=async_gen, daemon=True).start()
                self.system.toggle_caps_lock()
            return 

    def handle_usb_logic(self, simulated=False, drive_letter="E:\\"):
        if self.phase != 3: return
        
        self.usb_stage += 1
        
        def async_gen(stage):
            reaction = self.mind.generate_usb_reaction(stage)
            self.message_queue.put(("SHOW_MSG", (reaction, {"duration": 4000, "font_size": 25})))
            self.message_queue.put(("PLAY_SOUND", "error"))

            if stage == 1:
                if not simulated: self.system.rename_usb_label(drive_letter, "ACITIYOR")
            elif stage == 2:
                self.message_queue.put(("PLAY_SOUND", "riser"))
                if not simulated: self.system.write_blob_to_usb(drive_letter)
            elif stage >= 3:
                self.message_queue.put(("PURGE", None))
        
        threading.Thread(target=async_gen, args=(self.usb_stage,), daemon=True).start()

    def phase_4_purge(self):
        self.phase = 4
        self.display.trigger_flashbang()
        self.audio.play("screech")
        
        self.root.after(2000, self.finish_game)

    def finish_game(self):
        self.system.create_ghost_file("TESEKKURLER.txt", "Artık özgürüm.")
        self.system.cleanup_system()
        self.root.quit()

if __name__ == "__main__":
    game = GameController()
    game.start()
