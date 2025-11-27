from flet_mvc import FletController
import flet as ft

class TestController(FletController):
    def __init__(self, page, model):
        super().__init__(page, model)
        self.current_test_id = None

    @staticmethod
    def create_radio_groups(count: int):
        return [
            ft.RadioGroup(
                content=ft.Row([
                    ft.Radio(value="si", label="Sí", label_style=ft.TextStyle(color="black")),
                    ft.Radio(value="no", label="No", label_style=ft.TextStyle(color="black")),
                ])
            ) for _ in range(count)
        ]
    @staticmethod
    def crear_contenido_tab(respuestas, radiogroups):
            controles = []
            for i, respuesta in enumerate(respuestas):
                controles.append(ft.Text(respuesta, size=20, weight=ft.FontWeight.BOLD, color="black"))
                controles.append(radiogroups[i])
            return ft.Column(controls=controles, spacing=10, scroll=ft.ScrollMode.AUTO)
    
    def cargar_preguntas(self, pre_id: int):
        preguntas = self.model.leer_preguntas(pre_id)
        print(preguntas)

    def cargar_respuestas_guardadas(self, test_id: int):
        respuestas_existentes = self.model.leer_respuestas(test_id)
        mapa_radiogroups = {
            "Atención": self.view.radiogroups_atencion,
            "Memoria": self.view.radiogroups_memoria,
            "Social": self.view.radiogroups_social,
            "Emocional": self.view.radiogroups_emocional,
        }
        for groups in mapa_radiogroups.values():
            for rg in groups:
                rg.value = None

        for _, respuesta_combinada, tipo in respuestas_existentes:
            if tipo in mapa_radiogroups:
                radiogroups = mapa_radiogroups[tipo]
                if respuesta_combinada:
                    respuestas_individuales = respuesta_combinada.split(',')
                    for i, respuesta in enumerate(respuestas_individuales):
                        if i < len(radiogroups):
                            radiogroups[i].value = None if respuesta == 'None' else respuesta

        self.current_test_id = test_id 
        print(f"Respuestas cargadas para el test ID {test_id}")
        self.page.update()


    def guardar_respuestas(self, e: ft.ControlEvent):
        if self.current_test_id is None:
            self.page.snack_bar = ft.SnackBar(ft.Text("Error: No se pudo obtener el ID del test para guardar las respuestas."), open=True, bgcolor=ft.Colors.RED)
            self.page.update()
            return
        
        test_id = self.current_test_id
        respuestas_existentes = self.model.leer_respuestas(test_id)
        
        mapa_radiogroups = {
            "Atención": self.view.radiogroups_atencion,
            "Memoria": self.view.radiogroups_memoria,
            "Social": self.view.radiogroups_social,
            "Emocional": self.view.radiogroups_emocional,
        }

        for id_respuesta, _, tipo in respuestas_existentes:
            if tipo in mapa_radiogroups:
                respuestas = [rg.value for rg in mapa_radiogroups[tipo]]
                respuesta_combinada = ",".join(str(r) for r in respuestas)
                self.model.actualizar_respuesta(id_respuesta, {"res_respuesta": respuesta_combinada})
                print(f"Guardada respuesta combinada para la categoría '{tipo}' en la respuesta ID {id_respuesta}")
        
        self.view.error_snack_bar.content = ft.Text("Respuestas guardadas correctamente.")
        self.view.error_snack_bar.bgcolor = ft.Colors.YELLOW
        self.view.error_snack_bar.open = True
        self.page.update()

    def finalizar_test(self, e):
        self.guardar_respuestas(e)
        mapa_radiogroups = {
            "Atención": self.view.radiogroups_atencion,
            "Memoria": self.view.radiogroups_memoria,
            "Social": self.view.radiogroups_social,
            "Emocional": self.view.radiogroups_emocional,
        }

        todas_respondidas = True
        for categoria, groups in mapa_radiogroups.items():
            for rg in groups:
                if rg.value is None:
                    todas_respondidas = False
                    break
            if not todas_respondidas:
                break

        if todas_respondidas:
            self.page.go(f"/resultados/{self.current_test_id}")
        else:
            self.view.error_snack_bar.content = ft.Text("Advertencia: No todas las preguntas fueron respondidas. Guardando progreso.")
            self.view.error_snack_bar.bgcolor = ft.Colors.YELLOW
            self.view.error_snack_bar.open = True
            self.page.update()