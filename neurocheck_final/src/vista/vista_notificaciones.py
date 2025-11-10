import flet as ft
from flet_mvc import FletView
from colors import color_Docente, color_Background_PIE

class NotificacionesView(FletView):
    def __init__(self, controller, model):
        self.page = controller.page
        self.list_view = ft.ListView(expand=True, spacing=10, padding=20)
        
        view = ft.View(
            "/notificaciones",
            controls=[
                ft.Row(
                    [
                        self.list_view
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ],
            bgcolor=color_Background_PIE,
        )
        super().__init__(model, view, controller)

    def build_notification_list(self, notifications):
        self.list_view.controls.clear()
        if not notifications:
            self.list_view.controls.append(
                ft.Text("No tienes notificaciones.", size=18, text_align=ft.TextAlign.CENTER)
            )
        else:
            for notif in notifications:
                self.list_view.controls.append(
                    ft.Card(
                        content=ft.Container(
                            padding=15,
                            content=ft.Row(
                                [
                                    ft.Icon(ft.Icons.CIRCLE, color=ft.Colors.RED if notif.not_status == 0 else ft.Colors.TRANSPARENT, size=12),
                                    ft.Text(notif.not_mensaje, expand=True, weight=ft.FontWeight.BOLD if notif.not_status == 0 else ft.FontWeight.NORMAL),
                                    ft.Text(notif.noti_fecha_creacion.strftime("%d/%m/%Y %H:%M")),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            on_click=self.controller.on_notification_click,
                            data=notif,
                        )
                    )
                )