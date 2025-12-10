import flet as ft
from flet_mvc import FletView
from colors import color_Docente, color_Background_Docente, color_Background_PIE

class TestView(FletView):
    def __init__(self, controller, model):
        self.error_snack_bar = ft.SnackBar(content = ft.Text(""))

        def get_pregunta_text(pre_id, index):
            pregunta = controller.model.leer_preguntas(pre_id)
            if pregunta:
                return f"{index}. {pregunta[0][1]}"
            return f"{index}. (Error al cargar pregunta)"

        preguntas_atencion = [
            ft.Text(get_pregunta_text(1, 1), selectable=True),
            ft.Text(get_pregunta_text(2, 2), selectable=True),
            ft.Text(get_pregunta_text(3, 3), selectable=True),
            ft.Text(get_pregunta_text(4, 4), selectable=True),
            ft.Text(get_pregunta_text(5, 5), selectable=True),
            ft.Text(get_pregunta_text(6, 6), selectable=True),
            ft.Text(get_pregunta_text(7, 7), selectable=True),
            ft.Text(get_pregunta_text(8, 8), selectable=True),
            ft.Text(get_pregunta_text(9, 9), selectable=True),
            ft.Text(get_pregunta_text(10, 10), selectable=True),
        ]
        preguntas_memoria = [
            ft.Text(get_pregunta_text(11, 1), selectable=True),
            ft.Text(get_pregunta_text(12, 2), selectable=True),
            ft.Text(get_pregunta_text(13, 3), selectable=True),
            ft.Text(get_pregunta_text(14, 4), selectable=True),
            ft.Text(get_pregunta_text(15, 5), selectable=True),
            ft.Text(get_pregunta_text(16, 6), selectable=True),
            ft.Text(get_pregunta_text(17, 7), selectable=True),
            ft.Text(get_pregunta_text(18, 8), selectable=True),
            ft.Text(get_pregunta_text(19, 9), selectable=True),
            ft.Text(get_pregunta_text(20, 10), selectable=True),
        ]
        preguntas_social = [
            ft.Text(get_pregunta_text(21, 1), selectable=True),
            ft.Text(get_pregunta_text(22, 2), selectable=True),
            ft.Text(get_pregunta_text(23, 3), selectable=True),
            ft.Text(get_pregunta_text(24, 4), selectable=True),
            ft.Text(get_pregunta_text(25, 5), selectable=True),
            ft.Text(get_pregunta_text(26, 6), selectable=True),
            ft.Text(get_pregunta_text(27, 7), selectable=True),
            ft.Text(get_pregunta_text(28, 8), selectable=True),
            ft.Text(get_pregunta_text(29, 9), selectable=True),
            ft.Text(get_pregunta_text(30, 10), selectable=True),
        ]
        preguntas_emocional = [
            ft.Text(get_pregunta_text(31, 1), selectable=True),
            ft.Text(get_pregunta_text(32, 2), selectable=True),
            ft.Text(get_pregunta_text(33, 3), selectable=True),
            ft.Text(get_pregunta_text(34, 4), selectable=True),
            ft.Text(get_pregunta_text(35, 5), selectable=True),
            ft.Text(get_pregunta_text(36, 6), selectable=True),
            ft.Text(get_pregunta_text(37, 7), selectable=True),
            ft.Text(get_pregunta_text(38, 8), selectable=True),
            ft.Text(get_pregunta_text(39, 9), selectable=True),
            ft.Text(get_pregunta_text(40, 10), selectable=True),
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