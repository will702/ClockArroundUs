from kivymd.uix.screen import MDScreen


class Screen1(MDScreen):
    pass
from kivy_garden.mapview import MapView
from kivy.clock import Clock




class FarmersMapView(MapView):
    getting_markets_timer = None

    def start_getting_markets_in_fov(self):
        # After one second, get the markets in the field of view
        try:
            self.getting_markets_timer.cancel()
        except:
            pass

        self.getting_markets_timer = Clock.schedule_once(self.get_markets_in_fov, 1)

    def get_markets_in_fov(self, *args):
        pass





