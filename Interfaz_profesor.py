# menu.py
import flet as ft

def mostrar_menu_principal(page: ft.Page, nombre_usuario):
    page.clean()

    page.add(
        ft.Column(
            [
                ft.Text(f"Bienvenido, {nombre_usuario}!", size=25, weight="bold", color="green"),
                ft.Text("Esta es la segunda interfaz 🎉", size=18),
                ft.ElevatedButton("Nuevo test", on_click= registro_alumno(page))
            ],
            alignment="center",
            horizontal_alignment="center",
            expand=True
        )
    )
def registro_alumno(page:ft.Page):
    page.clean()
    page.add(
        ft.Text("Ingresa los datos del alumno.")
    )