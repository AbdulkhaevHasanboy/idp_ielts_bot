from locales.uz import STRINGS as UZ_STRINGS
from locales.ru import STRINGS as RU_STRINGS
from locales.en import STRINGS as EN_STRINGS

LOCALES = {
    "uz": UZ_STRINGS,
    "ru": RU_STRINGS,
    "en": EN_STRINGS
}

def t(key: str, lang: str = "uz", **kwargs) -> str:
    strings = LOCALES.get(lang, UZ_STRINGS)
    text = strings.get(key, UZ_STRINGS.get(key, key))
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text
