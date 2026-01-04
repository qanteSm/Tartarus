import cv2
import threading
import time
import numpy as np
import speech_recognition as sr
import pyautogui
from PIL import Image

class SensorManager:
    def __init__(self):
        self.camera_active = False
        self.mic_active = False
        self.last_frame = None
        self.noise_level = 0
        self.recognizer = sr.Recognizer()
        self.is_looking_at_screen = False  # YENİ: Sonucu burada saklayacağız
        
        # Jumpscare için yüz/göz tespiti (Haar Cascades)
        self.face_cascade = None
        try:
            # OpenCV'nin içinde gelen cascade'i kullan
            path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.face_cascade = cv2.CascadeClassifier(path)
        except:
            print("Yüz tanıma modülü yüklenemedi.")

    def start_monitoring(self):
        """Kamera ve Mikrofon izlemeyi başlatır."""
        self.camera_active = True
        self.mic_active = True
        
        threading.Thread(target=self._camera_loop, daemon=True).start()
        threading.Thread(target=self._mic_loop, daemon=True).start()

    def stop_monitoring(self):
        self.camera_active = False
        self.mic_active = False

    def _camera_loop(self):
        cap = cv2.VideoCapture(0)
        while self.camera_active:
            ret, frame = cap.read()
            if ret:
                self.last_frame = frame

                # --- DÜZELTME BAŞLANGICI ---
                # Görüntü işlemeyi Thread içinde yapıyoruz, GUI donmuyor.
                if self.face_cascade:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
                    self.is_looking_at_screen = len(faces) > 0
                # --- DÜZELTME BİTİŞİ ---

            time.sleep(0.05)
        cap.release()

    def get_user_face(self):
        """Kullanıcının yüzünün normal bir görüntüsünü alır (Doppelgänger için)."""
        if self.last_frame is None:
            return None
        
        # BGR -> RGB
        rgb = cv2.cvtColor(self.last_frame, cv2.COLOR_BGR2RGB)
        return Image.fromarray(rgb)

    def check_gaze(self):
        """Artık işlem yapmıyor, sadece son sonucu anlık döndürüyor."""
        return self.is_looking_at_screen

    def get_noise_level_raw(self):
        """Ham gürültü seviyesini döndürür."""
        return self.noise_level

    def _mic_loop(self):
        # Arka plan gürültüsünü dinler (Basit versiyon: Sadece seviye ölçer)
        # Tam speech recognition yavaşlatabilir, o yüzden sadece enerji seviyesi bakalım.
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                while self.mic_active:
                    try:
                        audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=2)
                        # Basit enerji seviyesi tahmini (SpeechRecognition doğrudan enerji vermez, ama byte data uzunluğu veya içeriği fikir verir)
                        # Daha iyisi: audio.get_raw_data() üzerinden RMS hesaplamak.
                        data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
                        rms = np.sqrt(np.mean(data**2))
                        self.noise_level = int(rms)
                        time.sleep(0.1)
                        # Resetleme hemen yapılmaz, continuous akış lazım ama bu loop iş görür.
                    except sr.WaitTimeoutError:
                        self.noise_level = 0
                        self.noise_level = 0
                    except:
                        pass
        except:
            print("Mikrofon hatası.")

    def get_scary_face(self):
        """Kameradan son görüntüyü alıp 'şeytanileştirir'."""
        if self.last_frame is None:
            return None
        
        frame = self.last_frame.copy()
        
        # 1. Griye çevir
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 2. Negatif yap
        inv = cv2.bitwise_not(gray)
        
        # 3. Kontrastı patlat (Threshold)
        _, thresh = cv2.threshold(inv, 100, 255, cv2.THRESH_BINARY)
        
        # 4. Gürültü ekle
        noise = np.random.randint(0, 50, thresh.shape, dtype='uint8')
        final = cv2.add(thresh, noise)
        
        # PIL Image'a çevir
        return Image.fromarray(final)

    def is_noisy(self):
        """Ortam gürültülü mü?"""
        return self.noise_level > 50

    def trigger_mouse_chaos(self):
        """Mouse'u rastgele oynatır."""
        try:
            x, y = pyautogui.position()
            pyautogui.moveTo(x + np.random.randint(-50, 50), y + np.random.randint(-50, 50))
        except:
            pass
