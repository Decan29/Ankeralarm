from kivy.lang import Builder
from kivymd.app import MDApp
from kivy_garden.mapview import MapView, MapSource

from kivy.graphics import Line
from kivy_garden.mapview import MapMarkerPopup
from kivy.graphics import Canvas, Color, Ellipse, Rectangle
from kivy.graphics.context_instructions import Translate, Scale
from kivy.core.window import Window
from kivy_garden.mapview.clustered_marker_layer import KDBush, Marker
from kivy.uix.widget import Widget
from kivy_garden.mapview import MapLayer
from kivy.properties import NumericProperty, ListProperty
from random import random

class MainApp(MDApp):
    def __init__(self, **kwargs):
        self.title = "Ankeralarm"
        super().__init__(**kwargs)

    
    def build(self):
        screen = Builder.load_file("windowsmd.kv")
        
        #self.circle = Circle(lat=49.566848, lon=77.377053)
        #self.map.add_marker(self.circle)
        return screen
    
    def set_map_source(self):
        my_map_source = MapSource(
            url='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            min_zoom=0,
            max_zoom=19,
            attribution='Map data  © OpenStreetMap contributors'
        )
        self.mapview.map_source = my_map_source
    
    def drawLine(self):
        lat=49.566848
        lon=77.377053
        zoom = 8
        radius = 500
        self.root.ids.mapview
        #print(self.root.ids)
        self.root.ids.mapview.zoom = zoom
        self.root.ids.mapview.center_on(lat, lon)

        self.mapview = self.root.ids.mapview
        self.set_map_source()
        x_pos = self.mapview.map_source.get_x(zoom, lon)
        y_pos = self.mapview.map_source.get_y(zoom, lat)

        # self.circle = Circle(x_pos, y_pos)
        # self.mapview.add_marker(self.circle)

        #circle_layer = Circle(x= x_pos, y=y_pos, canvas_width=Window.width, zoom=8)
        #self.root.ids.mapview.add_layer(circle_layer)

        circle = Circle(lat=lat, lon=lon)
        self.root.ids.mapview.add_marker(circle)
        

        print("x: ", x_pos, "y: ", y_pos)

        return self.mapview

class Circle(MapMarkerPopup):
    def __init__(self,**kwargs):
        super(Circle, self).__init__(**kwargs)
        with self.canvas:
            self.canvas.clear()
            Color(1,0,0,1)
            Line(circle=(kwargs["lat"]+500, kwargs["lon"]+500, 500), width=2.0)
            print("Self:",kwargs["lat"], kwargs["lon"])


if __name__ == "__main__":
    MainApp().run()