import flet as ft
import threading
import time
from data import DATA, count_words, all_words_flat
from subscription import state, TIERS


FAQ_DATA = {
    "💳 Подписка и оплата": [
        {"q": "Как оформить подписку?",
         "a": "Откройте главный экран и нажмите на голубую карточку тарифа сверху — или сразу перейдите в раздел «Подписка». Выберите план и нажмите «Оформить». Оплата проходит мгновенно, доступ активируется сразу."},
        {"q": "Какие тарифы доступны?",
         "a": "🆓 Бесплатный — 30 слов в день, базовый раздел.\n\n⭐ Плюс — 199 ₽/мес: 500 слов в день, все разделы, продвинутый уровень.\n\n👑 Премиум — 499 ₽/мес: безлимит, экспорт прогресса, приоритетная поддержка."},
        {"q": "Есть ли пробный период?",
         "a": "Да! При первом запуске автоматически активируется 7 дней тарифа Плюс. По истечении срока вы можете оформить подписку или продолжить на бесплатном тарифе."},
        {"q": "Как отменить подписку?",
         "a": "Подписка не продлевается автоматически — оплата разовая на выбранный период. По окончании срока вы просто вернётесь на бесплатный тариф."},
        {"q": "Какие способы оплаты?",
         "a": "Принимаем банковские карты Visa, MasterCard и МИР. Платежи защищены, данные карты не хранятся на наших серверах."},
        {"q": "Как получить возврат средств?",
         "a": "Возврат возможен в течение 14 дней с момента оплаты. Напишите на support@perfectenglish.app с указанием даты покупки и названия тарифа."},
    ],
    "📱 Использование приложения": [
        {"q": "Как добавить слово в избранное?",
         "a": "Откройте карточку слова и нажмите ❤ в правом верхнем углу. Все избранные слова доступны в нижней вкладке «Избранное»."},
        {"q": "Что значит статус «Изучено»?",
         "a": "Слово помечается как «Изучено», когда вы нажимаете зелёную кнопку ✓ на карточке. Такие слова учитываются в общей статистике прогресса."},
        {"q": "Как работает статистика?",
         "a": "Раздел «Статистика» показывает:\n🔥 серию дней обучения (streak)\n📖 количество изученных слов\n⭐ количество слов в избранном"},
        {"q": "Работает ли приложение офлайн?",
         "a": "Да! Все слова хранятся локально на устройстве. Приложение полностью работает без интернета. Сеть нужна только для оплаты подписки."},
        {"q": "Как найти нужное слово?",
         "a": "В нижней вкладке «Поиск» введите слово на русском или английском — приложение найдёт все совпадения по всем разделам."},
        {"q": "Как переключить тему оформления?",
         "a": "На главном экране нажмите на иконку ☀/🌙 в правом верхнем углу — приложение переключится между светлой и тёмной темой."},
    ],
    "🇬🇧 Изучение английского": [
        {"q": "С чего начать изучение?",
         "a": "Начните с раздела «База»: алфавит, числа, цвета, местоимения. Это фундамент. Затем переходите к «Словарному запасу» — семья, еда, дом, животные."},
        {"q": "Что такое IPA-транскрипция?",
         "a": "IPA (International Phonetic Alphabet) — международный фонетический алфавит. Запись [ˈæp.əl] показывает правильное произношение. Знак ˈ означает ударение на следующий слог."},
        {"q": "Как эффективно запоминать слова?",
         "a": "Метод интервального повторения:\n1. Учите 10–15 слов в день\n2. Повторяйте через 1, 3 и 7 дней\n3. Используйте слова в речи и письме\n4. Сложные добавляйте в избранное ❤"},
        {"q": "Сколько слов нужно знать?",
         "a": "• 1500–2000 — для повседневного общения\n• 3000–5000 — для чтения книг и новостей\n• 8000+ — для свободного владения\n\nВ приложении уже 200+ слов, постоянно добавляем новые."},
        {"q": "Как улучшить произношение?",
         "a": "Слушайте носителей и повторяйте вслух. Обращайте внимание на транскрипцию. Особенно тренируйте звуки: θ (think), ð (this), ŋ (sing), w (water), r (red)."},
        {"q": "Сколько времени заниматься?",
         "a": "15–20 минут ежедневно эффективнее, чем 2 часа раз в неделю. Мозг лучше усваивает информацию небольшими порциями через короткие регулярные интервалы."},
    ],
}


def main(page: ft.Page):
    page.title = "Perfect English"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)

    chat_messages = [
        {"text": "👋 Привет! Я техподдержка Perfect English.\nЧем могу помочь? Выберите тему ниже или задайте вопрос — а в разделе ❓ FAQ вы найдёте ответы на частые вопросы.", "is_user": False}
    ]

    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        page.update()

    def navigate(route):
        page.views.clear()
        if route == "/":
            page.views.append(home_view())
        elif route == "/section":
            page.views.append(section_view())
        elif route == "/flashcards":
            page.views.append(flashcards_view())
        elif route == "/search":
            page.views.append(search_view())
        elif route == "/favorites":
            page.views.append(favorites_view())
        elif route == "/stats":
            page.views.append(stats_view())
        elif route == "/subscription":
            page.views.append(subscription_view())
        elif route == "/support":
            page.views.append(support_view())
        elif route == "/faq":
            page.views.append(faq_view())
        page.update()

    # --- ГЛАВНОЕ МЕНЮ ---
    def home_view():
        tier = TIERS[state.license["tier"]]

        section_cards = []
        for name, item in DATA.items():
            is_locked = (name.startswith("5.") and state.license["tier"] == "free")
            lock_icon = ft.Icon(ft.Icons.LOCK, color=ft.Colors.RED) if is_locked else ft.Icon(ft.Icons.CHEVRON_RIGHT, color=ft.Colors.GREY_400)

            section_cards.append(
                ft.Container(
                    content=ft.ListTile(
                        leading=ft.Container(
                            content=ft.Text(item["icon"], size=28),
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE),
                            border_radius=10, width=50, height=50,
                            alignment=ft.Alignment.CENTER
                        ),
                        title=ft.Text(name, weight=ft.FontWeight.BOLD, size=16, soft_wrap=True),
                        subtitle=ft.Text(item["desc"], color=ft.Colors.GREY_600, size=12, soft_wrap=True, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                        trailing=lock_icon,
                    ),
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                    border_radius=20, padding=5,
                    margin=ft.Margin(bottom=12),
                    shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK), offset=ft.Offset(0, 5)),
                    on_click=lambda e, n=name, locked=is_locked: open_section(n, locked)
                )
            )

        return ft.View(
            controls=[
                ft.AppBar(
                    title=ft.Text("Perfect English", weight=ft.FontWeight.BOLD),
                    bgcolor=ft.Colors.TRANSPARENT,
                    actions=[
                        ft.IconButton(ft.Icons.BAR_CHART, tooltip="Статистика", on_click=lambda e: navigate("/stats")),
                        ft.IconButton(ft.Icons.BRIGHTNESS_6, on_click=toggle_theme)
                    ]
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Container(
                            content=ft.Row([
                                ft.Column([
                                    ft.Text(f"{tier['icon']} {tier['name']} тариф", weight=ft.FontWeight.BOLD, size=18, soft_wrap=True),
                                    ft.Text("Управление подпиской", size=12, color=ft.Colors.WHITE_70, soft_wrap=True),
                                ], expand=True, spacing=4),  # <-- FIX: expand=True
                                ft.Icon(ft.Icons.DIAMOND, color=ft.Colors.ORANGE_400, size=30)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                            bgcolor=ft.Colors.BLUE_600, padding=20,
                            border_radius=20, margin=ft.Margin(bottom=20),
                            on_click=lambda e: navigate("/subscription")
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
             "👋 Здравствуйте! Рад помочь. Задайте ваш вопрос или выберите тему быстрого ответа ниже.\n\n💡 Совет: в разделе ❓ FAQ собраны ответы на самые частые вопросы."),
            (["оплат", "купить", "оформ", "подписк", "тариф", "прем", "плюс"],
             "💳 Оформить подписку можно двумя способами:\n\n1️⃣ Нажать на голубую карточку тарифа на главном экране\n2️⃣ Перейти в раздел «Подписка»\n\nТарифы:\n⭐ Плюс — 199 ₽/мес (все разделы)\n👑 Премиум — 499 ₽/мес (безлимит + экспорт)\n\nЕсть 7 дней бесплатного пробного Плюса!"),
            (["промокод", "скидк", "акци", "купон"],
             "🎟 Промокоды и акции публикуются в нашем Telegram-канале. Если у вас есть код — введите его при оформлении подписки в разделе «Подписка»."),
            (["баг", "ошибк", "не работает", "глючит", "падает", "вылет", "тормоз"],
             "⚠ Приносим извинения за неудобства!\n\nОпишите, пожалуйста, подробнее:\n• Что вы делали перед ошибкой?\n• Что именно произошло?\n• Модель устройства\n\nМы сразу передадим информацию в разработку."),
            (["возврат", "вернуть", "отмен", "деньг"],
             "💸 Возврат возможен в течение 14 дней после оплаты.\n\nНапишите на support@perfectenglish.app и укажите:\n• Дату покупки\n• Название тарифа\n• Причину возврата\n\nОбработаем в течение 2 рабочих дней."),
            (["слов", "карточк", "учить", "учиться", "запомина", "зубр"],
             "📚 Рекомендую метод интервального повторения:\n\n1️⃣ Учите 10–15 слов в день\n2️⃣ Возвращайтесь к ним через 1, 3 и 7 дней\n3️⃣ Сложные слова добавляйте в ❤ Избранное\n4️⃣ Проговаривайте слова вслух\n\nОтмечайте выученное зелёной кнопкой ✓ — так работает статистика."),
            (["транскрипц", "ipa", "произнош", "звук", "акцент"],
             "🔊 IPA — это международный фонетический алфавит.\n\nПример: apple [ˈæp.əl]\n• ˈ — ударение на следующий слог\n• æ — открытый звук «э»\n• ə — безударный «шва»\n\nСлушайте эталон и повторяйте вслух — тренируйте сложные звуки: θ, ð, ŋ, w, r."),
            (["статистик", "прогресс", "streak", "серия"],
             "📊 Раздел «Статистика» доступен по иконке 📈 в верхней панели главного экрана.\n\nТам вы увидите:\n🔥 серию дней обучения\n📖 количество изученных слов\n⭐ количество слов в избранном"),
            (["избранн", "любим", "сердечк"],
             "❤ Чтобы добавить слово в избранное — откройте карточку и нажмите на сердечко в правом верхнем углу.\n\nВсе избранные слова доступны в нижней вкладке «Избранное»."),
            (["поиск", "найти", "где найти"],
             "🔍 В нижней вкладке «Поиск» введите слово на русском или английском. Приложение найдёт все совпадения во всех разделах."),
            (["офлайн", "интернет", "без сети"],
             "📴 Да, приложение работает полностью офлайн! Все слова хранятся на устройстве. Интернет нужен только для оплаты подписки."),
            (["спасиб", "благодар", "thanks"],
             "😊 Всегда рады помочь! Если появятся ещё вопросы — обращайтесь. Успехов в изучении английского! 🇬🇧"),
            (["faq", "вопрос", "част"],
             "❓ Раздел «Частые вопросы» открывается по кнопке в правом верхнем углу этого экрана — или нажмите на чип «FAQ» ниже.\n\nТам 18 ответов по трём категориям: подписка, приложение, изучение английского."),
            (["приложен", "версия", "обновл"],
             "📱 Вы используете актуальную версию Perfect English 1.0.0. Следите за обновлениями — мы регулярно добавляем новые слова и функции."),
        ]
        for keywords, response in rules:
            if any(k in t for k in keywords):
                return response
        return ("🤔 Спасибо за вопрос! Я передал его оператору — ответим в течение 24 часов.\n\n"
                "А пока загляните в раздел ❓ FAQ — возможно, там уже есть готовый ответ!")

    def support_view():
        messages_list = ft.ListView(expand=True, spacing=10, padding=20)

        def make_bubble_row(msg):
            """Пузырь занимает максимум 75% ширины, прижат к нужному краю."""
            is_user = msg["is_user"]
            bubble = ft.Container(
                content=ft.Text(
                    msg["text"],
                    color=ft.Colors.WHITE if is_user else ft.Colors.BLACK,
                    size=14,
                    soft_wrap=True,
                ),
                bgcolor=ft.Colors.BLUE_400 if is_user else ft.Colors.GREY_200,
                padding=15,
                border_radius=ft.BorderRadius(
                    top_left=15, top_right=15,
                    bottom_left=15 if is_user else 0,
                    bottom_right=0 if is_user else 15
                )
            )
            bubble_zone = ft.Container(
                content=bubble,
                expand=4,  # до 80% ширины
                alignment=ft.Alignment.CENTER_RIGHT if is_user else ft.Alignment.CENTER_LEFT,
            )
            spacer = ft.Container(expand=1)
            if is_user:
                return ft.Row([spacer, bubble_zone])
            else:
                return ft.Row([bubble_zone, spacer])

        def render_messages():
            messages_list.controls.clear()
            for msg in chat_messages:
                if msg.get("is_typing"):
                    messages_list.controls.append(
                        ft.Row([
                            ft.Container(
                                content=ft.Row([
                                    ft.ProgressRing(width=14, height=14, stroke_width=2),
                                    ft.Text("печатает…", size=12, color=ft.Colors.GREY_600, italic=True)
                                ], spacing=8),
                                bgcolor=ft.Colors.GREY_200,
                                padding=12,
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
        input_field = ft.TextField(
            hint_text="Введите сообщение…",
            expand=True,
            border_radius=20,
            on_submit=send_message
        )

        def make_chip(label, text):
            return ft.Chip(
                label=ft.Text(label, size=12, soft_wrap=True),
                on_click=lambda e: send_text(text),
            )

        # <-- FIX: горизонтальный ListView вместо Row(scroll=...)
        quick_replies = ft.Container(
            content=ft.ListView(
                controls=[
                    make_chip("💳 Подписка", "Как оформить подписку?"),
                    make_chip("💸 Возврат", "Хочу вернуть деньги"),
                    make_chip("⚠ Проблема", "У меня проблема с приложением"),
                    make_chip("📚 Обучение", "Как эффективнее учить слова?"),
                    make_chip("🔊 Произношение", "Как улучшить произношение?"),
                    ft.Chip(label=ft.Text("❓ FAQ", size=12),
                            on_click=lambda e: navigate("/faq")),
                ],
                spacing=8,
                horizontal=True,
                height=45,
            ),
            padding=ft.Padding(left=10, right=10, top=8, bottom=4),
        )

        return ft.View(
            controls=[
                ft.AppBar(
                    title=ft.Text("Техподдержка"),
                    bgcolor=ft.Colors.TRANSPARENT,
                    leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/")),
                    actions=[
                        ft.IconButton(ft.Icons.HELP_OUTLINE, tooltip="Частые вопросы",
                                      on_click=lambda e: navigate("/faq"))
                    ]
                ),
                messages_list,
                quick_replies,
                ft.Container(
                    content=ft.Row([
                        input_field,
                        ft.IconButton(ft.Icons.SEND, icon_color=ft.Colors.BLUE, on_click=send_message)
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

    # --- ЧАСТЫЕ ВОПРОСЫ (FAQ) ---
    def faq_view():
        expanded = {}
        faq_list = ft.Column(
            spacing=6,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,  # <-- FIX: растягиваем по ширине
        )

        def render_faq():
            faq_list.controls.clear()
            for category, questions in FAQ_DATA.items():
                faq_list.controls.append(
                    ft.Container(
                        content=ft.Text(category, size=16, weight=ft.FontWeight.BOLD, soft_wrap=True),
                        margin=ft.Margin(top=15, bottom=5, left=4)
                    )
                )
                for i, item in enumerate(questions):
                    key = f"{category}#{i}"
                    is_open = expanded.get(key, False)
                    faq_list.controls.append(
                        ft.Container(
                            content=ft.Column([
                                ft.Container(
                                    content=ft.Row([
                                        ft.Text(item["q"], weight=ft.FontWeight.W_600, size=14,
                                                expand=True, soft_wrap=True),
                                        ft.Icon(
                                            ft.Icons.EXPAND_LESS if is_open else ft.Icons.EXPAND_MORE,
                                            color=ft.Colors.BLUE, size=20
                                        ),
                                    ]),
                                    padding=15,
                                    on_click=lambda e, k=key: toggle_faq(k),
                                ),
                                ft.Container(
                                    content=ft.Text(item["a"], size=13, color=ft.Colors.GREY_700, soft_wrap=True),
                                    padding=ft.Padding(left=15, right=15, bottom=15, top=0),
                                    visible=is_open,
                                ),
                            ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.STRETCH),
                            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                            border_radius=15,
                        )
                    )
            page.update()

        def toggle_faq(key):
            expanded[key] = not expanded.get(key, False)
            render_faq()

        render_faq()

        return ft.View(
            controls=[
                ft.AppBar(
                    title=ft.Text("Частые вопросы", weight=ft.FontWeight.BOLD),
                    bgcolor=ft.Colors.TRANSPARENT,
                    leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/support")),
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(ft.Icons.SUPPORT_AGENT, color=ft.Colors.BLUE, size=30),
                                ft.Column([
                                    ft.Text("Не нашли ответ?", weight=ft.FontWeight.BOLD, size=14, soft_wrap=True),
                                    ft.Text("Задайте вопрос в поддержке", size=12, color=ft.Colors.GREY_600, soft_wrap=True),
                                ], spacing=2, expand=True),
                                ft.Icon(ft.Icons.CHEVRON_RIGHT, color=ft.Colors.GREY_400),
                            ]),
                            bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.BLUE),
                            padding=15, border_radius=15,
                            margin=ft.Margin(bottom=10),
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

    # --- ЛОГИКА РАЗДЕЛОВ ---
    current_section_data = {}

    def open_section(section_name, is_locked):
        if is_locked:
            page.show_dialog(ft.AlertDialog(
                title=ft.Text("Раздел заблокирован"),
                content=ft.Text("Для доступа к «Продвинутому уровню» необходимо оформить подписку.", soft_wrap=True),
                actions=[
                    ft.TextButton("Отмена", on_click=lambda e: page.pop_dialog()),
                    ft.TextButton("Оформить", on_click=lambda e: (page.pop_dialog(), navigate("/subscription")))
                ]
            ))
            return
        current_section_data.clear()
        current_section_data.update({"name": section_name, "item": DATA[section_name]})
        navigate("/section")

    def section_view():
        name = current_section_data["name"]
        item = current_section_data["item"]
        subs_list = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True,
                              horizontal_alignment=ft.CrossAxisAlignment.STRETCH)

        def render_subs(query=""):
            subs_list.controls.clear()
            for sub_name, sub_item in item["subsections"].items():
                if query and query.lower() not in sub_name.lower():
                    continue
                subs_list.controls.append(
                    ft.Container(
                        content=ft.ListTile(
                            title=ft.Text(sub_name, weight=ft.FontWeight.W_600, soft_wrap=True),
                            trailing=ft.Icon(ft.Icons.PLAY_CIRCLE_FILL, color=ft.Colors.BLUE_400, size=30),
                        ),
                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                        border_radius=15, padding=5,
                        on_click=lambda e, n=sub_name, i=sub_item: open_flashcards(n, i)
                    )
                )
            page.update()

        render_subs()

        return ft.View(
            controls=[
                ft.AppBar(title=ft.Text(name, weight=ft.FontWeight.BOLD, soft_wrap=True), bgcolor=ft.Colors.TRANSPARENT,
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

    # --- КАРТОЧКИ ---
    current_cards_data = {"words": [], "index": 0, "title": ""}

    def open_flashcards(title, sub_item):
        words = sub_item.get("words", [])
        if not words:
            return
        current_cards_data["words"] = words
        current_cards_data["index"] = 0
        current_cards_data["title"] = title
        navigate("/flashcards")

    def flashcards_view():
        if not current_cards_data["words"]:
            return ft.View(controls=[ft.Text("Нет слов")])
        word = current_cards_data["words"][current_cards_data["index"]]
        is_known = word["en"] in state.progress["known"]
        is_fav = word["en"] in state.progress["favorites"]

        # <-- FIX: динамический размер шрифта для длинных слов
        en_word = word["en"]
        if len(en_word) <= 12:
            font_size = 42
        elif len(en_word) <= 20:
            font_size = 32
        else:
            font_size = 24

        def next_word(e):
            current_cards_data["index"] = (current_cards_data["index"] + 1) % len(current_cards_data["words"])
            page.views[-1] = flashcards_view()
            page.update()

        def prev_word(e):
            current_cards_data["index"] = (current_cards_data["index"] - 1) % len(current_cards_data["words"])
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

        return ft.View(
            controls=[
                ft.AppBar(
                    title=ft.Text(current_cards_data["title"], soft_wrap=True, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                    bgcolor=ft.Colors.TRANSPARENT,
                    leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/section")),
                    actions=[ft.IconButton(ft.Icons.FAVORITE if is_fav else ft.Icons.FAVORITE_BORDER,
                                           icon_color=ft.Colors.RED if is_fav else ft.Colors.GREY, on_click=toggle_fav)]
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Container(
                            content=ft.Column([
                                ft.Text("НОВОЕ СЛОВО" if not is_known else "ИЗУЧЕНО", size=12,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.GREEN_600 if is_known else ft.Colors.BLUE_400),
                                ft.Container(height=20),
                                ft.Text(en_word, size=font_size, weight=ft.FontWeight.BOLD,
                                        text_align=ft.TextAlign.CENTER, soft_wrap=True),
                                ft.Text(f"[{word['ipa']}]", size=16, color=ft.Colors.GREY_600,
                                        italic=True, text_align=ft.TextAlign.CENTER, soft_wrap=True),
                                ft.Container(height=30),
                                ft.Button(
                                    content=ft.Row([ft.Icon(ft.Icons.VISIBILITY), ft.Text("Показать перевод")],
                                                   alignment=ft.MainAxisAlignment.CENTER, tight=True),
                                    on_click=lambda e: page.show_dialog(ft.AlertDialog(
                                        title=ft.Text("Перевод", text_align=ft.TextAlign.CENTER),
                                        content=ft.Text(word["ru"], size=24, text_align=ft.TextAlign.CENTER, soft_wrap=True),
                                        alignment=ft.Alignment.CENTER)),
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), padding=20)
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST, border_radius=30, padding=25,
                            shadow=ft.BoxShadow(blur_radius=30,
                                                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                                                offset=ft.Offset(0, 10)),
                            expand=True
                        ),
                        ft.Container(height=20),
                        # <-- FIX: убран width=300, добавлен padding для узких экранов
                        ft.Container(
                            content=ft.Row([
                                ft.IconButton(ft.Icons.ARROW_BACK_IOS, icon_size=28, on_click=prev_word),
                                ft.Row([
                                    ft.Button(content=ft.Icon(ft.Icons.CLOSE, color=ft.Colors.WHITE),
                                              bgcolor=ft.Colors.RED_400, on_click=next_word,
                                              width=60, height=60,
                                              style=ft.ButtonStyle(shape=ft.CircleBorder())),
                                    ft.Button(content=ft.Icon(ft.Icons.CHECK, color=ft.Colors.WHITE),
                                              bgcolor=ft.Colors.GREEN_400, on_click=mark_known,
                                              width=60, height=60,
                                              style=ft.ButtonStyle(shape=ft.CircleBorder())),
                                ], spacing=40, alignment=ft.MainAxisAlignment.CENTER),
                                ft.IconButton(ft.Icons.ARROW_FORWARD_IOS, icon_size=28, on_click=next_word),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            padding=ft.Padding(left=20, right=20),
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True),
                    padding=20, expand=True
                )
            ]
        )

    # --- ПОДПИСКА ---
    def subscription_view():
        current_tier = state.license["tier"]

        def make_card(name, tier_id, price, features):
            is_current = (tier_id == current_tier)
            card_bg = ft.Colors.BLUE_50 if is_current else ft.Colors.SURFACE_CONTAINER_HIGHEST

            def process_payment(e):
                dlg = ft.AlertDialog(title=ft.Text("Оплата"), content=ft.Text("Соединение с банком…"))
                page.show_dialog(dlg)

                def finish():
                    page.pop_dialog()
                    state.license["tier"] = tier_id
                    state.save_license()
                    page.show_dialog(ft.AlertDialog(title=ft.Text("Успешно"),
                                                    content=ft.Text(f"Тариф «{name}» активирован!")))
                    page.views[-1] = subscription_view()
                    page.update()

                threading.Timer(2.0, finish).start()

            btn = ft.Button(
                content="Текущий план" if is_current else "Оформить",
                disabled=is_current,
                bgcolor=ft.Colors.BLUE if not is_current else ft.Colors.GREY_300,
                color=ft.Colors.WHITE, height=50, width=float("inf"),  # <-- FIX: на всю ширину
                on_click=process_payment
            )
            return ft.Container(
                content=ft.Column([
                    ft.Text(f"{TIERS[tier_id]['icon']} {name}", size=22, weight=ft.FontWeight.BOLD, soft_wrap=True),
                    ft.Text(f"{price} ₽/мес" if price > 0 else "Бесплатно", size=28,
                            color=ft.Colors.BLUE, weight=ft.FontWeight.BOLD, soft_wrap=True),
                    ft.Divider(),
                    ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN, size=16),
                            ft.Text(f, size=14, expand=True, soft_wrap=True),  # <-- FIX: expand=True
                        ])
                        for f in features
                    ]),
                    btn
                ], spacing=8),
                bgcolor=card_bg, border_radius=20, padding=25, margin=ft.Margin(bottom=15),
            )

        return ft.View(
            controls=[
                ft.AppBar(title=ft.Text("Подписка"), bgcolor=ft.Colors.TRANSPARENT,
                          leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/"))),
                ft.Container(
                    content=ft.Column([
                        make_card("Бесплатный", "free", 0, ["30 слов в день", "Базовый раздел"]),
                        make_card("Плюс", "plus", 199, ["500 слов в день", "Все разделы", "Продвинутый уровень"]),
                        make_card("Премиум", "premium", 499, ["Безлимит", "Экспорт прогресса", "Поддержка"]),
                    ], scroll=ft.ScrollMode.AUTO, expand=True,
                       horizontal_alignment=ft.CrossAxisAlignment.STRETCH),  # <-- FIX: растягиваем карточки
                    padding=20, expand=True
                )
            ]
        )

    # --- ВСПОМОГАТЕЛЬНЫЕ ЭКРАНЫ ---
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
                results_list.controls.append(
                    ft.Container(content=ft.ListTile(
                        title=ft.Text(w["en"], weight=ft.FontWeight.BOLD, soft_wrap=True),
                        subtitle=ft.Text(w["ru"], soft_wrap=True)),
                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                        border_radius=15, padding=5)
                )
            page.update()

        return ft.View(
            controls=[
                ft.AppBar(title=ft.Text("Поиск"), bgcolor=ft.Colors.TRANSPARENT,
                          leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/"))),
                ft.Container(content=ft.Column([
                    ft.TextField(hint_text="Введите слово…", on_change=on_search,
                                 prefix_icon=ft.Icons.SEARCH, border_radius=15, filled=True),
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
                title=ft.Text(w["en"], weight=ft.FontWeight.BOLD, soft_wrap=True),
                subtitle=ft.Text(w["ru"], soft_wrap=True)),
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                border_radius=15, padding=5, margin=ft.Margin(bottom=5))
            for w in fav_words
        ] if fav_words else [ft.Text("Вы пока не добавили слова в избранное", color=ft.Colors.GREY_600, soft_wrap=True)]
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

        def stat_card(emoji, title, value):
            return ft.Container(
                content=ft.ListTile(
                    leading=ft.Text(emoji, size=30),
                    title=ft.Text(title, weight=ft.FontWeight.BOLD, soft_wrap=True),
                    subtitle=ft.Text(value, soft_wrap=True)),
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                border_radius=15, margin=5
            )

        return ft.View(
            controls=[
                ft.AppBar(title=ft.Text("Статистика"), bgcolor=ft.Colors.TRANSPARENT,
                          leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/"))),
                ft.Container(
                    content=ft.Column([
                        stat_card("🔥", "Серия дней", f"{streak} дн."),
                        stat_card("📖", "Изучено", f"{known_count} из {total_count}"),
                        stat_card("⭐", "Избранное", str(len(state.progress["favorites"]))),
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
