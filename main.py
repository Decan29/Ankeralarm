import json
import math
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.graphics import Color, Line
from kivy_garden.mapview import MapSource
from kivymd.uix.button import MDFlatButton
from kivy_garden.mapview import MapMarkerPopup, MapMarker
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton

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

    def drawCircle(self):
        lat= 48.4715279
        lon= 7.9512879

        self.lat = lat
        self.lan = lon
        self.offcenter = 21
        
        self.marker_anchor = MapMarker(lat=self.lat, lon=self.lan, source='src/images/anchor_32.png')
        self.root.ids.mapview.add_widget(self.marker_anchor)
        
        # Boot immer bei GPS Position
        self.marker_boat = MapMarker(lat=self.marker_anchor.lat, lon=self.marker_anchor.lon, source='src/images/boat_32.png')
        self.root.ids.mapview.add_widget(self.marker_boat)

        self.calculate_distance()

        with self.root.canvas:
            Color(1,0,0,1)
            self.line = Line(circle=(self.marker_anchor.pos[0]+self.offcenter, self.marker_anchor.pos[1]+self.offcenter, int(self.root.ids.radius.text)*self.pixel_per_meter), width=2)
        self.clock = Clock.schedule_interval(self.update_circle, 1/500)

        return
    
    def MoveAnchor(self, key):
        print(key)
        match key:
            case 'up':
                self.marker_anchor.lat +=0.0001
            case 'left':
                self.marker_anchor.lon -=0.0001
            case 'right':
                self.marker_anchor.lon += 0.0001
            case 'down':
                self.marker_anchor.lat -= 0.0001
            case _:
                return
        
        self.root.ids.mapview.trigger_update('full')


        # hoch und runter
        #self.marker_anchor.lat

    def calculate_distance(self):
        current_width_x=self.root.size[0]

        # hole Koordinaten vom linken Rand
        left_coord = self.root.ids.mapview.get_latlon_at(0,0,self.root.ids.mapview.zoom)
        # hole Koordinaten vom rechten Rand
        right_coord = self.root.ids.mapview.get_latlon_at(current_width_x,0,self.root.ids.mapview.zoom)

        # Entfernungsberechnung
        dx = 71.5 * (left_coord[1] - right_coord[1])
        dy = 111.3 * (left_coord[0] - right_coord[0])

        distance = math.sqrt((dx * dx) + (dy * dy))

        # Umrechnung von Fensterbreite in Pixel und Distanz in Meter zu Pixel Pro Meter 
        self.pixel_per_meter = (current_width_x / distance) / 1000

    def update_circle(self, *args):
        self.calculate_distance()
        self.line.circle = self.marker_anchor.pos[0]+self.offcenter, self.marker_anchor.pos[1]+self.offcenter, int(self.root.ids.radius.text)*self.pixel_per_meter
        coord = self.root.ids.mapview.get_latlon_at(self.marker_anchor.pos[0] + int(self.root.ids.radius.text), self.marker_anchor.pos[1] + int(self.root.ids.radius.text))
        print("Anchor lon", self.marker_anchor.lon)
        # self.isInside(self.line.circle[0], self.line.circle[1], 200, self.marker.pos[0]+200, self.marker.pos[1]+200)
        self.isInside(self.line.circle[0], self.line.circle[1], int(self.root.ids.radius.text)*self.pixel_per_meter, self.marker_boat.pos[0], self.marker_boat.pos[1])
    # check if point is inside circle
    def isInside(self, circle_x, circle_y, rad, x, y, *args):
        if ((x - circle_x) * (x - circle_x) + (y - circle_y) * (y - circle_y) <= rad * rad):
            print("inside")
        else:
            print("outside")
        
    def centerMap(self, lat=48.4715279, lon=7.9512879, zoom=16):
        self.root.ids.mapview.zoom = zoom
        self.root.ids.mapview.center_on(lat, lon)
        return
    
    def Stop_Update_Circle(self):
        try:
            self.clock.cancel()
            self.line.circle = 0,0,0
        except AttributeError:
            print("AttributeError crash bei Stop_Update_Circle wurde abgefangen!")
        # self.root.canvas.clear()

    def radiuserhoehen(self):
        #Zugriff auf das Widget mit der id 'radius'
        self.radius_widget = self.root.ids.radius
        #Erhöhen des aktuellen Wertes um 1
        self.radius_widget.text = str(int(self.radius_widget.text) + 10)

    def radiusverringern(self):
        # Zugriff auf das Widget mit der id 'radius'
        self.radius_widget = self.root.ids.radius
        # Verringere den aktuellen Wert um 1
        self.radius_widget.text = str(int(self.radius_widget.text) - 10)
    
    def dateiSchreiben(self):
        self.radius_widget = self.root.ids.radius.text
        self.spinner_widget = self.root.ids.sound_spinner.text

        dictionary = {
        "Bereich": "Einstellungen",
        "Radius": self.radius_widget,
        'Audio Data': self.spinner_widget
        }
        with open ("src/json/daten.json", "w") as file:
            json.dump(dictionary,file)

    def toggle_function(self):
        # Umschaltende Logik, die entscheidet, welche Funktion aufgerufen wird
        if self.root.ids.launchButton.state == 'normal':
            self.drawLine()
        else:
            print("test")

    def schliesse_dialog(self, instance):
        # Schließen des Dialogs
        instance.parent.parent.parent.dismiss()

class CustomMarker(MapMarkerPopup):
    def __init__(self, **kwargs):
        super(CustomMarker, self).__init__(**kwargs)

        with self.canvas:
            self.image = Image(source='src/images/Goku.jpg')
            self.image.pos = self.pos[0] + 12, self.pos[1] + 12

if __name__ == "__main__":
    MainApp().run()