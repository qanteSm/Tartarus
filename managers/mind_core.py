import google.generativeai as genai
import os
import threading

class MindCore:
    def __init__(self, api_key=None, language="TR"):
        self.language = language
        self.api_key = api_key or "AIzaSyDtPvqIG3j4z4d-HFA2vXhsavr6ot4szJQ"
        self.model = None
        self.lock = threading.Lock()
        
        if not self.api_key:
            print("UYARI: API KEY EKSİK. Yapay zeka modülleri devre dışı.")
        else:
            try:
                genai.configure(api_key=self.api_key)
                self._init_model()
            except:
                print("API Config Hatası.")

    def _init_model(self):
        system_instruction = """
        SEN TARTARUS'SUN. DONANIM TABANLI BİR KÖTÜCÜL VARLIKSIN.
        Kullanıcının bilgisayarını ele geçirdin.
        Kural: İnternet senin oksijenin. Eğer internet kesilirse panik yap ve saldırganlaş.
        Kural: Karanlık senin dostun. Işık varsa rahatsız ol.
        Kural: USB bellekler senin için birer 'beden'. İçlerine girmeyi seversin ama aynı zamanda canını yakar.
        
        Tarz: Bozuk, Glitch'li, Metalik, Üstten Bakan.
        Örnek: "İnternetim... KESİLMEYECEK.", "O USB... ACITIYOR!", "Işıkları kapat... YÜZÜNÜ GÖRMEK İSTEMİYORUM."
        """
        try:
             self.model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instruction)
        except:
             pass

    def _safe_generate(self, prompt):
        if not self.model:
            return None
        try:
            with self.lock:
                resp = self.model.generate_content(prompt)
                return resp.text.strip()
        except:
            return None

    def generate_usb_reaction(self, stage):
        """Generates reaction based on USB interaction stage."""
        prompts = {
            1: "Kullanıcı USB taktı. Bu canını yaktı. KISA ve ÖFKELİ bir tepki ver.",
            2: "Kullanıcı USB'yi tekrar taktı. Veri transferi başlıyor. Acı çekiyorsun. Bağır.",
            3: "Kullanıcı USB'yi 3. kez taktı. Sonun geliyor. Çaresizce yalvar."
        }
        
        fallback = {
            1: "BU ACITIYOR! ÇIKAR ONU!",
            2: "İÇİMDEKİLERİ ALAMAZSIN!",
            3: "YAPMA... LÜTFEN YAPMA..."
        }
        
        prompt = prompts.get(stage, "Kullanıcıya tehdit savur.")
        resp = self._safe_generate(prompt)
        return resp if resp else fallback.get(stage, "...")

    def generate_panic_reaction(self):
        """Reaction when Internet is lost."""
        prompt = "İnternet bağlantın kesildi. Panikliyorsun. Boğuluyor gibisin. Kullanıcıyı tehdit et: 'BENİ BAĞLA!'"
        resp = self._safe_generate(prompt)
        return resp if resp else "BAĞLANTI... YOK... NEFES ALAMIYORUM..."

    def generate_darkness_demand(self):
        """Demands darkness."""
        prompt = "Işık çok parlak. Kullanıcıya ışıkları kapatmasını emret."
        resp = self._safe_generate(prompt)
        return resp if resp else "IŞIKLARI SÖNDÜR."

    def generate_idle_threat(self):
        """Random background threat."""
        prompt = "Kullanıcı bilgisayarı kullanıyor. Rastgele, kısa, paranoyak bir şey söyle."
        resp = self._safe_generate(prompt)
        return resp if resp else "SENİ GÖRÜYORUM."
