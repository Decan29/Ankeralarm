import json
from plyer import gps
from random import random
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.graphics import Line
from kivy.graphics import Color
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivy_garden.mapview import MapSource
from kivymd.uix.button import MDFlatButton
from kivy_garden.mapview import MapMarkerPopup, MapMarker
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton

from kivy.clock import Clock
from kivy.uix.image import Image

class MyToggleButton(MDFlatButton, MDToggleButton):
    pass

class MainApp(MDApp):
    def __init__(self, **kwargs):
        self.title = "Ankeralarm"
        super().__init__(**kwargs)
    
    def build(self):
        screen = Builder.load_file("windowsmd.kv")
        return screen
    
    def set_map_source(self):
        my_map_source = MapSource(
            url='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            min_zoom=8,
            max_zoom=19,
            attribution='Map data  © OpenStreetMap contributors'
        )
        self.mapview.map_source = my_map_source

    # def drawCircle(self):
    #     lat=49.566848
    #     lon=77.377053
    #     zoom = 8
    #     radius = 500

    #     self.lat = lat
    #     self.lan = lon
    #     self.offcenter = 48
        
    #     self.marker = MapMarker(lat=self.lat, lon=self.lan, source='Goku.jpg')
        
    #     self.root.ids.mapview.add_widget(self.marker)

    #     with self.root.canvas:
    #         Color(1,0,0,1)
    #         self.line = Line(circle=(self.marker.pos[0]+self.offcenter, self.marker.pos[1]+self.offcenter, 200), width=4)
    #     Clock.schedule_interval(self.update_circle, 1/500)

    #     return
    
    # def update_circle(self, *args):
    #     self.line.circle = self.marker.pos[0]+self.offcenter, self.marker.pos[1]+self.offcenter, 200
    #     # self.centerMap(lat=self.marker.lat, lon=self.marker.lon, zoom=8)
    #     coord = self.root.ids.mapview.get_latlon_at(self.marker.pos[0]+200, self.marker.pos[1]+200)
    #     print("lat/lon:", coord)
    #     print("Difference:", coord[0]-49.566848, coord[1]-77.377053)
    #     # disable zoom
    #     self.root.ids.mapview.zoom = 8
    #     # print("circle:",self.line.circle[0], self.line.circle[1])
    #     # print("marker:",self.marker.pos[0], self.marker.pos[1])
    #     # self.isInside(self.line.circle[0], self.line.circle[1], 200, self.marker.pos[0]+200, self.marker.pos[1]+200)

    # def isInside(self, circle_x, circle_y, rad, x, y, *args):
    #     if ((x - circle_x) * (x - circle_x) + (y - circle_y) * (y - circle_y) <= rad * rad):
    #         print("inside")
    #     else:
    #         print("outside")
        
    # def centerMap(self, lat=49.566848, lon=77.377053, zoom=8):
    #     self.root.ids.mapview.zoom = zoom
    #     self.root.ids.mapview.center_on(lat, lon)
    #     return

    # def radiuserhoehen(self):
    #     #Zugriff auf das Widget mit der id 'radius'
    #     radius_widget = self.root.ids.radius
    #     #Erhöhen des aktuellen Wertes um 1
    #     radius_widget.text = str(int(radius_widget.text) + 1)

    # def radiusverringern(self):
    #     # Zugriff auf das Widget mit der id 'radius'
    #     radius_widget = self.root.ids.radius
    #     # Verringere den aktuellen Wert um 1
    #     radius_widget.text = str(int(radius_widget.text) - 1)
    
    # def dateiSchreiben(self):
    #     radius_widget = self.root.ids.radius.text
    #     spinner_widget = self.root.ids.sound_spinner.text

    #     dictionary = {
    #     "Bereich": "Einstellungen",
    #     "Radius": radius_widget,
    #     'Audio Data': spinner_widget
    #     }
    #     with open (".\daten.json", "w") as file:
    #         json.dump(dictionary,file)

    # def toggle_function(self):
    #     # Umschaltende Logik, die entscheidet, welche Funktion aufgerufen wird
    #     if self.root.ids.launchButton.state == 'normal':
    #         self.drawLine()
    #     else:
    #         print("test")

    # def get_gps(self, *args):
    #     gps.configure(on_location=self.on_location)
    #     gps.start()

    # def on_location(self, **kwargs):
    #     print('Latitude: ', kwargs['lat'], 'Longitude: ', kwargs['lon'])
    #     self.map.lat = kwargs['lat']
    #     self.map.lon = kwargs['lon']
    #     gps.stop()

    # def frage_nach_location(self):
    #     # Erstellen eines Dialogs, um den Benutzer zu fragen, ob er seinen Standort teilen möchte
    #     dialog = MDDialog(
    #          title="Standortfreigabe",
    #          text="Möchten Sie Ihren Standort teilen?",
    #          buttons=[
    #              MDFlatButton(
    #                 text="JA",
    #                  on_release=self.get_gps
    #              ),
    #              MDFlatButton(
    #                  text="NEIN",
    #                  on_release=self.close_dialog
    #              )
    #          ]
    #      )
    #     dialog.open()

    # def schliesse_dialog(self, instance):
        # Schließen des Dialogs
        instance.parent.parent.parent.dismiss()

class CustomMarker(MapMarkerPopup):
    def __init__(self, **kwargs):
        super(CustomMarker, self).__init__(**kwargs)

        with self.canvas:
            self.image = Image(source='Goku.jpg')
            self.image.pos = self.pos[0] + 12, self.pos[1] + 12

if __name__ == "__main__":
    MainApp().run()