import flet as ft
from flet_mvc import FletView
from colors import color_Docente, color_Background_PIE
class ExportPDFView(FletView):
    def __init__(self, controller, model):
        self.pdf_content = ft.Column(
            [
                ft.Text("Generando PDF...", size=20),
                ft.ProgressRing(),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )
        self.nombre_completo_es = ft.Text("", color="black")
        self.rut_es = ft.Text("", color="black")
        self.curso_es = ft.Text("", color="black")
        self.sexo_es = ft.Text("", color="black")
        self.fecha_nacimiento_es = ft.Text("", color="black")
        self.profesor_jefe = ft.Text("", color="black")
        
        self.puntaje_obtenido = ft.Text("", color="black",size=40)
        self.porcentaje_riesgo = ft.Text("", color="black",size=40)

        # Controles para los porcentajes por categoría
        self.porcentaje_atencion = ft.Text("", color="black", weight=ft.FontWeight.BOLD)
        self.porcentaje_memoria = ft.Text("", color="black", weight=ft.FontWeight.BOLD)
        self.porcentaje_social = ft.Text("", color="black", weight=ft.FontWeight.BOLD)
        self.porcentaje_emocional = ft.Text("", color="black", weight=ft.FontWeight.BOLD)

        # Controles para los indicios
        self.indicios_atencion = ft.Text("", color="black", width=600, )
        self.indicios_memoria = ft.Text("", color="black", width=600, )
        self.indicios_social = ft.Text("", color="black", width=600, )
        self.indicios_emocional = ft.Text("", color="black", width=600, )

        self.fecha_informe = ft.Text("", color="black")

        self.titulo_datos_est = ft.Text("Datos del Estudiante:", size=20, weight=ft.FontWeight.BOLD, color="black")
        self.titulo_datos_pro = ft.Text("Datos del Docente emisor del test:", size=20, weight=ft.FontWeight.BOLD, color="black")
        self.titulo_resultados_test = ft.Text("Resultados del Test:", size=20, weight=ft.FontWeight.BOLD, color="black")
        self.titulo_indicios = ft.Text("Indicios de Riesgo Detectados:", size=20, weight=ft.FontWeight.BOLD, color="black")

        self.datos_alumno_table1 = ft.DataTable(
            heading_row_color=color_Docente,
                heading_text_style=ft.TextStyle(color="white", weight=ft.FontWeight.BOLD),
                bgcolor="white",
                data_text_style=ft.TextStyle(color="black"),
                vertical_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
                horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
                width=800,
            columns=[
                ft.DataColumn(ft.Text("Nombre Completo", text_align=ft.TextAlign.CENTER)),
                ft.DataColumn(ft.Text("RUT", text_align=ft.TextAlign.CENTER)),
                ft.DataColumn(ft.Text("Sexo", text_align=ft.TextAlign.CENTER)),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Container(content=self.nombre_completo_es, alignment=ft.alignment.center)),
                        ft.DataCell(ft.Container(content=self.rut_es, alignment=ft.alignment.center)),
                        ft.DataCell(ft.Container(content=self.sexo_es, alignment=ft.alignment.center)),
                    ]
                )
            ],
        )
        
        self.datos_alumno_table2 = ft.DataTable(
            heading_row_color=color_Docente,
                heading_text_style=ft.TextStyle(color="white", weight=ft.FontWeight.BOLD),
                bgcolor="white",
                data_text_style=ft.TextStyle(color="black"),
                border=ft.border.symmetric(vertical=ft.border.BorderSide(2, ft.Colors.BLACK)),
                horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
                vertical_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
                width=800,
            columns=[
                ft.DataColumn(ft.Text("Fecha de nacimento", text_align=ft.TextAlign.CENTER)),
                ft.DataColumn(ft.Text("Curso", text_align=ft.TextAlign.CENTER)),
                ft.DataColumn(ft.Text("Repitencias", text_align=ft.TextAlign.CENTER)),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Container(content=self.fecha_nacimiento_es, alignment=ft.alignment.center)),
                        ft.DataCell(ft.Container(content=self.curso_es, alignment=ft.alignment.center)),
                        ft.DataCell(ft.Container(content=ft.Text("xxxx"), alignment=ft.alignment.center)),
                    ]
                )
            ],
        )
        self.datos_alumno_table3 = ft.DataTable(
            heading_row_color=color_Docente,
                heading_text_style=ft.TextStyle(color="white", weight=ft.FontWeight.BOLD),
                bgcolor="white",
                data_text_style=ft.TextStyle(color="black"),
                horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
                width=800,
            columns=[
                ft.DataColumn(ft.Text("Profesor Jefe", text_align=ft.TextAlign.CENTER)),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Container(content=self.profesor_jefe, alignment=ft.alignment.center)),
                    ]
                )
            ],
        )
        self.profesor_emisor_nombre = ft.Text("", color="black")
        self.profesor_emisor_rut = ft.Text("", color="black")
        self.profesor_emisor_cargo = ft.Text("", color="black")

        self.datos_profesor_table1 = ft.DataTable(
            heading_row_color=color_Docente,
            heading_text_style=ft.TextStyle(color="white", weight=ft.FontWeight.BOLD),
            bgcolor="white",
            data_text_style=ft.TextStyle(color="black"),
            vertical_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
            width=800,
            columns=[
                ft.DataColumn(ft.Text("Nombre", text_align=ft.TextAlign.CENTER)),                
                ft.DataColumn(ft.Text("RUT", text_align=ft.TextAlign.CENTER)),
                ft.DataColumn(ft.Text("Cargo", text_align=ft.TextAlign.CENTER)),
                
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Container(content=self.profesor_emisor_nombre, alignment=ft.alignment.center)),
                        ft.DataCell(ft.Container(content=self.profesor_emisor_rut, alignment=ft.alignment.center)),
                        ft.DataCell(ft.Container(content=self.profesor_emisor_cargo, alignment=ft.alignment.center)),
                    ]
                )
            ],
            
        )
        self.datos_profesor_table2 = ft.DataTable(
            heading_row_color=color_Docente,
            heading_text_style=ft.TextStyle(color="white", weight=ft.FontWeight.BOLD),
            bgcolor="white",
            data_text_style=ft.TextStyle(color="black"),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
            width=800,
            columns=[
                ft.DataColumn(ft.Text("Fecha de informe", text_align=ft.TextAlign.CENTER)),
                
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Container(content=self.fecha_informe, alignment=ft.alignment.center)),
                    ]
                )
            ],
            
        )
        self.datos_resultados_table1 = ft.DataTable(
            heading_row_color=color_Docente,
                heading_text_style=ft.TextStyle(color="white", weight=ft.FontWeight.BOLD),
                bgcolor="white",
                data_text_style=ft.TextStyle(color="black"),
                border=ft.border.symmetric(vertical=ft.border.BorderSide(2, ft.Colors.BLACK)),
                vertical_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
                horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
                width=800,
                data_row_max_height=100,
            columns=[
                ft.DataColumn(ft.Text("Puntaje obtenido", text_align=ft.TextAlign.CENTER)),
                ft.DataColumn(ft.Text("Porcentaje de riesgo", text_align=ft.TextAlign.CENTER))
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Container(content=self.puntaje_obtenido, alignment=ft.alignment.center)),
                        ft.DataCell(ft.Container(content=self.porcentaje_riesgo, alignment=ft.alignment.center)),
                    ]
                )
            ],
        )

        self.datos_indicios_table = ft.DataTable(
            heading_row_color=color_Docente,
            heading_text_style=ft.TextStyle(color="white", weight=ft.FontWeight.BOLD),
            bgcolor="white",
            data_text_style=ft.TextStyle(color="black"),
            border=ft.border.all(2, ft.Colors.BLACK),
            data_row_max_height=90,
            vertical_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
            columns=[
                ft.DataColumn(ft.Text("Categoría", text_align=ft.TextAlign.CENTER)),
                ft.DataColumn(ft.Text("Porcentaje de Riesgo", text_align=ft.TextAlign.CENTER)),
                ft.DataColumn(ft.Text("Indicios Detectados", text_align=ft.TextAlign.CENTER)),
            ],
            rows=[
                ft.DataRow(cells=[
                    ft.DataCell(ft.Container(content=ft.Text("Atención"), alignment=ft.alignment.center)),
                    ft.DataCell(ft.Container(content=self.porcentaje_atencion, alignment=ft.alignment.center)),
                
                    ft.DataCell(ft.Container(
                        content=self.indicios_atencion, # Asegura el word wrap
                        alignment=ft.alignment.center_left, 
                    )),
                ]),
                ft.DataRow(cells=[
                    ft.DataCell(ft.Container(content=ft.Text("Memoria"), alignment=ft.alignment.center)),
                    ft.DataCell(ft.Container(content=self.porcentaje_memoria, alignment=ft.alignment.center)),
                    ft.DataCell(ft.Container(
                        content=self.indicios_memoria, 
                        alignment=ft.alignment.center_left, 
                        padding=1,
                    )),
                ]),
                ft.DataRow(cells=[
                    ft.DataCell(ft.Container(content=ft.Text("Social"), alignment=ft.alignment.center)),
                    ft.DataCell(ft.Container(content=self.porcentaje_social, alignment=ft.alignment.center)),
                    ft.DataCell(ft.Container(
                        content=self.indicios_social, # Aplicado no_wrap
                        alignment=ft.alignment.center_left, 
                        padding=1,
                    )),
                ]),
                ft.DataRow(cells=[
                    ft.DataCell(ft.Container(content=ft.Text("Emocional"), alignment=ft.alignment.center)),
                    ft.DataCell(ft.Container(content=self.porcentaje_emocional, alignment=ft.alignment.center)),
                    ft.DataCell(ft.Container(
                        content=self.indicios_emocional, # Aplicado no_wrap
                        alignment=ft.alignment.center_left, 
                        padding=1,
                    )),
                ]),
            ],
        )

        self.contenedor_datos_del_alumno = ft.Container(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        width=800,
                        spacing=0, # Elimina el espacio vertical entre las tablas
                        controls=[
                            self.titulo_datos_est, 
                            ft.Container(
                                border=ft.border.all(2, ft.Colors.BLACK),
                                content=ft.Column(
                                    controls=[self.datos_alumno_table1, self.datos_alumno_table2, self.datos_alumno_table3],
                                    spacing=0
                                )
                            )
                        ]
                    )
                ]
            )
        )
        self.contenedor_datos_del_profesor = ft.Container(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        width=800,
                        controls=[
                            self.titulo_datos_pro,
                            ft.Container(
                                border=ft.border.all(2, ft.Colors.BLACK),
                                content=ft.Column(
                                    controls=[self.datos_profesor_table1, self.datos_profesor_table2],
                                    spacing=0
                                )
                            ),
                            
                            ]
                    )
                ]
            )
        )
        self.contenedor_datos_resultados = ft.Container(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        width=800,
                        controls=[self.titulo_resultados_test, self.datos_resultados_table1]
                    )
                ]
            )
        )
        self.contenedor_indicios = ft.Container(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        controls=[self.titulo_indicios, self.datos_indicios_table]
                    )
                ]
            )
        )

        self.generate_pdf_button = ft.ElevatedButton("Generar PDF", on_click=controller.generar_pdf, icon=ft.icons.PICTURE_AS_PDF, bgcolor=color_Docente, color=ft.colors.WHITE)
        self.feedback_text = ft.Text("", size=16, weight=ft.FontWeight.BOLD)

        view = ft.View(
            "/export_pdf/:res_det_id",
            scroll=ft.ScrollMode.ADAPTIVE,
            bgcolor=color_Background_PIE,
            controls=[
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Exportar a PDF", size=30, weight=ft.FontWeight.BOLD),
                            ft.Row(
                                controls=[self.contenedor_datos_del_alumno],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            ft.Row(
                                controls=[self.contenedor_datos_del_profesor],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            ft.Row(
                                controls=[self.contenedor_datos_resultados],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            ft.Row(
                                controls=[self.contenedor_indicios],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            self.generate_pdf_button,
                            self.feedback_text,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20
                    ),
                ),
                    
            ],
        )
        super().__init__(model, view, controller)
