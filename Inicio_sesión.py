import flet as ft

def main(page: ft.Page):
    page.title = "NeuroCheck"
    page.vertical_alignment = "center"

    txt_nombre = ft.TextField(label="Escribe tu nombre")
    saludo = ft.Text()

    def saludar(e):
        saludo.value = f"¡Hola, {txt_nombre.value}!"
        page.update()

    page.add(
        txt_nombre,
        ft.ElevatedButton("Saludar", on_click=saludar),
        saludo
    )

# Ejecutar en el navegador
ft.app(target=main, view=ft.WEB_BROWSER)