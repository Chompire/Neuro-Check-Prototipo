import flet as ft
import pyodbc
from DB import CONNECTION_STRING
from CRUD import profesorCREATE,profesorREAD


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
            ft.Column(
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Text("¡Bienvenido!", size=50, weight=ft.FontWeight.BOLD, color="black"),
                    ft.Text(f"Profesor {doc_name}", size=20, weight=ft.FontWeight.BOLD, color="black"),
                    ft.Row(
                        [ft.Text("¿Qué desea hacer?", size=25, weight=ft.FontWeight.BOLD, color="black")],
                        alignment=ft.MainAxisAlignment.START
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

def modificación_docente(page: ft.Page, profesor_data):
    """Crea la vista para modificar, añadir o eliminar docentes."""
    
    # --- Controles ---
    # Botones de acción, editar y eliminar son invisibles al principio.
    add_button = ft.IconButton(icon=ft.Icons.ADD, icon_color=ft.Colors.WHITE, bgcolor=color_PIE, tooltip="Añadir nuevo")
    edit_button = ft.IconButton(icon=ft.Icons.EDIT, icon_color=ft.Colors.WHITE, bgcolor="#007bff", visible=False, tooltip="Editar")
    delete_button = ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.WHITE, bgcolor="#dc3545", visible=False, tooltip="Eliminar")

    # --- Funciones / Manejadores ---
    def on_row_select(e):
        """Maneja la selección de una fila para mantenerla resaltada y mostrar los botones de acción."""
        # 1. Deselecciona todas las filas para empezar con un estado limpio.
        for row in data_table.rows:
            row.selected = False

        # 2. Selecciona únicamente la fila que disparó el evento.
        e.control.selected = True

        # 3. Haz visibles los botones de acción.
        edit_button.visible = True
        delete_button.visible = True

        # 4. Actualiza la página para que los cambios sean visibles.
        page.update()

    # --- Creación de la Tabla ---
    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nombres")), ft.DataColumn(ft.Text("Apellidos")),
            ft.DataColumn(ft.Text("Nacimiento")), ft.DataColumn(ft.Text("RUT")),
            ft.DataColumn(ft.Text("Cargo")), ft.DataColumn(ft.Text("Curso")),
        ],
        rows=[], # Las filas se llenarán desde la base de datos
        heading_text_style=ft.TextStyle(color="black", weight=ft.FontWeight.BOLD),
        data_text_style=ft.TextStyle(color="black"),
        border=ft.border.all(1, ft.Colors.BLACK),
        vertical_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
        horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
        data_row_color={ft.ControlState.HOVERED: ft.Colors.with_opacity(0.3, color_PIE)},
    )

    # Llenar la tabla con datos de los profesores
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
                    ],
                    data=prof,  # Guarda todos los datos del profesor en la fila
                    on_select_changed=on_row_select,
                )
            )
    nombre1 = ft.TextField(label="Primer nombre",label_style=ft.TextStyle(color="black"),color="black")
    nombre2 = ft.TextField(label="Segundo nombre", label_style=ft.TextStyle(color="black"),color="black")
    nombre3 = ft.TextField(label="Tercer nombre", label_style=ft.TextStyle(color="black"),color="black")
    apellido_pat = ft.TextField(label="Apellido paterno", label_style=ft.TextStyle(color="black"),color="black")
    apellido_mat = ft.TextField(label="Apellido materno", label_style=ft.TextStyle(color="black"),color="black")
    
    # Definir la lista de cursos antes de usarla
    cursos_disponibles = ["4° Básico A", "4° Básico B", "4° Básico C", "4° Básico D"]
    # --- Controles y lógica para el DatePicker ---
    fecha_nacimiento_field = ft.TextField(
        label="Fecha de nacimiento",
        label_style=ft.TextStyle(color="black"),
        color="black",
        read_only=True,
        on_click=lambda _: page.open(ft.DatePicker(on_change=handle_change))
    )
    rut_field = ft.TextField(label="RUT", width=300,label_style=ft.TextStyle(color="black"),color="black")
    cargo_field =  ft.Dropdown(
        label="Cargo",
        width=300,
        options=[ft.dropdown.Option("Profesional PIE"), ft.dropdown.Option("Profesor Docente")],
        label_style=ft.TextStyle(color="black"),color="black",
    )
    curso_field = ft.Dropdown(
        label="Curso",
        width=300,
        options=[ft.dropdown.Option(curso) for curso in cursos_disponibles],
        label_style=ft.TextStyle(color="black"),
        color="black",
    )
    

    def handle_change(e):
        """Actualiza el campo de texto con la fecha seleccionada y cierra el selector."""
        fecha_nacimiento_field.value = e.control.value.strftime('%Y-%m-%d')
        page.close(e.control) # Cierra el DatePicker
        page.update()

    def add_pofesor(e):
        plus_prof= [nombre1.value,nombre2.value,nombre3.value, apellido_pat.value , apellido_mat.value, fecha_nacimiento_field.value]
        pass


    return ft.View(
        route="/modificación_docente",
        bgcolor="#d1d1d1",
        controls=[
            create_app_bar(page, "Modificación Docente"),
            ft.Column(
                scroll=ft.ScrollMode.AUTO,
                expand=True,            
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    # Contenedor para la sección de la tabla
                    ft.Column([
                        ft.Text("Lista de Docentes", size=20, weight=ft.FontWeight.BOLD, color="black"),
                        data_table,
                    ], horizontal_alignment=ft.CrossAxisAlignment.START),

                    ft.Divider(height=20, color="transparent"),

                    # Contenedor para la sección del formulario
                    ft.Column(
                        [
                            ft.Text("Añadir / Editar Docente", size=20, weight=ft.FontWeight.BOLD, color="black"),
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
                            ft.Row([add_button, edit_button, delete_button], alignment=ft.MainAxisAlignment.CENTER),
                        ],
                        width=950, # Ancho aproximado de 3 campos + espaciado
                        horizontal_alignment=ft.CrossAxisAlignment.START
                    ),
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
        columns=[
            ft.DataColumn(ft.Text("Nombres")),
            ft.DataColumn(ft.Text("Apellidos")),
            ft.DataColumn(ft.Text("Nacimiento"), numeric=True),
            ft.DataColumn(ft.Text("RUT")),
            ft.DataColumn(ft.Text("Cargo")),
            ft.DataColumn(ft.Text("Curso")),
        ],
        rows=[
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(f"{doc_info[1]} {doc_info[2] or ''} {doc_info[3] or ''}".strip())),
                ft.DataCell(ft.Text(f"{doc_info[4]} {doc_info[5]}")),
                ft.DataCell(ft.Text(f"{doc_info[6]}")),
                ft.DataCell(ft.Text(f"{doc_info[7]}")),
                ft.DataCell(ft.Text("Profesional PIE" if doc_info[8] else "Profesor Docente")),
                ft.DataCell(ft.Text(f"{doc_info[10]}")),
            ]),
        ],
        data_text_style=ft.TextStyle(color="black"),
        heading_text_style=ft.TextStyle(color="black", weight=ft.FontWeight.BOLD),
        border=ft.border.all(1, ft.Colors.BLACK),
        vertical_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
        horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
    )

    return ft.View(
        route="/perfil_docente",
        bgcolor="#d1d1d1",
        controls=[
            create_app_bar(page, "Perfil Docente"),
            ft.Column(
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                controls=[
                    ft.Container(content=info_table, padding=20, alignment=ft.alignment.center)
                ]
            )
        ]
    )

def menu_principalPIE(page: ft.Page, pro_nameID: int):
    page.clean()
    page.title = "Neuro Check - Profesor"
    page.bgcolor = "#d1d1d1"
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
