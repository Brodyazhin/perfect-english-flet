import flet as ft
from data import DATA, count_words
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
        page.update()

    # --- Главное меню ---
    def home_view():
        tier = TIERS[state.license["tier"]]
        
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
                        ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
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

    # --- Карточки ---
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
                    ft.Button(
                        content="Назад",
                        on_click=lambda e: navigate("/section")
                    )
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
                        ft.Button(
                            content="Показать перевод",
                            on_click=lambda e: page.show_dialog(
                                ft.AlertDialog(title=ft.Text("Перевод"), content=ft.Text(word["ru"]))
                            )
                        ),
                        ft.Row([
                            ft.Button(
                                content="✅ Знаю",
                                on_click=mark_known,
                                bgcolor=ft.Colors.GREEN_400,
                                color=ft.Colors.WHITE
                            ),
                            ft.Button(
                                content="Следующее →",
                                on_click=next_word,
                                bgcolor=ft.Colors.BLUE_400,
                                color=ft.Colors.WHITE
                            )
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    expand=True,
                    padding=20
                )
            ]
        )

    navigate("/")

ft.run(main)
