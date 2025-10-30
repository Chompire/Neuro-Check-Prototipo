import flet as ft
from flet_mvc import FletView # Importamos nuestra nueva clase base
from colors import color_Background,color_Docente

class ResultadosView(FletView):
    def __init__(self, controller, model):
        
        self.det_id = None
        self.test_id = None
        self.puntaje_control = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Puntaje", weight=ft.FontWeight.BOLD, size=20, color="white"),
                    ft.Text("N/A", size=50, weight=ft.FontWeight.BOLD, color="white"),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            border=ft.border.all(2, color_Docente),
            border_radius=8,
            padding=15,
            bgcolor=color_Docente
        )
        self.porcentaje_control = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Porcentaje", weight=ft.FontWeight.BOLD, size=20, color="white"),
                    ft.Text("N/A", size=50, weight=ft.FontWeight.BOLD, color="white"),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            border=ft.border.all(2, color_Docente),
            border_radius=8,
            padding=15,
            bgcolor=color_Docente
        )
        self.datatable = ft.DataTable(
            heading_row_color=color_Docente,
            heading_text_style=ft.TextStyle(color="white", weight=ft.FontWeight.BOLD),
            bgcolor="white",
            border=ft.border.all(2, ft.Colors.BLACK),
            vertical_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
            data_text_style=ft.TextStyle(color="black"),
            columns=[
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Apellidos")),
                ft.DataColumn(ft.Text("Curso")),
            ]
        )
        view = ft.View(
            route="/resultados_detallados",
            bgcolor=color_Background,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Column(
                            expand=True,
                            scroll=ft.ScrollMode.AUTO,
                            controls=[
                                ft.Text("Resultados detallados", size=30, weight=ft.FontWeight.BOLD, color="black"),
                                self.puntaje_control,
                                self.porcentaje_control
                            ]
                        )
                        ]
                ),
                self.datatable
            ]
        )
        super().__init__(model, view, controller)