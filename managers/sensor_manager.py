import cv2
import threading
import time
import numpy as np
import speech_recognition as sr
import pyautogui
import os
from PIL import Image

class SensorManager:
    def __init__(self):
        self.camera_active = False
        self.mic_active = False
        self.last_frame = None
        self.noise_level = 0
        self.recognizer = sr.Recognizer()
        self.is_looking_at_screen = False
        self.avg_brightness = 255
        
        self.face_cascade = None
        try:
            path = os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml')
            if not os.path.exists(path):
                path = 'haarcascade_frontalface_default.xml'
            
            classifier = cv2.CascadeClassifier(path)
            if classifier.empty():
                print("Hata: Cascade yüklenemedi (Empty).")
                self.face_cascade = None
            else:
                self.face_cascade = classifier
        except Exception as e:
            print(f"Yüz tanıma modülü yüklenemedi: {e}")
            self.face_cascade = None

    def start_monitoring(self):
        self.camera_active = True
        self.mic_active = True
        
        threading.Thread(target=self._camera_loop, daemon=True).start()
        threading.Thread(target=self._mic_loop, daemon=True).start()

    def stop_monitoring(self):
        self.camera_active = False
        self.mic_active = False

    def _camera_loop(self):
        cap = cv2.VideoCapture(0)
        delay = 0.5 
        
        while self.camera_active:
            try:
                ret, frame = cap.read()
                if ret:
                    self.last_frame = frame
                    
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    self.avg_brightness = np.mean(gray)
                    
                    if self.face_cascade:
                        try:
                            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
                            self.is_looking_at_screen = len(faces) > 0
                        except Exception as e:
                            print(f"Face detect error: {e}")
                            self.face_cascade = None
            except Exception as e:
                pass
            
            time.sleep(delay)
            
        cap.release()

    def get_brightness(self):
        return self.avg_brightness

    def get_user_face(self):
        if self.last_frame is None:
            return None
        
        rgb = cv2.cvtColor(self.last_frame, cv2.COLOR_BGR2RGB)
        return Image.fromarray(rgb)

    def check_gaze(self):
        return self.is_looking_at_screen

    def get_noise_level_raw(self):
        return self.noise_level

    def _mic_loop(self):
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                while self.mic_active:
                    try:
                        audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=2)
                        data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
                        rms = np.sqrt(np.mean(data**2))
                        self.noise_level = int(rms)
                        time.sleep(0.1)
                    except sr.WaitTimeoutError:
                        self.noise_level = 0
                    except:
                        pass
        except:
            print("Mikrofon hatası.")

    def get_scary_face(self):
        if self.last_frame is None:
            return None
        
        frame = self.last_frame.copy()
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        inv = cv2.bitwise_not(gray)
        
        _, thresh = cv2.threshold(inv, 100, 255, cv2.THRESH_BINARY)
        
        noise = np.random.randint(0, 50, thresh.shape, dtype='uint8')
        final = cv2.add(thresh, noise)
        
        return Image.fromarray(final)

    def is_noisy(self):
        return self.noise_level > 50

    def trigger_mouse_chaos(self):
        try:
            x, y = pyautogui.position()
            pyautogui.moveTo(x + np.random.randint(-50, 50), y + np.random.randint(-50, 50))
        except:
            pass
