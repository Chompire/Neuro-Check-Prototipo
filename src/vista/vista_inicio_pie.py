import flet as ft
from flet_mvc import FletView
from colors import color_Docente, color_Background_PIE

class InicioPIEView(FletView):
    def __init__(self, controller, model):
        self.welcome_text = ft.Text(size=30, weight=ft.FontWeight.NORMAL, color="black")

        view = ft.View(
            "/inicio_pie",
            bgcolor=color_Background_PIE,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                
                ft.ResponsiveRow(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            col={"sm": 12, "md": 10, "lg": 8},
                            content=ft.Column(
                                expand=True,
                                scroll=ft.ScrollMode.AUTO,
                                controls=[
                                    ft.Text("¡Bienvenido/a, Profesional PIE!", size=40, weight=ft.FontWeight.BOLD, color="black"),
                                    self.welcome_text,
                                    ft.Text("", size=20, weight=ft.FontWeight.BOLD, color="black"),
                                    ft.Container(
                                        content=ft.Text("¿Qué desea hacer?", size=25, weight=ft.FontWeight.BOLD, color="black"),
                                    ),
                                    ft.Card(
                                        elevation=0, color=color_Docente,
                                        content=ft.Container(
                                            content=ft.Column([
                                                ft.ListTile(
                                                    title=ft.Text("Realizar test", size=20, weight=ft.FontWeight.BOLD),
                                                    subtitle=ft.Text("Acceder a la selección de estudiantes para iniciar o reanudar un test.", size=15),
                                                ),
                                                ft.ElevatedButton(text="Entrar", color="black", bgcolor=color_Background_PIE, on_click=lambda _: controller.page.go("/realizar_test"))
                                            ]),
                                            padding=10,
                                        )
                                    ),
                                    ft.Card(
                                        color=color_Docente,
                                        content=ft.Container(
                                            content=ft.Column([
                                                ft.ListTile(
                                                    title=ft.Text("Mi Perfil", size=20, weight=ft.FontWeight.BOLD),
                                                    subtitle=ft.Text("Ver tu información personal y los resultados de los tests finalizados.", size=15),
                                                ),
                                                ft.ElevatedButton(text="Entrar", color="black", bgcolor=color_Background_PIE, on_click=lambda _: controller.page.go("/perfil_docente"))
                                            ]),
                                            padding=10
                                        )
                                    ),
                                    ft.Card(
                                        color=color_Docente,
                                        content=ft.Container(
                                            content=ft.Column([
                                                ft.ListTile(
                                                    title=ft.Text("Mis tests", size=20, weight=ft.FontWeight.BOLD),
                                                    subtitle=ft.Text(
                                                        "Revisa los resultados de los tests que has finalizado.",
                                                        size=15
                                                    ),
                                                ),
                                                ft.ElevatedButton(
                                                    text="Entrar",
                                                    color="black",
                                                    bgcolor=color_Background_PIE,
                                                    on_click=lambda _: controller.page.go("/mis_tests")
                                                )
                                            ]),
                                            padding=10
                                        )
                                    ),
                                    ft.Card(
                                        color=color_Docente,
                                        content=ft.Container(
                                            content=ft.Column([
                                                ft.ListTile(
                                                    title=ft.Text("Gestión", size=20, weight=ft.FontWeight.BOLD),
                                                    subtitle=ft.Text("Añadir, editar o eliminar la información de los docentes del sistema y alumnos que ya no estan matriculados.", size=15),
                                                ),
                                                ft.ElevatedButton(text="Entrar", color="black", bgcolor=color_Background_PIE, on_click=lambda _: controller.page.go("/gestion"))
                                            ]),
                                            padding=10
                                        )
                                    ),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15
                            )
                        )
                    ]
                ),
            ],
        )
        super().__init__(model, view, controller)