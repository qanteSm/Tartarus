import tkinter as tk
from tkinter import font
import random
import platform
from PIL import Image, ImageTk

class DisplayManager:
    def __init__(self, root, audio_manager):
        self.root = root
        self.audio = audio_manager
        
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        
        self.os_type = platform.system()

        # Ghost Overlay Setup
        self.root.overrideredirect(True)
        self.root.geometry(f"{self.width}x{self.height}+0+0")
        self.root.configure(bg='black')
        self.root.attributes('-topmost', True)

        # Transparent Window Trick (Windows only)
        if self.os_type == "Windows":
             try:
                 self.root.wm_attributes("-transparentcolor", "black")
                 self.root.wm_attributes("-alpha", 0.01) # Nearly invisible interaction layer
             except:
                 pass
        else:
             # Linux fallback: just minimize or keep hidden until needed
             self.root.attributes('-alpha', 0.0)

        self.root.protocol("WM_DELETE_WINDOW", lambda: None)
        
        self.overlay_windows = []

    def ask_language(self):
        # In Ghost Mode, we skip the language prompt or use a simple popup
        # For now, defaulting to TR as per the "Ritual" context being Turkish
        # Or we can just use a simple popup
        return "TR"

    def show_ghost_message(self, text, duration=3000, color="red", font_size=20):
        """Displays floating text on the screen without a window border."""
        try:
            top = tk.Toplevel(self.root)
            top.overrideredirect(True)
            top.attributes('-topmost', True)
            
            # Position randomly or center
            x = random.randint(100, self.width - 400)
            y = random.randint(100, self.height - 200)
            top.geometry(f"+{x}+{y}")
            
            if self.os_type == "Windows":
                top.wm_attributes("-transparentcolor", "black")
            
            lbl = tk.Label(top, text=text, font=("Arial", font_size, "bold"), fg=color, bg="black")
            lbl.pack()
            
            self.overlay_windows.append(top)
            
            def fade_out():
                top.destroy()
                if top in self.overlay_windows:
                    self.overlay_windows.remove(top)
                    
            self.root.after(duration, fade_out)
        except Exception as e:
            print(f"Ghost Text Error: {e}")

    def trigger_flashbang(self):
        """Fills the screen with white light."""
        top = tk.Toplevel(self.root)
        top.attributes('-fullscreen', True)
        top.attributes('-topmost', True)
        top.configure(bg="white")
        
        self.root.after(2000, top.destroy)

    def glitch_screen(self, duration=500):
        """Simulates screen glitching by flashing colors."""
        pass # In overlay mode, this is harder, maybe flash overlay windows

    def clear(self):
        for win in self.overlay_windows:
            try:
                win.destroy()
            except:
                pass
        self.overlay_windows = []
    
    def keep_focus(self):
        self.root.after(1000, self.keep_focus)
