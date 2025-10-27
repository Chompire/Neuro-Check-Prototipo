import flet as ft
from test import iniciar_test
from CRUD import profesorREAD, estudiantesREAD, preguntaREAD, testREAD

color_Docente = "#FF0000"
color_Background = "#FF7F7F"

def create_app_bar(page: ft.Page, title: str):
    return ft.AppBar(
        title=ft.TextButton(
            content=ft.Text("Neuro Check", size=25, weight=ft.FontWeight.BOLD, color="white"),
            on_click=lambda _: page.go("/inicio_profesor")
        ),
        bgcolor=color_Docente,
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
        bgcolor=color_Background,
        controls=[
            create_app_bar(page, "Inicio"),
            ft.Column(
                expand=True,
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
                                    color=color_Docente,
                                    content=ft.Container(
                                        content=ft.Column([
                                            ft.ListTile(
                                                title=ft.Text("Realizar test", size=20, weight=ft.FontWeight.BOLD),
                                                subtitle=ft.Text(
                                                    "El test sirve para obtener el porcentaje de riesgo del estudiante para posiblemente derivarlo al equipo PIE.",
                                                    size=15
                                                ),
                                            ),
                                            ft.ElevatedButton(text="Entrar", color="black", bgcolor=color_Background, on_click=lambda _: page.go("/seleccionar_estudiante"))
                                        ]),
                                        width=600,
                                        padding=10,
                                    )
                                ),
                                ft.Card(
                                    color=color_Docente,
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
                                                bgcolor= color_Background   ,
                                                on_click=lambda _: page.go("/perfil_docente")
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
                     # El pie de página se coloca al final
                ]
            ),
        ]
    )
def create_perfil_view(page: ft.Page, estudiantes_data, profesor_data, test_data):
    
    if not profesor_data:
        return ft.View(
            route="/perfil_docente",
            bgcolor=color_Background,
            controls=[
                create_app_bar(page, "Perfil Docente"),
                ft.Text("No se pudo cargar la información del perfil.", color="red")
            ]
        )
    
    test_completos =ft.DataTable(
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
                    ft.DataColumn(ft.Text("Fecha de finalización")),
                    ft.DataColumn(ft.Text("Estado")),
                ],
    )
    
    def carga_estudiantes(id_to_select = None): 
        test_completos.rows.clear()
        test = test_data
        
        if test:
            for test_dat in test_data:
                test_completos.rows.append(
                        ft.DataRow(
                            cells=[
                            ft.DataCell(ft.Text(f"{test_dat[4]}")),
                            ft.DataCell(ft.Text(f"{test_dat[5]}")),
                            ft.DataCell(ft.Text(f"{test_dat[6]}")),#rut
                            ft.DataCell(ft.Text(f"{test_dat[7]}")),#curso
                            ft.DataCell(ft.Text(f"{test_dat[8]} {test_dat[9] or ''}".strip())),#profesor
                            ft.DataCell(ft.Text(f"{test_dat[2] or ''}")),
                            ft.DataCell(ft.Text(f"{test_dat[3] or ''}")),
                            ft.DataCell(ft.Text("Incompleto" if test_dat[0] == 0 else "Completo")),
                            ],
                            data = test_dat,
                            selected=True if id_to_select is not None and test_dat[0] == id_to_select else False,
                            
                        ),
        )   
        page.update()
    
    carga_estudiantes()
   

    doc_info = list(profesor_data)
    print(doc_info)
    info_table = ft.DataTable(
        heading_row_color= color_Docente,
        data_row_color="white",
        columns=[
            ft.DataColumn(ft.Text("Nombres")),
            ft.DataColumn(ft.Text("Apellidos")),
            ft.DataColumn(ft.Text("RUT")),
            ft.DataColumn(ft.Text("Cargo")),
            ft.DataColumn(ft.Text("Curso")),
        ],
        rows=[
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(f"{doc_info[1]} {doc_info[2] or ''} {doc_info[3] or ''}".strip())),
                ft.DataCell(ft.Text(f"{doc_info[4]} {doc_info[5]}")),
                ft.DataCell(ft.Text(f"{doc_info[6]}")), # pro_rut is at index 7
                ft.DataCell(ft.Text("Profesional PIE" if doc_info[9] == 1 else "Profesor Docente")), # pro_cargo is at index 9
                ft.DataCell(ft.Text(f"{doc_info[12] or ''}")), # Usamos el índice 13 (nombre del curso)
            ]),
        ],
        data_text_style=ft.TextStyle(color="black"),
        heading_text_style=ft.TextStyle(color="white", weight=ft.FontWeight.BOLD),
        border=ft.border.all(2, ft.Colors.BLACK),
        vertical_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
        horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
    )
    return ft.View(
        route="/perfil_docente",
        bgcolor=color_Background,
        controls=[
            create_app_bar(page, "Perfil Docente"),
            
            ft.Column(
                scroll=ft.ScrollMode.AUTO,
                expand=True, 
                controls=[
                    ft.Text("Datos del docente", size=30, weight=ft.FontWeight.BOLD, color="black"),
                    ft.Row(
                        controls=[info_table],
                        scroll=ft.ScrollMode.AUTO
                    ),
                    ft.Divider(color="black"),
                    ft.Column(controls=[
                        ft.Row(controls=[ft.Text("Resultados de tests", size=30, weight=ft.FontWeight.BOLD, color="black")]),
                        test_completos]),
                ]),
            
        ]
    )

def seleccionar_estudiante(page: ft.Page, estudiante_data, profesor_data, test_data):
    if not estudiante_data:
        return ft.View(
            route="/seleccionar_estudiante",
            bgcolor=color_Background,
            controls=[
                create_app_bar(page, "Seleccionar Estudiante"),
                ft.Text("No se pudo cargar la información del los estudiantes.", color="red")
            ]
        )
    
    selected_es_id = None
    selected_test_id = None
    estudiante_table = ft.DataTable(
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
                    ft.DataColumn(ft.Text("Profesor Jefe")),
                ],
    )
    test_incompletos =ft.DataTable(
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
    def es_row_select(e):
        nonlocal selected_es_id
        selected_es= e.control.data
        is_currently_selected = e.control.selected

        for row in estudiante_table.rows:
            row.selected = False
        if not is_currently_selected:
            e.control.selected = True
            next_button.visible = True
            selected_es_id =  selected_es[0]
            
        else:
            for row in estudiante_table.rows:
                row.selected = False
            if selected_es_id is not None:
                next_button.visible = False
        for row in test_incompletos.rows:
            row.selected = False
        
        page.update()
    def test_row_select(e):
        nonlocal selected_test_id
        selected_test= e.control.data
        is_currently_selected = e.control.selected

        for row in test_incompletos.rows:
            row.selected = False
        if not is_currently_selected:
            e.control.selected = True
            upload_button.visible = True
            selected_test_id =  selected_test[1]
            
            
        else:
            for row in test_incompletos.rows:
                row.selected = False
            if selected_test_id is not None:
                upload_button.visible = False
        page.update()       
    
    def carga_estudiantes(id_to_select = None):
        
        estudiante_table.rows.clear()
        estudiante = estudiante_data
        test_incompletos.rows.clear()
        test = test_data
        
        if estudiante:
            for est_dat in estudiante_data:
                estudiante_table.rows.append(
                        ft.DataRow(
                            cells=[
                            ft.DataCell(ft.Text(f"{est_dat[1]} {est_dat[2] or ''}{est_dat[3] or ''}".strip())),
                            ft.DataCell(ft.Text(f"{est_dat[4]} {est_dat[5]}")),
                            ft.DataCell(ft.Text(f"{est_dat[6]}")), #nacimiento
                            ft.DataCell(ft.Text(f"{est_dat[7]}")),# rut
                            ft.DataCell(ft.Text(f"{est_dat[12]}")),#curso
                            ft.DataCell(ft.Text(f"{est_dat[13]}")),
                        ],
                        data=est_dat, # Se asignan los datos de la fila al atributo 'data'
                        selected=True if id_to_select is not None and est_dat[0] == id_to_select else False,
                        on_select_changed=es_row_select,
                    ),
            
        )
        if test:
            for test_dat in test_data:
                test_incompletos.rows.append(
                        ft.DataRow(
                            cells=[
                            ft.DataCell(ft.Text(f"{test_dat[4]}")),
                            ft.DataCell(ft.Text(f"{test_dat[5]}")),
                            ft.DataCell(ft.Text(f"{test_dat[6]}")),#rut
                            ft.DataCell(ft.Text(f"{test_dat[7]}")),#curso
                            ft.DataCell(ft.Text(f"{test_dat[8]} {test_dat[9] or ''}".strip())),#profesor
                            ft.DataCell(ft.Text(f"{test_dat[2] or ''}")), # Fecha de creación
                            ft.DataCell(ft.Text("Incompleto" if test_dat[0] == 0 else "Completo")),
                            ],
                            data = test_dat,
                            selected=True if id_to_select is not None and test_dat[0] == id_to_select else False,
                            on_select_changed=test_row_select,
                        ),
        )

            
        page.update()
    carga_estudiantes()
   

    def on_iniciar_test_click(_):
        if selected_es_id is None:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, selecciona un estudiante para iniciar el test."), bgcolor=ft.Colors.RED)
            page.snack_bar.open = True
            page.update()
            return
        if profesor_data is None or len(profesor_data) < 1: # Asegurarse de que profesor_data sea válido y tenga pro_nameID
            page.snack_bar = ft.SnackBar(ft.Text("Error: No se pudo obtener la información del profesor para iniciar el test."), bgcolor=ft.Colors.RED)
            page.snack_bar.open = True
            page.update()
            return
        iniciar_test(page, selected_es_id, profesor_data[0])

    def on_reanudar_test_click(_):
        if selected_test_id is None:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, selecciona un test para reanudar."), bgcolor=ft.Colors.RED)
            page.snack_bar.open = True
            page.update()
            return
        # Reutilizamos iniciar_test para reanudar, pasándole el test_id
        iniciar_test(page, es_nameID=None, pro_nameID=None, test_id=selected_test_id)

    next_button = ft.ElevatedButton(
        text="Iniciar Test",
        icon=ft.Icons.PLAY_ARROW,
        icon_color=ft.Colors.WHITE,
        color=ft.Colors.WHITE,
        bgcolor=color_Docente,
        visible=False,
        on_click=on_iniciar_test_click,
        width=150,
        height=50)
    upload_button = ft.ElevatedButton(
        text="Reanudar Test",
        icon=ft.Icons.PLAY_CIRCLE_OUTLINE,
        icon_color=ft.Colors.WHITE,
        color=ft.Colors.WHITE,
        bgcolor=color_Docente, visible=False, on_click=on_reanudar_test_click,
        width=150,
        height=50)


    return ft.View(
        route="/seleccionar_estudiante",
        bgcolor=color_Background,
        controls=[
            create_app_bar(page, "Seleccionar Estudiante"),
            ft.Container(
                
                expand = True,
                content=ft.Row(vertical_alignment=ft.CrossAxisAlignment.START,controls=[
            ft.Column(
                expand = True,
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Column(controls=[
                        ft.Row(controls=[ft.Text("Nuevo test", size=30, weight=ft.FontWeight.BOLD, color="black"),next_button]),
                        estudiante_table]),
                    ft.Divider(color="black"),
                    ft.Column(controls=[
                        ft.Row(controls=[ft.Text("Terminar test", size=30, weight=ft.FontWeight.BOLD, color="black"),upload_button]),
                        test_incompletos]),
                ],
            )]
            )
            )
        ]
    )

def mostrar_menu_principal(page: ft.Page, pro_nameID: int):
    page.clean()
    page.title = "Neuro Check - Profesor"
    page.bgcolor = color_Background
    profesor_data = profesorREAD(pro_nameID)
    test_data_false = testREAD(test_ID=None,test_status=0)
    test_data_true = testREAD(test_ID=None,test_status=1)
    page.route = "/inicio_profesor"

    def route_change(e: ft.RouteChangeEvent):
        print(f"Cambiando a la ruta: {e.route}")
        page.views.clear()
        page.views.append(create_inicio_view(page, profesor_data)) # Vista inicial
        if page.route == "/perfil_docente":
            page.views.append(create_perfil_view(page, estudiantesREAD(),profesor_data, test_data_true))
        elif page.route == "/seleccionar_estudiante":
            page.views.append(seleccionar_estudiante(page, estudiantesREAD(), profesor_data, test_data_false)) # Carga los estudiantes al navegar
        
        page.update()

    def view_pop(e: ft.ViewPopEvent):
        print(f"Cerrando vista: {e.view}")
        page.views.pop() # Elimina la vista actual
        if page.views: # Verifica si aún quedan vistas en la pila
            top_view = page.views[-1]
            page.go(top_view.route)
        else:
            # Si no quedan vistas, regresa a la pantalla de inicio de sesión principal
            page.go("/")
            page.update()

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go("/inicio_profesor")
if __name__ == "__main__":
    def main_standalone(page: ft.Page):
        id_profesor_pie_test = 2
        mostrar_menu_principal(page, id_profesor_pie_test) # Se elimina el argumento faltante

    ft.app(target=main_standalone, assets_dir="assets",view=ft.AppView.FLET_APP)