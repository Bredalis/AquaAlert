
# Libraries
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
from src.timer import timer

pygame.mixer.init()
Window.size = (370, 660)

# Interface creation
Builder.load_string("""
<ScreenManagement>:
    Home:
    Reminder: 
    Progress:
    LoginSection:
""")

# Load interface design
Builder.load_file("kv/home.kv")
Builder.load_file("kv/reminder.kv")
Builder.load_file("kv/progress.kv")
Builder.load_file("kv/login_section.kv")


# Screen manager
class ScreenManagement(ScreenManager):
    pass


class Functions(BoxLayout, Screen):
    # Functions to navigate between interfaces
    def home_page(self):
        self.manager.current = "home"

    def reminder_page(self):
        self.manager.current = "reminder"

    def progress_page(self):
        self.manager.current = "progress"

    def login_section_page(self):
        self.manager.current = "login_section"


# App structure
class Home(Functions):
    def login_button(self, name):
        # Rename the button
        self.ids.login_section.text = name


class Reminder(Functions):
    def send_notification(self):
        notification.notify(
            title="AquaAlert - Reminder",
            message="Don't forget to drink water 😁!",
            app_icon="assets/images/logo.ico"
        )

    def notification(self):
        try:
            self.ids.error_message_1.text = ""
            self.ids.error_message_2.text = ""
            time = int(self.ids.time.text)

            timer(time)
            self.send_notification()
            pygame.mixer.music.load("assets/audio/notification.mp3")
            pygame.mixer.music.play()            

        except Exception as e:
            self.ids.error_message_1.text = "Unexpected"
            self.ids.error_message_2.text = "Value"
            print(f"Unexpected error: {e}")


class Progress(Functions):
    def water_amount(self, button):
        number = int(button.text[0:2])
        if number != 8:
            button.text = f"{str(number + 1)} / 8"
            return

        button.text = "0 / 8"


class LoginSection(Functions):
    def save_data(self): 
        try:
            self.ids.error_message_1.text = ""
            self.ids.error_message_2.text = ""
            
            # Create and connect to remote database
            load_dotenv()
            client = MongoClient(
                os.getenv("MONGO_KEY"), 
                server_api=ServerApi("1")
            )
            db = client["AquaAlert"]
            collection = db["User"]

            # Get user data
            name = self.ids.name.text
            password = self.ids.password.text

            if not name or not password:
                print("Error: Both fields must be filled.")
                return

            # Insert data
            document = {"Name": name, "Password": password}
            collection.insert_one(document)

            # Redirect to Home page
            home_screen = self.manager.get_screen("home")
            home_screen.login_button(name)

            self.home_page()
            print("The connection was successful!")

        except Exception as e:
            self.ids.error_message.text = "Connection error"
            return f"Unexpected error: {e}"


# Main application
class AquaAlert(App):
    title = "AquaAlert"

    def on_start(self):
        self.icon = "assets/images/logo.png"
        super().on_start()

    def build(self):
        return ScreenManagement()


if __name__ == "__main__":
    AquaAlert().run()
