import flet as ft
from flet_mvc import FletView
from colors import color_Background_Docente,color_Docente, color_Background_PIE
class PerfilDocenteView(FletView):
    def __init__(self, controller, model):
        self.info_table = ft.DataTable(
            heading_row_color=color_Docente,
            heading_text_style=ft.TextStyle(color="white", weight=ft.FontWeight.BOLD),
            bgcolor="white",
            data_text_style=ft.TextStyle(color="black"),
            border=ft.border.all(2, ft.Colors.BLACK),
            vertical_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
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
        self.cursos_designados_table = None # Inicializar como None
        if model.datos_profesor.pro_cargo == 1:
            self.cursos_designados_table= ft.DataTable(
                heading_row_color=color_Docente,
                heading_text_style=ft.TextStyle(color="white", weight=ft.FontWeight.BOLD),
                bgcolor="white",
                data_text_style=ft.TextStyle(color="black"),
                border=ft.border.all(2, ft.Colors.BLACK),
                vertical_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
                horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
                columns=[
                    ft.DataColumn(ft.Text("Curso")),
                    ft.DataColumn(ft.Text("Año")),
                    ft.DataColumn(ft.Text("Numero de encuestas")),
                    ft.DataColumn(ft.Text("Estado")),
                ],
                rows=[]
            )
        

        # Determinar el color de fondo de forma segura
        background_color = color_Background_Docente
        if hasattr(model, 'datos_profesor') and model.datos_profesor and model.datos_profesor.pro_cargo != 0:
            background_color = color_Background_PIE

        view = ft.View(
            "/perfil_docente",
            bgcolor=background_color,
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
                                self.info_table,
                                self.cursos_designados_table if self.cursos_designados_table is not None else ft.Container(),
                                ])]),
                                
                    
                    ft.Divider(color="black"),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                        ft.Column(controls=[
                            ft.Row(controls=[ft.Text("Mis tests:", size=30, weight=ft.FontWeight.BOLD, color="black")]),
                            self.test_completos_table
                            ])
                            ])
                ]),            
        
            ]

        )
        
        super().__init__(model, view, controller)