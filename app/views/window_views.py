import asyncio


import flet as ft
from views.home_views import HomeView

# pylint: disable=E1121,E1123
class Window:

    def __init__(self,page: ft.Page):

        self.page = page
        self.home_view = HomeView()

         # Titulo

        self.page.title = "Climora"

        # Tamaño de Ventana
        self.page.window.width = 920
        self.page.window.height = 735

        #Tamaño Maximo y Minimo de ventana
        self.page.window.max_width = 920
        self.page.window.min_width = 920
        self.page.window.min_height = 735
        self.page.window.max_height = 735
        # Ventana Maximizable
        self.page.window.maximizable =False

        # Color de fondo de ventana
        self.page.bgcolor = "#272727"
        self.page.padding = 0
        self.page.spacing = 0

        # Fuentes de texto
        self.page.fonts = {
            "Colombo": "fonts/Colombo Sans Font.ttf",
            "Reboto": "fonts/Reboto.ttf"
        }

        self.page.on_route_change = self.route_change
        self.page.on_view_pop = self.view_pop



        self.btn_start = ft.ElevatedButton(content= ft.Text(value="START",
                                                            font_family="Reboto",size=25),
                                                            color = "#ffffff",
                                                            bgcolor="#2C5F5F",
                                                            width=200,
                                                            height=70,
                                                            scale=1.0,
                                                            animate_scale=ft.Animation(300,ft.AnimationCurve.EASE),
                                                            on_hover= lambda e: self.elevate_button_animation(e,self.btn_start),
                                                            on_click= lambda e: asyncio.create_task(self.page.push_route("/Home"))
                                                        )



    async def setup(self):

        self.page.views.append(
            ft.View(
                ft.Stack([
                    ft.Container(
                    expand=True,
                    image=ft.DecorationImage(
                        src="/images/Bg.png",
                        fit= ft.BoxFit.COVER,
                    ),
                    alignment=ft.Alignment.CENTER
                ),
                    ft.Container(
                        content=ft.Text(value="CLIMORA",size=50,font_family="Colombo"),
                        alignment= ft.Alignment.TOP_CENTER,
                        padding= ft.Padding.only(top=20)
                ),
                    ft.Container(
                        content= self.btn_start,
                        alignment= ft.Alignment.CENTER
                    )
                ],
                expand= True
            ),
            expand=True,
            route="/",
            spacing=0,
            padding=0
            )
        )

        if not self.page.web:
            await self.page.window.center()

        self.page.window.visible = True
        self.page.update()


    def elevate_button_animation(self,e,btn):

        if e.data:
            btn.scale = 1.2

        else:
            btn.scale = 1.0

        self.page.update()



    def route_change(self):

        self.page.views.clear()



        if self.page.route == "/Home":
            self.page.views.append(self.home_view.setup("Colombo"))

        self.page.update()

    async def view_pop(self,e):

        if e.view is not None:

            self.page.views.remove(e.view)
            top_view = self.page.views[-1]

            await self.page.push_route(top_view.route)