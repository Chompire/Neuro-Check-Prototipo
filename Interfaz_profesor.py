# menu.py
import flet as ft

def mostrar_menu_principal(page: ft.Page, nombre_usuario):
    page.clean()
    page.add(
        ft.Column(
            [
                ft.Text(f"Bienvenido, {nombre_usuario}!", size=25, weight="bold", color="green"),
                ft.Text("Esta es la segunda interfaz 🎉", size=18),
                ft.ElevatedButton("Cerrar sesión", on_click=lambda e: page.window_destroy())
            ],
            alignment="center",
            horizontal_alignment="center",
            expand=True
        ),
        alignment=ft.alignment.center,
        expand=True,
    )
