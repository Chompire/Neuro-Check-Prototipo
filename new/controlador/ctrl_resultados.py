from flet_mvc import FletController
import flet as ft
from datetime import datetime

class ResultadosController(FletController):
    def __init__(self, page, model):
        super().__init__(page, model)
        self.current_test_id = None
        self.puntaje = 0
        self.porcentaje = 0

    def calcular_resultados(self, test_id: int):
        """Calcula el puntaje y porcentaje del test."""
        self.current_test_id = test_id
        preguntas_del_test = self.model.leer_preguntas(test_id)

        puntaje = 0
        total_preguntas_respondidas = 0

        for _, respuesta, _ in preguntas_del_test:
            if respuesta is not None:
                total_preguntas_respondidas += 1
                if respuesta == "si":
                    puntaje += 1

        self.puntaje = puntaje
        self.porcentaje = (puntaje / len(preguntas_del_test)) * 100 if preguntas_del_test else 0
        
        # Actualizar la vista
        self.view.porcentaje_val.value = f"{self.porcentaje:.2f}%"
        self.page.update()

    def guardar_test(self, e):
        """Guarda los resultados y marca el test como finalizado."""
        if self.current_test_id is None: return

        # 1. Actualizar estado y fecha del test
        self.model.actualizar_test(self.current_test_id, {
            "test_status": 1,
            "test_fecha_termino": datetime.now()
        })

        # 2. Crear registro en la tabla de resultados detallados
        test_info = self.model.leer_info_test(self.current_test_id)
        if test_info:
            detalles_data = (
                test_info.es_nombre_1,
                test_info.es_apellido_pat,
                test_info.cur_nombre,
                test_info.pro_nombre_1,
                test_info.pro_apellido_pat,
                self.porcentaje,
                self.puntaje,
                datetime.now().date(),
                self.current_test_id
            )
            self.model.crear_resultado_detallado(*detalles_data)

        self.view.save_snackbar.content = ft.Text("Resultados guardados exitosamente.")
        self.view.save_snackbar.open = True
        self.page.update()
        self.page.go("/realizar_test")

    def rehacer_test(self, e):
        """Borra las respuestas y regresa a la pantalla del test."""
        if self.current_test_id is None: return
        
        preguntas = self.model.leer_preguntas(self.current_test_id)
        for pre_id, _, _ in preguntas:
            self.model.actualizar_pregunta(pre_id, {"pre_respuesta": None})
        
        self.cerrar_dialogo('rehacer')
        self.page.go(f"/test/{self.current_test_id}")

    def eliminar_test(self, e):
        """Elimina el test y todas sus preguntas asociadas."""
        if self.current_test_id is None: return

        self.model.eliminar_preguntas_por_test(self.current_test_id)
        self.model.eliminar_test(self.current_test_id)
        
        self.cerrar_dialogo('eliminar')
        self.page.go("/realizar_test")

    def abrir_dialogo(self, tipo: str):
        dialog = self.view.rework_alert if tipo == 'rehacer' else self.view.delete_alert
        dialog.open = True
        self.page.update()

    def cerrar_dialogo(self, tipo: str):
        dialog = self.view.rework_alert if tipo == 'rehacer' else self.view.delete_alert
        dialog.open = False
        self.page.update()
