import os
import google.generativeai as genai
from dotenv import load_dotenv
from tabulate import tabulate

# API anahtarını yükle
load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Sabit test metni
text = "Bilinmeyen bir adaya düşen çocuklar"

# PROMPT ŞABLONLARI
PROMPTS = {
    "yaratici_yazma": {
        "zero_shot": 'Aşağıdaki konuya göre yaratıcı bir hikaye başlat:\n"{text}"',
        "one_shot": '''Örnek:\nKonu: Uzayda yalnız kalan bir astronot\nHikaye: Sessizlik içinde süzülen gemide, astronot Ayla son sinyali Dünya’ya gönderdi...\n\nKonu: {text}\nHikaye:''',
        "few_shot": '''Aşağıda verilen konu başlıklarına göre kısa hikayeler yazılmıştır. Yeni bir konu için sen de benzer bir şekilde yaratıcı bir hikaye yaz. Örnek Konu: Kayıp bir köy hazinesi Hikaye: Efsanelere göre, köyün merkezinde gömülü bir kutu vardı. Yüzyıllardır kimse yerini bilmezdi. Ancak genç Elif’in bulduğu eski bir harita, köyün kaderini değiştirecekti...Örnek Konu: Zaman yolculuğu yapan bir kedi  Hikaye: Minnoş sıradan bir sokak kedisiydi. Ta ki eski bir saat kulesinin tepesine çıkıp zamanda kaybolana kadar. Şimdi Minnoş, geçmişi değiştirip geleceği kurtarmak zorunda...Konu: {text}  Hikaye:''',
        "cot": '''Önce karakteri, sonra mekanı, ardından olay örgüsünü kur.\nKonu: "{text}"\nAdım adım düşün ve bir hikaye oluştur.''',
        "instructional": 'Aşağıdaki konudan kısa bir yaratıcı giriş paragrafı oluştur.\nKonu: "{text}"'
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
    for format_adi, prompt_sablonu in PROMPTS["yaratici_yazma"].items():
        filled_prompt = prompt_sablonu.format(text=text)
        yanit = ask_gemini(filled_prompt)
        results.append([format_adi, filled_prompt.strip(), yanit])

    print("\n📊 Test Sonuçları:")
    print(tabulate(results, headers=["Prompt Tipi", "Gönderilen Prompt", "Gemini Yanıtı"], tablefmt="fancy_grid", maxcolwidths=[12, 50, 50]))

# Kodun çalıştırıldığı yer
if __name__ == "__main__":
    test_all_prompts(text)
