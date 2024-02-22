from kivy.lang import Builder
from kivymd.app import MDApp
from kivy_garden.mapview import MapView

from kivy.graphics import Line
from kivy_garden.mapview import MapMarkerPopup
from kivy.graphics import Color
from kivy.graphics.context_instructions import Translate, Scale
from kivy.core.window import Window

class MainApp(MDApp):
    def build(self):
        #return CustomMapView(zoom=15, lat=50.6394, lon=3.0572)
        self.map = MapView(zoom=15, lat=49.566848, lon=77.377053, double_tap_zoom=True)
        self.circle = Circle(lat=49.566848, lon=77.377053)
        self.map.add_marker(self.circle)
        return Builder.load_file("windowsmd.kv")
        # return self.map
# class CustomMapView(MapView):
#     def on_touch_down(self, touch):
#         super(CustomMapView, self).on_touch_down(touch)
#         with self.canvas:
#             Line(points=[touch.x, touch.y, touch.x, touch.y + 100], width=2)
            
class Circle(MapMarkerPopup):
    def __init__(self, **kwargs):
        super(Circle, self).__init__(**kwargs)
        with self.canvas:
            Color(.6,0,0,.6)
            Line(circle=(Window.size[1] /2, Window.size[0]/2, 100), width=200)

if __name__ == "__main__":
    MainApp().run()