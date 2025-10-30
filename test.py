import flet as ft
from CRUD import testCREATE, preguntaCREATE, preguntaREAD, preguntaUPDATE, testREAD,testUPDATE
import datetime
import time
color_Background = "#FF7F7F"
color_Docente = "#FF0000"
def create_app_bar(page: ft.Page, title: str):
    return ft.AppBar(
        title=ft.TextButton(
            content=ft.Text("Neuro Check", size=25, weight=ft.FontWeight.BOLD, color="white"),
            on_click=lambda _: page.go("/seleccionar_estudiante")
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
def view_test(page: ft.Page,test_id, id_atencion, id_memoria, id_social, id_emocional, respuestas_atencion=None, respuestas_memoria=None, respuestas_social=None, respuestas_emocional=None):
    error_snack_bar = ft.SnackBar(content = ft.Text(""), bgcolor=ft.Colors.GREEN)
    preguntas_atencion = [
        "1. ¿El estudiante se distrae con facilidad en clases?",
        "2. ¿Le cuesta mantener la atención en tareas o actividades lúdicas?",
        "3. ¿Parece no escuchar cuando se le habla directamente?",
        "4. ¿Evita, le disgusta o es renuente a dedicarse a tareas que requieren un esfuerzo mental sostenido?",
        "5. ¿A menudo pierde cosas necesarias para tareas o actividades?"
    ]
    preguntas_memoria = [
        "1. ¿Olvida con frecuencia información recién aprendida?",
        "2. ¿Tiene dificultad para recordar eventos o encargos importantes?",
        "3. ¿Necesita que le repitan las instrucciones varias veces?",
        "4. ¿Le cuesta seguir una conversación o una historia larga?",
        "5. ¿Confunde nombres, fechas o lugares con frecuencia?"
    ]
    preguntas_social = [
        "1. ¿Le cuesta iniciar o mantener una conversación con sus compañeros?",
        "2. ¿Prefiere jugar solo en lugar de en grupo?",
        "3. ¿Tiene dificultades para entender las reglas de los juegos en grupo?",
        "4. ¿Le resulta difícil interpretar las emociones de los demás (expresiones faciales, tono de voz)?",
        "5. ¿Comparte sus juguetes o materiales con otros niños de forma reacia?"
    ]
    preguntas_emocional = [
        "1. ¿Tiene rabietas o explosiones de ira frecuentes o intensas?",
        "2. ¿Se muestra a menudo ansioso, preocupado o temeroso sin una razón aparente?",
        "3. ¿Parece triste, desanimado o irritable la mayor parte del tiempo?",
        "4. ¿Le cuesta calmarse después de una situación estresante o frustrante?",
        "5. ¿Reacciona de forma exagerada a críticas o comentarios negativos?"
    ]

    def manejar_respuestas(e, accion: str, ids_atencion, ids_memoria, ids_social, ids_emocional):
       
        respuestas_atencion = [rg.value for rg in radiogroups_atencion]
        respuestas_memoria = [rg.value for rg in radiogroups_memoria]
        respuestas_social = [rg.value for rg in radiogroups_social]
        respuestas_emocional = [rg.value for rg in radiogroups_emocional]
        
        
        for i, _ in enumerate(preguntas_atencion):
            preguntaUPDATE(ids_atencion[i], {"pre_respuesta": respuestas_atencion[i]})
        for i, _ in enumerate(preguntas_memoria):
            preguntaUPDATE(ids_memoria[i], {"pre_respuesta": respuestas_memoria[i]})
        for i, _ in enumerate(preguntas_social):
            preguntaUPDATE(ids_social[i], {"pre_respuesta": respuestas_social[i]})
        for i, _ in enumerate(preguntas_emocional):
            preguntaUPDATE(ids_emocional[i], {"pre_respuesta": respuestas_emocional[i]})
        if accion == "guardar":
            
            error_snack_bar.content = ft.Text("Respuestas guardadas (Puede salir de la ventana).")
            error_snack_bar.open = True # Regresa al menú
        
        elif accion == "finalizar":
            todas_las_preguntas = preguntaREAD(test_id)
            test_completo = all(pregunta[1] is not None for pregunta in todas_las_preguntas)
            if test_completo:
                from resultados import ver_resultados
                error_snack_bar.content = ft.Text("Test finalizado")
                error_snack_bar.bgcolor = ft.Colors.GREEN
                error_snack_bar.open = True
                page.update()        
                time.sleep(2)

                testUPDATE(test_id, {"test_status": 1}) 
                ver_resultados(page, test_id)
            else:
                error_snack_bar.content = ft.Text("Advertencia: No todas las preguntas fueron respondidas. Guardando progreso.")
                error_snack_bar.bgcolor = ft.Colors.YELLOW
                error_snack_bar.open = True
        
        page.update()



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
    
    radiogroups_atencion = [atencion_radiogroup1, atencion_radiogroup2, atencion_radiogroup3, atencion_radiogroup4, atencion_radiogroup5]
    radiogroups_memoria = [memoria_radiogroup1, memoria_radiogroup2, memoria_radiogroup3, memoria_radiogroup4, memoria_radiogroup5]
    radiogroups_social = [social_radiogroup1, social_radiogroup2, social_radiogroup3, social_radiogroup4, social_radiogroup5]
    radiogroups_emocional = [emocional_radiogroup1, emocional_radiogroup2, emocional_radiogroup3, emocional_radiogroup4, emocional_radiogroup5]

    if respuestas_atencion:
        for i, rg in enumerate(radiogroups_atencion):
            if i < len(respuestas_atencion):
                rg.value = respuestas_atencion[i]

    if respuestas_memoria:
        for i, rg in enumerate(radiogroups_memoria):
            if i < len(respuestas_memoria):
                rg.value = respuestas_memoria[i]

    if respuestas_social:
        for i, rg in enumerate(radiogroups_social):
            if i < len(respuestas_social):
                rg.value = respuestas_social[i]

    if respuestas_emocional:
        for i, rg in enumerate(radiogroups_emocional):
            if i < len(respuestas_emocional):
                rg.value = respuestas_emocional[i]

    column = ft.Column(
        
        controls=[
            ft.Text("Atención", size=30, weight=ft.FontWeight.BOLD, color="black"),
            ft.Text(preguntas_atencion[0], size=20, weight=ft.FontWeight.BOLD, color="black"), atencion_radiogroup1,
            ft.Text(preguntas_atencion[1], size=20, weight=ft.FontWeight.BOLD, color="black"), atencion_radiogroup2,
            ft.Text(preguntas_atencion[2], size=20, weight=ft.FontWeight.BOLD, color="black"), atencion_radiogroup3,
            ft.Text(preguntas_atencion[3], size=20, weight=ft.FontWeight.BOLD, color="black"), atencion_radiogroup4,
            ft.Text(preguntas_atencion[4], size=20, weight=ft.FontWeight.BOLD, color="black"), atencion_radiogroup5,
            ft.Divider(color="black", thickness=2),
            ft.Text("Memoria", size=30, weight=ft.FontWeight.BOLD, color="black"),
            ft.Text(preguntas_memoria[0], size=20, weight=ft.FontWeight.BOLD, color="black"), memoria_radiogroup1,
            ft.Text(preguntas_memoria[1], size=20, weight=ft.FontWeight.BOLD, color="black"), memoria_radiogroup2,
            ft.Text(preguntas_memoria[2], size=20, weight=ft.FontWeight.BOLD, color="black"),memoria_radiogroup3,
            ft.Text(preguntas_memoria[3], size=20, weight=ft.FontWeight.BOLD, color="black"), memoria_radiogroup4,
            ft.Text(preguntas_memoria[4], size=20, weight=ft.FontWeight.BOLD, color="black"), memoria_radiogroup5,
            ft.Divider(color="black", thickness=2),
            ft.Text("Social", size=30, weight=ft.FontWeight.BOLD, color="black"),
            ft.Text(preguntas_social[0], size=20, weight=ft.FontWeight.BOLD, color="black"), social_radiogroup1,
            ft.Text(preguntas_social[1], size=20, weight=ft.FontWeight.BOLD, color="black"), social_radiogroup2,
            ft.Text(preguntas_social[2], size=20, weight=ft.FontWeight.BOLD, color="black"), social_radiogroup3,
            ft.Text(preguntas_social[3], size=20, weight=ft.FontWeight.BOLD, color="black"), social_radiogroup4,
            ft.Text(preguntas_social[4], size=20, weight=ft.FontWeight.BOLD, color="black"), social_radiogroup5,
            ft.Text("Emocional", size=30, weight=ft.FontWeight.BOLD, color="black"),
            ft.Divider(color="black", thickness=2),
            ft.Text(preguntas_emocional[0], size=20, weight=ft.FontWeight.BOLD, color="black"), emocional_radiogroup1,
            ft.Text(preguntas_emocional[1], size=20, weight=ft.FontWeight.BOLD, color="black"), emocional_radiogroup2,
            ft.Text(preguntas_emocional[2], size=20, weight=ft.FontWeight.BOLD, color="black"), emocional_radiogroup3,
            ft.Text(preguntas_emocional[3], size=20, weight=ft.FontWeight.BOLD, color="black"), emocional_radiogroup4,
            ft.Text(preguntas_emocional[4], size=20, weight=ft.FontWeight.BOLD, color="black"), emocional_radiogroup5,
                ],
    )
    
    # Se usa la técnica de argumentos por defecto en lambda para capturar el valor actual de las listas de IDs
    save_button = ft.ElevatedButton("Guardar respuestas", 
                                    on_click= lambda e, ids_a=id_atencion, ids_m=id_memoria, ids_s=id_social, ids_e=id_emocional: 
                                        manejar_respuestas(e, "guardar", ids_a, ids_m, ids_s, ids_e), 
                                    bgcolor=ft.Colors.RED, color=ft.Colors.WHITE)
    
    finalizar_button = ft.ElevatedButton("Finalizar Test", 
                                         on_click=lambda e, ids_a=id_atencion, ids_m=id_memoria, ids_s=id_social, ids_e=id_emocional: 
                                             manejar_respuestas(e, "finalizar", ids_a, ids_m, ids_s, ids_e), 
                                         bgcolor=ft.Colors.RED, color=ft.Colors.WHITE)  
    return ft.View(
        route="/test",
        bgcolor=color_Background,
        controls=[
            create_app_bar(page, "Test"),
            ft.Column(
                expand=True,
                    scroll=ft.ScrollMode.AUTO,
                    spacing=20,
                    controls=[
                        error_snack_bar,
                        column,
                        ft.Row([save_button,finalizar_button]),
                ]                
            )
        ]
    )   

def iniciar_test(page: ft.Page, es_nameID, pro_nameID: int, test_id: int | None = None):
    page.clean()
    page.title = "Neuro Check - Test"
    page.bgcolor = color_Background
    id_atencion =[]
    id_memoria = []
    id_social = []
    id_emocional = []
    respuestas_atencion = []
    respuestas_memoria = []
    respuestas_social = []
    respuestas_emocional = []
    if test_id is None:
        crear_id = testCREATE((es_nameID, pro_nameID, datetime.datetime.now(), None)) # es_ID, pro_ID, fecha_inicio, fecha_termino
        print(f"Creando preguntas iniciales para el test ID: {crear_id}")
        print(f"{pro_nameID}")
        for i in range(5):
            pre_id = preguntaCREATE((None,"Atención", crear_id))
            print(f"  -> Pregunta de Atención creada con ID: {pre_id}")
            id_atencion.append(pre_id)
            
        for i in range(5):
            pre_id = preguntaCREATE((None,"Memoria", crear_id))
            print(f"  -> Pregunta de Memoria creada con ID: {pre_id}")
            id_memoria.append(pre_id)

        for i in range(5):
            pre_id = preguntaCREATE((None,"Social", crear_id))
            print(f"  -> Pregunta Social creada con ID: {pre_id}")
            id_social.append(pre_id)

        for i in range(5):
            pre_id = preguntaCREATE((None,"Emocional", crear_id))
            print(f"  -> Pregunta Emocional creada con ID: {pre_id}")
            id_emocional.append(pre_id)
    elif es_nameID is not None:
        crear_id = es_nameID
    else:
        crear_id = test_id
        print(crear_id)    
        preguntas_existentes = preguntaREAD(test_id)
        for pregunta in preguntas_existentes:
            pre_id = pregunta[0]
            pre_respuesta = pregunta[1]
            pre_tipo = pregunta[2]
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

    def route_change(e: ft.RouteChangeEvent):
        print(f"Cambiando a la ruta: {e.route}")
        page.views.clear()
        page.views.append(view_test(page,crear_id,id_atencion,id_memoria,id_social,id_emocional,respuestas_atencion,respuestas_memoria,respuestas_social,respuestas_emocional))
        
        if page.route == "/seleccionar_estudiante":
            from INTER_Profesores import mostrar_menu_principal
            if test_id is not None:
                idprolist = testREAD(test_id)
                idpro = idprolist[2]
                mostrar_menu_principal(page, pro_nameID=idpro)
            else:
                mostrar_menu_principal(page, pro_nameID)
            page.go("/seleccionar_estudiante")
        page.update()
    
    def view_pop(e: ft.ViewPopEvent):
        print(f"Cerrando vista: {e.view}")
        page.views.pop() # Elimina la vista actual
        if page.views:
            top_view = page.views[-1]
            page.go(top_view.route)
        else:
            # Si no quedan vistas, regresa a la pantalla de inicio de sesión principal
            page.go("/")
            page.update()
        

    page.on_route_change = route_change
    page.on_view_pop = view_pop


    page.go("/test")
if __name__ == "__main__":
    def main_standalone(page: ft.Page):
        iniciar_test(page, 3, 2) # Se elimina el argumento faltante

    ft.app(target=main_standalone, assets_dir="assets",view=ft.AppView.FLET_APP)