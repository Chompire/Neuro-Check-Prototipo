import flet as ft
from flet_mvc import FletView
from colors import color_Docente, color_Background_PIE

class ModificacionDocenteView(FletView):
    def __init__(self, controller, model):
        self.controller = controller
        self.feedback_snackbar = ft.SnackBar(content=ft.Text(""), bgcolor=ft.colors.GREEN)

        # --- Dialogs ---
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
                ft.TextButton("Sí, eliminar", on_click=controller.delete_profesor, style=ft.ButtonStyle(color=ft.colors.RED)),
                ft.TextButton("Cancelar", on_click=lambda e: controller.close_dialog(e, 'delete'))
            ]
        )

        # --- DataTable ---
        self.data_table = ft.DataTable(
            heading_row_color=color_Docente,
            columns=[
                ft.DataColumn(ft.Text("Nombres")), ft.DataColumn(ft.Text("Apellidos")),
                ft.DataColumn(ft.Text("RUT")), ft.DataColumn(ft.Text("Email")),
                ft.DataColumn(ft.Text("Cargo")), ft.DataColumn(ft.Text("Curso")),
                ft.DataColumn(ft.Text("Estado")),
            ],
            heading_text_style=ft.TextStyle(color="white", weight=ft.FontWeight.BOLD),
            data_text_style=ft.TextStyle(color="black"),
            border=ft.border.all(1, ft.colors.BLACK),
            vertical_lines=ft.border.BorderSide(1, ft.colors.BLACK),
            horizontal_lines=ft.border.BorderSide(1, ft.colors.BLACK),
            data_row_color={
                ft.ControlState.HOVERED: ft.colors.with_opacity(0.6, color_Docente),
                ft.ControlState.SELECTED: ft.colors.with_opacity(0.5, color_Docente),
            },
            rows=[]
        )

        # --- Form Fields ---
        self.nombre1 = ft.TextField(label="Primer nombre", color="black", label_style=ft.TextStyle(color="black"))
        self.nombre2 = ft.TextField(label="Segundo nombre", color="black", label_style=ft.TextStyle(color="black"))
        self.apellido_pat = ft.TextField(label="Apellido paterno", color="black", label_style=ft.TextStyle(color="black"))
        self.apellido_mat = ft.TextField(label="Apellido materno", color="black", label_style=ft.TextStyle(color="black"))
        self.rut_field = ft.TextField(label="RUT", width=300, color="black", on_change=controller.formato_rut, label_style=ft.TextStyle(color="black"))
        self.cargo_field = ft.Dropdown(
            label="Cargo", width=300,
            options=[ft.dropdown.Option("Profesional PIE"), ft.dropdown.Option("Docente")],
            color="black",
            label_style=ft.TextStyle(color="black")
        )
        self.curso_field = ft.Dropdown(
            label="Curso", width=300,
            options=controller.lista_cursos(),
            color="black",
            label_style=ft.TextStyle(color="black")
        )
        self.estado_field = ft.Dropdown(
            label="Estado", width=300,
            options=[ft.dropdown.Option("Habilitado"), ft.dropdown.Option("Inhabilitado")],
            color="black",
            label_style=ft.TextStyle(color="black")
        )

        self.add_button = ft.IconButton(icon=ft.icons.ADD, icon_color=ft.colors.WHITE, bgcolor=color_Docente, tooltip="Añadir nuevo", on_click=lambda e: controller.open_dialog(e, 'add'))
        self.edit_button = ft.IconButton(icon=ft.icons.EDIT, icon_color=ft.colors.WHITE, bgcolor="#007bff", visible=False, tooltip="Editar", on_click=lambda e: controller.open_dialog(e, 'edit'))
        self.delete_button = ft.IconButton(icon=ft.icons.DELETE, icon_color=ft.colors.WHITE, bgcolor="#dc3545", visible=False, tooltip="Eliminar", on_click=lambda e: controller.open_dialog(e, 'delete'))

        view = ft.View(
            "/modificacion_docente",
            bgcolor=color_Background_PIE,
            controls=[
                self.feedback_snackbar, self.add_dialog, self.edit_dialog, self.delete_dialog,
                ft.Column(
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Lista de Docentes", size=20, weight=ft.FontWeight.BOLD, color="black"),
                                self.data_table,
                            ]),
                            padding=10, border=ft.border.all(2, ft.colors.BLACK), border_radius=8, bgcolor=ft.colors.WHITE
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Añadir / Editar Docente", size=20, weight=ft.FontWeight.BOLD, color="black"),
                                ft.Row([self.nombre1, self.nombre2]),
                                ft.Row([self.apellido_pat, self.apellido_mat]),
                                ft.Row([self.rut_field]),
                                ft.Row([self.cargo_field, self.curso_field, self.estado_field]),
                                ft.Row([self.add_button, self.edit_button, self.delete_button]),
                            ]),
                            padding=10, border=ft.border.all(2, ft.colors.BLACK), border_radius=8, bgcolor=ft.colors.WHITE
                        )
                    ]
                )
            ]
        )
        super().__init__(model, view, controller)
        self.page = controller.page # Guardar referencia a la página

    def show_feedback(self, message: str, color: str):
        self.feedback_snackbar.content = ft.Text(message)
        self.feedback_snackbar.bgcolor = color
        self.feedback_snackbar.open = True
        self.page.update()