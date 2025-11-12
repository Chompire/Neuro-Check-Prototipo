from flet_mvc import FletController
import flet as ft
import base64
import fitz

class ExportPDFController(FletController):
    def __init__(self, page, model):
        self.selected_est_id = None
        self.res_det_id = None
        self.pdf_bytes = None # Variable para almacenar los bytes del PDF
        super().__init__(page, model)

    def cargar_alumno(self, res_det_id: int):
        self.res_det_id = res_det_id
        self.view.feedback_text.value = "Cargando PDF desde la base de datos..."
        self.view.feedback_text.color = ft.Colors.BLUE
        self.view.contenedor_pdf.content.controls.clear()
        self.page.update()

        # 1. Construir el nombre del archivo y buscarlo en la BD
        file_name_to_find = f"informe_estudiante_{res_det_id}.pdf"
        pdf_document = self.model.leer_documento_por_nombre(file_name_to_find)

        if not pdf_document:
            self.view.feedback_text.value = f"Error: No se encontró el PDF '{file_name_to_find}' en la base de datos."
            self.view.feedback_text.color = ft.Colors.RED
            self.page.update()
            return

        # 2. Obtener el contenido en bytes del PDF
        self.pdf_bytes = pdf_document.pdf_contenido # Guardar los bytes en el controlador

        # 3. Limpiar el área de visualización y renderizar el PDF
        self.view.contenedor_pdf.content.controls.clear()
        try:
            # Abrir el PDF desde los bytes en memoria
            doc = fitz.open(stream=self.pdf_bytes, filetype="pdf")
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
            self.view.feedback_text.color = ft.Colors.GREEN
        except Exception as ex:
            self.view.contenedor_pdf.content.controls.append(ft.Text(f"Error al mostrar el PDF: {ex}", color=ft.Colors.RED))
            self.view.feedback_text.value = "Error al renderizar el PDF."
            self.view.feedback_text.color = ft.Colors.RED

        self.page.update()

    def descargar_pdf(self, e):
        if self.pdf_bytes:
            file_name = f"informe_estudiante_{self.res_det_id}.pdf"
            self.view.file_picker.save_file(
                dialog_title="Guardar PDF como...",
                file_name=file_name,
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=["pdf"]
            )
        else:
            print("Error: No hay datos de PDF para descargar.")

    def guardar_archivo_resultado(self, e: ft.FilePickerResultEvent):
        # Para la web, el navegador maneja la descarga.
        # Para escritorio, este código guarda el archivo.
        if e.path:
            with open(e.path, "wb") as f:
                f.write(self.pdf_bytes)
            print(f"Archivo guardado en (escritorio): {e.path}")
        else:
            print("Descarga iniciada en el navegador.")
