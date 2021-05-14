from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from py_librus_api import Librus
from datetime import date
global tajne_akta
librus = Librus()

with open("login.txt", "r") as fp:
    login=fp.read()
with open("haslo.txt", "r") as f:
    password=f.read()


while not librus.logged_in:
    if not librus.login(login, password):
        print("Log in failed! Check your username and/or password!")
    else:
        print("Logged in successfully!")


tajne_akta = librus.get_teacher_free_days()
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


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        def ToDate(text):
            text = text.split('-')
            return date(int(text[0]), int(text[1]), int(text[2]))
        actual = []
        for x in tajne_akta:
            if date.today() <= ToDate(x["DateTo"]):
                actual.append(x)
        self.data = [{'text': str(j)} for j in actual]


class TestApp(App):
    def build(self):
        return RV()


if __name__ == '__main__':
    TestApp().run()