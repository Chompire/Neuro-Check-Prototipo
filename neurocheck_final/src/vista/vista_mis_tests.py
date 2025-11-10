import flet as ft
from flet_mvc import FletView
from colors import color_Background_Docente,color_Docente, color_Background_PIE

class MisTestsView(FletView):
    def __init__(self, controller, model):
        self.test_completos_table = ft.DataTable(
            heading_row_color=color_Docente,
            heading_text_style=ft.TextStyle(color="white", weight=ft.FontWeight.BOLD),
            bgcolor="white",
            data_text_style=ft.TextStyle(color="black"),
            border=ft.border.all(2, ft.Colors.BLACK),
            vertical_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
            data_row_color={
                ft.ControlState.HOVERED: ft.Colors.with_opacity(0.6, color_Docente),
                ft.ControlState.SELECTED: ft.Colors.with_opacity(0.5, color_Docente),                
            },
            columns=[
                ft.DataColumn(ft.Text("Nombre Est.")),
                ft.DataColumn(ft.Text("Apellido Est.")),
                ft.DataColumn(ft.Text("RUT Est.")),
                ft.DataColumn(ft.Text("Curso")),
                ft.DataColumn(ft.Text("Fecha de Creación")),
                ft.DataColumn(ft.Text("Fecha de Finalización")),
                ft.DataColumn(ft.Text("Riesgo")),
            ],
            rows=[]
        )
        self.test_profesores_table = None
        if model.datos_profesor.pro_cargo == 1:
            self.test_profesores_table = ft.DataTable(
                heading_row_color=color_Docente,
                heading_text_style=ft.TextStyle(color="white", weight=ft.FontWeight.BOLD),
                bgcolor="white",
                data_text_style=ft.TextStyle(color="black"),
                border=ft.border.all(2, ft.Colors.BLACK),
                vertical_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
                horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
                data_row_color={
                    ft.ControlState.HOVERED: ft.Colors.with_opacity(0.6, color_Docente),
                    ft.ControlState.SELECTED: ft.Colors.with_opacity(0.5, color_Docente),                
                },
                columns=[
                    ft.DataColumn(ft.Text("Nombre Est.")),
                    ft.DataColumn(ft.Text("Apellido Est.")),
                    ft.DataColumn(ft.Text("RUT Est.")),
                    ft.DataColumn(ft.Text("Curso")),
                    ft.DataColumn(ft.Text("Fecha de Creación")),
                    ft.DataColumn(ft.Text("Fecha de Finalización")),
                    ft.DataColumn(ft.Text("Riesgo")),
                ],
                rows=[]
            )

        # Build the column controls conditionally
        column_controls = [
            ft.Text("Mis tests:", size=30, weight=ft.FontWeight.BOLD, color="black"),
            ft.Row([self.test_completos_table], scroll=ft.ScrollMode.AUTO),
        ]

        if self.test_profesores_table is not None:
            column_controls.extend([
                ft.Text("Test de otros profesores:", size=30, weight=ft.FontWeight.BOLD, color="black"),
                ft.Row([self.test_profesores_table], scroll=ft.ScrollMode.AUTO)
            ])

        view = ft.View(
            "/mis_tests",
            scroll=ft.ScrollMode.AUTO,
            bgcolor=color_Background_PIE if model.datos_profesor.pro_cargo == 1 else color_Background_Docente,
            controls=[
                ft.Column(
                    controls=column_controls,
                )
            ]
        )
        super().__init__(model, view, controller)