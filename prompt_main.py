from tabulate import tabulate
import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Ortam değişkenlerini yükle ve Gemini API yapılandır
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# 2. Görev bazlı prompt sözlüğü
PROMPTS = {
    "metin_siniflandirma": {
        "zero_shot": 'Bu cümlenin duygusunu analiz et: "{text}"\nCevap sadece "Olumlu", "Olumsuz" veya "Nötr" olmalı.',
        "one_shot": '''Örnek:\nCümle: "Bu ürünü çok beğendim!"\nDuygu: Olumlu\n\nŞimdi analiz et:\nCümle: "{text}"\nDuygu:''',
        "few_shot": '''Örnekler:\nCümle: "Film çok kötüydü."\nDuygu: Olumsuz\nCümle: "Tatilde çok eğlendik."\nDuygu: Olumlu\n\nAnaliz et:\nCümle: "{text}"\nDuygu:''',
        "cot": '''Cümleyi analiz et: "{text}"\nÖnce duygusal kelimeleri bul, sonra bu ifadelerin tonunu değerlendir.\nSonuç: ''',
        "instructional": 'Aşağıdaki cümleye bakarak duygusal tonunu sınıflandır. Sadece "Olumlu", "Olumsuz" veya "Nötr".\nCümle: "{text}"'
    },
    "bilgi_cikarma": {
        "zero_shot": 'Aşağıdaki cümleden kişi, yer ve organizasyon isimlerini çıkar:\n"{text}"',
        "one_shot": '''Örnek:\nMetin: "Ali İstanbul’da IBM ile toplantı yaptı."\nÇıkarılan Bilgiler: Kişi: Ali, Yer: İstanbul, Organizasyon: IBM\n\nŞimdi analiz et:\nMetin: "{text}"''',
        "few_shot": '''Metin: "Ayşe Ankara’da Google'da işe başladı."\nÇıkarılan: Kişi: Ayşe, Yer: Ankara, Organizasyon: Google\n\nMetin: "{text}"\nÇıkarılan:''',
        "cot": '''Cümleyi parçalara ayır ve özel isimleri tanımla.\nMetin: "{text}"\nAdım adım düşün ve kişi, yer, kurumları belirt.''',
        "instructional": 'Aşağıdaki metindeki kişi, yer ve organizasyon isimlerini listele.\nMetin: "{text}"'
    },
    "yaratici_yazma": {
        "zero_shot": 'Aşağıdaki konuya göre yaratıcı bir hikaye başlat:\n"{text}"',
        "one_shot": '''Örnek:\nKonu: Uzayda yalnız kalan bir astronot\nHikaye: Sessizlik içinde süzülen gemide, astronot Ayla son sinyali Dünya’ya gönderdi...\n\nKonu: {text}\nHikaye:''',
        "few_shot": '''Konu: Kayıp bir köy hazinesi\nHikaye: Efsanelere göre, köyün merkezinde gömülü bir kutu vardı...\n\nKonu: {text}\nHikaye:''',
        "cot": '''Önce karakteri, sonra mekanı, ardından olay örgüsünü kur.\nKonu: "{text}"\nAdım adım düşün ve bir hikaye oluştur.''',
        "instructional": 'Aşağıdaki konudan kısa bir yaratıcı giriş paragrafı oluştur.\nKonu: "{text}"'
    }
}

# 3. Gemini'den içerik istemek için fonksiyon
def ask_gemini(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

# 4. Prompt hazırlayıcı
def build_prompt(gorev, format, text):
    template = PROMPTS[gorev][format]
    return template.format(text=text)

# 5. Test etme fonksiyonu
def test_all_formats_for_task(gorev, text):
    print(f"\n🎯 Görev: {gorev.upper()} | Girdi: {text}")
    for format in PROMPTS[gorev]:
        prompt = build_prompt(gorev, format, text)
        print(f"\n🧪 Format: {format}")
        print(f"📤 Prompt:\n{prompt}\n")
        result = ask_gemini(prompt)
        print(f"📥 Yanıt:\n{result}\n{'-'*50}")

# 🔍 Test: Metin Sınıflandırma Görevi
if __name__ == "__main__":
    # Örnek girişleri değiştirerek diğer görevleri de test edebilirsin
    test_all_formats_for_task("metin_siniflandirma", "Bugün gerçekten çok kötü geçti.")
    test_all_formats_for_task("bilgi_cikarma", "Ahmet, Ankara'da Microsoft ile buluştu.")
    test_all_formats_for_task("yaratici_yazma", "Bilinmeyen bir adaya düşen çocuklar")

def test_all_formats_for_task(gorev, text):
    results = []
    for format in PROMPTS[gorev]:
        prompt = build_prompt(gorev, format, text)
        response = ask_gemini(prompt)
        results.append([format, prompt.strip(), response.strip()])
    
    print(f"\n🎯 Görev: {gorev.upper()} | Girdi: {text}")
    print(tabulate(results, headers=["Format", "Prompt", "Yanıt"], tablefmt="fancy_grid", maxcolwidths=[12, 60, 60]))
