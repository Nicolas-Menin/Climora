import flet as ft



# pylint: disable=E1121,E1123

class WheaterView(ft.View):

    def __init__(self):
        super().__init__()



    def setup(self):


        return ft.View(
                route = "/wheater",
                padding=0,
                spacing=0,
                controls=[
                    ft.Stack(
                        expand= True,
                        fit = ft.BoxFit.COVER,
                        controls=[
                            ft.Container(
                                image= ft.DecorationImage("/images/Bg.png")
                            )
                        ]
                    )

                ]
            )

