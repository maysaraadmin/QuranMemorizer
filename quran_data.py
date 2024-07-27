import json
import os

AUDIO_DIR = "audio/Qari1"

qari_styles = {
    "Qari1": {i: f"audio/Qari1/{i:03}.mp3" for i in range(1, 115)},
    # Add more Qaris...
}

# Check if the file exists before loading
quran_data_path = "quran_data/quran.json"
if not os.path.exists(quran_data_path):
    raise FileNotFoundError(f"The file {quran_data_path} does not exist.")

with open(quran_data_path, "r", encoding="utf-8") as file:
    try:
        _QURAN_DATA = json.load(file)
    except json.JSONDecodeError as e:
        raise ValueError("Error decoding JSON file.") from e

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

suras_dict = {i: suras_names[i] for i in range(1, len(suras_names))}

assert (
    len(suras_names) == 115
), "suras_names should have 115 elements including the None placeholder at index 0"


def sura_exist(sura):
    """Check if the sura name or sura number exists."""
    return sura in suras_names[1:] or sura in suras_dict


def _get_sura_by_name(sura_name):
    """Get sura by name."""
    for s in _QURAN_DATA:
        if s["name"] == sura_name:
            return [aya["text"] for aya in s["verses"]]
    raise ValueError(f"Sura name '{sura_name}' not found.")


def _get_sura_by_num(sura_num):
    """Get sura by number."""
    for s in _QURAN_DATA:
        if s["number"] == sura_num:
            return [aya["text"] for aya in s["verses"]]
    raise ValueError(f"Sura number '{sura_num}' not found.")


def get_sura(sura):
    """Get sura by name or number."""
    if isinstance(sura, str):
        return _get_sura_by_name(sura)
    elif isinstance(sura, int):
        return _get_sura_by_num(sura)
    else:
        raise TypeError("Sura must be a string or integer.")
