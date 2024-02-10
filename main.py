from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout

class MainGridLayout(GridLayout):
    pass

class MainApp(App):
    def build(self):
        return Builder.load_file("main.kv")
    
if __name__ == "__main__":
    MainApp().run()