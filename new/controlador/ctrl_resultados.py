from flet_mvc import FletController
import flet as ft
from datetime import datetime

class ResultadosController(FletController):
    def __init__(self, page, model):
        super().__init__(page, model)
        self.current_test_id = None
        self.puntaje = 0
        self.porcentaje = 0
        self.porcentaje_atencion = 0
        self.porcentaje_memoria = 0
        self.porcentaje_social = 0
        self.porcentaje_emocional = 0

        self.indicios_atencion = "Trastorno por Déficit de Atención con Hiperactividad (TDAH) (Tipo inatento, hiperactivo o combinado). Dificultades de Función Ejecutiva."
        self.indicios_memoria = "Dificultades Específicas del Aprendizaje (DEA) (dislexia, discalculia, si se asocia a fallas académicas). Déficit en Memoria Operativa o a Corto Plazo."
        self.indicios_social = "Déficit en Habilidades Sociales. Trastorno del Espectro Autista (TEA). Problemas de Conducta (incluyendo Trastorno Negativista Desafiante - TND)."
        self.indicios_emocional = "Trastorno de Ansiedad Generalizada o Específico. Depresión Infantil o Dificultad de Adaptación. Dificultad en Regulación Emocional."

        

    def calcular_resultados(self, test_id: int):
        self.current_test_id = test_id
        respuestas_del_test = self.model.leer_respuestas(test_id)
        
        puntaje = 0
        total_preguntas = 0
        total_preguntas_atencion = 0
        puntaje_atencion = 0
        total_preguntas_memoria = 0
        puntaje_memoria = 0
        total_preguntas_social = 0
        puntaje_social = 0
        total_preguntas_emocional = 0
        puntaje_emocional = 0
        # Mapa de categorías y sus respuestas guardadas
        mapa_respuestas = {
            "Atención": respuestas_del_test[0][1].split(',') if respuestas_del_test and len(respuestas_del_test) > 0 and respuestas_del_test[0][1] else [],
            "Memoria": respuestas_del_test[1][1].split(',') if respuestas_del_test and len(respuestas_del_test) > 1 and respuestas_del_test[1][1] else [],
            "Social": respuestas_del_test[2][1].split(',') if respuestas_del_test and len(respuestas_del_test) > 2 and respuestas_del_test[2][1] else [],
            "Emocional": respuestas_del_test[3][1].split(',') if respuestas_del_test and len(respuestas_del_test) > 3 and respuestas_del_test[3][1] else [],
        }

        preguntas_db_atencion = self.model.leer_preguntas(pre_cat="Atención")
        respuestas_atencion = mapa_respuestas.get("Atención", [2])
        respuesta_atencion_test = []

        preguntas_db_memoria = self.model.leer_preguntas(pre_cat="Memoria")
        respuestas_memoria = mapa_respuestas.get("Memoria", [2])
        respuesta_memoria_test = []

        preguntas_db_social = self.model.leer_preguntas(pre_cat="Social")
        respuestas_social = mapa_respuestas.get("Social", [2])
        respuesta_social_test = []

        preguntas_db_emocional = self.model.leer_preguntas(pre_cat="Emocional")
        respuestas_emocional = mapa_respuestas.get("Emocional", [2])
        respuesta_emocional_test = []


        for i in preguntas_db_atencion:
            respuesta_atencion_test.append(i[2])
            total_preguntas_atencion += 1

        for respuesta_correcta, respuesta_usuario in zip(respuestas_atencion, respuesta_atencion_test):
                if respuesta_correcta == respuesta_usuario:
                    puntaje_atencion += 1


        for i in preguntas_db_memoria:
            respuesta_memoria_test.append(i[2])
            total_preguntas_memoria += 1


        for respuesta_correcta, respuesta_usuario in zip(respuestas_memoria, respuesta_memoria_test):
                if respuesta_correcta == respuesta_usuario:
                    puntaje_memoria += 1

        for i in preguntas_db_social:
            respuesta_social_test.append(i[2])
            total_preguntas_social += 1

        for respuesta_correcta, respuesta_usuario in zip(respuestas_social, respuesta_social_test):
                if respuesta_correcta == respuesta_usuario:
                    puntaje_social += 1

        for i in preguntas_db_emocional:
            respuesta_emocional_test.append(i[2])
            total_preguntas_emocional += 1

        for respuesta_correcta, respuesta_usuario in zip(respuestas_emocional, respuesta_emocional_test):
                if respuesta_correcta == respuesta_usuario:
                    puntaje_emocional += 1

        total_preguntas = total_preguntas_atencion + total_preguntas_memoria + total_preguntas_social + total_preguntas_emocional
        puntaje = puntaje_atencion + puntaje_memoria + puntaje_social + puntaje_emocional
        
        self.porcentaje_atencion = (puntaje_atencion / total_preguntas_atencion) * 100 if total_preguntas_atencion > 0 else 0
        self.porcentaje_memoria = (puntaje_memoria / total_preguntas_memoria) * 100 if total_preguntas_memoria > 0 else 0
        self.porcentaje_social = (puntaje_social / total_preguntas_social) * 100 if total_preguntas_social > 0 else 0
        self.porcentaje_emocional = (puntaje_emocional / total_preguntas_emocional) * 100 if total_preguntas_emocional > 0 else 0

        self.puntaje = puntaje
        self.porcentaje = (puntaje / total_preguntas) * 100 if total_preguntas > 0 else 0
        
        # Función auxiliar para generar el texto de indicios
        def get_indicios_text(porcentaje, indicios_base):
            if porcentaje >= 70:
                return f"Indicios severos de: {indicios_base}"
            elif porcentaje >= 40:
                return f"Indicios moderados de: {indicios_base}"
            return "Sin indicios."

        # Generar texto de indicios para cada categoría
        indi_text_atencion = get_indicios_text(self.porcentaje_atencion, self.indicios_atencion)
        indi_text_memoria = get_indicios_text(self.porcentaje_memoria, self.indicios_memoria)
        indi_text_social = get_indicios_text(self.porcentaje_social, self.indicios_social)
        indi_text_emocional = get_indicios_text(self.porcentaje_emocional, self.indicios_emocional)

        # Actualizar la vista
        self.view.porcentaje_val.value = f"{self.porcentaje:.2f}%"
        self.view.porcentaje_atencion_val.value = indi_text_atencion
        self.view.porcentaje_memoria_val.value = indi_text_memoria
        self.view.porcentaje_social_val.value = indi_text_social
        self.view.porcentaje_emocional_val.value = indi_text_emocional
        self.page.update()

    def guardar_test(self, e):
        """Guarda los resultados y marca el test como finalizado."""
        if self.current_test_id is None: 
            
            self.page.go("/resultados_detallados")


        # 1. Actualizar estado y fecha del test
        self.model.actualizar_test(self.current_test_id, {
            "test_status": 1,
            "test_fecha_termino": datetime.now()
        })

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
        
        respuestas = self.model.leer_respuestas(self.current_test_id)
        for pre_id, _, _ in respuestas:
            self.model.actualizar_respuesta(pre_id, {"pre_respuesta": None})
        
        self.cerrar_dialogo('rehacer')
        self.page.go(f"/test/{self.current_test_id}")

    def eliminar_test(self, e):
        if self.current_test_id is None: return

        self.model.eliminar_respuestas_por_test(self.current_test_id)
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
