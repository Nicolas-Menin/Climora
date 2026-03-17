import flet as ft



# pylint: disable=too-many-positional-arguments
class CustomAppBar(ft.AppBar):

    def __init__(self):
        super().__init__()

        self.title = ft.Text(value="Dashboard",size=20) # pylint: disable=E1121,E1123
        self.bgcolor = "#2C2C2C"
        self.center_title = True
