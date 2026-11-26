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
         "a": "На главном экране нажмите на голубую карточку тарифа сверху или перейдите в раздел «Подписка»."},
        {"q": "Какие тарифы доступны?",
         "a": "🆓 Бесплатный — 30 карточек в день.\n⭐ Плюс — 199 ₽/мес.\n👑 Премиум — 499 ₽/мес."},
        {"q": "Есть ли пробный период?",
         "a": "Да, 7 дней тарифа Плюс при первом запуске."},
        {"q": "Какие промокоды есть?",
         "a": "🎟 WELCOME (−10%), STUDENT (−20%), FRIEND (−15%)."},
    ],
    "📱 Использование": [
        {"q": "Как добавить в избранное?",
         "a": "Откройте карточку и нажмите ❤ в правом верхнем углу."},
        {"q": "Как посмотреть перевод?",
         "a": "Нажмите «Показать перевод» на карточке."},
        {"q": "Что такое серия дней?",
         "a": "🔥 Сколько дней подряд вы заходите в приложение."},
        {"q": "Как пройти тест?",
         "a": "Откройте подраздел и нажмите 🧠 в правом верхнем углу на экране карточек."},
    ],
    "🇬🇧 Изучение": [
        {"q": "С чего начать?",
         "a": "С раздела «База»: буквы, числа, цвета, местоимения."},
        {"q": "Что такое IPA-транскрипция?",
         "a": "International Phonetic Alphabet. Запись [ˈæp.əl] — произношение."},
        {"q": "Как эффективно запоминать?",
         "a": "10–15 карточек в день, повтор через 1/3/7 дней, проверка в квизах."},
    ],
}

OPTION_COLORS = [
    ft.Colors.BLUE_100, ft.Colors.PURPLE_100,
    ft.Colors.ORANGE_100, ft.Colors.TEAL_100,
]

TYPE_INFO = {
    "letter":       {"emoji": "📖", "label": "БУКВА",        "color": ft.Colors.BLUE_400},
    "word":         {"emoji": "📝", "label": "СЛОВО",        "color": ft.Colors.GREEN_600},
    "phrase":       {"emoji": "💬", "label": "ФРАЗА",        "color": ft.Colors.PURPLE_400},
    "sentence":     {"emoji": "🗨️", "label": "ПРЕДЛОЖЕНИЕ",  "color": ft.Colors.ORANGE_500},
    "idiom":        {"emoji": "🎭", "label": "ИДИОМА",       "color": ft.Colors.PINK_400},
    "phrasal_verb": {"emoji": "🔗", "label": "ФРАЗ. ГЛАГОЛ", "color": ft.Colors.TEAL_500},
    "slang":        {"emoji": "😎", "label": "СЛЕНГ",        "color": ft.Colors.AMBER_700},
}

PROMO_CODES = {"WELCOME": 0.10, "STUDENT": 0.20, "FRIEND": 0.15}


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
    page.spacing = 0
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)

    state.record_activity()

    def wrap(content):
        """Простая обёртка без SafeArea - только padding."""
        return ft.Container(
            content=content,
            padding=ft.Padding(left=14, right=14, top=8, bottom=12),
            expand=True,
        )

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
            lock_icon = (ft.Icon(ft.Icons.LOCK, color=ft.Colors.RED, size=20)
                         if is_locked
                         else ft.Icon(ft.Icons.CHEVRON_RIGHT, color=ft.Colors.GREY_400, size=20))

            section_cards.append(
                ft.Container(
                    content=ft.ListTile(
                        leading=ft.Container(
                            content=ft.Text(item["icon"], size=24),
                            bgcolor=ft.Colors.with_opacity(0.25, accent),
                            border_radius=12, width=44, height=44,
                            alignment=ft.Alignment.CENTER
                        ),
                        title=ft.Text(name, weight=ft.FontWeight.BOLD, size=15),
                        subtitle=ft.Text(item["desc"], color=ft.Colors.GREY_600, size=11,
                                         max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                        trailing=lock_icon,
                    ),
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                    border=ft.Border.all(2, accent),
                    border_radius=16,
                    margin=ft.Margin(bottom=10),
                    on_click=lambda e, n=name, locked=is_locked: open_section(n, locked)
                )
            )

        continue_card = ft.Container()
        last_section = state.progress.get("last_section")
        last_subsection = state.progress.get("last_subsection")
        if last_section and last_subsection and last_section in DATA:
            accent = DATA[last_section].get("color", "#7c9cf5")
            continue_card = ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.PLAY_ARROW, color=ft.Colors.WHITE, size=22),
                        width=42, height=42,
                        alignment=ft.Alignment.CENTER,
                        bgcolor=ft.Colors.with_opacity(0.25, ft.Colors.WHITE),
                        border_radius=12,
                    ),
                    ft.Column([
                        ft.Text("Продолжить", weight=ft.FontWeight.BOLD, size=13,
                                color=ft.Colors.WHITE),
                        ft.Text(f"{last_section} · {last_subsection}", size=11,
                                color=ft.Colors.WHITE_70,
                                max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                    ], spacing=2, expand=True),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT, color=ft.Colors.WHITE, size=20),
                ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor=accent, padding=12,
                border_radius=16, margin=ft.Margin(bottom=10),
                on_click=lambda e: continue_learning()
            )

        header_card = ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text(f"{tier['icon']} {tier['name']}",
                            weight=ft.FontWeight.BOLD, size=15),
                    ft.Text("Управление подпиской", size=11, color=ft.Colors.WHITE_70),
                ], expand=True, spacing=2),
                ft.Icon(ft.Icons.DIAMOND, color=ft.Colors.ORANGE_400, size=26)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
               vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.BLUE_600, padding=14,
            border_radius=16, margin=ft.Margin(bottom=10),
            on_click=lambda e: navigate("/subscription")
        )

        quiz_card = ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Text("🧠", size=26),
                    width=48, height=48,
                    alignment=ft.Alignment.CENTER,
                    bgcolor=ft.Colors.with_opacity(0.25, ft.Colors.WHITE),
                    border_radius=12,
                ),
                ft.Column([
                    ft.Text("Тесты и квизы", weight=ft.FontWeight.BOLD, size=15,
                            color=ft.Colors.WHITE),
                    ft.Text("Проверьте свои знания", size=11, color=ft.Colors.WHITE_70),
                ], spacing=2, expand=True),
                ft.Icon(ft.Icons.CHEVRON_RIGHT, color=ft.Colors.WHITE, size=20),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
               vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.DEEP_ORANGE_400, padding=14,
            border_radius=16, margin=ft.Margin(bottom=14),
            on_click=lambda e: navigate("/quiz_select")
        )

        body = ft.Column([
            header_card,
            continue_card,
            quiz_card,
            ft.Text("Разделы", size=17, weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREY_800),
            ft.Container(height=6),
            ft.Column(section_cards, spacing=0),
        ], spacing=0, scroll=ft.ScrollMode.AUTO, expand=True)

        return ft.View(
            controls=[
                ft.AppBar(
                    title=ft.Text("Perfect English", weight=ft.FontWeight.BOLD, size=17),
                    bgcolor=ft.Colors.TRANSPARENT,
                    actions=[
                        ft.IconButton(ft.Icons.BAR_CHART, tooltip="Статистика",
                                      icon_color=ft.Colors.PURPLE_400,
                                      on_click=lambda e: navigate("/stats")),
                        ft.IconButton(ft.Icons.BRIGHTNESS_6, icon_color=ft.Colors.ORANGE_400,
                                      on_click=toggle_theme)
                    ]
                ),
                wrap(body),
            ],
            navigation_bar=ft.NavigationBar(
                destinations=[
                    ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Главная"),
                    ft.NavigationBarDestination(icon=ft.Icons.SEARCH, label="Поиск"),
                    ft.NavigationBarDestination(icon=ft.Icons.FAVORITE, label="Избранное"),
                    ft.NavigationBarDestination(icon=ft.Icons.SUPPORT_AGENT, label="Поддержка"),
                ],
                on_change=lambda e: navigate(["/", "/search", "/favorites", "/support"][e.control.selected_index])
            ),
            padding=0, spacing=0
        )

    # --- ТЕХПОДДЕРЖКА ---
    def get_bot_response(text: str) -> str:
        t = text.lower()
        rules = [
            (["привет", "здравств", "hello", "hi"],
             "👋 Здравствуйте! Задайте вопрос или выберите тему ниже."),
            (["тест", "квиз", "quiz"],
             "🧠 Откройте подраздел и нажмите 🧠 в правом верхнем углу на экране карточек."),
            (["оплат", "купить", "подписк", "тариф"],
             "💳 Раздел «Подписка» или голубая карточка на главной.\n⭐ Плюс 199 ₽, 👑 Премиум 499 ₽."),
            (["промокод", "скидк"],
             "🎟 WELCOME (−10%), STUDENT (−20%), FRIEND (−15%)"),
            (["перевод", "перевест"],
             "🔍 Нажмите «Показать перевод» на карточке."),
            (["баг", "ошибк", "не работает"],
             "⚠ Опишите, что произошло — передадим в разработку."),
            (["возврат", "вернуть"],
             "💸 Возврат — 14 дней. support@perfectenglish.app"),
            (["слов", "карточк", "учить"],
             "📚 10–15 карточек в день, повтор через 1/3/7 дней."),
            (["ipa", "транскрипц"],
             "🔊 IPA: apple [ˈæp.əl]."),
            (["статистик", "прогресс"],
             "📊 По иконке 📈 в верхней панели."),
            (["избранн", "любим"],
             "❤ Нажмите ❤ в правом верхнем углу карточки."),
            (["поиск", "найти"],
             "🔍 В нижней вкладке «Поиск»."),
            (["офлайн", "интернет"],
             "📴 Работает офлайн."),
            (["спасиб", "thanks"],
             "😊 Всегда рады помочь!"),
        ]
        for keywords, response in rules:
            if any(k in t for k in keywords):
                return response
        return "🤔 Передал оператору. А пока загляните в ❓ FAQ!"

    def support_view():
        messages_list = ft.ListView(expand=True, spacing=10, padding=12, auto_scroll=True)

        def make_bubble_row(msg):
            is_user = msg["is_user"]
            bubble = ft.Container(
                content=ft.Text(msg["text"],
                                color=ft.Colors.WHITE if is_user else ft.Colors.BLACK,
                                size=13),
                bgcolor=ft.Colors.BLUE_500 if is_user else ft.Colors.GREY_200,
                padding=10,
                border_radius=ft.BorderRadius(
                    top_left=13, top_right=13,
                    bottom_left=13 if is_user else 0,
                    bottom_right=0 if is_user else 13
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
                                    ft.ProgressRing(width=12, height=12, stroke_width=2,
                                                    color=ft.Colors.BLUE_400),
                                    ft.Text("печатает…", size=11, color=ft.Colors.GREY_600, italic=True)
                                ], spacing=6),
                                bgcolor=ft.Colors.GREY_200, padding=10,
                                border_radius=ft.BorderRadius(top_left=13, top_right=13,
                                                              bottom_left=0, bottom_right=13),
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
        input_field = ft.TextField(
            hint_text="Введите сообщение…",
            expand=True,
            border_radius=22,
            on_submit=send_message,
            content_padding=ft.Padding(left=14, right=14, top=10, bottom=10),
            text_size=13,
        )

        def make_chip(label, text, color):
            return ft.Chip(
                label=ft.Text(label, size=11, color=ft.Colors.WHITE),
                bgcolor=color,
                on_click=lambda e: send_text(text),
            )

        quick_replies = ft.Container(
            content=ft.ListView(
                controls=[
                    make_chip("🧠 Тесты", "Как пройти тест?", ft.Colors.DEEP_ORANGE_400),
                    make_chip("💳 Подписка", "Как оформить подписку?", ft.Colors.BLUE_400),
                    make_chip("🎟 Промокод", "Какие есть промокоды?", ft.Colors.PURPLE_400),
                    make_chip("💸 Возврат", "Хочу вернуть деньги", ft.Colors.RED_400),
                    make_chip("🔍 Перевод", "Как посмотреть перевод?", ft.Colors.INDIGO_400),
                    make_chip("❓ FAQ", "faq", ft.Colors.TEAL_500),
                ],
                spacing=8, horizontal=True, height=42,
            ),
            padding=ft.Padding(left=10, right=10, top=6, bottom=4),
        )

        input_row = ft.Container(
            content=ft.Row([
                input_field,
                ft.Container(
                    content=ft.Icon(ft.Icons.SEND, color=ft.Colors.WHITE, size=18),
                    bgcolor=ft.Colors.BLUE_500,
                    width=42, height=42,
                    border_radius=21,
                    alignment=ft.Alignment.CENTER,
                    on_click=send_message
                )
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.Padding(left=10, right=10, top=8, bottom=8),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        )

        body = ft.Column([messages_list, quick_replies, input_row],
                         spacing=0, expand=True)

        return ft.View(
            controls=[
                ft.AppBar(
                    title=ft.Text("Техподдержка", size=17),
                    bgcolor=ft.Colors.TRANSPARENT,
                    leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/")),
                    actions=[ft.IconButton(ft.Icons.HELP_OUTLINE, icon_color=ft.Colors.TEAL_500,
                                           tooltip="Частые вопросы",
                                           on_click=lambda e: navigate("/faq"))]
                ),
                ft.Container(content=body, expand=True),
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
            ),
            padding=0, spacing=0
        )

    # --- FAQ ---
    def faq_view():
        expanded = {}
        faq_list = ft.Column(spacing=6, expand=True,
                             horizontal_alignment=ft.CrossAxisAlignment.STRETCH)

        def render_faq():
            faq_list.controls.clear()
            for category, questions in FAQ_DATA.items():
                faq_list.controls.append(
                    ft.Container(content=ft.Text(category, size=14, weight=ft.FontWeight.BOLD),
                                 margin=ft.Margin(top=10, bottom=4, left=2))
                )
                for i, item in enumerate(questions):
                    key = f"{category}#{i}"
                    is_open = expanded.get(key, False)
                    faq_list.controls.append(
                        ft.Container(
                            content=ft.Column([
                                ft.Container(
                                    content=ft.Row([
                                        ft.Text(item["q"], weight=ft.FontWeight.W_600,
                                                size=13, expand=True),
                                        ft.Icon(ft.Icons.EXPAND_LESS if is_open else ft.Icons.EXPAND_MORE,
                                                color=ft.Colors.BLUE, size=18),
                                    ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                                    padding=12,
                                    on_click=lambda e, k=key: toggle_faq(k),
                                ),
                                ft.Container(
                                    content=ft.Text(item["a"], size=12, color=ft.Colors.GREY_700),
                                    padding=ft.Padding(left=12, right=12, bottom=12, top=0),
                                    visible=is_open,
                                ),
                            ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.STRETCH),
                            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                            border_radius=12,
                        )
                    )
            page.update()

        def toggle_faq(key):
            expanded[key] = not expanded.get(key, False)
            render_faq()

        render_faq()

        banner = ft.Container(
            content=ft.Row([
                ft.Container(content=ft.Icon(ft.Icons.SUPPORT_AGENT, color=ft.Colors.WHITE, size=20),
                             bgcolor=ft.Colors.BLUE_500, padding=7, border_radius=10),
                ft.Column([
                    ft.Text("Не нашли ответ?", weight=ft.FontWeight.BOLD, size=12),
                    ft.Text("Задайте вопрос в поддержке", size=11, color=ft.Colors.GREY_600),
                ], spacing=2, expand=True),
                ft.Icon(ft.Icons.CHEVRON_RIGHT, color=ft.Colors.GREY_400, size=20),
            ]),
            bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.BLUE),
            padding=10, border_radius=12, margin=ft.Margin(bottom=8),
            on_click=lambda e: navigate("/support"),
        )

        body = ft.Column([banner, faq_list], expand=True, spacing=0, scroll=ft.ScrollMode.AUTO)

        return ft.View(
            controls=[
                ft.AppBar(title=ft.Text("Частые вопросы", weight=ft.FontWeight.BOLD, size=17),
                          bgcolor=ft.Colors.TRANSPARENT,
                          leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/support"))),
                wrap(body),
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
            ),
            padding=0, spacing=0
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
        subs_list = ft.Column(spacing=8, expand=True,
                              horizontal_alignment=ft.CrossAxisAlignment.STRETCH)

        def render_subs(query=""):
            subs_list.controls.clear()
            for sub_name, sub_item in item["subsections"].items():
                if query and query.lower() not in sub_name.lower():
                    continue
                kind = sub_item.get("kind", "word")
                info = TYPE_INFO.get(kind, TYPE_INFO["word"])

                # Чистая карточка: только иконка + название + шеврон
                subs_list.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Container(
                                content=ft.Text(info["emoji"], size=20),
                                width=42, height=42,
                                alignment=ft.Alignment.CENTER,
                                bgcolor=ft.Colors.with_opacity(0.15, accent),
                                border_radius=12,
                            ),
                            ft.Text(sub_name, weight=ft.FontWeight.W_600, size=14,
                                    expand=True, max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS),
                            ft.Icon(ft.Icons.CHEVRON_RIGHT, color=ft.Colors.GREY_400, size=20),
                        ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                        padding=10,
                        border_radius=14,
                        margin=ft.Margin(bottom=8),
                        on_click=lambda e, n=sub_name, i=sub_item: open_flashcards(n, i),
                    )
                )
            page.update()

        render_subs()

        body = ft.Column([
            ft.TextField(
                hint_text="Поиск по темам…",
                prefix_icon=ft.Icons.SEARCH,
                on_change=lambda e: render_subs(e.control.value),
                border_radius=14, filled=True,
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                border_color=ft.Colors.TRANSPARENT,
                text_size=13,
                content_padding=ft.Padding(left=14, right=14, top=10, bottom=10),
            ),
            ft.Container(height=6),
            subs_list,
        ], expand=True, spacing=0)

        return ft.View(
            controls=[
                ft.AppBar(title=ft.Text(name, weight=ft.FontWeight.BOLD, size=16,
                                        max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                          bgcolor=ft.Colors.TRANSPARENT,
                          leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/"))),
                wrap(body),
            ],
            padding=0, spacing=0
        )

    # --- КАРТОЧКИ ---
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
        font_size = 36 if len(en_word) <= 12 else (28 if len(en_word) <= 20 else 22)

        def start_test(e):
            words = current_cards_data["words"]
            title = current_cards_data["title"]
            if len(words) < 4:
                page.show_dialog(ft.AlertDialog(
                    title=ft.Text("Мало карточек"),
                    content=ft.Text(f"Для теста нужно минимум 4 карточки."),
                    actions=[ft.TextButton("Ок", on_click=lambda e: page.pop_dialog())]
                ))
                return
            questions = build_quiz(words)
            if not questions:
                return
            current_quiz.update({"questions": questions, "current": 0, "score": 0,
                                 "section_name": title, "selected_idx": None})
            navigate("/quiz")

        def next_word(e):
            if not state.can_see_more():
                limit = TIERS[state.license["tier"]]["limit"]
                tier_name = TIERS[state.license["tier"]]["name"]
                page.show_dialog(ft.AlertDialog(
                    title=ft.Text("Дневной лимит"),
                    content=ft.Text(
                        f"На тарифе «{tier_name}» — {limit} карточек в день.\n\n"
                        "Лимит обновится завтра или оформите подписку Плюс/Премиум."
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

        # Содержимое карточки (скроллится)
        card_items = [
            ft.Container(
                content=ft.Text(f"{tinfo['emoji']} {tinfo['label']}", size=10,
                                weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                bgcolor=tinfo["color"],
                padding=ft.Padding(left=10, right=10, top=5, bottom=5),
                border_radius=13,
            ),
            ft.Container(height=14),
            ft.Text(en_word, size=font_size, weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER),
            ft.Text(f"[{word['ipa']}]", size=14, color=ft.Colors.GREY_600,
                    italic=True, text_align=ft.TextAlign.CENTER),
        ]

        if word.get("example"):
            card_items += [
                ft.Container(height=10),
                ft.Container(
                    content=ft.Text(f"💡 {word['example']}", size=12,
                                    color=ft.Colors.GREY_700, italic=True,
                                    text_align=ft.TextAlign.CENTER),
                    bgcolor=ft.Colors.with_opacity(0.08, tinfo["color"]),
                    padding=10, border_radius=10, width=float("inf"),
                ),
            ]

        card_items += [
            ft.Container(height=12),
            ft.Container(
                content=ft.Text("─" * 20, color=ft.Colors.GREY_300,
                                text_align=ft.TextAlign.CENTER, size=12),
                margin=ft.Margin(bottom=8),
            ),
        ]

        if show:
            card_items.append(
                ft.Column([
                    ft.Text(word["ru"], size=22, weight=ft.FontWeight.BOLD,
                            color=tinfo["color"], text_align=ft.TextAlign.CENTER),
                    ft.Container(height=4),
                    ft.TextButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.VISIBILITY_OFF, size=13, color=ft.Colors.GREY_500),
                            ft.Text("Скрыть", size=11, color=ft.Colors.GREY_500),
                        ], alignment=ft.MainAxisAlignment.CENTER, tight=True),
                        on_click=toggle_translation,
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
            )
        else:
            card_items.append(
                ft.Button(
                    content=ft.Row([
                        ft.Icon(ft.Icons.VISIBILITY, color=ft.Colors.WHITE, size=16),
                        ft.Text("Показать перевод", color=ft.Colors.WHITE, size=13),
                    ], alignment=ft.MainAxisAlignment.CENTER, tight=True),
                    bgcolor=tinfo["color"],
                    on_click=toggle_translation,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=12),
                        padding=ft.Padding(left=16, right=16, top=12, bottom=12),
                    ),
                )
            )

        def nav_btn(icon, color, size, on_click, diameter):
            return ft.Container(
                content=ft.Icon(icon, color=ft.Colors.WHITE, size=size),
                bgcolor=color,
                width=diameter, height=diameter,
                border_radius=diameter // 2,
                alignment=ft.Alignment.CENTER,
                on_click=on_click,
            )

        main_col = ft.Column([
            ft.ProgressBar(
                value=(idx + 1) / total,
                height=4,
                color=tinfo["color"],
                bgcolor=ft.Colors.GREY_200,
            ),
            ft.Container(height=6),
            ft.Text(f"{idx + 1} / {total}", size=11, color=ft.Colors.GREY_600,
                    weight=ft.FontWeight.W_500, text_align=ft.TextAlign.CENTER),
            ft.Container(height=6),
            ft.Container(
                content=ft.Column(
                    card_items,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=4,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                ),
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                border_radius=24, padding=16,
                shadow=ft.BoxShadow(
                    blur_radius=28,
                    color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                    offset=ft.Offset(0, 8),
                ),
                expand=True,
            ),
            ft.Container(height=12),
            ft.Row([
                nav_btn(ft.Icons.ARROW_BACK_IOS, ft.Colors.INDIGO_400, 22, prev_word, 44),
                ft.Container(
                    content=ft.Row([
                        nav_btn(ft.Icons.CLOSE, ft.Colors.RED_400, 28, next_word, 54),
                        nav_btn(ft.Icons.CHECK, ft.Colors.GREEN_500, 28, mark_known, 54),
                    ], spacing=26, alignment=ft.MainAxisAlignment.CENTER),
                    expand=True,
                ),
                nav_btn(ft.Icons.ARROW_FORWARD_IOS, ft.Colors.INDIGO_400, 22, next_word, 44),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
               vertical_alignment=ft.CrossAxisAlignment.CENTER),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
           expand=True, spacing=0)

        return ft.View(
            controls=[
                ft.AppBar(
                    title=ft.Text(current_cards_data["title"], size=15,
                                  max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                    bgcolor=ft.Colors.TRANSPARENT,
                    leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/section")),
                    actions=[
                        ft.IconButton(ft.Icons.QUIZ, icon_color=ft.Colors.DEEP_ORANGE_400,
                                      tooltip="Пройти тест", on_click=start_test),
                        ft.IconButton(ft.Icons.SHUFFLE, icon_color=ft.Colors.INDIGO_400,
                                      tooltip="Перемешать", on_click=shuffle_cards),
                        ft.IconButton(ft.Icons.FAVORITE if is_fav else ft.Icons.FAVORITE_BORDER,
                                      icon_color=ft.Colors.RED if is_fav else ft.Colors.GREY,
                                      on_click=toggle_fav),
                    ]
                ),
                wrap(main_col),
            ],
            padding=0, spacing=0
        )

    # --- КВИЗЫ ---
    current_quiz = {"questions": [], "current": 0, "score": 0, "section_name": "", "selected_idx": None}

    def quiz_select_view():
        cards = []
        all_words = all_words_flat()
        cards.append(
            ft.Container(
                content=ft.Row([
                    ft.Container(content=ft.Text("🎲", size=26), width=48, height=48,
                                 alignment=ft.Alignment.CENTER,
                                 bgcolor=ft.Colors.with_opacity(0.25, ft.Colors.WHITE),
                                 border_radius=12),
                    ft.Column([
                        ft.Text("Случайный тест", weight=ft.FontWeight.BOLD, size=15,
                                color=ft.Colors.WHITE),
                        ft.Text("Из всех разделов", size=11, color=ft.Colors.WHITE_70),
                    ], spacing=2, expand=True),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT, color=ft.Colors.WHITE, size=20),
                ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor=ft.Colors.DEEP_ORANGE_400, padding=12,
                border_radius=14, margin=ft.Margin(bottom=8),
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
                        ft.Container(content=ft.Text(item["icon"], size=22), width=48, height=48,
                                     alignment=ft.Alignment.CENTER,
                                     bgcolor=ft.Colors.with_opacity(0.25, accent),
                                     border_radius=12),
                        ft.Text(name, weight=ft.FontWeight.BOLD, size=14,
                                expand=True, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                        ft.Icon(ft.Icons.CHEVRON_RIGHT,
                                color=accent if has_enough else ft.Colors.GREY_400, size=20),
                    ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                    border=ft.Border.all(2, accent if has_enough else ft.Colors.GREY_300),
                    padding=12, border_radius=14, margin=ft.Margin(bottom=8),
                    on_click=lambda e, w=words, n=name, ok=has_enough: (
                        start_quiz_by_words(w, n) if ok else None
                    ),
                )
            )

        body = ft.Column([
            ft.Text("🧠 Выберите тему", size=17, weight=ft.FontWeight.BOLD,
                    color=ft.Colors.DEEP_ORANGE_400),
            ft.Text("До 10 случайных вопросов", size=11, color=ft.Colors.GREY_600),
            ft.Container(height=10),
            ft.Column(cards, spacing=0),
        ], spacing=0, scroll=ft.ScrollMode.AUTO, expand=True)

        return ft.View(
            controls=[
                ft.AppBar(title=ft.Text("Тесты", weight=ft.FontWeight.BOLD, size=17),
                          bgcolor=ft.Colors.TRANSPARENT,
                          leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/"))),
                wrap(body),
            ],
            navigation_bar=ft.NavigationBar(
                destinations=[
                    ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Главная"),
                    ft.NavigationBarDestination(icon=ft.Icons.SEARCH, label="Поиск"),
                    ft.NavigationBarDestination(icon=ft.Icons.FAVORITE, label="Избранное"),
                    ft.NavigationBarDestination(icon=ft.Icons.SUPPORT_AGENT, label="Поддержка"),
                ],
                on_change=lambda e: navigate(["/", "/search", "/favorites", "/support"][e.control.selected_index])
            ),
            padding=0, spacing=0
        )

    def start_quiz_by_words(words_pool, title):
        if len(words_pool) < 4:
            page.show_dialog(ft.AlertDialog(
                title=ft.Text("Мало карточек"),
                content=ft.Text(f"Для теста нужно минимум 4 карточки."),
                actions=[ft.TextButton("Ок", on_click=lambda e: page.pop_dialog())]
            ))
            return
        questions = build_quiz(words_pool)
        if not questions:
            return
        current_quiz.update({"questions": questions, "current": 0, "score": 0,
                             "section_name": title, "selected_idx": None})
        navigate("/quiz")

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

        result_card = ft.Container(
            content=ft.Column([
                ft.Text(emoji, size=56, text_align=ft.TextAlign.CENTER),
                ft.Text(msg, size=22, weight=ft.FontWeight.BOLD, color=color,
                        text_align=ft.TextAlign.CENTER),
                ft.Container(height=6),
                ft.Text(f"{score} из {total}", size=26, weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER),
                ft.Text(f"Правильных: {pct}%", size=12, color=ft.Colors.GREY_600,
                        text_align=ft.TextAlign.CENTER),
                ft.Container(height=4),
                ft.Text(f"Тема: {current_quiz['section_name']}", size=11,
                        color=ft.Colors.GREY_500, text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            padding=24, border_radius=20,
            border=ft.Border.all(3, color),
        )

        body = ft.Column([
            result_card,
            ft.Container(height=14),
            ft.Button(
                content=ft.Row([ft.Icon(ft.Icons.REFRESH, color=ft.Colors.WHITE),
                                ft.Text("Пройти ещё раз", color=ft.Colors.WHITE, size=14)],
                               alignment=ft.MainAxisAlignment.CENTER, tight=True),
                bgcolor=ft.Colors.DEEP_ORANGE_400,
                height=48, expand=True, on_click=restart,
            ),
            ft.Container(height=8),
            ft.Button(
                content=ft.Text("Другая тема", color=ft.Colors.WHITE, size=14),
                bgcolor=ft.Colors.BLUE_500,
                height=48, expand=True,
                on_click=lambda e: navigate("/quiz_select"),
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
           spacing=0, scroll=ft.ScrollMode.AUTO, expand=True)

        return ft.View(
            controls=[
                ft.AppBar(title=ft.Text("Результат", size=17), bgcolor=ft.Colors.TRANSPARENT,
                          leading=ft.IconButton(ft.Icons.ARROW_BACK,
                                                on_click=lambda e: navigate("/quiz_select"))),
                wrap(body),
            ],
            padding=0, spacing=0
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
                title=ft.Text("Выйти?"),
                content=ft.Text("Прогресс не сохранится."),
                actions=[
                    ft.TextButton("Отмена", on_click=lambda e: page.pop_dialog()),
                    ft.TextButton("Выйти", on_click=lambda e: (page.pop_dialog(), navigate("/quiz_select")))
                ]
            ))

        question_card = ft.Container(
            content=ft.Column([
                ft.Text("Выберите перевод" if q["mode"] == "en_ru" else "Выберите слово",
                        size=11, color=ft.Colors.GREY_600,
                        text_align=ft.TextAlign.CENTER),
                ft.Container(height=8),
                ft.Text(q["prompt"], size=20, weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            padding=18, border_radius=16,
            border=ft.Border.all(2, ft.Colors.DEEP_ORANGE_200),
            margin=ft.Margin(bottom=12),
        )

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
                                            color=text_color, size=13),
                            width=28, height=28, alignment=ft.Alignment.CENTER,
                            bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                            border_radius=14,
                        ),
                        ft.Text(opt, size=13, expand=True, color=text_color,
                                weight=ft.FontWeight.W_500),
                    ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=base_color, padding=12, border_radius=12,
                    margin=ft.Margin(bottom=8),
                    on_click=lambda e, idx=i: answer(idx),
                )
            )

        feedback = ft.Container()
        if answered:
            if is_correct:
                feedback = ft.Container(
                    content=ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.WHITE, size=18),
                                    ft.Text("Верно!", color=ft.Colors.WHITE,
                                            weight=ft.FontWeight.BOLD, size=13)],
                                   alignment=ft.MainAxisAlignment.CENTER),
                    bgcolor=ft.Colors.GREEN_500, padding=10, border_radius=10,
                    margin=ft.Margin(top=8),
                )
            else:
                feedback = ft.Container(
                    content=ft.Column([
                        ft.Row([ft.Icon(ft.Icons.CANCEL, color=ft.Colors.WHITE, size=18),
                                ft.Text("Неверно", color=ft.Colors.WHITE,
                                        weight=ft.FontWeight.BOLD, size=13)],
                               alignment=ft.MainAxisAlignment.CENTER),
                        ft.Text(f"Правильный: {q['options'][q['correct_idx']]}",
                                color=ft.Colors.WHITE, size=12,
                                text_align=ft.TextAlign.CENTER),
                    ], spacing=4),
                    bgcolor=ft.Colors.RED_500, padding=10, border_radius=10,
                    margin=ft.Margin(top=8),
                )

        body = ft.Column([
            ft.ProgressBar(value=(current + 1) / total,
                           bgcolor=ft.Colors.GREY_200,
                           color=ft.Colors.DEEP_ORANGE_400, height=6),
            ft.Container(height=8),
            ft.Text(f"Вопрос {current + 1} из {total}", size=11,
                    color=ft.Colors.GREY_600, weight=ft.FontWeight.W_500),
            ft.Container(height=8),
            question_card,
            ft.Column(option_buttons, spacing=0),
            feedback,
            ft.Container(height=10),
            ft.Button(
                content=ft.Row([
                    ft.Text("Дальше" if current + 1 < total else "Завершить",
                            color=ft.Colors.WHITE, size=14, weight=ft.FontWeight.BOLD),
                    ft.Icon(ft.Icons.ARROW_FORWARD, color=ft.Colors.WHITE, size=18),
                ], alignment=ft.MainAxisAlignment.CENTER, tight=True),
                bgcolor=ft.Colors.DEEP_ORANGE_400 if answered else ft.Colors.GREY_400,
                disabled=not answered,
                height=48, expand=True,
                on_click=next_q,
            ),
        ], spacing=0, scroll=ft.ScrollMode.AUTO, expand=True)

        return ft.View(
            controls=[
                ft.AppBar(
                    title=ft.Text(q_data["section_name"], size=13,
                                  max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                    bgcolor=ft.Colors.TRANSPARENT,
                    leading=ft.IconButton(ft.Icons.CLOSE, on_click=exit_quiz),
                    actions=[
                        ft.Container(content=ft.Text(f"{q_data['score']} / {current + 1}",
                                                     weight=ft.FontWeight.BOLD, size=12,
                                                     color=ft.Colors.DEEP_ORANGE_400),
                                     padding=ft.Padding(left=8, right=14, top=6, bottom=6))
                    ]
                ),
                wrap(body),
            ],
            padding=0, spacing=0
        )

    # --- ПОДПИСКА ---
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
                return "Номер карты — 16 цифр"
            exp = card_exp.value.strip()
            if len(exp) != 5 or exp[2] != "/" or not (exp[:2].isdigit() and exp[3:].isdigit()):
                return "Срок в формате ММ/ГГ"
            mm = int(exp[:2])
            if mm < 1 or mm > 12:
                return "Неверный месяц"
            if not (len(card_cvv.value) == 3 and card_cvv.value.isdigit()):
                return "CVV — 3 цифры"
            if len(card_holder.value.strip()) < 3:
                return "Укажите имя"
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
                    pstate["error_msg"] = "Банк отклонил платёж."
                    pstate["step"] = "error"
                render()

            threading.Thread(target=finish, daemon=True).start()

        card_num = card_exp = card_cvv = card_holder = None

        def build():
            step = pstate["step"]

            if step == "method":
                items = [
                    ft.Text(f"{TIERS[tier_id]['icon']} {name}", size=18,
                            weight=ft.FontWeight.BOLD),
                    ft.Text(f"К оплате: {final_price()} ₽ / мес", size=15,
                            color=ft.Colors.BLUE_500, weight=ft.FontWeight.BOLD),
                ]
                if pstate["promo"]:
                    items.append(ft.Text(f"✅ {pstate['promo']}: −{int(pstate['discount']*100)}%",
                                         size=11, color=ft.Colors.GREEN_600))
                if pstate["error_msg"]:
                    items.append(ft.Text(pstate["error_msg"], size=11,
                                         color=ft.Colors.RED_500))
                items += [
                    ft.Divider(),
                    ft.Text("Способ оплаты:", size=12, color=ft.Colors.GREY_600),
                    ft.Button(
                        content=ft.Row([ft.Icon(ft.Icons.CREDIT_CARD, color=ft.Colors.WHITE, size=18),
                                        ft.Text("Банковская карта", color=ft.Colors.WHITE,
                                                weight=ft.FontWeight.BOLD, size=13)],
                                       alignment=ft.MainAxisAlignment.CENTER),
                        bgcolor=ft.Colors.BLUE_500, height=44, expand=True,
                        on_click=lambda e: (pstate.update({"method": "card"}), set_step("card")),
                    ),
                    ft.Button(
                        content=ft.Row([ft.Icon(ft.Icons.PHONE_ANDROID, color=ft.Colors.WHITE, size=18),
                                        ft.Text("СБП", color=ft.Colors.WHITE,
                                                weight=ft.FontWeight.BOLD, size=13)],
                                       alignment=ft.MainAxisAlignment.CENTER),
                        bgcolor=ft.Colors.GREEN_500, height=44, expand=True,
                        on_click=lambda e: (pstate.update({"method": "sbp"}), set_step("card")),
                    ),
                    ft.Row([
                        ft.TextButton("🎟 Промокод", on_click=lambda e: set_step("promo")),
                        ft.TextButton("Отмена", on_click=close),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ]
                return ft.Column(items, spacing=8, tight=True)

            if step == "card":
                card_num = ft.TextField(label="Номер карты", hint_text="1234 5678 9012 3456",
                                        keyboard_type=ft.KeyboardType.NUMBER, max_length=19,
                                        prefix_icon=ft.Icons.CREDIT_CARD, text_size=13)
                card_exp = ft.TextField(label="Срок", hint_text="ММ/ГГ", max_length=5,
                                         width=110, text_size=13)
                card_cvv = ft.TextField(label="CVV", hint_text="123", max_length=3,
                                        width=90, password=True, can_reveal_password=True,
                                        text_size=13)
                card_holder = ft.TextField(label="Держатель", hint_text="IVAN IVANOV",
                                            capitalization=ft.TextCapitalization.CHARACTERS,
                                            text_size=13)

                items = [
                    ft.Text(f"💳 Оплата {final_price()} ₽", size=15,
                            weight=ft.FontWeight.BOLD),
                    ft.Text("Тестовые данные", size=10, color=ft.Colors.GREY_500, italic=True),
                    ft.Container(height=4),
                    card_num,
                    ft.Row([card_exp, card_cvv], spacing=8),
                    card_holder,
                ]
                if pstate["error_msg"]:
                    items.append(ft.Container(
                        content=ft.Text(pstate["error_msg"], size=11,
                                        color=ft.Colors.RED_500),
                        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.RED),
                        padding=8, border_radius=6,
                    ))
                items += [
                    ft.Button(
                        content=ft.Row([ft.Icon(ft.Icons.LOCK, color=ft.Colors.WHITE, size=16),
                                        ft.Text(f"Оплатить {final_price()} ₽",
                                                color=ft.Colors.WHITE,
                                                weight=ft.FontWeight.BOLD, size=13)],
                                       alignment=ft.MainAxisAlignment.CENTER),
                        bgcolor=ft.Colors.GREEN_600, height=44, expand=True,
                        on_click=process_payment,
                    ),
                    ft.TextButton("← Назад", on_click=lambda e: set_step("method")),
                ]
                return ft.Column(items, spacing=6, tight=True)

            if step == "promo":
                promo_field = ft.TextField(label="Промокод", hint_text="WELCOME",
                                            capitalization=ft.TextCapitalization.CHARACTERS,
                                            text_size=13)

                def apply_promo(e):
                    code = promo_field.value.strip().upper()
                    if code in PROMO_CODES:
                        pstate["discount"] = PROMO_CODES[code]
                        pstate["promo"] = code
                        set_step("method")
                    else:
                        pstate["error_msg"] = "Не найден"
                        render()

                items = [
                    ft.Text("🎟 Промокод", size=15, weight=ft.FontWeight.BOLD),
                    ft.Text("WELCOME, STUDENT, FRIEND", size=10, color=ft.Colors.GREY_500),
                    promo_field,
                ]
                if pstate["error_msg"]:
                    items.append(ft.Text(pstate["error_msg"], size=11,
                                         color=ft.Colors.RED_500))
                items += [
                    ft.Button(
                        content=ft.Text("Применить", color=ft.Colors.WHITE,
                                        weight=ft.FontWeight.BOLD, size=13),
                        bgcolor=ft.Colors.PURPLE_400, height=42, expand=True,
                        on_click=apply_promo,
                    ),
                    ft.TextButton("← Назад", on_click=lambda e: set_step("method")),
                ]
                return ft.Column(items, spacing=8, tight=True)

            if step == "processing":
                return ft.Column([
                    ft.Container(height=16),
                    ft.ProgressRing(width=50, height=50, stroke_width=4,
                                    color=ft.Colors.BLUE_500),
                    ft.Container(height=10),
                    ft.Text("Обработка…", size=14, weight=ft.FontWeight.BOLD),
                    ft.Text("Соединение с банком", size=11, color=ft.Colors.GREY_600),
                    ft.Container(height=16),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, tight=True)

            if step == "success":
                txn = pstate["txn"]
                return ft.Column([
                    ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_500, size=56),
                    ft.Text("Оплата успешна!", size=18, weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREEN_600, text_align=ft.TextAlign.CENTER),
                    ft.Container(height=8),
                    ft.Container(
                        content=ft.Column([
                            ft.Row([ft.Text("Тариф", size=11, color=ft.Colors.GREY_600),
                                    ft.Text(f"{TIERS[tier_id]['icon']} {name}", size=11,
                                            weight=ft.FontWeight.BOLD)],
                                   alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Row([ft.Text("Сумма", size=11, color=ft.Colors.GREY_600),
                                    ft.Text(f"{final_price()} ₽", size=11,
                                            weight=ft.FontWeight.BOLD)],
                                   alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Row([ft.Text("Транзакция", size=11, color=ft.Colors.GREY_600),
                                    ft.Text(txn["txn_id"], size=11)],
                                   alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ], spacing=5),
                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                        padding=12, border_radius=10, width=float("inf"),
                    ),
                    ft.Button(
                        content=ft.Text("Понятно", color=ft.Colors.WHITE,
                                        weight=ft.FontWeight.BOLD, size=13),
                        bgcolor=ft.Colors.GREEN_600, height=44, expand=True,
                        on_click=success_close,
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8, tight=True)

            if step == "error":
                return ft.Column([
                    ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED_500, size=56),
                    ft.Text("Платёж не прошёл", size=18, weight=ft.FontWeight.BOLD,
                            color=ft.Colors.RED_500, text_align=ft.TextAlign.CENTER),
                    ft.Text(pstate["error_msg"], size=12, color=ft.Colors.GREY_700,
                            text_align=ft.TextAlign.CENTER),
                    ft.Container(height=8),
                    ft.Button(
                        content=ft.Text("Повторить", color=ft.Colors.WHITE,
                                        weight=ft.FontWeight.BOLD, size=13),
                        bgcolor=ft.Colors.BLUE_500, height=44, expand=True,
                        on_click=lambda e: set_step("card"),
                    ),
                    ft.TextButton("Отмена", on_click=close),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8, tight=True)

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
                                color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=14),
                disabled=is_current,
                bgcolor=color if not is_current else ft.Colors.GREY_400,
                height=44, expand=True,
                on_click=lambda e: open_payment_flow(tier_id, name, price),
            )
            return ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(f"{TIERS[tier_id]['icon']} {name}", size=18,
                                weight=ft.FontWeight.BOLD, expand=True),
                        ft.Container(content=ft.Icon(ft.Icons.DIAMOND, color=color, size=18),
                                     bgcolor=ft.Colors.with_opacity(0.2, color),
                                     padding=6, border_radius=16),
                    ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    ft.Text(f"{price} ₽/мес" if price > 0 else "Бесплатно", size=22,
                            color=color, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.Column([
                        ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, color=color, size=14),
                                ft.Text(f, size=12, expand=True)])
                        for f in features
                    ]),
                    btn
                ], spacing=6),
                bgcolor=card_bg, border_radius=16, padding=16,
                margin=ft.Margin(bottom=10),
                border=ft.Border.all(2, color),
            )

        txns = state.progress.get("transactions", [])[-3:]
        history_block = ft.Container()
        if txns:
            history_items = []
            for t in reversed(txns):
                history_items.append(
                    ft.Row([
                        ft.Text(t["txn_id"], size=10, color=ft.Colors.GREY_600),
                        ft.Text(f"{t['amount']} ₽", size=10, weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREEN_600),
                        ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_500, size=12),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                )
            history_block = ft.Container(
                content=ft.Column([
                    ft.Text("Транзакции", size=12, weight=ft.FontWeight.BOLD),
                    ft.Divider(height=1),
                    *history_items,
                ], spacing=5),
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                padding=12, border_radius=12, margin=ft.Margin(top=6, bottom=10),
            )

        body = ft.Column([
            make_card("Бесплатный", "free", 0,
                      ["30 карточек в день", "Базовый раздел"],
                      ft.Colors.GREY_600),
            make_card("Плюс", "plus", 199,
                      ["500 карточек в день", "Все разделы", "Продвинутый уровень"],
                      ft.Colors.BLUE_500),
            make_card("Премиум", "premium", 499,
                      ["Безлимит", "Экспорт прогресса", "Приоритетная поддержка"],
                      ft.Colors.AMBER_600),
            history_block,
        ], spacing=0, scroll=ft.ScrollMode.AUTO, expand=True)

        return ft.View(
            controls=[
                ft.AppBar(title=ft.Text("Подписка", size=17), bgcolor=ft.Colors.TRANSPARENT,
                          leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/"))),
                wrap(body),
            ],
            padding=0, spacing=0
        )

    # --- ПОИСК / ИЗБРАННОЕ / СТАТИСТИКА ---
    def search_view():
        results_list = ft.Column(spacing=8, expand=True,
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
                        leading=ft.Container(content=ft.Text(tinfo["emoji"], size=18),
                                             width=36, height=36,
                                             alignment=ft.Alignment.CENTER,
                                             bgcolor=ft.Colors.with_opacity(0.15, tinfo["color"]),
                                             border_radius=10),
                        title=ft.Text(w["en"], weight=ft.FontWeight.BOLD, size=13),
                        subtitle=ft.Text(w["ru"], size=11)),
                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                        border_radius=12, padding=4,
                        border=ft.Border.all(1, ft.Colors.BLUE_200),
                        margin=ft.Margin(bottom=6))
                )
            page.update()

        body = ft.Column([
            ft.TextField(
                hint_text="Введите слово…",
                on_change=on_search,
                prefix_icon=ft.Icons.SEARCH,
                border_radius=14, filled=True,
                focused_border_color=ft.Colors.BLUE_500,
                text_size=13,
                content_padding=ft.Padding(left=14, right=14, top=10, bottom=10),
            ),
            ft.Container(height=8),
            results_list,
        ], expand=True, spacing=0)

        return ft.View(
            controls=[
                ft.AppBar(title=ft.Text("Поиск", size=17), bgcolor=ft.Colors.TRANSPARENT,
                          leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/"))),
                wrap(body),
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
            ),
            padding=0, spacing=0
        )

    def favorites_view():
        fav_words = [w for w in all_words_flat() if w["en"] in state.progress["favorites"]]
        items = [
            ft.Container(content=ft.ListTile(
                leading=ft.Icon(ft.Icons.FAVORITE, color=ft.Colors.RED_400, size=18),
                title=ft.Text(w["en"], weight=ft.FontWeight.BOLD, size=13),
                subtitle=ft.Text(w["ru"], size=11)),
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                border_radius=12, padding=4, margin=ft.Margin(bottom=6),
                border=ft.Border.all(1, ft.Colors.PINK_200))
            for w in fav_words
        ] if fav_words else [
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.FAVORITE_BORDER, size=50, color=ft.Colors.GREY_400),
                    ft.Text("Пока нет избранных карточек",
                            color=ft.Colors.GREY_600,
                            text_align=ft.TextAlign.CENTER, size=13),
                    ft.Text("Нажмите ❤ на карточке",
                            color=ft.Colors.GREY_500, size=11,
                            text_align=ft.TextAlign.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=32,
            )
        ]

        body = ft.Column(items, spacing=0,
                         horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                         scroll=ft.ScrollMode.AUTO, expand=True)

        return ft.View(
            controls=[
                ft.AppBar(title=ft.Text("Избранное", size=17), bgcolor=ft.Colors.TRANSPARENT,
                          leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/"))),
                wrap(body),
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
            ),
            padding=0, spacing=0
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
                    leading=ft.Container(content=ft.Text(emoji, size=22),
                                         width=42, height=42,
                                         alignment=ft.Alignment.CENTER,
                                         bgcolor=ft.Colors.with_opacity(0.2, color),
                                         border_radius=12),
                    title=ft.Text(title, weight=ft.FontWeight.BOLD, size=13),
                    subtitle=ft.Text(value, size=11)),
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                border_radius=12, margin=ft.Margin(bottom=6),
                border=ft.Border.all(1, ft.Colors.with_opacity(0.3, color))
            )

        body = ft.Column([
            stat_card("🔥", "Серия дней", f"{streak} дн.", ft.Colors.ORANGE_500),
            stat_card("📖", "Изучено карточек", f"{known_count} из {total_count}", ft.Colors.BLUE_500),
            stat_card("⭐", "В избранном", str(len(state.progress["favorites"])), ft.Colors.PINK_500),
            stat_card("🧠", "Пройдено тестов", str(total_quizzes), ft.Colors.DEEP_ORANGE_400),
            stat_card("🎯", "Средний результат", f"{accuracy}%", ft.Colors.GREEN_600),
        ], spacing=0, scroll=ft.ScrollMode.AUTO, expand=True)

        return ft.View(
            controls=[
                ft.AppBar(title=ft.Text("Статистика", size=17), bgcolor=ft.Colors.TRANSPARENT,
                          leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/"))),
                wrap(body),
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
            ),
            padding=0, spacing=0
        )

    navigate("/")


ft.run(main)
