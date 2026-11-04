import flet as ft
from data import DATA, count_words, all_words_flat
from subscription import state, TIERS

def main(page: ft.Page):
    page.title = "Perfect English"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)
    
    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        page.update()
    
    # --- Навигация ---
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
        page.update()

    # --- ЭКРАН 1: Главное меню ---
    def home_view():
        tier = TIERS[state.license["tier"]]
        
        section_cards = []
        for name, item in DATA.items():
            section_cards.append(
                ft.Container(
                    content=ft.ListTile(
                        leading=ft.Container(
                            content=ft.Text(item["icon"], size=28),
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE),
                            border_radius=10, width=50, height=50,
                            alignment=ft.Alignment.CENTER
                        ),
                        title=ft.Text(name, weight=ft.FontWeight.BOLD, size=16),
                        subtitle=ft.Text(f"{count_words(item)} слов", color=ft.Colors.GREY_600),
                        trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT, color=ft.Colors.GREY_400),
                    ),
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                    border_radius=20,
                    padding=5,
                    margin=ft.Margin(bottom=12),
                    shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK), offset=ft.Offset(0, 5)),
                    on_click=lambda e, n=name: open_section(n)
                )
            )

        return ft.View(
            controls=[
                ft.AppBar(
                    title=ft.Text("Perfect English", weight=ft.FontWeight.BOLD), 
                    bgcolor=ft.Colors.TRANSPARENT,
                    actions=[ft.IconButton(ft.Icons.BRIGHTNESS_6, on_click=toggle_theme)]
                ),
                ft.Container(
                    content=ft.Column([
                        # Баннер подписки
                        ft.Container(
                            content=ft.Row([
                                ft.Column([
                                    ft.Text(f"{tier['icon']} {tier['name']} тариф", weight=ft.FontWeight.BOLD, size=18),
                                    ft.Text("Управление подпиской", size=12, color=ft.Colors.WHITE_70),
                                ]),
                                ft.Icon(ft.Icons.DIAMOND, color=ft.Colors.ORANGE_400, size=30)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            bgcolor=ft.Colors.BLUE_600,
                            padding=20,
                            border_radius=20,
                            margin=ft.Margin(bottom=20),
                            on_click=lambda e: navigate("/subscription")
                        ),
                        ft.Text("Разделы", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800),
                        ft.Container(height=10),
                        ft.Column(section_cards, spacing=0)
                    ], scroll=ft.ScrollMode.AUTO),
                    padding=20,
                    expand=True
                )
            ],
            navigation_bar=ft.NavigationBar(
                destinations=[
                    ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Главная"),
                    ft.NavigationBarDestination(icon=ft.Icons.SEARCH, label="Поиск"),
                    ft.NavigationBarDestination(icon=ft.Icons.FAVORITE, label="Избранное"),
                    ft.NavigationBarDestination(icon=ft.Icons.BAR_CHART, label="Статистика"),
                ],
                on_change=lambda e: navigate(["/", "/search", "/favorites", "/stats"][e.control.selected_index])
            )
        )

    # --- Логика разделов ---
    current_section_data = {}
    
    def open_section(section_name):
        current_section_data.clear()
        current_section_data.update({"name": section_name, "item": DATA[section_name]})
        navigate("/section")

    def section_view():
        name = current_section_data["name"]
        item = current_section_data["item"]
        
        subs_list = ft.Column(spacing=10)
        
        def render_subs(query=""):
            subs_list.controls.clear()
            for sub_name, sub_item in item["subsections"].items():
                if query and query.lower() not in sub_name.lower():
                    continue
                subs_list.controls.append(
                    ft.Container(
                        content=ft.ListTile(
                            title=ft.Text(sub_name, weight=ft.FontWeight.W_600),
                            subtitle=ft.Text(f"{count_words(sub_item)} слов", color=ft.Colors.GREY_600),
                            trailing=ft.Icon(ft.Icons.PLAY_CIRCLE_FILL, color=ft.Colors.BLUE_400, size=30),
                        ),
                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                        border_radius=15,
                        padding=5,
                        on_click=lambda e, n=sub_name, i=sub_item: open_flashcards(n, i)
                    )
                )
            page.update()

        render_subs()

        def on_search(e):
            render_subs(e.control.value)

        return ft.View(
            controls=[
                ft.AppBar(
                    title=ft.Text(name, weight=ft.FontWeight.BOLD), 
                    bgcolor=ft.Colors.TRANSPARENT,
                    leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/"))
                ),
                ft.Container(
                    content=ft.Column([
                        ft.TextField(
                            hint_text="Поиск по темам...", 
                            prefix_icon=ft.Icons.SEARCH,
                            on_change=on_search,
                            border_radius=15,
                            filled=True,
                            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                            border_color=ft.Colors.TRANSPARENT,
                        ),
                        ft.Container(height=10),
                        ft.Column([subs_list], scroll=ft.ScrollMode.AUTO, expand=True)
                    ]),
                    padding=20,
                    expand=True
                )
            ]
        )

    # --- ЭКРАН 3: Карточки ---
    current_cards_data = {"words": [], "index": 0, "title": ""}
    
    def open_flashcards(title, sub_item):
        words = sub_item.get("words", [])
        if "subsections" in sub_item:
            words = []
            for s in sub_item["subsections"].values():
                words.extend(s.get("words", []))
                
        if not words: return
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
        
        def next_word(e):
            current_cards_data["index"] = (current_cards_data["index"] + 1) % len(current_cards_data["words"])
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
                    title=ft.Text(current_cards_data["title"]),
                    bgcolor=ft.Colors.TRANSPARENT,
                    leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/section")),
                    actions=[
                        ft.IconButton(
                            ft.Icons.FAVORITE if is_fav else ft.Icons.FAVORITE_BORDER, 
                            icon_color=ft.Colors.RED if is_fav else ft.Colors.GREY, 
                            on_click=toggle_fav
                        )
                    ]
                ),
                ft.Container(
                    content=ft.Column([
                        # Сама карточка
                        ft.Container(
                            content=ft.Column([
                                ft.Text("НОВОЕ СЛОВО" if not is_known else "ИЗУЧЕНО", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_600 if is_known else ft.Colors.BLUE_400),
                                ft.Container(height=20),
                                ft.Text(word["en"], size=42, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                                ft.Text(f"[{word['ipa']}]", size=18, color=ft.Colors.GREY_600, italic=True),
                                ft.Container(height=40),
                                # Кнопка перевода
                                ft.Button(
                                    content=ft.Row([ft.Icon(ft.Icons.VISIBILITY), ft.Text("Показать перевод")], alignment=ft.MainAxisAlignment.CENTER),
                                    on_click=lambda e: page.show_dialog(
                                        ft.AlertDialog(
                                            title=ft.Text("Перевод", text_align=ft.TextAlign.CENTER),
                                            content=ft.Text(word["ru"], size=24, text_align=ft.TextAlign.CENTER),
                                            alignment=ft.Alignment.CENTER
                                        )
                                    ),
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), padding=20)
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                            border_radius=30,
                            padding=40,
                            shadow=ft.BoxShadow(blur_radius=30, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK), offset=ft.Offset(0, 10)),
                            expand=True
                        ),
                        ft.Container(height=30),
                        # Кнопки управления
                        ft.Row([
                            ft.Button( # <-- ИСПРАВЛЕНО
                                content=ft.Row([ft.Icon(ft.Icons.CLOSE, color=ft.Colors.WHITE), ft.Text("Не знаю", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)]),
                                bgcolor=ft.Colors.RED_400, on_click=next_word, expand=True, height=60,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15))
                            ),
                            ft.Button( # <-- ИСПРАВЛЕНО
                                content=ft.Row([ft.Icon(ft.Icons.CHECK, color=ft.Colors.WHITE), ft.Text("Знаю", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)]),
                                bgcolor=ft.Colors.GREEN_400, on_click=mark_known, expand=True, height=60,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15))
                            ),
                        ], spacing=20)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=20,
                    expand=True
                )
            ]
        )

    # --- Вспомогательные экраны (Поиск, Избранное, Статистика, Подписка) ---
    def search_view():
        results_list = ft.Column(spacing=10)
        def on_search(e):
            results_list.controls.clear()
            query = e.control.value.lower()
            if not query: return
            words = all_words_flat()
            found = [w for w in words if query in w["en"].lower() or query in w["ru"].lower()][:30]
            for w in found:
                results_list.controls.append(
                    ft.Container(
                        content=ft.ListTile(title=ft.Text(w["en"], weight=ft.FontWeight.BOLD), subtitle=ft.Text(w["ru"])),
                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST, border_radius=15, padding=5
                    )
                )
            page.update()

        return ft.View(
            controls=[
                ft.AppBar(title=ft.Text("Поиск"), bgcolor=ft.Colors.TRANSPARENT, leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/"))),
                ft.Container(
                    content=ft.Column([
                        ft.TextField(hint_text="Введите слово...", on_change=on_search, prefix_icon=ft.Icons.SEARCH, border_radius=15, filled=True),
                        ft.Container(height=10),
                        ft.Column([results_list], scroll=ft.ScrollMode.AUTO, expand=True)
                    ]),
                    padding=20, expand=True
                )
            ]
        )

    def favorites_view():
        fav_words = [w for w in all_words_flat() if w["en"] in state.progress["favorites"]]
        items = []
        if not fav_words:
            items.append(ft.Text("Вы пока не добавили слова в избранное", color=ft.Colors.GREY_600))
        else:
            for w in fav_words:
                items.append(ft.Container(content=ft.ListTile(title=ft.Text(w["en"], weight=ft.FontWeight.BOLD), subtitle=ft.Text(w["ru"])), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST, border_radius=15, padding=5, margin=ft.Margin(bottom=5)))
                
        return ft.View(
            controls=[
                ft.AppBar(title=ft.Text("Избранное"), bgcolor=ft.Colors.TRANSPARENT, leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/"))),
                ft.Container(content=ft.Column(items, scroll=ft.ScrollMode.AUTO, expand=True), padding=20, expand=True)
            ],
            navigation_bar=ft.NavigationBar(
                destinations=[ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Главная"), ft.NavigationBarDestination(icon=ft.Icons.SEARCH, label="Поиск"), ft.NavigationBarDestination(icon=ft.Icons.FAVORITE, label="Избранное"), ft.NavigationBarDestination(icon=ft.Icons.BAR_CHART, label="Статистика")],
                selected_index=2, on_change=lambda e: navigate(["/", "/search", "/favorites", "/stats"][e.control.selected_index])
            )
        )

    def stats_view():
        known_count = len(state.progress["known"])
        total_count = len(all_words_flat())
        streak = state.progress.get("streak", 0)
        
        return ft.View(
            controls=[
                ft.AppBar(title=ft.Text("Статистика"), bgcolor=ft.Colors.TRANSPARENT, leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/"))),
                ft.Container(
                    content=ft.Column([
                        ft.Container(content=ft.ListTile(leading=ft.Text("🔥", size=30), title=ft.Text("Серия дней", weight=ft.FontWeight.BOLD), subtitle=ft.Text(f"{streak} дн.")), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST, border_radius=15, margin=5),
                        ft.Container(content=ft.ListTile(leading=ft.Text("📖", size=30), title=ft.Text("Изучено", weight=ft.FontWeight.BOLD), subtitle=ft.Text(f"{known_count} из {total_count}")), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST, border_radius=15, margin=5),
                        ft.Container(content=ft.ListTile(leading=ft.Text("⭐", size=30), title=ft.Text("Избранное", weight=ft.FontWeight.BOLD), subtitle=ft.Text(str(len(state.progress["favorites"])))), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST, border_radius=15, margin=5),
                    ], scroll=ft.ScrollMode.AUTO),
                    padding=20, expand=True
                )
            ],
            navigation_bar=ft.NavigationBar(
                destinations=[ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Главная"), ft.NavigationBarDestination(icon=ft.Icons.SEARCH, label="Поиск"), ft.NavigationBarDestination(icon=ft.Icons.FAVORITE, label="Избранное"), ft.NavigationBarDestination(icon=ft.Icons.BAR_CHART, label="Статистика")],
                selected_index=3, on_change=lambda e: navigate(["/", "/search", "/favorites", "/stats"][e.control.selected_index])
            )
        )

    def subscription_view():
        current_tier = state.license["tier"]
        
        def make_card_safe(name, tier_id, price, features):
            is_current = (tier_id == current_tier)
            card_bg = ft.Colors.BLUE_50 if is_current else ft.Colors.SURFACE_CONTAINER_HIGHEST
            return ft.Container(
                content=ft.Column([
                    ft.Text(f"{TIERS[tier_id]['icon']} {name}", size=22, weight=ft.FontWeight.BOLD),
                    ft.Text(f"{price} ₽/мес" if price > 0 else "Бесплатно", size=28, color=ft.Colors.BLUE, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.Column([ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN, size=16), ft.Text(f, size=14)]) for f in features]),
                    ft.Button(content="Текущий план" if is_current else "Оформить", disabled=is_current, bgcolor=ft.Colors.BLUE if not is_current else ft.Colors.GREY_300, color=ft.Colors.WHITE, height=50),
                ]),
                bgcolor=card_bg, border_radius=20, padding=25, margin=ft.Margin(bottom=15),
            )

        return ft.View(
            controls=[
                ft.AppBar(title=ft.Text("Подписка"), bgcolor=ft.Colors.TRANSPARENT, leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/"))),
                ft.Container(
                    content=ft.Column([
                        make_card_safe("Бесплатный", "free", 0, ["30 слов в день", "Базовый раздел"]),
                        make_card_safe("Плюс", "plus", 199, ["500 слов в день", "Все разделы", "Тесты"]),
                        make_card_safe("Премиум", "premium", 499, ["Безлимит", "Экспорт прогресса", "Поддержка"]),
                    ], scroll=ft.ScrollMode.AUTO),
                    padding=20, expand=True
                )
            ]
        )

    navigate("/")

ft.run(main)
