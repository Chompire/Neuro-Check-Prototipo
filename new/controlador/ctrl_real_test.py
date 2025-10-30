from flet_mvc import FletController
import flet as ft
import crud as db
from datetime import datetime

class RealizarTestController(FletController):
    def __init__(self, page, model):
        super().__init__(page, model)
        self.selected_student = None
        self.id_profesor = model.datos_profesor.pro_nameID if hasattr(model, 'datos_profesor') and model.datos_profesor else None
        self.selected_test_id = None
        
    def cargar_estudiantes(self, e=None):
        self.view.estudiante_table.rows.clear()
        lista_estudiantes = db.estudiantesREAD()
        print(self.id_profesor)

        # Obtenemos el ID del profesor desde el modelo en el momento justo.
        id_profesor = self.model.datos_profesor.pro_nameID if hasattr(self.model, 'datos_profesor') and self.model.datos_profesor else None
        print(f"ID del profesor actual: {id_profesor}")
        
        if id_profesor is None:
            # Si no hay profesor, no cargamos estudiantes. Opcional: mostrar mensaje.
            self.page.update()
            return

        # Filtramos los estudiantes por el ID del profesor que ha iniciado sesión.
        lista_estudiantes = db.estudiantesREAD(pro_nameID=id_profesor)
        
        for estudiante in lista_estudiantes:
            self.view.estudiante_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(estudiante.es_nombre_1)),
                    ft.DataCell(ft.Text(estudiante.es_apellido_pat)),
                    ft.DataCell(ft.Text(estudiante.es_nacimiento.strftime('%Y-%m-%d'))), # Formatear fecha
                    ft.DataCell(ft.Text(estudiante.es_rut)),
                    ft.DataCell(ft.Text(estudiante.cur_nombre)),
                    ft.DataCell(ft.Text(f"{estudiante.pro_nombre_1} {estudiante.pro_apellido_pat}")),
                ],
                data=estudiante,
                on_select_changed=self.es_row_select,
            )
            )
        self.page.update()

    def es_row_select(self, e):
        selected_es_id = None
        selected_es= e.control.data
        is_currently_selected = e.control.selected
        for row in self.view.estudiante_table.rows:
            row.selected = False

        if not is_currently_selected:
            e.control.selected = True
            self.view.next_button.visible = True
            self.selected_es_id = selected_es[0]
        else:
            for row in self.view.estudiante_table.rows:
                row.selected = False
                if selected_es_id is not None:
                    self.view.next_button.visible = False
                for row in self.view.estudiante_table.rows:
                    row.selected = False
        self.page.update()

    def cargar_test_incompletos(self, e=None):
        self.view.test_incompletos.rows.clear()
        lista_test_incompletos = db.testREAD(test_status=0)
        
        if lista_test_incompletos:
            for test in lista_test_incompletos:
                # Añadimos la fila a la tabla correcta (test_incompletos)
                self.view.test_incompletos.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(test.es_nombre_1)),
                        ft.DataCell(ft.Text(test.es_apellido_pat)),
                        ft.DataCell(ft.Text(test.es_rut)),
                        ft.DataCell(ft.Text(test.cur_nombre)),
                        ft.DataCell(ft.Text(f"{test.pro_nombre_1} {test.pro_apellido_pat}")),
                        ft.DataCell(ft.Text(test.test_fecha_inicio.strftime('%Y-%m-%d'))),
                        ft.DataCell(ft.Text("Incompleto")), # El estado es 0 (Incompleto)
                    ],
                    data=test,
                    on_select_changed=self.test_row_select,)
                )
    def test_row_select(self, e):
        selected_test_id = None
        selected_test= e.control.data
        is_currently_selected = e.control.selected
        for row in self.view.estudiante_table.rows:
            row.selected = False
        if not is_currently_selected:
            e.control.selected = True
            self.view.upload_button.visible = True
            self.selected_test_id = selected_test.test_ID
        else:
            for row in self.view.estudiante_table.rows:
                row.selected = False
                if selected_test_id  is not None:
                    self.view.upload_button.visible = False
                for row in self.view.estudiante_table.rows:
                    row.selected = False
        self.page.update()

    def on_iniciar_test_click(self, e):
        fecha_inicio = datetime.now()

        
        pro_id = self.id_profesor
        pro_id = self.model.datos_profesor.pro_nameID if hasattr(self.model, 'datos_profesor') and self.model.datos_profesor else None

        test_data = (self.selected_es_id, pro_id, fecha_inicio, None)
        test_id = db.testCREATE(test_data)
        print (test_id)
        self.selected_test_id = test_id
        if self.selected_test_id is not None:
            self.page.go(f"/test/{self.selected_test_id}")

    def on_reanudar_test_click(self, e):
        if self.selected_test_id is not None:
            print(f"Reanudando el test con ID: {self.selected_test_id}")
            self.page.go(f"/test/{self.selected_test_id}")
        else:
            # Opcional: Mostrar un mensaje de error si no hay ningún test seleccionado
            self.page.snack_bar = ft.SnackBar(ft.Text("Por favor, selecciona un test para reanudar."), open=True, bgcolor=ft.colors.RED_700)
            self.page.update()
        self.selected_test_id = test_id
        if self.selected_test_id is not None:
            self.page.go(f"/test/{self.selected_test_id}")

    def on_reanudar_test_click(self, e):
        if self.selected_test_id is not None:
            print(f"Reanudando el test con ID: {self.selected_test_id}")
            self.page.go(f"/test/{self.selected_test_id}")
        else:
            # Opcional: Mostrar un mensaje de error si no hay ningún test seleccionado
            self.page.snack_bar = ft.SnackBar(ft.Text("Por favor, selecciona un test para reanudar."), open=True, bgcolor=ft.colors.RED_700)
            self.page.update()