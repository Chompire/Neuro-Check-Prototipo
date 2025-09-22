# menu.py
import flet as ft
def mostrar_menu_principal(page: ft.Page, nombre_usuario):
    page.clean()

    def buttonclick(e):
        registro_alumno(page)
        page.update()
    page.add(
        ft.Container(
            ft.Column(
            [
                ft.Text(f"Bienvenido, {nombre_usuario}!", size=25, weight="bold", color="green"),
                ft.Text("Esta es la segunda interfaz 🎉", size=18),
                ft.ElevatedButton("Nuevo test", on_click=buttonclick)
            ],
            alignment="center",
            horizontal_alignment="center",
            expand=True
            )
        )
        
    )
def registro_alumno(page:ft.Page):
    page.clean()
    def back(e):
        mostrar_menu_principal(page)
        page.update()
    page.add(
        ft.Container(
            ft.Column(
                [ft.Text("Ingresa los datos del alumno."), ft.ElevatedButton("Volver", on_click= back)]
            )
            
        )
        
    )
