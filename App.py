
# Librerias

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from plyer import notification

from Temporizador import temporizador

Window.size = (370, 660)

# Creacion de las interfaces

Builder.load_string("""

<ScreenManagement>:
    Home:
    Recordatorio:
    Progreso:
""")

# Archivo de cada interfaz

Builder.load_file("Home.kv")
Builder.load_file("Recordatorio.kv")
Builder.load_file("Progreso.kv")

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

# Estructura de la app

class Home(Funciones):
	pass

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