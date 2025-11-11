from flet_mvc import FletController
import flet as ft
from datetime import datetime

class NotificacionesController(FletController):
    def __init__(self, page, model):
        super().__init__(page, model)
        self.view = None

    def cargar_notificaciones(self):
        if self.model.datos_profesor and self.model.datos_profesor.pro_cargo == 1:
            prof_id = self.model.datos_profesor.pro_nameID
            notificaciones = self.model.leer_notificaciones(prof_id=prof_id, solo_no_leidas=False)
            
            self.view.notification_list.controls.clear()
            if not notificaciones:
                self.view.notification_list.controls.append(
                    ft.Text("No tienes notificaciones.", size=18, text_align=ft.TextAlign.CENTER)
                )
            else:
                for notif in notificaciones:
                    self.view.notification_list.controls.append(
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
                                on_click=self.on_notification_click,
                                data=notif,
                            )
                        )
                    )
            self.page.update()

    def on_notification_click(self, e):
        notif_data = e.control.data
        det_id = notif_data.id_resultados_detallados
        not_id = notif_data.noti_ID
        self.model.marcar_notificacion_leida(not_id)
        if det_id:
            self.page.go(f"/resultados_detallados/{det_id}")

    def eliminar_leidas(self, e):
        if self.model.datos_profesor and self.model.datos_profesor.pro_cargo == 1:
            prof_id = self.model.datos_profesor.pro_nameID
            success = self.model.eliminar_notificaciones(prof_id=prof_id, not_status=1)
            if success:
                self.view.show_feedback("Notificaciones leídas eliminadas.", ft.Colors.GREEN)
                self.cargar_notificaciones() # Recargar la lista
            else:
                self.view.show_feedback("Error al eliminar las notificaciones.", ft.Colors.RED)
            self.page.update()