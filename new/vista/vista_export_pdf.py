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

        self.datos_alumno_table1 = ft.DataTable(
            heading_row_color=color_Docente,
                heading_text_style=ft.TextStyle(color="white", weight=ft.FontWeight.BOLD),
                bgcolor="white",
                data_text_style=ft.TextStyle(color="black"),
                border=ft.border.all(2, ft.Colors.BLACK),
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
                border=ft.border.all(2, ft.Colors.BLACK),
                vertical_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
                horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
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
                border=ft.border.all(2, ft.Colors.BLACK),
                vertical_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
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

        
        self.contenedor_datos_del_alumno = ft.Container(
            # Eliminamos el contenedor exterior y centramos una columna con ancho fijo.
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        width=800, # Ancho fijo para ambas tablas
                        controls=[self.datos_alumno_table1, self.datos_alumno_table2,self.datos_alumno_table3]
                    )
                ]
            )
        )

        self.generate_pdf_button = ft.ElevatedButton("Generar PDF", on_click=controller.generar_pdf, icon=ft.icons.PICTURE_AS_PDF, bgcolor=color_Docente, color=ft.colors.WHITE)
        self.feedback_text = ft.Text("", size=16, weight=ft.FontWeight.BOLD)
        self.download_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER)

        view = ft.View(
            "/export_pdf/:res_det_id",
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
                            self.generate_pdf_button,
                            self.download_row,
                            self.feedback_text,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20
                    ),
                ),
                    
            ],
        )
        super().__init__(model, view, controller)
