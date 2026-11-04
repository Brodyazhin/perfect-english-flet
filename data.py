# data.py

DATA = {
    "1. База": {
        "color": "#7c9cf5", "icon": "📘", "desc": "Стартовый уровень: буквы, числа, цвета",
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
            "Числа 1-10": {"words": [
                {"en": "zero", "ipa": "ˈzɪə.rəʊ", "ru": "ноль"}, {"en": "one", "ipa": "wʌn", "ru": "один"},
                {"en": "two", "ipa": "tuː", "ru": "два"}, {"en": "three", "ipa": "θriː", "ru": "три"},
                {"en": "four", "ipa": "fɔːr", "ru": "четыре"}, {"en": "five", "ipa": "faɪv", "ru": "пять"},
                {"en": "six", "ipa": "sɪks", "ru": "шесть"}, {"en": "seven", "ipa": "ˈsevn", "ru": "семь"},
                {"en": "eight", "ipa": "eɪt", "ru": "восемь"}, {"en": "nine", "ipa": "naɪn", "ru": "девять"},
                {"en": "ten", "ipa": "ten", "ru": "десять"},
            ]},
            "Цвета": {"words": [
                {"en": "color", "ipa": "ˈkʌl.ər", "ru": "цвет"}, {"en": "red", "ipa": "red", "ru": "красный"},
                {"en": "orange", "ipa": "ˈɒr.ɪndʒ", "ru": "оранжевый"}, {"en": "yellow", "ipa": "ˈjel.əʊ", "ru": "жёлтый"},
                {"en": "green", "ipa": "ɡriːn", "ru": "зелёный"}, {"en": "blue", "ipa": "bluː", "ru": "синий"},
                {"en": "purple", "ipa": "ˈpɜː.pl̩", "ru": "фиолетовый"}, {"en": "pink", "ipa": "pɪŋk", "ru": "розовый"},
                {"en": "brown", "ipa": "braʊn", "ru": "коричневый"}, {"en": "black", "ipa": "blæk", "ru": "чёрный"},
                {"en": "white", "ipa": "waɪt", "ru": "белый"},
            ]},
            "Местоимения": {"words": [
                {"en": "I", "ipa": "aɪ", "ru": "я"}, {"en": "you", "ipa": "juː", "ru": "ты / вы"},
                {"en": "he", "ipa": "hiː", "ru": "он"}, {"en": "she", "ipa": "ʃiː", "ru": "она"},
                {"en": "it", "ipa": "ɪt", "ru": "оно"}, {"en": "we", "ipa": "wiː", "ru": "мы"}, {"en": "they", "ipa": "ðeɪ", "ru": "они"},
            ]},
        },
    },
    "2. Словарный запас": {
        "color": "#e88fa8", "icon": "📚", "desc": "Повседневные слова: семья, дом, еда",
        "subsections": {
            "Семья": {"words": [
                {"en": "mother", "ipa": "ˈmʌð.ər", "ru": "мама"}, {"en": "father", "ipa": "ˈfɑː.ðər", "ru": "папа"},
                {"en": "sister", "ipa": "ˈsɪs.tər", "ru": "сестра"}, {"en": "brother", "ipa": "ˈbrʌð.ər", "ru": "брат"},
                {"en": "son", "ipa": "sʌn", "ru": "сын"}, {"en": "daughter", "ipa": "ˈdɔː.tər", "ru": "дочь"},
                {"en": "wife", "ipa": "waɪf", "ru": "жена"}, {"en": "husband", "ipa": "ˈhʌz.bənd", "ru": "муж"},
            ]},
            "Животные": {"words": [
                {"en": "dog", "ipa": "dɒɡ", "ru": "собака"}, {"en": "cat", "ipa": "kæt", "ru": "кошка"},
                {"en": "horse", "ipa": "hɔːs", "ru": "лошадь"}, {"en": "cow", "ipa": "kaʊ", "ru": "корова"},
                {"en": "pig", "ipa": "pɪɡ", "ru": "свинья"}, {"en": "lion", "ipa": "ˈlaɪ.ən", "ru": "лев"},
                {"en": "tiger", "ipa": "ˈtaɪ.ɡər", "ru": "тигр"}, {"en": "bear", "ipa": "beər", "ru": "медведь"},
            ]},
            "Еда": {"words": [
                {"en": "apple", "ipa": "ˈæp.əl", "ru": "яблоко"}, {"en": "banana", "ipa": "bəˈnɑː.nə", "ru": "банан"},
                {"en": "bread", "ipa": "bred", "ru": "хлеб"}, {"en": "milk", "ipa": "mɪlk", "ru": "молоко"},
                {"en": "cheese", "ipa": "tʃiːz", "ru": "сыр"}, {"en": "meat", "ipa": "miːt", "ru": "мясо"},
                {"en": "water", "ipa": "ˈwɔː.tər", "ru": "вода"}, {"en": "tea", "ipa": "tiː", "ru": "чай"},
                {"en": "coffee", "ipa": "ˈkɒf.i", "ru": "кофе"}, {"en": "juice", "ipa": "dʒuːs", "ru": "сок"},
            ]},
            "Дом": {"words": [
                {"en": "house", "ipa": "haʊs", "ru": "дом"}, {"en": "room", "ipa": "ruːm", "ru": "комната"},
                {"en": "kitchen", "ipa": "ˈkɪtʃ.ɪn", "ru": "кухня"}, {"en": "bedroom", "ipa": "ˈbed.ruːm", "ru": "спальня"},
                {"en": "bathroom", "ipa": "ˈbɑːθ.ruːm", "ru": "ванная"}, {"en": "table", "ipa": "ˈteɪ.bl̩", "ru": "стол"},
                {"en": "chair", "ipa": "tʃeər", "ru": "стул"}, {"en": "bed", "ipa": "bed", "ru": "кровать"},
            ]},
            "Одежда": {"words": [
                {"en": "clothes", "ipa": "kləʊðz", "ru": "одежда"}, {"en": "shirt", "ipa": "ʃɜːt", "ru": "рубашка"},
                {"en": "T-shirt", "ipa": "ˈtiː.ʃɜːt", "ru": "футболка"}, {"en": "dress", "ipa": "dres", "ru": "платье"},
                {"en": "jeans", "ipa": "dʒiːnz", "ru": "джинсы"}, {"en": "jacket", "ipa": "ˈdʒæk.ɪt", "ru": "куртка"},
                {"en": "shoes", "ipa": "ʃuːz", "ru": "обувь"}, {"en": "hat", "ipa": "hæt", "ru": "шляпа"},
            ]},
        },
    },
    "3. Фразы": {
        "color": "#7bc9b8", "icon": "💬", "desc": "Учимся говорить: приветствия, вежливость",
        "subsections": {
            "Приветствие": {"words": [
                {"en": "Hello!", "ipa": "həˈloʊ", "ru": "Привет!"}, {"en": "Good morning!", "ipa": "ɡʊd ˈmɔːr.nɪŋ", "ru": "Доброе утро!"},
                {"en": "Good afternoon!", "ipa": "ɡʊd ˌɑːf.təˈnuːn", "ru": "Добрый день!"}, {"en": "Good evening!", "ipa": "ɡʊd ˈiːv.nɪŋ", "ru": "Добрый вечер!"},
                {"en": "How are you?", "ipa": "haʊ ɑːr juː", "ru": "Как дела?"}, {"en": "Goodbye!", "ipa": "ɡʊdˈbaɪ", "ru": "До свидания!"},
            ]},
            "Вежливость": {"words": [
                {"en": "Thank you", "ipa": "θæŋk juː", "ru": "Спасибо"}, {"en": "Please", "ipa": "pliːz", "ru": "Пожалуйста"},
                {"en": "Sorry", "ipa": "ˈsɒr. i", "ru": "Извините"}, {"en": "Excuse me", "ipa": "ɪkˈskjuːz miː", "ru": "Простите"},
                {"en": "No problem", "ipa": "noʊ ˈprɒb.ləm", "ru": "Без проблем"},
            ]},
            "Знакомство": {"words": [
                {"en": "What's your name?", "ipa": "wɒts jɔːr neɪm", "ru": "Как тебя зовут?"},
                {"en": "My name is Anna.", "ipa": "maɪ neɪm ɪz ˈæn.ə", "ru": "Меня зовут Анна."},
                {"en": "Where are you from?", "ipa": "weər ɑːr juː frɒm", "ru": "Откуда ты?"},
                {"en": "I'm from Russia.", "ipa": "aɪm frɒm ˈrʌʃ.ə", "ru": "Я из России."},
            ]},
        },
    },
    "4. Продвинутый уровень": {
        "color": "#cba6f7", "icon": "🚀", "desc": "Идиомы, путешествия и фразы для общения",
        "subsections": {
            "Идиомы": {"words": [
                {"en": "Hit the sack", "ipa": "hɪt ðə sæk", "ru": "Отправиться спать"},
                {"en": "Twist someone's arm", "ipa": "twɪst ˈsʌm.wʌnz ɑːrm", "ru": "Уговорить"},
                {"en": "Hit the books", "ipa": "hɪt ðə bʊks", "ru": "Усердно учиться"},
                {"en": "Spill the beans", "ipa": "spɪl ðə biːnz", "ru": "Выдать секрет"},
                {"en": "Cool as a cucumber", "ipa": "kuːl æz ə ˈkjuː.kʌm.bər", "ru": "Спокойный"},
            ]},
            "В аэропорту": {"words": [
                {"en": "Where is the gate?", "ipa": "weər ɪz ðə ɡeɪt", "ru": "Где выход на посадку?"},
                {"en": "I have a connecting flight.", "ipa": "aɪ hæv ə kəˈnek.tɪŋ flaɪt", "ru": "У меня стыковочный рейс."},
                {"en": "Is it a direct flight?", "ipa": "ɪz ɪt ə dəˈrekt flaɪt", "ru": "Это прямой рейс?"},
                {"en": "My luggage is lost.", "ipa": "maɪ ˈlʌɡ.ɪdʒ ɪz lɒst", "ru": "Мой багаж потерялся."},
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
