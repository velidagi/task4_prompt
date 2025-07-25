import os
import google.generativeai as genai
from dotenv import load_dotenv
from tabulate import tabulate

# API anahtarını yükle
load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Sabit test metni
text = "Başta güzel gibiydi ama zamanla hayal kırıklığına dönüştü."

# PROMPT ŞABLONLARI
PROMPTS = {
    "metin_siniflandirma": {
        "zero_shot": 'Bu cümlenin duygusunu analiz et: "{text}"\nCevap sadece "Olumlu", "Olumsuz" veya "Nötr" olmalı.',
        "one_shot": '''Örnek:\n Cümle: "Bu ürünü çok beğendim!"\nDuygu: Olumlu\n\nŞimdi analiz et:\nCümle: "{text}"\nDuygu:''',
        "few_shot": '''Örnekler:\n Cümle: "Film çok kötüydü."\nDuygu: Olumsuz\nCümle: "Tatilde çok eğlendik."\nDuygu: Olumlu\n\nAnaliz et:\nCümle: "{text}"\nDuygu:''',
        "cot": '''Cümleyi analiz et: "{text}"\nÖnce duygusal kelimeleri bul, sonra bu ifadelerin tonunu değerlendir.\nSonuç: ''',
        "instructional": 'Aşağıdaki cümleye bakarak duygusal tonunu sınıflandır. Sadece "Olumlu", "Olumsuz" veya "Nötr".\nCümle: "{text}"'
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
    for format_adi, prompt_sablonu in PROMPTS["metin_siniflandirma"].items():
        filled_prompt = prompt_sablonu.format(text=text)
        yanit = ask_gemini(filled_prompt)
        results.append([format_adi, filled_prompt.strip(), yanit])

    print("\n📊 Test Sonuçları:")
    print(tabulate(results, headers=["Prompt Tipi", "Gönderilen Prompt", "Gemini Yanıtı"], tablefmt="fancy_grid", maxcolwidths=[12, 50, 50]))

# Kodun çalıştırıldığı yer
if __name__ == "__main__":
    test_all_prompts(text)
