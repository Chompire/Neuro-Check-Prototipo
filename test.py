import flet as ft
from CRUD import estudiantesREAD, testCREATE, profesorREAD, preguntaCREATE, testREAD
from resultados import ver_resultados
color_Background = "#FF7F7F"

def test_viewATENCION(page: ft.Page,test_id):

    def guardar_respuestas(e):
        respuestas_atencion = [atencion_radiogroup1.value,atencion_radiogroup2.value,atencion_radiogroup3.value,atencion_radiogroup4.value,atencion_radiogroup5.value]
        for i, pregunta_texto in enumerate(preguntas_atencion):
            respuesta = respuestas_atencion[i]
            preguntaCREATE((pregunta_texto, respuesta,"Atención", test_id))
        page.snack_bar = ft.SnackBar(ft.Text("Sección de Atención guardada."), bgcolor=ft.Colors.GREEN)
        page.snack_bar.open = True
        page.go("/test_memoria")
        page.update()
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
def test_viewMEMORIA(page: ft.Page,test_id):
    def guardar_respuestas(e):
        respuestas_memoria = [memoria_radiogroup1.value,memoria_radiogroup2.value,memoria_radiogroup3.value,memoria_radiogroup4.value,memoria_radiogroup5.value]
        for i, pregunta_texto in enumerate(preguntas_memoria):
            respuesta = respuestas_memoria[i]
            preguntaCREATE((pregunta_texto, respuesta, "Memoria", test_id))
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

def test_viewSOCIAL(page: ft.Page, test_id):

    def guardar_respuestas(e):
        respuestas_social = [social_radiogroup1.value,social_radiogroup2.value,social_radiogroup3.value,social_radiogroup4.value,social_radiogroup5.value]
        for i, pregunta_texto in enumerate(preguntas_social):
            respuesta = respuestas_social[i]
            preguntaCREATE((pregunta_texto, respuesta, "Social", test_id))
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

def test_viewEMOCIONAL(page: ft.Page, test_id):
    def guardar_respuestas(e):
        respuestas_emocional = [emocional_radiogroup1.value,emocional_radiogroup2.value,emocional_radiogroup3.value,emocional_radiogroup4.value,emocional_radiogroup5.value]
        for i, pregunta_texto in enumerate(preguntas_emocional):
            respuesta = respuestas_emocional[i]
            preguntaCREATE((pregunta_texto, respuesta, "Emocional", test_id))
        page.snack_bar = ft.SnackBar(ft.Text("Test finalizado y respuestas guardadas."), bgcolor=ft.Colors.GREEN)
        page.snack_bar.open = True
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

def iniciar_test(page: ft.Page, es_nameID: int, pro_nameID: int):
    page.clean()
    page.title = "Neuro Check - Test"
    page.bgcolor = color_Background
    test_id = testCREATE((es_nameID, pro_nameID))

    def route_change(e: ft.RouteChangeEvent):
        print(f"Cambiando a la ruta: {e.route}")
        page.views.clear()
        page.views.append(test_viewATENCION(page,test_id))
        if  page.route == "/test_memoria":
            page.views.append(test_viewMEMORIA(page, test_id))
        elif page.route == "/test_social":
            page.views.append(test_viewSOCIAL(page, test_id))
        elif page.route == "/test_emocional":
            page.views.append(test_viewEMOCIONAL(page, test_id))
        page.update()
    
    def view_pop(e: ft.ViewPopEvent):
        print(f"Cerrando vista: {e.view}")
        page.views.pop()
        if page.views:
            top_view = page.views[-1]
            page.go(top_view.route)
        else:
            page.go("/")
            page.update()

    page.on_route_change = route_change
    page.on_view_pop = view_pop


    page.go("/test_atencion")
