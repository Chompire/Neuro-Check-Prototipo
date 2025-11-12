import flet as ft
from flet_mvc import FletView
from colors import color_Docente, color_Background_PIE

class CambiarPasswordView(FletView):
    def __init__(self, controller, model):
        self.feedback_text = ft.Text("", size=16, weight=ft.FontWeight.BOLD)
        self.nuevo_password = ft.TextField(label="Nueva contraseña", color="black", label_style=ft.TextStyle(color="black"), password=True)
        self.confirmar_password = ft.TextField(label="Nueva contraseña", color="black", label_style=ft.TextStyle(color="black"), password=True)
        view = ft.View(
            "/cambiar_contrasena",
            scroll=ft.ScrollMode.AUTO,
            bgcolor=color_Background_PIE,
            controls=[
                ft.Row([ft.Text("Inicio >", weight=ft.FontWeight.BOLD, color="black"), ft.Text("Cambiar Contraseña", weight=ft.FontWeight.BOLD, color=color_Docente)], alignment=ft.MainAxisAlignment.START),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Cambiar contraseña", size=20, weight=ft.FontWeight.BOLD, color="black"),
                            ft.Divider(),
                            ft.Row([self.nuevo_password]),
                            ft.Row([self.confirmar_password]),
                        ]
                    )
                )
            ]
        )
        super().__init__(model, view, controller)