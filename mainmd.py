from kivy.lang import Builder
from kivymd.app import MDApp
from kivy_garden.mapview import MapView

class MainApp(MDApp):
    def build(self):
       return Builder.load_file("windowsmd.kv")
    
if __name__ == "__main__":
    MainApp().run()