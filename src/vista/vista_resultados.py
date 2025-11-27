import flet as ft
from flet_mvc import FletView
from colors import color_Background_Docente, color_Docente, color_Background_PIE


class ResultadosView(FletView):
    def __init__(self, controller, model):
        self.porcentaje_atencion_val= ft.Text("0%", size=20, weight=ft.FontWeight.BOLD, color="black", selectable=True)
        self.porcentaje_memoria_val = ft.Text("0%", size=20, weight=ft.FontWeight.BOLD, color="black", selectable=True)
        self.porcentaje_social_val = ft.Text("0%", size=20, weight=ft.FontWeight.BOLD, color="black", selectable=True)
        self.porcentaje_emocional_val = ft.Text("0%", size=20, weight=ft.FontWeight.BOLD, color="black", selectable=True)
        self.porcentaje_val = ft.Text("0%", size=40, weight=ft.FontWeight.BOLD, color="black", selectable=True)
        self.save_snackbar = ft.SnackBar(content=ft.Text(""), bgcolor=ft.Colors.GREEN)

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
                ft.TextButton("Sí, eliminar", on_click=controller.eliminar_test, style=ft.ButtonStyle(color=ft.Colors.RED)),
                ft.TextButton("Cancelar", on_click=lambda e: controller.cerrar_dialogo('eliminar')),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # --- Botones de acción ---
        guardar_button = ft.IconButton(
            icon=ft.Icons.SAVE, icon_color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE,
            tooltip="Guardar resultados y finalizar", on_click=controller.guardar_test
        )
        rehacer_button = ft.IconButton(
            icon=ft.Icons.REFRESH, icon_color=ft.Colors.WHITE, bgcolor=ft.Colors.ORANGE,
            tooltip="Rehacer test", on_click=lambda e: controller.abrir_dialogo('rehacer')
        )
        eliminar_button = ft.IconButton(
            icon=ft.Icons.DELETE, icon_color=ft.Colors.WHITE, bgcolor=ft.Colors.RED,
            tooltip="Eliminar test", on_click=lambda e: controller.abrir_dialogo('eliminar')
        )

        view = ft.View(
            "/resultados",
            bgcolor=color_Background_Docente,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Row([ft.Text("Inicio >", weight=ft.FontWeight.BOLD, color="black"), ft.Text("Realizar Test >", weight=ft.FontWeight.BOLD, color="black"), ft.Text("Test >", weight=ft.FontWeight.BOLD, color="black"), ft.Text("Resultados", weight=ft.FontWeight.BOLD, color=color_Docente)], alignment=ft.MainAxisAlignment.START),
                self.save_snackbar,
                self.rework_alert,
                self.delete_alert,
                ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text("IDT", size=20, weight=ft.FontWeight.BOLD, color="black", selectable=True),
                        ft.Container(
                            width=600,
                            alignment=ft.alignment.center,
                            border=ft.border.all(1, ft.Colors.BLACK),
                            bgcolor=ft.Colors.WHITE,
                            padding=10,
                            content=self.porcentaje_val
                        ),
                        ft.Row(
                            controls=[guardar_button, rehacer_button, eliminar_button],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Text("Registro de indicios:", size=20, weight=ft.FontWeight.BOLD, color="black", selectable=True),
                        ft.Container(
                            alignment=ft.alignment.center,
                            border=ft.border.all(1, ft.Colors.BLACK),
                            bgcolor=ft.Colors.WHITE,
                            padding=10,
                            content=
                            ft.Column(
                                controls=[
                                    ft.Row(wrap=True,controls=[ft.Text("Atención: ", size=20, weight=ft.FontWeight.BOLD, color="black", selectable=True), self.porcentaje_atencion_val]),
                                    ft.Row(wrap=True,controls=[ft.Text("Memoria: ", size=20, weight=ft.FontWeight.BOLD, color="black", selectable=True),self.porcentaje_memoria_val]),
                                    ft.Row(wrap=True,controls=[ft.Text("Social: ", size=20, weight=ft.FontWeight.BOLD, color="black", selectable=True),self.porcentaje_social_val]),
                                    ft.Row(wrap=True,controls=[ft.Text("Emocional: ", size=20, weight=ft.FontWeight.BOLD, color="black", selectable=True),self.porcentaje_emocional_val])
                                    ]
                            )
                        ),                        
                    ]
                )
            ]
        )
        super().__init__(model, view, controller)
