import flet as ft
from flet_mvc import FletView
from colors import color_Background,color_Docente
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
        view = ft.View(
            "/perfil_docente",
            bgcolor=color_Background,
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
                            ft.Row(controls=[ft.Text("Resultados detallados:", size=30, weight=ft.FontWeight.BOLD, color="black")]),
                            ])
                            ])
                ]),            
        
            ]

        )
        super().__init__(model, view, controller)