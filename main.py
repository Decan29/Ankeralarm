import os
import json
import math
from random import random
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.utils import platform
from kivy.uix.image import Image
from kivy.core.window import Window
from kivymd.uix.label import MDLabel
from kivy.graphics import Line, Color
from kivymd.uix.dialog import MDDialog
from kivy.core.audio import SoundLoader
from kivy_garden.mapview import MapSource
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy_garden.mapview import MapMarker, MapMarkerPopup
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
# from kivy.uix.filechooser import FileChooserListView
# from kivy.uix.popup import Popup

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
        self.dialog = None
        self.isProgramStopped = True
        self.useOnce = True
        Clock.schedule_once(self.get_permission, 0)
        Clock.schedule_once(self.ClassThatDoesEverything, 1)
    
    def build(self):
        screen = Builder.load_file("windowsmd.kv")
        # if self.get_permission:
        #     print("Rechte wurden erteilt!")
            # try:
            #     self.centerMap(self.gps_latitude,self.gps_longitude)
            # except:
            #     print(f"Fehler Werte kaputt oder anderweitiger fehler. Latitude: {self.gps_latitude},Longitude: {self.gps_longitude}")
        return screen
    
    def get_permission(self, dt):
         if platform == 'android':
            from android.permissions import Permission, request_permissions
            permissions = [Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION]
            request_permissions(permissions, self.permission_callback)
            return True
         else:
             return False 

    def permission_callback(self, permissions, results):
        if all(results):
            print("Rechte erteilt")
            self.GetGps()
        else:
            print("Rechte abgelehnt")
    
    # def set_map_source(self):
    #     my_map_source = MapSource(
    #         url='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    #         min_zoom=16,
    #         max_zoom=19,
    #         attribution='Map data  © OpenStreetMap contributors'
    #     )
    #     self.mapview.map_source = my_map_source
    #     self.CenterMap(self.gps_latitude, self.gps_longitude, 16)
    #     print("SETTET MAP SOURCE LAN BRO ASDKLHAKLJHFELKJHFLKJHEFKLJSDLKFJHSLDKFLSKDJFKSDLJFFFFFFFFSKLDJHFKLJSDHFLKJSHDFKJSHD")

    def ToggleProgram(self):
        if self.isProgramStopped:
            self.DrawCircle()
            self.root.ids.launchButton.text = "Stop"
            self.isProgramStopped = False
            return
        if not self.isProgramStopped:
            self.StopUpdateCircle()
            self.root.ids.launchButton.text = "Start"
            self.isProgramStopped = True
            return

    def AddMarker(self):
        if self.marker:
            return

        self.marker_anchor = MapMarker(lat=self.marker_boat.lat, lon=self.marker_boat.lon, source='src/images/anchor_32.png')
        self.root.ids.mapview.add_widget(self.marker_anchor)

        self.marker = True

    def UpdateBoat(self):
        if platform == 'win':
            self.marker_boat.lat = 48.4715279
            self.marker_boat.lon = 7.9512879
        elif platform == 'android':
            self.marker_boat.lat = self.gps_latitude
            self.marker_boat.lon = self.gps_longitude
        self.root.ids.mapview.trigger_update('full')

    def DrawCircle(self):
        self.offcenter = 21

        if platform == 'win':
            # lat = 48.4715279
            # lon = 7.9512879
            lat = 50.0
            lon = 8.0
            print("indo")
        elif platform == 'android':
            lat = self.gps_latitude
            lon = self.gps_longitude

        try:
            self.marker_boat.lat = lat
            self.marker_boat.lon = lon
        except AttributeError:
            print("Marker Boot bei DrawCircle wurde nicht gefunden!")
            return

        self.CenterMap(lat=lat, lon=lon)
        self.AddMarker()
        self.CalculateDistance()

        with self.root.canvas:
            Color(1,0,0,1)
            self.line = Line(circle=(self.marker_anchor.pos[0]+self.offcenter, self.marker_anchor.pos[1]+self.offcenter, int(self.root.ids.radius.text)*self.pixel_per_meter), width=2)

        self.clock = Clock.schedule_interval(self.UpdateCircle, 1/250)

        return
    
    def MoveAnchor(self, direction):
        try:
            if direction == 'up':
                self.marker_anchor.lat +=0.0001
            if direction == 'left':
                self.marker_anchor.lon -=0.0001
            if direction == 'right':
                self.marker_anchor.lon += 0.0001
            if direction == 'down':
                self.marker_anchor.lat -= 0.0001
        
            self.root.ids.mapview.trigger_update('full')
        except AttributeError:
            print("Anchor-Objekt bei MoveAnchor nicht gefunden!")

    def CalculateDistance(self):
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

    def UpdateCircle(self, *args):
        self.CalculateDistance()
        self.line.circle = self.marker_anchor.pos[0]+self.offcenter, self.marker_anchor.pos[1]+self.offcenter, int(self.root.ids.radius.text)*self.pixel_per_meter
        #self.UpdateBoat()
        self.IsInsideCircle(self.marker_anchor.pos[0]+self.offcenter, self.marker_anchor.pos[1]+self.offcenter, int(self.root.ids.radius.text)*self.pixel_per_meter, self.marker_boat.pos[0], self.marker_boat.pos[1])
         
    # check if point is inside circle
    def IsInsideCircle(self, circle_x, circle_y, rad, x, y, *args):
        if ((x - circle_x) * (x - circle_x) + (y - circle_y) * (y - circle_y) <= rad * rad):
            return
        else:
            self.StopUpdateCircle()
            self.ShowDialog()
            self.PlaySound()
            return
    
    def ShowDialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="ALARM!",
                type="custom",
                md_bg_color= "#880015",
                content_cls=MDBoxLayout(
                    Image(source='src/images/error.png'),
                    MDLabel( 
                        text='IHR SCHIFF TREIBT AB!',
                        halign="center"
                    ),
                    orientation="vertical",
                    spacing="12dp",
                    size_hint_y=None,
                    height="120dp"
                ),
                buttons=[
                    MDFlatButton(
                        text="CLOSE",
                        on_release=self.CloseDialog,
                        
                    )
                ],
            )
        self.dialog.open()

    def CloseDialog(self, *args):
        self.dialog.dismiss()
        self.DrawCircle()
        self.sound.stop()

    def CenterMapButton(self):
        if platform == 'win':
            lat =  48.4715279
            lon = 7.9512879
            self.CenterMap(lat, lon, 16)
        elif platform == 'android':
            self.CenterMap(self.gps_latitude, self.gps_longitude, zoom=19)

    def CenterMap(self, lat, lon, zoom=19):
        self.root.ids.mapview.zoom = zoom
        self.root.ids.mapview.center_on(lat, lon)
        return
    
    def StopUpdateCircle(self):
        try:
            self.clock.cancel()
            self.line.circle = 0,0,0
            self.root.ids.mapview.remove_widget(self.marker_anchor)
            # self.root.ids.mapview.remove_widget(self.marker_boat)
            self.marker = False
        except AttributeError:
            print("AttributeError crash bei Stop_Update_Circle wurde abgefangen!")
        # self.root.canvas.clear()

    def IncreaseRadius(self):
        #Zugriff auf das Widget mit der id 'radius'
        self.radius_widget = self.root.ids.radius
        #Erhöhen des aktuellen Wertes um 10
        self.radius_widget.text = str(int(self.radius_widget.text) + 10)

    def DecreaseRadius(self):
        # Zugriff auf das Widget mit der id 'radius'
        self.radius_widget = self.root.ids.radius
        # Verringere den aktuellen Wert um 10
        self.radius_widget.text = str(int(self.radius_widget.text) - 10)
    
    def WriteToFile(self):
        self.radius_widget = self.root.ids.radius.text
        self.spinner_widget = self.root.ids.sound_spinner.text

        dictionary = {
        "Bereich": "Einstellungen",
        "Radius": self.radius_widget,
        'Audio Data': self.spinner_widget
        }
        with open ("src/json/daten.json", "w") as file:
            json.dump(dictionary,file)

    def LoadSettings(self):
        f = open("src/json/daten.json")
        data = json.load(f)
        self.root.ids.radius.text = data['Radius']
        self.root.ids.sound_spinner.text = data['Audio Data']
        f.close()

    def PlaySound(self):
        wahlsound = self.root.ids.sound_spinner.text
        soundNamenListe =["Alarm1","Alarm2","Alarm3"]
        if wahlsound in soundNamenListe:
            self.sound = SoundLoader.load(os.path.join(f'src/sounds/{wahlsound}.MP3'))
            self.sound.play()

    def GetGps(self, *args):
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
            self.OpenGpsAccessPopup()

    def OpenGpsAccessPopup(self):
        dialog = MDDialog(title="GPS Error", text= "Sie müssen die GPS daten aktivieren.")
        dialog.size_hint = [.8,.8]
        dialog.pos_hint = {'center_x':.5,'center_y':.5}
        dialog.open()

    def on_location(self, **kwargs):
        self.gps_latitude = kwargs.get('lat', None) 
        self.gps_longitude = kwargs.get('lon', None)

        if self.useOnce:
            self.root.ids.mapview.lat = self.gps_latitude
            self.root.ids.mapview.lon = self.gps_longitude
            self.CenterMap(self.gps_latitude, self.gps_longitude)
            self.useOnce = False
                        
    def AddBoatMarker(self):
        if platform == 'win':
            lat = 50.0
            lon = 8.0
        elif platform == 'android':
            lat = self.gps_latitude
            lon = self.gps_longitude

        if not hasattr(self, 'marker_boat'):
            self.marker_boat = MapMarker(lat=lat, lon=lon, source='src/images/boat_32.png')
            self.root.ids.mapview.add_widget(self.marker_boat)
            
    def ClassThatDoesEverything(self, dt):
        if platform == 'win':
            lat = 50.0
            lon = 8.0
        elif platform == 'android':
            lat = self.gps_latitude
            lon = self.gps_longitude

        self.AddBoatMarker()
        self.CenterMap(lat, lon)
        
if __name__ == "__main__":
    MainApp().run()