import flet as ft
from flet_mvc import FletView
# Asumo que estos imports funcionan
from colors import color_Docente, color_Background_PIE 

class ExportPDFView(FletView):
    def __init__(self, controller, model):
        
        # Texto para dar feedback al usuario
        self.feedback_text = ft.Text("", size=16, weight=ft.FontWeight.BOLD, color="black", selectable=True)

        # Usamos un IconButton estándar. La lógica de descarga estará en el controlador.
        self.download_button = ft.IconButton(
            icon=ft.Icons.DOWNLOAD,
            tooltip="Descargar PDF",
            on_click=controller.descargar_pdf,
            disabled=True, # Se habilita cuando el PDF está cargado.
            icon_color="white",
            bgcolor=color_Docente
        )
        
        self.contenedor_pdf = ft.Container(
            border=ft.border.all(1, ft.Colors.BLACK),
            padding=10,
            expand=True,
            content=ft.Column(
                controls=[ft.Text("El PDF generado se mostrará aquí.", size=16, color="grey", selectable=True)],
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
                ft.Row([
                    ft.Text("Inicio >", weight=ft.FontWeight.BOLD, color="black"), 
                    ft.Text("Mis Tests >", weight=ft.FontWeight.BOLD, color="black"), 
                    ft.Text("Resultados Detallados >", weight=ft.FontWeight.BOLD, color="black"), 
                    ft.Text("Exportar PDF", weight=ft.FontWeight.BOLD, color=color_Docente)
                ], alignment=ft.MainAxisAlignment.START), 
                
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text("Informe de Resultados", size=20, weight=ft.FontWeight.BOLD, selectable=True),
                                    self.download_button # Usamos el botón de descarga
                                ], 
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            self.feedback_text,
                            ft.Divider(visible=False),
                            self.contenedor_pdf, 
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                        expand=True
                    ),
                    expand=True
                ),
                
            ],
        )
        super().__init__(model, view, controller)