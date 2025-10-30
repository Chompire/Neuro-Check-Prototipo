import flet as ft
from flet_mvc import FletView
from colors import color_Background, color_Docente

class ResultadosView(FletView):
    def __init__(self, controller, model):
        # --- Controles dinámicos ---
        self.porcentaje_val = ft.Text("0%", size=40, weight=ft.FontWeight.BOLD, color="black")
        self.save_snackbar = ft.SnackBar(content=ft.Text(""), bgcolor=ft.colors.GREEN)

        # --- Diálogos de confirmación ---
        self.rework_alert = ft.AlertDialog(
            modal=True,
            title=ft.Text("Rehacer test"),
            content=ft.Text("¿Desea rehacer este test? Las respuestas actuales se borrarán."),
            actions=[
                ft.TextButton("Sí", on_click=controller.rehacer_test),
                ft.TextButton("No", on_click=lambda e: controller.cerrar_dialogo('rehacer')),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.delete_alert = ft.AlertDialog(
            modal=True,
            title=ft.Text("Eliminar test"),
            content=ft.Text("¿Está seguro? Esta acción no se puede deshacer."),
            actions=[
                ft.TextButton("Sí, eliminar", on_click=controller.eliminar_test, style=ft.ButtonStyle(color=ft.colors.RED)),
                ft.TextButton("Cancelar", on_click=lambda e: controller.cerrar_dialogo('eliminar')),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # --- Botones de acción ---
        guardar_button = ft.IconButton(
            icon=ft.icons.SAVE, icon_color=ft.colors.WHITE, bgcolor=ft.colors.BLUE,
            tooltip="Guardar resultados y finalizar", on_click=controller.guardar_test
        )
        rehacer_button = ft.IconButton(
            icon=ft.icons.REFRESH, icon_color=ft.colors.WHITE, bgcolor=ft.colors.ORANGE,
            tooltip="Rehacer test", on_click=lambda e: controller.abrir_dialogo('rehacer')
        )
        eliminar_button = ft.IconButton(
            icon=ft.icons.DELETE, icon_color=ft.colors.WHITE, bgcolor=ft.colors.RED,
            tooltip="Eliminar test", on_click=lambda e: controller.abrir_dialogo('eliminar')
        )

        view = ft.View(
            "/resultados",
            bgcolor=color_Background,
            controls=[
                self.save_snackbar,
                self.rework_alert,
                self.delete_alert,
                ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text("Porcentaje de riesgo:", size=30, weight=ft.FontWeight.BOLD, color="black"),
                        ft.Container(
                            width=600,
                            alignment=ft.alignment.center,
                            border=ft.border.all(1, ft.colors.BLACK),
                            bgcolor=ft.colors.WHITE,
                            padding=10,
                            content=self.porcentaje_val
                        ),
                        ft.Row(
                            controls=[guardar_button, rehacer_button, eliminar_button],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                    ]
                )
            ]
        )
        super().__init__(model, view, controller)
