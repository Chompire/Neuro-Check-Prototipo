import flet as ft
from flet_mvc import FletView
from colors import color_Docente, color_Background_PIE

class NotificacionesView(FletView):
    def __init__(self, controller, model):
        self.page = controller.page
        self.notification_list = ft.ListView(expand=True, spacing=10, padding=20)
        self.feedback_snackbar = ft.SnackBar(content=ft.Text(""))
        
        view = ft.View(
            "/notificaciones",
            controls=[
                ft.Row([ft.Text("Inicio >", weight=ft.FontWeight.BOLD, color="black"), ft.Text("Notificaciones", weight=ft.FontWeight.BOLD, color=color_Docente)], alignment=ft.MainAxisAlignment.START),
                self.feedback_snackbar,
                ft.Column(
                    expand=True,
                    controls=[
                        ft.Row(
                            [
                                ft.Text("Bandeja de Notificaciones", size=20, weight=ft.FontWeight.BOLD, color="black"),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_SWEEP,
                                    icon_color=ft.Colors.RED_400,
                                    tooltip="Eliminar notificaciones leídas",
                                    on_click=controller.eliminar_leidas,
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        ft.Divider(),
                        self.notification_list,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            ],
            bgcolor=color_Background_PIE,
        )
        super().__init__(model, view, controller)

    def show_feedback(self, message, color):
        self.feedback_snackbar.content = ft.Text(message)
        self.feedback_snackbar.bgcolor = color
        self.feedback_snackbar.open = True
        self.page.update()