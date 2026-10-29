import flet as ft
from data import DATA, count_words, all_words_flat
from subscription import state, TIERS

def main(page: ft.Page):
    page.title = "Perfect English"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    
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
        
        quick_actions = ft.Row([
            ft.IconButton(ft.Icons.SEARCH, icon_color=ft.Colors.BLUE, on_click=lambda e: navigate("/search")),
            ft.IconButton(ft.Icons.FAVORITE, icon_color=ft.Colors.RED, on_click=lambda e: navigate("/favorites")),
            ft.IconButton(ft.Icons.BAR_CHART, icon_color=ft.Colors.GREEN, on_click=lambda e: navigate("/stats")),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=30)

        section_cards = []
        for name, item in DATA.items():
            section_cards.append(
                ft.Container(
                    content=ft.ListTile(
                        leading=ft.Text(item["icon"], size=30),
                        title=ft.Text(name, weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(item["desc"]),
                        trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS),
                    ),
                    bgcolor=ft.Colors.WHITE,
                    border_radius=15,
                    margin=10,
                    shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK)),
                    on_click=lambda e, n=name: open_section(n)
                )
            )

        return ft.View(
            controls=[
                ft.Container(
                    content=ft.Column([
                        ft.Text("🎓", size=60),
                        ft.Text("Perfect English", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                        ft.Text(f"{tier['icon']} {tier['name']}", color=ft.Colors.ORANGE),
                        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                        quick_actions,
                        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                        ft.Button(
                            content=ft.Row([ft.Icon(ft.Icons.DIAMOND), ft.Text("Управление подпиской")]),
                            on_click=lambda e: navigate("/subscription"),
                            bgcolor=ft.Colors.ORANGE_100,
                        ),
                        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                        ft.Text("📚 Разделы", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        ft.Column(section_cards, spacing=0)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=30,
                    bgcolor=ft.Colors.GREY_50,
                    expand=True
                )
            ]
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
        
        subs = []
        for sub_name, sub_item in item["subsections"].items():
            subs.append(
                ft.Container(
                    content=ft.ListTile(
                        title=ft.Text(sub_name, weight=ft.FontWeight.W_500),
                        subtitle=ft.Text(f"{count_words(sub_item)} слов"),
                        trailing=ft.Icon(ft.Icons.PLAY_ARROW),
                    ),
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                    margin=8,
                    on_click=lambda e, n=sub_name, i=sub_item: open_flashcards(n, i)
                )
            )

        return ft.View(
            controls=[
                ft.AppBar(
                    title=ft.Text(name), 
                    bgcolor=ft.Colors.BLUE_100, 
                    leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/"))
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Выбери тему", size=16, color=ft.Colors.GREY_600),
                        ft.Column(subs, spacing=0)
                    ]),
                    padding=20
                )
            ]
        )

    # --- ЭКРАН 3: Карточки ---
    current_cards_data = {"words": [], "index": 0, "title": ""}
    
    def open_flashcards(title, sub_item):
        words = sub_item.get("words", [])
        if not words: return
        current_cards_data["words"] = words
        current_cards_data["index"] = 0
        current_cards_data["title"] = title
        navigate("/flashcards")

    def flashcards_view():
        if not current_cards_data["words"]:
            return ft.View(controls=[ft.Text("Нет слов")])

        word = current_cards_data["words"][current_cards_data["index"]]
        
        if not state.can_see_more():
            return ft.View(
                controls=[
                    ft.Text("Дневной лимит исчерпан!", size=20, color=ft.Colors.RED),
                    ft.Button(content="Назад", on_click=lambda e: navigate("/section"))
                ]
            )

        def next_word(e):
            current_cards_data["index"] = (current_cards_data["index"] + 1) % len(current_cards_data["words"])
            page.views[-1] = flashcards_view()
            page.update()

        def mark_known(e):
            if word["en"] not in state.progress["known"]:
                state.progress["known"].append(word["en"])
                state.save_progress()
            next_word(e)

        return ft.View(
            controls=[
                ft.AppBar(
                    title=ft.Text(current_cards_data["title"]),
                    bgcolor=ft.Colors.GREEN_100,
                    leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/section"))
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Container(height=50),
                        ft.Text(word["en"], size=40, weight=ft.FontWeight.BOLD),
                        ft.Text(f"[{word['ipa']}]", size=18, color=ft.Colors.BLUE, italic=True),
                        ft.Divider(height=50, color=ft.Colors.TRANSPARENT),
                        ft.Row([
                            ft.Button(content="👁 Перевод", on_click=lambda e: page.show_dialog(
                                ft.AlertDialog(title=ft.Text("Перевод"), content=ft.Text(word["ru"]))
                            )),
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                        ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                        ft.Row([
                            ft.Button(content="✅ Знаю", on_click=mark_known, bgcolor=ft.Colors.GREEN_400, color=ft.Colors.WHITE),
                            ft.Button(content="Следующее →", on_click=next_word, bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE)
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    expand=True,
                    padding=20
                )
            ]
        )

    # --- НОВЫЙ ЭКРАН: Поиск ---
    def search_view():
        results_list = ft.Column(spacing=10)
        
        def on_search(e):
            results_list.controls.clear()
            query = e.control.value.lower()
            if not query: return
            
            words = all_words_flat()
            found = [w for w in words if query in w["en"].lower() or query in w["ru"].lower()][:20]
            
            if not found:
                results_list.controls.append(ft.Text("Ничего не найдено"))
            for w in found:
                results_list.controls.append(
                    ft.ListTile(
                        title=ft.Text(w["en"], weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(w["ru"]),
                    )
                )
            page.update()

        return ft.View(
            controls=[
                ft.AppBar(title=ft.Text("Поиск"), bgcolor=ft.Colors.BLUE_100, leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/"))),
                ft.Container(
                    content=ft.Column([
                        ft.TextField(hint_text="Введите слово...", on_change=on_search, prefix_icon=ft.Icons.SEARCH),
                        results_list
                    ]),
                    padding=20
                )
            ]
        )

    # --- НОВЫЙ ЭКРАН: Избранное ---
    def favorites_view():
        fav_words = [w for w in all_words_flat() if w["en"] in state.progress["favorites"]]
        
        items = []
        if not fav_words:
            items.append(ft.Text("Вы пока не добавили слова в избранное"))
        else:
            for w in fav_words:
                items.append(
                    ft.ListTile(
                        title=ft.Text(w["en"], weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(w["ru"]),
                    )
                )
                
        return ft.View(
            controls=[
                ft.AppBar(title=ft.Text("Избранное"), bgcolor=ft.Colors.RED_100, leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/"))),
                ft.Column(items, scroll=ft.ScrollMode.AUTO, expand=True)
            ]
        )

    # --- НОВЫЙ ЭКРАН: Статистика ---
    def stats_view():
        known_count = len(state.progress["known"])
        total_count = len(all_words_flat())
        streak = state.progress.get("streak", 0)
        
        return ft.View(
            controls=[
                ft.AppBar(title=ft.Text("Статистика"), bgcolor=ft.Colors.GREEN_100, leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/"))),
                ft.Container(
                    content=ft.Column([
                        ft.ListTile(leading=ft.Text("🔥", size=30), title=ft.Text("Серия дней", weight=ft.FontWeight.BOLD), subtitle=ft.Text(f"{streak} дн.")),
                        ft.ListTile(leading=ft.Text("📖", size=30), title=ft.Text("Изучено слов", weight=ft.FontWeight.BOLD), subtitle=ft.Text(f"{known_count} из {total_count}")),
                        ft.ListTile(leading=ft.Text("⭐", size=30), title=ft.Text("В избранном", weight=ft.FontWeight.BOLD), subtitle=ft.Text(str(len(state.progress["favorites"])))),
                    ]),
                    padding=20
                )
            ]
        )

    # --- НОВЫЙ ЭКРАН: Подписка ---
    def subscription_view():
        current_tier = state.license["tier"]
        
        def make_card(name, tier_id, price, features):
            is_current = (tier_id == current_tier)
            
            # Меняем цвет фона для текущего тарифа вместо рамки
            card_bgcolor = ft.Colors.BLUE_50 if is_current else ft.Colors.WHITE
            
            return ft.Container(
                content=ft.Column([
                    ft.Text(f"{TIERS[tier_id]['icon']} {name}", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text(f"{price} ₽/мес" if price > 0 else "Бесплатно", size=24, color=ft.Colors.BLUE),
                    ft.Column([ft.Text(f"✅ {f}") for f in features]),
                    ft.Button(
                        content="Текущий план" if is_current else "Оформить",
                        disabled=is_current,
                        on_click=lambda e, t=tier_id: page.show_dialog(
                            ft.AlertDialog(title=ft.Text("Оплата"), content=ft.Text("Здесь будет подключена ЮKassa."))
                        )
                    )
                ]),
                bgcolor=card_bgcolor,
                border_radius=15,
                padding=20,
                margin=10,
            )

        return ft.View(
            controls=[
                ft.AppBar(title=ft.Text("Подписка"), bgcolor=ft.Colors.ORANGE_100, leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: navigate("/"))),
                ft.Column([
                    make_card("Бесплатный", "free", 0, ["30 слов в день", "Базовый раздел"]),
                    make_card("Плюс", "plus", 199, ["500 слов в день", "Все разделы", "Тесты"]),
                    make_card("Премиум", "premium", 499, ["Безлимит", "Экспорт прогресса", "Приоритетная поддержка"]),
                ], scroll=ft.ScrollMode.AUTO)
            ]
        )

    navigate("/")

ft.run(main)
