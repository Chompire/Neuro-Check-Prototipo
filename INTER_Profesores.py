import flet as ft
from test import iniciar_test
from CRUD import profesorREAD, estudiantesREAD, testREAD, resultados_detalladosREAD
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
    page.update()

def create_perfil_view(page: ft.Page, estudiantes_data, profesor_data, test_data):
    page.update()
    if not profesor_data:
        return ft.View(
            route="/perfil_docente",
            bgcolor=color_Background,
            controls=[
                create_app_bar(page, "Perfil Docente"),
                ft.Text("No se pudo cargar la información del perfil.", color="red")
            ]
        )
    
    def test_completos_row_select(e):
        for row in test_completos.rows:
            row.selected = False
        e.control.selected = True
        test_id_seleccionado = e.control.data[1] # El test_ID está en el índice 1 de los datos de la fila
        print(f"Test seleccionado: {test_id_seleccionado}")
        page.go(f"/resultados_detallados/test/{test_id_seleccionado}")

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
                    ft.DataColumn(ft.Text("Fecha de creación")),
                    ft.DataColumn(ft.Text("Fecha de finalización")),
                    ft.DataColumn(ft.Text("Porcentaje de riesgo")),
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
                            ft.DataCell(ft.Text(f"{test_dat[2] or ''}")),
                            ft.DataCell(ft.Text(f"{test_dat[3] or ''}")),
                            ft.DataCell(ft.Text(f"{test_dat[11]}%")),
                            ],
                            data = test_dat,
                            selected=True if id_to_select is not None and test_dat[0] == id_to_select else False,
                            on_select_changed=test_completos_row_select,
                        ),
        )   
        page.update()
    
    carga_estudiantes()
   

    doc_info = list(profesor_data)
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
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Column(
                                scroll=ft.ScrollMode.AUTO,
                                controls=[
                                ft.Text("Datos del docente:", size=30, weight=ft.FontWeight.BOLD, color="black"),
                                info_table
                                ])]),
                    
                    ft.Divider(color="black"),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                        ft.Column(controls=[
                            ft.Row(controls=[ft.Text("Resultados detallados:", size=30, weight=ft.FontWeight.BOLD, color="black")]),
                            test_completos])
                            ])
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

    # --- Variables de estado para la paginación ---
    ROWS_PER_PAGE_EST = 5
    ROWS_PER_PAGE_TEST = 5
    current_page_estudiantes = 0
    current_page_tests = 0
    total_pages_est = 1
    total_pages_test = 1


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
    
    def carga_estudiantes(estudiantes_a_mostrar, test_a_mostrar, id_to_select=None):
        nonlocal total_pages_est, total_pages_test, current_page_estudiantes, current_page_tests

        estudiante_table.rows.clear()
        test_incompletos.rows.clear()
        
        # --- Lógica de paginación para Estudiantes ---
        total_items_est = len(estudiantes_a_mostrar)
        print("total_items_est: ", total_items_est)
        print("ROWS_PER_PAGE_EST: ", ROWS_PER_PAGE_EST)
        print("total_items_est: ", total_items_est)
        total_pages_est = (total_items_est + ROWS_PER_PAGE_EST - 1) // ROWS_PER_PAGE_EST
        start_index_est = current_page_estudiantes * ROWS_PER_PAGE_EST
        end_index_est = start_index_est + ROWS_PER_PAGE_EST
        estudiantes_pagina_actual = estudiantes_a_mostrar[start_index_est:end_index_est]

        page_label_est.value = f"Página {current_page_estudiantes + 1} de {total_pages_est}"
        prev_button_est.disabled = current_page_estudiantes == 0
        next_button_est.disabled = current_page_estudiantes >= total_pages_est - 1

        # Cargar datos de estudiantes de la página actual
        if estudiantes_a_mostrar:
            for est_dat in estudiantes_pagina_actual:
                estudiante_table.rows.append(
                        ft.DataRow(
                            cells=[
                                
                            ft.DataCell(content=ft.Text(f"{est_dat[1]} {est_dat[2] or ''}{est_dat[3] or ''}".strip())),
                            ft.DataCell(ft.Text(f"{est_dat[4]} {est_dat[5]}")),
                            ft.DataCell(ft.Text(f"{est_dat[6]}")), #nacimiento
                            ft.DataCell(ft.Text(f"{est_dat[7]}")),# rut
                            ft.DataCell(ft.Text(f"{est_dat[12]}")),#curso
                            ft.DataCell(ft.Text(f"{est_dat[13]}")),
                        ],
                        
                        data=est_dat, 
                        selected=True if id_to_select is not None and est_dat[0] == id_to_select else False,
                        on_select_changed=es_row_select,
                    ),
            
        )

        # --- Lógica de paginación para Tests ---
        print("test_a_mostrar: ", test_a_mostrar)
        total_items_test = len(test_a_mostrar)
        total_pages_test = (total_items_test + ROWS_PER_PAGE_TEST - 1) // ROWS_PER_PAGE_TEST
        start_index_test = current_page_tests
        end_index_test = start_index_test + ROWS_PER_PAGE_TEST
        tests_pagina_actual = test_a_mostrar[start_index_test:end_index_test]

        page_label_test.value = f"Página {current_page_tests + 1} de {total_pages_test}"
        prev_button_test.disabled = current_page_tests == 0
        next_button_test.disabled = current_page_tests >= total_pages_test - 1

        # Cargar datos de tests de la página actual
        if test_a_mostrar:
            for test_dat in tests_pagina_actual:
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

    # --- Funciones de Paginación ---
    def next_page_est(e):
        nonlocal current_page_estudiantes
        if current_page_estudiantes < total_pages_est - 1:
            current_page_estudiantes += 1
            handle_search() # Recargar con filtro actual

    def prev_page_est(e):
        nonlocal current_page_estudiantes
        if current_page_estudiantes > 0:
            current_page_estudiantes -= 1
            handle_search() # Recargar con filtro actual

    def next_page_test(e):
        nonlocal current_page_tests
        if current_page_tests < total_pages_test - 1:
            current_page_tests += 1
            test_search() # Recargar con filtro actual

    def prev_page_test(e):
        nonlocal current_page_tests
        if current_page_tests > 0:
            current_page_tests -= 1
            test_search() # Recargar con filtro actual


    def handle_search(reset_page=False):
        nonlocal current_page_estudiantes
        if reset_page:
            current_page_estudiantes = 0 # Resetear página solo si se solicita

        search_text = es_search_field.value.lower() if es_search_field.value else ""
        if not search_text:
            carga_estudiantes(estudiante_data, test_data)
        else:
            # Filtrar estudiantes
            estudiantes_filtrados = []
            for est in estudiante_data:
                nombre_completo = f"{est[1]} {est[4]}".lower()
                rut = str(est[7]).lower()
                curso = str(est[12]).lower()
    
                if search_text in nombre_completo or search_text in rut or search_text in curso:
                    estudiantes_filtrados.append(est)
            # Mostramos los estudiantes filtrados y la lista completa de tests
            carga_estudiantes(estudiantes_filtrados, test_data)

    def test_search(reset_page=False):
        nonlocal current_page_tests
        if reset_page:
            current_page_tests = 0

        search_text = test_search_field.value.lower() if test_search_field.value else ""
        if not search_text:
            # Al limpiar la búsqueda, mostramos ambas listas completas
            carga_estudiantes(estudiante_data, test_data)
        else:
            # Filtrar tests
            test_filtrados = []
            for test in test_data: # Corregido: buscar en test_data
                nombre_completo = f"{test[4]} {test[5]}".lower() # Corregido: índices para nombre y apellido en test_data
                rut = str(test[6]).lower() # Corregido: índice para rut en test_data
                curso = str(test[7]).lower() # Corregido: índice para curso en test_data
    
                if search_text in nombre_completo or search_text in rut or search_text in curso:
                    test_filtrados.append(test)
            carga_estudiantes(estudiante_data, test_filtrados)
   
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
        height=40)
    upload_button = ft.ElevatedButton(
        text="Reanudar Test",
        icon=ft.Icons.PLAY_CIRCLE_OUTLINE,
        icon_color=ft.Colors.WHITE,
        color=ft.Colors.WHITE,
        bgcolor=color_Docente, visible=False, on_click=on_reanudar_test_click,
        width=150,
        height=40)
    
    # --- Controles de Paginación UI ---
    page_label_est = ft.Text(f"Página 1 de {total_pages_est}", color="black")
    prev_button_est = ft.IconButton(ft.Icons.KEYBOARD_ARROW_LEFT, on_click=prev_page_est, disabled=True)
    next_button_est = ft.IconButton(ft.Icons.KEYBOARD_ARROW_RIGHT, on_click=next_page_est, disabled=True)
    pagination_controls_est = ft.Row([prev_button_est, page_label_est, next_button_est], alignment=ft.MainAxisAlignment.CENTER)

    page_label_test = ft.Text(f"Página 1 de {total_pages_test}", color="black")
    prev_button_test = ft.IconButton(ft.Icons.KEYBOARD_ARROW_LEFT, on_click=prev_page_test, disabled=True)
    next_button_test = ft.IconButton(ft.Icons.KEYBOARD_ARROW_RIGHT, on_click=next_page_test, disabled=True)
    pagination_controls_test = ft.Row([prev_button_test, page_label_test, next_button_test], alignment=ft.MainAxisAlignment.CENTER)

    es_search_field = ft.TextField(hint_text="Buscar por nombre, RUT o curso...", text_style=ft.TextStyle(color="white"), color="white", bgcolor=color_Docente, on_change=lambda e: handle_search(reset_page=True), expand=True)
    test_search_field = ft.TextField(hint_text="Buscar por nombre, RUT o curso...", text_style=ft.TextStyle(color="white"), color="white", bgcolor=color_Docente, on_change=lambda e: test_search(reset_page=True), expand=True)

    # Llamada inicial correcta con ambas listas de datos
    carga_estudiantes(estudiante_data, test_data)


    return ft.View(
        route="/seleccionar_estudiante",
        bgcolor=color_Background,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            create_app_bar(page, "Seleccionar Estudiante"), 
            
                    ft.Row(alignment=ft.MainAxisAlignment.CENTER,
                           controls=[ft.Column(controls=[
                               ft.Row(controls=[                                   
                                   ft.Text("Seleccionar estudiante:", size=30, weight=ft.FontWeight.BOLD, color="black"),
                                   next_button]),

                                   ft.Container(content=ft.Row(controls=[es_search_field])),
                                   
                                   estudiante_table,
                                   pagination_controls_est]),
                                    ]),
                    
                    ft.Divider(color="black"),
                    ft.Row(alignment=ft.MainAxisAlignment.CENTER,
                           controls=[ft.Column(controls=[
                               ft.Row(controls=[
                                   ft.Text("Terminar test incompleto:", size=30, weight=ft.FontWeight.BOLD, color="black"),
                                   upload_button]), 
                                   ft.Container(content=ft.Row(controls=[test_search_field])),
                                   test_incompletos,
                                   pagination_controls_test]),
                                    ]),
                ],
            )


def resultados_detallados(page: ft.Page, estudiantes_data, profesor_data, id_value: int, id_type: str):
    if id_type == 'test':
        test_info = resultados_detalladosREAD(test_ID=id_value)
    elif id_type == 'det':
        test_info = resultados_detalladosREAD(det_ID=id_value)
    else:
        test_info = []
    
    rows = []
    
    puntaje_control = ft.Container(
        content=ft.Column(
            [
                ft.Text("Puntaje", weight=ft.FontWeight.BOLD, size=20,color="white"),
                ft.Text(f"{test_info[0][7]}/20" if test_info else "N/A", size=50, weight=ft.FontWeight.BOLD,color="white"),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            
        ),
        border=ft.border.all(2, color_Docente),
        border_radius=8,
        padding=15,
        bgcolor=color_Docente
    )
    porcentaje_control = ft.Container(
        content=ft.Column(
            [
                ft.Text("Porcentaje", weight=ft.FontWeight.BOLD, size=20,color="white"),
                ft.Text(f"{test_info[0][6]}%", size=50, weight=ft.FontWeight.BOLD,color="white"),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            
        ),
        border=ft.border.all(2, color_Docente),
        border_radius=8,
        padding=15,
        bgcolor= color_Docente
    )

    if test_info:
        for test in test_info:
            nombre_es = test[1]
            apellido_es = test[2]
            curso = test[3]
            fecha_termino = test[8] # Correct index for det_fecha
            año_termino = fecha_termino.year if fecha_termino else "N/A"
            rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(nombre_es)),
                    ft.DataCell(ft.Text(apellido_es)),
                    ft.DataCell(ft.Text(curso)),
                    ft.DataCell(ft.Text(str(año_termino))),
                ])
            )
        # Si hay datos, actualizar los controles de puntaje y porcentaje con el primer resultado
        

    datatable = ft.DataTable(
        heading_row_color= color_Docente,
        heading_text_style=ft.TextStyle(color="white", weight=ft.FontWeight.BOLD),
        bgcolor="white",
        border=ft.border.all(2, ft.Colors.BLACK),
        vertical_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
        horizontal_lines=ft.border.BorderSide(1, ft.Colors.BLACK),
        data_text_style=ft.TextStyle(color="black"),
        columns=[
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Apellidos")),
            ft.DataColumn(ft.Text("Curso")),
            ft.DataColumn(ft.Text("Fecha de test"))],
        rows=rows
    )
    return ft.View(
        route="/resultados_detallados",
        bgcolor=color_Background,
        controls=[
            create_app_bar(page, "Resultados detallados"),
            ft.Column(
                expand=True,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Column(
                                scroll=ft.ScrollMode.AUTO,
                                controls=[
                                    ft.Text("Datos del alumno:", size=30, weight=ft.FontWeight.BOLD, color="black"),
                                    datatable,
                                ]
                            )                    
                        ]
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[puntaje_control, porcentaje_control]),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Column(
                                scroll=ft.ScrollMode.AUTO,
                                controls=[
                                    ft.Text("Posibles indicios de riesgo:", size=30, weight=ft.FontWeight.BOLD, color="black"),
                                    ft.Container( width=600, alignment=ft.alignment.center, border=ft.border.all(1, ft.Colors.BLACK),bgcolor=ft.Colors.WHITE, padding=10)
                                    
                                ]
                            )                    
                        ]
                    ),
                ]
            )
            
        ]
    )   

def mostrar_menu_principal(page: ft.Page, pro_nameID: int, test_ID: int = None, det_ID  = None, results_test_ID: int = None):
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
            page.views.append(seleccionar_estudiante(page, estudiantesREAD(), profesor_data, test_data_false))
        elif page.route.startswith("/resultados_detallados"):
            parts = page.route.split('/')
            if len(parts) == 4:
                id_type = parts[2] # 'test' o 'det'
                id_value = int(parts[3])
                page.views.append(resultados_detallados(page,estudiantesREAD(), profesor_data, id_value, id_type))
        page.update()

    def view_pop(e: ft.ViewPopEvent):
        print(f"Cerrando vista: {e.view}")
        if e.view.route.startswith("/resultados_detallados"):
            page.views.pop()
            page.go("/perfil_docente")
            page.update()
        else:
            page.views.pop() # Elimina la vista actual
            if page.views:  # Verifica si aún quedan vistas en la pila
                
                top_view = page.views[-1]
                page.go(top_view.route)
            else:
                page.go("/") # Fallback si no quedan vistas en la pila

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    if det_ID:
        page.go(f"/resultados_detallados/det/{det_ID}")
    elif test_ID:
        page.go(f"/resultados_detallados/test/{test_ID}")
    else:
        page.go("/inicio_profesor")
if __name__ == "__main__":
    def main_standalone(page: ft.Page):
        id_profesor_pie_test = 2
        mostrar_menu_principal(page, id_profesor_pie_test) # Se elimina el argumento faltante

    ft.app(target=main_standalone, assets_dir="assets",view=ft.AppView.FLET_APP)