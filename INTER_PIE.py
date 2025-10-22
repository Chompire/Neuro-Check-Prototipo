import flet as ft
import pyodbc
from DB import CONNECTION_STRING
from CRUD import profesorCREATE,profesorREAD, profesorUPDATE,profesorDELETE, cursoREAD_all
import datetime


color_PIE = "#FF0000"
color_Background = "#FFFFFF"
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

def create_footer():
    """Crea un control de pie de página reutilizable."""
    return ft.Container(
        content=ft.Text(
            "© 2024 Neuro Check. Todos los derechos reservados.",
            size=12,
            color=ft.Colors.BLACK54,
            text_align=ft.TextAlign.CENTER,
        ),
        alignment=ft.alignment.center,
        padding=10,
    )

def create_inicio_view(page: ft.Page, profesor_data):
    doc_name = profesor_data[1] if profesor_data else "Desconocido"
    return ft.View(
        route="/inicio_profesor",
        bgcolor=color_Background,
        controls=[
            create_app_bar(page, "Inicio"),
            ft.Column(
                expand=True, # Permite que la columna ocupe todo el espacio vertical
                controls=[
                    ft.Container(
                        expand=True, # El contenido principal se expande
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
                    ),
                    create_footer() # El pie de página se coloca al final
                ]
            ),
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
    def open_dialog(e, dialog):
        page.dialog = dialog
        dialog.open = True
        page.update()

    # --- Funciones de confirmación para los diálogos ---
    def confirm_add(e):
        add_profesor_logic(e)
        page.close(add_dialog)
    
    def confirm_update(e):
        update_profesor_logic()
        page.close(edit_dialog)
    

    def confirm_delete(e, dialog):
        delete_profesor_logic()
        page.close(delete_dialog)



    def close_dialog(e, dialog):
        dialog.open = False
        page.update()
        

    # --- Diálogos de Alerta ---
    add_dialog = ft.AlertDialog(
        modal=True, title=ft.Text("Confirmar Creación"),
        content=ft.Text("¿Desea agregar este nuevo profesor?"),
    )
    add_dialog.actions=[ft.TextButton("Sí, agregar", on_click= confirm_add ), ft.TextButton("Cancelar", on_click=lambda e: page.close(add_dialog))]
    edit_dialog = ft.AlertDialog(
        modal=True, title=ft.Text("Confirmar Actualización"),
        content=ft.Text("¿Desea guardar los cambios realizados?"),
    )
    edit_dialog.actions=[ft.TextButton("Sí, guardar", on_click=confirm_update), ft.TextButton("Cancelar", on_click=lambda e: page.close(edit_dialog))]
    delete_dialog = ft.AlertDialog(
        modal=True, title=ft.Text("Confirmar Eliminación"),
        content=ft.Text("¿Está seguro de que desea eliminar a este profesor? Esta acción no se puede deshacer."),
    )
    delete_dialog.actions=[ft.TextButton("Sí, eliminar", on_click=lambda e: confirm_delete(delete_dialog), style=ft.ButtonStyle(color=ft.Colors.RED)), ft.TextButton("Cancelar", on_click=lambda e: page.close(delete_dialog))]

    # --- Lógica de las operaciones (separada de los eventos de click) ---
    def add_profesor_logic(e):
        rut_a_verificar = rut_field.value.strip()
        email_a_verificar = mail_field.value.strip()

        # 1. Validar que el RUT no esté vacío
        if not rut_a_verificar:
            feedback_snackbar.content = ft.Text("Error: El campo RUT es obligatorio.")
            feedback_snackbar.bgcolor = ft.Colors.RED_700
            feedback_snackbar.open = True
            page.update()
            return

        # 3. Validar que los campos obligatorios (incluyendo Dropdowns) no estén vacíos
        # Incluimos todos los campos que probablemente son NOT NULL en la base de datos.
        # Si pro_nombre_2 o pro_nombre_3 son NOT NULL, también deberían agregarse aquí.
        # Asumimos que pro_password es manejado internamente y no puede ser vacío.

        campos_obligatorios = {
            "Primer nombre": nombre1.value,
            "Apellido paterno": apellido_pat.value,
            "Email": email_a_verificar,
            "Cargo": cargo_field.value,
            "Estado": estado_field.value,
            "Apellido materno": apellido_mat.value,
            "Curso": curso_field.value, # Añadido
        } 

        for nombre_campo, valor_campo in campos_obligatorios.items():
            # Un campo se considera vacío si no tiene valor (es None o una cadena vacía después de quitar espacios)
            if not valor_campo:
                feedback_snackbar.content = ft.Text(f"Error: El campo '{nombre_campo}' es obligatorio.")
                feedback_snackbar.bgcolor = ft.Colors.RED_700
                feedback_snackbar.open = True
                page.update()
                return

        # 2. Validar que el RUT no exista ya en la base de datos
        if profesorREAD(pro_rut=rut_a_verificar):
            feedback_snackbar.content = ft.Text(f"Error: El RUT '{rut_a_verificar}' ya está registrado.")
            feedback_snackbar.bgcolor = ft.Colors.RED_700
            feedback_snackbar.open = True
            page.update()
            return

        # 4. Si todas las validaciones pasan, proceder con la creación
        cargo_valor = 1 if cargo_field.value == "Profesional PIE" else 0
        estado_valor = 1 if estado_field.value == "Habilitado" else 0
        
        datos_nuevos = (
            nombre1.value, nombre2.value, nombre3.value,
            apellido_pat.value, apellido_mat.value,
            rut_a_verificar, email_a_verificar,
            cargo_valor, password_define, 
            curso_field.value, estado_valor,
        )

        if profesorCREATE(datos_profesor=datos_nuevos):
            feedback_snackbar.content = ft.Text("Profesor agregado con éxito")
            feedback_snackbar.bgcolor = ft.Colors.GREEN_700
            load_profesores_to_table()
            clear_form_fields()
            reset_selection_state()
        else:
            feedback_snackbar.content = ft.Text("Error al agregar profesor. Revisa los campos.")
            feedback_snackbar.bgcolor = ft.Colors.RED_700

        feedback_snackbar.open = True
        page.update()

    def update_profesor_logic():
        nonlocal selected_prof_id, original_selected_rut
        nuevo_rut = rut_field.value.strip()
        nuevo_email = mail_field.value.strip()

        # Validar campos obligatorios antes de la actualización
        campos_obligatorios = {
            "Primer nombre": nombre1.value, "Apellido paterno": apellido_pat.value,
            "Apellido materno": apellido_mat.value,
            "RUT": nuevo_rut, "Email": nuevo_email,
            "Cargo": cargo_field.value, "Estado": estado_field.value,
            "Curso": curso_field.value,
        }
        # ... (el resto de la validación de campos obligatorios es igual)
        # ... (el resto de la validación de campos obligatorios es igual)

        # 1. Verificar si el RUT ya existe para OTRO profesor
        profesor_con_mismo_rut = profesorREAD(pro_rut=nuevo_rut)
        if profesor_con_mismo_rut and profesor_con_mismo_rut[0] != selected_prof_id:
            feedback_snackbar.content = ft.Text(f"Error: El RUT '{nuevo_rut}' ya está registrado para otro usuario.")
            feedback_snackbar.bgcolor = ft.Colors.RED_700
            feedback_snackbar.open = True
            page.update()
            return

        # 2. Si no hay duplicados, proceder con la actualización
        if selected_prof_id is not None:
            estado_valor = 1 if estado_field.value == "Habilitado" else 0
            cargo_valor = 1 if cargo_field.value == "Profesional PIE" else 0
            datos_actualizados = {
                "pro_nombre_1": nombre1.value, "pro_nombre_2": nombre2.value, "pro_nombre_3": nombre3.value,
                "pro_apellido_pat": apellido_pat.value, "pro_apellido_mat": apellido_mat.value,
                "pro_rut": nuevo_rut,
                "pro_email": nuevo_email, "pro_cargo": cargo_valor,
                "lvl_curso": curso_field.value, "pro_state": estado_valor,
            }
            profesorUPDATE(selected_prof_id, datos_actualizados)
            feedback_snackbar.content = ft.Text("Profesor actualizado con éxito")
            feedback_snackbar.bgcolor = ft.Colors.GREEN_700
            feedback_snackbar.open = True
            load_profesores_to_table(id_to_select=selected_prof_id)

    def delete_profesor_logic():
        nonlocal selected_prof_id
        if selected_prof_id:
            profesorDELETE(selected_prof_id)
            feedback_snackbar.content = ft.Text("Profesor eliminado con éxito.")
            feedback_snackbar.bgcolor = ft.Colors.GREEN_700
            feedback_snackbar.open = True
            load_profesores_to_table()
            clear_form_fields()
            reset_selection_state()

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
            original_selected_rut = selected_prof[6] 
            nombre1.value = selected_prof[1] or ""
            nombre2.value = selected_prof[2] or ""
            nombre3.value = selected_prof[3] or ""
            apellido_pat.value = selected_prof[4] or ""
            apellido_mat.value = selected_prof[5] or ""
            rut_field.value = selected_prof[7] or "" # Este es pro_rut
            mail_field.value = selected_prof[8]
            cargo_field.value = "Profesional PIE" if selected_prof[9] else "Profesor Docente"
            curso_field.value = selected_prof[11] # Asignamos el ID del curso al Dropdown
            estado_field.value = "Habilitado" if selected_prof[12] else "Inhabilitado"
                
        else:
            clear_form_fields()
            reset_selection_state()

        # Para depuración: Imprime los valores actuales de los campos del formulario
        print(f"Valores en formulario: RUT='{rut_field.value}', Email='{mail_field.value}'")

            
        page.update()

    def clear_form_fields():
        nombre1.value = ""
        nombre2.value = ""
        nombre3.value = ""
        apellido_pat.value = ""
        apellido_mat.value = ""
        rut_field.value = ""
        mail_field.value = ""
        cargo_field.value = None
        curso_field.value = None
        estado_field.value = None

    def reset_selection_state():
        nonlocal selected_prof_id, original_selected_rut
        for row in data_table.rows:
            row.selected = False
        
        if selected_prof_id is not None:
            edit_button.visible = False
            delete_button.visible = False
            add_button.disabled = False # Habilita el botón de añadir
            selected_prof_id = None
            original_selected_rut = None # Limpiar el RUT guardado


    data_table = ft.DataTable(
        heading_row_color= color_PIE,
        columns=[
            ft.DataColumn(ft.Text("Nombres")), ft.DataColumn(ft.Text("Apellidos")),
            ft.DataColumn(ft.Text("RUT")),
            ft.DataColumn(ft.Text("Email")),
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
    mail_field = ft.TextField(label="Email", label_style=ft.TextStyle(color="black"), color="black")
    cargo_field = ft.Dropdown(
        label="Cargo",
        width=300,
        options=[ft.dropdown.Option("Profesional PIE"), ft.dropdown.Option("Profesor Docente")],
        label_style=ft.TextStyle(color="black"), color="black",
    )
    # Obtenemos los cursos desde la base de datos
    cursos_from_db = cursoREAD_all()
    curso_field = ft.Dropdown(
        label="Curso",
        width=300,
        # Creamos las opciones usando el ID como clave (key) y el nombre como texto visible
        options=[ft.dropdown.Option(key=curso[0], text=curso[1]) for curso in cursos_from_db],
        color="black",
    )
    estado_field = ft.Dropdown(
        label="Estado",
        width=300,
        options=[ft.dropdown.Option("Habilitado"), ft.dropdown.Option("Inhabilitado")],
        label_style=ft.TextStyle(color="black"), color="black",
    )    
    add_button = ft.IconButton(icon=ft.Icons.ADD, icon_color=ft.Colors.WHITE, bgcolor=color_PIE, tooltip="Añadir nuevo", on_click=lambda e: page.open(add_dialog))
    edit_button = ft.IconButton(icon=ft.Icons.EDIT, icon_color=ft.Colors.WHITE, bgcolor="#007bff", visible=False, tooltip="Editar", on_click=lambda e: page.open(edit_dialog))
    delete_button = ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.WHITE, bgcolor="#dc3545", visible=False, tooltip="Eliminar", on_click=lambda e: page.open(delete_dialog))
    
        
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
                        ft.DataCell(ft.Text("Profesional PIE" if prof[9] else "Profesor Docente")),
                        ft.DataCell(ft.Text(prof[12] or "")), # Usamos el índice 13 (nombre del curso)
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
        bgcolor=color_Background,
        controls=[
            feedback_snackbar,
            create_app_bar(page, "Modificación Docente"),
            ft.Column(
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.START,
                        expand=True,
                        controls=[
                            ft.Column(
                                spacing=20,
                                controls=[
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Row([head_mod_1]),
                                            ft.Row([data_table]),
                                            
                                        ],),
                                        
                                        padding=10,
                                        border=ft.border.all(2, ft.Colors.BLACK),
                                        border_radius=8 
                                    ),
                
                                    ft.Container(
                                        content=ft.Column([
                                            ft.Row([head_mod_2]),
                                            ft.Row([
                                                nombre1,
                                                nombre2,
                                                nombre3,
                                            ],),
                                            ft.Row([
                                                apellido_pat,
                                                apellido_mat,
                                                rut_field,
                                            ],),
                                            ft.Row([
                                                
                                                mail_field,
                                                cargo_field,
                                                curso_field,
                                                
                                            ],),
                                            ft.Row([                                                
                                                estado_field,
                                            ],  ),
                                            ft.Row([add_button, edit_button, delete_button],),
                                        ],),
                                        padding=10,
                                        border=ft.border.all(2, ft.Colors.BLACK),
                                        border_radius=8,
                                        bgcolor="white",                                                                                
                                    )
                                ]
                            )
                        ]
                    ),
                    create_footer()
                ]
            ),
        ]
    )
    
def create_perfil_view(page: ft.Page, profesor_data):
    if not profesor_data:
        return ft.View(
            route="/perfil_docente",
            bgcolor=color_Background,
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
            ft.DataColumn(ft.Text("Email")),
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
                ft.DataCell(ft.Text(f"{doc_info[8]}")),
                ft.DataCell(ft.Text("Profesional PIE" if doc_info[9] == 1 else "Profesor Docente")),
                ft.DataCell(ft.Text(f"{doc_info[13] or ''}")), # Usamos el índice 13 (nombre del curso)
                ft.DataCell(ft.Text(f"Habilitado" if doc_info[12] == 1 else "Inhabilitado")),
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
        bgcolor=color_Background,
        controls=[
            create_app_bar(page, "Perfil Docente"),
            ft.Column(
                expand=True,
                controls=[
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
                    ),
                    create_footer()
                ]
            ),
        ]
    )

def menu_principalPIE(page: ft.Page, pro_nameID: int):
    page.clean()
    page.title = "Neuro Check - Profesor"
    page.bgcolor = color_Background
    profesor_data = profesorREAD(pro_nameID)
    print(profesor_data)

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
        id_profesor_pie_test = 2
        menu_principalPIE(page, id_profesor_pie_test)

    ft.app(target=main_standalone, assets_dir="assets",view=ft.AppView.FLET_APP)
