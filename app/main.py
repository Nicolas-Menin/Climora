import flet as ft
from views.window_views import Window

# pylint: disable=too-many-positional-arguments

async def main(page: ft.Page):
    """Funcion Principal donde se setea la Pagina Principal"""
    windows = Window(page)

    await windows.setup()

if __name__ == "__main__":

    ft.run(main,view=ft.AppView.FLET_APP,assets_dir="assets")
