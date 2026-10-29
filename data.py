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
                {"en": "I i", "ipa": "aɪ", "ru": "ай", "say": "I"}, {"en": "J j", "ipa": "dʒeɪ", "ru": "джей", "say": "J"},
                {"en": "K k", "ipa": "keɪ", "ru": "кей", "say": "K"}, {"en": "L l", "ipa": "el", "ru": "эл", "say": "L"},
                {"en": "M m", "ipa": "em", "ru": "эм", "say": "M"}, {"en": "N n", "ipa": "en", "ru": "эн", "say": "N"},
                {"en": "O o", "ipa": "oʊ", "ru": "оу", "say": "O"}, {"en": "P p", "ipa": "piː", "ru": "пи", "say": "P"},
                {"en": "Q q", "ipa": "kjuː", "ru": "кью", "say": "Q"}, {"en": "R r", "ipa": "ɑːr", "ru": "ар", "say": "R"},
                {"en": "S s", "ipa": "es", "ru": "эс", "say": "S"}, {"en": "T t", "ipa": "tiː", "ru": "ти", "say": "T"},
                {"en": "U u", "ipa": "juː", "ru": "ю", "say": "U"}, {"en": "V v", "ipa": "viː", "ru": "ви", "say": "V"},
                {"en": "W w", "ipa": "ˈdʌb.əl.juː", "ru": "дабл-ю", "say": "W"}, {"en": "X x", "ipa": "eks", "ru": "экс", "say": "X"},
                {"en": "Y y", "ipa": "waɪ", "ru": "уай", "say": "Y"}, {"en": "Z z", "ipa": "zed / ziː", "ru": "зэд / зи", "say": "Z"},
            ]},
            "Числа": {"subsections": {
                "0 — 10": {"words": [
                    {"en": "zero", "ipa": "ˈzɪə.rəʊ", "ru": "ноль"}, {"en": "one", "ipa": "wʌn", "ru": "один"},
                    {"en": "two", "ipa": "tuː", "ru": "два"}, {"en": "three", "ipa": "θriː", "ru": "три"},
                    {"en": "four", "ipa": "fɔːr", "ru": "четыре"}, {"en": "five", "ipa": "faɪv", "ru": "пять"},
                    {"en": "six", "ipa": "sɪks", "ru": "шесть"}, {"en": "seven", "ipa": "ˈsevn", "ru": "семь"},
                    {"en": "eight", "ipa": "eɪt", "ru": "восемь"}, {"en": "nine", "ipa": "naɪn", "ru": "девять"},
                    {"en": "ten", "ipa": "ten", "ru": "десять"},
                ]},
                "11 — 20": {"words": [
                    {"en": "eleven", "ipa": "ɪˈlevn", "ru": "одиннадцать"}, {"en": "twelve", "ipa": "twelv", "ru": "двенадцать"},
                    {"en": "thirteen", "ipa": "ˌθɜːˈtiːn", "ru": "тринадцать"}, {"en": "fourteen", "ipa": "ˌfɔːˈtiːn", "ru": "четырнадцать"},
                    {"en": "fifteen", "ipa": "ˌfɪfˈtiːn", "ru": "пятнадцать"}, {"en": "sixteen", "ipa": "ˌsɪksˈtiːn", "ru": "шестнадцать"},
                    {"en": "seventeen", "ipa": "ˌsevnˈtiːn", "ru": "семнадцать"}, {"en": "eighteen", "ipa": "ˌeɪˈtiːn", "ru": "восемнадцать"},
                    {"en": "nineteen", "ipa": "ˌnaɪnˈtiːn", "ru": "девятнадцать"}, {"en": "twenty", "ipa": "ˈtwen.ti", "ru": "двадцать"},
                ]},
                "Десятки": {"words": [
                    {"en": "thirty", "ipa": "ˈθɜː.ti", "ru": "тридцать"}, {"en": "forty", "ipa": "ˈfɔː.ti", "ru": "сорок"},
                    {"en": "fifty", "ipa": "ˈfɪf.ti", "ru": "пятьдесят"}, {"en": "sixty", "ipa": "ˈsɪks.ti", "ru": "шестьдесят"},
                    {"en": "seventy", "ipa": "ˈsev.n.ti", "ru": "семьдесят"}, {"en": "eighty", "ipa": "ˈeɪ.ti", "ru": "восемьдесят"},
                    {"en": "ninety", "ipa": "ˈnaɪn.ti", "ru": "девяносто"},
                ]},
                "Большие числа": {"words": [
                    {"en": "hundred", "ipa": "ˈhʌn.drəd", "ru": "сто"}, {"en": "thousand", "ipa": "ˈθaʊ.znd", "ru": "тысяча"},
                    {"en": "million", "ipa": "ˈmɪl.jən", "ru": "миллион"}, {"en": "billion", "ipa": "ˈbɪl.jən", "ru": "миллиард"},
                ]},
                "Порядковые": {"words": [
                    {"en": "first", "ipa": "fɜːst", "ru": "первый"}, {"en": "second", "ipa": "ˈsek.ənd", "ru": "второй"},
                    {"en": "third", "ipa": "θɜːd", "ru": "третий"}, {"en": "fourth", "ipa": "fɔːθ", "ru": "четвёртый"},
                    {"en": "fifth", "ipa": "fɪfθ", "ru": "пятый"}, {"en": "sixth", "ipa": "sɪksθ", "ru": "шестой"},
                    {"en": "seventh", "ipa": "ˈsev.nθ", "ru": "седьмой"}, {"en": "eighth", "ipa": "eɪtθ", "ru": "восьмой"},
                    {"en": "ninth", "ipa": "naɪnθ", "ru": "девятый"}, {"en": "tenth", "ipa": "tenθ", "ru": "десятый"},
                ]},
            }},
            "Цвета": {"words": [
                {"en": "color / colour", "ipa": "ˈkʌl.ər", "ru": "цвет"}, {"en": "red", "ipa": "red", "ru": "красный"},
                {"en": "orange", "ipa": "ˈɒr.ɪndʒ", "ru": "оранжевый"}, {"en": "yellow", "ipa": "ˈjel.əʊ", "ru": "жёлтый"},
                {"en": "green", "ipa": "ɡriːn", "ru": "зелёный"}, {"en": "blue", "ipa": "bluː", "ru": "синий"},
                {"en": "purple", "ipa": "ˈpɜː.pl̩", "ru": "фиолетовый"}, {"en": "pink", "ipa": "pɪŋk", "ru": "розовый"},
                {"en": "brown", "ipa": "braʊn", "ru": "коричневый"}, {"en": "black", "ipa": "blæk", "ru": "чёрный"},
                {"en": "white", "ipa": "waɪt", "ru": "белый"}, {"en": "grey / gray", "ipa": "ɡreɪ", "ru": "серый"},
            ]},
            "Местоимения": {"subsections": {
                "Личные": {"words": [
                    {"en": "I", "ipa": "aɪ", "ru": "я"}, {"en": "you", "ipa": "juː", "ru": "ты / вы"},
                    {"en": "he", "ipa": "hiː", "ru": "он"}, {"en": "she", "ipa": "ʃiː", "ru": "она"},
                    {"en": "it", "ipa": "ɪt", "ru": "оно"}, {"en": "we", "ipa": "wiː", "ru": "мы"}, {"en": "they", "ipa": "ðeɪ", "ru": "они"},
                ]},
                "Объектные": {"words": [
                    {"en": "me", "ipa": "miː", "ru": "мне / меня"}, {"en": "you", "ipa": "juː", "ru": "тебе / тебя"},
                    {"en": "him", "ipa": "hɪm", "ru": "ему / его"}, {"en": "her", "ipa": "hɜːr", "ru": "ей / её"},
                    {"en": "it", "ipa": "ɪt", "ru": "ему / его"}, {"en": "us", "ipa": "ʌs", "ru": "нам / нас"},
                    {"en": "them", "ipa": "ðem", "ru": "им / их"},
                ]},
            }},
        },
    },
    "Словарный запас": {
        "color": "#e88fa8", "icon": "📚", "desc": "Семья, профессии, животные, еда, дом",
        "subsections": {
            "Семья": {"words": [
                {"en": "mother", "ipa": "ˈmʌð.ər", "ru": "мама"}, {"en": "father", "ipa": "ˈfɑː.ðər", "ru": "папа"},
                {"en": "sister", "ipa": "ˈsɪs.tər", "ru": "сестра"}, {"en": "brother", "ipa": "ˈbrʌð.ər", "ru": "брат"},
                {"en": "son", "ipa": "sʌn", "ru": "сын"}, {"en": "daughter", "ipa": "ˈdɔː.tər", "ru": "дочь"},
                {"en": "wife", "ipa": "waɪf", "ru": "жена"}, {"en": "husband", "ipa": "ˈhʌz.bənd", "ru": "муж"},
                {"en": "grandmother", "ipa": "ˈɡræn.mʌð.ər", "ru": "бабушка"}, {"en": "grandfather", "ipa": "ˈɡræn.fɑː.ðər", "ru": "дедушка"},
            ]},
            "Животные": {"words": [
                {"en": "dog", "ipa": "dɒɡ", "ru": "собака"}, {"en": "cat", "ipa": "kæt", "ru": "кошка"},
                {"en": "horse", "ipa": "hɔːs", "ru": "лошадь"}, {"en": "cow", "ipa": "kaʊ", "ru": "корова"},
                {"en": "pig", "ipa": "pɪɡ", "ru": "свинья"}, {"en": "chicken", "ipa": "ˈtʃɪk.ɪn", "ru": "курица"},
                {"en": "lion", "ipa": "ˈlaɪ.ən", "ru": "лев"}, {"en": "tiger", "ipa": "ˈtaɪ.ɡər", "ru": "тигр"},
                {"en": "bear", "ipa": "beər", "ru": "медведь"}, {"en": "wolf", "ipa": "wʊlf", "ru": "волк"},
            ]},
            "Еда": {"words": [
                {"en": "apple", "ipa": "ˈæp.əl", "ru": "яблоко"}, {"en": "banana", "ipa": "bəˈnɑː.nə", "ru": "банан"},
                {"en": "bread", "ipa": "bred", "ru": "хлеб"}, {"en": "milk", "ipa": "mɪlk", "ru": "молоко"},
                {"en": "cheese", "ipa": "tʃiːz", "ru": "сыр"}, {"en": "meat", "ipa": "miːt", "ru": "мясо"},
                {"en": "water", "ipa": "ˈwɔː.tər", "ru": "вода"}, {"en": "tea", "ipa": "tiː", "ru": "чай"},
                {"en": "coffee", "ipa": "ˈkɒf.i", "ru": "кофе"}, {"en": "juice", "ipa": "dʒuːs", "ru": "сок"},
            ]},
        },
    },
    "Фразы": {
        "color": "#7bc9b8", "icon": "💬", "desc": "Готовые фразы",
        "subsections": {
            "Приветствие": {"words": [
                {"en": "Hello!", "ipa": "həˈloʊ", "ru": "Привет!"}, {"en": "Good morning!", "ipa": "ɡʊd ˈmɔːr.nɪŋ", "ru": "Доброе утро!"},
                {"en": "Good evening!", "ipa": "ɡʊd ˈiːv.nɪŋ", "ru": "Добрый вечер!"}, {"en": "How are you?", "ipa": "haʊ ɑːr juː", "ru": "Как дела?"},
                {"en": "Goodbye!", "ipa": "ɡʊdˈbaɪ", "ru": "До свидания!"},
            ]},
            "Вежливость": {"words": [
                {"en": "Thank you", "ipa": "θæŋk juː", "ru": "Спасибо"}, {"en": "Please", "ipa": "pliːz", "ru": "Пожалуйста"},
                {"en": "Sorry", "ipa": "ˈsɒr.i", "ru": "Извините"}, {"en": "Excuse me", "ipa": "ɪkˈskjuːz miː", "ru": "Простите"},
                {"en": "No problem", "ipa": "noʊ ˈprɒb.ləm", "ru": "Без проблем"},
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
