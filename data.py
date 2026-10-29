# data.py

DATA = {
    "База": {
        "color": "#7c9cf5", "icon": "📘", "desc": "Алфавит, числа, цвета, местоимения",
        "subsections": {
            "Алфавит": {"words": [
                {"en": "A a", "ipa": "eɪ", "ru": "эй", "say": "A"}, {"en": "B b", "ipa": "biː", "ru": "би", "say": "B"},
                {"en": "C c", "ipa": "siː", "ru": "си", "say": "C"}, {"en": "D d", "ipa": "diː", "ru": "ди", "say": "D"},
                {"en": "E e", "ipa": "iː", "ru": "и", "say": "E"}, {"en": "F f", "ipa": "ef", "ru": "эф", "say": "F"},
                {"en": "G g", "ipa": "dʒiː", "ru": "джи", "say": "G"}, {"en": "H h", "ipa": "eɪtʃ", "ru": "эйч", "say": "H"},
            ]},
            "Цвета": {"words": [
                {"en": "color / colour", "ipa": "ˈkʌl.ər", "ru": "цвет"}, {"en": "red", "ipa": "red", "ru": "красный"},
                {"en": "orange", "ipa": "ˈɒr.ɪndʒ", "ru": "оранжевый"}, {"en": "yellow", "ipa": "ˈjel.əʊ", "ru": "жёлтый"},
                {"en": "green", "ipa": "ɡriːn", "ru": "зелёный"}, {"en": "blue", "ipa": "bluː", "ru": "синий"},
            ]},
        },
    },
    "Словарный запас": {
        "color": "#e88fa8", "icon": "📚", "desc": "Семья, животные, еда",
        "subsections": {
            "Семья": {"words": [
                {"en": "mother", "ipa": "ˈmʌð.ər", "ru": "мама"}, {"en": "father", "ipa": "ˈfɑː.ðər", "ru": "папа"},
                {"en": "sister", "ipa": "ˈsɪs.tər", "ru": "сестра"}, {"en": "brother", "ipa": "ˈbrʌð.ər", "ru": "брат"},
            ]},
            "Животные": {"words": [
                {"en": "dog", "ipa": "dɒɡ", "ru": "собака"}, {"en": "cat", "ipa": "kæt", "ru": "кошка"},
                {"en": "horse", "ipa": "hɔːs", "ru": "лошадь"}, {"en": "cow", "ipa": "kaʊ", "ru": "корова"},
            ]},
        },
    },
}

def count_words(item):
    if "words" in item: return len(item["words"])
    if "subsections" in item: return sum(count_words(s) for s in item["subsections"].values())
    return 0

def collect_words(item, out=None):
    if out is None: out = []
    if "words" in item: out.extend(item["words"])
    if "subsections" in item:
        for s in item["subsections"].values(): collect_words(s, out)
    return out

def all_words_flat():
    out = []
    for item in DATA.values(): collect_words(item, out)
    return out
