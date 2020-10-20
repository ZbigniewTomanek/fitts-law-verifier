from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from enum import Enum
import time
from kivy.graphics import Color
from random import random, randint
from math import sqrt
import pandas as pd

SIZES = [.05, .2]
DISTANCES = [100, 500]
WINDOW_SIZE = 1200
FILENAME = './fitts.csv'


class FittsWidget(FloatLayout):
    def __init__(self):
        super(FittsWidget, self).__init__()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.cursor_x = 0
        self.cursor_y = 0

        self.btn_created = False

        self.scores = []

        Window.bind(mouse_pos=self.set_cursor_pos)

    def set_cursor_pos(self, w, p):
        self.cursor_x, self.cursor_y = p

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def callback(self, start_time, size, distance):
        def add_score(instance):
            d = {'size': size, 'distance': distance, 'time': time.time() - start_time}
            self.scores.append(d)
            self.remove_widget(self.button)
            self.btn_created = False

        return add_score

    def generate_random_parameters(self):
        size = SIZES[randint(0, 1)]
        dist = DISTANCES[randint(0, 1)]
        if random() > .5:
            dist *= -1

        r = random()
        r += 0.01
        dx = dist * r
        dy = dist * (1. - r)

        dist = int(sqrt(dx ** 2 + dy ** 2))
        print(dist)

        pos = self.cursor_x + dx, self.cursor_y + dy

        return size, dist, pos

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        key = keycode[1]
        print(key)
        if key == 'spacebar':
            if self.btn_created:
                return

            size, distance, pos = self.generate_random_parameters()

            call = self.callback(time.time(), size, distance)

            color = (random(), random(), random(), 1)
            self.button = Button(text='Click', size_hint=(size, size), pos=pos, on_press=call, background_color=color)
            self.add_widget(self.button)
            self.btn_created = True

        elif key == 'escape':
            df = pd.DataFrame(self.scores)
            df.to_csv(FILENAME)

        return True


class MyPaintApp(App):
    def build(self):
        Window.size = (WINDOW_SIZE, WINDOW_SIZE)
        return FittsWidget()


if __name__ == '__main__':
    MyPaintApp().run()
