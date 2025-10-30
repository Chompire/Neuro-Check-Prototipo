from flet_mvc import FletController
import flet as ft

class TestController(FletController):
    def __init__(self, page, model):
        super().__init__(page, model)
        self.current_test_id = None # Para almacenar el ID del test actual

    def load_test(self, test_id: str):
        try:
            self.current_test_id = int(test_id)
            print(f"TestController: Cargando test con ID: {self.current_test_id}")
            
        except ValueError:
            print(f"Error: ID de test inválido recibido: {test_id}")
            # Manejar el error, por ejemplo, redirigir o mostrar un mensaje
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error: ID de test inválido: {test_id}"), open=True, bgcolor=ft.colors.RED_700)
            self.page.update()