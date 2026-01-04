import pygame
import numpy as np
import threading
import time
import random

class AudioManager:
    def __init__(self):
        self.active = False
        try:
            # Try initializing with specific parameters, fallback if fails
            pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
            pygame.mixer.init()
            self.active = True
        except Exception as e:
            print(f"Ses motoru başlatılamadı: {e}")
            self.active = False
        
        self.sounds = {}
        if self.active:
            try:
                self._generate_library()
            except Exception as e:
                print(f"Ses kütüphanesi oluşturulurken hata: {e}")
                self.active = False

    def _generate_wave(self, freq, duration, type="sine", volume=0.5, pan=0.0):
        """
        Numpy kullanarak ses dalgası oluşturur.
        """
        if not self.active: return None
        
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

        left_vol = 1.0 - pan if pan > 0 else 1.0
        right_vol = 1.0 + pan if pan < 0 else 1.0
        
        left_channel = wave * left_vol
        right_channel = wave * right_vol

        stereo_wave = np.column_stack((left_channel, right_channel))
        
        audio_data = (stereo_wave * volume * 32767).astype(np.int16)
        try:
            return pygame.sndarray.make_sound(audio_data)
        except:
            return None

    def _generate_library(self):
        """Oyun için gerekli sesleri dinamik olarak üretir."""
        print("Sesler sentezleniyor...")
        
        self.sounds["drone"] = self._generate_wave(50, 2.0, "sine", 0.3)
        self.sounds["beep"] = self._generate_wave(800, 0.1, "sine", 0.1)
        self.sounds["error"] = self._generate_wave(150, 0.4, "sawtooth", 0.2)
        
        self.sounds["whisper_left"] = self._generate_wave(100, 0.5, "noise", 0.1, pan=-0.8)
        self.sounds["whisper_right"] = self._generate_wave(100, 0.5, "noise", 0.1, pan=0.8)
        self.sounds["static"] = self._generate_wave(0, 1.0, "noise", 0.15)

        # Screech Generation
        sr = 44100
        dur = 0.5
        t = np.linspace(0, dur, int(sr*dur), False)
        mod = 500 * np.sin(2*np.pi*20*t)
        carrier = np.sign(np.sin(2*np.pi*(3000+mod)*t))
        noise = np.random.uniform(-0.5, 0.5, len(t))
        final = (carrier + noise) * 0.5
        stereo = np.column_stack((final, final))
        data = (stereo * 32767).astype(np.int16)
        try:
            self.sounds["screech"] = pygame.sndarray.make_sound(data)
        except:
            pass

        # Shepard Tone (Illusion of rising pitch)
        # Simplified simulation: overlapping rising sines
        # Doing a real shepard tone procedurally is complex, we will simulate a 'Riser'
        dur = 3.0
        t = np.linspace(0, dur, int(sr*dur), False)
        freq_start = 100
        freq_end = 400
        # Chirp signal
        k = (freq_end - freq_start) / dur
        chirp = np.sin(2 * np.pi * (freq_start * t + (k/2)*t**2))
        stereo_chirp = np.column_stack((chirp, chirp))
        data_chirp = (stereo_chirp * 32767 * 0.4).astype(np.int16)
        try:
            self.sounds["riser"] = pygame.sndarray.make_sound(data_chirp)
        except:
            pass

    def play(self, name, loops=0):
        if not self.active or name not in self.sounds or self.sounds[name] is None:
            return
        
        try:
            if name == "drone":
                self.sounds[name].play(loops=-1, fade_ms=2000)
            else:
                self.sounds[name].play(loops=loops)
        except:
            pass

    def stop_all(self):
        if self.active:
            try:
                pygame.mixer.stop()
            except:
                pass

    def play_async(self, name):
        """Thread içinde ses çalar (Gerekirse)"""
        if self.active:
            threading.Thread(target=lambda: self.play(name)).start()
