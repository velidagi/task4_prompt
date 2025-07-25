import os
import google.generativeai as genai
from dotenv import load_dotenv
from tabulate import tabulate

# API anahtarını yükle
load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Sabit test metni
text = "Ahmet, Ankara'da Microsoft ile buluştu."

# PROMPT ŞABLONLARI
PROMPTS = {
    "bilgi_cikarma": {
        "zero_shot": 'Aşağıdaki cümleden kişi, yer ve organizasyon isimlerini çıkar:\n"{text}"',
        "one_shot": '''Örnek metin: "Ali İstanbul’da IBM ile toplantı yaptı."\nÇıkarılan Bilgiler: Kişi: Ali, Yer: İstanbul, Organizasyon: IBM\n\nŞimdi analiz et:\nMetin: "{text}"''',
        "few_shot": '''Metin: "Ayşe Ankara’da Google'da işe başladı."\nÇıkarılan: Kişi: Ayşe, Yer: Ankara, Organizasyon: Google\n\nMetin: "{text}"\nÇıkarılan:''',
        "cot": '''Cümleyi parçalara ayır ve özel isimleri tanımla.\nMetin: "{text}"\nAdım adım düşün ve en sonunda doğru formatta kişi, yer, kurumları belirt. Doğru format: Kişi: [Kişi Adı], Yer: [Yer Adı], Organizasyon: [Organizasyon Adı]''',
        "instructional": 'Aşağıdaki metindeki kişi, yer ve organizasyon isimlerini listele.\nMetin: "{text}"'
    }
}

def ask_gemini(prompt):
    model = genai.GenerativeModel('gemini-2.5-flash')
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"[HATA] {str(e)}"

def test_all_prompts(text):
    results = []
    for format_adi, prompt_sablonu in PROMPTS["bilgi_cikarma"].items():
        filled_prompt = prompt_sablonu.format(text=text)
        yanit = ask_gemini(filled_prompt)
        results.append([format_adi, filled_prompt.strip(), yanit])

    print("\n📊 Test Sonuçları:")
    print(tabulate(results, headers=["Prompt Tipi", "Gönderilen Prompt", "Gemini Yanıtı"], tablefmt="fancy_grid", maxcolwidths=[12, 50, 50]))

# Kodun çalıştırıldığı yer
if __name__ == "__main__":
    test_all_prompts(text)
