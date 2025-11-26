import flet as ft
import os
import socket
from zeroconf import ServiceInfo, Zeroconf
from modelo.modelo import AppModel
from vista.vista_inicio import InicioView
from vista.vista_real_test import RealizarTestView
from vista.vista_login import LoginView
from vista.vista_test import TestView
from vista.vista_resultados import ResultadosView
from vista.vista_inicio_pie import InicioPIEView
from vista.vista_perfil_docente import PerfilDocenteView
from vista.vista_resultados_detallados import ResultadosDetalladosView
from vista.vista_modificacion_docente import ModificacionDocenteView
from vista.vista_export_pdf import ExportPDFView
from vista.vista_mis_tests import MisTestsView
from vista.vista_cambiar_password import CambiarPasswordView
from vista.vista_notificaciones import NotificacionesView
from controlador.ctrl_inicio import InicioController
from controlador.ctrl_real_test import RealizarTestController
from controlador.ctrl_login import LoginController
from controlador.ctrl_inicio_pie import InicioPIEController
from controlador.ctrl_test import TestController
from controlador.ctrl_resultados import ResultadosController
from controlador.ctrl_perfil_docente import PerfilDocenteController
from controlador.ctrl_modificacion_docente import ModificacionDocenteController
from controlador.ctrl_resultados_detallados import ResultadosDetalladosController
from controlador.ctrl_export_pdf import ExportPDFController
from controlador.ctrl_mis_tests import MisTestsController
from controlador.ctrl_notificaciones import NotificacionesController
from controlador.ctrl_cambiar_password import CambiarPasswordController
from colors import color_Docente, color_Background_Docente, color_Background_PIE

def create_appbar(page, view_title_control, back_handler, model, logout_handler, route_change_handler):
    back_button = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        on_click=lambda _: back_handler(None), 
        visible=False 
    )
    has_unread = False
    if model.datos_profesor and model.datos_profesor.pro_cargo == 1:
        prof_id = model.datos_profesor.pro_nameID
        notificaciones = model.leer_notificaciones(prof_id=prof_id, solo_no_leidas=True)
        has_unread = bool(notificaciones)
    popup_items = []
    if model.datos_profesor and model.datos_profesor.pro_cargo == 1:
        popup_items.append(
            ft.PopupMenuItem(
                content=ft.Row([
                    ft.Icon(ft.Icons.NOTIFICATIONS),
                    ft.Text("Notificaciones"),
                    ft.CircleAvatar(radius=4, bgcolor=ft.Colors.RED, visible=has_unread),
                ]),
                on_click=lambda _: page.go("/notificaciones")
            )
        )
    popup_items.append(
        ft.PopupMenuItem(
            icon=ft.Icons.PASSWORD,
            text="Cambiar contraseña",
            on_click=lambda _: page.go("/cambiar_contrasena")
        )
    )
    popup_items.append(
        ft.PopupMenuItem(
            icon=ft.Icons.EXIT_TO_APP,
            text="Cerrar sesión",
            on_click=logout_handler
        )
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
                view_title_control,
                ft.PopupMenuButton(items=popup_items)
            ]),
        ]
    )

def create_footer():
    return ft.Container(
        content=ft.Row(
            [ft.Text("© 2024 Neuro Check. Desarrollado por Benjamín Saavedra.", color=ft.colors.with_opacity(0.6, "black"), size=12)],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        padding=ft.padding.only(top=10, bottom=5),
    )

def main(page: ft.Page, model: AppModel):
    page.title = "Neuro Check"
    view_title = ft.Text("", color="white", size=20)

    def logout(e):
        if model.datos_profesor:
            prof_id = model.datos_profesor.pro_nameID
            model.actualizar_profesor(prof_id, {"pro_online_state": 0})
        page.client_storage.remove("profesor_id")
        model.datos_profesor = None
        page.views.clear()
        page.go("/")
    
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
        elif page.route == "/gestion":
            page.go("/inicio_pie")
        elif page.route == "/realizar_test":
            if hasattr(model, 'datos_profesor') and model.datos_profesor:
                if model.datos_profesor.pro_cargo == 1:
                    page.go("/inicio_pie")
                else:
                    page.go("/inicio_profesor")
        elif page.route.startswith("/resultados_detallados/"):
            page.go("/mis_tests") 
        elif page.route.startswith("/export_pdf/"):
            page.go(f"/resultados_detallados/{export_pdf_controller.res_det_id}")
        elif page.route == "/mis_tests":
            if hasattr(model, 'datos_profesor') and model.datos_profesor:
                if model.datos_profesor.pro_cargo == 1:
                    page.go("/inicio_pie")
                else:
                    page.go("/inicio_profesor")
        elif page.route == "/notificaciones":
            if hasattr(model, 'datos_profesor') and model.datos_profesor:
                if model.datos_profesor.pro_cargo == 1:
                    page.go("/inicio_pie")
        elif page.route == "/cambiar_contrasena":
            if hasattr(model, 'datos_profesor') and model.datos_profesor:
                if model.datos_profesor.pro_cargo == 1:
                    page.go("/inicio_pie")
                else:
                    page.go("/inicio_profesor")
    
    login_controller = LoginController(page, model)
    inicio_controller = InicioController(page, model)
    inicio_pie_controller = InicioPIEController(page, model)
    real_test_controller = RealizarTestController(page, model)
    test_controller = TestController(page, model)
    perfil_docente_controller = PerfilDocenteController(page, model)
    resultados_controller = ResultadosController(page, model)
    resultados_detallados_controller = ResultadosDetalladosController(page, model)
    modificacion_docente_controller = ModificacionDocenteController(page, model)
    export_pdf_controller = ExportPDFController(page, model)
    mis_tests_controller = MisTestsController(page, model)
    notificaciones_controller = NotificacionesController(page, model)
    cambiar_password_controller = CambiarPasswordController(page, model)

    login_view = LoginView(login_controller, model)
    inicio_view = InicioView(inicio_controller, model)
    inicio_pie_view = InicioPIEView(inicio_pie_controller, model)
    rel_test_view = RealizarTestView(real_test_controller, model)
    test_view = TestView(test_controller, model)
    resultados_view = ResultadosView(resultados_controller, model)
    perfil_docente_view = PerfilDocenteView(perfil_docente_controller, model)
    resultados_detallados_view = ResultadosDetalladosView(resultados_detallados_controller, model)
    modificacion_docente_view = ModificacionDocenteView(modificacion_docente_controller, model)
    export_pdf_view = ExportPDFView(export_pdf_controller, model)
    mis_tests_view = MisTestsView(mis_tests_controller, model)
    notificaciones_view = NotificacionesView(notificaciones_controller, model)
    cambiar_password_view  = CambiarPasswordView(cambiar_password_controller, model)    
    
    login_controller.view = login_view
    inicio_controller.view = inicio_view
    inicio_pie_controller.view = inicio_pie_view
    real_test_controller.view = rel_test_view
    test_controller.view = test_view
    resultados_controller.view = resultados_view
    perfil_docente_controller.view = perfil_docente_view
    resultados_detallados_controller.view = resultados_detallados_view
    modificacion_docente_controller.view = modificacion_docente_view
    export_pdf_controller.view = export_pdf_view
    mis_tests_controller.view = mis_tests_view
    notificaciones_controller.view = notificaciones_view
    cambiar_password_controller.view = cambiar_password_view
    def route_change(route):
        print(f"Cambiando a la ruta: {page.route}")
        page.views.clear() 
        current_view = None
        troute = ft.TemplateRoute(page.route)
        profesor_id_storage = page.client_storage.get("profesor_id")
        
        if profesor_id_storage:
            if not model.datos_profesor or model.datos_profesor.pro_nameID != profesor_id_storage:
                print(f"Restaurando sesión para el profesor ID: {profesor_id_storage}")
                if model.cargar_profesor_por_id(profesor_id_storage):
                    model.actualizar_profesor(profesor_id_storage, {"pro_online_state": 1})
        else:
            model.datos_profesor = None
        if not model.datos_profesor and page.route != "/":
             page.go("/")
             return

        if troute.match("/"):
            if model.datos_profesor:
                if model.datos_profesor.pro_cargo == 1:
                    page.go("/inicio_pie")
                else:
                    page.go("/inicio_profesor")
                return 
            else:
                view_title.value = "Inicio de Sesión"
                login_view.content.appbar = None
                current_view = login_view.content
                current_view.controls[0].controls.append(create_footer())
        
        elif troute.match("/inicio_profesor"):
            view_title.value = "Inicio Docente"
            inicio_view.content.appbar = create_appbar(page, view_title, view_pop, model, logout, route_change)
            if hasattr(model, 'datos_profesor') and model.datos_profesor and model.datos_profesor.pro_cargo == 1:
                inicio_view.content.bgcolor = color_Background_PIE
            else:
                inicio_view.content.bgcolor = color_Background_Docente
            if hasattr(model, 'datos_profesor') and model.datos_profesor:
                nombre_profesor = f"{model.datos_profesor.pro_nombre_1}"
                inicio_view.welcome_text.value = nombre_profesor
            current_view = inicio_view.content

        elif troute.match("/inicio_pie"):
            view_title.value = "Inicio PIE"
            inicio_pie_view.content.appbar = create_appbar(page, view_title, view_pop, model, logout, route_change)
            if hasattr(model, 'datos_profesor') and model.datos_profesor and model.datos_profesor.pro_cargo == 1:
                inicio_pie_view.content.bgcolor = color_Background_PIE
            else:
                inicio_pie_view.content.bgcolor = color_Background_Docente
            if hasattr(model, 'datos_profesor') and model.datos_profesor:
                nombre_profesor = f"{model.datos_profesor.pro_nombre_1}"
                inicio_pie_view.welcome_text.value = nombre_profesor
            current_view = inicio_pie_view.content
        
        elif troute.match("/realizar_test"):
            view_title.value = "Realizar test"
            rel_test_view.content.appbar = create_appbar(page, view_title, view_pop, model, logout, route_change)
            if hasattr(model, 'datos_profesor') and model.datos_profesor and model.datos_profesor.pro_cargo == 1:
                rel_test_view.content.bgcolor = color_Background_PIE
            else:
                rel_test_view.content.bgcolor = color_Background_Docente
            real_test_controller.cargar_estudiantes()
            real_test_controller.cargar_test_incompletos()
            current_view = rel_test_view.content

        elif troute.match("/perfil_docente"):
            view_title.value = "Mi Perfil"
            perfil_docente_view.content.appbar = create_appbar(page, view_title, view_pop, model, logout, route_change)

            if hasattr(model, 'datos_profesor') and model.datos_profesor and model.datos_profesor.pro_cargo == 1:
                perfil_docente_view.content.bgcolor = color_Background_PIE
            else:
                perfil_docente_view.content.bgcolor = color_Background_Docente
            perfil_docente_controller.cargar_datos_docente()
            perfil_docente_controller.cargar_estadisticas_cursos_encuestados()
            current_view = perfil_docente_view.content
        
        elif troute.match("/test/:test_id"):
            view_title.value = "Test"
            test_view.content.appbar = create_appbar(page, view_title, view_pop, model, logout, route_change)
            if hasattr(model, 'datos_profesor') and model.datos_profesor and model.datos_profesor.pro_cargo == 1:
                test_view.content.bgcolor = color_Background_PIE
            else:
                test_view.content.bgcolor = color_Background_Docente
            test_controller.cargar_respuestas_guardadas(int(troute.test_id))
            current_view = test_view.content

        elif troute.match("/resultados/:test_id"):
            view_title.value = "Resultados del Test"
            resultados_view.content.appbar = create_appbar(page, view_title, view_pop, model, logout, route_change)
            if hasattr(model, 'datos_profesor') and model.datos_profesor and model.datos_profesor.pro_cargo == 1:
                resultados_view.content.bgcolor = color_Background_PIE
            else:
                resultados_view.content.bgcolor = color_Background_Docente
            resultados_controller.calcular_resultados(int(troute.test_id))
            current_view = resultados_view.content
                    
        elif troute.match("/resultados_detallados/:det_id"):
            view_title.value = "Resultados detallados"
            resultados_detallados_view.content.appbar = create_appbar(page, view_title, view_pop, model, logout, route_change)
            if hasattr(model, 'datos_profesor') and model.datos_profesor and model.datos_profesor.pro_cargo == 1:
                resultados_detallados_view.content.bgcolor = color_Background_PIE
            else:
                resultados_detallados_view.content.bgcolor = color_Background_Docente
            is_pie = hasattr(model, 'datos_profesor') and model.datos_profesor and model.datos_profesor.pro_cargo == 1
            resultados_detallados_view.pie_controls_container.visible = is_pie
            resultados_detallados_view.observaciones_field.visible = is_pie
            resultados_detallados_controller.cargar_resultados_detallados(int(troute.det_id))
            current_view = resultados_detallados_view.content

        elif troute.match("/gestion"):
            view_title.value = "Gestión"
            modificacion_docente_view.content.appbar = create_appbar(page, view_title, view_pop, model, logout, route_change)
            modificacion_docente_controller.load_profesores_to_table()
            modificacion_docente_controller.initialize_view()
            modificacion_docente_controller.load_cursos_to_table()
            current_view = modificacion_docente_view.content

        elif troute.match("/export_pdf/:res_det_id"):
            view_title.value = "Exportar PDF"
            export_pdf_view.content.appbar = create_appbar(page, view_title, view_pop, model, logout, route_change)
            export_pdf_controller.cargar_alumno(int(troute.res_det_id))
            current_view = export_pdf_view.content

        elif troute.match("/mis_tests"):
            view_title.value = "Mis tests"
            mis_tests_view.content.appbar = create_appbar(page, view_title, view_pop, model, logout, route_change)
            if hasattr(model, 'datos_profesor') and model.datos_profesor and model.datos_profesor.pro_cargo == 1:
                mis_tests_view.content.bgcolor = color_Background_PIE
            else:
                mis_tests_view.content.bgcolor = color_Background_Docente
            mis_tests_controller.cargar_tests_completados()
            if model.datos_profesor.pro_cargo == 1:
                mis_tests_view.tests_profesores_title.visible = True
                mis_tests_view.test_profesores_table.visible = True
                mis_tests_view.pagination_controls_otros.visible = True
                mis_tests_controller.cargar_test_profesores()
            current_view = mis_tests_view.content
        
        elif troute.match("/cambiar_contrasena"):
            view_title.value = "Cambiar contraseña"
            cambiar_password_view.content.appbar = create_appbar(page, view_title, view_pop, model, logout, route_change)
            if hasattr(model, 'datos_profesor') and model.datos_profesor and model.datos_profesor.pro_cargo == 1:
                cambiar_password_view.content.bgcolor = color_Background_PIE
                cambiar_password_view.guardar_button.bgcolor = color_Background_PIE
            else:
                cambiar_password_view.content.bgcolor = color_Background_Docente
                cambiar_password_view.guardar_button.bgcolor = color_Background_Docente
            current_view = cambiar_password_view.content

        elif troute.match("/notificaciones"):
            view_title.value = "Notificaciones"
            notificaciones_view.content.appbar = create_appbar(page, view_title, view_pop, model, logout, route_change)
            notificaciones_controller.cargar_notificaciones()
            current_view = notificaciones_view.content

        if current_view:
            page.views.append(current_view)
            current_appbar = current_view.appbar
            if current_appbar and hasattr(current_appbar, 'leading'):
                is_home_view = page.route in ["/inicio_profesor", "/inicio_pie"]
                current_appbar.leading.visible = not is_home_view
            
            # Añadir el footer a todas las vistas excepto al login (que se maneja por separado)
            if page.route != "/":
                original_controls = current_view.controls
                current_view.controls = [
                    ft.Column(controls=original_controls, expand=True, scroll=current_view.scroll),
                    create_footer()
                ]
                current_view.scroll = None # El scroll ahora lo maneja la columna interna
        page.update()

    def on_resize(e):
        page.update()

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.on_resize = on_resize
    page.go("/")
    page.update()
if __name__ == "__main__":
    APP_PORT = 8000
    APP_NAME = "neurocheck"
    
    def main_standalone(page: ft.Page):
            model = AppModel()
            main(page, model)
        
    assets_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets"))
    zeroconf = Zeroconf()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()

        desc = {'path': '/'}
        info = ServiceInfo(
            "_http._tcp.local.",
            f"{APP_NAME}._http._tcp.local.",
            addresses=[socket.inet_aton(local_ip)],
            port=APP_PORT,
            properties=desc,
            server=f"{APP_NAME}.local.",
        )
        zeroconf.register_service(info)
        ft.app(target=main_standalone, assets_dir=assets_path, view=ft.AppView.WEB_BROWSER, port=APP_PORT, host="0.0.0.0")
    finally:
        print(f"Dejando de anunciar el servicio '{APP_NAME}'.")
        zeroconf.close()