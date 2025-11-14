import flet as ft
from flet_mvc import FletView
from colors import color_Docente, color_Background_PIE, color_Background_Docente

class CambiarPasswordView(FletView):
    def __init__(self, controller, model):
        self.feedback_snackbar = ft.SnackBar(content=ft.Text(""))
        self.nuevo_password = ft.TextField(label="Nueva contraseña", color="black", label_style=ft.TextStyle(color="black"), password=True, can_reveal_password=True)
        self.confirmar_password = ft.TextField(label="Confirmar nueva contraseña", color="black", label_style=ft.TextStyle(color="black"), password=True, can_reveal_password=True)
        self.guardar_button = ft.ElevatedButton(
            text="Guardar Cambios",
            on_click=controller.cambiar_contrasena,
            color="black",
            bgcolor=color_Docente
        )
        view = ft.View(
            "/cambiar_contrasena",
            scroll=ft.ScrollMode.AUTO,
            controls=[
                self.feedback_snackbar,
                ft.Row([ft.Text("Inicio >", weight=ft.FontWeight.BOLD, color="black"), ft.Text("Cambiar Contraseña", weight=ft.FontWeight.BOLD, color=color_Docente)], alignment=ft.MainAxisAlignment.START),
                ft.Container(
                    padding=20,
                    border_radius=10,
                    bgcolor=ft.Colors.with_opacity(0.5, "white"),
                    content=ft.Column(
                        [
                            ft.Text("Cambiar contraseña", size=20, weight=ft.FontWeight.BOLD, color="black"),
                            ft.Divider(),
                            self.nuevo_password,
                            self.confirmar_password,
                            ft.Row(
                                [
                                    self.guardar_button
                                ],
                                alignment=ft.MainAxisAlignment.END
                            )
                        ],
                        spacing=15
                    ),
                )
            ]
        )
        super().__init__(model, view, controller)