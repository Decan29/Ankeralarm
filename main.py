import json
import os
import math
from kivy.clock import Clock
from random import random
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.graphics import Line, Color
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivy.uix.image import Image
from kivy_garden.mapview import MapSource
from kivymd.uix.button import MDFlatButton
from kivy_garden.mapview import MapMarkerPopup, MapMarker
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivy.utils import platform
from kivy.uix.button import Button
# from kivy.uix.filechooser import FileChooserListView
# from kivy.uix.popup import Popup
from kivy.core.audio import SoundLoader


class MyToggleButton(MDFlatButton, MDToggleButton):
    pass

# class FileChooserPopup(Popup):
#     def __init__(self, **kwargs):
#         super(FileChooserPopup, self).__init__(**kwargs)
#         self.title = "Datei auswählen"
#         self.size_hint = (0.9, 0.9)
#         self.filechooser = FileChooserListView(filters=['*.mp3'])
#         self.filechooser.bind(on_selection=self.load_sound)
#         self.add_widget(self.filechooser)
    
#     def load_sound(self, instance, filename):
#         if instance:
#             sound = SoundLoader.load(os.path.join(instance.path, filename[0]))
#             self.root.ids.sound_spinner.text = filename
#             print("Ausgewählte Datei:", filename[0])
#             # Schließen Sie das Popup-Fenster
#             self.dismiss()
#             if sound:
#                 sound.play()

class MainApp(MDApp):
    def __init__(self, **kwargs):
        self.title = "Ankeralarm"
        super().__init__(**kwargs)
        self.marker = False
    
    def build(self):
        self.get_permission()
        screen = Builder.load_file("windowsmd.kv")
        return screen
    
    def get_permission(self):
         if platform == 'android':
            from android.permissions import Permission, request_permissions
            permissions = [Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION]
            request_permissions(permissions, self.permission_callback)
            return True
         else:
             return False 

    def permission_callback(self, permissions, results):
        if all(results):
            print("Permission granted")
            self.get_gps()
            self.centerMap(self.get_gps_latitude,self.get_gps_longitude)
        else:
            print("Permission denied")
    
    def set_map_source(self):
        my_map_source = MapSource(
            url='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            min_zoom=8,
            max_zoom=19,
            attribution='Map data  © OpenStreetMap contributors'
        )
        self.mapview.map_source = my_map_source

    def AddMarker(self, lat, lon):
        if self.marker:
            return
        
        # Boot immer bei GPS Position
        self.marker_boat = MapMarker(lat=lat, lon=lon, source='src/images/boat_32.png')
        self.root.ids.mapview.add_widget(self.marker_boat)

        self.marker_anchor = MapMarker(lat=self.marker_boat.lat, lon=self.marker_boat.lon, source='src/images/anchor_32.png')
        self.root.ids.mapview.add_widget(self.marker_anchor)

        self.marker = True

    def drawCircle(self):
        lat= 48.4715279
        lon= 7.9512879
        self.offcenter = 21

        #self.on_location()
        self.AddMarker(lat=lat, lon=lon)

        self.calculate_distance()

        with self.root.canvas:
            Color(1,0,0,1)
            self.line = Line(circle=(self.marker_anchor.pos[0]+self.offcenter, self.marker_anchor.pos[1]+self.offcenter, int(self.root.ids.radius.text)*self.pixel_per_meter), width=2)
        self.clock = Clock.schedule_interval(self.update_circle, 1/500)

        return
    
    def MoveAnchor(self, direction):
        if direction == 'up':
            self.marker_anchor.lat +=0.0001
        if direction == 'left':
            self.marker_anchor.lon -=0.0001
        if direction == 'right':
            self.marker_anchor.lon += 0.0001
        if direction == 'down':
            self.marker_anchor.lat -= 0.0001
        
        self.root.ids.mapview.trigger_update('full')

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
        #coord = self.root.ids.mapview.get_latlon_at(self.marker_anchor.pos[0] + int(self.root.ids.radius.text), self.marker_anchor.pos[1] + int(self.root.ids.radius.text))
        #self.on_location()
        
        self.isInside(self.marker_anchor.pos[0]+self.offcenter, self.marker_anchor.pos[1]+self.offcenter, int(self.root.ids.radius.text)*self.pixel_per_meter, self.marker_boat.pos[0], self.marker_boat.pos[1])
     
        print("circle: ", self.line.circle[0], self.line.circle[1])
    
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
            self.root.ids.mapview.remove_widget(self.marker_anchor)
            self.root.ids.mapview.remove_widget(self.marker_boat)
            self.marker = False
        except AttributeError:
            print("AttributeError crash bei Stop_Update_Circle wurde abgefangen!")
        # self.root.canvas.clear()

    def radiuserhoehen(self):
        #Zugriff auf das Widget mit der id 'radius'
        self.radius_widget = self.root.ids.radius
        #Erhöhen des aktuellen Wertes um 10
        self.radius_widget.text = str(int(self.radius_widget.text) + 10)

    def radiusverringern(self):
        # Zugriff auf das Widget mit der id 'radius'
        self.radius_widget = self.root.ids.radius
        # Verringere den aktuellen Wert um 10
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

    def choose_sound(self):
        #TODO ALARM mp3 übergeben.
        wahlsound = self.root.ids.sound_spinner.text
        sound = SoundLoader.load(os.path.join('alarm.mp3'))
        if wahlsound == "Alarm1":
            sound = SoundLoader.load(os.path.join('alarm1.mp3'))
            print("Alarm")
        elif wahlsound == "Alarm2":
            sound = SoundLoader.load(os.path.join('alarm2.mp3'))           
            print("Alarm2")
        #else:
            #self.show_filechooser(audiotext)

    def toggle_function(self):
        # Umschaltende Logik, die entscheidet, welche Funktion aufgerufen wird
        if self.root.ids.launchButton.state == 'normal':
            self.drawLine()
            self.root.ids.launchButton.text = "Stop"
        else:
            print("test")

    def get_gps(self, *args):
        if platform == 'android' or platform == 'ios':
            from plyer import gps   
            try:                           
                gps.configure(on_location=self.on_location, on_status=self.on_status)
                gps.start(minTime=1000, minDistance=0)
            except:
                import traceback
                traceback.print_exc()
                self.gps_status= "GPS is not implemented for your platform"
           
    def on_status(self, general_status, status_message):
        if general_status== 'provider-enabled':
            pass
        else:
            self.open_gps_access_popup()

    def open_gps_access_popup(self):
        dialog = MDDialog(title="GPS Error", text= "Sie müssen die GPS daten aktivieren.")
        dialog.size_hint = [.8,.8]
        dialog.pos_hint = {'center_x':.5,'center_y':.5}
        dialog.open()

    def on_location(self, *args, **kwargs):

        self.gps_latitude = kwargs.get('lat', None)
        self.gps_longitude = kwargs.get('lon', None)

        if self.gps_latitude and self.gps_longitude:
            print(f"Latitude: {self.gps_latitude}, Longitude: {self.gps_longitude}")

    #         if hasattr(self, 'user_marker'):
    #             # Update existing marker
    #             self.user_marker.lat = latitude
    #             self.user_marker.lon = longitude
    #             self.root.ids.mapview.lat = latitude
    #             self.root.ids.mapview.lon = longitude

    #         else:
    #             # Create new marker
    #             self.user_marker = MapMarker(lat=latitude, lon=longitude)
    #             self.mapview.add_widget(self.user_marker)  # Add the marker to the mapview
    #             self.root.ids.mapview.lat = latitude
    #             self.root.ids.mapview.lon = longitude
    #         # Remove old markers (optional)
    #         self.remove_old_markers(lat=latitude, lon=longitude)
    #         self.centerMap(latitude,longitude)

    # def remove_old_markers(self):
    #     # Remove markers other than the user's marker
    #     for marker in self.mapview.children:
    #         if isinstance(marker, MapMarker) and marker != self.user_marker:
    #             self.mapview.remove_widget(marker)

             
    def get_gps_latitude(self):
        return self.root.ids.mapview.lat
         

    def get_gps_longitude(self):        
        return self.root.ids.mapview.lon       

class CustomMarker(MapMarkerPopup):
    def __init__(self, **kwargs):
        super(CustomMarker, self).__init__(**kwargs)

        with self.canvas:
            self.image = Image(source='src/images/Goku.jpg')
            self.image.pos = self.pos[0] + 12, self.pos[1] + 12

if __name__ == "__main__":
    MainApp().run()