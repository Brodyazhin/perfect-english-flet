import flet as ft

def main(page: ft.Page):
    page.title = "Perfect English Test"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.add(
        ft.Text("Ура! Flet-приложение работает!", size=24, weight=ft.FontWeight.BOLD),
        ft.Text("Если ты видишь это на телефоне — сборка прошла успешно.", size=16),
    )

# Исправленная строка запуска для Flet 1.0+
ft.run(main)
