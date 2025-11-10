import flet as ft
from flet_mvc import FletView

class NotificacionesView(FletView):
    def __init__(self, controller, model):
        self.menu_notificaciones = ft.PopupMenuButton(
            icon=ft.icons.NOTIFICATIONS_OUTLINED,
            items=[
                ft.PopupMenuItem(text="Cargando...", disabled=True)
            ]
        )

        self.badge = ft.Badge(
            text="0",
            right=0,
            top=0
        )
        self.badge.visible = False

        view = ft.View(
            "/notificaciones",
            controls=
            [
                self.menu_notificaciones,
                self.badge,
            ]
        )

        super().__init__(model, view, controller)