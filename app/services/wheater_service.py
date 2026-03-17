
from config import API_KEY
import httpx


class CityService:

    async def get_city_data(self,city):

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

    async def city_filter(self,city):

        url = "http://api.openweathermap.org/geo/1.0/direct"
        params = {
            "q": city,
            "limit": 5,
            "appid": API_KEY
        }

        async with httpx.AsyncClient() as cliente:

            response  = await cliente.get(url,params=params,timeout=5)

        return response.json()