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
        self.nombre_completo_es = ft.Text("",color="black")
        self.rut_es = ft.Text("",color="black")
        self.curso_es = ft.Text("", color="black")
        self.sexo_es = ft.Text("", color="black")

        self.datos_alumno_table1 = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nombre Completo")),
                ft.DataColumn(ft.Text("RUT")),
                ft.DataColumn(ft.Text("Sexo")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(self.nombre_completo_es),
                        ft.DataCell(self.rut_es),
                        ft.DataCell(self.sexo_es),
                    ]
                )
            ],
            expand=True,
        )
        self.datos_alumno_table2 = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Fecha de nacimento")),
                ft.DataColumn(ft.Text("Sexo")),
                ft.DataColumn(ft.Text("Curso")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(self.nombre_completo_es),
                        ft.DataCell(self.rut_es),
                        ft.DataCell(self.curso_es),
                    ]
                )
            ],
            expand=True,
        )

        
        self.contenedor_datos_del_alumno = ft.Container(
            expand=True,
            content=ft.Column(
                [ft.Row([self.datos_alumno_table1])]

            ))

        view = ft.View(
            "/export_pdf/:res_det_id",
            bgcolor=color_Background_PIE,
            controls=[
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        [
                            ft.Text("Exportar a PDF", size=30, weight=ft.FontWeight.BOLD),
                            self.contenedor_datos_del_alumno 
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ),
                    
            ],
        )
        super().__init__(model, view, controller)
