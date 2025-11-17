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
        
        self.stat_cantidad_cursos_encuestados = ft.BarChart(
            bar_groups=[],
            border=ft.border.all(1, ft.Colors.GREY_400),
            width=700,
            left_axis=ft.ChartAxis(
                labels_size=40, title=ft.Text("Cantidad de tests realizados en el año", weight=ft.FontWeight.BOLD, color="black"), title_size=40,
                labels=[
                    ft.ChartAxisLabel(value=0, label=ft.Text("0", color="black")),
                    ft.ChartAxisLabel(value=5, label=ft.Text("5", color="black")),
                    ft.ChartAxisLabel(value=10, label=ft.Text("10", color="black")),
                    ft.ChartAxisLabel(value=15, label=ft.Text("15", color="black")),
                    ft.ChartAxisLabel(value=20, label=ft.Text("20", color="black")),
                ]
            ),
            bottom_axis=ft.ChartAxis(
                labels=[],
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.Colors.BLACK, width=1, dash_pattern=[3, 3]
            ),
            max_y=20,
            interactive=True,
        )

        self.stat_cantidad_cursos_encuestados_totales = ft.BarChart(
            bar_groups=[],
            border=ft.border.all(1, ft.Colors.GREY_400),
            width=700,
            left_axis=ft.ChartAxis(
                labels_size=40, title=ft.Text("Cantidad de tests totales realizados en el año", weight=ft.FontWeight.BOLD, color="black"), title_size=40,
                labels=[
                    ft.ChartAxisLabel(value=0, label=ft.Text("0", color="black")),
                    ft.ChartAxisLabel(value=5, label=ft.Text("5", color="black")),
                    ft.ChartAxisLabel(value=10, label=ft.Text("10", color="black")),
                    ft.ChartAxisLabel(value=15, label=ft.Text("15", color="black")),
                    ft.ChartAxisLabel(value=20, label=ft.Text("20", color="black")),
                ]
            ),
            bottom_axis=ft.ChartAxis(
                labels=[],
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.Colors.BLACK, width=1, dash_pattern=[3, 3]
            ),
            max_y=20,
            interactive=True,
        )

        self.cursos_en_rojo= ft.PieChart(            
            width=400,
            height=400,
            sections=[],
            sections_space=1,
            center_space_radius=0,
        )

        self.estudiantes_rojos = ft.PieChart(            
            width=400,
            height=400,
            sections=[],
            sections_space=1,
            center_space_radius=0,
        )
        
        self.graficos_container = ft.Column(
            visible=False, # Oculto por defecto
            controls=[
                ft.Row([ft.Text("Graficos:", size=20, weight=ft.FontWeight.BOLD, color="black")], alignment=ft.MainAxisAlignment.START),
                ft.Row([ft.Text("Graficos de barras:", size=15, weight=ft.FontWeight.BOLD, color="black")], alignment=ft.MainAxisAlignment.START),
                ft.Container(
                    content=ft.Row(
                        [self.stat_cantidad_cursos_encuestados, self.stat_cantidad_cursos_encuestados_totales],
                        scroll=ft.ScrollMode.ADAPTIVE
                    ),
                    padding=5,
                    expand=True
                ),
                ft.Container(
                    content=ft.Row(
                        [ft.Column([ft.Text("Cursos con mayor cantidad de resultados en IDT alto", weight=ft.FontWeight.BOLD, color="black", size=16), self.cursos_en_rojo]),
                         ft.Column([ft.Text("Estudiantes con mayor cantidad de test con IDT alto ", weight=ft.FontWeight.BOLD, color="black", size=16), self.estudiantes_rojos])],
                        scroll=ft.ScrollMode.ADAPTIVE
                    ),
                    padding=5,
                    expand=True
                )
            ])

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
                            ft.Column(spacing=5, expand=True, controls=[ # Añadido expand=True aquí
                                ft.Text("Mis datos:", size=20, weight=ft.FontWeight.BOLD, color="black"),
                                ft.Row([self.info_table], scroll=ft.ScrollMode.AUTO),
                                ft.Row([self.cursos_designados_table], scroll=ft.ScrollMode.AUTO),
                                self.graficos_container, # Contenedor de gráficos
                                ])
                        ]),
                ]),            
            ]
        )
        
        super().__init__(model, view, controller)