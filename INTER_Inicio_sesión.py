import flet as ft
import pyodbc
from INTER_Profesores import mostrar_menu_principal
from INTER_PIE import menu_principalPIE
from DB import CONNECTION_STRING

def get_profesor_id(pro_rut: str, pro_password: str):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                sql_verify = "SELECT pro_nameID FROM Profesores WHERE pro_rut = ? AND pro_password = ?"
                cursor.execute(sql_verify, pro_rut, pro_password)
                return cursor.fetchone()
    except pyodbc.Error as ex:
        print(f"Error de conexión o consulta: {ex.args[0]}")
        return None
    
def get_profesor_cargo(pro_id:int):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                sql_verify = "SELECT pro_cargo FROM Profesores WHERE pro_nameID = ?"
                cursor.execute(sql_verify, pro_id)
                return cursor.fetchone()
    except pyodbc.Error as ex:
        print(f"Error de conexión o consulta: {ex.args[0]}")
        return None
 


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
        prof_parameters = get_profesor_id(usuario.value, password.value)
        prof_cargo = get_profesor_cargo(prof_parameters[0])
        print(prof_cargo)
        print(prof_parameters[0])  
        if prof_parameters:
            if prof_cargo[0] == 1:
                menu_principalPIE(page, prof_parameters[0])
            else:
                mostrar_menu_principal(page, prof_parameters[0])
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

ft.app(target=main, port=5000, view=ft.AppView.WEB_BROWSER, assets_dir="assets")
