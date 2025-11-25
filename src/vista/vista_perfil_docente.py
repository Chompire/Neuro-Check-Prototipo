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
                ft.DataColumn(ft.Text("Numero de encuestas")),
            ],
        )
        self.mis_tests_view = None # Placeholder for the new view
        
        self.stat_cantidad_cursos_encuestados = ft.BarChart(
            bar_groups=[],
            border=ft.border.all(1, ft.Colors.GREY_400),
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
            visible=False,
            controls=[
                ft.Container(
                    alignment=ft.alignment.center,
                    content=ft.Column(
                        controls=[
                            ft.Row([ft.Text("Graficos:", size=20, weight=ft.FontWeight.BOLD, color="black")], alignment=ft.MainAxisAlignment.START),
                            ft.Row([ft.Text("Graficos de barras:", size=15, weight=ft.FontWeight.BOLD, color="black")], alignment=ft.MainAxisAlignment.START),
                            ft.ResponsiveRow(controls=[
                                ft.Container(content=self.stat_cantidad_cursos_encuestados_totales, col={"sm": 12, "lg": 6}),
                            ])
                        ]
                    ),
                    padding=5
                ),
                ft.Container(
                    alignment=ft.alignment.center,
                    content=ft.Column(
                        controls=[
                            ft.Text("Graficos circulares:", size=15, weight=ft.FontWeight.BOLD, color="black"),
                            ft.ResponsiveRow(
                                controls=[
                                    ft.Container(col={"sm": 12, "lg": 6}, content=ft.Column([ft.Text("Cursos con mayor cantidad de resultados en IDT alto", weight=ft.FontWeight.BOLD, color="black", size=16, text_align=ft.TextAlign.CENTER), self.cursos_en_rojo], horizontal_alignment=ft.CrossAxisAlignment.CENTER)),
                                    ft.Container(col={"sm": 12, "lg": 6}, content=ft.Column([ft.Text("Estudiantes con mayor cantidad de test con IDT alto ", weight=ft.FontWeight.BOLD, color="black", size=16, text_align=ft.TextAlign.CENTER), self.estudiantes_rojos], horizontal_alignment=ft.CrossAxisAlignment.CENTER))
                                ]
                            )
                        ]
                    ),
                    padding=5,
                    expand=True
                )
            ]
        )
        view = ft.View(
            "/mi_perfil",
            bgcolor=color_Background_Docente,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row([ft.Text("Inicio >", weight=ft.FontWeight.BOLD, color="black"), ft.Text("Mi Perfil", weight=ft.FontWeight.BOLD, color=color_Docente)], alignment=ft.MainAxisAlignment.START), # This line already exists, no change needed.
                ft.ResponsiveRow([
                    ft.Container(
                        col={"sm": 12},
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=15,
                            controls=[
                                ft.Column(
                                    spacing=15,
                                    controls=[
                                        ft.Text("Mis datos:", size=20, weight=ft.FontWeight.BOLD, color="black"),
                                        ft.Row([self.info_table], scroll=ft.ScrollMode.AUTO, expand=True),
                                    ]
                                ),
                                ft.Container(
                                    alignment=ft.alignment.center,
                                    content=ft.Column([ft.Row([ft.Text("Graficos:", size=20, weight=ft.FontWeight.BOLD, color="black")], alignment=ft.MainAxisAlignment.START), self.stat_cantidad_cursos_encuestados]),
                                    padding=5
                                ),
                                ft.Divider(height=20, color=ft.Colors.BLACK),
                                self.graficos_container, # Contenedor de gráficos,
                            ]
                        )
                    )
                ])
            ]
        )
        
        super().__init__(model, view, controller)