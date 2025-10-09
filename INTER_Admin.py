import flet as ft
import pyodbc
from DB import CONNECTION_STRING

def admin_int(page: ft.Page):
    page.clean()
    page.window_width = 400
    page.window_height = 300

    sql_add = "INSERT INTO Profesores (" \
    "pro_nombre_1, " \
    "pro_nombre_2, " \
    "pro_nombre_3, " \
    "pro_apellido_pat, " \
    "pro_apellido_mat, " \
    "pro_nacimiento, " \
    "pro_rut, " \
    "pro_password, " \
    "lvl_curso)" \
    "VALUES(?,?, ?, ?,?,?, ?,?,?);"
    
    nombre_1 = ft.TextField(label="Primer nombre", width=300, max_length=10)
    nombre_2 = ft.TextField(label="Segundo nombre", width=300, max_length=10)
    nombre_3 = ft.TextField(label="Tercer nombre", width=300, max_length=10)
    apellido_pat = ft.TextField(label="Apellido paterno", width=300, max_length=10)
    apellido_mat = ft.TextField(label="Apellido materno", width=300, max_length=10)
    naci = ft.TextField(label="Año de nacimiento", width=300, max_length=10)
    rut = ft.TextField(label="RUT", width=300, max_length=10)
    password = ft.TextField(label="Contraseña", width=300, max_length=10)
    curso = ft.TextField(label="curso", width=300, max_length=10)
    
    
    def add_click(e):
        try:
            cnxn = pyodbc.connect(CONNECTION_STRING)
            cursor = cnxn.cursor()
            cursor.execute(sql_add, nombre_1.value, nombre_2.value,nombre_3.value, apellido_pat.value,apellido_mat.value,naci.value,rut.value,password.value, curso.value)
            cnxn.commit()
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(f"Error de conexión: {sqlstate}")

    def obtener_datos_profesores():
        cnxn = None
        cursor = None
        datos = []
    
        try:
            cnxn = pyodbc.connect(CONNECTION_STRING)
            cursor = cnxn.cursor()
            
            # Consulta para obtener los datos
            sql_select = "SELECT pro_nameID, pro_nombre_1, pro_apellido_pat, lvl_curso FROM Profesores"
            cursor.execute(sql_select)
            
            # Obtener todos los resultados
            datos = cursor.fetchall() 
            
        except pyodbc.Error as ex:
            print(f"Error al consultar la DB: {ex.args[0]}")
            
        finally:
            if cursor:
                cursor.close()
            if cnxn:
                cnxn.close()
                
        return datos
    
    def crear_tabla_profesores(datos_profesores):
        # 1. Definir Encabezados (ft.DataColumn)
        columnas = [
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Apellido")),
            ft.DataColumn(ft.Text("Curso")),
        ]

        filas = []
        for fila_sql in datos_profesores:
            
            celdas = [
                ft.DataCell(ft.Text(str(fila_sql[0]))), # ID
                ft.DataCell(ft.Text(fila_sql[1])),     # Nombre
                ft.DataCell(ft.Text(fila_sql[2])),     # Apellido
                ft.DataCell(ft.Text(fila_sql[3])),     # Curso
            ]
            
            filas.append(ft.DataRow(cells=celdas))

        # 3. Crear el objeto DataTable
        tabla = ft.DataTable(
            columns=columnas,
            rows=filas,
            # Opcional: Estilos visuales
            bgcolor=ft.colors.WHITE70,
            border=ft.border.all(2, ft.colors.BLUE_GREY_100),
            sort_column_index=0,
            sort_ascending=True
        )
        return tabla

    add_button = ft.ElevatedButton("Ingresar", on_click=add_click,width=100,height= 30)
    page.add(
        ft.Stack(
            [
                ft.Container(
                    content = ft.Column(
                        [
                            nombre_1,
                            nombre_2, 
                            nombre_3,
                            apellido_pat,
                            apellido_mat,
                            naci,
                            rut,
                            password,
                            curso,
                            add_button
                        ]
                    )
                    
                ),
                ft.Container(
                    content= ft.Column(
                        [
                            ft.DataColumn(ft.Text("ID")),
                            ft.DataColumn(ft.Text("Nombre")),
                            ft.DataColumn(ft.Text("Apellido")),
                            ft.DataColumn(ft.Text("Curso")),
                        ]
                    )
                )
                
            ]
        )

    )
ft.app(target=admin_int, view=ft.WEB_BROWSER)
