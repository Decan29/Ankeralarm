from kivy.lang import Builder
from kivymd.app import MDApp
from kivy_garden.mapview import MapView, MapSource
from kivy_garden.mapview.clustered_marker_layer import KDBush, Marker
from kivy_garden.mapview import MapLayer
from kivy_garden.mapview import MapMarkerPopup
from kivy.graphics import Line
from kivy.graphics import Canvas, Color, Ellipse, Rectangle
from kivy.graphics.context_instructions import Translate, Scale
from kivy.core.window import Window
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.widget import Widget
from plyer import gps
from kivy.clock import Clock
from random import random
import json

class MyToggleButton(MDFlatButton, MDToggleButton):
    pass


class MainApp(MDApp):
    def __init__(self, **kwargs):
        self.title = "Ankeralarm"
        super().__init__(**kwargs)
        self.get_gps()
    
    def build(self):      
        try:          
           Clock.schedule_interval(self.mapview.get_gps,  1)
        except:
            print("Failure to get gps_data")
        screen = Builder.load_file("windowsmd.kv")
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
    
    # def drawLine(self):
    #     lat=49.566848
    #     lon=77.377053
    #     zoom = 8
    #     radius = 500
    #     self.root.ids.mapview
    #     #print(self.root.ids)
    #     self.root.ids.mapview.zoom = zoom
    #     self.root.ids.mapview.center_on(lat, lon)

    #     self.mapview = self.root.ids.mapview
    #     self.set_map_source()
    #     x_pos = self.mapview.map_source.get_x(zoom, lon)
    #     y_pos = self.mapview.map_source.get_y(zoom, lat)

    #     # self.circle = Circle(x_pos, y_pos)
    #     # self.mapview.add_marker(self.circle)

    #     #circle_layer = Circle(x= x_pos, y=y_pos, canvas_width=Window.width, zoom=8)
    #     #self.root.ids.mapview.add_layer(circle_layer)

    #     circle = Circle(lat=lat, lon=lon)
    #     self.root.ids.mapview.add_marker(circle)
        

    #     print("x: ", x_pos, "y: ", y_pos)

    #     return self.mapview
    
    def radiuserhoehen(self):
        #Zugriff auf das Widget mit der id 'radius'
        radius_widget = self.root.ids.radius
        #Erhöhen des aktuellen Wertes um 1
        radius_widget.text = str(int(radius_widget.text) + 1)

    def radiusverringern(self):
        # Zugriff auf das Widget mit der id 'radius'
        radius_widget = self.root.ids.radius
        # Verringere den aktuellen Wert um 1
        radius_widget.text = str(int(radius_widget.text) - 1)
    
    def dateiSchreiben(self):
        radius_widget = self.root.ids.radius.text
        spinner_widget = self.root.ids.sound_spinner.text

        dictionary = {
        "Bereich": "Einstellungen",
        "Radius": radius_widget,
        'Audio Data': spinner_widget
        }
        with open (".\daten.json", "w") as file:
            json.dump(dictionary,file)

    def toggle_function(self):
        # Umschaltende Logik, die entscheidet, welche Funktion aufgerufen wird
        if self.root.ids.launchButton.state == 'normal':
            self.drawLine()
        else:
            print("test")


    def get_gps(self, *args):
        gps.configure(on_location=self.on_location)
        gps.start(minTime=1000, minDistance=0)

    def on_location(self, **kwargs):
            print('Latitude: ', kwargs['lat'], 'Longitude: ', kwargs['lon'])
            self.lat = kwargs.get('lat')
            self.lon = kwargs.get('lon')
             
    def get_gps_latitude(self):
        return self.root.ids.mapview.lat
         

    def get_gps_longitude(self):        
        return self.root.ids.mapview.lon
        

    def frage_nach_location(self):
        # Erstellen eines Dialogs, um den Benutzer zu fragen, ob er seinen Standort teilen möchte
        dialog = MDDialog(
             title="Standortfreigabe",
             text="Möchten Sie Ihren Standort teilen?",
             buttons=[
                 MDFlatButton(
                    text="JA",
                     on_release=self.get_gps
                 ),
                 MDFlatButton(
                     text="NEIN",
                     on_release=self.close_dialog
                 )
             ]
         )
        dialog.open()

    def schliesse_dialog(self, instance):
        # Schließen des Dialogs
        instance.parent.parent.parent.dismiss()


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