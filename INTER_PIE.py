import flet as ft
import pyodbc
from DB import CONNECTION_STRING
from CRUD import profesorCREATE,profesorREAD, profesorUPDATE,profesorDELETE


color_PIE = "#CF6400"
def create_app_bar(page: ft.Page, title: str):
    return ft.AppBar(
        title=ft.TextButton(
            content=ft.Text("Neuro Check", size=25, weight=ft.FontWeight.BOLD, color="white"),
            on_click=lambda _: page.go("/inicio_profesor")
        ),
        bgcolor=color_PIE,
        center_title=False,
        actions=[
            ft.Row([
                ft.Text(title, color="white"),
                ft.PopupMenuButton(items=[
                    ft.PopupMenuItem(
                        icon=ft.Icons.EXIT_TO_APP,
                        text="Cerrar sesión",
                    ),
                ])
            ]),
        ]
    )

def create_inicio_view(page: ft.Page, profesor_data):
    doc_name = profesor_data[1] if profesor_data else "Desconocido"
    return ft.View(
        route="/inicio_profesor",
        bgcolor="#d1d1d1",
        controls=[
            create_app_bar(page, "Inicio"),
            ft.Container(
                expand=True,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Column(
                            expand=True,
                            scroll=ft.ScrollMode.AUTO,
                            controls=[
                                ft.Text("¡Bienvenido!", size=50, weight=ft.FontWeight.BOLD, color="black"),
                                ft.Text(f"Profesor {doc_name}", size=20, weight=ft.FontWeight.BOLD, color="black"),
                                    ft.Container(
                                    content=ft.Text(
                                        "¿Qué desea hacer?",
                                        size=25,
                                        weight=ft.FontWeight.BOLD,
                                        color="black",
                                    ),
                                    width=600,
                                ),
                                ft.Card(
                                    elevation=0,
                                    color=color_PIE,
                                    content=ft.Container(
                                        content=ft.Column([
                                            ft.ListTile(
                                                title=ft.Text("Realizar test", size=20, weight=ft.FontWeight.BOLD),
                                                subtitle=ft.Text(
                                                    "El test sirve para obtener el porcentaje de riesgo del estudiante para posiblemente derivarlo al equipo PIE.",
                                                    size=15
                                                ),
                                            ),
                                            ft.ElevatedButton(text="Entrar", color="black", bgcolor="#FCAD78")
                                        ]),
                                        width=600,
                                        padding=10,
                                    )
                                ),
                                ft.Card(
                                    color=color_PIE,
                                    content=ft.Container(
                                        content=ft.Column([
                                            ft.ListTile(
                                                title=ft.Text("Perfil docente", size=20, weight=ft.FontWeight.BOLD),
                                                subtitle=ft.Text(
                                                    "Puedes ver tu información personal y revisar los resultados de los tests.",
                                                    size=15
                                                ),
                                            ),
                                            ft.ElevatedButton(
                                                text="Entrar",
                                                color="black",
                                                bgcolor="#FCAD78",
                                                on_click=lambda _: page.go("/perfil_docente")
                                            )
                                        ]),
                                        width=600,
                                        padding=10
                                    )
                                ),
                                ft.Card(
                                    color=color_PIE,
                                    content=ft.Container(
                                        content=ft.Column([
                                            ft.ListTile(
                                                title=ft.Text("Modificación docente", size=20, weight=ft.FontWeight.BOLD),
                                                subtitle=ft.Text(
                                                    "Puedes realizar cambios en tu información personal o en la información de otros usuarios.",
                                                    size=15
                                                ),
                                            ),
                                            ft.ElevatedButton(
                                                text="Entrar",
                                                color="black",
                                                bgcolor="#FCAD78",
                                                on_click=lambda _: page.go("/modificación_docente")
                                            )
                                        ]),
                                        width=600,
                                        padding=10
                                    )
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=15
                        )
                    ]
                )
            )
        ]
    )

def modificación_docente(page: ft.Page, profesor_data):
    selected_prof_id = None
    original_selected_rut = None # Variable para guardar el RUT original al seleccionar
    password_define = "neurocheck2025"
    feedback_snackbar = ft.SnackBar(
        content=ft.Text(""),
        bgcolor=ft.Colors.GREEN_700
    )

    # --- Funciones de confirmación para los diálogos ---
    def confirm_add(e):
        page.dialog.open = False
        add_profesor_logic()

    def confirm_update(e):
        page.dialog.open = False
        update_profesor_logic()

    def confirm_delete(e):
        page.dialog.open = False
        delete_profesor_logic()

    def close_dialog(e):
        page.dialog.open = False
        page.update()

    # --- Diálogos de Alerta ---
    add_dialog = ft.AlertDialog(
        modal=True, title=ft.Text("Confirmar Creación"),
        content=ft.Text("¿Desea agregar este nuevo profesor?"),
        actions=[ft.TextButton("Sí, agregar", on_click=confirm_add), ft.TextButton("Cancelar", on_click=close_dialog)],
    )
    edit_dialog = ft.AlertDialog(
        modal=True, title=ft.Text("Confirmar Edición"),
        content=ft.Text("¿Desea guardar los cambios realizados?"),
        actions=[ft.TextButton("Sí, guardar", on_click=confirm_update), ft.TextButton("Cancelar", on_click=close_dialog)],
    )
    delete_dialog = ft.AlertDialog(
        modal=True, title=ft.Text("Confirmar Eliminación"),
        content=ft.Text("¿Está seguro de que desea eliminar a este profesor? Esta acción no se puede deshacer."),
        actions=[ft.TextButton("Sí, eliminar", on_click=confirm_delete, style=ft.ButtonStyle(color=ft.Colors.RED)), ft.TextButton("Cancelar", on_click=close_dialog)],
    )

    # --- Lógica de las operaciones (separada de los eventos de click) ---
    def add_profesor_logic():
        rut_a_verificar = rut_field.value
        if profesorREAD(pro_rut=rut_a_verificar):
            feedback_snackbar.content = ft.Text(f"Error: El RUT '{rut_a_verificar}' ya está registrado.")
            feedback_snackbar.bgcolor = ft.Colors.RED_700
            feedback_snackbar.open = True
            page.update()   
        else:
            cargo_valor = 1 if cargo_field.value == "Profesional PIE" else 0
            estado_valor = 1 if estado_field.value == "Habilitado" else 0
            profesorCREATE(datos_profesor=(
                nombre1.value,
                nombre2.value,
                nombre3.value,
                apellido_pat.value,
                apellido_mat.value,
                fecha_nacimiento_field.value,
                rut_a_verificar,
                cargo_valor,
                password_define,
                curso_field.value,
                estado_valor,
            ))
            feedback_snackbar.content = ft.Text("Profesor agregado con éxito")
            feedback_snackbar.bgcolor = ft.Colors.GREEN_700
            feedback_snackbar.open = True
            load_profesores_to_table()
            page.update()

    def update_profesor_logic():
        nonlocal selected_prof_id, original_selected_rut
        nuevo_rut = rut_field.value
        # 1. Verificar si el RUT ya existe para OTRO profesor
        profesor_existente = profesorREAD(pro_rut=rut_field.value)
        if profesor_existente and profesor_existente[0] != selected_prof_id:
            # 2. Si el nuevo RUT ya existe y no es del profesor actual, mostrar error
            feedback_snackbar.content = ft.Text(f"Error: El RUT '{rut_field.value}' ya está registrado para otro usuario.")
            feedback_snackbar.bgcolor = ft.Colors.RED_700
            feedback_snackbar.open = True
            page.update()
        elif selected_prof_id is not None:
            # 3. Si no hay duplicados, proceder con la actualización
            estado_valor = 1 if estado_field.value == "Habilitado" else 0
            cargo_valor = 1 if cargo_field.value == "Profesional PIE" else 0
            datos_actualizados = {
                "pro_nombre_1": nombre1.value, "pro_nombre_2": nombre2.value, "pro_nombre_3": nombre3.value,
                "pro_apellido_pat": apellido_pat.value, "pro_apellido_mat": apellido_mat.value,
                "pro_nacimiento": fecha_nacimiento_field.value, "pro_rut": nuevo_rut,
                "pro_cargo": cargo_valor, "lvl_curso": curso_field.value, "pro_state": estado_valor,
            }
            profesorUPDATE(selected_prof_id, datos_actualizados)
            feedback_snackbar.content = ft.Text("Profesor actualizado con éxito")
            feedback_snackbar.bgcolor = ft.Colors.GREEN_700
            feedback_snackbar.open = True
            load_profesores_to_table(id_to_select=selected_prof_id)

    def delete_profesor_logic():
        nonlocal selected_prof_id
        profesorDELETE(selected_prof_id)
        load_profesores_to_table()

    # --- Funciones que abren los diálogos (conectadas a los botones) ---
    def open_add_dialog(e):
        page.dialog = add_dialog
        add_dialog.open = True
        page.update()

    def open_edit_dialog(e):
        page.dialog = edit_dialog
        edit_dialog.open = True
        page.update()

    def open_delete_dialog(e):
        page.dialog = delete_dialog
        delete_dialog.open = True
        page.update()

    def on_row_select(e):
        nonlocal selected_prof_id, original_selected_rut
        selected_prof = e.control.data
        is_currently_selected = e.control.selected

        for row in data_table.rows:
            row.selected = False

        if not is_currently_selected:
            e.control.selected = True
            edit_button.visible = True
            delete_button.visible = True
            add_button.disabled = True  # Deshabilita el botón de añadir
            selected_prof_id = selected_prof[0]
            original_selected_rut = selected_prof[7] # Guardar el RUT original
            nombre1.value = selected_prof[1]
            nombre2.value = selected_prof[2]
            nombre3.value = selected_prof[3]
            apellido_pat.value = selected_prof[4]
            apellido_mat.value = selected_prof[5]
            fecha_nacimiento_field.value = selected_prof[6]
            rut_field.value = selected_prof[7]
            cargo_field.value = "Profesional PIE" if selected_prof[8] else "Profesor Docente"
            curso_field.value = selected_prof[10]
            estado_field.value = "Habilitado" if selected_prof[11] else "Inhabilitado"
            page.update()
                
        else:
            nombre1.value =None
            nombre2.value =None
            nombre3.value = None
            apellido_pat.value =None
            apellido_mat.value = None
            fecha_nacimiento_field.value = None
            rut_field.value = None
            cargo_field.value = None
            curso_field.value = None
            estado_field.value = None
            edit_button.visible = False
            delete_button.visible = False
            add_button.disabled = False # Habilita el botón de añadir
            selected_prof_id = None
            original_selected_rut = None # Limpiar el RUT guardado
            
        page.update()

    

    def handle_date_change(e):
        fecha_nacimiento_field.value = e.control.value.strftime('%Y-%m-%d')
        page.close(e.control)
        page.update()

    data_table = ft.DataTable(
        heading_row_color= color_PIE,
        columns=[
            ft.DataColumn(ft.Text("Nombres")), ft.DataColumn(ft.Text("Apellidos")),
            ft.DataColumn(ft.Text("Nacimiento")), ft.DataColumn(ft.Text("RUT")),
            ft.DataColumn(ft.Text("Cargo")), ft.DataColumn(ft.Text("Curso")),
            ft.DataColumn(ft.Text("Estado")),
        ],
        heading_text_style=ft.TextStyle(color="white", weight=ft.FontWeight.BOLD),
        data_text_style=ft.TextStyle(color="black"),
        border=ft.border.all(1, ft.Colors.BLACK),
        vertical_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
        horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
        data_row_color={
            ft.ControlState.HOVERED: ft.Colors.with_opacity(0.6, color_PIE),
            ft.ControlState.DEFAULT: ft.Colors.WHITE70,
            ft.ControlState.SELECTED: ft.Colors.with_opacity(0.5, color_PIE),
            
        },
    )

    nombre1 = ft.TextField(label="Primer nombre", label_style=ft.TextStyle(color="black"), color="black")
    nombre2 = ft.TextField(label="Segundo nombre", label_style=ft.TextStyle(color="black"), color="black")
    nombre3 = ft.TextField(label="Tercer nombre", label_style=ft.TextStyle(color="black"), color="black")
    apellido_pat = ft.TextField(label="Apellido paterno", label_style=ft.TextStyle(color="black"), color="black")
    apellido_mat = ft.TextField(label="Apellido materno", label_style=ft.TextStyle(color="black"), color="black")
    rut_field = ft.TextField(label="RUT", width=300, label_style=ft.TextStyle(color="black"), color="black")
    fecha_nacimiento_field = ft.TextField(
        label="Fecha de nacimiento",
        label_style=ft.TextStyle(color="black"),
        color="black",
        read_only=True,
        on_click=lambda _: page.open(ft.DatePicker(on_change=handle_date_change))
    )

    cursos_disponibles = ["4° Básico A", "4° Básico B", "4° Básico C", "4° Básico D"]
    cargo_field = ft.Dropdown(
        label="Cargo",
        width=300,
        options=[ft.dropdown.Option("Profesional PIE"), ft.dropdown.Option("Profesor Docente")],
        label_style=ft.TextStyle(color="black"), color="black",
    )
    curso_field = ft.Dropdown(
        label="Curso",
        width=300,
        options=[ft.dropdown.Option(curso) for curso in cursos_disponibles],
        label_style=ft.TextStyle(color="black"),
        color="black",
    )
    estado_field = ft.Dropdown(
        label="Estado",
        width=300,
        options=[ft.dropdown.Option("Habilitado"), ft.dropdown.Option("Inhabilitado")],
        label_style=ft.TextStyle(color="black"), color="black",
    )

    add_button = ft.IconButton(icon=ft.Icons.ADD, icon_color=ft.Colors.WHITE, bgcolor=color_PIE, tooltip="Añadir nuevo", on_click=lambda e:page.open(add_dialog))
    edit_button = ft.IconButton(icon=ft.Icons.EDIT, icon_color=ft.Colors.WHITE, bgcolor="#007bff", visible=False, tooltip="Editar", on_click=lambda e:page.open(edit_dialog))
    delete_button = ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.WHITE, bgcolor="#dc3545", visible=False, tooltip="Eliminar", on_click=lambda e:page.open(delete_dialog))
    def open_dialog(e, dialog):
        page.dialog = dialog
        dialog.open = True
        page.update()

    add_button = ft.IconButton(
        icon=ft.Icons.ADD, icon_color=ft.Colors.WHITE, bgcolor=color_PIE, 
        tooltip="Añadir nuevo", on_click=lambda e: open_dialog(e, add_dialog)
    )
    edit_button = ft.IconButton(
        icon=ft.Icons.EDIT, icon_color=ft.Colors.WHITE, bgcolor="#007bff", visible=False, 
        tooltip="Editar", on_click=lambda e: open_dialog(e, edit_dialog)
    )
    delete_button = ft.IconButton(
        icon=ft.Icons.DELETE, icon_color=ft.Colors.WHITE, bgcolor="#dc3545", visible=False, 
        tooltip="Eliminar", on_click=lambda e: open_dialog(e, delete_dialog)
    )

    head_mod_1= ft.Text("Lista de Docentes",size=20, weight=ft.FontWeight.BOLD, color="black")
    head_mod_2= ft.Text("Añadir / Editar Docente",size=20, weight=ft.FontWeight.BOLD, color="black")
    
    def load_profesores_to_table(id_to_select=None):
        data_table.rows.clear()
        profesores = profesorREAD()
        if profesores:
            for prof in profesores:
                data_table.rows.append(
                    ft.DataRow(
                        cells=[
                        ft.DataCell(ft.Text(f"{prof[1]} {prof[2] or ''} {prof[3] or ''}".strip())),
                        ft.DataCell(ft.Text(f"{prof[4]} {prof[5]}")),
                        ft.DataCell(ft.Text(str(prof[6]))),
                        ft.DataCell(ft.Text(prof[7])),
                        ft.DataCell(ft.Text("Profesional PIE" if prof[8] else "Profesor Docente")),
                        ft.DataCell(ft.Text(prof[10])),
                        ft.DataCell(ft.Text("Habilitado" if prof[11] else "Inhabilitado")),
                    ],
                        data=prof,
                        # Si el ID de esta fila coincide con el que queremos seleccionar, la marcamos.
                        selected=True if id_to_select is not None and prof[0] == id_to_select else False,
                        on_select_changed=on_row_select,
                    )
                )
        page.update()

    load_profesores_to_table()

    

    return ft.View(
        route="/modificación_docente",
        bgcolor="#d1d1d1",
        controls=[
            feedback_snackbar, # Añade el SnackBar a la vista para que pueda ser mostrado
            create_app_bar(page, "Modificación Docente"),
            ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.START,
                expand=True,
                controls=[
                    ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        spacing=20,
                        controls=[
                            ft.Container(
                                content=ft.Column([
                                    ft.Row([head_mod_1]),
                                    ft.Row([data_table]),
                                    
                                ], horizontal_alignment=ft.CrossAxisAlignment.START),
                                
                                padding=10,
                                border=ft.border.all(1, ft.Colors.BLACK26),
                                border_radius=8 
                            ),
        
                            ft.Container(
                                content=ft.Column([
                                    ft.Row([head_mod_2]),
                                    ft.Row([
                                        nombre1,
                                        nombre2,
                                        nombre3,
                                    ], alignment=ft.MainAxisAlignment.CENTER),
                                    ft.Row([
                                        apellido_pat,
                                        apellido_mat,
                                        fecha_nacimiento_field,
                                    ], alignment=ft.MainAxisAlignment.CENTER),
                                    ft.Row([
                                        rut_field,
                                        cargo_field,
                                        curso_field,
                                    ], alignment=ft.MainAxisAlignment.CENTER),
                                    ft.Row([
                                        estado_field,
                                    ], alignment=ft.MainAxisAlignment.CENTER),
                                    ft.Row([add_button, edit_button, delete_button], alignment=ft.MainAxisAlignment.START),
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                width=950,
                                padding=10,
                                border=ft.border.all(1, ft.Colors.BLACK26),
                                border_radius=8
                            )
                        ]
                    )
                ]
            )
        ]
    )
    
def create_perfil_view(page: ft.Page, profesor_data):
    if not profesor_data:
        return ft.View(
            route="/perfil_docente",
            bgcolor="#d1d1d1",
            controls=[
                create_app_bar(page, "Perfil Docente"),
                ft.Text("No se pudo cargar la información del perfil.", color="red")
            ]
        )

    doc_info = list(profesor_data)
    info_table = ft.DataTable(
        heading_row_color= color_PIE,
        data_row_color="white",
        columns=[
            ft.DataColumn(ft.Text("Nombres")),
            ft.DataColumn(ft.Text("Apellidos")),
            ft.DataColumn(ft.Text("Nacimiento"), numeric=True),
            ft.DataColumn(ft.Text("RUT")),
            ft.DataColumn(ft.Text("Cargo")),
            ft.DataColumn(ft.Text("Curso")),
            ft.DataColumn(ft.Text("Estado")),
        ],
        rows=[
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(f"{doc_info[1]} {doc_info[2] or ''} {doc_info[3] or ''}".strip())),
                ft.DataCell(ft.Text(f"{doc_info[4]} {doc_info[5]}")),
                ft.DataCell(ft.Text(f"{doc_info[6]}")),
                ft.DataCell(ft.Text(f"{doc_info[7]}")),
                ft.DataCell(ft.Text("Profesional PIE" if doc_info[8] else "Profesor Docente")),
                ft.DataCell(ft.Text(f"{doc_info[10]}")),
                ft.DataCell(ft.Text(f"Habilitado" if doc_info[11] else "Inhabilitado")),
            ]),
        ],
        data_text_style=ft.TextStyle(color="black"),
        heading_text_style=ft.TextStyle(color="white", weight=ft.FontWeight.BOLD),
        border=ft.border.all(1, ft.Colors.BLACK),
        vertical_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
        horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
    )

    return ft.View(
        route="/perfil_docente",
        bgcolor="#d1d1d1",
        controls=[
            create_app_bar(page, "Perfil Docente"),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.START,
                expand=True,
                controls=[
                    ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        spacing=20,
                        controls=[
                            ft.Container(
                        content=
                        ft.Column([
                            ft.Row([ft.Text("Datos de Docente",size=20, weight=ft.FontWeight.BOLD, color="black")]),
                            ft.Row([info_table], alignment=ft.MainAxisAlignment.CENTER)],
                            scroll=ft.ScrollMode.AUTO,
                        ),
                        border=ft.border.all(1, ft.Colors.BLACK26),
                        border_radius=8,
                        padding=10,
                    ),
                    ft.Container(
                        content=
                        ft.Column([
                            ft.Row([ft.Text("Lista de alumnos testeados",size=20, weight=ft.FontWeight.BOLD, color="black")]),
                            ft.Row([info_table], alignment=ft.MainAxisAlignment.CENTER)],
                            scroll=ft.ScrollMode.AUTO,
                        ),
                        border=ft.border.all(1, ft.Colors.BLACK26),
                        border_radius=8,
                        padding=10,
                    ),
                        ]
                    ),                    
                ]
            )
        ]
    )

def menu_principalPIE(page: ft.Page, pro_nameID: int):
    page.clean()
    page.title = "Neuro Check - Profesor"
    page.bgcolor = "#d1d1d1"
    profesor_data = profesorREAD(pro_nameID)
    

    def route_change(e: ft.RouteChangeEvent):
        print(f"Cambiando a la ruta: {e.route}")
        page.views.clear()
        page.views.append(create_inicio_view(page, profesor_data))
        if page.route == "/perfil_docente":
            page.views.append(create_perfil_view(page, profesor_data))
        elif page.route == "/modificación_docente":
            page.views.append(modificación_docente(page, profesor_data))
        
        page.update()

    def view_pop(e: ft.ViewPopEvent):
        print(f"Cerrando vista: {e.view}")
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go("/inicio_profesor")


if __name__ == "__main__":
    def main_standalone(page: ft.Page):
        id_profesor_pie_test = 13
        menu_principalPIE(page, id_profesor_pie_test)

    ft.app(target=main_standalone, assets_dir="assets",view=ft.AppView.WEB_BROWSER)
