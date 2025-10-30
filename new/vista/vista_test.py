import flet as ft
from flet_mvc import FletView
from colors import color_Docente, color_Background

class TestView(FletView):
    def __init__(self, controller, model):
        error_snack_bar = ft.SnackBar(content = ft.Text(""), bgcolor=ft.Colors.GREEN)
        preguntas_atencion = [
        "1. ¿El estudiante se distrae con facilidad en clases?",
        "2. ¿Le cuesta mantener la atención en tareas o actividades lúdicas?",
        "3. ¿Parece no escuchar cuando se le habla directamente?",
        "4. ¿Evita, le disgusta o es renuente a dedicarse a tareas que requieren un esfuerzo mental sostenido?",
        "5. ¿A menudo pierde cosas necesarias para tareas o actividades?"
    ]
        preguntas_memoria = [
        "1. ¿Olvida con frecuencia información recién aprendida?",
        "2. ¿Tiene dificultad para recordar eventos o encargos importantes?",
        "3. ¿Necesita que le repitan las instrucciones varias veces?",
        "4. ¿Le cuesta seguir una conversación o una historia larga?",
        "5. ¿Confunde nombres, fechas o lugares con frecuencia?"
    ]
        preguntas_social = [
            "1. ¿Le cuesta iniciar o mantener una conversación con sus compañeros?",
            "2. ¿Prefiere jugar solo en lugar de en grupo?",
            "3. ¿Tiene dificultades para entender las reglas de los juegos en grupo?",
            "4. ¿Le resulta difícil interpretar las emociones de los demás (expresiones faciales, tono de voz)?",
            "5. ¿Comparte sus juguetes o materiales con otros niños de forma reacia?"
        ]
        preguntas_emocional = [
            "1. ¿Tiene rabietas o explosiones de ira frecuentes o intensas?",
            "2. ¿Se muestra a menudo ansioso, preocupado o temeroso sin una razón aparente?",
            "3. ¿Parece triste, desanimado o irritable la mayor parte del tiempo?",
            "4. ¿Le cuesta calmarse después de una situación estresante o frustrante?",
            "5. ¿Reacciona de forma exagerada a críticas o comentarios negativos?"
        ]

        atencion_radiogroup1 = ft.RadioGroup(content=ft.Row([
            ft.Radio(value="si", label="Sí"),
            ft.Radio(value="no", label="No"),
        ]))
        atencion_radiogroup2 = ft.RadioGroup(content=ft.Row([
            ft.Radio(value="si", label="Sí"),
            ft.Radio(value="no", label="No"),
        ]))
        atencion_radiogroup3 = ft.RadioGroup(content=ft.Row([
            ft.Radio(value="si", label="Sí"),
            ft.Radio(value="no", label="No"),
        ]))
        atencion_radiogroup4 = ft.RadioGroup(content=ft.Row([
            ft.Radio(value="si", label="Sí"),
            ft.Radio(value="no", label="No"),
        ]))
        atencion_radiogroup5 = ft.RadioGroup(content=ft.Row([
            ft.Radio(value="si", label="Sí"),
            ft.Radio(value="no", label="No"),
        ]))
        
        memoria_radiogroup1 = ft.RadioGroup(content=ft.Row([
            ft.Radio(value="si", label="Sí"),
            ft.Radio(value="no", label="No"),
        ]))
        memoria_radiogroup2 = ft.RadioGroup(content=ft.Row([
            ft.Radio(value="si", label="Sí"),
            ft.Radio(value="no", label="No"),
        ]))
        memoria_radiogroup3 = ft.RadioGroup(content=ft.Row([
            ft.Radio(value="si", label="Sí"),
            ft.Radio(value="no", label="No"),
        ]))
        memoria_radiogroup4 = ft.RadioGroup(content=ft.Row([
            ft.Radio(value="si", label="Sí"),
            ft.Radio(value="no", label="No"),
        ]))
        memoria_radiogroup5 = ft.RadioGroup(content=ft.Row([
            ft.Radio(value="si", label="Sí"),
            ft.Radio(value="no", label="No"),
        ]))

        social_radiogroup1 = ft.RadioGroup(content=ft.Row([
            ft.Radio(value="si", label="Sí"),
            ft.Radio(value="no", label="No"),
        ]))
        social_radiogroup2 = ft.RadioGroup(content=ft.Row([
            ft.Radio(value="si", label="Sí"),
            ft.Radio(value="no", label="No"),
        ]))
        social_radiogroup3 = ft.RadioGroup(content=ft.Row([
            ft.Radio(value="si", label="Sí"),
            ft.Radio(value="no", label="No"),
        ]))
        social_radiogroup4 = ft.RadioGroup(content=ft.Row([
            ft.Radio(value="si", label="Sí"),
            ft.Radio(value="no", label="No"),
        ]))
        social_radiogroup5 = ft.RadioGroup(content=ft.Row([
            ft.Radio(value="si", label="Sí"),
            ft.Radio(value="no", label="No"),
        ]))
        
        emocional_radiogroup1 = ft.RadioGroup(content=ft.Row([
            ft.Radio(value="si", label="Sí"),
            ft.Radio(value="no", label="No"),
        ]))
        emocional_radiogroup2 = ft.RadioGroup(content=ft.Row([
            ft.Radio(value="si", label="Sí"),
            ft.Radio(value="no", label="No"),
        ]))
        emocional_radiogroup3 = ft.RadioGroup(content=ft.Row([
            ft.Radio(value="si", label="Sí"),
            ft.Radio(value="no", label="No"),
        ]))
        emocional_radiogroup4 = ft.RadioGroup(content=ft.Row([
            ft.Radio(value="si", label="Sí"),
            ft.Radio(value="no", label="No"),
        ]))
        emocional_radiogroup5 = ft.RadioGroup(content=ft.Row([
            ft.Radio(value="si", label="Sí"),
            ft.Radio(value="no", label="No"),
        ]))
        
        radiogroups_atencion = [atencion_radiogroup1, atencion_radiogroup2, atencion_radiogroup3, atencion_radiogroup4, atencion_radiogroup5]
        radiogroups_memoria = [memoria_radiogroup1, memoria_radiogroup2, memoria_radiogroup3, memoria_radiogroup4, memoria_radiogroup5]
        radiogroups_social = [social_radiogroup1, social_radiogroup2, social_radiogroup3, social_radiogroup4, social_radiogroup5]
        radiogroups_emocional = [emocional_radiogroup1, emocional_radiogroup2, emocional_radiogroup3, emocional_radiogroup4, emocional_radiogroup5]
        
        column = ft.Column(        
            controls=[
                ft.Text("Atención", size=30, weight=ft.FontWeight.BOLD, color="black"),
                ft.Text(preguntas_atencion[0], size=20, weight=ft.FontWeight.BOLD, color="black"), atencion_radiogroup1,
                ft.Text(preguntas_atencion[1], size=20, weight=ft.FontWeight.BOLD, color="black"), atencion_radiogroup2,
                ft.Text(preguntas_atencion[2], size=20, weight=ft.FontWeight.BOLD, color="black"), atencion_radiogroup3,
                ft.Text(preguntas_atencion[3], size=20, weight=ft.FontWeight.BOLD, color="black"), atencion_radiogroup4,
                ft.Text(preguntas_atencion[4], size=20, weight=ft.FontWeight.BOLD, color="black"), atencion_radiogroup5,
                ft.Divider(color="black", thickness=2),
                ft.Text("Memoria", size=30, weight=ft.FontWeight.BOLD, color="black"),
                ft.Text(preguntas_memoria[0], size=20, weight=ft.FontWeight.BOLD, color="black"), memoria_radiogroup1,
                ft.Text(preguntas_memoria[1], size=20, weight=ft.FontWeight.BOLD, color="black"), memoria_radiogroup2,
                ft.Text(preguntas_memoria[2], size=20, weight=ft.FontWeight.BOLD, color="black"),memoria_radiogroup3,
                ft.Text(preguntas_memoria[3], size=20, weight=ft.FontWeight.BOLD, color="black"), memoria_radiogroup4,
                ft.Text(preguntas_memoria[4], size=20, weight=ft.FontWeight.BOLD, color="black"), memoria_radiogroup5,
                ft.Divider(color="black", thickness=2),
                ft.Text("Social", size=30, weight=ft.FontWeight.BOLD, color="black"),
                ft.Text(preguntas_social[0], size=20, weight=ft.FontWeight.BOLD, color="black"), social_radiogroup1,
                ft.Text(preguntas_social[1], size=20, weight=ft.FontWeight.BOLD, color="black"), social_radiogroup2,
                ft.Text(preguntas_social[2], size=20, weight=ft.FontWeight.BOLD, color="black"), social_radiogroup3,
                ft.Text(preguntas_social[3], size=20, weight=ft.FontWeight.BOLD, color="black"), social_radiogroup4,
                ft.Text(preguntas_social[4], size=20, weight=ft.FontWeight.BOLD, color="black"), social_radiogroup5,
                ft.Text("Emocional", size=30, weight=ft.FontWeight.BOLD, color="black"),
                ft.Divider(color="black", thickness=2),
                ft.Text(preguntas_emocional[0], size=20, weight=ft.FontWeight.BOLD, color="black"), emocional_radiogroup1,
                ft.Text(preguntas_emocional[1], size=20, weight=ft.FontWeight.BOLD, color="black"), emocional_radiogroup2,
                ft.Text(preguntas_emocional[2], size=20, weight=ft.FontWeight.BOLD, color="black"), emocional_radiogroup3,
                ft.Text(preguntas_emocional[3], size=20, weight=ft.FontWeight.BOLD, color="black"), emocional_radiogroup4,
                ft.Text(preguntas_emocional[4], size=20, weight=ft.FontWeight.BOLD, color="black"), emocional_radiogroup5,
                    ],
    )
        save_button = ft.ElevatedButton("Guardar respuestas", bgcolor=ft.Colors.RED, color=ft.Colors.WHITE)
    
        finalizar_button = ft.ElevatedButton("Finalizar Test",bgcolor=ft.Colors.RED, color=ft.Colors.WHITE)  
        view = ft.View(
            "/test",
            bgcolor=color_Background,
            controls=[
                ft.Column(
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Column(
                            expand=True,
                            scroll=ft.ScrollMode.AUTO,
                            spacing=20,
                            controls=[
                                error_snack_bar,
                                column,
                            ft.Row([save_button,finalizar_button]),
                ]                
            )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        super().__init__(model, view, controller)