import json
import os

# Example paths, replace with your actual paths or URLs
AUDIO_DIR = "audio/Qari1"

qari_styles = {
    "Qari1": {
        i: os.path.join(AUDIO_DIR, "Qari1", f"{str(i).zfill(3)}.mp3")
        for i in range(1, 115)
    },
    # Add more Qaris as needed
}
# LOAD DATA
with open("quran.json", "r", encoding="utf-8") as file:
    _QURAN_DATA = json.load(file)

# GLOBAL VARS
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

# Ensure the length is correct
assert (
    len(suras_names) == 115
), "suras_names should have 115 elements including the None placeholder at index 0"


# FUNCTIONS TO HANDLE SURAS AND AYAS
def sura_exist(sura):
    """CHECK FOR SURA NAME OR SURA NUMBER"""
    return sura in suras_names[1:] or sura in suras_dict


def _get_sura_by_name(sura_name):
    for s in _QURAN_DATA:
        if s["name"] == sura_name:
            return [aya["text"] for aya in s["verses"]]


def _get_sura_by_number(sura_number):
    sura_name = suras_dict[sura_number]
    return _get_sura_by_name(sura_name)


def get_sura(sura_name_or_number):
    """GET SURA BY NAME OR BY NUMBER"""
    if sura_exist(sura_name_or_number):
        if isinstance(sura_name_or_number, str):
            return _get_sura_by_name(sura_name_or_number)
        elif isinstance(sura_name_or_number, int):
            return _get_sura_by_number(sura_name_or_number)
    else:
        return ["لم تقم بتحديد السورة"]


def get_sura_info(sura_name_or_number):
    """GET SURA INFO BY NAME OR BY NUMBER"""
    if sura_exist(sura_name_or_number):
        if isinstance(sura_name_or_number, str):
            return _get_sura_info_by_name(sura_name_or_number)
        elif isinstance(sura_name_or_number, int):
            return _get_sura_info_by_number(sura_name_or_number)
    else:
        print("sura not exist")
        return None


def _get_sura_info_by_name(sura_name):
    info = []
    for s in _QURAN_DATA:
        if s["name"] == sura_name:
            for key in s:
                if key != "verses":
                    info.append((key, s[key]))
    return info


def _get_sura_info_by_number(sura_number):
    sura_name = suras_dict[sura_number]
    return _get_sura_info_by_name(sura_name)


def get_sura_number(sura):
    for key, value in suras_dict.items():
        if sura == value:
            return key


def get_sura_from_aya(aya):
    for sura in suras_names[1:]:
        s = get_sura(sura)
        if aya in s:
            return sura
    return None
