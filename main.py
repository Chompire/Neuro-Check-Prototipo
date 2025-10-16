import flet as ft
from INTER_Profesores import mostrar_menu_principal
from INTER_PIE import menu_principalPIE
from CRUD import profesorREAD
 


def main(page: ft.Page):
    page.clean()
    page.title = "Inicio de Sesión"
    page.window.width = 400
    page.window.height = 300
    page.bgcolor= "#d1d1d1"
    titulo = ft.Text("Iniciar Sesión", size=20, weight=ft.FontWeight.BOLD)
    usuario = ft.TextField(label="RUT", width=300)


    password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)


    mensaje = ft.Text("", color="black")
    logo = ft.Image(src="/NEURO CHECK ICON.png",
        width=120,
        height=120,
        fit=ft.ImageFit.CONTAIN
    )
    fondo = ft.Container(ft.Image(src="/fondo.png", width= 1920, height= 1080,fit=ft.ImageFit.CONTAIN), expand=True)
    def login_click(e):
        profesor_data = profesorREAD(pro_rut=usuario.value, pro_password=password.value)
        
        if profesor_data:
            prof_id = profesor_data[0]
            prof_cargo = profesor_data[8]
            if prof_cargo == 1:
                menu_principalPIE(page, prof_id)
            else:
                mostrar_menu_principal(page, prof_id)
            page.update()
        else:
            mensaje.value = "Usuario o contraseña incorrectos"
            page.update()



    boton_login = ft.ElevatedButton("Entrar", on_click=login_click,width=100,height= 30)

    contenido = ft.Container(
        alignment=ft.alignment.center,
        expand=True,
        content=ft.Column(
            controls=[
                logo,
                titulo,
                usuario,
                password,
                boton_login,
                mensaje,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
    )

    page.add(
        ft.Stack(
            controls=[
                fondo,
                contenido,
            ],
            expand=True,
        )
    )

ft.app(target=main, assets_dir="assets", view=ft.AppView.FLET_APP)
