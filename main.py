from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen

class MainApp(App):
    def build(self):
        return Builder.load_file("windows.kv")
    
class MainWindow(Screen):
    pass
class SettingsWindow(Screen):
    pass
class WindowManager(ScreenManager):
    pass
    
if __name__ == "__main__":
    MainApp().run()