from flet_mvc import FletController
import flet as ft
from fpdf import FPDF
from datetime import datetime
import base64
import fitz

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

    def get_indicios_text(self, porcentaje, indicios_base):
        if porcentaje >= 70:
            return f"Indicios severos de: {indicios_base}"
        elif porcentaje >= 40:
            return f"Indicios moderados de: {indicios_base}"
        return "Sin indicios."

    def cargar_resultados_detallados(self, det_id):
        self.current_det_id = det_id
        
        # Si el usuario es PIE, puede ver cualquier resultado detallado por su ID.
        # Si no es PIE, solo puede ver los suyos.
        if self.model.datos_profesor.pro_cargo == 1: # Es PIE
            resultados_detallados = self.model.leer_resultados_detallados_by_det_id(det_id=det_id)
        else: # Es Docente
            resultados_detallados = self.model.leer_resultados_detallados_by_det_id(det_id=det_id, pro_id=self.model.datos_profesor.pro_nameID)

        if resultados_detallados:
            self.cargar_respuestas(resultados_detallados[0].id_test)
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

            self.view.indicios_atencion_val.value = self.get_indicios_text(resultados_detallados[0].det_porcentaje_atencion, self.indicios_atencion)
            self.view.indicios_memoria_val.value = self.get_indicios_text(resultados_detallados[0].det_porcentaje_memoria, self.indicios_memoria)
            self.view.indicios_social_val.value = self.get_indicios_text(resultados_detallados[0].det_porcentaje_social, self.indicios_social)
            self.view.indicios_emocional_val.value = self.get_indicios_text(resultados_detallados[0].det_porcentaje_emocional, self.indicios_emocional)

            self.view.puntaje_val.value = f"{resultados_detallados[0].det_puntaje}/{total_preguntas}"
            self.view.porcentaje_val.value = f"{resultados_detallados[0].det_porcentaje:.2f}%"

            self.page.update()
        
    def cargar_respuestas(self, test_id: int):
        self.current_test_id = test_id

        # Mapeo de categorías a sus respectivas tablas en la vista
        mapa_tablas = {
            "Atención": self.view.result_test_table_atencion,
            "Memoria": self.view.result_test_table_memoria,
            "Social": self.view.result_test_table_social,
            "Emocional": self.view.result_test_table_emocional,
        }
        

        # Limpiamos todas las tablas antes de llenarlas
        for tabla in mapa_tablas.values():
            tabla.rows.clear()
        # Obtenemos todas las respuestas guardadas para el test
        respuestas_guardadas = self.model.leer_respuestas(test_id)

        # Iteramos sobre cada categoría para llenar su tabla correspondiente
        for categoria, tabla_destino in mapa_tablas.items():
            preguntas_db = self.model.leer_preguntas(pre_cat=categoria)
            respuestas_usuario = []

            # Buscamos la cadena de respuestas combinada para la categoría actual
            for _, respuesta_combinada, tipo in respuestas_guardadas:
                if tipo == categoria and respuesta_combinada:
                    respuestas_usuario = respuesta_combinada.split(',')
                    break # Salimos del bucle una vez que encontramos la categoría

            # Llenamos la tabla con las preguntas y respuestas de la categoría
            for i, pregunta_info in enumerate(preguntas_db):
                pregunta_texto = pregunta_info[1]
                color_respuesta = ft.Colors.GREY

                if i < len(respuestas_usuario):
                    respuesta = respuestas_usuario[i].lower()
                    respuesta_texto = "Sí" if respuesta == 'si' else "No"
                    color_respuesta = ft.Colors.RED if respuesta == 'si' else ft.Colors.GREEN
                    
            
                tabla_destino.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(pregunta_texto)),
                        ft.DataCell(ft.Text(respuesta_texto, color=color_respuesta, weight=ft.FontWeight.BOLD)),
                    ])
                )
        
        self.page.update()

    def generar_y_navegar_pdf(self, e):
        if self.current_det_id is None:
            # Aquí podrías mostrar un snackbar de error si es necesario
            print("Error: No hay un ID de resultado detallado para generar el PDF.")
            return

        # --- Obtener datos para el PDF ---
        resultados = self.model.leer_resultados_detallados_by_det_id(det_id=self.current_det_id)
        if not resultados:
            print("Error al cargar los datos para el PDF.")
            return
        
        resultado = resultados[0]
        test_full = self.model.leer_test(resultado.id_test)
        estudiante = self.model.leer_estudiante_por_id(test_full[1])
        
        profesor_jefe_obj = self.model.cargar_profesor_id(estudiante.Pro_nameID) # Correcto: usar Pro_nameID del estudiante
        profesor_jefe = f"{profesor_jefe_obj.pro_nombre_1} {profesor_jefe_obj.pro_apellido_pat}" if profesor_jefe_obj else "N/A"

        profesor_emisor = self.model.cargar_profesor_id(test_full[2])

        nombre_completo_Es = f"{estudiante.es_nombre_1} {estudiante.es_nombre_2 or ''} {estudiante.es_apellido_pat} {estudiante.es_apellido_mat}".replace("  ", " ").strip()
        profesor_emisor_nombre = f"{profesor_emisor.pro_nombre_1} {profesor_emisor.pro_nombre_2 or ''} {profesor_emisor.pro_apellido_pat} {profesor_emisor.pro_apellido_mat}".replace("  ", " ").strip()

        total_preguntas = len(self.model.leer_preguntas(pre_cat="Atención")) + \
                          len(self.model.leer_preguntas(pre_cat="Memoria")) + \
                          len(self.model.leer_preguntas(pre_cat="Social")) + \
                          len(self.model.leer_preguntas(pre_cat="Emocional"))

        # --- Inicialización del PDF ---
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        col_width = pdf.w / 3.5 

        # --- Encabezado ---
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Informe de Derivación - Neuro Check", 0, 1, 'C')
        pdf.ln(10)

        pdf.set_fill_color(255, 0, 0)
        pdf.set_font("Arial", 'B', 10)
        
        pdf.cell(0, 10, "Datos del estudiante:", 0, 1, 'L')

        # --- Tabla Datos del Estudiante ---
        pdf.set_text_color(255, 255, 255)
        pdf.cell(col_width, 8, "Nombre Completo", 1, 0, 'C',fill=True)
        pdf.cell(col_width, 8, "RUT", 1, 0, 'C',fill=True)
        pdf.cell(col_width, 8, "Sexo", 1, 1, 'C',fill=True)
        
        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(0, 0, 0)

        cell_height_est = 10
        y_before_est = pdf.get_y()
        x_before_est = pdf.get_x()
        pdf.set_xy(x_before_est, y_before_est)
        pdf.multi_cell(col_width, cell_height_est, nombre_completo_Es, 1, 'C')
        y_after_nombre_est = pdf.get_y()
        height_est = y_after_nombre_est - y_before_est
        pdf.set_xy(x_before_est + col_width, y_before_est)
        pdf.cell(col_width, height_est, estudiante.es_rut, 1, 0, 'C')
        pdf.cell(col_width, height_est, "Masculino" if estudiante.es_sexo == 1 else "Femenino", 1, 1, 'C')
        pdf.set_y(y_after_nombre_est)
        pdf.ln(0)

        pdf.set_font("Arial", 'B', 10)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(col_width, 8, "Fecha de Nacimiento", 1, 0, 'C',fill=True)
        pdf.cell(col_width, 8, "Curso", 1, 0, 'C',fill=True)
        pdf.cell(col_width, 8, "Repitencias", 1, 1, 'C',fill=True)

        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(col_width, 8, estudiante.es_nacimiento.strftime('%Y-%m-%d'), 1, 0, 'C')
        pdf.cell(col_width, 8, resultado.lvl_curso, 1, 0, 'C')
        pdf.cell(col_width, 8, "xxxx", 1, 1, 'C')
        pdf.ln(0)

        pdf.set_font("Arial", 'B', 10)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(col_width * 3, 8, "Profesor Jefe", 1, 1, 'C',fill=True)
        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(col_width * 3, 8, profesor_jefe, 1, 1, 'C')
        pdf.ln(2)

        # --- Tabla Profesor Emisor ---
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 10, "Profesor emisor del test:", 0, 1, 'L')
        pdf.set_text_color(255, 255, 255)
        pdf.cell(col_width, 10, "Nombre Docente", 1, 0, 'C',fill=True)
        pdf.cell(col_width, 10, "Rut", 1, 0, 'C',fill=True)
        pdf.cell(col_width, 10, "Cargo", 1, 1, 'C',fill=True)

        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(0, 0, 0)

        cell_height_emi = 10 
        y_before_emi = pdf.get_y()
        x_before_emi = pdf.get_x()
        pdf.set_xy(x_before_emi, y_before_emi)
        pdf.multi_cell(col_width, cell_height_emi, profesor_emisor_nombre, 1, 'C')
        y_after_nombre_emi = pdf.get_y()
        height_emi = y_after_nombre_emi - y_before_emi
        pdf.set_xy(x_before_emi + col_width, y_before_emi) 
        pdf.cell(col_width, height_emi, profesor_emisor.pro_rut, 1, 0, 'C')
        pdf.cell(col_width, height_emi, "Profesional PIE" if profesor_emisor.pro_cargo == 1 else "Profesor Docente", 1, 1, 'C')
        pdf.set_y(y_after_nombre_emi)

        pdf.set_font("Arial", 'B', 10)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(col_width * 3, 8, "Fecha de Informe", 1, 1, 'C', fill=True)
        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(col_width * 3, 8, datetime.now().strftime('%Y-%m-%d'), 1, 1, 'C')
        pdf.ln(2)

        # --- Resultados del Test ---
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 10, "Resultados del Test:", 0, 1, 'L')
        
        col_width_res = pdf.w / 2.33 
        pdf.set_text_color(255, 255, 255)
        pdf.cell(col_width_res, 8, "Puntaje Obtenido", 1, 0, 'C', fill=True)
        pdf.cell(col_width_res, 8, "Porcentaje de Riesgo", 1, 1, 'C', fill=True)

        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(col_width_res, 8, f"{resultado.det_puntaje}/{total_preguntas}", 1, 0, 'C')
        pdf.cell(col_width_res, 8, f"{resultado.det_porcentaje}%", 1, 1, 'C')
        
        pdf.ln(0)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(col_width, 8, "Categoría", 1, 0, 'C', fill=True)
        pdf.cell(col_width, 8, "Porcentaje de Riesgo", 1, 0, 'C', fill=True)
        pdf.cell(col_width, 8, "Indicios Detectados", 1, 1, 'C', fill=True)

        pdf.set_font("Arial", '', 9)
        pdf.set_text_color(0, 0, 0)
        cell_height_indicios = 5 

        def draw_dynamic_row(category_name, porcentaje_val, indicios_val):
            estimated_min_height = 4 * cell_height_indicios 
            page_break_margin = 15
            if pdf.get_y() + estimated_min_height > (pdf.h - page_break_margin):
                 pdf.add_page()
                 pdf.set_text_color(255, 255, 255)
                 pdf.set_font("Arial", 'B', 10)
                 pdf.cell(col_width, 8, "Categoría", 1, 0, 'C', fill=True)
                 pdf.cell(col_width, 8, "Porcentaje de Riesgo", 1, 0, 'C', fill=True)
                 pdf.cell(col_width, 8, "Indicios Detectados", 1, 1, 'C', fill=True)
                 pdf.set_font("Arial", '', 9)
                 pdf.set_text_color(0, 0, 0)

            x_start, y_start = pdf.get_x(), pdf.get_y()
            pdf.set_xy(x_start + col_width * 2, y_start) 
            pdf.multi_cell(col_width, cell_height_indicios, indicios_val, 1, 'L') 
            y_end = pdf.get_y()
            row_height = y_end - y_start
            pdf.set_xy(x_start, y_start) 
            pdf.cell(col_width, row_height, category_name, 1, 0, 'C') 
            pdf.cell(col_width, row_height, porcentaje_val, 1, 0, 'C') 
            pdf.set_y(y_end)

        draw_dynamic_row("Atención", f"{resultado.det_porcentaje_atencion:.2f}%", self.get_indicios_text(resultado.det_porcentaje_atencion, self.indicios_atencion))
        draw_dynamic_row("Memoria", f"{resultado.det_porcentaje_memoria:.2f}%", self.get_indicios_text(resultado.det_porcentaje_memoria, self.indicios_memoria))
        draw_dynamic_row("Social", f"{resultado.det_porcentaje_social:.2f}%", self.get_indicios_text(resultado.det_porcentaje_social, self.indicios_social))
        draw_dynamic_row("Emocional", f"{resultado.det_porcentaje_emocional:.2f}%", self.get_indicios_text(resultado.det_porcentaje_emocional, self.indicios_emocional))

        pdf.ln(10)
        
        # --- Guardar el PDF en la BD ---
        file_name = f"informe_estudiante_{self.current_det_id}.pdf"
        pdf_output_bytes = pdf.output(dest="S").encode("latin-1")
        pdf_id = self.model.crear_documento_pdf(file_name, ".pdf", pdf_output_bytes)

        if pdf_id:
            # --- Navegar a la vista de exportación solo si el PDF se guardó correctamente ---
            self.page.go(f"/export_pdf/{self.current_det_id}")
        else:
            print("Error: No se pudo guardar el PDF en la base de datos.")