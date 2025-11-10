from flet_mvc import FletController
import flet as ft

class NotificacionesController(FletController):
    def __init__(self, page, model):
        super().__init__(page, model)

    def cargar_notificaciones(self):
        """Carga las notificaciones no leídas para el usuario actual."""
        if not self.model.datos_profesor:
            return

        pro_id = self.model.datos_profesor.pro_nameID
        notificaciones = self.model.leer_notificaciones(pro_id, solo_no_leidas=True)

        # Actualizar el contador del badge
        self.view.badge.text = str(len(notificaciones))
        self.view.badge.visible = len(notificaciones) > 0

        # Limpiar y llenar el menú de notificaciones
        self.view.menu_notificaciones.items.clear()
        if notificaciones:
            for notif in notificaciones:
                self.view.menu_notificaciones.items.append(
                    ft.PopupMenuItem(
                        text=f"{notif.not_mensaje}\n{notif.not_fecha.strftime('%Y-%m-%d %H:%M')}",
                        data=notif,
                        on_click=self.on_notificacion_click
                    )
                )
        else:
            self.view.menu_notificaciones.items.append(ft.PopupMenuItem(text="No hay notificaciones nuevas", disabled=True))
        
        self.page.update()

    def on_notificacion_click(self, e):
        notif = e.control.data
        self.model.marcar_notificacion_leida(notif.not_id)
        self.cargar_notificaciones() # Recargar para actualizar la lista y el contador
        if notif.not_enlace:
            self.page.go(notif.not_enlace)