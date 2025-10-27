import flet as ft
from CRUD import preguntaREAD, preguntaUPDATE, testREAD, testUPDATE
import datetime
from INTER_Profesores import mostrar_menu_principal
import time
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
def resultado(page: ft.Page, test_id, porcentaje, id_profesor):
    save_snackbar = ft.SnackBar(content = ft.Text(""), bgcolor=ft.Colors.GREEN)
    def rehacer_test(e, test_id, pro_id):
        testUPDATE(test_id, {"test_status": 0})
        from test import iniciar_test
        preguntas_del_test = preguntaREAD(test_id)
        for pregunta in preguntas_del_test:
            preguntaUPDATE(pregunta[0], {"pre_respuesta": None})
        iniciar_test(page, es_nameID=None, pro_nameID=pro_id, test_id=test_id)

    def guardar_test(e, test_id):
        page.overlay.append(save_snackbar)
        save_snackbar.content = ft.Text("Se han guardado los resultados exitosamente.")
        save_snackbar.open = True
        page.update()
        
        time.sleep(2)

        testUPDATE(test_id, {"test_status": 1})
        testUPDATE(test_id, {"test_fecha_termino": datetime.datetime.now()})        
        
        mostrar_menu_principal(page, pro_nameID=id_profesor)

    guardar_button = ft.IconButton(icon=ft.Icons.SAVE, icon_color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE, on_click=lambda e: guardar_test(e, test_id))
    rehacer_button = ft.IconButton(icon=ft.Icons.REFRESH, icon_color=ft.Colors.WHITE, bgcolor=ft.Colors.RED, on_click=lambda e: rehacer_test(e, test_id, id_profesor))
    info_button = ft.IconButton(icon=ft.Icons.INFO, icon_color=ft.Colors.WHITE, bgcolor=ft.Colors.GREEN, on_click=lambda e: page.go("/resultados_detallados"))
    porcentaje_val = ft.Text(f"{porcentaje}%",size=40, weight=ft.FontWeight.BOLD, color="black")
    
    return ft.View(
        route="/resultados",
        bgcolor=color_Background,
        controls=[
            create_app_bar(page, "Resultados"),
            ft.Column(
                scroll=ft.ScrollMode.AUTO,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,               
                controls=[
                    ft.Row([ft.Text("Porcentaje de riesgo:", size=40, weight=ft.FontWeight.BOLD, color="black")]),
                    ft.Column(
                        width=600,
                        controls=[ft.Row([guardar_button, rehacer_button, info_button], alignment=ft.MainAxisAlignment.END),
                                      ft.Container(alignment=ft.alignment.center, border=ft.border.all(1, ft.Colors.BLACK),bgcolor=ft.Colors.WHITE, padding=10,content=porcentaje_val)
                                      ]),
                    ft.Row([ft.Text("Registro de fallas:", size=40, weight=ft.FontWeight.BOLD, color="black")]),
                    ft.Row([ft.Text("Conclusión:", size=40, weight=ft.FontWeight.BOLD, color="black")]),
            ]
        )
    ]
)
def resultados_detallados(page: ft.Page):
    return ft.View(
        route="/resultados_detallados",
        bgcolor=color_Background,
        controls=[
            create_app_bar(page, "Resultados detallados"),
        ]
    )
def ver_resultados(page: ft.Page, ID_test: int):
    page.clean()
    page.title = "Neuro Check - Test"
    page.bgcolor = color_Background
    page.route = "/resultados"    
    preguntas_del_test = preguntaREAD(ID_test)
    test_info = testREAD(ID_test)
    id_profesor = test_info[2]
    atencion_res = 0
    memoria_res = 0
    social_res = 0
    emocional_res = 0
    total_preguntas_respondidas = 0

    for pregunta in preguntas_del_test:
        total_preguntas_respondidas += 1
        if pregunta[2] == "Atención":
            if pregunta[1] == "si":
                atencion_res += 1
        elif pregunta[2] == "Memoria":
            if pregunta[1] == "si":
                memoria_res += 1
        elif pregunta[2] == "Social":
            if pregunta[1] == "si":
                social_res += 1
        elif pregunta[2] == "Emocional":
            if pregunta[1] == "si":
                emocional_res += 1
    puntaje = atencion_res + memoria_res + social_res + emocional_res   
    porcentaje = (puntaje / total_preguntas_respondidas) * 100 if total_preguntas_respondidas > 0 else 0
    print(f"{porcentaje}%")


    def route_change(e: ft.RouteChangeEvent):
        print(f"Cambiando a la ruta: {e.route}")
        page.views.clear()
        page.views.append(resultado(page, ID_test, porcentaje, id_profesor))
        if page.route == "/test":
           from test import iniciar_test
           iniciar_test(page, ID_test)
        elif page.route == "/resultados_detallados":
           page.views.append(resultados_detallados(page))
           page.go("/resultados_detallados")
        else:
           page.go("/resultados") # Navegar a la vista por defecto
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
    page.go("/resultados")

if __name__ == "__main__":
    def main_standalone(page: ft.Page):
        id_profesor_pie_test = 2
        ver_resultados(page, id_profesor_pie_test)

    ft.app(target=main_standalone, assets_dir="assets",view=ft.AppView.FLET_APP)