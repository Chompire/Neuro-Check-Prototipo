import flet as ft
from flet_mvc import FletView # Importamos nuestra nueva clase base
from colors import color_Background_Docente, color_Docente

class LoginView(FletView):    
    def __init__(self, controller, model):
        self.rut_field = ft.Ref[ft.TextField]()
        self.password_field = ft.Ref[ft.TextField]()
        self.mensaje_error = ft.Ref[ft.Text]()

        titulo = ft.Text("Iniciar Sesión", size=20, weight=ft.FontWeight.BOLD)
        rut = ft.TextField(label="RUT (sin puntos ni guión)", width=300, ref=self.rut_field)
        password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300, ref=self.password_field)
        boton_login = ft.ElevatedButton("Entrar", on_click=lambda e: controller.handle_login_click(e), width=100, height=30)
        fondo = ft.Container(ft.Image(src="/fondo.png", width= 1920, height= 1080,fit=ft.ImageFit.CONTAIN), expand=True)
        mensaje = ft.Text(ref=self.mensaje_error, color="black")    
        logo = ft.Image(src="/NEURO CHECK ICON.png",
            width=120,
            height=120,
            fit=ft.ImageFit.CONTAIN
        )
        contenido = ft.Container(
            alignment=ft.alignment.center,
            expand=True,
            content=ft.Column(
                controls=[
                    logo,
                    titulo,
                    rut,
                    password,
                    boton_login,
                    mensaje,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
        )
        view = ft.View(
            "/",
            bgcolor=color_Background_Docente,
            controls=
            [
                ft.Stack(
                    controls=[
                        fondo,
                        contenido,
                    ],
                    expand=True,
                )
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        super().__init__(model, view, controller)
