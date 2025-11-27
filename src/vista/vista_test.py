import flet as ft
from flet_mvc import FletView
from colors import color_Docente, color_Background_Docente, color_Background_PIE

class TestView(FletView):
    def __init__(self, controller, model):
        self.error_snack_bar = ft.SnackBar(content = ft.Text(""))
        preguntas_atencion = [
            ft.Text(f"1. {controller.model.leer_preguntas(1)[0][1]}", selectable=True),
            ft.Text(f"2. {controller.model.leer_preguntas(2)[0][1]}", selectable=True),
            ft.Text(f"3. {controller.model.leer_preguntas(3)[0][1]}", selectable=True),
            ft.Text(f"4. {controller.model.leer_preguntas(4)[0][1]}", selectable=True),
            ft.Text(f"5. {controller.model.leer_preguntas(5)[0][1]}", selectable=True),
            ft.Text(f"6. {controller.model.leer_preguntas(6)[0][1]}", selectable=True),
            ft.Text(f"7. {controller.model.leer_preguntas(7)[0][1]}", selectable=True),
            ft.Text(f"8. {controller.model.leer_preguntas(8)[0][1]}", selectable=True),
            ft.Text(f"9. {controller.model.leer_preguntas(9)[0][1]}", selectable=True),
            ft.Text(f"10. {controller.model.leer_preguntas(10)[0][1]}", selectable=True),
        ]
        preguntas_memoria = [
            ft.Text(f"1. {controller.model.leer_preguntas(11)[0][1]}", selectable=True),
            ft.Text(f"2. {controller.model.leer_preguntas(12)[0][1]}", selectable=True),
            ft.Text(f"3. {controller.model.leer_preguntas(13)[0][1]}", selectable=True),
            ft.Text(f"4. {controller.model.leer_preguntas(14)[0][1]}", selectable=True),
            ft.Text(f"5. {controller.model.leer_preguntas(15)[0][1]}", selectable=True),
            ft.Text(f"6. {controller.model.leer_preguntas(16)[0][1]}", selectable=True),
            ft.Text(f"7. {controller.model.leer_preguntas(17)[0][1]}", selectable=True),
            ft.Text(f"8. {controller.model.leer_preguntas(18)[0][1]}", selectable=True),
            ft.Text(f"9. {controller.model.leer_preguntas(19)[0][1]}", selectable=True),
            ft.Text(f"10. {controller.model.leer_preguntas(20)[0][1]}", selectable=True),
        ]
        preguntas_social = [
            ft.Text(f"1. {controller.model.leer_preguntas(21)[0][1]}", selectable=True),
            ft.Text(f"2. {controller.model.leer_preguntas(22)[0][1]}", selectable=True),
            ft.Text(f"3. {controller.model.leer_preguntas(23)[0][1]}", selectable=True),
            ft.Text(f"4. {controller.model.leer_preguntas(24)[0][1]}", selectable=True),
            ft.Text(f"5. {controller.model.leer_preguntas(25)[0][1]}", selectable=True),
            ft.Text(f"6. {controller.model.leer_preguntas(26)[0][1]}", selectable=True),
            ft.Text(f"7. {controller.model.leer_preguntas(27)[0][1]}", selectable=True),
            ft.Text(f"8. {controller.model.leer_preguntas(28)[0][1]}", selectable=True),
            ft.Text(f"9. {controller.model.leer_preguntas(29)[0][1]}", selectable=True),
            ft.Text(f"10. {controller.model.leer_preguntas(30)[0][1]}", selectable=True),
        ]
        preguntas_emocional = [
            ft.Text(f"1. {controller.model.leer_preguntas(31)[0][1]}", selectable=True),
            ft.Text(f"2. {controller.model.leer_preguntas(32)[0][1]}", selectable=True),
            ft.Text(f"3. {controller.model.leer_preguntas(33)[0][1]}", selectable=True),
            ft.Text(f"4. {controller.model.leer_preguntas(34)[0][1]}", selectable=True),
            ft.Text(f"5. {controller.model.leer_preguntas(35)[0][1]}", selectable=True),
            ft.Text(f"6. {controller.model.leer_preguntas(36)[0][1]}", selectable=True),
            ft.Text(f"7. {controller.model.leer_preguntas(37)[0][1]}", selectable=True),
            ft.Text(f"8. {controller.model.leer_preguntas(38)[0][1]}", selectable=True),
            ft.Text(f"9. {controller.model.leer_preguntas(39)[0][1]}", selectable=True),
            ft.Text(f"10. {controller.model.leer_preguntas(40)[0][1]}", selectable=True),
        ]
        self.radiogroups_atencion = controller.create_radio_groups(10)
        self.radiogroups_memoria = controller.create_radio_groups(10)
        self.radiogroups_social = controller.create_radio_groups(10)
        self.radiogroups_emocional = controller.create_radio_groups(10)
        atencion_content = controller.crear_contenido_tab(preguntas_atencion, self.radiogroups_atencion)
        memoria_content = controller.crear_contenido_tab(preguntas_memoria, self.radiogroups_memoria)
        social_content = controller.crear_contenido_tab(preguntas_social, self.radiogroups_social)
        emocional_content = controller.crear_contenido_tab(preguntas_emocional, self.radiogroups_emocional)

        tabs_control = ft.Tabs(
            indicator_color=color_Docente, divider_color=ft.Colors.TRANSPARENT,
            unselected_label_color=ft.Colors.BLACK, label_color=color_Docente,
            overlay_color={
                ft.ControlState.HOVERED: ft.Colors.with_opacity(0.6, color_Docente),
                ft.ControlState.SELECTED: ft.Colors.with_opacity(0.5, color_Docente),
            },
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Atención",
                    content=ft.Container(content=atencion_content, padding=10),
                ),
                ft.Tab(
                    text="Memoria",
                    content=ft.Container(content=memoria_content, padding=10),
                ),
                ft.Tab(
                    text="Social",
                    content=ft.Container(content=social_content, padding=10),
                ),
                ft.Tab(
                    text="Emocional",
                    content=ft.Container(content=emocional_content, padding=10),
                ),
            ],
            expand=1,
        )

        save_button = ft.ElevatedButton("Guardar respuestas", bgcolor=ft.Colors.RED, color=ft.Colors.WHITE,on_click=controller.guardar_respuestas)
    
        finalizar_button = ft.ElevatedButton("Finalizar Test",bgcolor=ft.Colors.RED, color=ft.Colors.WHITE, on_click=controller.finalizar_test)
        view = ft.View(
            "/test",
            bgcolor=color_Background_Docente, 
            controls=[
                ft.Row([ft.Text("Inicio >", weight=ft.FontWeight.BOLD, color="black"), ft.Text("Realizar Test >", weight=ft.FontWeight.BOLD, color="black"), ft.Text("Test", weight=ft.FontWeight.BOLD, color=color_Docente)], alignment=ft.MainAxisAlignment.START),
                self.error_snack_bar,
                tabs_control,
                ft.Row(
                    [save_button, finalizar_button],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        super().__init__(model, view, controller)