import flet as ft
def mostrar_menu_principal(page: ft.Page, cerrar_main):    
    page.clean()
    content_container = ft.Container(expand=True)
    def new_test(e):
        registro_alumno(page, content_container) 
        page.update()

    def cerrar_sesión(e):
        cerrar_main(page)
        page.update()

    def mostrar_bienvenida():
        content_container.content = ft.Column(
            [
                ft.Text("¡Bienvenido!", size=18),
            ],
            alignment="center",
            horizontal_alignment="center",
        )
        page.update()
        
    nombre_usuario = "xd"
    
    barra = ft.Container(ft.Row(
        [
            ft.Text(f"NeuroCheck", size=25, weight="bold", color="black"), 
            ft.Container(
                ft.MenuBar(expand=True,controls=[ft.SubmenuButton(
                content=ft.Icon(ft.Icons.MENU), controls= 
                [
                    ft.MenuItemButton(
                    content=ft.Text("Nuevo test"),
                    leading=ft.Icon(ft.Icons.ADD),
                    style=ft.ButtonStyle(bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE}),
                    on_click = new_test),

                    ft.MenuItemButton(
                    content=ft.Text("Cerrar sesión"),
                    leading=ft.Icon(ft.Icons.EXIT_TO_APP),
                    style=ft.ButtonStyle(bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE}),
                    on_click=cerrar_sesión)                    
                    ])])
                        )
        ],
        alignment="spaceBetween"),
        bgcolor="red", padding=10)    
    page.add(
        
        ft.Container(
            ft.Column(
            [
                barra,
                content_container,                
            ],
            alignment="center",
            horizontal_alignment="center",
            
            )
        )
        
    )
    mostrar_bienvenida()

def registro_alumno(page:ft.Page, content_container: ft.Container):
    def back(e):
        content_container.content = ft.Text("¡Bienvenido!", size=18)
        page.update()
    año = ["",
        ft.MenuItemButton(
            content=ft.Text("1°"),
            leading=ft.Icon(ft.Icons.COLORIZE),
            style=ft.ButtonStyle(bgcolor={ft.ControlState.HOVERED: ft.Colors.BLUE})),
        ft.MenuItemButton(
                content=ft.Text("2°"),
                leading=ft.Icon(ft.Icons.COLORIZE),
                style=ft.ButtonStyle(
                        bgcolor={ft.ControlState.HOVERED: ft.Colors.GREEN})),
        ft.MenuItemButton(
                content=ft.Text("3°"),
                leading=ft.Icon(ft.Icons.COLORIZE),
                style=ft.ButtonStyle(
                    bgcolor={ft.ControlState.HOVERED: ft.Colors.RED})),
        ft.MenuItemButton(
                content=ft.Text("4°"),
                leading=ft.Icon(ft.Icons),
                style=ft.ButtonStyle(
                    bgcolor={ft.ControlState.HOVERED: ft.Colors.RED})),
            ]
    menubar = ft.MenuBar(
        expand=True,
        controls=[
            ft.SubmenuButton(
                content=ft.Text("Curso"),
                controls=[año[1],año[2],año[3],año[4]],                
            ),
            ft.SubmenuButton(content=ft.Text("Grado")),
        ],
    )
    
    
    boton_volver=ft.ElevatedButton("Volver", on_click=back, width=100, height=30)
    content_container.content = ft.Row(
        [
            ft.Column(
                [
                    ft.Text("Registro Alumno", size=20, weight="bold"),
                    menubar,
                    boton_volver,
                    ft.TextField(label="Usuario", width=300, max_length=9)
                ],
                alignment="start",
                horizontal_alignment="start",
            )
        ],
        alignment="start",
        expand=True
    )
    page.update()  
