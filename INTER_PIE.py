import flet as ft

def create_inicio_view(page: ft.Page):
    """Crea y devuelve la vista de Inicio para el profesional PIE."""
    return ft.View(
        "/inicio_pie",
        [
            ft.AppBar(title=ft.Text("Neuro Check - Módulo PIE"), bgcolor=ft.colors.BLUE_GREY),
            ft.Text("¡Bienvenido, Profesional PIE!", size=30, weight=ft.FontWeight.BOLD),
            ft.ElevatedButton("Ver resultados de estudiantes", on_click=lambda _: page.go("/resultados")),
            ft.ElevatedButton("Gestionar Estudiantes", on_click=lambda _: page.go("/estudiantes")),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )

def create_resultados_view(page: ft.Page):
    """Crea y devuelve la vista de Resultados."""
    return ft.View(
        "/resultados",
        [
            ft.AppBar(title=ft.Text("Resultados"), bgcolor=ft.colors.BLUE_GREY),
            ft.Text("Aquí se mostrarán los resultados de los tests.", style=ft.TextThemeStyle.BODY_MEDIUM),
            # Aquí iría la lógica para mostrar una tabla o lista de resultados.
            ft.ElevatedButton("Volver a Inicio", on_click=lambda _: page.go("/inicio_pie")),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )

def create_estudiantes_view(page: ft.Page):
    """Crea y devuelve la vista para gestionar estudiantes."""
    return ft.View(
        "/estudiantes",
        [
            ft.AppBar(title=ft.Text("Gestión de Estudiantes"), bgcolor=ft.colors.BLUE_GREY),
            ft.Text("Aquí se podrán gestionar los estudiantes.", style=ft.TextThemeStyle.BODY_MEDIUM),
            # Aquí iría la lógica para añadir, editar o ver estudiantes.
            ft.ElevatedButton("Volver a Inicio", on_click=lambda _: page.go("/inicio_pie")),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )

def main(page: ft.Page):
    page.title = "Módulo PIE - Neuro Check"
    page.theme_mode = ft.ThemeMode.LIGHT

    def route_change(e):
        print(f"Cambiando a la ruta: {e.route}")
        page.views.clear()

        # Vista base que siempre está presente
        page.views.append(create_inicio_view(page))

        # Apilar vistas adicionales según la ruta
        if page.route == "/resultados":
            page.views.append(create_resultados_view(page))
        elif page.route == "/estudiantes":
            page.views.append(create_estudiantes_view(page))

        page.update()

    def view_pop(e):
        print(f"Cerrando vista: {e.view}")
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # Iniciar en la ruta base para el profesional PIE
    page.go("/inicio_pie")


if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, assets_dir="assets")