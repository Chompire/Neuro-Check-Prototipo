import flet as ft
from flet_mvc import FletView

from colors import color_Docente, color_Background_Docente


class InicioView(FletView):  # Heredamos de BaseView
    def __init__(self, controller, model):
        self.welcome_text = ft.Text(size=30, weight=ft.FontWeight.NORMAL, color="black")
        view = ft.View(
            "/inicio_profesor", # La ruta URL para esta vista
            bgcolor=color_Background_Docente,
            controls=[
                ft.Container(
                    expand=True,  # El contenido principal se expande
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            ft.Column(
                                expand=True,
                                scroll=ft.ScrollMode.AUTO,
                                controls=[
                                    ft.Text("¡Bienvenido/a!", size=50, weight=ft.FontWeight.BOLD, color="black"),
                                    self.welcome_text, # Usamos el control ya creado
                                    ft.Text("", size=20, weight=ft.FontWeight.BOLD, color="black"),
                                    ft.Container(
                                        content=ft.Text(
                                            "¿Qué desea hacer?",
                                            size=25,
                                            weight=ft.FontWeight.BOLD,
                                            color="black",
                                        ),
                                        width=600,
                                    ),
                                    ft.Card(
                                        elevation=0,
                                        color=color_Docente,
                                        content=ft.Container(
                                            content=ft.Column([
                                                ft.ListTile(
                                                    title=ft.Text("Realizar test", size=20, weight=ft.FontWeight.BOLD),
                                                    subtitle=ft.Text(
                                                        "El test sirve para obtener el porcentaje de riesgo del estudiante para posiblemente derivarlo al equipo PIE.",
                                                        size=15
                                                    ),
                                                ),
                                                # La navegación se debe hacer a través del controlador
                                                ft.ElevatedButton(text="Entrar", color="black", bgcolor=color_Background_Docente, on_click=lambda _: controller.page.go("/realizar_test"))
                                            ]),
                                            width=600,
                                            padding=10,
                                        )
                                    ),
                                    ft.Card(
                                        color=color_Docente,
                                        content=ft.Container(
                                            content=ft.Column([
                                                ft.ListTile(
                                                    title=ft.Text("Perfil docente", size=20, weight=ft.FontWeight.BOLD),
                                                    subtitle=ft.Text(
                                                        "Puedes ver tu información personal y revisar los resultados de los tests.",
                                                        size=15
                                                    ),
                                                ),
                                                ft.ElevatedButton(
                                                    text="Entrar",
                                                    color="black",
                                                    bgcolor=color_Background_Docente,
                                                    on_click=lambda _: controller.page.go("/perfil_docente")
                                                )
                                            ]),
                                            width=600,
                                            padding=10
                                        )
                                    ),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=15
                            )
                        ]
                    )
                ),
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        super().__init__(model, view, controller)