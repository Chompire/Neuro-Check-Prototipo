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

        sql_name = "SELECT pro_nombre_1 FROM Profesores WHERE pro_rut = '19493468-8' AND pro_password = '1234'"
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
            if page.route == "/perfil_docente":
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
                                                    ft.DataColumn(ft.Text("First name")),
                                                    ft.DataColumn(ft.Text("Last name")),
                                                    ft.DataColumn(ft.Text("Age"), numeric=True),
                                                ],
                                                rows=[
                                                    ft.DataRow(cells=[
                                                        ft.DataCell(ft.Text("John")),
                                                        ft.DataCell(ft.Text("Smith")),
                                                        ft.DataCell(ft.Text("43")),
                                                    ]),
                                                    ft.DataRow(cells=[
                                                        ft.DataCell(ft.Text("Jack")),
                                                        ft.DataCell(ft.Text("Brown")),
                                                        ft.DataCell(ft.Text("19")),
                                                    ]),
                                                    ft.DataRow(cells=[
                                                        ft.DataCell(ft.Text("Alice")),
                                                        ft.DataCell(ft.Text("Wong")),
                                                        ft.DataCell(ft.Text("25")),
                                                    ]),
                                                ],
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

        page.update()

    def view_pop(e):
        print("View pop:", e.view)
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go(page.route)

    def perfil_docente(page: Page):
        page.clean()
        local_ruta = "Perfil docente"
        page.add(Text(local_ruta, size=20, weight=FontWeight.BOLD))
        page.update()

app(target=mostrar_menu_principal, port=5000, view=AppView.WEB_BROWSER)