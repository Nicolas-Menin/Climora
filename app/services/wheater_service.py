
import httpx
from app.config.config import API_KEY


class CityService:

    async def get_city_data(self,city):
        """Obtiene los datos del clima de la ciudad seleccionada"""

        try:

            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": city,
                "appid": API_KEY,
                "units": "metric",
                "lang": "es"
            }
            async with httpx.AsyncClient() as client:

                response = await client.get(url,params=params,timeout=5)


            return response.json()

        except httpx.ReadTimeout as e:
            raise ValueError("Error de tiempo con la API: ",e) from e
        except httpx.RequestError as e:
            raise ValueError("Error de conexion con la API: ",e) from e

    async def city_filter(self,city):
        """Obtiene las ciudades que tengan coincidencia con la cidad escrita"""
        try:

            url = "http://api.openweathermap.org/geo/1.0/direct"
            params = {
                "q": city,
                "limit": 5,
                "appid": API_KEY
            }

            async with httpx.AsyncClient() as client:

                response  = await client.get(url,params=params,timeout=5)

            return response.json()

        except httpx.RequestError as e:

            raise ValueError("Error de conexion con la API: ",e) from e
