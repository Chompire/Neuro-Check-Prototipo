from flet_mvc import FletController
import flet as ft

class ResultadosDetalladosController(FletController):
    def __init__(self, page, model):
        super().__init__(page, model)
        self.current_test_id = None
        self.current_det_id = None

        self.puntaje = 0
        self.porcentaje = 0
        self.porcentaje_atencion = 0
        self.porcentaje_memoria = 0
        self.porcentaje_social = 0
        self.porcentaje_emocional = 0
        self.resultados_detallados_id = None
    
        self.indicios_atencion = "Trastorno por Déficit de Atención con Hiperactividad (TDAH) (Tipo inatento, hiperactivo o combinado). Dificultades de Función Ejecutiva."
        self.indicios_memoria = "Dificultades Específicas del Aprendizaje (DEA) (dislexia, discalculia, si se asocia a fallas académicas). Déficit en Memoria Operativa o a Corto Plazo."
        self.indicios_social = "Déficit en Habilidades Sociales. Trastorno del Espectro Autista (TEA). Problemas de Conducta (incluyendo Trastorno Negativista Desafiante - TND)."
        self.indicios_emocional = "Trastorno de Ansiedad Generalizada o Específico. Depresión Infantil o Dificultad de Adaptación. Dificultad en Regulación Emocional."
    def cargar_resultados_detallados(self, det_id):
        self.current_det_id = det_id
        resultados_detallados = self.model.leer_resultados_detallados_by_det_id(det_id, self.model.datos_profesor.pro_nameID)
        if resultados_detallados:
            self.view.datatable.rows.clear()
            for resultado in resultados_detallados:
                self.view.datatable.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(resultado.det_nameES)),
                            ft.DataCell(ft.Text(resultado.det_apellidoES)),
                            ft.DataCell(ft.Text(resultado.lvl_curso)),
                            ft.DataCell(ft.Text(resultado.det_fecha))
                        ]
                    )
                )
            total_preguntas_atencion = len(self.model.leer_preguntas(pre_cat="Atención"))
            total_preguntas_memoria = len(self.model.leer_preguntas(pre_cat="Memoria"))
            total_preguntas_social = len(self.model.leer_preguntas(pre_cat="Social"))
            total_preguntas_emocional = len(self.model.leer_preguntas(pre_cat="Emocional"))
            total_preguntas = total_preguntas_atencion + total_preguntas_memoria + total_preguntas_social + total_preguntas_emocional
            self.view.porcentaje_atencion_val.value = f"{resultados_detallados[0].det_porcentaje_atencion:.2f}%"
            self.view.porcentaje_memoria_val.value = f"{resultados_detallados[0].det_porcentaje_memoria:.2f}%"
            self.view.porcentaje_social_val.value = f"{resultados_detallados[0].det_porcentaje_social:.2f}%"
            self.view.porcentaje_emocional_val.value = f"{resultados_detallados[0].det_porcentaje_emocional:.2f}%"

            

            def get_indicios_text(porcentaje, indicios_base):
                if porcentaje >= 70:
                    return f"Indicios severos de: {indicios_base}"
                elif porcentaje >= 40:
                    return f"Indicios moderados de: {indicios_base}"
                return "Sin indicios."
                self.page.update()

        self.view.indicios_atencion_val.value = get_indicios_text(resultados_detallados[0].det_porcentaje_atencion, self.indicios_atencion)
        self.view.indicios_memoria_val.value = get_indicios_text(resultados_detallados[0].det_porcentaje_memoria, self.indicios_memoria)
        self.view.indicios_social_val.value = get_indicios_text(resultados_detallados[0].det_porcentaje_social, self.indicios_social)
        self.view.indicios_emocional_val.value = get_indicios_text(resultados_detallados[0].det_porcentaje_emocional, self.indicios_emocional)

        self.view.puntaje_val.value = f"{resultados_detallados[0].det_puntaje}/{total_preguntas}"
        print(resultados_detallados[0].det_porcentaje)
        self.view.porcentaje_val.value = f"{resultados_detallados[0].det_porcentaje:.2f}%"
