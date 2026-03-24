import asyncio
import flet as ft
from services.wheater_service import CityService
from config.weather_icons import WEATHER_ICON

# pylint: disable=E1121,E1123,E1101

class WeatherView(ft.View):
    """View que muestra el clima"""
    def __init__(self,font):
        super().__init__()


        self.city_service = CityService() # Instancia del service de la API

        # Variable que nos permite saber si ya se mostro anteriormente pantalla de carga
        self.loading_task = None


        self.city_selected = None # Variable que recibe que Ciudad se eligio anteriormente en el buscador

        # Fuentes
        self.font_colombo = font[0]
        self.font_reboto = font[1]

        # Variable que recibe datos de la API
        self.weather = None


        # Textos que muestran los datos recibidos de la API
        self.city_name = ft.Text(
            value="",
            font_family=self.font_colombo,
            size=50,
            scale=0,
            animate_scale=250)
        self.temp_text = ft.Text(
            value="",
            font_family=self.font_reboto,
            size=70,
            weight=ft.FontWeight.BOLD,
            animate_scale=250,
            scale=0,
            margin=ft.margin.only(top=100)
            )
        self.weather_text = ft.Text(
            value="",
            font_family=self.font_reboto,
            size=50,
            weight=ft.FontWeight.BOLD,
            animate_scale=250,
            scale=0
            )
        self.feels_like = ft.Text(
            value="",
            font_family=self.font_reboto,
            size=20,
            weight=ft.FontWeight.BOLD,
            animate_scale=250,
            scale=0
            )
        self.temp_min_max = ft.Text(
            value="",
            font_family=self.font_reboto,
            size=30,
            weight=ft.FontWeight.BOLD,
            animate_scale=250,
            scale=0
            )

        self.wind_speed = ft.Text(
            value="",
            font_family=self.font_reboto,
            size=20,
            weight=ft.FontWeight.BOLD,
            animate_scale=250,
            scale=0
            )

        # Imagen que recibe el codigo de Icon de la API
        self.weather_icon = ft.Image(
            src="images/default.png",
            width=200,
            height=200,
            animate_scale=250,
            scale=0
            )

        #Boton para volver al anterior View
        self.btn_back = ft.ElevatedButton(content= ft.Text(
            value="BACK",
            font_family="Reboto",size=25),
            color = "#ffffff",
            bgcolor="#2C5F5F",
            width=150,
            height=70,
            scale=1.0,
            visible=False,
            animate_scale=ft.Animation(300,ft.AnimationCurve.EASE),
            on_hover= lambda e: self.elevate_button_animation(e,self.btn_back),
            on_click = self.go_back_action
            )


        # Texto que se muestra cuando se espera los datos de la API
        self.loading = ft.Text("LOADING...",
                               font_family=self.font_colombo,
                               size=50,
                               opacity=1,
                               animate_opacity=500)


        # Frame que ordena los textos que reciben los datos de la API
        self.weather_result = ft.Row(
            controls=[

                ft.Column(
                    controls=[
                        self.temp_text,
                        self.feels_like,

                        ft.Column(
                            controls=[
                                self.temp_min_max,
                                self.wind_speed
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),

                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                ),

                ft.Column(
                    controls=[
                        self.weather_icon,
                        self.weather_text,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10
                )

            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=50
        )


        # Presentar los textos en el controlador del View
        self.route = "/weather"
        self.padding = 0
        self.spacing = 0
        self.controls=[
                 ft.Stack(
                    expand= True,
                    fit = ft.BoxFit.COVER,
                    controls=[
                        ft.Container(
                            image= ft.DecorationImage("/images/Bg.png",
                                                      fit=ft.BoxFit.COVER),
                            expand=True,

                        ),
                        ft.Container(
                            content=self.city_name,
                            alignment= ft.Alignment.TOP_LEFT,
                            padding= ft.Padding.only(left=100,top=30)
                        ),
                        ft.Container(
                            content=self.weather_result,
                            alignment=ft.Alignment.CENTER,
                            expand=True,
                            padding= ft.Padding.only(bottom=100)
                        ),
                        ft.Container(
                            expand=True,
                            content=self.loading,
                            alignment= ft.Alignment.CENTER
                        ),

                        ft.Container(
                            expand=True,
                            content=self.btn_back,
                            alignment=ft.Alignment.BOTTOM_LEFT,
                            padding= ft.Padding.only(bottom=50,left=50)
                        )

                    ]
                )

        ]




    # Animaciones

    ###
    def elevate_button_animation(self,e,btn):
        """Animacion zoomin y zoomout de boton tipo Elevate"""
        if e.data:
            btn.scale = 1.2

        else:
            btn.scale = 1.0

        self.update()
    async def animation_loading(self,btn):
        """Animacion tipo fadein y fadeout de etiqueta Loading"""

        while True:

            if self.weather:
                btn.visible = False
                self.update()
                break

            btn.opacity = 0
            self.update()
            await asyncio.sleep(0.5)

            btn.opacity = 1
            self.update()
            await asyncio.sleep(0.5)

    async def animation_zoomin(self,lst_text):
        """Animacion zoomin de texto cuando aparecen"""
        for text in lst_text:

            text.scale = 1

            self.update()

    ###


    def did_mount(self):

        self.reset_all()
        query = self.page.query

        self.city_selected = query.get("name")

        if self.loading_task: # Verificamos si ya existio la tarea

            self.loading_task.cancel() # Cancelamos la tarea

        self.loading_task =self.page.run_task(self.animation_loading, self.loading) #Creamos nueva tarea

        if self.city_selected:
            self.page.run_task(self.search_wheater,self.city_selected)
            self.update()


    # ACCIONES

    ###
    async def search_wheater(self,city):

        """Funcion que hace llamado a la API mediante al service"""

        data = await self.city_service.get_city_data(city)

        if data.get("cod") != 200:

            return self.show_error()

        self.sort_data_api(data)



    def sort_data_api(self,data):
        """Ordena los datos recibidos de la API"""

        self.weather = {
            "weather": data["weather"][0]["main"],
            "icon": data["weather"][0]["icon"],
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "temp_min": data["main"]["temp_min"],
            "temp_max": data["main"]["temp_max"],
            "pressure": data["main"]["pressure"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "city": data["name"],
            "country": data["sys"]["country"]
        }

        self.set_data(self.weather)



    def set_data(self,weather_data):
        """Setea los datos recibidos de la API a sus respectivos textos e imagen"""

        if weather_data: # Si wheater_data recibio datos de la API entonces...

            #Instancio los datos de manera temporal para que sea mas comodo
            temp = round(weather_data["temp"])
            weather = weather_data["weather"]
            city = weather_data["city"]
            country = weather_data["country"]
            feels_like = round(weather_data["feels_like"])
            temp_min = round(weather_data["temp_min"])
            temp_max = round(weather_data["temp_max"])
            wind_speed = round(weather_data["wind_speed"])

            # Busca en el diccionario de iconos cual codigo coincide con el que dio la API y devuelve la imagen sino existe usa el icono por defecto
            icon = WEATHER_ICON.get(weather_data["icon"],WEATHER_ICON["default"])



            # Seteamos la informacion obtenida de la API en sus respectivas etiquetas
            self.city_name.value = f"{city}, {country}"
            self.weather_icon.src = f"images/{icon}"
            self.temp_text.value = f"{temp}° C"
            self.weather_text.value = f"{weather}"
            self.feels_like.value = f"Feels like {feels_like}°"
            self.temp_min_max.value = f"High {temp_max}° Low {temp_min}°"
            self.wind_speed.value = f"Wind speed {wind_speed} m/s"

            # Lista que tiene las etiquetas e imagen para que se utilice en la animacion de presentacion
            show_results= [
                self.city_name,
                self.wind_speed,
                self.weather_icon,
                self.temp_text,
                self.weather_text,
                self.feels_like,
                self.temp_min_max]

            self.btn_back.visible = True # Hacemos que sea visible el boton BACK para que pueda retroceders

            # Hacemos que se  ejecute como corrutina
            self.page.run_task(self.animation_zoomin,show_results)
            self.update()




    def show_error(self):
        """Manda una alerta si es que ocurrio error con la API"""

        error_dialog = ft.AlertDialog(
            title=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED),
                    ft.Text("Error", size=30,weight=ft.FontWeight.BOLD)
                ],
                spacing=10
            ),
            content=ft.Text("We sorry. We can't show the weather right now. Try later."),
            actions=[ft.TextButton("Acept", on_click=self.go_back_dialog)]
        )

        self.page.show_dialog(error_dialog) # Muestra Dialog (Alerta)


    def go_back_dialog(self):
        """Funcionn para volver al view anterior"""

        self.page.update()
        self.page.run_task(self.page.push_route,"/Home")

    def go_back_action(self):
        """Accion de boton que vuelve al view anterior"""
        self.reset_all()
        self.page.run_task(self.page.push_route,"/Home")


    def reset_all(self):
        """Resetea todas las etiquetas e imagen con sus escalas a la forma inicial"""
        self.weather = None
        self.loading.visible = True
        self.loading.opacity = 1
        self.btn_back.visible = False
        self.city_name.value = ""
        self.city_name.scale = 0
        self.wind_speed.value = ""
        self.wind_speed.scale = 0
        self.btn_back.scale = 1
        self.weather_icon.scale = 0
        self.temp_text.value = ""
        self.temp_text.scale = 0
        self.weather_text.value = ""
        self.weather_text.scale = 0
        self.feels_like.value = ""
        self.feels_like.scale = 0
        self.temp_min_max.value = ""
        self.temp_min_max.scale = 0

        self.update()

    ###