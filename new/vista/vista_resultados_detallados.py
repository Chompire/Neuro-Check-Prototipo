import flet as ft
from flet_mvc import FletView
from colors import color_Docente, color_Background_Docente, color_Background_PIE

class ResultadosDetalladosView(FletView):
    def __init__(self, controller, model):
        self.puntaje_val = ft.Text("N/A", size=50, weight=ft.FontWeight.BOLD, color="white")
        self.porcentaje_val = ft.Text("0%", size=50, weight=ft.FontWeight.BOLD, color="white")
        self.porcentaje_atencion_val = ft.Text("0%", size=20, weight=ft.FontWeight.BOLD, color="black")
        self.porcentaje_memoria_val = ft.Text("0%", size=20, weight=ft.FontWeight.BOLD, color="black")
        self.porcentaje_social_val = ft.Text("0%", size=20, weight=ft.FontWeight.BOLD, color="black")
        self.porcentaje_emocional_val = ft.Text("0%", size=20, weight=ft.FontWeight.BOLD, color="black")
        self.indicios_atencion_val = ft.Text("", size=15, color="black", weight=ft.FontWeight.BOLD)
        self.indicios_memoria_val = ft.Text("", size=15, color="black", weight=ft.FontWeight.BOLD)
        self.indicios_social_val = ft.Text("", size=15, color="black", weight=ft.FontWeight.BOLD)
        self.indicios_emocional_val = ft.Text("", size=15, color="black", weight=ft.FontWeight.BOLD)
        self.feedback_snackbar = ft.SnackBar(content=ft.Text(""))

        self.result_test_table_atencion = ft.DataTable(
            heading_row_color=color_Docente,
            heading_text_style=ft.TextStyle(color="white", weight=ft.FontWeight.BOLD),
            bgcolor="white",
            border=ft.border.all(2, ft.Colors.BLACK),
            vertical_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
            data_text_style=ft.TextStyle(color="black"),
            columns=[
                ft.DataColumn(ft.Text("Pregunta")),
                ft.DataColumn(ft.Text("Respuesta")),
            ],
            rows=[]
        )
        self.result_test_table_memoria = ft.DataTable(
            heading_row_color=color_Docente,
            heading_text_style=ft.TextStyle(color="white", weight=ft.FontWeight.BOLD),
            bgcolor="white",
            border=ft.border.all(2, ft.Colors.BLACK),
            vertical_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
            data_text_style=ft.TextStyle(color="black"),
            columns=[
                ft.DataColumn(ft.Text("Pregunta")),
                ft.DataColumn(ft.Text("Respuesta")),
            ],
            rows=[]
        )
        self.result_test_table_social= ft.DataTable(
            heading_row_color=color_Docente,
            heading_text_style=ft.TextStyle(color="white", weight=ft.FontWeight.BOLD),
            bgcolor="white",
            border=ft.border.all(2, ft.Colors.BLACK),
            vertical_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
            data_text_style=ft.TextStyle(color="black"),
            columns=[
                ft.DataColumn(ft.Text("Pregunta")),
                ft.DataColumn(ft.Text("Respuesta")),
            ],
            rows=[]
        )
        self.result_test_table_emocional = ft.DataTable(
            heading_row_color=color_Docente,
            heading_text_style=ft.TextStyle(color="white", weight=ft.FontWeight.BOLD),
            bgcolor="white",
            border=ft.border.all(2, ft.Colors.BLACK),
            vertical_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
            data_text_style=ft.TextStyle(color="black"),
            columns=[
                ft.DataColumn(ft.Text("Pregunta")),
                ft.DataColumn(ft.Text("Respuesta")),
            ],
            rows=[]
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
                ft.DataColumn(ft.Text("Fecha de test"))
            ],
            rows=[]
        )
        self.puntaje_control = ft.Container(
        content=ft.Column(
            [
                ft.Text("Puntaje", weight=ft.FontWeight.BOLD, size=20,color="white"),
                self.puntaje_val
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            
        ),
        border=ft.border.all(2, color_Docente),
        border_radius=8,
        padding=15,
        bgcolor=color_Docente,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.colors.with_opacity(0.3, ft.colors.BLACK),
            offset=ft.Offset(0, 4),
            blur_style=ft.ShadowBlurStyle.NORMAL,
        )
        )
        self.porcentaje_control = ft.Container(
        content=ft.Column(
            [
                ft.Text("Porcentaje", weight=ft.FontWeight.BOLD, size=20,color="white"),
                self.porcentaje_val
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            
        ),
        border=ft.border.all(2, color_Docente),
        border_radius=8,
        padding=15,
        bgcolor= color_Docente,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.colors.with_opacity(0.3, ft.colors.BLACK),
            offset=ft.Offset(0, 4),
            blur_style=ft.ShadowBlurStyle.NORMAL,
        )
    )
        self.preguntas_atencion = ft.Text(f"{controller.model.leer_preguntas(pre_cat='Atención')[0][1]}", size=30, weight=ft.FontWeight.BOLD)


        main_column_controls = [
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        controls=[
                            ft.Text("Datos del alumno:", size=30, weight=ft.FontWeight.BOLD, color="black"),
                            self.datatable,
                        ]
                    )                    
                ]
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[self.puntaje_control, self.porcentaje_control]),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        controls=[
                            ft.Text("Posibles indicios de riesgo:", size=30, weight=ft.FontWeight.BOLD, color="black"),
                            ft.Container(
                                alignment=ft.alignment.center_left,
                                border=ft.border.all(1, ft.Colors.BLACK),
                                bgcolor=ft.Colors.WHITE,
                                padding=10,
                                width=1000,
                                content=ft.ExpansionPanelList(
                                    expand_icon_color=ft.colors.BLACK,
                                    elevation=8,
                                    divider_color=ft.colors.BLACK,
                                    controls=[
                                        ft.ExpansionPanel(
                                            header=ft.ListTile(title=ft.Text("Atención"), content_padding = 10),
                                            bgcolor=color_Docente,
                                            content=ft.Container(content=ft.Column([
                                                ft.ListTile(title=ft.Row([ft.Text("Porcentaje: "), self.porcentaje_atencion_val])),
                                                ft.ListTile(title=self.indicios_atencion_val)
                                            ]), padding=10)
                                        ),
                                        ft.ExpansionPanel(
                                            header=ft.ListTile(title=ft.Text("Memoria"), content_padding = 10),
                                            bgcolor=color_Docente,
                                            content=ft.Container(content=ft.Column([
                                                ft.ListTile(title=ft.Row([ft.Text("Porcentaje: "), self.porcentaje_memoria_val])),
                                                ft.ListTile(title=self.indicios_memoria_val)
                                            ]), padding=10)
                                        ),
                                        ft.ExpansionPanel(
                                            header=ft.ListTile(title=ft.Text("Social"), content_padding = 10),
                                            bgcolor=color_Docente,
                                            content=ft.Container(content=ft.Column([
                                                ft.ListTile(title=ft.Row([ft.Text("Porcentaje: "), self.porcentaje_social_val])),
                                                ft.ListTile(title=self.indicios_social_val)
                                            ]), padding=10)
                                        ),
                                        ft.ExpansionPanel(
                                            header=ft.ListTile(title=ft.Text("Emocional"), content_padding = 10),
                                            bgcolor=color_Docente,
                                            content=ft.Container(content=ft.Column([
                                                ft.ListTile(title=ft.Row([ft.Text("Porcentaje: "), self.porcentaje_emocional_val])),
                                                ft.ListTile(title=self.indicios_emocional_val)
                                            ]), padding=10)
                                        )
                                    ]
                                )
                            )
                        ]
                    )                    
                ]
            ),
        ]

        # Añadir el contenedor de comentarios solo si el usuario es un profesional PIE
        if model.datos_profesor.pro_cargo == 1:
            tabs_control = ft.Tabs(
                selected_index=0,
                animation_duration=300,
                tabs=[
                    ft.Tab(
                        text="Atención",
                        content=ft.Column(
                            [self.result_test_table_atencion],
                            scroll=ft.ScrollMode.AUTO,
                            expand=True
                        ),
                    ),
                    ft.Tab(
                        text="Memoria",
                        content=ft.Column(
                            [self.result_test_table_memoria],
                            scroll=ft.ScrollMode.AUTO,
                            expand=True
                        ),
                    ),
                    ft.Tab(
                        text="Social",
                        content=ft.Column(
                            [self.result_test_table_social],
                            scroll=ft.ScrollMode.AUTO,
                            expand=True
                        ),
                    ),
                    ft.Tab(
                        text="Emocional",
                        content=ft.Column(
                            [self.result_test_table_emocional],
                            scroll=ft.ScrollMode.AUTO,
                            expand=True
                        ),
                    ),
                ],
                expand=1,
            )
            pie_comment_section = ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text("Respuestas del profesor:", size=20, weight=ft.FontWeight.BOLD, color="black"),
                            ft.Container(
                                width=1000, 
                                alignment=ft.alignment.center_left, 
                                border=ft.border.all(1, ft.Colors.BLACK), 
                                bgcolor=ft.Colors.WHITE, 
                                padding=10,
                                content=tabs_control
                            )
                        ]
                    )
                ]
            )
            main_column_controls.append(pie_comment_section)

        view = ft.View(
            "/resultados_detallado/:det_id",
            scroll=ft.ScrollMode.AUTO,
        bgcolor=color_Background_PIE if model.datos_profesor.pro_cargo == 1 else color_Background_Docente,
        controls=[
            self.feedback_snackbar,
            ft.Column(
                expand=True,
                controls=main_column_controls
            )
            
        ]
    ) 

        super().__init__(model, view, controller)
        self.page = controller.page # Store page reference for snackbar