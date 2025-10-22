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
    test_id = preguntaREAD((ID_test))
    
    atencion_res = 0
    memoria_res = 0
    social_res = 0
    emocional_res = 0
    for pregunta in test_id:
        if pregunta[1] == "Atención":
            if pregunta[0] == "si":
                atencion_res += 1
            elif pregunta[0] == "no" or pregunta[0] is None:
                atencion_res += 0
            else:
                atencion_res += 0
        elif pregunta[1] == "Memoria":
            if pregunta[0] == "si":
                memoria_res += 1
            elif pregunta[0] == "no" or pregunta[0] is None:
                memoria_res += 0
            else:
                memoria_res += 0
        elif pregunta[1] == "Social":
            if pregunta[0] == "si":
                social_res += 1
            elif pregunta[0] == "no" or pregunta[0] is None:
                social_res += 0
            else:
                social_res += 0
        elif pregunta[1] == "Emocional":
            if pregunta[0] == "si":
                emocional_res += 1
            elif pregunta[0] == "no" or pregunta[0] is None:
                emocional_res += 0
            else:
                emocional_res += 0

    
    puntaje = atencion_res + memoria_res + social_res + emocional_res
    porcentaje = (puntaje / 20) * 100
    print(f"{porcentaje}%")



    def route_change(e: ft.RouteChangeEvent):
       print(f"Cambiando a la ruta: {e.route}")
       page.views.clear()
       page.views.append(resultado(page,test_id, porcentaje))
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
        id_profesor_pie_test = 29
        ver_resultados(page, id_profesor_pie_test)

    ft.app(target=main_standalone, assets_dir="assets",view=ft.AppView.FLET_APP)