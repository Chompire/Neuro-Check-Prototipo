from flet_mvc import FletController
import flet as ft
import re
from datetime import datetime

class ModificacionDocenteController(FletController):
    def __init__(self, page, model):
        super().__init__(page, model)
        self.selected_prof_id = None
        self.password_define = "neurocheck2025"
        self.selected_curso_id = None
        self.online_state = False
        self.numpage_prof = 5
        self.numpage_cursos = 5
        self.current_page_prof = 0
        self.current_page_cursos = 0
        self.total_page_prof = 1
        self.total_page_cursos = 1
        self.numpage_estudiantes = 5
        self.current_page_estudiantes = 0
        self.total_page_estudiantes = 1
        self.selected_student_id = None

    def initialize_view(self):
        cursos = self.model.leer_cursos()
        self.build_cursos_checkboxes(cursos)
        self.view.cargo_field.on_change = self.on_cargo_change
        self.load_estudiantes_to_table()

    def load_profesores_to_table(self, id_to_select=None, profesores_a_mostrar = None):
        self.view.data_table.rows.clear()
        if profesores_a_mostrar is None:
            profesores_a_mostrar = self.model.leer_profesores()
        total_items_pro = len(profesores_a_mostrar)
        total_pages_pro = (total_items_pro + self.numpage_prof - 1) // self.numpage_prof
        if total_pages_pro == 0: total_pages_pro = 1
        start_index = self.current_page_prof * self.numpage_prof
        end_index = start_index + self.numpage_prof
        profesores_pagina_actual = profesores_a_mostrar[start_index:end_index]
        self.view.page_label_pro.value = f"Página {self.current_page_prof + 1} de {total_pages_pro}"
        self.view.prev_button_pro.visible = self.current_page_prof > 0
        self.view.next_button_pro.visible = self.current_page_prof < total_pages_pro - 1
        self.total_page_prof = total_pages_pro
        if profesores_a_mostrar:
            for prof in profesores_pagina_actual:
                    self.view.data_table.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(f"{prof.pro_nombre_1} {prof.pro_nombre_2 or ''}".strip(), selectable=True)),
                                ft.DataCell(ft.Text(f"{prof.pro_apellido_pat} {prof.pro_apellido_mat}", selectable=True)),
                                ft.DataCell(ft.Text(prof.pro_rut, selectable=True)),
                                ft.DataCell(ft.Text("Profesional PIE" if prof.pro_cargo else "Docente", selectable=True)),
                                ft.DataCell(ft.Text("Habilitado" if prof.pro_state else "Inhabilitado", selectable=True)),
                            ],
                            data=prof,
                            selected=True if id_to_select is not None and prof.pro_nameID == id_to_select else False,
                            on_select_changed=self.on_row_select,
                        )
                    )
                    self.page.update()

    def load_cursos_to_table(self, id_to_select=None, cursos_a_mostrar=None):
        self.view.curso_data_table.rows.clear()
        if cursos_a_mostrar is None:
            todos_los_cursos = self.model.leer_cursos()
            cursos_a_mostrar = [curso for curso in todos_los_cursos if curso.cur_state]

        if cursos_a_mostrar:
            total_items_cursos = len(cursos_a_mostrar)
            total_pages_cursos = (total_items_cursos + self.numpage_cursos - 1) // self.numpage_cursos
            if total_pages_cursos == 0: total_pages_cursos = 1
            self.total_page_cursos = total_pages_cursos
            
            start_index = self.current_page_cursos * self.numpage_cursos
            end_index = start_index + self.numpage_cursos
            cursos_pagina_actual = cursos_a_mostrar[start_index:end_index]

            self.view.page_label_cursos.value = f"Página {self.current_page_cursos + 1} de {total_pages_cursos}"
            self.view.prev_button_cursos.visible = self.current_page_cursos > 0
            self.view.next_button_cursos.visible = self.current_page_cursos < total_pages_cursos - 1

            for curso in cursos_pagina_actual:
                self.view.curso_data_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(curso.cur_nombre, selectable=True)),
                            ft.DataCell(ft.Text(str(curso.cur_año), selectable=True)),
                            ft.DataCell(ft.Text("Habilitado" if curso.cur_state else "Inhabilitado", selectable=True)),
                        ],
                        data=curso,
                        selected=True if id_to_select is not None and curso.cur_nameID == id_to_select else False,
                        on_select_changed=self.on_curso_row_select,
                    )
                )
        self.page.update()

    def load_estudiantes_to_table(self, estudiantes_a_mostrar=None):
        self.view.student_data_table.rows.clear()
        if estudiantes_a_mostrar is None:
            estudiantes_a_mostrar = self.model.leer_estudiantes()
        
        total_items = len(estudiantes_a_mostrar)
        total_pages = (total_items + self.numpage_estudiantes - 1) // self.numpage_estudiantes
        if total_pages == 0: total_pages = 1
        self.total_page_estudiantes = total_pages

        start_index = self.current_page_estudiantes * self.numpage_estudiantes
        end_index = start_index + self.numpage_estudiantes
        estudiantes_pagina = estudiantes_a_mostrar[start_index:end_index]

        self.view.page_label_estudiantes.value = f"Página {self.current_page_estudiantes + 1} de {total_pages}"
        self.view.prev_button_estudiantes.visible = self.current_page_estudiantes > 0
        self.view.next_button_estudiantes.visible = self.current_page_estudiantes < total_pages - 1

        for est in estudiantes_pagina:
            self.view.student_data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(est.es_nombre_1, selectable=True)),
                        ft.DataCell(ft.Text(f"{est.es_apellido_pat} {est.es_apellido_mat}", selectable=True)),
                        ft.DataCell(ft.Text(est.es_rut, selectable=True)),
                        ft.DataCell(ft.Text(est.cur_nombre, selectable=True)),
                        ft.DataCell(ft.Text(est.es_establecimiento, selectable=True)),
                    ],
                    data=est, on_select_changed=self.on_student_row_select
                )
            )
        self.page.update()
    def on_row_select(self, e):
        selected_prof = e.control.data
        is_currently_selected = e.control.selected

        for row in self.view.data_table.rows:
            row.selected = False

        if not is_currently_selected:
            e.control.selected = True
            self.view.edit_button.visible = True
            self.view.delete_button.visible = True
            self.view.add_button.disabled = True
            self.selected_prof_id = selected_prof.pro_nameID
            
            self.view.nombre1.value = selected_prof.pro_nombre_1 or ""
            self.view.nombre2.value = selected_prof.pro_nombre_2 or ""
            self.view.nombre3.value = selected_prof.pro_nombre_3 or ""
            self.view.apellido_pat.value = selected_prof.pro_apellido_pat or ""
            self.view.apellido_mat.value = selected_prof.pro_apellido_mat or ""
            self.view.rut_field.value = selected_prof.pro_rut or ""
            self.view.cargo_field.value = "Profesional PIE" if selected_prof.pro_cargo else "Docente"
            self.view.estado_field.value = "Habilitado" if selected_prof.pro_state else "Inhabilitado"
            
            self.view.cursos_checkbox_group.visible = True
            cursos_asignados_ids_str = self.model.leer_cursos_pie(self.selected_prof_id)

            cursos_asignados_ids = []
            if cursos_asignados_ids_str and cursos_asignados_ids_str.cursos_a_cargo:
                cursos_asignados_ids = cursos_asignados_ids_str.cursos_a_cargo.split(',')

            for checkbox in self.view.cursos_checkbox_group.content.controls[1:]:
                if isinstance(checkbox, ft.Checkbox):
                    checkbox.value = str(checkbox.data) in cursos_asignados_ids

        else:
            self.clear_form_fields()
            self.reset_selection_state()
        self.page.update()

    def on_cargo_change(self, e):
        """Muestra u oculta la lista de cursos según el cargo seleccionado."""
        es_pie = self.view.cargo_field.value == "Profesional PIE"
        self.view.cursos_checkbox_group.visible = es_pie
        self.page.update()


    def next_page_pro(self, e):
        if self.current_page_prof < self.total_page_prof - 1:
            self.current_page_prof += 1
            self.search_profesor()

    def prev_page_pro(self, e):
        if self.current_page_prof > 0:
            self.current_page_prof -= 1
            self.search_profesor()

    def search_profesor(self, reset_page=False):
        if reset_page: self.current_page_prof = 0
        search_term = self.view.profesor_search_field.value.lower()
        profesores_filtrados = [prof for prof in self.model.leer_profesores() if search_term in f"{prof.pro_nombre_1} {prof.pro_apellido_pat}".lower() or search_term in prof.pro_rut]
        self.load_profesores_to_table(profesores_a_mostrar=profesores_filtrados)


    def next_page_cursos(self, e):
        if self.current_page_cursos < self.total_page_cursos - 1:
            self.current_page_cursos += 1
            self.search_curso()

    def prev_page_cursos(self, e):
        if self.current_page_cursos > 0:
            self.current_page_cursos -= 1
            self.search_curso()

    def search_curso(self, reset_page=False):
        if reset_page: self.current_page_cursos = 0
        search_term = self.view.curso_search_field.value.lower()
        todos_los_cursos = self.model.leer_cursos()
        cursos_filtrados = [
            curso for curso in todos_los_cursos 
            if curso.cur_state and (search_term in curso.cur_nombre.lower() or search_term in str(curso.cur_año))
        ]
        self.load_cursos_to_table(cursos_a_mostrar=cursos_filtrados)

    def next_page_estudiantes(self, e):
        if self.current_page_estudiantes < self.total_page_estudiantes - 1:
            self.current_page_estudiantes += 1
            self.search_estudiante()

    def prev_page_estudiantes(self, e):
        if self.current_page_estudiantes > 0:
            self.current_page_estudiantes -= 1
            self.search_estudiante()

    def search_estudiante(self, reset_page=False):
        if reset_page: self.current_page_estudiantes = 0
        search_term = self.view.student_search_field.value.lower()
        estudiantes_filtrados = [est for est in self.model.leer_estudiantes() if search_term in est.es_nombre_1.lower() or search_term in est.es_rut]
        self.load_estudiantes_to_table(estudiantes_a_mostrar=estudiantes_filtrados)

    def clear_form_fields(self):
        self.view.nombre1.value = ""
        self.view.nombre2.value = ""
        self.view.nombre3.value = ""
        self.view.apellido_pat.value = ""
        self.view.apellido_mat.value = ""
        self.view.rut_field.value = ""
        self.view.cargo_field.value = None
        self.view.cursos_checkbox_group.visible = False
        self.view.estado_field.value = None
        for control in self.view.cursos_checkbox_group.content.controls:
            if isinstance(control, ft.Checkbox):
                control.value = False

    def clear_student_form_fields(self):
        self.view.bulk_student_input.value = ""

    def on_curso_row_select(self, e):
        selected_course = e.control.data
        is_currently_selected = e.control.selected

        for row in self.view.curso_data_table.rows:
            row.selected = False

        if not is_currently_selected:
            e.control.selected = True
            self.view.update_curso_button.visible = True
            self.selected_curso_id = selected_course.cur_nameID

            self.view.curso_name_field.value = selected_course.cur_nombre
            self.view.curso_year_field.value = str(selected_course.cur_año)
            self.view.curso_state_field.value = "Habilitado" if selected_course.cur_state else "Inhabilitado"
        else:
            for row in self.view.curso_data_table.rows:
                row.selected = False
                self.view.curso_name_field.value = ""
                self.view.curso_year_field.value = ""
                self.view.curso_state_field.value = None
                self.view.update_curso_button.visible = False
                self.selected_curso_id = None
                
        self.page.update()
    
    def on_student_row_select(self, e):
        selected_student = e.control.data
        is_currently_selected = e.control.selected

        for row in self.view.student_data_table.rows:
            row.selected = False

        if not is_currently_selected:
            e.control.selected = True
            self.selected_student_id = selected_student.es_nameID
            self.view.delete_student_button.visible = True
        else:
            self.selected_student_id = None
            self.view.delete_student_button.visible = False
        
        self.page.update()

    def show_feedback(self, message: str, color: str):
        self.view.feedback_snackbar.content = ft.Text(message)
        self.view.feedback_snackbar.bgcolor = color
        self.view.feedback_snackbar.open = True
        self.page.update()

    def build_cursos_checkboxes(self, cursos):
        if len(self.view.cursos_checkbox_group.content.controls) > 1:
            self.view.cursos_checkbox_group.content.controls = [self.view.cursos_checkbox_group.content.controls[0]]

        if cursos:
            cursos_habilitados = [
                curso for curso in cursos if curso.cur_state
            ]

            for curso in sorted(cursos_habilitados, key=lambda c: (c.cur_año, c.cur_nombre)):
                self.view.cursos_checkbox_group.content.controls.append(
                    ft.Checkbox(
                        label=f"{curso.cur_nombre} ({curso.cur_año})",
                        data=curso.cur_nameID,
                        check_color=ft.Colors.RED,
                        label_style=ft.TextStyle(color="black")
                    )
                )

    def show_feedback(self, message: str, color: str):
        self.view.feedback_snackbar.content = ft.Text(message)
        self.view.feedback_snackbar.bgcolor = color
        self.view.feedback_snackbar.open = True
        self.page.update()

    def reset_selection_state(self):
        for row in self.view.data_table.rows:
            row.selected = False        
        self.view.edit_button.visible = False
        self.view.delete_button.visible = False
        self.view.add_button.disabled = False
        self.selected_prof_id = None

    def add_profesor(self, e):
        rut = self.view.rut_field.value.strip()
        if not self.validar_rut(rut):
            self.show_feedback("Error: El RUT ingresado no es válido.", ft.Colors.RED)
            return

        if self.model.leer_profesor_por_rut(rut):
            self.show_feedback("Error: El RUT ya está registrado.", ft.Colors.RED)
            return

        cargo_valor = 1 if self.view.cargo_field.value == "Profesional PIE" else 0
        estado_valor = 1 if self.view.estado_field.value == "Habilitado" else 0
        
        datos_nuevos = (
            self.view.nombre1.value, self.view.nombre2.value, self.view.nombre3.value,
            self.view.apellido_pat.value, self.view.apellido_mat.value,
            rut, cargo_valor, 
            self.password_define, estado_valor,
        )
        success = self.model.crear_profesor(datos_nuevos)

        if success:
            new_prof = self.model.leer_profesor_por_rut(rut)
            ids_cursos_seleccionados = [
                str(cb.data) for cb in self.view.cursos_checkbox_group.content.controls 
                if isinstance(cb, ft.Checkbox) and cb.value
            ]
            
            if ids_cursos_seleccionados:
                if cargo_valor == 1:
                    todos_los_cursos = self.model.leer_cursos()
                    nombres_seleccionados = {c.cur_nombre for c in todos_los_cursos if str(c.cur_nameID) in ids_cursos_seleccionados}
                    
                    ids_completos_a_asignar = set(ids_cursos_seleccionados)
                    
                    for curso in todos_los_cursos:
                        if curso.cur_nombre in nombres_seleccionados and not curso.cur_state:
                            ids_completos_a_asignar.add(str(curso.cur_nameID))
                    
                    self.model.crear_asignacion_pie(new_prof.pro_nameID, ",".join(list(ids_completos_a_asignar)))
                else:
                    self.model.crear_asignacion_pie(new_prof.pro_nameID, ",".join(ids_cursos_seleccionados))

            self.show_feedback("Profesor agregado con éxito.", ft.Colors.GREEN)
            self.load_profesores_to_table()
            self.clear_form_fields()
            self.reset_selection_state()
        else:
            self.show_feedback("Error al agregar profesor.", ft.Colors.RED)
        
        self.close_dialog(e, 'add')

    def update_profesor(self, e):
        if self.selected_prof_id is None: return

        rut = self.view.rut_field.value.strip()
        if not self.validar_rut(rut):
            self.show_feedback("Error: El RUT ingresado no es válido.", ft.Colors.RED)
            return

        estado_valor = 1 if self.view.estado_field.value == "Habilitado" else 0
        cargo_valor = 1 if self.view.cargo_field.value == "Profesional PIE" else 0
        datos_actualizados = {
            "pro_nombre_1": self.view.nombre1.value, "pro_nombre_2": self.view.nombre2.value, "pro_nombre_3": self.view.nombre3.value,
            "pro_apellido_pat": self.view.apellido_pat.value, "pro_apellido_mat": self.view.apellido_mat.value,
            "pro_rut": self.view.rut_field.value,
            "pro_cargo": cargo_valor, "pro_state": estado_valor,
        }
        self.model.actualizar_profesor(self.selected_prof_id, datos_actualizados)

        ids_cursos_seleccionados = [
            str(cb.data) for cb in self.view.cursos_checkbox_group.content.controls 
            if isinstance(cb, ft.Checkbox) and cb.value
        ]
        
        # Lógica especial para PIE: añadir cursos inhabilitados con el mismo nombre
        if cargo_valor == 1:
            todos_los_cursos = self.model.leer_cursos()
            nombres_seleccionados = {c.cur_nombre for c in todos_los_cursos if str(c.cur_nameID) in ids_cursos_seleccionados}
            
            ids_completos_a_asignar = set(ids_cursos_seleccionados)
            
            for curso in todos_los_cursos:
                if curso.cur_nombre in nombres_seleccionados and not curso.cur_state:
                    ids_completos_a_asignar.add(str(curso.cur_nameID))
            
            self.model.actualizar_asignacion_pie(self.selected_prof_id, ",".join(list(ids_completos_a_asignar)))
        else:
            # Para docentes, solo se actualizan los seleccionados
            self.model.actualizar_asignacion_pie(self.selected_prof_id, ",".join(ids_cursos_seleccionados))

        self.show_feedback("Profesor actualizado con éxito.", ft.Colors.GREEN)
        self.load_profesores_to_table(id_to_select=self.selected_prof_id)
        self.close_dialog(e, 'edit')

    def update_curso(self, e):
        if self.selected_curso_id is None: return

        nuevo_estado_str = self.view.curso_state_field.value
        nuevo_estado_val = 1 if nuevo_estado_str == "Habilitado" else 0

        datos_actualizados = {"cur_state": nuevo_estado_val}
        self.model.actualizar_curso(self.selected_curso_id, datos_actualizados)
        self.show_feedback("Estado del curso actualizado.", ft.Colors.GREEN)

        if nuevo_estado_val == 0:
            nombre_curso_actual = self.view.curso_name_field.value
            año_actual = int(self.view.curso_year_field.value)
            año_siguiente = año_actual + 1
            if "1" in nombre_curso_actual or "primer" in nombre_curso_actual.lower():
                todos_los_cursos = self.model.leer_cursos()
                primer_basico_siguiente_año_existe = any(
                    ("1" in c.cur_nombre or "primer" in c.cur_nombre.lower()) and c.cur_año == año_siguiente for c in todos_los_cursos
                )
                if not primer_basico_siguiente_año_existe:
                    self.model.crear_curso(nombre_curso_actual, año_siguiente)

            if "8" in nombre_curso_actual or "octavo" in nombre_curso_actual.lower():
                self.show_feedback(f"Curso '{nombre_curso_actual}' inhabilitado. No se promueven estudiantes desde 8° básico.", ft.Colors.BLUE)
            else:
                match = re.search(r'\d+', nombre_curso_actual)
                if match:
                    nivel_actual = int(match.group())
                    siguiente_nivel = nivel_actual + 1
                    nombre_siguiente_curso = nombre_curso_actual.replace(str(nivel_actual), str(siguiente_nivel), 1)
                    
                    todos_los_cursos = self.model.leer_cursos()
                    siguiente_curso_obj = next((c for c in todos_los_cursos if c.cur_nombre.lower() == nombre_siguiente_curso.lower() and c.cur_año == año_siguiente), None)

                    if not siguiente_curso_obj:
                        self.model.crear_curso(nombre_siguiente_curso, año_siguiente)
                        todos_los_cursos = self.model.leer_cursos()
                        siguiente_curso_obj = next((c for c in todos_los_cursos if c.cur_nombre.lower() == nombre_siguiente_curso.lower() and c.cur_año == año_siguiente), None)

                    if siguiente_curso_obj:
                        estudiantes_a_mover = self.model.leer_estudiantes_por_curso(self.selected_curso_id)
                        for estudiante in estudiantes_a_mover:
                            self.model.actualizar_estudiante(estudiante.es_nameID, {"lvl_curso": siguiente_curso_obj.cur_nameID})
                        self.show_feedback(f"{len(estudiantes_a_mover)} estudiantes movidos a '{nombre_siguiente_curso}'.", ft.Colors.BLUE)
                    else:
                        self.show_feedback(f"Error: No se pudo crear o encontrar el curso '{nombre_siguiente_curso}'.", ft.Colors.RED)

        self.load_cursos_to_table(id_to_select=self.selected_curso_id)
        self.page.update()

    def add_estudiantes_en_masa(self, e):
        texto_completo = self.view.bulk_student_input.value
        if not texto_completo.strip():
            self.show_feedback("Error: El campo de lista de estudiantes está vacío.", ft.Colors.RED)
            return

        lineas = texto_completo.strip().split('\n')
        agregados_count = 0
        errores = []
        
        number_map = {
            "primer": "1", "segundo": "2", "tercer": "3", "cuarto": "4",
            "quinto": "5", "sexto": "6", "séptimo": "7", "octavo": "8"
        }
        def normalize_curso_name(name: str) -> str:
            name = name.lower().strip()
            for word, digit in number_map.items():
                name = name.replace(word, digit)
            return name.replace(" año", "").replace('°', '').replace('º', '')

        cursos_map = {
            (normalize_curso_name(c.cur_nombre), str(c.cur_año)): c.cur_nameID 
            for c in self.model.leer_cursos()
        }

        for i, linea in enumerate(lineas):
            try:
                partes = [p.strip() for p in linea.split(',', 8)]
                if len(partes) != 9:
                    errores.append(f"Línea {i+1}: Formato incorrecto (se esperaban 9 campos).")
                    continue
                nombres_full, apellido_pat, apellido_mat, rut, fecha_str, sexo_str, curso_str, año_str, establecimiento = partes
                if self.model.estudiante_existe_por_rut(rut):
                    errores.append(f"Línea {i+1}: RUT '{rut}' ya existe.")
                    continue
                
                try:
                    fecha_nacimiento = datetime.strptime(fecha_str, '%Y-%m-%d').date()
                except ValueError:
                    fecha_nacimiento = datetime.strptime(fecha_str, '%d-%m-%Y').date()
                sexo_valor = 1 if sexo_str.lower() == "masculino" else 0
                
                curso_normalizado = normalize_curso_name(curso_str)                
                curso_id = cursos_map.get((curso_normalizado, año_str))
                if not curso_id:
                    errores.append(f"Línea {i+1}: Curso '{curso_str}' del año '{año_str}' no encontrado.")
                    continue

                datos_estudiante = (nombres_full, apellido_pat, apellido_mat, rut, fecha_nacimiento, sexo_valor, curso_id, establecimiento)
                
                if self.model.crear_estudiante(datos_estudiante):
                    agregados_count += 1
                else:
                    errores.append(f"Línea {i+1}: Error al guardar en la base de datos.")

            except Exception as ex:
                errores.append(f"Línea {i+1}: Error de procesamiento - {ex}")

        if agregados_count > 0:
            self.show_feedback(f"Proceso completado. {agregados_count} estudiantes agregados.", ft.Colors.GREEN)
        if errores:
            error_msg = f"Se encontraron {len(errores)} errores: " + " | ".join(errores[:3])
            self.show_feedback(error_msg, ft.Colors.RED)
        if agregados_count > 0 and not errores:
            self.clear_student_form_fields()

        self.page.update()

    def delete_estudiante(self, e):
        if self.selected_student_id:
            success = self.model.eliminar_estudiante(self.selected_student_id)
            if success:
                self.show_feedback("Estudiante eliminado con éxito.", ft.Colors.GREEN)
                self.load_estudiantes_to_table()
                self.view.delete_student_button.visible = False
                self.selected_student_id = None
            else:
                self.show_feedback("Error al eliminar el estudiante.", ft.Colors.RED)
        self.close_dialog(e, 'delete_student')

    def open_curso_dialog(self, e):
        self.load_cursos_to_table()
        self.view.curso_dialog.open = True
        self.page.update()

    def close_curso_dialog(self, e):
        self.view.curso_dialog.open = False
        self.page.update()

    def delete_profesor(self, e):
        if self.selected_prof_id:
            self.model.eliminar_asignacion_pie(self.selected_prof_id)

            self.model.eliminar_profesor(self.selected_prof_id)
            self.show_feedback("Profesor eliminado con éxito.", ft.Colors.GREEN)
            self.load_profesores_to_table()
            self.clear_form_fields()
            self.reset_selection_state()
        self.close_dialog(e, 'delete')

    def open_dialog(self, e, tipo: str):
        dialog = getattr(self.view, f"{tipo}_dialog")
        dialog.open = True
        self.page.update()

    def close_dialog(self, e, tipo: str):
        dialog = getattr(self.view, f"{tipo}_dialog")
        dialog.open = False
        self.page.update()

    def formato_rut(self, e: ft.ControlEvent):
        rut_field = e.control
        raw_rut = "".join(filter(lambda char: char.isdigit() or char.upper() == 'K', rut_field.value))
        if not raw_rut:
            return
        body = raw_rut[:-1]
        dv = raw_rut[-1]
        if body:
            reversed_body = body[::-1]
            formatted_reversed_body = ".".join(reversed_body[i:i+3] for i in range(0, len(reversed_body), 3))
            formatted_body = formatted_reversed_body[::-1]
            rut_field.value = f"{formatted_body}-{dv}"
        else:
            rut_field.value = dv
        self.page.update()

    @staticmethod
    def validar_rut(rut: str) -> bool:
        rut = rut.upper().replace(".", "").replace("-", "")
        if not rut[:-1].isdigit() or not (rut[-1].isdigit() or rut[-1] == 'K'):
            return False
        
        numero = rut[:-1]
        dv = rut[-1]
        
        try:
            reversed_numero = numero[::-1]
            multiplicador = 2
            suma = 0
            for d in reversed_numero:
                suma += int(d) * multiplicador
                multiplicador += 1
                if multiplicador == 8:
                    multiplicador = 2
            
            resto = suma % 11
            dv_calculado = 11 - resto
            
            if dv_calculado == 11:
                dv_esperado = '0'
            elif dv_calculado == 10:
                dv_esperado = 'K'
            else:
                dv_esperado = str(dv_calculado)
                
            return dv == dv_esperado
        except Exception:
            return False