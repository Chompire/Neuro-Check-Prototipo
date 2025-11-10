from flet_mvc import FletController
import flet as ft
import base64
import fitz

class ExportPDFController(FletController):
    def __init__(self, page, model):
        self.selected_est_id = None
        self.res_det_id = None
        super().__init__(page, model)

    def cargar_alumno(self, res_det_id: int):
        self.res_det_id = res_det_id
        self.view.feedback_text.value = "Cargando PDF desde la base de datos..."
        self.view.feedback_text.color = ft.colors.BLUE
        self.view.contenedor_pdf.content.controls.clear()
        self.page.update()

        # 1. Construir el nombre del archivo y buscarlo en la BD
        file_name_to_find = f"informe_estudiante_{res_det_id}.pdf"
        pdf_document = self.model.leer_documento_por_nombre(file_name_to_find)

        if not pdf_document:
            self.view.feedback_text.value = f"Error: No se encontró el PDF '{file_name_to_find}' en la base de datos."
            self.view.feedback_text.color = ft.colors.RED
            self.page.update()
            return

        # 2. Obtener el contenido en bytes del PDF
        pdf_bytes = pdf_document.pdf_contenido

        # 3. Limpiar el área de visualización y renderizar el PDF
        self.view.contenedor_pdf.content.controls.clear()
        try:
            # Abrir el PDF desde los bytes en memoria
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                img_bytes = pix.tobytes(output="png")
                img_base64 = base64.b64encode(img_bytes).decode("utf-8")
                
                self.view.contenedor_pdf.content.controls.append(
                    ft.Image(src_base64=img_base64, fit=ft.ImageFit.CONTAIN, width=800)
                )
            doc.close()
            self.view.feedback_text.value = "PDF cargado correctamente."
            self.view.feedback_text.color = ft.colors.GREEN
        except Exception as ex:
            self.view.contenedor_pdf.content.controls.append(ft.Text(f"Error al mostrar el PDF: {ex}", color=ft.colors.RED))
            self.view.feedback_text.value = "Error al renderizar el PDF."
            self.view.feedback_text.color = ft.colors.RED

        self.page.update()
