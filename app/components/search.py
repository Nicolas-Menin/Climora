import asyncio
import flet as ft
from services.wheater_service import CityService


# pylint: disable=E1121,E1123,E1101

class SearchController:
    """Clase Controlador de Busqueda de Ciudad"""
    def __init__(self,list_city,page):

        # Instancia del service de la API
        self.city_services = CityService()

        # Lista que recibe el ListView del View Home para utilizarlo en esta clase
        self.list_cities = list_city

        # Referencia a la Raiz Principal
        self.page_ref = page





    async def search_city(self,e):
        """Realiza filtrado de ciudades con la API mediante el service y los presenta"""
        city_search = e.control.value

        if len(city_search) < 3: # Si el campo tiene menos de 3 caracteres borra el filtrado

            self.list_cities.controls.clear()
            self.page_ref.update()
            return



        cities =  await self.city_services.city_filter(city_search) # Obtiene las ciudades que coindicen  con la busqueda

        self.list_cities.controls.clear()

        for city in cities:

            # Agrega las ciudades a la lista
            self.list_cities.controls.append(
                ft.ListTile(title=f"{city['name']}, {city.get('state','')}, {city['country']}",
                            bgcolor="#353535",
                            trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT),
                            hover_color="#4b4b4b",
                            on_click = lambda e, c=city: self.city_weather(e.control.title)))


        self.page_ref.update()


    def city_weather(self,city):
        """Dirige al View donde se muestra el clima"""

        city_selected = city # Toma el nombre de la ciudad elegida
        asyncio.create_task(self.page_ref.push_route(f"/weather?name={city_selected}")) # Se le agrega el nombre de la ciudad al endpoint