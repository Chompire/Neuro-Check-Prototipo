import flet as ft
import pyodbc
from DB import CONNECTION_STRING

def get_profesor_data(pro_nameID: int):
    try:
        with pyodbc.connect(CONNECTION_STRING) as cnxn:
            with cnxn.cursor() as cursor:
                sql_info = "SELECT * FROM Profesores WHERE pro_nameID = ?"
                cursor.execute(sql_info, pro_nameID)
                return cursor.fetchone()
    except pyodbc.Error as ex:
        print(f"Error de conexión o consulta: {ex.args[0]}")
        return None

def create_app_bar(page: ft.Page, title: str):
    return ft.AppBar(
        title=ft.TextButton(
            content=ft.Text("Neuro Check", size=25, weight=ft.FontWeight.BOLD, color="white"),
            on_click=lambda _: page.go("/inicio_profesor")
        ),
        bgcolor="#0A00CF",
        center_title=False,
        actions=[
            ft.Row([
                ft.Text(title, color="white"),
                ft.PopupMenuButton(items=[
                    ft.PopupMenuItem(
                        icon=ft.icons.EXIT_TO_APP,
                        text="Cerrar sesión",
                        # Aquí deberías agregar la lógica para cerrar sesión, ej: page.go("/")
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
                controls=[
                    ft.Text("¡Bienvenido!", size=50, weight=ft.FontWeight.BOLD, color="black"),
                    ft.Text(f"Profesor {doc_name}", size=20, weight=ft.FontWeight.BOLD, color="black"),
                    ft.Row(
                        [ft.Text("¿Qué desea hacer?", size=25, weight=ft.FontWeight.BOLD, color="black")],
                        alignment=ft.MainAxisAlignment.START
                    ),
                    ft.Card(
                        elevation=0,
                        color="#0A00CF",
                        content=ft.Container(
                            content=ft.Column([
                                ft.ListTile(
                                    title=ft.Text("Realizar test", size=20, weight=ft.FontWeight.BOLD),
                                    subtitle=ft.Text(
                                        "El test sirve para obtener el porcentaje de riesgo del estudiante para posiblemente derivarlo al equipo PIE.",
                                        size=15
                                    ),
                                ),
                                ft.ElevatedButton(text="Entrar", color="black", bgcolor="#8E78FC")
                            ]),
                            width=450,
                            padding=10,
                        )
                    ),
                    ft.Card(
                        color="#0A00CF",
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
                                    bgcolor="#8E78FC",
                                    on_click=lambda _: page.go("/perfil_docente")
                                )
                            ]),
                            width=450,
                            padding=10
                        )
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
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
        border=ft.border.all(1, ft.colors.BLACK),
        vertical_lines=ft.border.BorderSide(1, ft.colors.BLACK),
        horizontal_lines=ft.border.BorderSide(1, ft.colors.BLACK),
    )

    return ft.View(
        route="/perfil_docente",
        bgcolor="#d1d1d1",
        controls=[
            create_app_bar(page, "Perfil Docente"),
            ft.Container(content=info_table, padding=20, alignment=ft.alignment.center)
        ]
    )

def mostrar_menu_principal(page: ft.Page, pro_nameID: int):
    page.clean()
    page.title = "Neuro Check - Profesor"
    page.bgcolor = "#d1d1d1"
    profesor_data = get_profesor_data(pro_nameID)

    def route_change(e: ft.RouteChangeEvent):
        print(f"Cambiando a la ruta: {e.route}")
        page.views.clear()
        page.views.append(create_inicio_view(page, profesor_data))
        if page.route == "/perfil_docente":
            page.views.append(create_perfil_view(page, profesor_data))
        
        page.update()

    def view_pop(e: ft.ViewPopEvent):
        print(f"Cerrando vista: {e.view}")
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # Iniciar en la ruta principal del profesor
    page.go("/inicio_profesor")
