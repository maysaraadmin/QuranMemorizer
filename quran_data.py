import json
import os

# Define the directory for audio files
AUDIO_DIR = "audio/Qari1"

# Define qari styles with audio file paths
qari_styles = {
    "Qari1": {i: os.path.join(AUDIO_DIR, f"{i:03}.mp3") for i in range(1, 115)},
    # Add more Qaris here if needed
}

# Check if the Quran data file exists
quran_data_path = "quran_data/quran.json"
if not os.path.exists(quran_data_path):
    raise FileNotFoundError(f"The file {quran_data_path} does not exist.")

# Load Quran data
try:
    with open(quran_data_path, "r", encoding="utf-8") as file:
        _QURAN_DATA = json.load(file)
except json.JSONDecodeError as e:
    raise ValueError("Error decoding JSON file.") from e
except IOError as e:
    raise RuntimeError(f"Error opening or reading file: {e}")

# Define sura names
suras_names = [
    None,
    "الفاتحة",
    "البقرة",
    "آل عمران",
    "النساء",
    "المائدة",
    "الأنعام",
    "الأعراف",
    "الأنفال",
    "التوبة",
    "يونس",
    "هود",
    "يوسف",
    "الرعد",
    "ابراهيم",
    "الحجر",
    "النحل",
    "الإسراء",
    "الكهف",
    "مريم",
    "طه",
    "الأنبياء",
    "الحج",
    "المؤمنون",
    "النور",
    "الفرقان",
    "الشعراء",
    "النمل",
    "القصص",
    "العنكبوت",
    "الروم",
    "لقمان",
    "السجدة",
    "الأحزاب",
    "سبإ",
    "فاطر",
    "يس",
    "الصافات",
    "ص",
    "الزمر",
    "غافر",
    "فصلت",
    "الشورى",
    "الزخرف",
    "الدخان",
    "الجاثية",
    "الأحقاف",
    "محمد",
    "الفتح",
    "الحجرات",
    "ق",
    "الذاريات",
    "الطور",
    "النجم",
    "القمر",
    "الرحمن",
    "الواقعة",
    "الحديد",
    "المجادلة",
    "الحشر",
    "الممتحنة",
    "الصف",
    "الجمعة",
    "المنافقون",
    "التغابن",
    "الطلاق",
    "التحريم",
    "الملك",
    "القلم",
    "الحاقة",
    "المعارج",
    "نوح",
    "الجن",
    "المزمل",
    "المدثر",
    "القيامة",
    "الانسان",
    "المرسلات",
    "النبإ",
    "النازعات",
    "عبس",
    "التكوير",
    "الإنفطار",
    "المطففين",
    "الإنشقاق",
    "البروج",
    "الطارق",
    "الأعلى",
    "الغاشية",
    "الفجر",
    "البلد",
    "الشمس",
    "الليل",
    "الضحى",
    "الشرح",
    "التين",
    "العلق",
    "القدر",
    "البينة",
    "الزلزلة",
    "العاديات",
    "القارعة",
    "التكاثر",
    "العصر",
    "الهمزة",
    "الفيل",
    "قريش",
    "الماعون",
    "الكوثر",
    "الكافرون",
    "النصر",
    "المسد",
    "الإخلاص",
    "الفلق",
    "الناس",
]

# Dictionary for sura names with their corresponding numbers
suras_dict = {i: suras_names[i] for i in range(1, len(suras_names))}

# Ensure suras_names has 115 elements
if len(suras_names) != 115:
    raise AssertionError("suras_names should have 115 elements including the None placeholder at index 0")

def sura_exists(sura):
    return sura in suras_names[1:] or sura in suras_dict

def _get_sura_by_name(sura_name):
    for s in _QURAN_DATA:
        if s.get("name") == sura_name:
            return [aya.get("text") for aya in s.get("verses", [])]
    raise ValueError(f"Sura name '{sura_name}' not found.")

def _get_sura_by_num(sura_num):
    for s in _QURAN_DATA:
        if s.get("number") == sura_num:
            return [aya.get("text") for aya in s.get("verses", [])]
    raise ValueError(f"Sura number '{sura_num}' not found.")

def get_sura(sura):
    if isinstance(sura, str):
        return _get_sura_by_name(sura)
    elif isinstance(sura, int):
        return _get_sura_by_num(sura)
    else:
        raise TypeError("Sura must be a string or integer.")

# Sample usage for testing
if __name__ == "__main__":
    # Test getting a sura by name
    sura_name = "الفاتحة"
    if sura_exists(sura_name):
        print(f"Sura '{sura_name}' exists.")
        print(get_sura(sura_name))
    else:
        print(f"Sura '{sura_name}' does not exist.")

    # Test getting a sura by number
    sura_num = 2
    if sura_exists(sura_num):
        print(f"Sura number '{sura_num}' exists.")
        print(get_sura(sura_num))
    else:
        print(f"Sura number '{sura_num}' does not exist.")