# === app.py ===
from flask import Flask, render_template, request
import google.generativeai as genai

app = Flask(__name__)

# Konfigurasi API Gemini
GEMINI_API_KEY = "AIzaSyAJD7eddtLwji6ZrXHLdAX_tws7tmJGb3Q"  # Ganti dengan API key kamu
genai.configure(api_key=GEMINI_API_KEY)

# Indeks DASS
DEPRESSION_IDX = [3, 5, 10, 13, 16, 17, 24, 26, 30, 31, 34, 36, 38, 42]
ANXIETY_IDX =    [2, 4, 7, 9, 15, 19, 20, 23, 25, 28, 33, 35, 39, 41]
STRESS_IDX =     [1, 6, 8, 11, 12, 14, 18, 21, 22, 27, 29, 32, 37, 40]

# Pertanyaan DASS-42
QUESTIONS = [
    "Menjadi marah karena hal-hal kecil/sepele",
    "Mulut terasa kering",
    "Tidak dapat melihat hal yang positif dari suatu kejadian",
    "Merasakan gangguan dalam bernapas (napas cepat, sulit bernapas)",
    "Merasa sepertinya tidak kuat lagi untuk melakukan suatu kegiatan",
    "Cenderung bereaksi berlebihan pada situasi",
    "Kelemahan pada anggota tubuh",
    "Kesulitan untuk relaksasi/bersantai",
    "Cemas yang berlebihan dalam suatu situasi namun bisa lega jika hal/situasi itu berakhir",
    "Pesimis",
    "Mudah merasa kesal",
    "Merasa banyak menghabiskan energi karena cemas",
    "Merasa sedih dan depresi",
    "Tidak sabaran",
    "Kelelahan",
    "Kehilangan minat pada banyak hal (misal: makan, ambulasi, sosialisasi)",
    "Merasa diri tidak layak",
    "Mudah tersinggung",
    "Berkeringat tanpa stimulasi oleh cuaca maupun latihan fisik",
    "Ketakutan tanpa alasan yang jelas",
    "Merasa hidup tidak berharga",
    "Sulit untuk beristirahat",
    "Kesulitan dalam menelan",
    "Tidak dapat menikmati hal-hal yang saya lakukan",
    "Perubahan kegiatan jantung dan denyut nadi tanpa stimulasi oleh latihan fisik",
    "Merasa hilang harapan dan putus asa",
    "Mudah marah",
    "Mudah panik",
    "Kesulitan untuk tenang setelah sesuatu yang mengganggu",
    "Takut diri terhambat oleh tugas-tugas yang tidak biasa dilakukan",
    "Sulit untuk antusias pada banyak hal",
    "Sulit mentoleransi gangguan-gangguan terhadap hal yang sedang dilakukan",
    "Berada pada keadaan tegang",
    "Merasa tidak berharga",
    "Tidak dapat memaklumi hal apapun yang menghalangi Anda untuk menyelesaikan hal yang sedang Anda lakukan",
    "Ketakutan",
    "Tidak ada harapan untuk masa depan",
    "Merasa hidup tidak berarti",
    "Mudah gelisah",
    "Khawatir dengan situasi saat diri Anda mungkin menjadi panik dan mempermalukan diri sendiri",
    "Gemetar",
    "Sulit untuk meningkatkan inisiatif dalam melakukan sesuatu"
]

def get_category(score):
    if score <= 35:
        return "Normal"
    elif score <= 40:
        return "Ringan"
    elif score <= 65:
        return "Sedang"
    elif score <= 80:
        return "Berat"
    else:
        return "Berat Sekali"

def ai_suggestion(categories):
    prompt = f"""
Buatkan saran coping singkat dalam bentuk satu paragraf yang cocok untuk remaja Gen Z berdasarkan hasil tes DASS-42 berikut:
- Depresi: {categories['Depresi'][1]} (Skor: {categories['Depresi'][0]})
- Kecemasan: {categories['Kecemasan'][1]} (Skor: {categories['Kecemasan'][0]})
- Stres: {categories['Stress'][1]} (Skor: {categories['Stress'][0]})

Syarat:
- Gunakan bahasa yang santai, simple, dan cocok untuk Gen Z
- Sertakan emoji yang sesuai (boleh 5–8 emoji)
- Panjang maksimal 5–7 kalimat saja
- Hindari bullet point, langsung jadikan 1 paragraf
- Tutup dengan kalimat motivasi di akhir yang singkat dan semangat
"""

    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()


@app.route('/')
def home():
    return render_template('index.html', questions=QUESTIONS)

@app.route('/submit', methods=['POST'])
def submit():
    responses = [int(request.form.get(f'q{i}')) for i in range(1, 43)]

    dep_score = sum([responses[i - 1] for i in DEPRESSION_IDX])
    anx_score = sum([responses[i - 1] for i in ANXIETY_IDX])
    str_score = sum([responses[i - 1] for i in STRESS_IDX])

    categories = {
        'Depresi': (dep_score, get_category(dep_score)),
        'Kecemasan': (anx_score, get_category(anx_score)),
        'Stress': (str_score, get_category(str_score))
    }

    suggestion = ai_suggestion(categories)

    return render_template('result.html', categories=categories, suggestion=suggestion)

if __name__ == '__main__':
    app.run(debug=True)
