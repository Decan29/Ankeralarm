import json
from kivy.clock import Clock
from random import random
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.graphics import Line, Ellipse
from kivy.graphics import Color
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivy_garden.mapview import MapSource
from kivymd.uix.button import MDFlatButton
from kivy_garden.mapview import MapMarkerPopup, MapMarker
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivy.utils import platform
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup

from kivy.clock import Clock
from kivy.uix.image import Image

class MyToggleButton(MDFlatButton, MDToggleButton):
    pass

class FileChooserPopup(Popup):
    def __init__(self, **kwargs):
        super(FileChooserPopup, self).__init__(**kwargs)
        self.title = "Datei auswählen"
        self.size_hint = (0.9, 0.9)
        self.filechooser = FileChooserListView()
        self.add_widget(self.filechooser)

class MainApp(MDApp):
    def __init__(self, **kwargs):
        self.title = "Ankeralarm"
        super().__init__(**kwargs)
    
    def build(self):
        self.get_permission 
        screen = Builder.load_file("windows.kv")
        #self.map.add_marker(self.circle)          
        return screen
    
    def set_filechooser(self):
        self.root.ids.sound_spinner.bind(text=self.show_filechooser)  

    def show_filechooser(self, text):
        if text == 'Datei auswählen':
            popup = FileChooserPopup()
            popup.open()
    
    def get_permission(self):
         if platform == 'android':
            from android.permissions import Permission, request_permissions
            permissions = [Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION]
            request_permissions(permissions, self.permission_callback) 

    def permission_callback(self, permissions, results):
        if all(results):
            print("Permission granted")
            self.get_gps()
        else:
            print("Permission denied")

   
    def set_map_source(self):
         my_map_source = MapSource(
            url='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            min_zoom=0,
            max_zoom=19,
            attribution='Map data  © OpenStreetMap contributors'
         )
         self.mapview.map_source = my_map_source
    
    def drawCircle(self):
        lat=self.root.ids.mapview.lat
        lon=self.root.ids.mapview.lon
        zoom = 8
        radius = str(int(self.root.ids.radius.text))

        self.lat = lat
        self.lan = lon
        self.offcenter = 48
        
        self.marker = MapMarker(lat=self.lat, lon=self.lan, source='Goku.jpg')
        self.markerbtn = Button(size=(self.root.width*0.2, self.root.height*0.05), pos=(self.marker.pos[0], self.marker.pos[1]))
        self.marker = CustomMarker(lat=self.lat, lon=self.lan, source='transparent.png')
        self.markerbtn = Image(source="Goku.jpg")
        self.marker.add_widget(self.markerbtn)
        self.root.ids.mapview.add_widget(self.marker)
        with self.root.canvas:
            Color(1,0,0,1)
            self.line = Line(circle=(self.marker.pos[0]+self.offcenter, self.marker.pos[1]+self.offcenter, 200), width=4)
        Clock.schedule_interval(self.update_circle, 1/500)

        return
    
    def update_circle(self, *args):
        self.line.circle = float(self.marker.pos[0])+self.offcenter, float(self.marker.pos[1]+self.offcenter), 200
        print("circle:",self.line.circle[0], self.line.circle[1])
        print("marker:",self.marker.pos[0], self.marker.pos[1])
        self.isInside(self.line.circle[0], self.line.circle[1], 200, self.marker.pos[0]+200, self.marker.pos[1]+200)

    def isInside(self, circle_x, circle_y, rad, x, y, *args):
        if ((x - circle_x) * (x - circle_x) + (y - circle_y) * (y - circle_y) <= rad * rad):
             print("inside")
        else:
             print("outside")
        


    def centerMap(self,lat, lon, zoom=8):
        self.root.ids.mapview.zoom = zoom
        self.root.ids.mapview.center_on(lat, lon)

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

        latitude = kwargs.get('lat', None)
        longitude = kwargs.get('lon', None)
        self.centerMap(lat= latitude, lon= longitude)
        if latitude and longitude:
            print(f"Latitude: {latitude}, Longitude: {longitude}")

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
            self.image = Image(source='Goku.jpg')
            self.image.pos = self.pos[0] + 12, self.pos[1] + 12

if __name__ == "__main__":
    MainApp().run()