from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from urllib import parse
from kivymd.uix.button import MDFlatButton,MDRaisedButton
from kivy.network.urlrequest import UrlRequest
from kivy.app import App
from timezonefinder import TimezoneFinder
from certifi import where



#> datetime.timedelta(0, 7200)
class Content(BoxLayout):

    pass

class MDInputDialog:
    app_id = "29J5DPrBlkNXqYCPGHM4"

    app_code = "uEmoDW5E3IM3luVFPMXkIA"
    def __init__(self):
        self.todaynow  = None
        self.dialog = MDDialog(
            title="Fill The Address:",
            type="custom",
            content_cls=Content(),
            buttons=[
                MDFlatButton(
                    text="CANCEL", text_color=App.get_running_app().theme_cls.primary_color,on_press=self.dismiss_menu
                ),
                MDRaisedButton(
                    text="ENTER",on_press=self.get_value
                ),
            ],
        )

    def open_menu(self):
        self.dialog.open()
    def dismiss_menu(self,*args):
        self.dialog.dismiss()
    def get_value(self,*args):
        self.dialog.dismiss()
        
        self.value = (self.dialog.content_cls.ids.address.text)
        self.geocode_get_lat_lon(self.value)

    def geocode_get_lat_lon(self, address):

        
        address = parse.quote(address)
        url = "https://geocoder.api.here.com/6.2/geocode.json?searchtext=%s&app_id=%s&app_code=%s" % (
        address, self.app_id, self.app_code)
        UrlRequest(url, on_success=self.success, on_failure=self.failure, on_error=self.error, ca_file=where())

    def success(self, urlrequest, result):


        self.latitude = result['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]['Latitude']
        self.longitude = result['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]['Longitude']
        app = App.get_running_app()
        mapview = app.screen.ids.mainscreen.ids.screen1.ids.map_view

        self.check_time()

        mapview.center_on(self.latitude, self.longitude)

       
        

    # def snack_show(self,*args):
    #     self.snackbar = Snackbar(text=f"{self.value} Timezone Now:{self.todaynow.strftime('%H:%M:%S')}", duration=3)
    #     self.snackbar.open()



    def check_time(self,*args):
        # from kivy.clock import Clock


        tf = TimezoneFinder()

        App.get_running_app().local  = False
        App.get_running_app().region = (tf.timezone_at(lng=self.longitude, lat=self.latitude))


        # self.todaynow = datetime.datetime.now(tz=pytz.timezone(a))
        # Clock.schedule_once(self.snack_show)





    def error(self, urlrequest, result):
        print("error")
        print(result)

    def failure(self, urlrequest, result):
        print("failure")
        print(result)



class SearchPopupMenu(MDInputDialog):
    def __init__(self):
        super().__init__()
        self.size = [.9,.3]
    def open(self,*args):
        self.open_menu()



