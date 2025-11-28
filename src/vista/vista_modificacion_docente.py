import flet as ft
from flet_mvc import FletView
from colors import color_Docente, color_Background_PIE

class ModificacionDocenteView(FletView):
    def __init__(self, controller, model):
        self.feedback_snackbar = ft.SnackBar(content=ft.Text(""), bgcolor=ft.Colors.GREEN)

        self.add_dialog = ft.AlertDialog(
            modal=True, title=ft.Text("Confirmar Creación"),
            content=ft.Text("¿Desea agregar este nuevo profesor?"),
            actions=[
                ft.TextButton("Sí, agregar", on_click=controller.add_profesor),
                ft.TextButton("Cancelar", on_click=lambda e: controller.close_dialog(e, 'add'))
            ]
        )
        self.edit_dialog = ft.AlertDialog(
            modal=True, title=ft.Text("Confirmar Actualización"),
            content=ft.Text("¿Desea guardar los cambios realizados?"),
            actions=[
                ft.TextButton("Sí, guardar", on_click=controller.update_profesor),
                ft.TextButton("Cancelar", on_click=lambda e: controller.close_dialog(e, 'edit'))
            ]
        )
        self.delete_dialog = ft.AlertDialog(
            modal=True, title=ft.Text("Confirmar Eliminación"),
            content=ft.Text("¿Está seguro? Esta acción no se puede deshacer."),
            actions=[
                ft.TextButton("Sí, eliminar", on_click=controller.delete_profesor, style=ft.ButtonStyle(color=ft.Colors.RED)),
                ft.TextButton("Cancelar", on_click=lambda e: controller.close_dialog(e, 'delete'))
            ]
        )
        self.delete_student_dialog = ft.AlertDialog(
            modal=True, title=ft.Text("Confirmar Eliminación de Estudiante"),
            content=ft.Text("¿Está seguro? Se eliminarán todos los datos del estudiante, incluyendo tests y resultados. Esta acción no se puede deshacer."),
            actions=[
                ft.TextButton("Sí, eliminar", on_click=controller.delete_estudiante, style=ft.ButtonStyle(color=ft.Colors.RED)),
                ft.TextButton("Cancelar", on_click=lambda e: controller.close_dialog(e, 'delete_student'))
            ]
        )

        self.data_table = ft.DataTable(
            
            heading_row_color=color_Docente,
            columns=[
                ft.DataColumn(ft.Text("Nombres")), ft.DataColumn(ft.Text("Apellidos")),
                ft.DataColumn(ft.Text("RUT")),
                ft.DataColumn(ft.Text("Cargo")),
                ft.DataColumn(ft.Text("Estado")),
            ],
            heading_text_style=ft.TextStyle(color="white", weight=ft.FontWeight.BOLD),
            data_text_style=ft.TextStyle(color="black"),
            border=ft.border.all(1, ft.Colors.BLACK),
            vertical_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
            data_row_color={
                ft.ControlState.HOVERED: ft.Colors.with_opacity(0.6, color_Docente),
                ft.ControlState.SELECTED: ft.Colors.with_opacity(0.5, color_Docente),
            },
            rows=[]
        )
        self.profesor_search_field = ft.TextField(
            bgcolor="white",
            label="Buscar Profesor por Nombre o RUT",
            on_change=lambda e: controller.search_profesor(reset_page=True),
            color="black", label_style=ft.TextStyle(color="black")
        )
        self.prev_button_pro = ft.IconButton(ft.Icons.KEYBOARD_ARROW_LEFT, on_click=controller.prev_page_pro,icon_color=color_Docente)
        self.page_label_pro = ft.Text("Página 1 de 1", color="black")
        self.next_button_pro = ft.IconButton(ft.Icons.KEYBOARD_ARROW_RIGHT, on_click=controller.next_page_pro,icon_color=color_Docente)
        self.pagination_controls_pro = ft.Row([self.prev_button_pro, self.page_label_pro, self.next_button_pro], alignment=ft.MainAxisAlignment.CENTER)

        self.nombre1 = ft.TextField(bgcolor="white",label="Primer nombre", color="black", label_style=ft.TextStyle(color="black"))
        self.nombre2 = ft.TextField(bgcolor="white",label="Segundo nombre", color="black", label_style=ft.TextStyle(color="black"))
        self.nombre3 = ft.TextField(bgcolor="white",label="Tercer nombre", color="black", label_style=ft.TextStyle(color="black"))
        self.apellido_pat = ft.TextField(bgcolor="white",label="Apellido paterno", color="black", label_style=ft.TextStyle(color="black"))
        self.apellido_mat = ft.TextField(bgcolor="white",label="Apellido materno", color="black", label_style=ft.TextStyle(color="black"))
        self.rut_field = ft.TextField(bgcolor="white",label="RUT", width=300, color="black", on_change=controller.formato_rut, label_style=ft.TextStyle(color="black"))
        self.cargo_field = ft.Dropdown(
            label="Cargo", width=500,
            options=[ft.dropdown.Option("Profesional PIE"), ft.dropdown.Option("Docente")],
            color="black", on_change=controller.toggle_cursos_visibility,
            label_style=ft.TextStyle(color="black")
        )
        self.estado_field = ft.Dropdown(
            label="Estado", width=500,
            options=[ft.dropdown.Option("Habilitado"), ft.dropdown.Option("Inhabilitado")],
            color="black",
            label_style=ft.TextStyle(color="black")
        )

        self.cursos_checkbox_group = ft.Container(
            visible=False,
            height=250,
            border=ft.border.all(1, ft.Colors.BLACK),
            border_radius=5, padding=10,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                controls=[ft.Text("Cursos a Cargo:", weight=ft.FontWeight.BOLD, color="black")]
            )
        )

        self.add_button = ft.IconButton(icon=ft.Icons.ADD, icon_color=ft.Colors.WHITE, bgcolor=color_Docente, tooltip="Añadir nuevo", on_click=lambda e: controller.open_dialog(e, 'add'))
        self.edit_button = ft.IconButton(icon=ft.Icons.EDIT, icon_color=ft.Colors.WHITE, bgcolor="#007bff", visible=False, tooltip="Editar", on_click=lambda e: controller.open_dialog(e, 'edit'))
        self.delete_button = ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.WHITE, bgcolor="#dc3545", visible=False, tooltip="Eliminar", on_click=lambda e: controller.open_dialog(e, 'delete'))

        self.curso_data_table = ft.DataTable(
            heading_row_color=color_Docente,
            
            columns=[
                ft.DataColumn(ft.Text("Nombre Curso")), ft.DataColumn(ft.Text("Año")), ft.DataColumn(ft.Text("Estado")),
            ],
            heading_text_style=ft.TextStyle(color="white", weight=ft.FontWeight.BOLD),
            data_text_style=ft.TextStyle(color="black"),
            border=ft.border.all(1, ft.Colors.BLACK),
            vertical_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
            data_row_color={
                ft.ControlState.HOVERED: ft.Colors.with_opacity(0.6, color_Docente),
                ft.ControlState.SELECTED: ft.Colors.with_opacity(0.5, color_Docente),
            },
            rows=[]
        )
        self.curso_search_field = ft.TextField(bgcolor="white",
            label="Buscar Curso por Nombre o Año",
            on_change=lambda e: controller.search_curso(reset_page=True),
            color="black", label_style=ft.TextStyle(color="black")
        )
        self.curso_name_field = ft.TextField(bgcolor="white",label="Nombre del Curso", read_only=True, color="black", label_style=ft.TextStyle(color="black"))
        self.curso_year_field = ft.TextField(bgcolor="white",label="Año", read_only=True, color="black", label_style=ft.TextStyle(color="black"))
        self.curso_state_field = ft.Dropdown(label="Estado del Curso", width=300, options=[ft.dropdown.Option("Habilitado"), ft.dropdown.Option("Inhabilitado")], color="black", label_style=ft.TextStyle(color="black"))
        self.update_curso_button = ft.ElevatedButton("Actualizar Curso", on_click=controller.update_curso, visible=False, bgcolor=color_Docente, color=ft.Colors.WHITE)
        self.prev_button_cursos = ft.IconButton(ft.Icons.KEYBOARD_ARROW_LEFT, on_click=controller.prev_page_cursos, icon_color=color_Docente)
        self.page_label_cursos = ft.Text("Página 1 de 1", color="black")
        self.next_button_cursos = ft.IconButton(ft.Icons.KEYBOARD_ARROW_RIGHT, on_click=controller.next_page_cursos, icon_color=color_Docente)
        self.pagination_controls_cursos = ft.Row([self.prev_button_cursos, self.page_label_cursos, self.next_button_cursos], alignment=ft.MainAxisAlignment.CENTER)

        self.bulk_student_input = ft.TextField(bgcolor="white",
            label="Lista de Estudiantes",
            multiline=True,
            min_lines=8,
            hint_text="Pegue aquí la lista de estudiantes. Un estudiante por línea.\nFormato: Nombres, Apellido Pat, Apellido Mat, RUT, Fecha Nac (YYYY-MM-DD), Sexo, Curso, Año, Establecimiento",
            color="black", label_style=ft.TextStyle(color="black")
        )
        self.add_student_button = ft.ElevatedButton(
            "Añadir Estudiantes", on_click=controller.add_estudiantes_en_masa,
            bgcolor=color_Docente, color=ft.Colors.WHITE
        )
        self.student_search_field = ft.TextField(bgcolor="white",
            label="Buscar Estudiante por Nombre o RUT",
            on_change=lambda e: controller.search_estudiante(reset_page=True),
            color="black", label_style=ft.TextStyle(color="black")
        )
        self.student_data_table = ft.DataTable(
            
            heading_row_color=color_Docente,
            columns=[
                ft.DataColumn(ft.Text("Nombre")), ft.DataColumn(ft.Text("Apellidos")),
                ft.DataColumn(ft.Text("RUT")), ft.DataColumn(ft.Text("Curso")),
                ft.DataColumn(ft.Text("Establecimiento")),
            ],
            heading_text_style=ft.TextStyle(color="white", weight=ft.FontWeight.BOLD),
            data_text_style=ft.TextStyle(color="black"),
            border=ft.border.all(1, ft.Colors.BLACK),
            vertical_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
            data_row_color={
                ft.ControlState.HOVERED: ft.Colors.with_opacity(0.6, color_Docente),
                ft.ControlState.SELECTED: ft.Colors.with_opacity(0.5, color_Docente),
            },
            rows=[]
        )
        self.delete_student_button = ft.ElevatedButton(
            "Eliminar Estudiante Seleccionado", on_click=lambda e: controller.open_dialog(e, 'delete_student'),
            visible=False, bgcolor=ft.Colors.RED, color=ft.Colors.WHITE
        )
        self.prev_button_estudiantes = ft.IconButton(ft.Icons.KEYBOARD_ARROW_LEFT, on_click=controller.prev_page_estudiantes, icon_color=color_Docente)
        self.page_label_estudiantes = ft.Text("Página 1 de 1", color="black")
        self.next_button_estudiantes = ft.IconButton(ft.Icons.KEYBOARD_ARROW_RIGHT, on_click=controller.next_page_estudiantes, icon_color=color_Docente)
        self.pagination_controls_estudiantes = ft.Row([self.prev_button_estudiantes, self.page_label_estudiantes, self.next_button_estudiantes], alignment=ft.MainAxisAlignment.CENTER)

        view = ft.View(
            "/gestion_docente",
            scroll=ft.ScrollMode.AUTO,
            bgcolor=color_Background_PIE,
            controls=[
                
                ft.Row([ft.Text("Inicio >", weight=ft.FontWeight.BOLD, color="black"), ft.Text("Gestión de Docentes", weight=ft.FontWeight.BOLD, color=color_Docente)], alignment=ft.MainAxisAlignment.START),
                ft.ResponsiveRow(
                    controls=[
                        ft.Container(
                            col={"sm": 12},
                            content=ft.Column([
                                ft.Text("Añadir / Editar Docente:", size=20, weight=ft.FontWeight.BOLD, color="black"),
                                self.profesor_search_field,
                                ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER,spacing=15, controls=[
                                ft.Row([self.data_table], scroll=ft.ScrollMode.AUTO, expand=True, alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row([self.pagination_controls_pro,], alignment=ft.MainAxisAlignment.CENTER),])
                            ])
                        )
                    ]
                ),
                ft.ResponsiveRow(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            col={"sm": 12, "md": 8},
                            content=ft.Column(
                                controls=[
                                    ft.ResponsiveRow(controls=[
                                        ft.Container(content=self.nombre1, col={"sm": 12, "md": 6}),
                                        ft.Container(content=self.nombre2, col={"sm": 12, "md": 6}),
                                    ]),
                                    ft.ResponsiveRow(controls=[
                                        ft.Container(content=self.nombre3, col={"sm": 12, "md": 6}),
                                        ft.Container(content=self.apellido_pat, col={"sm": 12, "md": 6}),
                                    ]),
                                    ft.ResponsiveRow(controls=[
                                        ft.Container(content=self.apellido_mat, col={"sm": 12, "md": 6}),
                                        ft.Container(content=self.rut_field, col={"sm": 12, "md": 6}),
                                        ft.Container(content=self.cargo_field, col={"sm": 12, "md": 6}),
                                        ft.Container(content=self.estado_field, col={"sm": 12, "md": 6}),
                                    ]),
                                ]
                            )
                        ),
                        ft.Container(content=self.cursos_checkbox_group, col={"sm": 12, "md": 4}),
                    ]
                ),
                ft.Row([self.add_button, self.edit_button, self.delete_button], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                ft.ResponsiveRow(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            col={"sm": 12, "md": 10, "lg": 12},
                            content=ft.Column([
                                ft.Text("Gestión de Cursos", size=20, weight=ft.FontWeight.BOLD, color="black"),
                                self.curso_search_field,
                                ft.Column(spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=[
                                ft.Row([self.curso_data_table], scroll=ft.ScrollMode.AUTO, expand=True, alignment=ft.MainAxisAlignment.CENTER),
                                self.pagination_controls_cursos,
                                ])
                            ])
                        )
                    ]
                ),
                ft.ResponsiveRow(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Container(content=self.curso_name_field, col={"sm": 12, "md": 4}),
                        ft.Container(content=self.curso_year_field, col={"sm": 12, "md": 4}),
                        ft.Container(content=self.curso_state_field, col={"sm": 12, "md": 4}),
                    ]
                ),
                ft.Row([self.update_curso_button], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                ft.ResponsiveRow(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            col={"sm": 12, "md": 10, "lg": 8},
                            content=ft.Column([
                                ft.Text("Añadir Estudiante", size=20, weight=ft.FontWeight.BOLD, color="black"),
                                self.bulk_student_input,
                                ft.Row([self.add_student_button], alignment=ft.MainAxisAlignment.CENTER),
                            ])
                        )
                    ]
                ),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                ft.ResponsiveRow(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            col={"sm": 12, "md": 10, "lg": 12},
                            content=ft.Column([ 
                                ft.Text("Eliminar Estudiante", size=20, weight=ft.FontWeight.BOLD, color="black"),
                                self.student_search_field,
                                ft.Column(spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=[
                                ft.Row([self.student_data_table], scroll=ft.ScrollMode.AUTO, expand=True, alignment=ft.MainAxisAlignment.CENTER),
                                self.pagination_controls_estudiantes,])
                            ])
                        )
                    ]
                ),
                ft.Row([self.delete_student_button], alignment=ft.MainAxisAlignment.CENTER),
                self.feedback_snackbar, self.add_dialog, self.edit_dialog, self.delete_dialog, self.delete_student_dialog,
            ]
        )
        super().__init__(model, view, controller)
        self.page = controller.page