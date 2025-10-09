import flet as ft
import pyodbc
from INTER_Profesores import mostrar_menu_principal
from DB import CONNECTION_STRING
def main(page: ft.Page):
    page.clean()
    page.title = "Inicio de Sesión"
    page.window.width = 400
    page.window.height = 300
    page.bgcolor= "#d1d1d1"

    sql_verify = "SELECT pro_nameID FROM Profesores WHERE pro_rut = ? AND pro_password = ?"


    titulo = ft.Text("Iniciar Sesión", size=20, weight=ft.FontWeight.BOLD)
    usuario = ft.TextField(label="RUT", width=300, max_length=10)


    password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)


    mensaje = ft.Text("", color="black")
    logo = ft.Image(src="/neuro_check_icon.png",
        width=120,
        height=120,
        fit=ft.ImageFit.CONTAIN
    )
    fondo = ft.Container(ft.Image(src="/fondo.png", width= 1920, height= 1080,fit=ft.ImageFit.CONTAIN), expand=True)
    def login_click(e):
        try:
            cnxn = pyodbc.connect(CONNECTION_STRING)
            cursor = cnxn.cursor()
            cursor.execute(sql_verify, usuario.value, password.value) 
            res_is = cursor.fetchone()
            print(res_is)
            if  res_is:
                mostrar_menu_principal(page, cerrar_main=main)
                page.update()
            else:
                mensaje.value = "Usuario o contraseña incorrectos."
                page.update()
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Error de conexión: {sqlstate}")

    boton_login = ft.ElevatedButton("Entrar", on_click=login_click,width=100,height= 30)

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

            alignment=ft.MainAxisAlignment.CENTER,  
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
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

ft.app(target=main, port=5000, view=ft.AppView.WEB_BROWSER, assets_dir="assets")
