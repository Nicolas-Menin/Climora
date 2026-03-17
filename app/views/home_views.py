import flet as ft
from components.list import Search


# pylint: disable=E1121,E1123

class HomeView(ft.View):

    def __init__(self):
        super().__init__(route="/Home")
        self.fonts = None

    def setup(self, fonts):
        self.fonts = fonts

        return ft.View(
            route="/Home",
            padding=0,
            spacing=0,
            controls=[
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
                            content=ft.Text(
                                value="ELIJA UNA CIUDAD",
                                size=30,
                                font_family=self.fonts
                            ),
                        ),
                        ft.Container(
                            content= Search(),
                            alignment=ft.Alignment.TOP_CENTER,
                            padding= ft.Padding.only(bottom=0)
                        )
                    ],
                )

            ]
        )