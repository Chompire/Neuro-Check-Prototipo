from flet_mvc import FletController
import flet as ft
from fpdf import FPDF

class ExportPDFController(FletController):
    def __init__(self, page, model):
        self.selected_est_id = None
        self.res_det_id = None
        super().__init__(page, model)
    def cargar_alumno(self, res_det_id: int):
        self.res_det_id = res_det_id

        # Leer los resultados detallados usando el ID
        resultados = self.model.leer_resultados_detallados_by_det_id(det_id=res_det_id)

        if resultados:
            resultado = resultados[0]
            test_id = resultado.id_test
            test_full = self.model.leer_test(test_id)
            estudiante_id = test_full[1]
            estudiante = self.model.leer_estudiante_por_id(estudiante_id)
            profesor_jefe = f"{estudiante[13]} {estudiante[14]}"
            print(profesor_jefe)
            if estudiante.es_nombre_3 is None:
                nombre_completo = f"{estudiante.es_nombre_1} {estudiante.es_nombre_2} {estudiante.es_apellido_pat} {estudiante.es_apellido_mat}"
            else:
                nombre_completo = f"{estudiante.es_nombre_1} {estudiante.es_nombre_2} {estudiante.es_nombre_3} {estudiante.es_apellido_pat} {estudiante.es_apellido_mat}"

            self.view.nombre_completo_es.value = nombre_completo
            self.view.rut_es.value = estudiante.es_rut
            self.view.sexo_es.value = "Masculino" if estudiante.es_sexo == 1 else "Femenino"
            self.view.curso_es.value = resultado.lvl_curso
            self.view.fecha_nacimiento_es.value = estudiante.es_nacimiento.strftime('%Y-%m-%d')
            self.view.profesor_jefe.value = profesor_jefe
            self.page.update()

    def generar_pdf(self, e):
        try:
            # Limpiar mensajes anteriores
            self.view.feedback_text.value = ""
            self.view.download_row.controls.clear()

            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)

            # --- Encabezado ---
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, "Informe de Estudiante - Neuro Check", 0, 1, 'C')
            pdf.ln(10)

            # --- Tabla 1: Datos Personales ---
            pdf.set_font("Arial", 'B', 12)
            col_width = pdf.w / 3.5
            pdf.cell(col_width, 10, "Nombre Completo", 1, 0, 'C')
            pdf.cell(col_width, 10, "RUT", 1, 0, 'C')
            pdf.cell(col_width, 10, "Sexo", 1, 1, 'C')

            pdf.set_font("Arial", '', 12)
            pdf.cell(col_width, 10, self.view.nombre_completo_es.value, 1, 0, 'C')
            pdf.cell(col_width, 10, self.view.rut_es.value, 1, 0, 'C')
            pdf.cell(col_width, 10, self.view.sexo_es.value, 1, 1, 'C')
            pdf.ln(5)

            # --- Tabla 2: Datos Académicos ---
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(col_width, 10, "Fecha de Nacimiento", 1, 0, 'C')
            pdf.cell(col_width, 10, "Curso", 1, 0, 'C')
            pdf.cell(col_width, 10, "Repitencias", 1, 1, 'C')

            pdf.set_font("Arial", '', 12)
            pdf.cell(col_width, 10, self.view.fecha_nacimiento_es.value, 1, 0, 'C')
            pdf.cell(col_width, 10, self.view.curso_es.value, 1, 0, 'C')
            pdf.cell(col_width, 10, "xxxx", 1, 1, 'C') # Placeholder de repitencias
            pdf.ln(5)

            # --- Tabla 3: Profesor Jefe ---
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(col_width * 3, 10, "Profesor Jefe", 1, 1, 'C')

            pdf.set_font("Arial", '', 12)
            pdf.cell(col_width * 3, 10, self.view.profesor_jefe.value, 1, 1, 'C')
            pdf.ln(10)

            # --- Guardar el PDF en la carpeta de assets ---
            file_name = f"informe_estudiante_{self.res_det_id}.pdf"
            file_path = f"assets/{file_name}"
            pdf.output(file_path)

            # --- Mostrar enlace de descarga ---
            self.view.feedback_text.value = "PDF generado con éxito."
            self.view.feedback_text.color = ft.colors.GREEN
            self.view.download_row.controls.append(
                ft.ElevatedButton(
                    "Descargar PDF",
                    icon=ft.icons.DOWNLOAD,
                    url=f"/{file_name}",  # Flet sirve los archivos de 'assets' en la raíz
                    target="_blank",
                    bgcolor=ft.colors.BLUE,
                    color=ft.colors.WHITE
                )
            )
        except Exception as ex:
            self.view.feedback_text.value = f"Error al generar el PDF: {ex}"
            self.view.feedback_text.color = ft.colors.RED
        
        self.page.update()