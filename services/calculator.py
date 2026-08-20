"""
IELTS Band Score Calculator module according to official IDP IELTS standards.
"""
from data.ielts_knowledge import LISTENING_SCORES, READING_ACADEMIC_SCORES, READING_GENERAL_SCORES, CEFR_MAPPING

def get_listening_band(raw_score: int) -> float:
    raw_score = max(0, min(40, raw_score))
    for (low, high), band in LISTENING_SCORES.items():
        if low <= raw_score <= high:
            return band
    return 0.0

def get_academic_reading_band(raw_score: int) -> float:
    raw_score = max(0, min(40, raw_score))
    for (low, high), band in READING_ACADEMIC_SCORES.items():
        if low <= raw_score <= high:
            return band
    return 0.0

def get_general_reading_band(raw_score: int) -> float:
    raw_score = max(0, min(40, raw_score))
    for (low, high), band in READING_GENERAL_SCORES.items():
        if low <= raw_score <= high:
            return band
    return 0.0

def calculate_overall_band(listening: float, reading: float, writing: float, speaking: float) -> tuple[float, float]:
    """
    Calculates overall IELTS band with exact official IDP rounding.
    Returns (raw_average, final_overall_band).
    """
    avg = (listening + reading + writing + speaking) / 4.0
    int_part = int(avg)
    fraction = avg - int_part
    
    # Official IELTS rounding rule
    if fraction < 0.25:
        final_band = float(int_part)
    elif fraction < 0.75:
        final_band = float(int_part) + 0.5
    else:
        final_band = float(int_part) + 1.0
        
    return round(avg, 3), final_band

def get_band_feedback(band: float, lang: str = "uz") -> str:
    band_str = f"{band:.1f}"
    info = CEFR_MAPPING.get(band_str, {"cefr": "N/A", "level_uz": "Natija", "desc": ""})
    
    if lang == "uz":
        return f"🏆 *CEFR Darajasi:* `{info['cefr']}`\n📌 *Tavsif:* {info['desc']}"
    elif lang == "ru":
        return f"🏆 *Уровень CEFR:* `{info['cefr']}`\n📌 *Статус:* Соответствует международному уровню {info['cefr']}."
    else:
        return f"🏆 *CEFR Level:* `{info['cefr']}`\n📌 *Proficiency:* {info.get('level_uz', '')} (CEFR {info['cefr']})."
