from kivymd.app import MDApp
from kivy.lang import Builder

from kivy.core.window import Window

from time import strftime
from kivy.clock import Clock
from searchpopupmenu import SearchPopupMenu
import pytz
from kivy.utils import platform
from kivymd.uix.dialog import MDDialog


from datetime import datetime
if platform == 'macosx':

    Window.size = (450, 750)



class OneApp(MDApp):
    '''

    KIVYMD SYNTAX FOR 1.O.0.DEV0
    '''
    search_menu = None
    def __init__(self):

        super().__init__()




        self.theme_cls.primary_palette = 'Orange'
        self.theme_cls.primary_style = 'Light'
        self.title = 'StopWatch'
        self.has_centered_map = False

        self.sw_seconds = 0
        self.sw_started = False
        self.local = True
        self.region = None

        # self.start_service()



        '''USING SERVICE TO MAKE SURE THAT STOPWATCH STILL COUNTING WHEN WE ARE OPENING OTHER APPS'''

        self.screen = Builder.load_file('main.kv')

        self.screen = Builder.load_file('main.kv')

    def centering_map(self,*args):
        # Get a reference to GpsBlinker, then call blink()

        # Request permissions on Android
        if platform == 'android':
            from android.permissions import Permission, request_permissions
            def callback(permission, results):
                if all([res for res in results]):
                    print("Got all permissions")
                    from plyer import gps
                    gps.configure(on_location=self.update_blinker_position,
                                  on_status=self.on_auth_status)
                    gps.start(minTime=1000, minDistance=0)
                else:
                    print("Did not get all permissions")

            request_permissions([Permission.ACCESS_COARSE_LOCATION,
                                 Permission.ACCESS_FINE_LOCATION], callback)

        # Configure GPS
        if platform == 'ios':
            from plyer import gps
            gps.configure(on_location=self.update_blinker_position,
                          on_status=self.on_auth_status)
            gps.start(minTime=1000, minDistance=0)

    def update_blinker_position(self, *args, **kwargs):
        my_lat = kwargs['lat']
        my_lon = kwargs['lon']
        print("GPS POSITION", my_lat, my_lon)
        # Update GpsBlinker position


        # Center map on gps
        if not self.has_centered_map:
            map = self.screen.ids.mainscreen.ids.screen1.ids.map_view
            map.center_on(my_lat, my_lon)
            self.has_centered_map = True

    def on_auth_status(self, general_status, status_message):
        if general_status == 'provider-enabled':
            pass
        else:
            self.open_gps_access_popup()

    def open_gps_access_popup(self):
        dialog = MDDialog(title="GPS Error", text="You need to enable GPS access for the app to function properly")
        dialog.size_hint = [.8, .8]
        dialog.pos_hint = {'center_x': .5, 'center_y': .5}
        dialog.open()


    def build(self):

        return self.screen




    def update_time(self, nap):
        if self.sw_started:
            self.sw_seconds += nap
        minutes, seconds = divmod(self.sw_seconds, 60)
        part_seconds = seconds * 100 % 100
        self.screen.ids.mainscreen.ids.screen1.ids.budi.text = f'{int(minutes):02}:{int(seconds):02}.[size=40]{int(part_seconds):02}[/size]'
        if self.local == False:
            self.screen.ids.mainscreen.ids.screen1.ids.real_time.text = f'{datetime.now(tz=pytz.timezone(self.region)).strftime("[b]%H:%M:%S[/b]")}'

        elif self.local == True:
            self.screen.ids.mainscreen.ids.screen1.ids.real_time.text = strftime('[b]%H:%M:%S[/b]')

    def on_start(self):

        Clock.schedule_interval(self.update_time, 1/60)


        self.search_menu= SearchPopupMenu()




    def start_stop(self):

        self.sw_started = not self.sw_started
        if self.screen.ids.mainscreen.ids.screen1.ids.play_button.icon == 'play':
            self.screen.ids.mainscreen.ids.screen1.ids.play_button.icon= 'pause'
        else:
            self.screen.ids.mainscreen.ids.screen1.ids.play_button.icon= 'play'



    def reset(self):
        if self.sw_started:

            self.sw_started = False
        # print('lol')

        self.sw_seconds = 0

if __name__ == '__main__':
    OneApp().run()
