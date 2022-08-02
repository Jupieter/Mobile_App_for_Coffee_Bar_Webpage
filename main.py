from kivy.lang import Builder
from kivymd.app import MDApp


class TestNavigationDrawer(MDApp):

    def build(self):
        return Builder.load_file('kv/main.kv')

if __name__ == '__main__':
    # print('START MAIN')
    TestNavigationDrawer().run()

