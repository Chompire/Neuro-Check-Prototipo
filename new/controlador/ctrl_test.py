from flet_mvc import FletController
import flet as ft

class TestController(FletController):
    def __init__(self, page, model):
        super().__init__(page, model)
        self.current_test_id = None # Initialize an attribute to store the test_id

    @staticmethod
    def create_radio_groups(count: int):
        """Crea una lista de RadioGroup."""
        return [
            ft.RadioGroup(
                content=ft.Row([
                    ft.Radio(value="si", label="Sí"),
                    ft.Radio(value="no", label="No"),
                ])
            ) for _ in range(count)
        ]
    @staticmethod
    def crear_contenido_tab(preguntas, radiogroups):
            controles = []
            for i, pregunta in enumerate(preguntas):
                controles.append(ft.Text(pregunta, size=20, weight=ft.FontWeight.BOLD, color="black"))
                controles.append(radiogroups[i])
            return ft.Column(controls=controles, spacing=10)

    def cargar_respuestas_guardadas(self, test_id: int):
        preguntas_existentes = self.model.leer_preguntas(test_id)
        respuestas_por_tipo = {"Atención": [], "Memoria": [], "Social": [], "Emocional": []}
        for _, pre_respuesta, pre_tipo in preguntas_existentes:
            if pre_tipo in respuestas_por_tipo:
                respuestas_por_tipo[pre_tipo].append(pre_respuesta)

        # Mapear tipos a los grupos de radio buttons de la vista
        mapa_radiogroups = {
            "Atención": self.view.radiogroups_atencion,
            "Memoria": self.view.radiogroups_memoria,
            "Social": self.view.radiogroups_social,
            "Emocional": self.view.radiogroups_emocional,
        }
        for tipo, respuestas in respuestas_por_tipo.items():
            radiogroups = mapa_radiogroups.get(tipo)
            if radiogroups:
                for i, respuesta in enumerate(respuestas):
                    if i < len(radiogroups):
                        radiogroups[i].value = respuesta # Asigna la respuesta (puede ser 'si', 'no', o None)
        self.current_test_id = test_id 
        print(f"Respuestas cargadas para el test ID {test_id}")
        self.page.update()


    def guardar_respuestas(self, e: ft.ControlEvent):
        """
        Guarda todas las respuestas de los RadioGroups en la vista del test.
        """
        if self.current_test_id is None:
            # Handle the case where test_id was not set (e.g., if the view was accessed incorrectly)
            self.page.snack_bar = ft.SnackBar(ft.Text("Error: No se pudo obtener el ID del test para guardar las respuestas."), open=True, bgcolor=ft.colors.RED)
            self.page.update()
            return
        
        test_id = self.current_test_id # Use the stored test_id
        preguntas_existentes = self.model.leer_preguntas(test_id)  # Agrupar preguntas por tipo
        preguntas_por_tipo = {"Atención": [], "Memoria": [], "Social": [], "Emocional": []}
        for pre_id, _, pre_tipo in preguntas_existentes:
            if pre_tipo in preguntas_por_tipo:
                preguntas_por_tipo[pre_tipo].append(pre_id)
        mapa_radiogroups = {
            "Atención": self.view.radiogroups_atencion,
            "Memoria": self.view.radiogroups_memoria,
            "Social": self.view.radiogroups_social,
            "Emocional": self.view.radiogroups_emocional,
        }
        
        for tipo, ids_preguntas in preguntas_por_tipo.items():
            for i, id_pregunta in enumerate(ids_preguntas):
                if i < len(mapa_radiogroups[tipo]):
                    respuesta = mapa_radiogroups[tipo][i].value
                    if respuesta is not None:
                        self.model.actualizar_pregunta(id_pregunta, {"pre_respuesta": respuesta})
                        print(f"Guardada respuesta '{respuesta}' para la pregunta ID {id_pregunta}")
        
        self.page.snack_bar = ft.SnackBar(ft.Text("Respuestas guardadas correctamente."), open=True, bgcolor=ft.colors.GREEN)
        self.page.update()

    def finalizar_test(self, e):
        # Primero, guardar las respuestas actuales
        self.guardar_respuestas(e)

        # Verificar si todas las preguntas están respondidas
        preguntas = self.model.leer_preguntas(self.current_test_id)
        if not all(p.pre_respuesta is not None for p in preguntas):
            self.page.snack_bar = ft.SnackBar(ft.Text("Advertencia: No todas las preguntas fueron respondidas."), open=True, bgcolor=ft.colors.AMBER)
            self.page.update()
        
        # Navegar a la vista de resultados
        self.page.go(f"/resultados/{self.current_test_id}")