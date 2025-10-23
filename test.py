import flet as ft
from CRUD import testCREATE, preguntaCREATE, preguntaREAD, preguntaUPDATE, testREAD,testUPDATE
from resultados import ver_resultados
color_Background = "#FF7F7F"
color_Docente = "#FF0000"
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
def test_viewATENCION(page: ft.Page,test_id, id_atencion, respuestas_guardadas=None):

    def guardar_respuestas(e):
        respuestas_atencion = [atencion_radiogroup1.value,atencion_radiogroup2.value,atencion_radiogroup3.value,atencion_radiogroup4.value,atencion_radiogroup5.value]
        for i, pregunta_texto in enumerate(preguntas_atencion):
            respuesta = respuestas_atencion[i]
            preguntaUPDATE(id_atencion[i], {"pre_respuesta": respuesta})
        page.snack_bar = ft.SnackBar(ft.Text("Sección de Atención guardada."), bgcolor=ft.Colors.GREEN)
        page.snack_bar.open = True
        page.go("/test_memoria")
        page.update()

    # --- Variables para las preguntas de Atención ---
    preguntas_atencion = [
        "1. ¿El estudiante se distrae con facilidad en clases?",
        "2. ¿Le cuesta mantener la atención en tareas o actividades lúdicas?",
        "3. ¿Parece no escuchar cuando se le habla directamente?",
        "4. ¿Evita, le disgusta o es renuente a dedicarse a tareas que requieren un esfuerzo mental sostenido?",
        "5. ¿A menudo pierde cosas necesarias para tareas o actividades?"
    ]

    atencion_radiogroup1 = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="si", label="Sí"),
        ft.Radio(value="no", label="No"),
    ]))
    atencion_radiogroup2 = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="si", label="Sí"),
        ft.Radio(value="no", label="No"),
    ]))
    atencion_radiogroup3 = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="si", label="Sí"),
        ft.Radio(value="no", label="No"),
    ]))
    atencion_radiogroup4 = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="si", label="Sí"),
        ft.Radio(value="no", label="No"),
    ]))
    atencion_radiogroup5 = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="si", label="Sí"),
        ft.Radio(value="no", label="No"),
    ]))

    # Si hay respuestas guardadas, las asignamos a los RadioGroups
    if respuestas_guardadas:
        atencion_radiogroup1.value = respuestas_guardadas[0]
        atencion_radiogroup2.value = respuestas_guardadas[1]
        atencion_radiogroup3.value = respuestas_guardadas[2]
        atencion_radiogroup4.value = respuestas_guardadas[3]
        atencion_radiogroup5.value = respuestas_guardadas[4]
    
    atencion_column = ft.Column(
                        controls=[
                            ft.Text("Atención", size=40, weight=ft.FontWeight.BOLD, color="black"),
                            ft.Text(preguntas_atencion[0], size=20, weight=ft.FontWeight.BOLD, color="black"),
                            atencion_radiogroup1,
                            
                            ft.Text(preguntas_atencion[1], size=20, weight=ft.FontWeight.BOLD, color="black"),
                            atencion_radiogroup2,

                            ft.Text(preguntas_atencion[2], size=20, weight=ft.FontWeight.BOLD, color="black"),
                            atencion_radiogroup3,

                            ft.Text(preguntas_atencion[3], size=20, weight=ft.FontWeight.BOLD, color="black"),
                            atencion_radiogroup4,
                            
                            ft.Text(preguntas_atencion[4], size=20, weight=ft.FontWeight.BOLD, color="black"),
                            atencion_radiogroup5,
                            ],
                        )
    
    finalizar_button = ft.ElevatedButton("Finalizar Test", on_click=guardar_respuestas, bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE)
    siguiente_button = ft.ElevatedButton("Siguiente", on_click=guardar_respuestas, bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE)
    return ft.View(
        route="/test_atencion",
        bgcolor=color_Background,
        controls=[
            create_app_bar(page, "Test"),
                ft.Column(
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                    spacing=20,
                    controls=[
                        atencion_column,
                        siguiente_button
                    ]
                )
            ]
        )
def test_viewMEMORIA(page: ft.Page,test_id, id_memoria, respuestas_guardadas=None):
    def guardar_respuestas(e):
        respuestas_memoria = [memoria_radiogroup1.value,memoria_radiogroup2.value,memoria_radiogroup3.value,memoria_radiogroup4.value,memoria_radiogroup5.value]
        for i, pregunta_texto in enumerate(preguntas_memoria):
            respuesta = respuestas_memoria[i]
            preguntaUPDATE(id_memoria[i], {"pre_respuesta": respuesta})
        page.snack_bar = ft.SnackBar(ft.Text("Sección de Memoria guardada."), bgcolor=ft.Colors.GREEN)
        page.snack_bar.open = True
        page.go("/test_social")
        page.update()

    # --- Variables para las preguntas de Memoria ---
    preguntas_memoria = [
        "1. ¿Olvida con frecuencia información recién aprendida?",
        "2. ¿Tiene dificultad para recordar eventos o encargos importantes?",
        "3. ¿Necesita que le repitan las instrucciones varias veces?",
        "4. ¿Le cuesta seguir una conversación o una historia larga?",
        "5. ¿Confunde nombres, fechas o lugares con frecuencia?"
    ]
    memoria_radiogroup1 = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="si", label="Sí"),
        ft.Radio(value="no", label="No"),
    ]))
    memoria_radiogroup2 = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="si", label="Sí"),
        ft.Radio(value="no", label="No"),
    ]))
    memoria_radiogroup3 = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="si", label="Sí"),
        ft.Radio(value="no", label="No"),
    ]))
    memoria_radiogroup4 = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="si", label="Sí"),
        ft.Radio(value="no", label="No"),
    ]))
    memoria_radiogroup5 = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="si", label="Sí"),
        ft.Radio(value="no", label="No"),
    ]))

    # Si hay respuestas guardadas, las asignamos a los RadioGroups
    if respuestas_guardadas:
        memoria_radiogroup1.value = respuestas_guardadas[0]
        memoria_radiogroup2.value = respuestas_guardadas[1]
        memoria_radiogroup3.value = respuestas_guardadas[2]
        memoria_radiogroup4.value = respuestas_guardadas[3]
        memoria_radiogroup5.value = respuestas_guardadas[4]
    memoria_column = ft.Column(
                        controls=[
                            ft.Text("Memoria", size=40, weight=ft.FontWeight.BOLD, color="black"),
                            ft.Text(preguntas_memoria[0], size=20, weight=ft.FontWeight.BOLD, color="black"),
                            memoria_radiogroup1,
                            ft.Text(preguntas_memoria[1], size=20, weight=ft.FontWeight.BOLD, color="black"),
                            memoria_radiogroup2,
                            ft.Text(preguntas_memoria[2], size=20, weight=ft.FontWeight.BOLD, color="black"),
                            memoria_radiogroup3,
                            ft.Text(preguntas_memoria[3], size=20, weight=ft.FontWeight.BOLD, color="black"),
                            memoria_radiogroup4,
                            ft.Text(preguntas_memoria[4], size=20, weight=ft.FontWeight.BOLD, color="black"),
                            memoria_radiogroup5,
                            ]
                        )
    siguiente_button = ft.ElevatedButton("Siguiente", on_click=guardar_respuestas, bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE)
    return ft.View(
        route="/test_memoria",
        bgcolor=color_Background,
        controls=[
            ft.Column(
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                    spacing=20,
                    controls=[
                        memoria_column, 
                        siguiente_button
                    ]
                )
        ]
    )

def test_viewSOCIAL(page: ft.Page, test_id, id_social, respuestas_guardadas=None):

    def guardar_respuestas(e):
        respuestas_social = [social_radiogroup1.value,social_radiogroup2.value,social_radiogroup3.value,social_radiogroup4.value,social_radiogroup5.value]
        for i, pregunta_texto in enumerate(preguntas_social):
            respuesta = respuestas_social[i]
            preguntaUPDATE(id_social[i], {"pre_respuesta": respuesta})
        page.snack_bar = ft.SnackBar(ft.Text("Sección Social guardada."), bgcolor=ft.Colors.GREEN)
        page.snack_bar.open = True
        page.go("/test_emocional")
        page.update()

    # --- Variables para las preguntas Sociales ---
    preguntas_social = [
        "1. ¿Le cuesta iniciar o mantener una conversación con sus compañeros?",
        "2. ¿Prefiere jugar solo en lugar de en grupo?",
        "3. ¿Tiene dificultades para entender las reglas de los juegos en grupo?",
        "4. ¿Le resulta difícil interpretar las emociones de los demás (expresiones faciales, tono de voz)?",
        "5. ¿Comparte sus juguetes o materiales con otros niños de forma reacia?"
    ]
    social_radiogroup1 = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="si", label="Sí"),
        ft.Radio(value="no", label="No"),
    ]))
    social_radiogroup2 = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="si", label="Sí"),
        ft.Radio(value="no", label="No"),
    ]))
    social_radiogroup3 = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="si", label="Sí"),
        ft.Radio(value="no", label="No"),
    ]))
    social_radiogroup4 = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="si", label="Sí"),
        ft.Radio(value="no", label="No"),
    ]))
    social_radiogroup5 = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="si", label="Sí"),
        ft.Radio(value="no", label="No"),
    ]))

    # Si hay respuestas guardadas, las asignamos a los RadioGroups
    if respuestas_guardadas:
        social_radiogroup1.value = respuestas_guardadas[0]
        social_radiogroup2.value = respuestas_guardadas[1]
        social_radiogroup3.value = respuestas_guardadas[2]
        social_radiogroup4.value = respuestas_guardadas[3]
        social_radiogroup5.value = respuestas_guardadas[4]
    social_column = ft.Column(
                        controls=[
                            ft.Text("Social", size=40, weight=ft.FontWeight.BOLD, color="black"),
                            ft.Text(preguntas_social[0], size=20, weight=ft.FontWeight.BOLD, color="black"),
                            social_radiogroup1,
                            ft.Text(preguntas_social[1], size=20, weight=ft.FontWeight.BOLD, color="black"),
                            social_radiogroup2,
                            ft.Text(preguntas_social[2], size=20, weight=ft.FontWeight.BOLD, color="black"),
                            social_radiogroup3,
                            ft.Text(preguntas_social[3], size=20, weight=ft.FontWeight.BOLD, color="black"),
                            social_radiogroup4,
                            ft.Text(preguntas_social[4], size=20, weight=ft.FontWeight.BOLD, color="black"),
                            social_radiogroup5,
                            ]
                        )
    siguiente_button = ft.ElevatedButton("Siguiente", on_click=guardar_respuestas, bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE)
    return ft.View(
        route="/test_social",
        bgcolor=color_Background,
        controls=[
            ft.Column(
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                    spacing=20,
                    controls=[
                        social_column, 
                        siguiente_button
                    ]
                )
        ]
    )

def test_viewEMOCIONAL(page: ft.Page, test_id, id_emocional, respuestas_guardadas=None):
    def guardar_respuestas(e):
        respuestas_emocional = [emocional_radiogroup1.value,emocional_radiogroup2.value,emocional_radiogroup3.value,emocional_radiogroup4.value,emocional_radiogroup5.value]
        for i, pregunta_texto in enumerate(preguntas_emocional):
            respuesta = respuestas_emocional[i]
            preguntaUPDATE(id_emocional[i], {"pre_respuesta": respuesta}) # Corregido: Esta línea estaba fuera del bucle
            
        page.snack_bar = ft.SnackBar(ft.Text("Test finalizado y respuestas guardadas."), bgcolor=ft.Colors.GREEN)
        page.snack_bar.open = True
        testUPDATE(test_id, {"test_status": 1})
        ver_resultados(page, test_id)
        page.update()

    # --- Variables para las preguntas Emocionales ---
    preguntas_emocional = [
        "1. ¿Tiene rabietas o explosiones de ira frecuentes o intensas?",
        "2. ¿Se muestra a menudo ansioso, preocupado o temeroso sin una razón aparente?",
        "3. ¿Parece triste, desanimado o irritable la mayor parte del tiempo?",
        "4. ¿Le cuesta calmarse después de una situación estresante o frustrante?",
        "5. ¿Reacciona de forma exagerada a críticas o comentarios negativos?"
    ]
    emocional_radiogroup1 = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="si", label="Sí"),
        ft.Radio(value="no", label="No"),
    ]))
    emocional_radiogroup2 = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="si", label="Sí"),
        ft.Radio(value="no", label="No"),
    ]))
    emocional_radiogroup3 = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="si", label="Sí"),
        ft.Radio(value="no", label="No"),
    ]))
    emocional_radiogroup4 = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="si", label="Sí"),
        ft.Radio(value="no", label="No"),
    ]))
    emocional_radiogroup5 = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="si", label="Sí"),
        ft.Radio(value="no", label="No"),
    ]))

    # Si hay respuestas guardadas, las asignamos a los RadioGroups
    if respuestas_guardadas:
        emocional_radiogroup1.value = respuestas_guardadas[0]
        emocional_radiogroup2.value = respuestas_guardadas[1]
        emocional_radiogroup3.value = respuestas_guardadas[2]
        emocional_radiogroup4.value = respuestas_guardadas[3]
        emocional_radiogroup5.value = respuestas_guardadas[4]
    emocional_column = ft.Column(
                        controls=[
                            ft.Text("Emocional", size=40, weight=ft.FontWeight.BOLD, color="black"),
                            ft.Text(preguntas_emocional[0], size=20, weight=ft.FontWeight.BOLD, color="black"),
                            emocional_radiogroup1,
                            ft.Text(preguntas_emocional[1], size=20, weight=ft.FontWeight.BOLD, color="black"),
                            emocional_radiogroup2,
                            ft.Text(preguntas_emocional[2], size=20, weight=ft.FontWeight.BOLD, color="black"),
                            emocional_radiogroup3,
                            ft.Text(preguntas_emocional[3], size=20, weight=ft.FontWeight.BOLD, color="black"),
                            emocional_radiogroup4,
                            ft.Text(preguntas_emocional[4], size=20, weight=ft.FontWeight.BOLD, color="black"),
                            emocional_radiogroup5,
                            ]
                        )
    finalizar_button = ft.ElevatedButton("Finalizar Test", on_click=guardar_respuestas, bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE)
    return ft.View(
        route="/test_emocional",
        bgcolor=color_Background,
        controls=[
            ft.Column(
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                    spacing=20,
                    controls=[
                        emocional_column, 
                        finalizar_button
                    ]
                )
        ]
    )

def iniciar_test(page: ft.Page, es_nameID: int | None, pro_nameID: int | None, test_id: int | None = None):
    page.clean()
    page.title = "Neuro Check - Test"
    page.bgcolor = color_Background
    id_atencion =[]
    id_memoria = []
    id_social = []
    id_emocional = []
    # Listas para almacenar las respuestas al reanudar
    respuestas_atencion = []
    respuestas_memoria = []
    respuestas_social = []
    respuestas_emocional = []
    if test_id is None:
        crear_id = testCREATE((es_nameID, pro_nameID))
        print(f"Creando preguntas iniciales para el test ID: {crear_id}")
        for i in range(5):
            pre_id = preguntaCREATE(("",None,"Atención", crear_id))
            print(f"  -> Pregunta de Atención creada con ID: {pre_id}")
            id_atencion.append(pre_id)
            
        for i in range(5):
            pre_id = preguntaCREATE(("",None,"Memoria", crear_id))
            print(f"  -> Pregunta de Memoria creada con ID: {pre_id}")
            id_memoria.append(pre_id)

        for i in range(5):
            pre_id = preguntaCREATE(("",None,"Social", crear_id))
            print(f"  -> Pregunta Social creada con ID: {pre_id}")
            id_social.append(pre_id)

        for i in range(5):
            pre_id = preguntaCREATE(("",None,"Emocional", crear_id))
            print(f"  -> Pregunta Emocional creada con ID: {pre_id}")
            id_emocional.append(pre_id)
    elif es_nameID is not None:
        crear_id = es_nameID
    else:
        crear_id = test_id
        print(f"Reanudando test ID: {crear_id}. Obteniendo IDs de preguntas existentes...")
        preguntas_existentes = preguntaREAD(test_id)
        for pregunta in preguntas_existentes:
            # La tupla es (pre_ID, pre_texto, pre_respuesta, pre_tipo)
            pre_id = pregunta[0]
            pre_respuesta = pregunta[2]
            pre_tipo = pregunta[3]
            if pre_tipo == "Atención":
                id_atencion.append(pre_id)
                respuestas_atencion.append(pre_respuesta)
            elif pre_tipo == "Memoria":
                id_memoria.append(pre_id)
                respuestas_memoria.append(pre_respuesta)
            elif pre_tipo == "Social":
                id_social.append(pre_id)
                respuestas_social.append(pre_respuesta)
            elif pre_tipo == "Emocional":
                id_emocional.append(pre_id)
                respuestas_emocional.append(pre_respuesta)
        print(f"IDs de Atención cargados: {id_atencion}")
        print(f"Respuestas de Atención cargadas: {respuestas_atencion}")
        print(f"IDs de Memoria cargados: {id_memoria}")
        print(f"Respuestas de Memoria cargadas: {respuestas_memoria}")
        print(f"IDs de Social cargados: {id_social}")
        print(f"Respuestas de Social cargadas: {respuestas_social}")
        print(f"IDs de Emocional cargados: {id_emocional}")
        print(f"Respuestas de Emocional cargadas: {respuestas_emocional}")
    

    def route_change(e: ft.RouteChangeEvent):
        print(f"Cambiando a la ruta: {e.route}")
        page.views.clear()
        page.views.append(test_viewATENCION(page,crear_id, id_atencion, respuestas_atencion))
        if  page.route == "/test_memoria":
            page.views.append(test_viewMEMORIA(page, crear_id, id_memoria, respuestas_memoria))
        elif page.route == "/test_social":
            page.views.append(test_viewSOCIAL(page, crear_id, id_social, respuestas_social))
        elif page.route == "/test_emocional":
            page.views.append(test_viewEMOCIONAL(page, crear_id, id_emocional, respuestas_emocional))
        elif page.route == "/inicio_profesor":
            from INTER_Profesores import mostrar_menu_principal
            mostrar_menu_principal(page, pro_nameID)
            page.go("/inicio_profesor") # Navegamos a la ruta correcta después de reiniciar
        page.update()
    
    def view_pop(e: ft.ViewPopEvent):
        print(f"Cerrando vista: {e.view}")
        # Solo intentar hacer pop si hay vistas en la lista para evitar el IndexError
        if page.views: 
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)
        else:
            # Al salir del test, volver a la selección de estudiante
            page.update()

    page.on_route_change = route_change
    page.on_view_pop = view_pop


    page.go("/test_atencion")
