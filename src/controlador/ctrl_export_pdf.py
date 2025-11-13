from flet_mvc import FletController
import flet as ft
import base64
import fitz

class ExportPDFController(FletController):
    def __init__(self, page, model):
        self.res_det_id = None
        self.pdf_bytes = None
        super().__init__(page, model)

    def cargar_alumno(self, res_det_id: int):
        self.res_det_id = res_det_id
        self.view.feedback_text.value = "Cargando PDF desde la base de datos..."
        self.view.feedback_text.color = "blue"
        self.view.contenedor_pdf.content.controls.clear()
        
        # Deshabilitar el Anchor y su contenido hasta que el PDF esté listo
        self.view.download_button.disabled = True
        self.page.update()

        # 1. Buscar el PDF en la BD
        file_name_to_find = f"informe_estudiante_{res_det_id}.pdf"
        pdf_document = self.model.leer_documento_por_nombre(file_name_to_find)

        if not pdf_document:
            self.view.feedback_text.value = f"Error: No se encontró el PDF '{file_name_to_find}' en la base de datos."
            self.view.feedback_text.color = "red"
            self.page.update()
            return

        # 2. Guardar los bytes del PDF
        self.pdf_bytes = pdf_document.pdf_contenido

        # Habilitar el botón de descarga ahora que tenemos los datos del PDF
        self.view.download_button.disabled = False

        # 5. Renderizar el PDF para visualización en la página
        self.view.contenedor_pdf.content.controls.clear()
        try:
            doc = fitz.open(stream=self.pdf_bytes, filetype="pdf")
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                # Aumentamos la resolución para mejor calidad
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                img_bytes = pix.tobytes(output="png")
                img_base64 = base64.b64encode(img_bytes).decode("utf-8")
                
                self.view.contenedor_pdf.content.controls.append(
                    ft.Image(src_base64=img_base64, fit=ft.ImageFit.CONTAIN, width=800, border_radius=ft.border_radius.all(5))
                )
            doc.close()
            
            self.view.feedback_text.value = "PDF cargado y listo para descargar."
            self.view.feedback_text.color = "green"
            
        except Exception as ex:
            self.view.contenedor_pdf.content.controls.append(ft.Text(f"Error al mostrar el PDF: {ex}", color="red"))
            self.view.feedback_text.value = "PDF cargado, pero no se pudo mostrar."
            self.view.feedback_text.color = "orange"
            
        self.page.update()

    def descargar_pdf(self, e):
        if self.pdf_bytes:
            pdf_base64 = base64.b64encode(self.pdf_bytes).decode('utf-8')
            file_name = f"informe_estudiante_{self.res_det_id}.pdf"

            # Con Flet actualizado, usamos page.launch_url con un data URI.
            # El navegador interpreta esto como una descarga.
            data_uri = f"data:application/pdf;base64,{pdf_base64}"
            self.page.launch_url(url=data_uri, web_window_name=file_name)
            print(f"Iniciando descarga de {file_name}...")
            self.page.update()
        else:
            print("Error: No hay datos de PDF para descargar.")

    def guardar_archivo_resultado(self, e: ft.FilePickerResultEvent):
        # Este método ya no es necesario para la descarga web.
        pass