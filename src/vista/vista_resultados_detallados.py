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
            color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
            offset=ft.Offset(0, 4),
            blur_style=ft.ShadowBlurStyle.NORMAL,
        )
        )
        self.porcentaje_control = ft.Container(
        content=ft.Column(
            [
                ft.Text("IDT", weight=ft.FontWeight.BOLD, size=20,color="white"),
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
            color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
            offset=ft.Offset(0, 4),
            blur_style=ft.ShadowBlurStyle.NORMAL,
        )
    )
        self.preguntas_atencion = ft.Text(f"{controller.model.leer_preguntas(pre_cat='Atención')[0][1]}", size=20, weight=ft.FontWeight.BOLD)


        main_column_controls = [
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("Datos del alumno:", size=20, weight=ft.FontWeight.BOLD, color="black"),
                            ft.Row([self.datatable], scroll=ft.ScrollMode.AUTO),
                        ]
                    )                    
                ]
            ),
            ft.ResponsiveRow(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(content=self.puntaje_control, col={"sm": 12, "md": 6}),
                    ft.Container(content=self.porcentaje_control, col={"sm": 12, "md": 6}),
                ]
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        controls=[
                            ft.Text("Posibles indicios de riesgo:", size=20, weight=ft.FontWeight.BOLD, color="black"),
                            ft.Container(
                                alignment=ft.alignment.center_left,
                                border=ft.border.all(1, ft.Colors.BLACK),
                                bgcolor=ft.Colors.WHITE,
                                padding=10,
                                width=1450,
                                content=ft.ExpansionPanelList(
                                    expand_icon_color=ft.Colors.BLACK,
                                    elevation=8,
                                    divider_color=ft.Colors.BLACK,
                                    controls=[
                                        ft.ExpansionPanel(
                                            header=ft.ListTile(title=ft.Text("Atención"), content_padding = 10),
                                            bgcolor=color_Docente,
                                            content=ft.Container(content=ft.Column([
                                                ft.ListTile(title=ft.Row([ft.Text("IDT: "), self.porcentaje_atencion_val])),
                                                ft.ListTile(title=self.indicios_atencion_val)
                                            ]), padding=10)
                                        ),
                                        ft.ExpansionPanel(
                                            header=ft.ListTile(title=ft.Text("Memoria"), content_padding = 10),
                                            bgcolor=color_Docente,
                                            content=ft.Container(content=ft.Column([
                                                ft.ListTile(title=ft.Row([ft.Text("IDT: "), self.porcentaje_memoria_val])),
                                                ft.ListTile(title=self.indicios_memoria_val)
                                            ]), padding=10)
                                        ),
                                        ft.ExpansionPanel(
                                            header=ft.ListTile(title=ft.Text("Social"), content_padding = 10),
                                            bgcolor=color_Docente,
                                            content=ft.Container(content=ft.Column([
                                                ft.ListTile(title=ft.Row([ft.Text("IDT: "), self.porcentaje_social_val])),
                                                ft.ListTile(title=self.indicios_social_val)
                                            ]), padding=10)
                                        ),
                                        ft.ExpansionPanel(
                                            header=ft.ListTile(title=ft.Text("Emocional"), content_padding = 10),
                                            bgcolor=color_Docente,
                                            content=ft.Container(content=ft.Column([
                                                ft.ListTile(title=ft.Row([ft.Text("IDT: "), self.porcentaje_emocional_val])),
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
        
        
        self.generate_pdf_button = ft.ElevatedButton(
            text="Generar arhivo PDF", icon=ft.Icons.SAVE, icon_color=ft.Colors.WHITE,
            color=ft.Colors.WHITE, bgcolor=color_Docente, on_click=controller.generar_y_navegar_pdf
        )
        self.view_pdf_button = ft.ElevatedButton(
            text="Ver archivo PDF", icon=ft.Icons.PICTURE_AS_PDF, icon_color=ft.Colors.WHITE,
            color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE_GREY,
            on_click=lambda _: controller.page.go(f"/export_pdf/{controller.current_det_id}")
        )
        self.update_pdf_button = ft.ElevatedButton(
            text="Actualizar PDF", icon=ft.Icons.UPDATE, icon_color=ft.Colors.WHITE,
            color=ft.Colors.WHITE, bgcolor=ft.Colors.ORANGE,
            on_click=controller.generar_y_navegar_pdf, visible=False
        )
        
        tabs_control = ft.Tabs(
            indicator_color=color_Docente, divider_color=ft.Colors.TRANSPARENT,
            unselected_label_color=ft.Colors.BLACK, label_color=color_Docente,
            overlay_color={
                ft.ControlState.HOVERED: ft.Colors.with_opacity(0.6, color_Docente),
                ft.ControlState.SELECTED: ft.Colors.with_opacity(0.5, color_Docente),
            },
            selected_index=0, animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Atención",
                    content=ft.Container(padding=20, content=ft.Column(
                        [self.result_test_table_atencion],
                        scroll=ft.ScrollMode.AUTO)
                    )
                ),
                ft.Tab(
                    text="Memoria",
                    content=ft.Container(padding=20, content=ft.Column(
                        [self.result_test_table_memoria],
                        scroll=ft.ScrollMode.AUTO)
                    )
                ),
                ft.Tab(
                    text="Social",
                    content=ft.Container(padding=20, content=ft.Column(
                        controls=[self.result_test_table_social],
                        scroll=ft.ScrollMode.AUTO)
                    )
                ),
                ft.Tab(
                    text="Emocional",
                    content=ft.Container(padding=20, content=ft.Column(
                        controls=[self.result_test_table_emocional],
                        scroll=ft.ScrollMode.AUTO)
                    )
                ),
            ]
        )

        # Campo para que el profesional PIE escriba sus observaciones
        self.observaciones_field = ft.TextField(
            label="Observaciones del Profesional",
            multiline=True,
            min_lines=4,
            max_lines=8,
            hint_text="Escriba aquí las observaciones que se incluirán en el PDF...",
            color="black",
            label_style=ft.TextStyle(color="black"),
        )

        self.pie_controls_container = ft.Column(
            visible=False, # Oculto por defecto
            controls=[
                self.observaciones_field,
                ft.Row([self.generate_pdf_button, self.view_pdf_button, self.update_pdf_button], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                tabs_control,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                
            ]
        )
        main_column_controls.append(self.pie_controls_container)

        view = ft.View(
            "/resultados_detallado/:det_id",
            bgcolor=color_Background_Docente, # Se establecerá un color base, main.py lo corregirá
            scroll=ft.ScrollMode.AUTO,
            controls=[
                self.feedback_snackbar,
                ft.Row([ft.Text("Inicio >", weight=ft.FontWeight.BOLD, color="black"), ft.Text("Mis Tests >", weight=ft.FontWeight.BOLD, color="black"), ft.Text("Resultados Detallados", weight=ft.FontWeight.BOLD, color=color_Docente)], alignment=ft.MainAxisAlignment.START),
                ft.Column(
                    controls=main_column_controls
                ),
            ]
        )
        super().__init__(model, view, controller)