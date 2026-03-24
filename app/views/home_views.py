import flet as ft
import asyncio
from components.search import SearchController

# pylint: disable=E1121,E1123,E1101

class HomeView(ft.View):
    """Clase HomeView que permite buscar ciudad"""
    def __init__(self,font):
        super().__init__()
        # Instancia del controlador de busqueda
        self.city_controller = None
        # Fuente
        self.fonts = font

        # Nombre de route
        self.route="/Home"

        self.padding=0
        self.spacing=0





        # Lista donde se van a cargar las ciudades filtradas
        self.list_cities = ft.ListView(
            width=300,
        )

        # Titulo
        self.city_title = ft.Text(
                                value="CHOOSE A CITY",
                                size=30,
                                animate_scale=500,
                                scale=0,
                                font_family=self.fonts,

                            )

        # Instancia del controlador de busqueda

        # Campo para escribir que ciudad vas a buscar
        self.search = ft.TextField(
                    hint_text="Write a city...",
                    max_lines=2,
                    bgcolor="#292929",
                    max_length=30,
                    width=300,
                    animate_scale=500,
                    scale=0,
                    on_change=  lambda e: self.page.run_task(self.city_controller.search_city,e)
                    )

        # Frame donde se acomoda los widget
        self.search_frame =  ft.Column(
            alignment = ft.CrossAxisAlignment.CENTER,
            spacing = 10,
            expand = True,
            controls=[
                    self.search,
                    self.list_cities],

        )

        # Controlador del view
        self.controls=[
                ft.Stack(
                    expand=True,
                    controls=[
                        ft.Container(
                            expand=True,
                            image=ft.DecorationImage(
                                src="/images/Bg.png",
                                fit=ft.BoxFit.COVER,
                            ),
                        ),
                        ft.Container(
                            alignment=ft.Alignment.TOP_CENTER,
                            padding=ft.padding.only(top=40),
                            content=self.city_title
                        ),
                        ft.Container(
                            content= self.search_frame,
                            alignment=ft.Alignment.TOP_CENTER,
                            padding= ft.Padding.only(bottom=0)
                        )
                    ],
                )

            ]



    def did_mount(self):
        self.city_controller = SearchController(self.list_cities,self.page)


        widget =  [
            self.search,
            self.city_title
        ]
        self.page.run_task(self.entry_animation,widget)
        self.update()


    async def entry_animation(self,widget):
        """Animacion zoomin de entrada"""

        for w in widget:
            await asyncio.sleep(0.05)
            w.scale = 1

            self.update()
