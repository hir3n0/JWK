import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.properties import StringProperty, ObjectProperty

from py_librus_api import Librus
from datetime import date

import time

global tajne_akta

Builder.load_string('''
<RV>:
    viewclass: 'Label'
    RecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
''')

class MyGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super(MyGridLayout, self).__init__(**kwargs)
        self.logowanie()


    def logowanie(self):
        self.cols = 1

        self.top_grid = GridLayout()
        self.top_grid.cols = 2

        self.second_grid = GridLayout()
        self.second_grid.cols = 1

        self.error_grid = GridLayout()
        self.error_grid.cols = 1

        # dodajemy widgety
        # text box z loginem
        self.top_grid.add_widget(Label(text="Login: "))
        self.login = TextInput(multiline=False)
        self.top_grid.add_widget(self.login)
        # text box z haslem
        self.top_grid.add_widget(Label(text="Hasło: "))
        self.haslo = TextInput(multiline=False)
        self.top_grid.add_widget(self.haslo)

        self.add_widget(self.top_grid)
        # przycisk
        self.submit = Button(text="zaloguj", font_size=32)
        self.submit.bind(on_press=self.press)
        self.add_widget(self.submit)

    def press(self, instance):
        librus = Librus()

        login = self.login.text
        password = self.haslo.text

        while not librus.logged_in:
            if not librus.login(login, password):
                print("Log in failed! Check your username and/or password!")
                time.sleep(2)
            else:
                print("Logged in successfully!")

        tajne_akta = librus.get_teacher_free_days()

        def ToDate(text):
            text = text.split('-')
            return date(int(text[0]), int(text[1]), int(text[2]))

        actual = []

        for x in tajne_akta:
            if date.today() <= ToDate(x["DateTo"]):
                actual.append(x)

        self.data = [{'text': str(j)} for j in actual]

        for i in self.data:
            self.second_grid.add_widget(Label(text=str(i['text']), font_size=10))

        self.add_widget(self.second_grid)


'''class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        def ToDate(text):
            text = text.split('-')
            return date(int(text[0]), int(text[1]), int(text[2]))
        actual = []
        for x in tajne_akta:
            if date.today() <= ToDate(x["DateTo"]):
                actual.append(x)
        self.data = [{'text': str(j)} for j in actual]'''

class TestApp(App):
    def build(self):
        return MyGridLayout()

if __name__ == '__main__':
    TestApp().run()