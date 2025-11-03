import flet as ft
from modelo.modelo import AppModel
from vista.vista_inicio import InicioView
from vista.vista_real_test import RealizarTestView
from vista.vista_login import LoginView
from vista.vista_test import TestView
from vista.vista_resultados import ResultadosView
from vista.vista_inicio_pie import InicioPIEView
from vista.vista_perfil_docente import PerfilDocenteView

from controlador.ctrl_inicio import InicioController
from controlador.ctrl_real_test import RealizarTestController
from controlador.ctrl_login import LoginController
from controlador.ctrl_inicio_pie import InicioPIEController
from controlador.ctrl_test import TestController
from controlador.ctrl_resultados import ResultadosController
from controlador.ctrl_perfil_docente import PerfilDocenteController


from colors import color_Docente, color_Background_Docente

def create_appbar(page, view_title_control, back_handler, model):
    back_button = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        on_click=lambda _: back_handler(None), 
        visible=False 
    )
    return ft.AppBar(
        leading=back_button,
        leading_width=40,
        title=ft.TextButton(
            content=ft.Text("Neuro Check", size=25, weight=ft.FontWeight.BOLD, color="white"),
            on_click=lambda _: page.go("/inicio_pie") if model.datos_profesor.pro_cargo == 1 else page.go("/inicio_profesor")
        ),
        bgcolor=color_Docente,
        center_title=False,
        actions=[
            ft.Row([
                view_title_control, # El control de título dinámico
                ft.PopupMenuButton(items=[
                    ft.PopupMenuItem(
                        icon=ft.Icons.EXIT_TO_APP,
                        text="Cerrar sesión",
                    ),
                ])
            ]),
        ]
    )


def main(page, model: AppModel): # main ahora recibe el modelo
    page.title = "NeuroCheck"
    view_title = ft.Text("", color="white", size=20)
    
    def view_pop(view):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)
        elif page.route == "/perfil_docente":
            if hasattr(model, 'datos_profesor') and model.datos_profesor:
                if model.datos_profesor.pro_cargo == 1:
                    page.go("/inicio_pie")
                else:
                    page.go("/inicio_profesor")
        elif page.route.startswith("/test/"):
            page.go("/realizar_test")
        elif page.route == "/modificacion_docente":
            page.go("/inicio_pie")
        elif page.route == "/realizar_test":
            if hasattr(model, 'datos_profesor') and model.datos_profesor:
                if model.datos_profesor.pro_cargo == 1:
                    page.go("/inicio_pie")
                else:
                    page.go("/inicio_profesor")
        elif page.route == "/resultados_detallados":
            page.go("/inicio_profesor")
        elif page.route == "/inicio_profesor":            
            page.go("/")

   
    login_controller = LoginController(page, model)
    inicio_controller = InicioController(page, model)
    inicio_pie_controller = InicioPIEController(page, model)
    real_test_controller = RealizarTestController(page, model) # <--- CORRECCIÓN: Usar el modelo principal
    test_controller = TestController(page, model)
    perfil_docente_controller = PerfilDocenteController(page, model)
    resultados_controller = ResultadosController(page, model)
    
    login_view = LoginView(login_controller, model)
    inicio_view = InicioView(inicio_controller, model)
    inicio_pie_view = InicioPIEView(inicio_pie_controller, model)
    rel_test_view = RealizarTestView(real_test_controller, model)
    test_view = TestView(test_controller, model)
    resultados_view = ResultadosView(resultados_controller, model)
    perfil_docente_view = PerfilDocenteView(perfil_docente_controller, model)
    
    login_controller.view = login_view
    inicio_controller.view = inicio_view
    inicio_pie_controller.view = inicio_pie_view
    real_test_controller.view = rel_test_view
    test_controller.view = test_view
    resultados_controller.view = resultados_view
    perfil_docente_controller.view = perfil_docente_view
    
    def route_change(route):
        print(f"Cambiando a la ruta: {page.route}")
        page.views.clear() 
        troute = ft.TemplateRoute(page.route)
        current_view = None

        if troute.match("/"):
            view_title.value = "Inicio de Sesión"
            login_view.content.appbar = None 
            current_view = login_view.content
        
        elif troute.match("/inicio_profesor"):
            view_title.value = "Inicio Docente"
            inicio_view.content.appbar = create_appbar(page, view_title, view_pop, model)
            if hasattr(model, 'datos_profesor') and model.datos_profesor:
                nombre_profesor = f"{model.datos_profesor.pro_nombre_1}" # Accedemos al nombre desde el modelo
                inicio_view.welcome_text.value = nombre_profesor # Actualizamos el texto de bienvenida
            current_view = inicio_view.content

        elif troute.match("/inicio_pie"):
            view_title.value = "Inicio PIE"
            inicio_pie_view.content.appbar = create_appbar(page, view_title, view_pop, model)
            if hasattr(model, 'datos_profesor') and model.datos_profesor:
                nombre_profesor = f"{model.datos_profesor.pro_nombre_1}"
                inicio_pie_view.welcome_text.value = nombre_profesor
            current_view = inicio_pie_view.content
        
        elif troute.match("/realizar_test"):
            view_title.value = "Realizar test"
            rel_test_view.content.appbar = create_appbar(page, view_title, view_pop, model)
            real_test_controller.cargar_estudiantes()
            real_test_controller.cargar_test_incompletos()
            current_view = rel_test_view.content

        elif troute.match("/perfil_docente"):
            view_title.value = "Perfil Docente"
            perfil_docente_view.content.appbar = create_appbar(page, view_title, view_pop, model)
            perfil_docente_controller.cargar_datos_docente() # Cargar datos en la tabla
            perfil_docente_controller.cargar_tests_completados() # Cargar tests del docente
            current_view = perfil_docente_view.content
        
        elif troute.match("/test/:test_id"): # Cambia la ruta para aceptar un ID
            view_title.value = "Test"
            test_view.content.appbar = create_appbar(page, view_title, view_pop, model)
            test_controller.cargar_respuestas_guardadas(int(troute.test_id))
            current_view = test_view.content

        elif troute.match("/resultados/:test_id"):
            view_title.value = "Resultados del Test"
            resultados_view.content.appbar = create_appbar(page, view_title, view_pop, model)
            resultados_controller.calcular_resultados(int(troute.test_id))
            current_view = resultados_view.content

    
        if current_view:
            page.views.append(current_view)
            current_appbar = current_view.appbar
            if current_appbar and hasattr(current_appbar, 'leading') and current_appbar.leading:
                current_appbar.leading.visible = page.route != "/inicio_profesor"

        page.update()

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    if model.datos_profesor.pro_cargo == 1:
        page.go("/inicio_pie")
    else:
        page.go("/inicio_profesor") 


if __name__ == "__main__":
    def main_standalone(page: ft.Page):
        model = AppModel()
        test_profesor_data = model.cargar_profesor_id(1)
        if test_profesor_data:
            model.datos_profesor = test_profesor_data
        main(page, model)

    ft.app(target=main_standalone, assets_dir="assets",view=ft.AppView.FLET_APP)
