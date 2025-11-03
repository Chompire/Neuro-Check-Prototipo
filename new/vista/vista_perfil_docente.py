import flet as ft
from flet_mvc import FletView
from colors import color_Background_Docente,color_Docente, color_Background_PIE
class PerfilDocenteView(FletView):
    def __init__(self, controller, model):
        self.info_table = ft.DataTable(
            heading_row_color= color_Docente,
            data_row_color="white",
            columns=[
                ft.DataColumn(ft.Text("Nombres")),
                ft.DataColumn(ft.Text("Apellidos")),
                ft.DataColumn(ft.Text("RUT")),
                ft.DataColumn(ft.Text("Cargo")),
                ft.DataColumn(ft.Text("Curso")),
            ],
        )
        self.test_completos_table = ft.DataTable(
            heading_row_color=color_Docente,
            heading_text_style=ft.TextStyle(color="white", weight=ft.FontWeight.BOLD),
            bgcolor="white",
            data_text_style=ft.TextStyle(color="black"),
            border=ft.border.all(2, ft.Colors.BLACK),
            vertical_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
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
        view = ft.View(
            "/perfil_docente",
            bgcolor=color_Background_Docente if model.datos_profesor.pro_cargo == 0 else color_Background_PIE,
            controls=[
                ft.Column(
                scroll=ft.ScrollMode.AUTO,
                expand=True, 
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Column(
                                scroll=ft.ScrollMode.AUTO,
                                controls=[
                                ft.Text("Datos del docente:", size=30, weight=ft.FontWeight.BOLD, color="black"),
                                self.info_table
                                ])]),
                    
                    ft.Divider(color="black"),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                        ft.Column(controls=[
                            ft.Row(controls=[ft.Text("Tests Completados:", size=30, weight=ft.FontWeight.BOLD, color="black")]),
                            self.test_completos_table
                            ])
                            ])
                ]),            
        
            ]

        )
        super().__init__(model, view, controller)