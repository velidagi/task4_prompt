import os
import google.generativeai as genai
from dotenv import load_dotenv

# .env dosyasından çevre değişkenlerini yükle
load_dotenv()

def test_gemini_api():
    try:
        # API anahtarını çevre değişkeninden al
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            print("HATA: GOOGLE_API_KEY çevre değişkeni bulunamadı!")
            return
        
        # Gemini API'yi yapılandır
        genai.configure(api_key=api_key)
        
        # Ücretsiz model kullan (gemini-1.5-flash)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Test mesajı
        prompt = "Merhaba! Bu bir API test mesajıdır. Kısa bir yanıt ver."
        
        print("Gemini API'ye bağlanılıyor...")
        print(f"Prompt: {prompt}")
        print("-" * 50)
        
        # API çağrısı yap
        response = model.generate_content(prompt)
        
        # Yanıtı yazdır
        print("API Yanıtı:")
        print(response.text)
        print("-" * 50)
        print("✅ Test başarılı!")
        
    except Exception as e:
        print(f"Hata oluştu: {str(e)}")




if __name__ == "__main__":
    test_gemini_api()