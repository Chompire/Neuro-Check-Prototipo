from flet_mvc import FletController

class InicioController(FletController):
    prof_id = None
    def __init__(self, page, model):
        super().__init__(page, model)

    def go_realizar_test(self, e):
        self.page.go("/realizar_test")

    def go_perfil_docente(self, e):
        self.page.go("/mi_perfil")