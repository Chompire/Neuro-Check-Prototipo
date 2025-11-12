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
            width= 800,
            columns=[
                ft.DataColumn(ft.Text("Nombres")),
                ft.DataColumn(ft.Text("Apellidos")),
                ft.DataColumn(ft.Text("RUT")),
                ft.DataColumn(ft.Text("Cargo")),
                ft.DataColumn(ft.Text("Curso")),
            ],
        )
        self.mis_tests_view = None # Placeholder for the new view
        self.cursos_designados_table= ft.DataTable(
            heading_row_color=color_Docente,
            heading_text_style=ft.TextStyle(color="white", weight=ft.FontWeight.BOLD),
            bgcolor="white",
            data_text_style=ft.TextStyle(color="black"),
            border=ft.border.all(2, ft.Colors.BLACK),
            vertical_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
            width= 800,
            columns=[
                ft.DataColumn(ft.Text("Curso")),
                ft.DataColumn(ft.Text("Año")),
                ft.DataColumn(ft.Text("Numero de encuestas")),
                ft.DataColumn(ft.Text("Estado")),
            ],
            rows=[]
        )

        view = ft.View(
            "/mi_perfil",
            bgcolor=color_Background_Docente, # Se establecerá un color base, main.py lo corregirá
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Row([ft.Text("Inicio >", weight=ft.FontWeight.BOLD, color="black"), ft.Text("Mi Perfil", weight=ft.FontWeight.BOLD, color=color_Docente)], alignment=ft.MainAxisAlignment.START), # This line already exists, no change needed.
                ft.Column(                    
                controls=[
                    ft.Row(
                        controls=[
                            ft.Column(spacing=5,controls=[
                                ft.Text("Datos del docente:", size=20, weight=ft.FontWeight.BOLD, color="black"),
                                ft.Row([self.info_table], scroll=ft.ScrollMode.AUTO),
                                ft.Row([self.cursos_designados_table], scroll=ft.ScrollMode.AUTO),
                                ])
                        ]),
                ]),            
            ]
        )
        
        super().__init__(model, view, controller)