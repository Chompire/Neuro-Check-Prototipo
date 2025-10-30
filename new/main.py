import flet as ft
from modelo.modelo import LoginAppModel, EstudiantesAppModel
from vista.vista_inicio import InicioView
from vista.vista_real_test import RealizarTestView
from vista.vista_login import LoginView
from vista.vista_test import TestView
from controlador.ctrl_inicio import InicioController
from controlador.ctrl_real_test import RealizarTestController
from controlador.ctrl_login import LoginController
from controlador.ctrl_test import Test
from colors import color_Docente, color_Background
def create_appbar(page, view_title_control, back_handler):
    """Crea y devuelve una nueva instancia de ft.AppBar para cada vista."""
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
            on_click=lambda _: page.go("/inicio_profesor")
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


def main(page):
    page.title = "App MVC con Rutas"
    page.bgcolor = color_Background
    view_title = ft.Text("", color="white", size=20)
    
    def view_pop(view):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)
        
        elif page.route.startswith("/test/"):
            page.go("/realizar_test")

        elif page.route == "/realizar_test":
            page.go("/inicio_profesor") 
  
        elif page.route == "/inicio_profesor":            
            page.go("/")

    # Inicialización de MVC
    model = LoginAppModel()
    model_estudiantes = EstudiantesAppModel()
    
    login_controller = LoginController(page, model)
    inicio_controller = InicioController(page, model)
    real_test_controller = RealizarTestController(page, model) # <--- CORRECCIÓN: Usar el modelo principal
    test_controller = Test(page, model)
    
    # Obtener el contenido View de cada vista
    login_view = LoginView(login_controller, model)
    inicio_view = InicioView(inicio_controller, model)
    rel_test_view = RealizarTestView(real_test_controller, model)
    test_view = TestView(test_controller, model)
    
    # Asociar vistas con sus controladores
    login_controller.view = login_view
    inicio_controller.view = inicio_view
    real_test_controller.view = rel_test_view
    test_controller.view = test_view
    


    # --- 2. Lógica de enrutamiento (GESTIÓN DE PILA CORRECTA) ---
    def route_change(route):
        print(f"Cambiando a la ruta: {page.route}")
        page.views.clear() 
        troute = ft.TemplateRoute(page.route)
        current_view = None
        
        # === VISTA DE LOGIN (Ruta base principal) ===
        if troute.match("/"):
            view_title.value = "Inicio de Sesión"
            page.bgcolor = color_Background
            # La vista de login no tiene AppBar
            login_view.content.appbar = None 
            current_view = login_view.content

        
        elif troute.match("/inicio_profesor"):
            view_title.value = "Inicio Docente"
            page.bgcolor = color_Background
            inicio_view.content.appbar = create_appbar(page, view_title, view_pop)
            # Actualizamos el texto de bienvenida con el nombre del profesor
            if hasattr(model, 'datos_profesor') and model.datos_profesor:
                nombre_profesor = f"{model.datos_profesor.pro_nombre_1}"
                
                inicio_view.welcome_text.value = nombre_profesor
            current_view = inicio_view.content
        
        elif troute.match("/realizar_test"):
            view_title.value = "Realizar test"
            page.bgcolor = color_Background
            rel_test_view.content.appbar = create_appbar(page, view_title, view_pop)
            real_test_controller.cargar_estudiantes()
            real_test_controller.cargar_test_incompletos()
            current_view = rel_test_view.content

        elif troute.match("/test/:test_id"): # Cambia la ruta para aceptar un ID
            test_id = troute.test_id # Se accede al parámetro como un atributo
            test_controller.load_test(test_id) # Llama a un nuevo método en TestController
            view_title.value = "Test"
            page.bgcolor = color_Background
            test_view.content.appbar = create_appbar(page, view_title, view_pop)
            current_view = test_view.content
    
        if current_view:
            page.views.append(current_view)
            current_appbar = current_view.appbar
            if current_appbar and current_appbar.leading:
                current_appbar.leading.visible = page.route != "/inicio_profesor"

        page.update()

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go("/") 


# Es importante usar ft.AppView.FLET_APP para que el enrutamiento funcione correctamente.
ft.app(target=main, view=ft.AppView.FLET_APP)
