import flet as ft
from flet_mvc import FletView
from colors import color_Docente, color_Background

class InicioPIEView(FletView):
    def __init__(self, controller, model):
        self.welcome_text = ft.Text(size=30, weight=ft.FontWeight.NORMAL, color="black")

        view = ft.View(
            "/inicio_pie",
            bgcolor=color_Background,
            controls=[
                ft.Container(
                    expand=True,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            ft.Column(
                                expand=True,
                                scroll=ft.ScrollMode.AUTO,
                                controls=[
                                    ft.Text("¡Bienvenido/a, Profesional PIE!", size=40, weight=ft.FontWeight.BOLD, color="black"),
                                    self.welcome_text,
                                    ft.Text("", size=20, weight=ft.FontWeight.BOLD, color="black"),
                                    ft.Container(
                                        content=ft.Text("¿Qué desea hacer?", size=25, weight=ft.FontWeight.BOLD, color="black"),
                                        width=600,
                                    ),
                                    # Card para Realizar Test
                                    ft.Card(
                                        elevation=0, color=color_Docente,
                                        content=ft.Container(
                                            content=ft.Column([
                                                ft.ListTile(
                                                    title=ft.Text("Realizar test", size=20, weight=ft.FontWeight.BOLD),
                                                    subtitle=ft.Text("Acceder a la selección de estudiantes para iniciar o reanudar un test.", size=15),
                                                ),
                                                ft.ElevatedButton(text="Entrar", color="black", bgcolor=color_Background, on_click=lambda _: controller.page.go("/realizar_test"))
                                            ]),
                                            width=600, padding=10,
                                        )
                                    ),
                                    # Card para Perfil
                                    ft.Card(
                                        color=color_Docente,
                                        content=ft.Container(
                                            content=ft.Column([
                                                ft.ListTile(
                                                    title=ft.Text("Perfil", size=20, weight=ft.FontWeight.BOLD),
                                                    subtitle=ft.Text("Ver tu información personal y los resultados de los tests finalizados.", size=15),
                                                ),
                                                ft.ElevatedButton(text="Entrar", color="black", bgcolor=color_Background, on_click=lambda _: controller.page.go("/perfil_docente"))
                                            ]),
                                            width=600, padding=10
                                        )
                                    ),
                                    # Card para Modificación de Docentes
                                    ft.Card(
                                        color=color_Docente,
                                        content=ft.Container(
                                            content=ft.Column([
                                                ft.ListTile(
                                                    title=ft.Text("Gestión de Docentes", size=20, weight=ft.FontWeight.BOLD),
                                                    subtitle=ft.Text("Añadir, editar o eliminar la información de los docentes del sistema.", size=15),
                                                ),
                                                ft.ElevatedButton(text="Entrar", color="black", bgcolor=color_Background, on_click=lambda _: controller.page.go("/modificacion_docente"))
                                            ]),
                                            width=600, padding=10
                                        )
                                    ),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15
                            )
                        ]
                    )
                ),
            ],
        )
        super().__init__(model, view, controller)