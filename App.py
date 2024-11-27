
# Librerías
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from plyer import notification
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import pygame 
import os
from Scripts.Temporizador import temporizador

pygame.mixer.init()
Window.size = (370, 660)

# Creación de las interfaces
Builder.load_string("""
<ScreenManagement>:
    Home:
    Recordatorio: 
    Progreso:
    InicioSeccion:
""")

# Cargar diseño de interfaces
Builder.load_file("KV/Home.kv")
Builder.load_file("KV/Recordatorio.kv")
Builder.load_file("KV/Progreso.kv")
Builder.load_file("KV/Inicio_Seccion.kv")

# Administrador de pantallas
class ScreenManagement(ScreenManager):
    pass

class Funciones(BoxLayout, Screen):
    # Funciones para desplazarse en cada interfaz
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
        # Renombrar el botón
        self.ids.inicio_seccion.text = nombre

class Recordatorio(Funciones):
    def enviar_notificacion(self):
        notification.notify(
            title = "AquaAlert - Recordatorio",
            message = "¡No olvides tomar agua 😁!",
            app_icon = "Assets/Logo.ico"
        )

    def notificacion(self):
        try:
            self.ids.mensaje_error_1.text = ""
            self.ids.mensaje_error_2.text = ""
            tiempo = int(self.ids.tiempo.text)

            temporizador(tiempo)
            self.enviar_notificacion()
            pygame.mixer.music.load("Assets/Notificacion.mp3")
            pygame.mixer.music.play()            

        except Exception as e:
            self.ids.mensaje_error_1.text = "Valor"
            self.ids.mensaje_error_2.text = "Inesperado"
            print(f"Error inesperado: {e}")

class Progreso(Funciones):
    def cantidad_agua(self, button):
        numero = int(button.text[0:2])
        if numero != 8:
            button.text = f"{str(numero + 1)} / 8"
            return

        button.text = "0 / 8"

class InicioSeccion(Funciones):
    def guardar_datos(self): 
        try:
            self.ids.mensaje_error_1.text = ""
            self.ids.mensaje_error_2.text = ""
            
            # Crear y conectar la bbdd remota
            load_dotenv()
            cliente = MongoClient(os.getenv("CLAVE_MONGO"), server_api = ServerApi("1"))
            db = cliente["AquaAlert"]
            coleccion = db["Usuario"]

            # Obtener los datos del usuario
            nombre = self.ids.nombre.text
            contrasena = self.ids.contrasena.text

            if not nombre or not contrasena:
                print("Error: Los compos deben estar llenos los dos.")
                return

            # Insertar datos
            documento = {"Nombre": nombre, "Contraseña": contrasena}
            coleccion.insert_one(documento)

            # Redireccionar a la página Home
            home_screen = self.manager.get_screen("home")
            home_screen.boton_inicio_seccion(nombre)

            self.pagina_principal()
            print("¡La conexión fue un éxito!")

        except Exception as e:
            self.ids.mensaje_error.text = "Error de conexión"
            return f"Error inesperado: {e}"
            
# Aplicación principal
class AquaAlert(App):
    title = "AquaAlert"

    def on_start(self):
        self.icon = "Assets/Logo.png"
        super().on_start()

    def build(self):
        return ScreenManagement()

if __name__ == "__main__":
    AquaAlert().run()