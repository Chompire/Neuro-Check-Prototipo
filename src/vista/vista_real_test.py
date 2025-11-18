import flet as ft
from flet_mvc import FletView # Importamos nuestra nueva clase base
from colors import color_Background_Docente,color_Docente,color_Background_PIE


class RealizarTestView(FletView):  # Heredamos de BaseView
    def __init__(self, controller, model):
        self.feedback_snackbar = ft.SnackBar(content=ft.Text(""))
        self.prev_button_test = ft.IconButton(ft.Icons.KEYBOARD_ARROW_LEFT, on_click=controller.prev_page_test,icon_color=color_Docente)
        self.page_label_test = ft.Text("Página 1 de 1", color="black")
        self.next_button_test = ft.IconButton(ft.Icons.KEYBOARD_ARROW_RIGHT, on_click=controller.next_page_test,icon_color=color_Docente)
        self.pagination_controls_test = ft.Row([self.prev_button_test, self.page_label_test, self.next_button_test], alignment=ft.MainAxisAlignment.CENTER)

        self.prev_button_est = ft.IconButton(ft.Icons.KEYBOARD_ARROW_LEFT, on_click=controller.prev_page_est,icon_color=color_Docente)
        self.page_label_est = ft.Text("Página 1 de 1", color="black")
        self.next_button_est = ft.IconButton(ft.Icons.KEYBOARD_ARROW_RIGHT, on_click=controller.next_page_est,icon_color=color_Docente)
        self.pagination_controls_est = ft.Row([self.prev_button_est, self.page_label_est, self.next_button_est], alignment=ft.MainAxisAlignment.CENTER)
        self.estudiante_search = ft.TextField(bgcolor=color_Docente,
            prefix_icon=ft.Icons.SEARCH,
            label="Buscar estudiante",
            on_change=lambda e: controller.est_search(reset_page=True),
            )
        
        self.test_search = ft.TextField(bgcolor=color_Docente,
            prefix_icon=ft.Icons.SEARCH,
            label="Buscar estudiante",
            on_change=lambda e: controller.test_search(reset_page=True),
            )
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
            bgcolor=color_Background_Docente, # Se establecerá un color base, main.py lo corregirá
            scroll=ft.ScrollMode.AUTO,
            controls=
            [                
                ft.Row([ft.Text("Inicio >", weight=ft.FontWeight.BOLD, color="black"), ft.Text("Realizar Test", weight=ft.FontWeight.BOLD, color=color_Docente)], alignment=ft.MainAxisAlignment.START), # This line already exists, no change needed.
                self.feedback_snackbar,
                ft.Column(
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[ # Esta es la lista de controles para la columna principal
                        ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                  controls=[ # Primera sección: "Seleccionar estudiante"
                                   ft.Row(controls=[
                                       ft.Text("Seleccionar estudiante:", size=20, weight=ft.FontWeight.BOLD, color="black"),
                                       self.next_button]),
                                       ft.Row(controls=[self.estudiante_search], expand=True),
                                       ft.Row([self.estudiante_table], scroll=ft.ScrollMode.AUTO),
                                       self.pagination_controls_est,
                                       ]),
                        ft.Divider(color="black"),
                        ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                  controls=[ # Segunda sección: "Terminar test incompleto"
                                   ft.Row(controls=[
                                       ft.Text("Terminar test incompleto:", size=20, weight=ft.FontWeight.BOLD, color="black"),
                                       self.upload_button]),
                                       ft.Row(controls=[self.test_search], expand=True),
                                       ft.Row([self.test_incompletos], scroll=ft.ScrollMode.AUTO),
                                       self.pagination_controls_test]),
                    ]
                )
            ] # Cierra la lista de controles de la vista
        ) # Cierra la llamada al constructor de ft.View
        super().__init__(model, view, controller)
        