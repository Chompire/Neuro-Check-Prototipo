import flet as ft
from flet_mvc import FletView
from colors import color_Docente, color_Background_PIE
class ExportPDFView(FletView):
    def __init__(self, controller, model):
        
        # Re-añadimos el FilePicker, que es necesario para la descarga.
        self.file_picker = ft.FilePicker(on_result=controller.guardar_archivo_resultado)

        self.feedback_text = ft.Text("", size=16, weight=ft.FontWeight.BOLD)

        # 2. Añadir el botón de descarga
        self.download_button = ft.IconButton(icon=ft.Icons.DOWNLOAD, on_click=controller.descargar_pdf, tooltip="Descargar PDF")
        # New control to display PDF pages as images
        self.contenedor_pdf = ft.Container(
            border=ft.border.all(1, ft.Colors.BLACK),
            padding=10,
            expand=True,
            content=ft.Column(
                controls=[ft.Text("El PDF generado se mostrará aquí.", size=16, color=ft.Colors.GREY)],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                expand=True,
            )
        )
        view = ft.View(
            "/export_pdf/:res_det_id",
            scroll=ft.ScrollMode.ADAPTIVE,
            bgcolor=color_Background_PIE,
            controls=[
                ft.Row([ft.Text("Inicio >", weight=ft.FontWeight.BOLD, color="black"), ft.Text("Mis Tests >", weight=ft.FontWeight.BOLD, color="black"), ft.Text("Resultados Detallados >", weight=ft.FontWeight.BOLD, color="black"), ft.Text("Exportar PDF", weight=ft.FontWeight.BOLD, color=color_Docente)], alignment=ft.MainAxisAlignment.START),                
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row([self.download_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            self.contenedor_pdf, # Add the PDF display area
                            ft.Divider(),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20
                    ),
                ),
                    
            ],
        )
        super().__init__(model, view, controller)
