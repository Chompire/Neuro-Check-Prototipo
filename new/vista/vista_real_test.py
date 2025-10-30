import flet as ft
from flet_mvc import FletView # Importamos nuestra nueva clase base
from colors import color_Background,color_Docente


class RealizarTestView(FletView):  # Heredamos de BaseView
    def __init__(self, controller, model):
        self.estudiante_search = ft.TextField(bgcolor=color_Docente,
            prefix_icon=ft.icons.SEARCH,
            label="Buscar estudiante",)
        self.estudiante_table = ft.DataTable(
            border=ft.border.all(2, ft.Colors.BLACK),
            bgcolor="white",
            heading_row_color= color_Docente,        
            heading_text_style=ft.TextStyle(color="white", weight=ft.FontWeight.BOLD),
            data_text_style=ft.TextStyle(color="black"),        
            vertical_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
            data_row_color={
            ft.ControlState.HOVERED: ft.Colors.with_opacity(0.6, color_Docente),    
            ft.ControlState.SELECTED: ft.Colors.with_opacity(0.5, color_Docente),                
                },
                    columns=[
                        
                        ft.DataColumn(ft.Text("Nombre")),
                        ft.DataColumn(ft.Text("Apellido")),
                        ft.DataColumn(ft.Text("Nacimiento")),
                        ft.DataColumn(ft.Text("RUT")),
                        ft.DataColumn(ft.Text("Curso")),
                        ft.DataColumn(ft.Text("Profesor Jefe")),
                    ],
                    rows=[] # Inicializamos las filas vacías
        )
        self.test_incompletos =ft.DataTable(
                heading_row_color= color_Docente,
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
                    ft.DataColumn(ft.Text("Nombre")),
                    ft.DataColumn(ft.Text("Apellido")),                    
                    ft.DataColumn(ft.Text("RUT")),
                    ft.DataColumn(ft.Text("Curso")),
                    ft.DataColumn(ft.Text("Profesor emisor")),                    
                    ft.DataColumn(ft.Text("Fecha de creación")),
                    ft.DataColumn(ft.Text("Estado")),
                ],
    )

        self.next_button = ft.ElevatedButton(
                text="Iniciar Test",
                icon=ft.Icons.PLAY_ARROW,
                icon_color=ft.Colors.WHITE,
                color=ft.Colors.WHITE,
                bgcolor=color_Docente,
                visible=False,
                on_click=controller.on_iniciar_test_click,
                width=150,
                height=40)
        self.upload_button = ft.ElevatedButton(
                text="Reanudar Test",
                icon=ft.Icons.PLAY_CIRCLE_OUTLINE,
                icon_color=ft.Colors.WHITE,
                color=ft.Colors.WHITE,
                bgcolor=color_Docente, 
                visible=False, 
                on_click=controller.on_reanudar_test_click,
                width=150,
                height=40)


        view = ft.View(
            
            "/realizar_test",
            bgcolor=color_Background,
            controls=
            [
                ft.Column(
                expand = True,
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Row(alignment=ft.MainAxisAlignment.CENTER,
                           controls=[ft.Column(controls=[
                               ft.Row(controls=[
                                   ft.Text("Seleccionar estudiante:", size=30, weight=ft.FontWeight.BOLD, color="black"),
                                   self.next_button]),
                                   ft.Row(controls=[self.estudiante_search]),
                                   self.estudiante_table]),
                                    ]),
                    
                    ft.Divider(color="black"),
                    ft.Row(alignment=ft.MainAxisAlignment.CENTER,
                           controls=[ft.Column(controls=[
                               ft.Row(controls=[
                                   ft.Text("Terminar test incompleto:", size=30, weight=ft.FontWeight.BOLD, color="black"),
                                   self.upload_button]), 
                                   self.test_incompletos]),
                                    ]),
                ],
            )
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        super().__init__(model, view, controller)
        