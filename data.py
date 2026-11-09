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
            "Числа": {"words": [
                {"en": "zero", "ipa": "ˈzɪə.rəʊ", "ru": "ноль"}, {"en": "one", "ipa": "wʌn", "ru": "один"},
                {"en": "two", "ipa": "tuː", "ru": "два"}, {"en": "three", "ipa": "θriː", "ru": "три"},
                {"en": "four", "ipa": "fɔːr", "ru": "четыре"}, {"en": "five", "ipa": "faɪv", "ru": "пять"},
                {"en": "six", "ipa": "sɪks", "ru": "шесть"}, {"en": "seven", "ipa": "ˈsevn", "ru": "семь"},
                {"en": "eight", "ipa": "eɪt", "ru": "восемь"}, {"en": "nine", "ipa": "naɪn", "ru": "девять"},
                {"en": "ten", "ipa": "ten", "ru": "десять"},
            ]},
            "Цвета": {"words": [
                {"en": "red", "ipa": "red", "ru": "красный"}, {"en": "orange", "ipa": "ˈɒr.ɪndʒ", "ru": "оранжевый"},
                {"en": "yellow", "ipa": "ˈjel.əʊ", "ru": "жёлтый"}, {"en": "green", "ipa": "ɡriːn", "ru": "зелёный"},
                {"en": "blue", "ipa": "bluː", "ru": "синий"}, {"en": "purple", "ipa": "ˈpɜː.pl̩", "ru": "фиолетовый"},
                {"en": "pink", "ipa": "pɪŋk", "ru": "розовый"}, {"en": "black", "ipa": "blæk", "ru": "чёрный"},
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
        "color": "#e88fa8", "icon": "📚", "desc": "Повседневные слова: семья, еда, дом, тело",
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
            "Части тела": {"words": [
                {"en": "head", "ipa": "hed", "ru": "голова"}, {"en": "eye", "ipa": "aɪ", "ru": "глаз"},
                {"en": "ear", "ipa": "ɪər", "ru": "ухо"}, {"en": "nose", "ipa": "nəʊz", "ru": "нос"},
                {"en": "mouth", "ipa": "maʊθ", "ru": "рот"}, {"en": "hand", "ipa": "hænd", "ru": "рука"},
                {"en": "leg", "ipa": "leɡ", "ru": "нога"}, {"en": "heart", "ipa": "hɑːt", "ru": "сердце"},
            ]},
            "Профессии": {"words": [
                {"en": "doctor", "ipa": "ˈdɒk.tər", "ru": "врач"}, {"en": "teacher", "ipa": "ˈtiː.tʃər", "ru": "учитель"},
                {"en": "engineer", "ipa": "ˌen.dʒɪˈnɪər", "ru": "инженер"}, {"en": "programmer", "ipa": "ˈprəʊ.ɡræm.ər", "ru": "программист"},
                {"en": "driver", "ipa": "ˈdraɪ.vər", "ru": "водитель"}, {"en": "cook", "ipa": "kʊk", "ru": "повар"},
            ]},
        },
    },
    "3. Время и природа": {
        "color": "#f9e2af", "icon": "🌍", "desc": "Дни недели, погода, природа и космос",
        "subsections": {
            "Дни недели": {"words": [
                {"en": "Monday", "ipa": "ˈmʌn.deɪ", "ru": "понедельник"}, {"en": "Tuesday", "ipa": "ˈtjuːz.deɪ", "ru": "вторник"},
                {"en": "Wednesday", "ipa": "ˈwenz.deɪ", "ru": "среда"}, {"en": "Thursday", "ipa": "ˈθɜːz.deɪ", "ru": "четверг"},
                {"en": "Friday", "ipa": "ˈfraɪ.deɪ", "ru": "пятница"}, {"en": "Saturday", "ipa": "ˈsæt.ə.deɪ", "ru": "суббота"},
                {"en": "Sunday", "ipa": "ˈsʌn.deɪ", "ru": "воскресенье"},
            ]},
            "Месяцы": {"words": [
                {"en": "January", "ipa": "ˈdʒæn.ju.ər.i", "ru": "январь"}, {"en": "February", "ipa": "ˈfeb.ru.ər.i", "ru": "февраль"},
                {"en": "March", "ipa": "mɑːtʃ", "ru": "март"}, {"en": "April", "ipa": "ˈeɪ.prəl", "ru": "апрель"},
                {"en": "May", "ipa": "meɪ", "ru": "май"}, {"en": "June", "ipa": "dʒuːn", "ru": "июнь"},
                {"en": "July", "ipa": "dʒuˈlaɪ", "ru": "июль"}, {"en": "August", "ipa": "ɔːˈɡʌst", "ru": "август"},
                {"en": "September", "ipa": "sepˈtem.bər", "ru": "сентябрь"}, {"en": "October", "ipa": "ɒkˈtəʊ.bər", "ru": "октябрь"},
                {"en": "November", "ipa": "nəʊˈvem.bər", "ru": "ноябрь"}, {"en": "December", "ipa": "dɪˈsem.bər", "ru": "декабрь"},
            ]},
            "Погода": {"words": [
                {"en": "weather", "ipa": "ˈweð.ər", "ru": "погода"}, {"en": "sun", "ipa": "sʌn", "ru": "солнце"},
                {"en": "rain", "ipa": "reɪn", "ru": "дождь"}, {"en": "snow", "ipa": "snəʊ", "ru": "снег"},
                {"en": "wind", "ipa": "wɪnd", "ru": "ветер"}, {"en": "cloud", "ipa": "klaʊd", "ru": "облако"},
                {"en": "hot", "ipa": "hɒt", "ru": "жарко"}, {"en": "cold", "ipa": "kəʊld", "ru": "холодно"},
            ]},
            "Космос": {"words": [
                {"en": "space", "ipa": "speɪs", "ru": "космос"}, {"en": "star", "ipa": "stɑːr", "ru": "звезда"},
                {"en": "moon", "ipa": "muːn", "ru": "луна"}, {"en": "planet", "ipa": "ˈplæn.ɪt", "ru": "планета"},
                {"en": "Earth", "ipa": "ɜːθ", "ru": "Земля"}, {"en": "Mars", "ipa": "mɑːz", "ru": "Марс"},
            ]},
        },
    },
    "4. Фразы и общение": {
        "color": "#7bc9b8", "icon": "💬", "desc": "Приветствия, вежливость, путешествия",
        "subsections": {
            "Приветствие": {"words": [
                {"en": "Hello!", "ipa": "həˈloʊ", "ru": "Привет!"}, {"en": "Good morning!", "ipa": "ɡʊd ˈmɔːr.nɪŋ", "ru": "Доброе утро!"},
                {"en": "Good evening!", "ipa": "ɡʊd ˈiːv.nɪŋ", "ru": "Добрый вечер!"}, {"en": "How are you?", "ipa": "haʊ ɑːr juː", "ru": "Как дела?"},
                {"en": "Goodbye!", "ipa": "ɡʊdˈbaɪ", "ru": "До свидания!"},
            ]},
            "Вежливость": {"words": [
                {"en": "Thank you", "ipa": "θæŋk juː", "ru": "Спасибо"}, {"en": "Please", "ipa": "pliːz", "ru": "Пожалуйста"},
                {"en": "Sorry", "ipa": "ˈsɒr. i", "ru": "Извините"}, {"en": "Excuse me", "ipa": "ɪkˈskjuːz miː", "ru": "Простите"},
                {"en": "No problem", "ipa": "noʊ ˈprɒb.ləm", "ru": "Без проблем"},
            ]},
            "В аэропорту": {"words": [
                {"en": "Where is the gate?", "ipa": "weər ɪz ðə ɡeɪt", "ru": "Где выход на посадку?"},
                {"en": "I have a connecting flight.", "ipa": "aɪ hæv ə kəˈnek.tɪŋ flaɪt", "ru": "У меня стыковочный рейс."},
                {"en": "Is it a direct flight?", "ipa": "ɪz ɪt ə dəˈrekt flaɪt", "ru": "Это прямой рейс?"},
                {"en": "My luggage is lost.", "ipa": "maɪ ˈlʌɡ.ɪdʒ ɪz lɒst", "ru": "Мой багаж потерялся."},
            ]},
        },
    },
    "5. Продвинутый уровень": {
        "color": "#cba6f7", "icon": "🚀", "desc": "Идиомы, сленг и деловой английский (Платно)",
        "subsections": {
            "Идиомы": {"words": [
                {"en": "Hit the sack", "ipa": "hɪt ðə sæk", "ru": "Отправиться спать"},
                {"en": "Twist someone's arm", "ipa": "twɪst ˈsʌm.wʌnz ɑːrm", "ru": "Уговорить"},
                {"en": "Hit the books", "ipa": "hɪt ðə bʊks", "ru": "Усердно учиться"},
                {"en": "Spill the beans", "ipa": "spɪl ðə biːnz", "ru": "Выдать секрет"},
            ]},
            "Фразовые глаголы": {"words": [
                {"en": "Give up", "ipa": "ɡɪv ʌp", "ru": "Сдаваться"},
                {"en": "Look after", "ipa": "lʊk ˈɑːf.tər", "ru": "Заботиться"},
                {"en": "Find out", "ipa": "faɪnd aʊt", "ru": "Выяснить"},
                {"en": "Turn on / off", "ipa": "tɜːn ɒn / ɒf", "ru": "Включить / выключить"},
                {"en": "Put off", "ipa": "pʊt ɒf", "ru": "Откладывать"},
            ]},
            "Полезные прилагательные": {"words": [
                {"en": "Amazing", "ipa": "əˈmeɪ.zɪŋ", "ru": "Изумительный"},
                {"en": "Awful", "ipa": "ˈɔː.fəl", "ru": "Ужасный"},
                {"en": "Huge", "ipa": "hjuːdʒ", "ru": "Огромный"},
                {"en": "Tiny", "ipa": "ˈtaɪ.ni", "ru": "Крошечный"},
                {"en": "Exhausted", "ipa": "ɪɡˈzɔː.stɪd", "ru": "Измученный"},
            ]},
            "Деловой английский": {"words": [
                {"en": "Deadline", "ipa": "ˈded.laɪn", "ru": "Крайний срок"},
                {"en": "Meeting", "ipa": "ˈmiː.tɪŋ", "ru": "Встреча"},
                {"en": "Report", "ipa": "rɪˈpɔːt", "ru": "Отчёт"},
                {"en": "Client", "ipa": "ˈklaɪ.ənt", "ru": "Клиент"},
            ]},
            "Сленг": {"words": [
                {"en": "Chill", "ipa": "tʃɪl", "ru": "Расслабляться"},
                {"en": "Awesome", "ipa": "ˈɔː.səm", "ru": "Круто"},
                {"en": "Broke", "ipa": "brəʊk", "ru": "Без денег"},
                {"en": "Hang out", "ipa": "hæŋ aʊt", "ru": "Тусоваться"},
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
