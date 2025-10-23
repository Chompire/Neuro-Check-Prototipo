import flet as ft
from CRUD import preguntaREAD
color_Background = "#FF7F7F"


def resultado(page: ft.Page, test_id, porcentaje):  
    guardar_button = ft.IconButton(icon=ft.Icons.SAVE, icon_color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE)
    rehacer_button = ft.IconButton(icon=ft.Icons.REFRESH, icon_color=ft.Colors.WHITE, bgcolor=ft.Colors.RED)
    info_button = ft.IconButton(icon=ft.Icons.INFO, icon_color=ft.Colors.WHITE, bgcolor=ft.Colors.GREEN)
    porcentaje_val = ft.Text(f"{porcentaje}%",size=40, weight=ft.FontWeight.BOLD, color="black")
    return ft.View(
        route="/resultados",
        bgcolor=color_Background,
        controls=[
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

def ver_resultados(page: ft.Page, ID_test: int):
    page.clean()
    page.title = "Neuro Check - Test"
    page.bgcolor = color_Background
    page.route = "/resultados"
    
    preguntas_del_test = preguntaREAD(ID_test)
    print("Preguntas del test:",preguntas_del_test)

    atencion_res = 0
    memoria_res = 0
    social_res = 0
    emocional_res = 0
    total_preguntas_respondidas = 0

    for pregunta in preguntas_del_test:
        print(pregunta)
        total_preguntas_respondidas += 1
        if pregunta[3] == "Atención":
            if pregunta[2] == "si":
                atencion_res += 1
        elif pregunta[3] == "Memoria":
            if pregunta[2] == "si":
                memoria_res += 1
        elif pregunta[3] == "Social":
            if pregunta[2] == "si":
                social_res += 1
        elif pregunta[3] == "Emocional":
            if pregunta[2] == "si":
                emocional_res += 1

    print(f"Atención: {atencion_res}")
    print(f"Memoria: {memoria_res}")
    print(f"Social: {social_res}")
    print(f"Emocional: {emocional_res}")
    puntaje = atencion_res + memoria_res + social_res + emocional_res
    
    # Calcular porcentaje dinámicamente basado en el número de preguntas respondidas
    porcentaje = (puntaje / total_preguntas_respondidas) * 100 if total_preguntas_respondidas > 0 else 0
    print(f"{porcentaje}%")


    def route_change(e: ft.RouteChangeEvent):
       print(f"Cambiando a la ruta: {e.route}")
       page.views.clear()
       page.views.append(resultado(page, ID_test, porcentaje))
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
        id_profesor_pie_test = 72
        ver_resultados(page, id_profesor_pie_test)

    ft.app(target=main_standalone, assets_dir="assets",view=ft.AppView.FLET_APP)