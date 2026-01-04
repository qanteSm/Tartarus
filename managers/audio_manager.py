import pygame
import numpy as np
import threading
import time
import random

class AudioManager:
    def __init__(self):
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self.active = True
        except Exception as e:
            print(f"Ses motoru başlatılamadı: {e}")
            self.active = False
        
        self.sounds = {}
        if self.active:
            self._generate_library()

    def _generate_wave(self, freq, duration, type="sine", volume=0.5, pan=0.0):
        """
        Numpy kullanarak ses dalgası oluşturur.
        type: 'sine', 'square', 'sawtooth', 'noise'
        pan: -1.0 (Sol) ile 1.0 (Sağ) arası.
        """
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        t = np.linspace(0, duration, n_samples, False)
        
        if type == "sine":
            wave = np.sin(2 * np.pi * freq * t)
        elif type == "square":
            wave = np.sign(np.sin(2 * np.pi * freq * t))
        elif type == "sawtooth":
            wave = 2 * (t * freq - np.floor(t * freq + 0.5))
        elif type == "noise":
            wave = np.random.uniform(-1, 1, n_samples)
        else:
            wave = np.zeros(n_samples)

        # Stereo Panning (3D Ses)
        # pan = 0.0 -> Sol: 1.0, Sağ: 1.0
        # pan = -1.0 -> Sol: 2.0, Sağ: 0.0 (Basit lineer pan)
        left_vol = 1.0 - pan if pan > 0 else 1.0
        right_vol = 1.0 + pan if pan < 0 else 1.0
        
        left_channel = wave * left_vol
        right_channel = wave * right_vol

        stereo_wave = np.column_stack((left_channel, right_channel))
        
        # 16-bit integer'a çevir
        audio_data = (stereo_wave * volume * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(audio_data)

    def _generate_library(self):
        """Oyun için gerekli sesleri dinamik olarak üretir."""
        print("Sesler sentezleniyor...")
        
        # 1. DRONE (Arka plan gerilimi) - Düşük frekanslı sine dalgaları
        drone_base = self._generate_wave(50, 2.0, "sine", 0.3) 
        self.sounds["drone"] = drone_base

        # 2. BEEP (Bilgisayar sesi)
        self.sounds["beep"] = self._generate_wave(800, 0.1, "sine", 0.1)
        self.sounds["error"] = self._generate_wave(150, 0.4, "sawtooth", 0.2)
        
        # 3. WHISPERS (3D Fısıltılar)
        self.sounds["whisper_left"] = self._generate_wave(100, 0.5, "noise", 0.1, pan=-0.8)
        self.sounds["whisper_right"] = self._generate_wave(100, 0.5, "noise", 0.1, pan=0.8)

        # 4. SCREECH (Jumpscare) - Karışık yüksek frekanslar
        # Bunu biraz daha kaotik yapalım
        sr = 44100
        dur = 0.5
        t = np.linspace(0, dur, int(sr*dur), False)
        # Frekans modülasyonu
        mod = 500 * np.sin(2*np.pi*20*t)
        carrier = np.sign(np.sin(2*np.pi*(3000+mod)*t)) # Kare dalga çığlık
        noise = np.random.uniform(-0.5, 0.5, len(t))
        final = (carrier + noise) * 0.5
        stereo = np.column_stack((final, final))
        data = (stereo * 32767).astype(np.int16)
        self.sounds["screech"] = pygame.sndarray.make_sound(data)

        # 4. STATIC (Sinyal kaybı)
        self.sounds["static"] = self._generate_wave(0, 1.0, "noise", 0.15)

    def play(self, name, loops=0):
        if not self.active or name not in self.sounds:
            return
        
        # Arka plan için ayrı kanal, efektler için ayrı
        if name == "drone":
            self.sounds[name].play(loops=-1, fade_ms=2000)
        else:
            self.sounds[name].play(loops=loops)

    def stop_all(self):
        if self.active:
            pygame.mixer.stop()

    def play_async(self, name):
        """Thread içinde ses çalar (Gerekirse)"""
        threading.Thread(target=lambda: self.play(name)).start()
