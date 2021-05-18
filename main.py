import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.properties import StringProperty, ObjectProperty
from kivy.core.window import Window

from py_librus_api import Librus
from datetime import date

from collections.abc import Mapping
import os

import time

librus = Librus()

Builder.load_file('gui2.kv')

Window.clearcolor = (30/255,30/255,30/255,0)

class MyLibrus():
    def __init__(self, login, password, nr):
        self.login = login
        self.password = password
        self.nr = nr

    def czyZalogowano(self):
        if not librus.logged_in:
            if not librus.login(self.login, self.password):
                print("Nie zalogowano")
                os.system("python main.py")
                exit()

    def nieObecnosci(self):
        #   To jest do zmiany by pokazywało w aplikacji! I narazie nie działa.
        tajne_akta = librus.get_teacher_free_days()

        def ToDate(text):
            text = text.split('-')
            return date(int(text[0]), int(text[1]), int(text[2]))

        actual = []
        for x in tajne_akta:
            if date.today() <= ToDate(x["DateTo"]):
                actual.append(x)

        data = [{'text': str(j)} for j in actual]

        nieobecnosc = ''
        for i in data:
            s = eval(i['text'])
            if 'Teacher' in s:
                for x in s['Teacher']:
                    nieobecnosc += str(s['Teacher'][x]) + " "
                del s['Teacher']
            for j in s:
                nieobecnosc += str(s[j]) + " "
            nieobecnosc += '\n'

        return nieobecnosc

class MyGridLayout(Widget):

    login = ObjectProperty(None)
    password = ObjectProperty(None)
    nr = ObjectProperty(None)

    def press(self):
        login = self.ids.login.text
        password = self.ids.password.text
        nr = self.ids.sz_nr.text

        lib = MyLibrus(login, password, nr)

        lib.czyZalogowano()
        self.ids.nie.text = lib.nieObecnosci()


class MyApp(App):
    def build(self):
        Window.size = (1080 / 2.5, 2244 / 2.5)
        return MyGridLayout()

if __name__ == '__main__':
    MyApp().run()
