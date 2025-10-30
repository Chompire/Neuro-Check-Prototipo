import flet as ft
from flet_mvc import FletView
from colors import color_Docente, color_Background
class TestView(FletView):
    def __init__(self, controller, model):
        error_snack_bar = ft.SnackBar(content = ft.Text(""), bgcolor=ft.Colors.GREEN)
        preguntas_atencion = [
        "1. ¿Tiene dificultad para recordar y seguir instrucciones de más de un paso?",
        "2. ¿Olvida con frecuencia tareas, materiales o fechas importantes?",
        "3. ¿Necesita repetición constante para retener información nueva (conceptos, definiciones)?",
        "4. ¿Muestra dificultad para recordar la grafía o la forma visual de las palabras (memoria visual)?",
        "5. ¿Le cuesta aprender y recordar series o listas (días, meses, tablas de multiplicar)?",
        "6. ¿Parece tener dificultades para recuperar información ya aprendida (hechos o procedimientos)?",
        "7. ¿Confunde o mezcla información cuando debe recordar secuencias o narrativas?",
        "8. ¿Muestra una memoria a corto plazo funcional para el aprendizaje diario? (NO = dificultad)",
        "9. ¿Muestra dificultad en la memoria de trabajo, por ejemplo, al realizar cálculos mentales?",
        "10. ¿Recuerda sucesos personales o eventos pasados recientes sin dificultad? (NO = dificultad)"
    ]
        preguntas_memoria = [
        "1. ¿Tiene dificultad para recordar y seguir instrucciones de más de un paso?",
        "2. ¿Olvida con frecuencia tareas, materiales o fechas importantes?",
        "3. ¿Necesita repetición constante para retener información nueva (conceptos, definiciones)?",
        "4. ¿Muestra dificultad para recordar la grafía o la forma visual de las palabras (memoria visual)?",
        "5. ¿Le cuesta aprender y recordar series o listas (días, meses, tablas de multiplicar)?",
        "6. ¿Parece tener dificultades para recuperar información ya aprendida (hechos o procedimientos)?",
        "7. ¿Confunde o mezcla información cuando debe recordar secuencias o narrativas?",
        "8. ¿Muestra una memoria a corto plazo funcional para el aprendizaje diario? (NO = dificultad)",
        "9. ¿Muestra dificultad en la memoria de trabajo, por ejemplo, al realizar cálculos mentales?",
        "10. ¿Recuerda sucesos personales o eventos pasados recientes sin dificultad? (NO = dificultad)"
    ]
        preguntas_social = [
            "1. ¿El alumno interactúa y se relaciona de manera apropiada con sus compañeros? (NO = dificultad)",
            "2. ¿Prefiere el aislamiento o el juego en solitario de forma persistente y notable?",
            "3. ¿Muestra dificultad para comprender y seguir las normas sociales y las reglas del grupo?",
            "4. ¿Se muestra agresivo (verbal o físicamente) o irascible con frecuencia hacia sus pares?",
            "5. ¿Tiene dificultades para resolver conflictos con sus compañeros de manera verbal y pacífica?",
            "6. ¿Es capaz de trabajar en equipo, respetando turnos y compartiendo materiales? (NO = dificultad)",
            "7. ¿Muestra empatía y reconoce los sentimientos de los demás? (NO = dificultad)",
            "8. ¿Parece comprender o responder de forma inusual o limitada a las señales sociales (lenguaje corporal)?",
            "9. ¿Muestra comportamientos que desafían o se oponen a las peticiones de los adultos de forma persistente?",
            "10. ¿Busca constantemente la aprobación o atención excesiva del profesor o de sus pares?"
        ]
        preguntas_emocional = [
            "1. ¿El alumno expresa sus emociones de manera adecuada a su edad y al contexto? (NO = dificultad)",
            "2. ¿Se muestra excesivamente ansioso o preocupado por el rendimiento escolar o situaciones nuevas?",
            "3. ¿Experimenta cambios de humor repentinos o intensos que interfieren con la actividad en clase?",
            "4. ¿Muestra una baja autoestima o una actitud de autocrítica negativa constante?",
            "5. ¿Suele llorar o entristecerse fácilmente sin una causa aparente o proporcional?",
            "6. ¿Manifiesta síntomas somáticos relacionados con el estrés (dolores de cabeza o estómago recurrentes)?",
            "7. ¿Parece tener dificultades para calmarse o regularse después de una molestia o frustración?",
            "8. ¿Tiene miedos o fobias que limitan su participación en actividades escolares o sociales?",
            "9. ¿Se muestra excesivamente dependiente del profesor o de otros adultos para realizar tareas?",
            "10. ¿Muestra una motivación e interés general por el aprendizaje? (NO = dificultad)"
        ]

        # Crear 10 radio groups para cada categoría usando la función auxiliar
        self.radiogroups_atencion = controller.create_radio_groups(10)
        self.radiogroups_memoria = controller.create_radio_groups(10)
        self.radiogroups_social = controller.create_radio_groups(10)
        self.radiogroups_emocional = controller.create_radio_groups(10)
        
        # Crear el contenido para cada pestaña
        

        atencion_content = controller.crear_contenido_tab(preguntas_atencion, self.radiogroups_atencion)
        memoria_content = controller.crear_contenido_tab(preguntas_memoria, self.radiogroups_memoria)
        social_content = controller.crear_contenido_tab(preguntas_social, self.radiogroups_social)
        emocional_content = controller.crear_contenido_tab(preguntas_emocional, self.radiogroups_emocional)

        # Crear el control de pestañas
        tabs_control = ft.Tabs(
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
            bgcolor=color_Background,
            controls=[
                error_snack_bar,
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