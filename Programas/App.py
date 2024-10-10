
# Librerías

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from plyer import notification

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from Temporizador import temporizador

Window.size = (370, 660)

# Creacion de las interfaces

Builder.load_string("""

<ScreenManagement>:
    Home:
    Recordatorio:
    Progreso:
    InicioSeccion:    
""")

# Archivo de cada interfaz

Builder.load_file("Home.kv")
Builder.load_file("Recordatorio.kv")
Builder.load_file("Progreso.kv")
Builder.load_file("Inicio_Seccion.kv")

class ScreenManagement(ScreenManager):
    pass

# Funciones para desplazarse en cada interfaz

class Funciones(BoxLayout, Screen):
	def pagina_principal(self):
		self.manager.current = "home"

	def pagina_recordatorio(self):
		self.manager.current = "recordatorio"

	def pagina_progreso(self):
		self.manager.current = "progreso"

	def pagina_inicio_seccion(self):
		self.manager.current = "inicio_seccion"

# Estructura de la app

class Home(Funciones):
	def boton_inicio_seccion(self, nombre):

		# Renombrar el boton
		self.ids.inicio_seccion.text = nombre

class Recordatorio(Funciones):
    def enviar_notificacion(self, dt):        
        notification.notify(
            title = "AquaAlert - Recordatorio",
            message = "¡No olvides tomar agua 😁!",
        )

    def notificacion(self):

    	try:
		    tiempo = int(self.ids.tiempo.text)

		    temporizador(tiempo)
		    self.enviar_notificacion(1)

    	except Exception as e:
    		print(f"Error: {e}")

class Progreso(Funciones):
	def cantidad_agua(self, button):

		if int(button.text[0:2]) != 8:
			button.text = f"{str(int(button.text[0:2]) + 1)} / 8"
			return 			

		button.text = "0 / 8"	

class InicioSeccion(Funciones):
	def guardar_datos(self):

		try:

			# Crear y conectar la bbdd remota
	
			url = "mongodb+srv://bredalisgautreaux:ItF6fAeKDLNFpBAD@cluster0.3myzkvu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
			cliente = MongoClient(url, server_api = ServerApi("1"))
			db = cliente["AquaAlert"]
			coleccion = db["Usuario"]

			# Obtener los datos del usuario
	 
			nombre = self.ids.nombre.text
			contraseña = self.ids.contraseña.text

			# Insertar datos

			documento = {"Nombre": nombre, "Contraseña": contraseña}
			coleccion.insert_one(documento)

			# Redireccionar a la pagina Home
			
			home_screen = self.manager.get_screen("home")
			home_screen.boton_inicio_seccion(nombre)
            			
			self.pagina_principal()

			print("¡La coneccion fue un exito!")

		except Exception as e:
		    print("Error:", e)

class App(App):
	title = "AquaAlert"

	def on_start(self):
		self.icon = "Logo.png"
		super().on_start()	

	def build(self):
		return ScreenManagement()

# Inicio de la app 

if __name__ == "__main__":
	App().run()