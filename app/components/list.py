import flet as ft
from services.wheater_service import CityService


# pylint: disable=E1121,E1123

class Search(ft.Column):

    def __init__(self):
        super().__init__()
        self.alignment = ft.CrossAxisAlignment.CENTER
        self.spacing = 10
        self.expand = True

        self.search = ft.TextField(
            hint_text="Escribe una ciudad",
            max_lines=2,
            bgcolor="#292929",
            max_length=30,
            width=300,
            on_change=  self.search_city_on_change
        )

        # ListView dentro de un Container que se expande
        self.list_cities = ft.ListView(
            width=300,
        )

        self.city_controller = SearchController(self.list_cities)

        self.controls = [
            self.search,
            self.list_cities
        ]


    async def search_city_on_change(self,e):

        await self.city_controller.search_city(e,self)





class SearchController:

    def __init__(self,list_city):
        self.city_services = CityService()
        self.list_cities = list_city




    async def search_city(self,e,page):

        city = e.control.value

        if len(city) < 3:
            if self.list_cities:
                self.list_cities.controls.clear()

            return



        cities =  await self.city_services.city_filter(city)

        self.list_cities.controls.clear()

        for city in cities:

            self.list_cities.controls.append(
                ft.ListTile(title=f"{city['name']}, {city.get('state','')}, {city['country']}",
                            bgcolor="#353535",
                            trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT),
                            hover_color="#4b4b4b",
                            on_click=lambda : print("hola")))


        page.update()