import flet as ft
from Interfaz_profesor import mostrar_menu_principal


user_is = "admin"
contra_is = "1234"

def main(page: ft.Page):
    page.title = "Inicio de Sesión"
    page.window_width = 400
    page.window_height = 300

    titulo = ft.Text("Iniciar Sesión", size=20, weight="bold")
    usuario = ft.TextField(label="Usuario", width=300)
    password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
    mensaje = ft.Text("", color="black")
    logo = ft.Image(src="/Nuevo logo.png",
        width=120,
        height=120,
        fit=ft.ImageFit.COVER
    )
    fondo = ft.Container(bgcolor="red", expand=True)
    def login_click(e):
        if usuario.value == user_is and password.value == contra_is:
            mostrar_menu_principal(page, usuario.value)
            page.update()
        else:
            mensaje.value = "Usuario o contraseña incorrectos."
            page.update()

    boton_login = ft.ElevatedButton("Entrar", on_click=login_click) 

    contenido = ft.Container(
        content=ft.Column(
            [
                logo,
                titulo,
                usuario,
                password,
                boton_login,
                mensaje,
            ],
            
            alignment="center",  
            horizontal_alignment="center",
            spacing=10,
        ),
        alignment=ft.alignment.center,
        expand=True,
    ) 
    page.add(
        ft.Stack(
            [
                fondo,
                contenido,
            ],
            expand=True,
        )
    )

ft.app(target=main, view=ft.WEB_BROWSER)
