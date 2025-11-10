import flet as ft
from flet_mvc import FletView
from colors import color_Docente, color_Background_PIE
class ExportPDFView(FletView):
    def __init__(self, controller, model):
        

        self.feedback_text = ft.Text("", size=16, weight=ft.FontWeight.BOLD)

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
                ft.Container(
                    content=ft.Column(
                        [
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
