import flet as ft
import pyodbc
from flet import *
from DB import CONNECTION_STRING

welcome = Text("¡Bienvenido!", size=50, weight=FontWeight.BOLD, color="black")

def mostrar_menu_principal(page: Page):
    page.clean()
    page.title = "Neuro Check"
    page.route = "/inicio"
    page.bgcolor = "#d1d1d1"

    def open_inicio(e):
        page.go("/inicio")

    def open_perfil_docente(e):
        page.go("/perfil_docente")

    def route_change(e):
        nombre_ruta = "Inicio"
        if page.route == "/inicio":
            nombre_ruta = "Inicio"
        elif page.route == "/perfil_docente":
            nombre_ruta = "Perfil docente"

        sql_name = "SELECT pro_nombre_1 FROM Profesores WHERE pro_rut = '27.543.891-K' AND pro_password = '1234'"
        sql_info = "SELECT * FROM Profesores WHERE pro_rut = '27.543.891-K' AND pro_password = '1234'"
        barra = AppBar(
            title=TextButton(
                content=Text("Neuro Check", size=25, weight=FontWeight.BOLD, color="white"),
                on_click=open_inicio
            ),
            bgcolor="#0A00CF",
            center_title=False,
            actions=[
                Row([
                    Text(nombre_ruta),
                    PopupMenuButton(items=[
                        PopupMenuItem(
                            icon=Icons.EXIT_TO_APP,
                            text="Cerrar sesión",
                        ),
                    ])
                ]),
            ]
        )
        print("Route change:", e.route)
        page.views.clear()
        try:
            cnxn = pyodbc.connect(CONNECTION_STRING)
            cursor = cnxn.cursor()
            cursor.execute(sql_name)
            doc_name_tuple = cursor.fetchone()
            doc_name = doc_name_tuple[0]
            print(doc_name)
            page.views.append(
                View(
                    "/inicio",
                    bgcolor="#d1d1d1",
                    controls=[
                        barra,
                        Column(
                            controls=[
                                Text("¡Bienvenido!", size=50, weight=FontWeight.BOLD, color="black"),
                                Text(f"Teacher {doc_name}", size=20, weight=FontWeight.BOLD, color="black"),
                                Row(
                                    [Text("¿Que desea hacer?", size=25, weight=FontWeight.BOLD, color="black")],
                                    alignment=MainAxisAlignment.START
                                ),
                                Card(
                                    elevation=0,
                                    color="#0A00CF",
                                    content=Container(
                                        content=Column([
                                            ListTile(
                                                title=Text("Realizar test", size=20, weight=FontWeight.BOLD),
                                                subtitle=Text(
                                                    "El test sirve para obtener el porcentaje de riesgo del estudiante para posiblemente derviarlo al equipo PIE.",
                                                    size=15
                                                ),
                                                bgcolor="#0A00CF",
                                            ),
                                            ElevatedButton(text="Entrar", color="black", bgcolor="#8E78FC")
                                        ]),
                                        width=450,
                                        padding=10,
                                    )
                                ),
                                Card(
                                    color="#0A00CF",
                                    content=Container(
                                        content=Column([
                                            ListTile(
                                                title=Text("Perfil docente", size=20, weight=FontWeight.BOLD),
                                                subtitle=Text(
                                                    "Puedes ver tú información personal y revisar los resultados de los tests.",
                                                    size=15
                                                ),
                                                bgcolor="#0A00CF"
                                            ),
                                            ElevatedButton(
                                                text="Entrar",
                                                color="black",
                                                bgcolor="#8E78FC",
                                                on_click=open_perfil_docente
                                            )
                                        ]),
                                        width=450,
                                        padding=10
                                    )
                                ),
                            ],
                            horizontal_alignment=CrossAxisAlignment.CENTER
                        )
                    ]
                )
            )
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Error de conexión: {sqlstate}")
        finally:
            try:
                cnxn.close()
            except:
                pass
            if page.route == "/perfil_docente":
                try:
                    cnxn = pyodbc.connect(CONNECTION_STRING)
                    cursor = cnxn.cursor()
                    cursor.execute(sql_info)
                    doc_info_tuple = cursor.fetchone()
                    doc_info = list(doc_info_tuple)
                    print(doc_info)
                    page.views.append(
                        View(
                            "/perfil_docente",
                            bgcolor="#d1d1d1",
                            controls=[
                                barra,
                                Column(
                                    controls=[
                                        Row(
                                            controls=[
                                                DataTable(
                                                    columns=[
                                                        ft.DataColumn(ft.Text("Nombres", text_align=ft.TextAlign.CENTER)),
                                                        ft.DataColumn(ft.Text("Apellidos", text_align=ft.TextAlign.CENTER)),
                                                        ft.DataColumn(ft.Text("Año de nacimiento", text_align=ft.TextAlign.CENTER), numeric=True),
                                                        ft.DataColumn(ft.Text("RUT", text_align=ft.TextAlign.CENTER)),
                                                        ft.DataColumn(ft.Text("Cargo", text_align=ft.TextAlign.CENTER)),
                                                        ft.DataColumn(ft.Text("Curso designado", text_align=ft.TextAlign.CENTER)),
                                                    ],
                                                    rows=[
                                                        ft.DataRow(cells=[
                                                            ft.DataCell(ft.Text(f"{doc_info[1]} {doc_info[2]} {doc_info[3]}", text_align=ft.TextAlign.CENTER)),
                                                            ft.DataCell(ft.Text(f"{doc_info[4]} {doc_info[5]}", text_align=ft.TextAlign.CENTER)),
                                                            ft.DataCell(ft.Text(f"{doc_info[6]}", text_align=ft.TextAlign.CENTER)),
                                                            ft.DataCell(ft.Text(f"{doc_info[7]}", text_align=ft.TextAlign.CENTER)),
                                                            ft.DataCell(ft.Text("Profesor Docente" if doc_info[8] == False else "Profesional PIE", text_align=ft.TextAlign.CENTER)),
                                                            ft.DataCell(ft.Text(f"{doc_info[10]}", text_align=ft.TextAlign.CENTER)),
                                                        ]),
                                                    ],
                                                    data_text_style=TextStyle(color="black"),
                                                    heading_text_style=ft.TextStyle(color="black"),
                                                    border=ft.Border(
                                                        left=ft.BorderSide(1, ft.Colors.BLACK),
                                                        top=ft.BorderSide(1, ft.Colors.BLACK),
                                                        right=ft.BorderSide(1, ft.Colors.BLACK),
                                                        bottom=ft.BorderSide(1, ft.Colors.BLACK)
                                                    )
                                                )
                                            ],
                                            alignment=MainAxisAlignment.CENTER
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                except pyodbc.Error as ex:
                    sqlstate = ex.args[0]
                    print(f"Error de conexión: {sqlstate}")
                finally:
                    try:
                        cnxn.close()
                    except:
                        pass
        
        page.update()

    def view_pop(e):
        print("View pop:", e.view)
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go(page.route)
