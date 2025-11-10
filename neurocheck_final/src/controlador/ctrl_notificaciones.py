from flet_mvc import FletController

class NotificacionesController(FletController):
    def __init__(self, page, model):
        super().__init__(page, model)
        self.view = None

    def cargar_notificaciones(self):
        """Carga todas las notificaciones (leídas y no leídas) para el profesor PIE."""
        if self.model.datos_profesor and self.model.datos_profesor.pro_cargo == 1:
            prof_id = self.model.datos_profesor.pro_nameID
            # Pasamos solo_no_leidas=False para obtener todas
            notificaciones = self.model.leer_notificaciones(prof_id=prof_id, solo_no_leidas=False)
            self.view.build_notification_list(notificaciones)

    def on_notification_click(self, e):
        """Maneja el clic en una notificación, la marca como leída y navega a los detalles."""
        notif_data = e.control.data
        det_id = notif_data.id_resultados_detallados
        not_id = notif_data.noti_ID
        self.model.marcar_notificacion_leida(not_id)
        if det_id:
            self.page.go(f"/resultados_detallados/{det_id}")