from kivymd.uix.screen import MDScreen
from kivy.lang import Builder

import os
folder = os.path.dirname(os.path.realpath(__file__))
Builder.load_file(folder+'/screen1.kv')
Builder.load_file(folder+"/mainscreen.kv")

from .screen1 import Screen1,FarmersMapView

class MainScreen(MDScreen):

    def change_screen(self, screen, *args):
        self.ids.screen_manager.current = screen

