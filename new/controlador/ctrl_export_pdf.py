from flet_mvc import FletController
import flet as ft
from fpdf import FPDF
from datetime import datetime

class ExportPDFController(FletController):
    def __init__(self, page, model):
        self.selected_est_id = None
        self.res_det_id = None
        super().__init__(page, model)

    def get_indicios_text(self, porcentaje, indicios_base):
        if porcentaje >= 70:
            return f"Indicios severos de: {indicios_base}"
        elif porcentaje >= 40:
            return f"Indicios moderados de: {indicios_base}"
        return "Sin indicios."
    def cargar_alumno(self, res_det_id: int):
        self.res_det_id = res_det_id

        # Leer los resultados detallados usando el ID
        resultados = self.model.leer_resultados_detallados_by_det_id(det_id=res_det_id)
        prof_id = self.model.datos_profesor.pro_nameID

        if resultados:
            resultado = resultados[0]
            test_id = resultado.id_test
            test_full = self.model.leer_test(test_id)
            estudiante_id = test_full[1]
            estudiante = self.model.leer_estudiante_por_id(estudiante_id)
            profesor_jefe = f"{estudiante[13]} {estudiante[14]}"

            profesor_emisor_id = test_full[2]
            profesor_emisor = self.model.cargar_profesor_id(profesor_emisor_id)

            
            if estudiante.es_nombre_3 is None:
                nombre_completo_Es = f"{estudiante.es_nombre_1} {estudiante.es_nombre_2} {estudiante.es_apellido_pat} {estudiante.es_apellido_mat}"
            else:
                nombre_completo_Es = f"{estudiante.es_nombre_1} {estudiante.es_nombre_2} {estudiante.es_nombre_3} {estudiante.es_apellido_pat} {estudiante.es_apellido_mat}"

            self.view.nombre_completo_es.value = nombre_completo_Es
            self.view.rut_es.value = estudiante.es_rut
            self.view.sexo_es.value = "Masculino" if estudiante.es_sexo == 1 else "Femenino"
            self.view.curso_es.value = resultado.lvl_curso
            self.view.fecha_nacimiento_es.value = estudiante.es_nacimiento.strftime('%Y-%m-%d')

            total_preguntas_atencion = len(self.model.leer_preguntas(pre_cat="Atención"))
            total_preguntas_memoria = len(self.model.leer_preguntas(pre_cat="Memoria"))
            total_preguntas_social = len(self.model.leer_preguntas(pre_cat="Social"))
            total_preguntas_emocional = len(self.model.leer_preguntas(pre_cat="Emocional"))
            total_preguntas = total_preguntas_atencion + total_preguntas_memoria + total_preguntas_social + total_preguntas_emocional

            if profesor_emisor.pro_nombre_3 is None:
                profesor_emisor_nombre = f"{profesor_emisor.pro_nombre_1} {profesor_emisor.pro_nombre_2} {profesor_emisor.pro_apellido_pat} {profesor_emisor.pro_apellido_mat}"
            else:
                profesor_emisor_nombre = f"{profesor_emisor.pro_nombre_1} {profesor_emisor.pro_nombre_2} {profesor_emisor.pro_nombre_3} {profesor_emisor.pro_apellido_pat} {profesor_emisor.pro_apellido_mat}"
            
            self.view.profesor_jefe.value = profesor_jefe

            self.view.profesor_emisor_nombre.value = profesor_emisor_nombre
            self.view.profesor_emisor_rut.value = profesor_emisor.pro_rut
            self.view.profesor_emisor_cargo.value = "Profesor Diferencial" if profesor_emisor.pro_cargo == 1 else "Profesor Docente"

            self.view.fecha_informe.value = datetime.now().strftime('%Y-%m-%d')

            self.view.puntaje_obtenido.value = f"{resultados[0].det_puntaje}/{total_preguntas}"
            self.view.porcentaje_riesgo.value = f"{resultados[0].det_porcentaje}%"

            # Cargar porcentajes por categoría
            self.view.porcentaje_atencion.value = f"{resultados[0].det_porcentaje_atencion:.2f}%"
            self.view.porcentaje_memoria.value = f"{resultados[0].det_porcentaje_memoria:.2f}%"
            self.view.porcentaje_social.value = f"{resultados[0].det_porcentaje_social:.2f}%"
            self.view.porcentaje_emocional.value = f"{resultados[0].det_porcentaje_emocional:.2f}%"

            # Cargar indicios
            indicios_atencion_base = "Trastorno por Déficit de Atención con Hiperactividad (TDAH) (Tipo inatento, hiperactivo o combinado). Dificultades de Función Ejecutiva."
            indicios_memoria_base = "Dificultades Específicas del Aprendizaje (DEA) (dislexia, discalculia, si se asocia a fallas académicas). Déficit en Memoria Operativa o a Corto Plazo."
            indicios_social_base = "Déficit en Habilidades Sociales. Trastorno del Espectro Autista (TEA). Problemas de Conducta (incluyendo Trastorno Negativista Desafiante - TND)."
            indicios_emocional_base = "Trastorno de Ansiedad Generalizada o Específico. Depresión Infantil o Dificultad de Adaptación. Dificultad en Regulación Emocional."

            self.view.indicios_atencion.value = self.get_indicios_text(resultados[0].det_porcentaje_atencion, indicios_atencion_base)
            self.view.indicios_memoria.value = self.get_indicios_text(resultados[0].det_porcentaje_memoria, indicios_memoria_base)
            self.view.indicios_social.value = self.get_indicios_text(resultados[0].det_porcentaje_social, indicios_social_base)
            self.view.indicios_emocional.value = self.get_indicios_text(resultados[0].det_porcentaje_emocional, indicios_emocional_base)
            self.page.update()

    def generar_pdf(self, e):
        if self.res_det_id is None:
            self.view.feedback_text.value = "Error: No se ha cargado un alumno para generar el PDF."
            self.view.feedback_text.color = ft.colors.RED
            self.page.update()
            return
            
        self.view.feedback_text.value = ""

        # --- Inicialización del PDF ---
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Se utiliza un ancho de columna general (col_width) para las tablas de 3 columnas
        col_width = pdf.w / 3.5 

        # --- Encabezado ---
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Informe de Derivación - Neuro Check", 0, 1, 'C')
        pdf.ln(10)

        pdf.set_fill_color(255, 0, 0)
        pdf.set_font("Arial", 'B', 10)
        
        pdf.cell(0, 10, "Datos del estudiante:", 0, 1, 'L')

        # --- Tabla Datos del Estudiante (Encabezados) ---
        pdf.set_text_color(255, 255, 255)
        pdf.cell(col_width, 8, "Nombre Completo", 1, 0, 'C',fill=True)
        pdf.cell(col_width, 8, "RUT", 1, 0, 'C',fill=True)
        pdf.cell(col_width, 8, "Sexo", 1, 1, 'C',fill=True)

        
        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(0, 0, 0)

        # ----------------------------------------------------
        # Fila Datos del Estudiante (CORRECCIÓN DE DUPLICACIÓN)
        # ----------------------------------------------------
        cell_height_est = 10 # Altura de línea base para multi_cell de estudiante
        y_before_est = pdf.get_y()
        x_before_est = pdf.get_x()

        # 1. Dibuja la celda del Nombre con multi_cell (Borde 1 y contenido)
        pdf.set_xy(x_before_est, y_before_est)
        pdf.multi_cell(col_width, cell_height_est, self.view.nombre_completo_es.value, 1, 'C') # Borde 1, imprime texto 1 vez
        y_after_nombre_est = pdf.get_y()
        height_est = y_after_nombre_est - y_before_est

        # 2. Dibuja las celdas contiguas, comenzando en la segunda columna.
        pdf.set_xy(x_before_est + col_width, y_before_est)
        pdf.cell(col_width, height_est, self.view.rut_es.value, 1, 0, 'C')
        pdf.cell(col_width, height_est, self.view.sexo_es.value, 1, 1, 'C') # 3ra Col, salta línea
        pdf.set_y(y_after_nombre_est) # Vuelve a la Y final
        pdf.ln(0)

        # --- Tabla de Nacimiento/Curso/Repitencias ---
        pdf.set_font("Arial", 'B', 10)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(col_width, 8, "Fecha de Nacimiento", 1, 0, 'C',fill=True)
        pdf.cell(col_width, 8, "Curso", 1, 0, 'C',fill=True)
        pdf.cell(col_width, 8, "Repitencias", 1, 1, 'C',fill=True)

        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(col_width, 8, self.view.fecha_nacimiento_es.value, 1, 0, 'C')
        pdf.cell(col_width, 8, self.view.curso_es.value, 1, 0, 'C')
        pdf.cell(col_width, 8, "xxxx", 1, 1, 'C')
        pdf.ln(0)

        # --- Tabla 3: Profesor Jefe ---
        pdf.set_font("Arial", 'B', 10)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(col_width * 3, 8, "Profesor Jefe", 1, 1, 'C',fill=True)

        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(col_width * 3, 8, self.view.profesor_jefe.value, 1, 1, 'C')
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

        # ----------------------------------------------------
        # Fila Datos del Emisor (CORRECCIÓN DE DUPLICACIÓN)
        # ----------------------------------------------------
        cell_height_emi = 10 
        y_before_emi = pdf.get_y()
        x_before_emi = pdf.get_x()
        
        # 1. Dibuja la celda del Nombre con multi_cell (Borde 1 y contenido)
        pdf.set_xy(x_before_emi, y_before_emi)
        pdf.multi_cell(col_width, cell_height_emi, self.view.profesor_emisor_nombre.value, 1, 'C') # Borde 1, imprime texto 1 vez
        y_after_nombre_emi = pdf.get_y()
        height_emi = y_after_nombre_emi - y_before_emi
        
        # 2. Dibuja las celdas contiguas, comenzando en la segunda columna.
        pdf.set_xy(x_before_emi + col_width, y_before_emi) 
        pdf.cell(col_width, height_emi, self.view.profesor_emisor_rut.value, 1, 0, 'C') # 2da Col
        pdf.cell(col_width, height_emi, self.view.profesor_emisor_cargo.value, 1, 1, 'C') # 3ra Col
        pdf.set_y(y_after_nombre_emi) # Asegura que la siguiente línea comience correctamente

        # --- Tabla de Fecha de Informe ---
        pdf.set_font("Arial", 'B', 10)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(col_width * 3, 8, "Fecha de Informe", 1, 1, 'C', fill=True)
        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(col_width * 3, 8, datetime.now().strftime('%Y-%m-%d'), 1, 1, 'C')

        pdf.ln(2)

        # --- Resultados del Test (Totales) ---
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 10, "Resultados del Test:", 0, 1, 'L')
        
        # Tabla Puntaje/Riesgo Total
        col_width_res = pdf.w / 2.33 
        pdf.set_text_color(255, 255, 255)
        pdf.cell(col_width_res, 8, "Puntaje Obtenido", 1, 0, 'C', fill=True)
        pdf.cell(col_width_res, 8, "Porcentaje de Riesgo", 1, 1, 'C', fill=True)

        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(col_width_res, 8, self.view.puntaje_obtenido.value, 1, 0, 'C')
        pdf.cell(col_width_res, 8, self.view.porcentaje_riesgo.value, 1, 1, 'C')
        
        # --- Tabla de Categorías de Riesgo ---
        pdf.ln(0)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(col_width, 8, "Categoría", 1, 0, 'C', fill=True)
        pdf.cell(col_width, 8, "Porcentaje de Riesgo", 1, 0, 'C', fill=True)
        pdf.cell(col_width, 8, "Indicios Detectados", 1, 1, 'C', fill=True)

        pdf.set_font("Arial", '', 9)
        pdf.set_text_color(0, 0, 0)
        cell_height_indicios = 5 # Altura base de cada línea para multi_cell de indicios

        # --------------------------
        # Función Auxiliar para Filas Dinámicas
        # --------------------------
        def draw_dynamic_row(category_name, porcentaje_val, indicios_val):
            x_start = pdf.get_x() 
            y_start = pdf.get_y()

            # 1. Dibujar la celda más larga (Indicios) para determinar la altura
            pdf.set_xy(x_start + col_width * 2, y_start) 
            # Alineación 'L' (Izquierda) es más apropiada para texto descriptivo largo
            pdf.multi_cell(col_width, cell_height_indicios, indicios_val, 1, 'L') 
            y_end = pdf.get_y()
            row_height = y_end - y_start

            # 2. Dibujar las celdas restantes usando la altura calculada
            pdf.set_xy(x_start, y_start) 
            pdf.cell(col_width, row_height, category_name, 1, 0, 'C') 
            pdf.cell(col_width, row_height, porcentaje_val, 1, 0, 'C') 

            # 3. Mover el cursor a la posición Y final
            pdf.set_y(y_end)


        # --------------------------
        # Fila 1 a 4: Categorías
        # --------------------------
        draw_dynamic_row("Atención", self.view.porcentaje_atencion.value, self.view.indicios_atencion.value)
        draw_dynamic_row("Memoria", self.view.porcentaje_memoria.value, self.view.indicios_memoria.value)
        # Asumiendo que el view tiene estas variables, ya que estaban en tu código anterior
        draw_dynamic_row("Social", self.view.porcentaje_social.value, self.view.indicios_social.value)
        draw_dynamic_row("Emocional", self.view.porcentaje_emocional.value, self.view.indicios_emocional.value)

        # --------------------------
        # Fila "Total" (si la necesitas, añádela aquí)
        # --------------------------
        # if hasattr(self.view, 'porcentaje_total'):
        #     draw_dynamic_row("Total", self.view.porcentaje_total.value, self.view.indicios_total.value)
        
        pdf.ln(10)
        
        # --- Guardar el PDF ---
        file_name = f"informe_estudiante_{self.res_det_id}.pdf"
        file_path = f"assets/{file_name}"
        pdf.output(file_path)

        # --- Mostrar feedback en Flet ---
        self.view.feedback_text.value = f"PDF generado con éxito: {file_name}"
        self.view.feedback_text.color = ft.colors.GREEN
        
        self.page.update()