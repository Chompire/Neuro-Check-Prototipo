import flet as ft
from flet_mvc import FletView
from colors import color_Background_Docente,color_Docente, color_Background_PIE

class MisTestsView(FletView):
    def __init__(self, controller, model):
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

        # Siempre crear la tabla, pero ocultarla por defecto
        self.tests_profesores_title = ft.Text("Tests de otros profesores:", size=20, weight=ft.FontWeight.BOLD, color="black", visible=False)
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
            visible=False # Oculto por defecto
        )

        self.prev_button_otros = ft.IconButton(ft.Icons.KEYBOARD_ARROW_LEFT, on_click=controller.prev_page_otros, icon_color=color_Docente)
        self.page_label_otros = ft.Text("Página 1 de 1", color="black")
        self.next_button_otros = ft.IconButton(ft.Icons.KEYBOARD_ARROW_RIGHT, on_click=controller.next_page_otros, icon_color=color_Docente)
        self.pagination_controls_otros = ft.Row([self.prev_button_otros, self.page_label_otros, self.next_button_otros], alignment=ft.MainAxisAlignment.CENTER, visible=False)

        # Build the column controls conditionally
        column_controls = [
            ft.Text("Mis tests:", size=20, weight=ft.FontWeight.BOLD, color="black"),
            ft.Row([self.test_completos_table], scroll=ft.ScrollMode.AUTO),
            self.pagination_controls_completos,
        ]
        # Añadir los controles de PIE, que estarán ocultos por defecto
        column_controls.extend([self.tests_profesores_title, ft.Row([self.test_profesores_table], scroll=ft.ScrollMode.AUTO), self.pagination_controls_otros])

        view = ft.View(
            "/mis_tests",
            scroll=ft.ScrollMode.AUTO,
            bgcolor=color_Background_Docente, # Se establecerá un color base, main.py lo corregirá
            controls=[
                ft.Row([ft.Text("Inicio >", weight=ft.FontWeight.BOLD, color="black"), ft.Text("Mis Tests", weight=ft.FontWeight.BOLD, color=color_Docente)], alignment=ft.MainAxisAlignment.START),
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=column_controls,
                )
            ]
        )
        super().__init__(model, view, controller)