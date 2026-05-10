import flet as ft
from flet_mvc import FletView
from colors import color_Background_Docente,color_Docente

class MisTestsView(FletView):
    def __init__(self, controller, model):
        self.search_completos_field = ft.TextField(bgcolor="white",
            label="Buscar en mis tests (Nombre, Apellido o RUT del estudiante)",
            on_change=lambda e: controller.search_completos(reset_page=True),
            color="black", label_style=ft.TextStyle(color="black")
        )
        self.search_otros_field = ft.TextField(bgcolor="white",
            label="Buscar en tests de otros (Nombre, Apellido o RUT del estudiante)",
            on_change=lambda e: controller.search_otros(reset_page=True), 
            color="black", label_style=ft.TextStyle(color="black"),
            visible=False
        )

        self.test_completos_table = ft.DataTable(
            heading_row_color=color_Docente,
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
                ft.DataColumn(ft.Text("Nombre Est.")),
                ft.DataColumn(ft.Text("Apellido Est.")),
                ft.DataColumn(ft.Text("RUT Est.")),
                ft.DataColumn(ft.Text("Curso")),
                ft.DataColumn(ft.Text("Fecha de Creación")),
                ft.DataColumn(ft.Text("Fecha de Finalización")),
                ft.DataColumn(ft.Text("IDT")),
            ],
            rows=[]
        )
        
        self.prev_button_completos = ft.IconButton(ft.Icons.KEYBOARD_ARROW_LEFT, on_click=controller.prev_page_completos, icon_color=color_Docente)
        self.page_label_completos = ft.Text("Página 1 de 1", color="black")
        self.next_button_completos = ft.IconButton(ft.Icons.KEYBOARD_ARROW_RIGHT, on_click=controller.next_page_completos, icon_color=color_Docente)
        self.pagination_controls_completos = ft.Row([self.prev_button_completos, self.page_label_completos, self.next_button_completos], alignment=ft.MainAxisAlignment.CENTER)
        self.tests_profesores_title = ft.Text("Tests de otros profesores:", size=20, weight=ft.FontWeight.BOLD, color="black", visible=False, selectable=True)
        self.test_profesores_table = ft.DataTable(
            heading_row_color=color_Docente,
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
                ft.DataColumn(ft.Text("Nombre Est.")),
                ft.DataColumn(ft.Text("Apellido Est.")),
                ft.DataColumn(ft.Text("RUT Est.")),
                ft.DataColumn(ft.Text("Curso")),
                ft.DataColumn(ft.Text("Fecha de Creación")),
                ft.DataColumn(ft.Text("Fecha de Finalización")),
                ft.DataColumn(ft.Text("Profesor Emisor")),
                ft.DataColumn(ft.Text("IDT")),
            ],
            rows=[],
            visible=False
        )
        self.prev_button_otros = ft.IconButton(ft.Icons.KEYBOARD_ARROW_LEFT, on_click=controller.prev_page_otros, icon_color=color_Docente)
        self.page_label_otros = ft.Text("Página 1 de 1", color="black")
        self.next_button_otros = ft.IconButton(ft.Icons.KEYBOARD_ARROW_RIGHT, on_click=controller.next_page_otros, icon_color=color_Docente)
        self.pagination_controls_otros = ft.Row([self.prev_button_otros, self.page_label_otros, self.next_button_otros], alignment=ft.MainAxisAlignment.CENTER, visible=False)

        view = ft.View(
            "/mis_tests",
            scroll=ft.ScrollMode.AUTO,
            bgcolor=color_Background_Docente,
            controls=[
                ft.Row([ft.Text("Inicio >", weight=ft.FontWeight.BOLD, color="black"), ft.Text("Mis Tests", weight=ft.FontWeight.BOLD, color=color_Docente)], alignment=ft.MainAxisAlignment.START),
                ft.ResponsiveRow(
                    controls=[
                        ft.Container(
                            col={"sm": 12},
                            content=ft.Column([
                                ft.Text("Mis tests:", size=20, weight=ft.FontWeight.BOLD, color="black", selectable=True),
                                self.search_completos_field,
                                ft.Column(spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=[
                                ft.Row([self.test_completos_table], scroll=ft.ScrollMode.AUTO, expand=True, alignment=ft.MainAxisAlignment.CENTER),
                                self.pagination_controls_completos,]),
                                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                                self.tests_profesores_title,
                                self.search_otros_field,
                                ft.Column(spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=[
                                ft.Row([self.test_profesores_table], scroll=ft.ScrollMode.AUTO, expand=True, alignment=ft.MainAxisAlignment.CENTER),
                                self.pagination_controls_otros,])
                            ], expand=True)
                        )
                    ]
                )
            ]
        )
        super().__init__(model, view, controller)