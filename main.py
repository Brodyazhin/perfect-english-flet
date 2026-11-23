import flet as ft
import threading
import time
import random
from datetime import date
from data import DATA, count_words, all_words_flat, collect_words
from subscription import state, TIERS


FAQ_DATA = {
    "💳 Подписка и оплата": [
        {"q": "Как оформить подписку?",
         "a": "На главном экране нажмите на голубую карточку тарифа сверху — или сразу перейдите в раздел «Подписка». Выберите план, нажмите «Оформить» и введите данные карты (можно использовать тестовые). Оплата проходит мгновенно."},
        {"q": "Какие тарифы доступны?",
         "a": "🆓 Бесплатный — 30 карточек в день, базовый раздел.\n\n⭐ Плюс — 199 ₽/мес: 500 карточек в день, все разделы, продвинутый уровень.\n\n👑 Премиум — 499 ₽/мес: безлимит, экспорт прогресса, приоритетная поддержка."},
        {"q": "Есть ли пробный период?",
         "a": "Да! При первом запуске автоматически активируется 7 дней тарифа Плюс. По истечении срока вы можете оформить подписку или продолжить на бесплатном тарифе."},
        {"q": "Какие промокоды есть?",
         "a": "🎟 Попробуйте в диалоге оплаты:\n• WELCOME — скидка 10%\n• STUDENT — скидка 20%\n• FRIEND — скидка 15%"},
        {"q": "Какие способы оплаты?",
         "a": "Банковская карта и СБП. Платежи имитируются — реальные деньги не списываются, данные карты не сохраняются."},
        {"q": "Как получить возврат средств?",
         "a": "Возврат возможен в течение 14 дней с момента оплаты. Напишите на support@perfectenglish.app с указанием даты покупки и названия тарифа."},
    ],
    "📱 Использование приложения": [
        {"q": "Как добавить карточку в избранное?",
         "a": "Откройте карточку и нажмите ❤ в правом верхнем углу. Все избранные карточки доступны в нижней вкладке «Избранное»."},
        {"q": "Как посмотреть перевод?",
         "a": "На карточке нажмите кнопку «Показать перевод» — перевод появится прямо под словом. Чтобы скрыть — нажмите «Скрыть»."},
        {"q": "Что значит статус «Изучено»?",
         "a": "Карточка помечается как «Изучено», когда вы нажимаете зелёную кнопку ✓. Такие карточки учитываются в статистике прогресса."},
        {"q": "Что такое серия дней?",
         "a": "🔥 Серия (streak) — это сколько дней подряд вы заходите в приложение. Если пропустите день — серия начнётся заново с 1."},
        {"q": "Что означают типы карточек?",
         "a": "📖 БУКВА — буква алфавита\n📝 СЛОВО — отдельное слово\n💬 ФРАЗА — короткое выражение\n🗨️ ПРЕДЛОЖЕНИЕ — полное предложение\n🎭 ИДИОМА — выражение с переносным смыслом\n🔗 ФРАЗ. ГЛАГОЛ — глагол с предлогом\n😎 СЛЕНГ — неформальное выражение"},
        {"q": "Работает ли приложение офлайн?",
         "a": "Да! Все карточки хранятся локально. Приложение полностью работает без интернета."},
    ],
    "🧠 Тесты и квизы": [
        {"q": "Как пройти тест?",
         "a": "Два способа:\n1️⃣ На главной — карточка «Тесты и квизы» → выберите тему\n2️⃣ В любом разделе → нажмите иконку 🧠 рядом с подразделом\n\nКаждый тест содержит до 10 вопросов: половина — перевод en→ru, половина — ru→en."},
        {"q": "Как считаются результаты?",
         "a": "За каждый правильный ответ +1 балл. В конце — процент:\n🏆 90–100% — отлично\n🎉 70–89% — хорошо\n👍 50–69% — неплохо\n📚 < 50% — стоит повторить"},
    ],
    "🇬🇧 Изучение английского": [
        {"q": "С чего начать?",
         "a": "С раздела «База»: буквы, числа, цвета, местоимения. Затем — «Словарный запас»: семья, еда, дом, животные."},
        {"q": "Что такое IPA-транскрипция?",
         "a": "International Phonetic Alphabet — международный фонетический алфавит. Запись [ˈæp.əl] показывает произношение. ˈ — ударение на следующий слог."},
        {"q": "Как эффективно запоминать?",
         "a": "1. Учите 10–15 карточек в день\n2. Повторяйте через 1, 3 и 7 дней\n3. Используйте в речи и письме\n4. Сложные добавляйте в избранное ❤\n5. Проверяйте себя в квизах 🧠"},
    ],
}

OPTION_COLORS = [
    ft.Colors.BLUE_100, ft.Colors.PURPLE_100,
    ft.Colors.ORANGE_100, ft.Colors.TEAL_100,
]

TYPE_INFO = {
    "letter":       {"emoji": "📖", "label": "БУКВА",         "color": ft.Colors.BLUE_400},
    "word":         {"emoji": "📝", "label": "СЛОВО",         "color": ft.Colors.GREEN_600},
    "phrase":       {"emoji": "💬", "label": "ФРАЗА",         "color": ft.Colors.PURPLE_400},
    "sentence":     {"emoji": "🗨️", "label": "ПРЕДЛОЖЕНИЕ",   "color": ft.Colors.ORANGE_500},
    "idiom":        {"emoji": "🎭", "label": "ИДИОМА",        "color": ft.Colors.PINK_400},
    "phrasal_verb": {"emoji": "🔗", "label": "ФРАЗ. ГЛАГОЛ",  "color": ft.Colors.TEAL_500},
    "slang":        {"emoji": "😎", "label": "СЛЕНГ",         "color": ft.Colors.AMBER_700},
}

PROMO_CODES = {"WELCOME": 0.10, "STUDENT": 0.20, "FRIEND": 0.15}


def cards_plural(n):
    n = abs(n)
    if n % 10 == 1 and n % 100 != 11:
        return f"{n} карточка"
    if 2 <= n % 10 <= 4 and not (12 <= n % 100 <= 14):
        return f"{n} карточки"
    return f"{n} карточек"


def build_quiz(words, count=10):
    if len(words) < 4:
        return []
    all_words = all_words_flat()
    sample = random.sample(words, min(count, len(words)))
    questions = []
    for i, w in enumerate(sample):
        mode = "en_ru" if i % 2 == 0 else "ru_en"
        if mode == "en_ru":
            prompt, correct, field = w["en"], w["ru"], "ru"
        else:
            prompt, correct, field = w["ru"], w["en"], "en"

        candidates = list({x[field] for x in all_words if x[field] != correct})
        if len(candidates) < 3:
            candidates = list({x[field] for x in words if x[field] != correct})
        if len(candidates) < 3:
            continue

        distractors = random.sample(candidates, 3)
        options = distractors + [correct]
        random.shuffle(options)
        questions.append({
            "word": w, "prompt": prompt, "options": options,
            "correct_idx": options.index(correct), "mode": mode,
        })
    return questions


def main(page: ft.Page):
    page.title = "Perfect English"
    page.theme_mode = (ft.ThemeMode.DARK
                       if state.progress.get("theme_mode") == "dark"
                       else ft.ThemeMode.LIGHT)
    page.padding = 0
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)

    state.record_activity()

    chat_messages = [
        {"text": "👋 Привет! Я техподдержка Perfect English.\nЧем могу помочь? Выберите тему ниже или задайте вопрос — а в разделе ❓ FAQ вы найдёте ответы на частые вопросы.", "is_user": False}
    ]

    def toggle_theme(e):
        new_mode = (ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT
                    else ft.ThemeMode.LIGHT)
        page.theme_mode = new_mode
        state.set_theme("dark" if new_mode == ft.ThemeMode.DARK else "light")
        page.update()

    def navigate(route):
        page.views.clear()
        views = {
            "/": home_view, "/section": section_view, "/flashcards": flashcards_view,
            "/search": search_view, "/favorites": favorites_view, "/stats": stats_view,
            "/subscription": subscription_view, "/support": support_view,
            "/faq": faq_view, "/quiz_select": quiz_select_view, "/quiz": quiz_view,
        }
        page.views.append(views[route]())
        page.update()

    # --- ГЛАВНОЕ МЕНЮ ---
    def home_view():
        tier = TIERS[state.license["tier"]]

        section_cards = []
        for name, item in DATA.items():
            is_locked = (name.startswith("5.") and state.license["tier"] == "free")
            accent = item.get("color", "#7c9cf5")
            lock_icon = ft.Icon(ft.Icons.LOCK, color=ft.Colors.RED) if is_locked else ft.Icon(ft.Icons.CHEVRON_RIGHT, color=ft.Colors.GREY_400)

            section_cards.append(
                ft.Container(
                    content=ft.Container(
                        content=ft.ListTile(
                            leading=ft.Container(
                                content=ft.Text(item["icon"], size=28),
                                bgcolor=ft.Colors.with_opacity(0.25, accent),
                                border_radius=12, width=50, height=50,
                                alignment=ft.Alignment.CENTER
                            ),
                            title=ft.Text(name, weight=ft.FontWeight.BOLD, size=16),
                            subtitle=ft.Text(item["desc"], color=ft.Colors.GREY_600, size=12,
                                             max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                            trailing=lock_icon,
                        ),
                        padding=5, border_radius=16,
                    ),
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                    border=ft.Border.all(2, accent),
                    border_radius=20, margin=ft.Margin(bottom=12),
                    shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK), offset=ft.Offset(0, 5)),
                    on_click=lambda e, n=name, locked=is_locked: open_section(n, locked)
                )
            )

        # Карточка "Продолжить обучение"
        continue_card = ft.Container()
        last_section = state.progress.get("last_section")
        last_subsection = state.progress.get("last_subsection")
        if last_section and last_subsection and last_section in DATA:
            section_item = DATA[last_section]
            accent = section_item.get("color", "#7c9cf5")
            continue_card = ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.PLAY_ARROW, color=ft.Colors.WHITE, size=26),
                        width=50, height=50,
                        alignment=ft.Alignment.CENTER,
                        bgcolor=ft.Colors.with_opacity(0.25, ft.Colors.WHITE),
                        border_radius=15,
                    ),
                    ft.Column([
                        ft.Text("Продолжить обучение", weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.WHITE),
                        ft.Text(f"{last_section} · {last_subsection}", size=12, color=ft.Colors.WHITE_70),
                    ], spacing=2, expand=True),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT, color=ft.Colors.WHITE),
                ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor=accent, padding=15,
                border_radius=18, margin=ft.Margin(bottom=15),
                on_click=lambda e: continue_learning()
            )

        return ft.View(
            controls=[
                ft.AppBar(
                    title=ft.Text("Perfect English", weight=ft.FontWeight.BOLD),
                    bgcolor=ft.Colors.TRANSPARENT,
                    actions=[
                        ft.IconButton(ft.Icons.BAR_CHART, tooltip="Статистика", icon_color=ft.Colors.PURPLE_400,
                                      on_click=lambda e: navigate("/stats")),
                        ft.IconButton(ft.Icons.BRIGHTNESS_6, icon_color=ft.Colors.ORANGE_400, on_click=toggle_theme)
                    ]
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Container(
                            content=ft.Row([
                                ft.Column([
                                    ft.Text(f"{tier['icon']} {tier['name']} тариф", weight=ft.FontWeight.BOLD, size=18),
                                    ft.Text("Управление подпиской", size=12, color=ft.Colors.WHITE_70),
                                ], expand=True, spacing=4),
                                ft.Icon(ft.Icons.DIAMOND, color=ft.Colors.ORANGE_400, size=30)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                            bgcolor=ft.Colors.BLUE_600, padding=20,
                            border_radius=20, margin=ft.Margin(bottom=15),
                            on_click=lambda e: navigate("/subscription")
                        ),
                        continue_card,
                        ft.Container(
                            content=ft.Row([
                                ft.Container(
                                    content=ft.Text("🧠", size=32),
                                    width=60, height=60,
                                    alignment=ft.Alignment.CENTER,
                                    bgcolor=ft.Colors.with_opacity(0.25, ft.Colors.WHITE),
                                    border_radius=15,
                                ),
                                ft.Column([
                                    ft.Text("Тесты и квизы", weight=ft.FontWeight.BOLD, size=18, color=ft.Colors.WHITE),
                                    ft.Text("Проверьте свои знания", size=12, color=ft.Colors.WHITE_70),
                                ], spacing=2, expand=True),
                                ft.Icon(ft.Icons.CHEVRON_RIGHT, color=ft.Colors.WHITE),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                            bgcolor=ft.Colors.DEEP_ORANGE_400, padding=20,
                            border_radius=20, margin=ft.Margin(bottom=20),
                            on_click=lambda e: navigate("/quiz_select")
                        ),
                        ft.Text("Разделы", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800),
                        ft.Container(height=10),
                        ft.Column(section_cards, spacing=0)
                    ], scroll=ft.ScrollMode.AUTO),
                    padding=20, expand=True
                )
            ],
            navigation_bar=ft.NavigationBar(
                destinations=[
                    ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Главная"),
                    ft.NavigationBarDestination(icon=ft.Icons.SEARCH, label="Поиск"),
                    ft.NavigationBarDestination(icon=ft.Icons.FAVORITE, label="Избранное"),
                    ft.NavigationBarDestination(icon=ft.Icons.SUPPORT_AGENT, label="Поддержка"),
                ],
                on_change=lambda e: navigate(["/", "/search", "/favorites", "/support"][e.control.selected_index])
            )
        )

    # --- ТЕХПОДДЕРЖКА ---
    def get_bot_response(text: str) -> str:
        t = text.lower()
        rules = [
            (["привет", "здравств", "hello", "hi", "добр"],
             "👋 Здравствуйте! Рад помочь. Задайте вопрос или выберите тему ниже.\n\n💡 Совет: в разделе ❓ FAQ собраны ответы на самые частые вопросы."),
            (["тест", "квиз", "quiz", "провер"],
             "🧠 Тесты и квизы доступны двумя способами:\n\n1️⃣ На главной — карточка «Тесты и квизы»\n2️⃣ В любом разделе — иконка 🧠 рядом с подразделом\n\nВ каждом тесте до 10 вопросов: половина en→ru, половина ru→en."),
            (["streak", "серия", "дней"],
             "🔥 Серия — это сколько дней подряд вы заходите в приложение. Если пропустите день — серия начнётся заново с 1."),
            (["оплат", "купить", "оформ", "подписк", "тариф", "прем", "плюс"],
             "💳 Оформить подписку можно двумя способами:\n\n1️⃣ Голубая карточка тарифа на главном экране\n2️⃣ Раздел «Подписка»\n\nТарифы:\n⭐ Плюс — 199 ₽/мес\n👑 Премиум — 499 ₽/мес\n\n🎟 Промокоды: WELCOME (−10%), STUDENT (−20%), FRIEND (−15%)"),
            (["промокод", "скидк", "акци", "купон"],
             "🎟 Промокоды:\n• WELCOME — скидка 10%\n• STUDENT — скидка 20%\n• FRIEND — скидка 15%\n\nВводятся в диалоге оплаты."),
            (["перевод", "перевест", "значен"],
             "🔍 Нажмите «Показать перевод» под английским словом на карточке — перевод появится прямо в карточке. Нажмите «Скрыть» — спрячется."),
            (["баг", "ошибк", "не работает", "глючит", "падает", "вылет"],
             "⚠ Приносим извинения!\n\nОпишите, пожалуйста:\n• Что вы делали перед ошибкой?\n• Что произошло?\n• Модель устройства\n\nПередадим в разработку."),
            (["возврат", "вернуть", "отмен", "деньг"],
             "💸 Возврат возможен в течение 14 дней после оплаты.\n\nНапишите на support@perfectenglish.app с датой покупки и названием тарифа."),
            (["слов", "карточк", "учить", "учиться", "запомина"],
             "📚 Метод интервального повторения:\n\n1️⃣ Учите 10–15 карточек в день\n2️⃣ Возвращайтесь через 1, 3 и 7 дней\n3️⃣ Сложные — в ❤ Избранное\n4️⃣ Проверяйте себя в квизах 🧠"),
            (["транскрипц", "ipa", "произнош", "звук"],
             "🔊 IPA — международный фонетический алфавит.\n\nПример: apple [ˈæp.əl]\n• ˈ — ударение на следующий слог\n• æ — звук «э»\n• ə — безударный «шва»"),
            (["статистик", "прогресс", "streak", "серия"],
             "📊 «Статистика» — по иконке 📈 в верхней панели.\n\n🔥 серия дней\n📖 изучено карточек\n⭐ избранное\n🧠 результаты квизов"),
            (["избранн", "любим", "сердечк"],
             "❤ Открывайте карточку и жмите ❤ в правом верхнем углу."),
            (["поиск", "найти", "где найти"],
             "🔍 В нижней вкладке «Поиск» введите слово или перевод."),
            (["офлайн", "интернет", "без сети"],
             "📴 Приложение работает полностью офлайн!"),
            (["спасиб", "благодар", "thanks"],
             "😊 Всегда рады помочь! Успехов в изучении английского! 🇬🇧"),
        ]
        for keywords, response in rules:
            if any(k in t for k in keywords):
                return response
        return ("🤔 Передал вопрос оператору — ответим в течение 24 часов.\n\n"
                "А пока загляните в ❓ FAQ!")

    def support_view():
        messages_list = ft.ListView(expand=True, spacing=10, padding=20)

        def make_bubble_row(msg):
            is_user = msg["is_user"]
            bubble = ft.Container(
                content=ft.Text(msg["text"], color=ft.Colors.WHITE if is_user else ft.Colors.BLACK, size=14),
                bgcolor=ft.Colors.BLUE_500 if is_user else ft.Colors.GREY_200,
                padding=15,
                border_radius=ft.BorderRadius(
                    top_left=15, top_right=15,
                    bottom_left=15 if is_user else 0,
                    bottom_right=0 if is_user else 15
                )
            )
            bubble_zone = ft.Container(content=bubble, expand=4,
                                       alignment=ft.Alignment.CENTER_RIGHT if is_user else ft.Alignment.CENTER_LEFT)
            spacer = ft.Container(expand=1)
            return ft.Row([spacer, bubble_zone]) if is_user else ft.Row([bubble_zone, spacer])

        def render_messages():
            messages_list.controls.clear()
            for msg in chat_messages:
                if msg.get("is_typing"):
                    messages_list.controls.append(
                        ft.Row([
                            ft.Container(
                                content=ft.Row([
                                    ft.ProgressRing(width=14, height=14, stroke_width=2, color=ft.Colors.BLUE_400),
                                    ft.Text("печатает…", size=12, color=ft.Colors.GREY_600, italic=True)
                                ], spacing=8),
                                bgcolor=ft.Colors.GREY_200, padding=12,
                                border_radius=ft.BorderRadius(top_left=15, top_right=15, bottom_left=0, bottom_right=15),
                            )
                        ], alignment=ft.MainAxisAlignment.START)
                    )
                else:
                    messages_list.controls.append(make_bubble_row(msg))
            page.update()

        def send_text(text: str):
            if not text.strip():
                return
            chat_messages.append({"text": text, "is_user": True})
            typing_msg = {"text": "", "is_user": False, "is_typing": True}
            chat_messages.append(typing_msg)
            render_messages()

            def bot_reply():
                time.sleep(0.9)
                try:
                    chat_messages.remove(typing_msg)
                except ValueError:
                    pass
                chat_messages.append({"text": get_bot_response(text), "is_user": False})
                render_messages()

            threading.Thread(target=bot_reply, daemon=True).start()

        def send_message(e):
            text = input_field.value
            input_field.value = ""
            page.update()
            send_text(text)

        render_messages()
        input_field = ft.TextField(hint_text="Введите сообщение…", expand=True,
                                   border_radius=20, on_submit=send_message)

        def make_chip(label, text, color):
            return ft.Chip(label=ft.Text(label, size=12, color=ft.Colors.WHITE),
                           bgcolor=color, on_click=lambda e: send_text(text))

        quick_replies = ft.Container(
            content=ft.ListView(
                controls=[
                    make_chip("🧠 Тесты", "Как пройти тест?", ft.Colors.DEEP_ORANGE_400),
                    make_chip("💳 Подписка", "Как оформить подписку?", ft.Colors.BLUE_400),
                    make_chip("🎟 Промокод", "Какие есть промокоды?", ft.Colors.PURPLE_400),
                    make_chip("💸 Возврат", "Хочу вернуть деньги", ft.Colors.RED_400),
                    make_chip("🔍 Перевод", "Как посмотреть перевод?", ft.Colors.INDIGO_400),
                    make_chip("📚 Обучение", "Как эффективнее учить?", ft.Colors.GREEN_600),
                    ft.Chip(label=ft.Text("❓ FAQ", size=12, color=ft.Colors.WHITE),
                            bgcolor=ft.Colors.TEAL_500,
                            on_click=lambda e: navigate("/faq")),
                ],
                spacing=8, horizontal=True, height=45,
            ),
            padding=ft.Padding(left=10, right=10, top=8, bottom=4),
        )

        return ft.View(
            controls=[
                ft.AppBar(
                    title=ft.Text("Техподдержка"), bgcolor=ft.Colors.TRANSPARENT,
                    leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/")),
                    actions=[ft.IconButton(ft.Icons.HELP_OUTLINE, icon_color=ft.Colors.TEAL_500,
                                           tooltip="Частые вопросы", on_click=lambda e: navigate("/faq"))]
                ),
                messages_list,
                quick_replies,
                ft.Container(
                    content=ft.Row([
                        input_field,
                        ft.Container(
                            content=ft.Icon(ft.Icons.SEND, color=ft.Colors.WHITE),
                            bgcolor=ft.Colors.BLUE_500, padding=10, border_radius=25,
                            on_click=send_message
                        )
                    ]),
                    padding=10, bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
                )
            ],
            navigation_bar=ft.NavigationBar(
                destinations=[
                    ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Главная"),
                    ft.NavigationBarDestination(icon=ft.Icons.SEARCH, label="Поиск"),
                    ft.NavigationBarDestination(icon=ft.Icons.FAVORITE, label="Избранное"),
                    ft.NavigationBarDestination(icon=ft.Icons.SUPPORT_AGENT, label="Поддержка"),
                ],
                selected_index=3,
                on_change=lambda e: navigate(["/", "/search", "/favorites", "/support"][e.control.selected_index])
            )
        )

    # --- FAQ ---
    def faq_view():
        expanded = {}
        faq_list = ft.Column(spacing=6, scroll=ft.ScrollMode.AUTO, expand=True,
                             horizontal_alignment=ft.CrossAxisAlignment.STRETCH)

        def render_faq():
            faq_list.controls.clear()
            for category, questions in FAQ_DATA.items():
                faq_list.controls.append(
                    ft.Container(content=ft.Text(category, size=16, weight=ft.FontWeight.BOLD),
                                 margin=ft.Margin(top=15, bottom=5, left=4))
                )
                for i, item in enumerate(questions):
                    key = f"{category}#{i}"
                    is_open = expanded.get(key, False)
                    faq_list.controls.append(
                        ft.Container(
                            content=ft.Column([
                                ft.Container(
                                    content=ft.Row([
                                        ft.Text(item["q"], weight=ft.FontWeight.W_600, size=14, expand=True),
                                        ft.Icon(ft.Icons.EXPAND_LESS if is_open else ft.Icons.EXPAND_MORE,
                                                color=ft.Colors.BLUE, size=20),
                                    ]),
                                    padding=15, on_click=lambda e, k=key: toggle_faq(k),
                                ),
                                ft.Container(
                                    content=ft.Text(item["a"], size=13, color=ft.Colors.GREY_700),
                                    padding=ft.Padding(left=15, right=15, bottom=15, top=0),
                                    visible=is_open,
                                ),
                            ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.STRETCH),
                            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST, border_radius=15,
                        )
                    )
            page.update()

        def toggle_faq(key):
            expanded[key] = not expanded.get(key, False)
            render_faq()

        render_faq()

        return ft.View(
            controls=[
                ft.AppBar(title=ft.Text("Частые вопросы", weight=ft.FontWeight.BOLD),
                          bgcolor=ft.Colors.TRANSPARENT,
                          leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/support"))),
                ft.Container(
                    content=ft.Column([
                        ft.Container(
                            content=ft.Row([
                                ft.Container(content=ft.Icon(ft.Icons.SUPPORT_AGENT, color=ft.Colors.WHITE, size=24),
                                             bgcolor=ft.Colors.BLUE_500, padding=10, border_radius=10),
                                ft.Column([
                                    ft.Text("Не нашли ответ?", weight=ft.FontWeight.BOLD, size=14),
                                    ft.Text("Задайте вопрос в поддержке", size=12, color=ft.Colors.GREY_600),
                                ], spacing=2, expand=True),
                                ft.Icon(ft.Icons.CHEVRON_RIGHT, color=ft.Colors.GREY_400),
                            ]),
                            bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.BLUE),
                            padding=15, border_radius=15, margin=ft.Margin(bottom=10),
                            on_click=lambda e: navigate("/support"),
                        ),
                        faq_list,
                    ], expand=True),
                    padding=20, expand=True,
                ),
            ],
            navigation_bar=ft.NavigationBar(
                destinations=[
                    ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Главная"),
                    ft.NavigationBarDestination(icon=ft.Icons.SEARCH, label="Поиск"),
                    ft.NavigationBarDestination(icon=ft.Icons.FAVORITE, label="Избранное"),
                    ft.NavigationBarDestination(icon=ft.Icons.SUPPORT_AGENT, label="Поддержка"),
                ],
                selected_index=3,
                on_change=lambda e: navigate(["/", "/search", "/favorites", "/support"][e.control.selected_index])
            )
        )

    # --- РАЗДЕЛЫ ---
    current_section_data = {}

    def open_section(section_name, is_locked):
        if is_locked:
            page.show_dialog(ft.AlertDialog(
                title=ft.Text("Раздел заблокирован"),
                content=ft.Text("Для доступа к «Продвинутому уровню» оформите подписку."),
                actions=[
                    ft.TextButton("Отмена", on_click=lambda e: page.pop_dialog()),
                    ft.TextButton("Оформить", on_click=lambda e: (page.pop_dialog(), navigate("/subscription")))
                ]
            ))
            return
        current_section_data.clear()
        current_section_data.update({"name": section_name, "item": DATA[section_name]})
        navigate("/section")

    def continue_learning():
        section_name = state.progress.get("last_section")
        sub_name = state.progress.get("last_subsection")
        if section_name and sub_name and section_name in DATA:
            item = DATA[section_name]
            if sub_name in item["subsections"]:
                current_section_data.clear()
                current_section_data.update({"name": section_name, "item": item})
                open_flashcards(sub_name, item["subsections"][sub_name])
                return
        navigate("/")

    def section_view():
        name = current_section_data["name"]
        item = current_section_data["item"]
        accent = item.get("color", "#7c9cf5")
        subs_list = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True,
                              horizontal_alignment=ft.CrossAxisAlignment.STRETCH)

        def render_subs(query=""):
            subs_list.controls.clear()
            for sub_name, sub_item in item["subsections"].items():
                if query and query.lower() not in sub_name.lower():
                    continue
                words = collect_words(sub_item)
                has_quiz = len(words) >= 4
                kind = sub_item.get("kind", "word")
                info = TYPE_INFO.get(kind, TYPE_INFO["word"])

                actions = ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.STYLE, color=ft.Colors.WHITE, size=20),
                        bgcolor=ft.Colors.BLUE_500, width=38, height=38, border_radius=10,
                        alignment=ft.Alignment.CENTER,
                        on_click=lambda e, n=sub_name, i=sub_item: open_flashcards(n, i),
                    ),
                    ft.Container(
                        content=ft.Icon(ft.Icons.QUIZ, color=ft.Colors.WHITE, size=20),
                        bgcolor=ft.Colors.DEEP_ORANGE_400 if has_quiz else ft.Colors.GREY_400,
                        width=38, height=38, border_radius=10,
                        alignment=ft.Alignment.CENTER,
                        on_click=lambda e, i=sub_item, has=has_quiz, n=sub_name: (
                            start_quiz_by_words(collect_words(i), n) if has else None
                        ),
                    ),
                ], spacing=6, tight=True)

                subs_list.controls.append(
                    ft.Container(
                        content=ft.ListTile(
                            title=ft.Text(sub_name, weight=ft.FontWeight.W_600),
                            subtitle=ft.Text(f"{info['emoji']} {info['label']}",
                                             size=11, color=ft.Colors.GREY_600),
                            trailing=actions,
                        ),
                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                        border=ft.Border.all(1, ft.Colors.with_opacity(0.3, accent)),
                        border_radius=15, padding=5,
                    )
                )
            page.update()

        render_subs()

        return ft.View(
            controls=[
                ft.AppBar(title=ft.Text(name, weight=ft.FontWeight.BOLD), bgcolor=ft.Colors.TRANSPARENT,
                          leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/"))),
                ft.Container(
                    content=ft.Column([
                        ft.TextField(hint_text="Поиск по темам…", prefix_icon=ft.Icons.SEARCH,
                                     on_change=lambda e: render_subs(e.control.value),
                                     border_radius=15, filled=True,
                                     bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                                     border_color=ft.Colors.TRANSPARENT),
                        ft.Container(height=10),
                        subs_list,
                    ], expand=True),
                    padding=20, expand=True
                )
            ]
        )

    # --- КАРТОЧКИ (перевод прямо в карточке) ---
    current_cards_data = {"words": [], "index": 0, "title": "", "show_translation": False}

    def open_flashcards(title, sub_item):
        words = collect_words(sub_item)
        if not words:
            return
        current_cards_data["words"] = words
        current_cards_data["index"] = 0
        current_cards_data["title"] = title
        current_cards_data["show_translation"] = False
        if current_section_data.get("name"):
            state.set_last_opened(current_section_data["name"], title)
        navigate("/flashcards")

    def flashcards_view():
        if not current_cards_data["words"]:
            return ft.View(controls=[ft.Text("Нет карточек")])
        word = current_cards_data["words"][current_cards_data["index"]]
        is_known = word["en"] in state.progress["known"]
        is_fav = word["en"] in state.progress["favorites"]
        idx = current_cards_data["index"]
        total = len(current_cards_data["words"])
        show = current_cards_data.get("show_translation", False)

        wtype = word.get("type", "word")
        tinfo = TYPE_INFO.get(wtype, TYPE_INFO["word"])

        en_word = word["en"]
        font_size = 42 if len(en_word) <= 12 else (32 if len(en_word) <= 20 else 24)

        def next_word(e):
            if not state.can_see_more():
                limit = TIERS[state.license["tier"]]["limit"]
                tier_name = TIERS[state.license["tier"]]["name"]
                page.show_dialog(ft.AlertDialog(
                    title=ft.Text("Дневной лимит"),
                    content=ft.Text(
                        f"На тарифе «{tier_name}» можно изучать {limit} карточек в день.\n\n"
                        "Лимит обновится завтра. Или оформите подписку Плюс/Премиум для продолжения."
                    ),
                    actions=[
                        ft.TextButton("Позже", on_click=lambda e: page.pop_dialog()),
                        ft.TextButton("Оформить",
                                      on_click=lambda e: (page.pop_dialog(), navigate("/subscription")))
                    ]
                ))
                return
            state.add_seen()
            current_cards_data["index"] = (idx + 1) % total
            current_cards_data["show_translation"] = False
            page.views[-1] = flashcards_view()
            page.update()

        def prev_word(e):
            current_cards_data["index"] = (idx - 1) % total
            current_cards_data["show_translation"] = False
            page.views[-1] = flashcards_view()
            page.update()

        def mark_known(e):
            if not is_known:
                state.progress["known"].append(word["en"])
                state.save_progress()
            next_word(e)

        def toggle_fav(e):
            if is_fav:
                state.progress["favorites"].remove(word["en"])
            else:
                state.progress["favorites"].append(word["en"])
            state.save_progress()
            page.views[-1] = flashcards_view()
            page.update()

        def toggle_translation(e):
            current_cards_data["show_translation"] = not show
            page.views[-1] = flashcards_view()
            page.update()

        def shuffle_cards(e):
            random.shuffle(current_cards_data["words"])
            current_cards_data["index"] = 0
            current_cards_data["show_translation"] = False
            page.views[-1] = flashcards_view()
            page.update()

        # Только тип карточки (без "НОВАЯ"/"ИЗУЧЕНО")
        type_badge = ft.Container(
            content=ft.Text(f"{tinfo['emoji']} {tinfo['label']}", size=11,
                            weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            bgcolor=tinfo["color"],
            padding=ft.Padding(left=12, right=12, top=6, bottom=6),
            border_radius=15,
            alignment=ft.Alignment.CENTER,
        )

        card_items = [
            type_badge,
            ft.Container(height=20),
            ft.Text(en_word, size=font_size, weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER),
            ft.Text(f"[{word['ipa']}]", size=16, color=ft.Colors.GREY_600,
                    italic=True, text_align=ft.TextAlign.CENTER),
        ]

        if word.get("example"):
            card_items += [
                ft.Container(height=15),
                ft.Container(
                    content=ft.Text(f"💡 {word['example']}", size=13,
                                    color=ft.Colors.GREY_700, italic=True,
                                    text_align=ft.TextAlign.CENTER),
                    bgcolor=ft.Colors.with_opacity(0.08, tinfo["color"]),
                    padding=12, border_radius=10, width=float("inf"),
                ),
            ]

        # Блок перевода прямо в карточке
        card_items.append(ft.Container(height=20))
        card_items.append(
            ft.Container(
                content=ft.Text("─" * 20, color=ft.Colors.GREY_300,
                                text_align=ft.TextAlign.CENTER, size=12),
                margin=ft.Margin(bottom=10),
            )
        )

        if show:
            translation_block = ft.Container(
                content=ft.Column([
                    ft.Text(word["ru"], size=26, weight=ft.FontWeight.BOLD,
                            color=tinfo["color"], text_align=ft.TextAlign.CENTER),
                    ft.Container(height=8),
                    ft.TextButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.VISIBILITY_OFF, size=14, color=ft.Colors.GREY_500),
                            ft.Text("Скрыть", size=12, color=ft.Colors.GREY_500),
                        ], alignment=ft.MainAxisAlignment.CENTER, tight=True),
                        on_click=toggle_translation,
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                width=float("inf"),
            )
        else:
            translation_block = ft.Container(
                content=ft.Button(
                    content=ft.Row([
                        ft.Icon(ft.Icons.VISIBILITY, color=ft.Colors.WHITE, size=18),
                        ft.Text("Показать перевод", color=ft.Colors.WHITE, size=14),
                    ], alignment=ft.MainAxisAlignment.CENTER, tight=True),
                    bgcolor=tinfo["color"],
                    on_click=toggle_translation,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=12),
                        padding=ft.Padding(left=20, right=20, top=14, bottom=14),
                    ),
                ),
                width=float("inf"),
            )

        card_items.append(translation_block)

        return ft.View(
            controls=[
                ft.AppBar(
                    title=ft.Text(current_cards_data["title"], max_lines=1,
                                  overflow=ft.TextOverflow.ELLIPSIS),
                    bgcolor=ft.Colors.TRANSPARENT,
                    leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/section")),
                    actions=[
                        ft.Container(
                            content=ft.Text(f"{idx + 1} / {total}", size=13,
                                            weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_600),
                            padding=ft.Padding(left=5, right=5, top=12, bottom=12),
                        ),
                        ft.IconButton(ft.Icons.SHUFFLE, icon_color=ft.Colors.INDIGO_400,
                                      tooltip="Перемешать", on_click=shuffle_cards),
                        ft.IconButton(ft.Icons.FAVORITE if is_fav else ft.Icons.FAVORITE_BORDER,
                                      icon_color=ft.Colors.RED if is_fav else ft.Colors.GREY,
                                      on_click=toggle_fav),
                    ]
                ),
                ft.Container(
                    content=ft.Column([
                        ft.ProgressBar(
                            value=(idx + 1) / total,
                            height=4,
                            color=tinfo["color"],
                            bgcolor=ft.Colors.GREY_200,
                        ),
                        ft.Container(height=10),
                        ft.Container(
                            content=ft.Column(
                                card_items,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=4,
                            ),
                            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                            border_radius=30, padding=25,
                            shadow=ft.BoxShadow(blur_radius=30,
                                                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                                                offset=ft.Offset(0, 10)),
                            expand=True
                        ),
                        ft.Container(height=20),
                        ft.Container(
                            content=ft.Row([
                                ft.Container(
                                    content=ft.Icon(ft.Icons.ARROW_BACK_IOS, color=ft.Colors.WHITE, size=24),
                                    bgcolor=ft.Colors.INDIGO_400, width=50, height=50,
                                    border_radius=25, alignment=ft.Alignment.CENTER,
                                    on_click=prev_word,
                                ),
                                ft.Row([
                                    ft.Container(
                                        content=ft.Icon(ft.Icons.CLOSE, color=ft.Colors.WHITE, size=32),
                                        bgcolor=ft.Colors.RED_400, width=60, height=60,
                                        border_radius=30, alignment=ft.Alignment.CENTER,
                                        on_click=next_word,
                                    ),
                                    ft.Container(
                                        content=ft.Icon(ft.Icons.CHECK, color=ft.Colors.WHITE, size=32),
                                        bgcolor=ft.Colors.GREEN_500, width=60, height=60,
                                        border_radius=30, alignment=ft.Alignment.CENTER,
                                        on_click=mark_known,
                                    ),
                                ], spacing=40, alignment=ft.MainAxisAlignment.CENTER),
                                ft.Container(
                                    content=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, color=ft.Colors.WHITE, size=24),
                                    bgcolor=ft.Colors.INDIGO_400, width=50, height=50,
                                    border_radius=25, alignment=ft.Alignment.CENTER,
                                    on_click=next_word,
                                ),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            padding=ft.Padding(left=20, right=20),
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True),
                    padding=20, expand=True
                )
            ]
        )

    # --- КВИЗЫ ---
    current_quiz = {"questions": [], "current": 0, "score": 0, "section_name": "", "selected_idx": None}

    def start_quiz_by_words(words_pool, title):
        if len(words_pool) < 4:
            page.show_dialog(ft.AlertDialog(
                title=ft.Text("Мало карточек"),
                content=ft.Text(f"В теме «{title}» только {cards_plural(len(words_pool))}. Для теста нужно минимум 4."),
                actions=[ft.TextButton("Ок", on_click=lambda e: page.pop_dialog())]
            ))
            return
        questions = build_quiz(words_pool)
        if not questions:
            return
        current_quiz.update({"questions": questions, "current": 0, "score": 0,
                             "section_name": title, "selected_idx": None})
        navigate("/quiz")

    def quiz_select_view():
        cards = []
        all_words = all_words_flat()
        cards.append(
            ft.Container(
                content=ft.Row([
                    ft.Container(content=ft.Text("🎲", size=32), width=60, height=60,
                                 alignment=ft.Alignment.CENTER,
                                 bgcolor=ft.Colors.with_opacity(0.25, ft.Colors.WHITE),
                                 border_radius=15),
                    ft.Column([
                        ft.Text("Случайный тест", weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.WHITE),
                        ft.Text("Из всех разделов", size=12, color=ft.Colors.WHITE_70),
                    ], spacing=2, expand=True),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT, color=ft.Colors.WHITE),
                ]),
                bgcolor=ft.Colors.DEEP_ORANGE_400, padding=15,
                border_radius=18, margin=ft.Margin(bottom=10),
                on_click=lambda e: start_quiz_by_words(all_words, "🎲 Случайный тест")
            )
        )

        for name, item in DATA.items():
            words = collect_words(item)
            accent = item.get("color", "#7c9cf5")
            has_enough = len(words) >= 4
            cards.append(
                ft.Container(
                    content=ft.Row([
                        ft.Container(content=ft.Text(item["icon"], size=28), width=60, height=60,
                                     alignment=ft.Alignment.CENTER,
                                     bgcolor=ft.Colors.with_opacity(0.25, accent),
                                     border_radius=15),
                        ft.Column([
                            ft.Text(name, weight=ft.FontWeight.BOLD, size=15),
                            ft.Text("Проверить знания" if has_enough else "Недостаточно карточек",
                                    size=12, color=ft.Colors.GREY_600),
                        ], spacing=2, expand=True),
                        ft.Icon(ft.Icons.QUIZ,
                                color=accent if has_enough else ft.Colors.GREY_400, size=22),
                    ]),
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                    border=ft.Border.all(2, accent if has_enough else ft.Colors.GREY_300),
                    padding=15, border_radius=18, margin=ft.Margin(bottom=10),
                    on_click=lambda e, w=words, n=name, ok=has_enough: (
                        start_quiz_by_words(w, n) if ok else None
                    ),
                )
            )

        return ft.View(
            controls=[
                ft.AppBar(title=ft.Text("Выберите тему", weight=ft.FontWeight.BOLD),
                          bgcolor=ft.Colors.TRANSPARENT,
                          leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/"))),
                ft.Container(
                    content=ft.Column([
                        ft.Text("🧠 Проверьте свои знания", size=20, weight=ft.FontWeight.BOLD,
                                color=ft.Colors.DEEP_ORANGE_400),
                        ft.Text("Каждый тест — до 10 случайных вопросов. В конце — ваш результат.",
                                size=12, color=ft.Colors.GREY_600),
                        ft.Container(height=15),
                        ft.Column(cards, spacing=0),
                    ], scroll=ft.ScrollMode.AUTO, expand=True,
                       horizontal_alignment=ft.CrossAxisAlignment.STRETCH),
                    padding=20, expand=True,
                )
            ],
            navigation_bar=ft.NavigationBar(
                destinations=[
                    ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Главная"),
                    ft.NavigationBarDestination(icon=ft.Icons.SEARCH, label="Поиск"),
                    ft.NavigationBarDestination(icon=ft.Icons.FAVORITE, label="Избранное"),
                    ft.NavigationBarDestination(icon=ft.Icons.SUPPORT_AGENT, label="Поддержка"),
                ],
                on_change=lambda e: navigate(["/", "/search", "/favorites", "/support"][e.control.selected_index])
            )
        )

    def save_quiz_result():
        state.progress.setdefault("quiz_history", [])
        state.progress["quiz_history"].append({
            "section": current_quiz["section_name"],
            "score": current_quiz["score"],
            "total": len(current_quiz["questions"]),
            "date": str(date.today()),
        })
        state.progress["quiz_history"] = state.progress["quiz_history"][-50:]
        state.save_progress()

    def quiz_result_view():
        total = len(current_quiz["questions"])
        score = current_quiz["score"]
        pct = int(score / total * 100) if total else 0
        save_quiz_result()

        if pct >= 90:
            emoji, msg, color = "🏆", "Отлично!", ft.Colors.AMBER_500
        elif pct >= 70:
            emoji, msg, color = "🎉", "Хорошо!", ft.Colors.GREEN_500
        elif pct >= 50:
            emoji, msg, color = "👍", "Неплохо", ft.Colors.BLUE_500
        else:
            emoji, msg, color = "📚", "Стоит повторить", ft.Colors.ORANGE_500

        def restart(e):
            start_quiz_by_words(
                [q["word"] for q in current_quiz["questions"]],
                current_quiz["section_name"]
            )

        return ft.View(
            controls=[
                ft.AppBar(title=ft.Text("Результат"), bgcolor=ft.Colors.TRANSPARENT,
                          leading=ft.IconButton(ft.Icons.ARROW_BACK,
                                                on_click=lambda e: navigate("/quiz_select"))),
                ft.Container(
                    content=ft.Column([
                        ft.Container(
                            content=ft.Column([
                                ft.Text(emoji, size=80, text_align=ft.TextAlign.CENTER),
                                ft.Text(msg, size=28, weight=ft.FontWeight.BOLD, color=color,
                                        text_align=ft.TextAlign.CENTER),
                                ft.Container(height=10),
                                ft.Text(f"{score} из {total}", size=36, weight=ft.FontWeight.BOLD,
                                        text_align=ft.TextAlign.CENTER),
                                ft.Text(f"Правильных: {pct}%", size=14, color=ft.Colors.GREY_600,
                                        text_align=ft.TextAlign.CENTER),
                                ft.Container(height=10),
                                ft.Text(f"Тема: {current_quiz['section_name']}", size=12,
                                        color=ft.Colors.GREY_500, text_align=ft.TextAlign.CENTER),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                            padding=40, border_radius=25,
                            border=ft.Border.all(3, color),
                            expand=True,
                        ),
                        ft.Container(height=20),
                        ft.Button(
                            content=ft.Row([ft.Icon(ft.Icons.REFRESH, color=ft.Colors.WHITE),
                                            ft.Text("Пройти ещё раз", color=ft.Colors.WHITE, size=16)],
                                           alignment=ft.MainAxisAlignment.CENTER, tight=True),
                            bgcolor=ft.Colors.DEEP_ORANGE_400,
                            height=55, width=float("inf"), on_click=restart,
                        ),
                        ft.Container(height=10),
                        ft.Button(
                            content=ft.Text("Выбрать другую тему", color=ft.Colors.WHITE, size=16),
                            bgcolor=ft.Colors.BLUE_500,
                            height=55, width=float("inf"),
                            on_click=lambda e: navigate("/quiz_select"),
                        ),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True),
                    padding=20, expand=True,
                )
            ]
        )

    def quiz_view():
        q_data = current_quiz
        if not q_data["questions"]:
            return ft.View(controls=[ft.Text("Нет вопросов")])

        total = len(q_data["questions"])
        current = q_data["current"]
        if current >= total:
            return quiz_result_view()

        q = q_data["questions"][current]
        selected = q_data["selected_idx"]
        answered = selected is not None
        is_correct = answered and selected == q["correct_idx"]

        def answer(idx):
            if q_data["selected_idx"] is not None:
                return
            q_data["selected_idx"] = idx
            if idx == q["correct_idx"]:
                q_data["score"] += 1
            page.views[-1] = quiz_view()
            page.update()

        def next_q(e):
            q_data["current"] += 1
            q_data["selected_idx"] = None
            page.views[-1] = quiz_view()
            page.update()

        def exit_quiz(e):
            page.show_dialog(ft.AlertDialog(
                title=ft.Text("Выйти из теста?"),
                content=ft.Text("Прогресс не сохранится."),
                actions=[
                    ft.TextButton("Отмена", on_click=lambda e: page.pop_dialog()),
                    ft.TextButton("Выйти", on_click=lambda e: (page.pop_dialog(), navigate("/quiz_select")))
                ]
            ))

        progress = ft.ProgressBar(value=(current + 1) / total,
                                  bgcolor=ft.Colors.GREY_200,
                                  color=ft.Colors.DEEP_ORANGE_400, height=8)

        option_buttons = []
        for i, opt in enumerate(q["options"]):
            base_color = OPTION_COLORS[i]
            text_color = ft.Colors.BLACK
            if answered:
                if i == q["correct_idx"]:
                    base_color, text_color = ft.Colors.GREEN_500, ft.Colors.WHITE
                elif i == selected:
                    base_color, text_color = ft.Colors.RED_500, ft.Colors.WHITE

            option_buttons.append(
                ft.Container(
                    content=ft.Row([
                        ft.Container(
                            content=ft.Text("ABCD"[i], weight=ft.FontWeight.BOLD,
                                            color=text_color, size=15),
                            width=32, height=32, alignment=ft.Alignment.CENTER,
                            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                            border_radius=16,
                        ),
                        ft.Text(opt, size=15, expand=True, color=text_color,
                                weight=ft.FontWeight.W_500),
                    ], spacing=12),
                    bgcolor=base_color, padding=15, border_radius=15,
                    on_click=lambda e, idx=i: answer(idx),
                )
            )

        feedback = ft.Container()
        if answered:
            if is_correct:
                feedback = ft.Container(
                    content=ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.WHITE, size=20),
                                    ft.Text("Верно!", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)],
                                   alignment=ft.MainAxisAlignment.CENTER),
                    bgcolor=ft.Colors.GREEN_500, padding=12, border_radius=10,
                    margin=ft.Margin(top=10),
                )
            else:
                feedback = ft.Container(
                    content=ft.Column([
                        ft.Row([ft.Icon(ft.Icons.CANCEL, color=ft.Colors.WHITE, size=20),
                                ft.Text("Неверно", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)],
                               alignment=ft.MainAxisAlignment.CENTER),
                        ft.Text(f"Правильный ответ: {q['options'][q['correct_idx']]}",
                                color=ft.Colors.WHITE, size=13, text_align=ft.TextAlign.CENTER),
                    ]),
                    bgcolor=ft.Colors.RED_500, padding=12, border_radius=10,
                    margin=ft.Margin(top=10),
                )

        return ft.View(
            controls=[
                ft.AppBar(
                    title=ft.Text(q_data["section_name"], max_lines=1,
                                  overflow=ft.TextOverflow.ELLIPSIS),
                    bgcolor=ft.Colors.TRANSPARENT,
                    leading=ft.IconButton(ft.Icons.CLOSE, on_click=exit_quiz),
                    actions=[
                        ft.Container(content=ft.Text(f"{q_data['score']} / {current + 1}",
                                                     weight=ft.FontWeight.BOLD, size=14,
                                                     color=ft.Colors.DEEP_ORANGE_400),
                                     padding=ft.Padding(left=10, right=15, top=6, bottom=6))
                    ]
                ),
                ft.Container(
                    content=ft.Column([
                        progress,
                        ft.Container(height=20),
                        ft.Text(f"Вопрос {current + 1} из {total}", size=13,
                                color=ft.Colors.GREY_600, weight=ft.FontWeight.W_500),
                        ft.Container(height=10),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Выберите перевод" if q["mode"] == "en_ru" else "Выберите слово",
                                        size=12, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER),
                                ft.Container(height=15),
                                ft.Text(q["prompt"], size=26, weight=ft.FontWeight.BOLD,
                                        text_align=ft.TextAlign.CENTER),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                            padding=30, border_radius=20,
                            border=ft.Border.all(2, ft.Colors.DEEP_ORANGE_200),
                            margin=ft.Margin(bottom=20),
                        ),
                        ft.Column(option_buttons, spacing=10),
                        feedback,
                        ft.Container(expand=True),
                        ft.Button(
                            content=ft.Row([
                                ft.Text("Дальше" if current + 1 < total else "Завершить",
                                        color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.BOLD),
                                ft.Icon(ft.Icons.ARROW_FORWARD, color=ft.Colors.WHITE),
                            ], alignment=ft.MainAxisAlignment.CENTER, tight=True),
                            bgcolor=ft.Colors.DEEP_ORANGE_400 if answered else ft.Colors.GREY_400,
                            disabled=not answered,
                            height=55, width=float("inf"),
                            on_click=next_q, margin=ft.Margin(top=15),
                        )
                    ], expand=True),
                    padding=20, expand=True,
                )
            ]
        )

    # --- ПОДПИСКА + ОПЛАТА ---
    def open_payment_flow(tier_id, name, price):
        pstate = {"step": "method", "method": None, "promo": None,
                  "discount": 0.0, "error_msg": "", "txn": None}
        dlg = ft.AlertDialog(modal=True)

        def final_price():
            return max(0, int(round(price * (1 - pstate["discount"]))))

        def render():
            dlg.content = build()
            page.update()

        def close(e=None):
            page.pop_dialog()

        def set_step(step):
            pstate["step"] = step
            pstate["error_msg"] = ""
            render()

        def success_close(e=None):
            page.pop_dialog()
            page.views[-1] = subscription_view()
            page.update()

        def validate_card():
            num = "".join(c for c in card_num.value if c.isdigit())
            if len(num) != 16:
                return "Номер карты должен содержать 16 цифр"
            exp = card_exp.value.strip()
            if len(exp) != 5 or exp[2] != "/" or not (exp[:2].isdigit() and exp[3:].isdigit()):
                return "Срок действия в формате ММ/ГГ"
            mm = int(exp[:2])
            if mm < 1 or mm > 12:
                return "Неверный месяц"
            if not (len(card_cvv.value) == 3 and card_cvv.value.isdigit()):
                return "CVV — 3 цифры"
            if len(card_holder.value.strip()) < 3:
                return "Укажите имя держателя"
            return None

        def process_payment(e):
            err = validate_card()
            if err:
                pstate["error_msg"] = err
                render()
                return
            pstate["step"] = "processing"
            pstate["error_msg"] = ""
            render()

            def finish():
                time.sleep(1.8)
                success = random.random() < 0.85
                if success:
                    txn = state.add_transaction(
                        amount=final_price(), tier=tier_id,
                        method=pstate["method"], status="success",
                        promo=pstate["promo"],
                    )
                    state.license["tier"] = tier_id
                    state.save_license()
                    pstate["txn"] = txn
                    pstate["step"] = "success"
                else:
                    pstate["error_msg"] = "Банк отклонил платёж. Проверьте данные и попробуйте снова."
                    pstate["step"] = "error"
                render()

            threading.Thread(target=finish, daemon=True).start()

        card_num = card_exp = card_cvv = card_holder = None

        def build():
            step = pstate["step"]

            if step == "method":
                items = [
                    ft.Text(f"{TIERS[tier_id]['icon']} {name}", size=22, weight=ft.FontWeight.BOLD),
                    ft.Text(f"К оплате: {final_price()} ₽ / мес", size=18,
                            color=ft.Colors.BLUE_500, weight=ft.FontWeight.BOLD),
                ]
                if pstate["promo"]:
                    items.append(ft.Text(f"✅ Промокод {pstate['promo']}: −{int(pstate['discount']*100)}%",
                                         size=12, color=ft.Colors.GREEN_600))
                if pstate["error_msg"]:
                    items.append(ft.Text(pstate["error_msg"], size=12, color=ft.Colors.RED_500))
                items += [
                    ft.Divider(),
                    ft.Text("Выберите способ оплаты:", size=13, color=ft.Colors.GREY_600),
                    ft.Button(
                        content=ft.Row([ft.Icon(ft.Icons.CREDIT_CARD, color=ft.Colors.WHITE),
                                        ft.Text("Банковская карта", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)],
                                       alignment=ft.MainAxisAlignment.CENTER),
                        bgcolor=ft.Colors.BLUE_500, width=float("inf"), height=50,
                        on_click=lambda e: (pstate.update({"method": "card"}), set_step("card")),
                    ),
                    ft.Button(
                        content=ft.Row([ft.Icon(ft.Icons.PHONE_ANDROID, color=ft.Colors.WHITE),
                                        ft.Text("СБП (быстрый платёж)", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)],
                                       alignment=ft.MainAxisAlignment.CENTER),
                        bgcolor=ft.Colors.GREEN_500, width=float("inf"), height=50,
                        on_click=lambda e: (pstate.update({"method": "sbp"}), set_step("card")),
                    ),
                    ft.Row([
                        ft.TextButton("🎟 Промокод", on_click=lambda e: set_step("promo")),
                        ft.TextButton("Отмена", on_click=close),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ]
                return ft.Column(items, spacing=10, tight=True)

            if step == "card":
                card_num = ft.TextField(label="Номер карты", hint_text="1234 5678 9012 3456",
                                        keyboard_type=ft.KeyboardType.NUMBER, max_length=19,
                                        prefix_icon=ft.Icons.CREDIT_CARD)
                card_exp = ft.TextField(label="Срок", hint_text="ММ/ГГ", max_length=5, width=120)
                card_cvv = ft.TextField(label="CVV", hint_text="123", max_length=3, width=100,
                                        password=True, can_reveal_password=True)
                card_holder = ft.TextField(label="Держатель", hint_text="IVAN IVANOV",
                                            capitalization=ft.TextCapitalization.CHARACTERS)

                items = [
                    ft.Text(f"💳 Оплата {final_price()} ₽", size=18, weight=ft.FontWeight.BOLD),
                    ft.Text("Данные тестовые — реальные деньги не списываются",
                            size=11, color=ft.Colors.GREY_500, italic=True),
                    ft.Container(height=5),
                    card_num,
                    ft.Row([card_exp, card_cvv]),
                    card_holder,
                ]
                if pstate["error_msg"]:
                    items.append(ft.Container(
                        content=ft.Text(pstate["error_msg"], size=12, color=ft.Colors.RED_500),
                        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.RED), padding=10, border_radius=8,
                    ))
                items += [
                    ft.Button(
                        content=ft.Row([ft.Icon(ft.Icons.LOCK, color=ft.Colors.WHITE),
                                        ft.Text(f"Оплатить {final_price()} ₽", color=ft.Colors.WHITE,
                                                weight=ft.FontWeight.BOLD)],
                                       alignment=ft.MainAxisAlignment.CENTER),
                        bgcolor=ft.Colors.GREEN_600, width=float("inf"), height=50,
                        on_click=process_payment,
                    ),
                    ft.TextButton("← Назад", on_click=lambda e: set_step("method")),
                ]
                return ft.Column(items, spacing=8, tight=True)

            if step == "promo":
                promo_field = ft.TextField(label="Промокод", hint_text="WELCOME",
                                            capitalization=ft.TextCapitalization.CHARACTERS)

                def apply_promo(e):
                    code = promo_field.value.strip().upper()
                    if code in PROMO_CODES:
                        pstate["discount"] = PROMO_CODES[code]
                        pstate["promo"] = code
                        set_step("method")
                    else:
                        pstate["error_msg"] = "Промокод не найден"
                        render()

                items = [
                    ft.Text("🎟 Промокод", size=18, weight=ft.FontWeight.BOLD),
                    ft.Text("Попробуйте: WELCOME, STUDENT или FRIEND",
                            size=11, color=ft.Colors.GREY_500),
                    promo_field,
                ]
                if pstate["error_msg"]:
                    items.append(ft.Text(pstate["error_msg"], size=12, color=ft.Colors.RED_500))
                items += [
                    ft.Button(
                        content=ft.Text("Применить", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                        bgcolor=ft.Colors.PURPLE_400, width=float("inf"), height=45,
                        on_click=apply_promo,
                    ),
                    ft.TextButton("← Назад", on_click=lambda e: set_step("method")),
                ]
                return ft.Column(items, spacing=10, tight=True)

            if step == "processing":
                return ft.Column([
                    ft.Container(height=20),
                    ft.ProgressRing(width=60, height=60, stroke_width=4, color=ft.Colors.BLUE_500),
                    ft.Container(height=15),
                    ft.Text("Обработка платежа…", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text("Соединение с банком", size=12, color=ft.Colors.GREY_600),
                    ft.Container(height=20),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, tight=True)

            if step == "success":
                txn = pstate["txn"]
                return ft.Column([
                    ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_500, size=70),
                    ft.Text("Оплата успешна!", size=22, weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREEN_600, text_align=ft.TextAlign.CENTER),
                    ft.Container(height=10),
                    ft.Container(
                        content=ft.Column([
                            ft.Row([ft.Text("Тариф", size=13, color=ft.Colors.GREY_600),
                                    ft.Text(f"{TIERS[tier_id]['icon']} {name}", size=13,
                                            weight=ft.FontWeight.BOLD)],
                                   alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Row([ft.Text("Сумма", size=13, color=ft.Colors.GREY_600),
                                    ft.Text(f"{final_price()} ₽", size=13,
                                            weight=ft.FontWeight.BOLD)],
                                   alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Row([ft.Text("Способ", size=13, color=ft.Colors.GREY_600),
                                    ft.Text("Карта" if pstate["method"] == "card" else "СБП", size=13)],
                                   alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Row([ft.Text("Транзакция", size=13, color=ft.Colors.GREY_600),
                                    ft.Text(txn["txn_id"], size=13)],
                                   alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Divider(),
                            ft.Text("Чек отправлен на email", size=11, color=ft.Colors.GREY_500,
                                    text_align=ft.TextAlign.CENTER),
                        ], spacing=8),
                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                        padding=15, border_radius=12, width=float("inf"),
                    ),
                    ft.Button(
                        content=ft.Text("Понятно", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                        bgcolor=ft.Colors.GREEN_600, width=float("inf"), height=50,
                        on_click=success_close,
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10, tight=True)

            if step == "error":
                return ft.Column([
                    ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED_500, size=70),
                    ft.Text("Платёж не прошёл", size=22, weight=ft.FontWeight.BOLD,
                            color=ft.Colors.RED_500, text_align=ft.TextAlign.CENTER),
                    ft.Text(pstate["error_msg"], size=13, color=ft.Colors.GREY_700,
                            text_align=ft.TextAlign.CENTER),
                    ft.Container(height=10),
                    ft.Button(
                        content=ft.Text("Повторить", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                        bgcolor=ft.Colors.BLUE_500, width=float("inf"), height=50,
                        on_click=lambda e: set_step("card"),
                    ),
                    ft.TextButton("Отмена", on_click=close),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10, tight=True)

            return ft.Column([ft.Text("…")])

        render()
        page.show_dialog(dlg)

    def subscription_view():
        current_tier = state.license["tier"]

        def make_card(name, tier_id, price, features, color):
            is_current = (tier_id == current_tier)
            card_bg = (ft.Colors.with_opacity(0.1, color) if is_current
                       else ft.Colors.SURFACE_CONTAINER_HIGHEST)

            btn = ft.Button(
                content=ft.Text("Текущий план" if is_current else "Оформить",
                                color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=16),
                disabled=is_current,
                bgcolor=color if not is_current else ft.Colors.GREY_400,
                height=50, width=float("inf"),
                on_click=lambda e: open_payment_flow(tier_id, name, price),
            )
            return ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(f"{TIERS[tier_id]['icon']} {name}", size=22,
                                weight=ft.FontWeight.BOLD, expand=True),
                        ft.Container(content=ft.Icon(ft.Icons.DIAMOND, color=color, size=22),
                                     bgcolor=ft.Colors.with_opacity(0.2, color),
                                     padding=8, border_radius=20),
                    ]),
                    ft.Text(f"{price} ₽/мес" if price > 0 else "Бесплатно", size=28,
                            color=color, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.Column([
                        ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, color=color, size=18),
                                ft.Text(f, size=14, expand=True)])
                        for f in features
                    ]),
                    btn
                ], spacing=8),
                bgcolor=card_bg, border_radius=20, padding=25,
                margin=ft.Margin(bottom=15),
                border=ft.Border.all(2, color),
            )

        txns = state.progress.get("transactions", [])[-3:]
        history_block = ft.Container()
        if txns:
            history_items = []
            for t in reversed(txns):
                history_items.append(
                    ft.Row([
                        ft.Text(t["txn_id"], size=11, color=ft.Colors.GREY_600),
                        ft.Text(f"{t['amount']} ₽", size=11, weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREEN_600),
                        ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_500, size=14),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                )
            history_block = ft.Container(
                content=ft.Column([
                    ft.Text("Последние транзакции", size=13, weight=ft.FontWeight.BOLD),
                    ft.Divider(height=1),
                    *history_items,
                ], spacing=6),
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                padding=15, border_radius=15, margin=ft.Margin(top=10, bottom=15),
            )

        return ft.View(
            controls=[
                ft.AppBar(title=ft.Text("Подписка"), bgcolor=ft.Colors.TRANSPARENT,
                          leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/"))),
                ft.Container(
                    content=ft.Column([
                        make_card("Бесплатный", "free", 0,
                                  ["30 карточек в день", "Базовый раздел"],
                                  ft.Colors.GREY_600),
                        make_card("Плюс", "plus", 199,
                                  ["500 карточек в день", "Все разделы", "Продвинутый уровень"],
                                  ft.Colors.BLUE_500),
                        make_card("Премиум", "premium", 499,
                                  ["Безлимит карточек", "Экспорт прогресса", "Приоритетная поддержка"],
                                  ft.Colors.AMBER_600),
                        history_block,
                    ], scroll=ft.ScrollMode.AUTO, expand=True,
                       horizontal_alignment=ft.CrossAxisAlignment.STRETCH),
                    padding=20, expand=True
                )
            ]
        )

    # --- ПОИСК / ИЗБРАННОЕ / СТАТИСТИКА ---
    def search_view():
        results_list = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True,
                                 horizontal_alignment=ft.CrossAxisAlignment.STRETCH)

        def on_search(e):
            results_list.controls.clear()
            query = e.control.value.lower()
            if not query:
                page.update()
                return
            found = [w for w in all_words_flat()
                     if query in w["en"].lower() or query in w["ru"].lower()][:30]
            for w in found:
                tinfo = TYPE_INFO.get(w.get("type", "word"), TYPE_INFO["word"])
                results_list.controls.append(
                    ft.Container(content=ft.ListTile(
                        leading=ft.Container(content=ft.Text(tinfo["emoji"], size=22),
                                             width=40, height=40, alignment=ft.Alignment.CENTER,
                                             bgcolor=ft.Colors.with_opacity(0.15, tinfo["color"]),
                                             border_radius=10),
                        title=ft.Text(w["en"], weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(w["ru"])),
                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                        border_radius=15, padding=5,
                        border=ft.Border.all(1, ft.Colors.BLUE_200))
                )
            page.update()

        return ft.View(
            controls=[
                ft.AppBar(title=ft.Text("Поиск"), bgcolor=ft.Colors.TRANSPARENT,
                          leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/"))),
                ft.Container(content=ft.Column([
                    ft.TextField(hint_text="Введите слово или перевод…", on_change=on_search,
                                 prefix_icon=ft.Icons.SEARCH, border_radius=15, filled=True,
                                 focused_border_color=ft.Colors.BLUE_500),
                    ft.Container(height=10),
                    results_list,
                ], expand=True), padding=20, expand=True)
            ],
            navigation_bar=ft.NavigationBar(
                destinations=[
                    ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Главная"),
                    ft.NavigationBarDestination(icon=ft.Icons.SEARCH, label="Поиск"),
                    ft.NavigationBarDestination(icon=ft.Icons.FAVORITE, label="Избранное"),
                    ft.NavigationBarDestination(icon=ft.Icons.SUPPORT_AGENT, label="Поддержка"),
                ],
                selected_index=1,
                on_change=lambda e: navigate(["/", "/search", "/favorites", "/support"][e.control.selected_index])
            )
        )

    def favorites_view():
        fav_words = [w for w in all_words_flat() if w["en"] in state.progress["favorites"]]
        items = [
            ft.Container(content=ft.ListTile(
                leading=ft.Icon(ft.Icons.FAVORITE, color=ft.Colors.RED_400, size=20),
                title=ft.Text(w["en"], weight=ft.FontWeight.BOLD),
                subtitle=ft.Text(w["ru"])),
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                border_radius=15, padding=5, margin=ft.Margin(bottom=5),
                border=ft.Border.all(1, ft.Colors.PINK_200))
            for w in fav_words
        ] if fav_words else [
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.FAVORITE_BORDER, size=60, color=ft.Colors.GREY_400),
                    ft.Text("Вы пока не добавили карточки в избранное",
                            color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER),
                    ft.Text("Открывайте карточки и нажимайте ❤",
                            color=ft.Colors.GREY_500, size=12, text_align=ft.TextAlign.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=40,
            )
        ]
        return ft.View(
            controls=[
                ft.AppBar(title=ft.Text("Избранное"), bgcolor=ft.Colors.TRANSPARENT,
                          leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/"))),
                ft.Container(content=ft.Column(
                    items, scroll=ft.ScrollMode.AUTO, expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH),
                    padding=20, expand=True)
            ],
            navigation_bar=ft.NavigationBar(
                destinations=[
                    ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Главная"),
                    ft.NavigationBarDestination(icon=ft.Icons.SEARCH, label="Поиск"),
                    ft.NavigationBarDestination(icon=ft.Icons.FAVORITE, label="Избранное"),
                    ft.NavigationBarDestination(icon=ft.Icons.SUPPORT_AGENT, label="Поддержка"),
                ],
                selected_index=2,
                on_change=lambda e: navigate(["/", "/search", "/favorites", "/support"][e.control.selected_index])
            )
        )

    def stats_view():
        known_count = len(state.progress["known"])
        total_count = len(all_words_flat())
        streak = state.progress.get("streak", 0)
        quiz_history = state.progress.get("quiz_history", [])
        total_quizzes = len(quiz_history)
        total_correct = sum(q["score"] for q in quiz_history)
        total_questions = sum(q["total"] for q in quiz_history)
        accuracy = int(total_correct / total_questions * 100) if total_questions > 0 else 0

        def stat_card(emoji, title, value, color):
            return ft.Container(
                content=ft.ListTile(
                    leading=ft.Container(content=ft.Text(emoji, size=26),
                                         width=50, height=50, alignment=ft.Alignment.CENTER,
                                         bgcolor=ft.Colors.with_opacity(0.2, color),
                                         border_radius=12),
                    title=ft.Text(title, weight=ft.FontWeight.BOLD),
                    subtitle=ft.Text(value)),
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                border_radius=15, margin=5,
                border=ft.Border.all(1, ft.Colors.with_opacity(0.3, color))
            )

        return ft.View(
            controls=[
                ft.AppBar(title=ft.Text("Статистика"), bgcolor=ft.Colors.TRANSPARENT,
                          leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/"))),
                ft.Container(
                    content=ft.Column([
                        stat_card("🔥", "Серия дней", f"{streak} дн.", ft.Colors.ORANGE_500),
                        stat_card("📖", "Изучено карточек", f"{known_count} из {total_count}", ft.Colors.BLUE_500),
                        stat_card("⭐", "В избранном", str(len(state.progress["favorites"])), ft.Colors.PINK_500),
                        stat_card("🧠", "Пройдено тестов", str(total_quizzes), ft.Colors.DEEP_ORANGE_400),
                        stat_card("🎯", "Средний результат", f"{accuracy}%", ft.Colors.GREEN_600),
                    ], scroll=ft.ScrollMode.AUTO, expand=True,
                       horizontal_alignment=ft.CrossAxisAlignment.STRETCH),
                    padding=20, expand=True
                )
            ],
            navigation_bar=ft.NavigationBar(
                destinations=[
                    ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Главная"),
                    ft.NavigationBarDestination(icon=ft.Icons.SEARCH, label="Поиск"),
                    ft.NavigationBarDestination(icon=ft.Icons.FAVORITE, label="Избранное"),
                    ft.NavigationBarDestination(icon=ft.Icons.SUPPORT_AGENT, label="Поддержка"),
                ],
                selected_index=3,
                on_change=lambda e: navigate(["/", "/search", "/favorites", "/support"][e.control.selected_index])
            )
        )

    navigate("/")


ft.run(main)
