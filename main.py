from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.core.window import Window
import time
from random import random
from math import sqrt
import pandas as pd
from matplotlib import pyplot as plt
from pandas import DataFrame
import numpy as np


# GUI Constants
MAX_SIZE = .3
MAX_DISTANCE = 500
WINDOW_SIZE = 1200

# pandas constants
SIZE_LABEL = 'size'
DISTANCE_LABEL = 'distance'
TIME_LABEL = 'time'
FITSS_LABEL = 'fitts'
FILENAME = './fitts.csv'


def add_fitts_data_to_df(df, a=.001, b=200, c=.5):
    y = a + b * np.log2(((2 * df[DISTANCE_LABEL])/df[SIZE_LABEL]) + c)
    df[FITSS_LABEL] = y


def plot_sizes(df: DataFrame):
    fig, axes = plt.subplots(nrows=2)

    ax = df.plot.scatter(x=SIZE_LABEL, y=TIME_LABEL, ax=axes[0])
    ax.set_xlabel('button size [px]')
    ax.set_ylabel('time [ms]')
    ax.set_title('Empirical data')

    ax = df.plot.scatter(x=SIZE_LABEL, y=FITSS_LABEL, ax=axes[1])
    ax.set_xlabel('button_size [px]')
    ax.set_ylabel('time [ms]')
    ax.set_title('Fitts law prediction')
    plt.show()


def plot_distances(df: DataFrame):
    fig, axes = plt.subplots(nrows=2)

    ax = df.plot.scatter(x=DISTANCE_LABEL, y=TIME_LABEL, ax=axes[0])
    ax.set_xlabel('distance [px]')
    ax.set_ylabel('time [ms]')
    ax.set_title('Empirical data')

    ax = df.plot.scatter(x=DISTANCE_LABEL, y=FITSS_LABEL, ax=axes[1])
    ax.set_xlabel('distance [px]')
    ax.set_ylabel('time [ms]')
    ax.set_title('Fitts law prediction')
    plt.show()


class FittsWidget(FloatLayout):
    def __init__(self):
        super(FittsWidget, self).__init__()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.cursor_x = 0
        self.cursor_y = 0

        self.btn_created = False

        self.test_size = True
        self.test_distance = False

        self.scores = []

        self.label = Label(text='Press space to place a button\npress escape to end test',
                           size_hint=(.1, .1), pos=(100, 950))
        self.add_widget(self.label)

        Window.bind(mouse_pos=self.set_cursor_pos)

    def set_cursor_pos(self, w, p):
        self.cursor_x, self.cursor_y = p

    def set_label_text(self):
        if self.test_size:
            text = f'Size mode, to change press (e)\nYou have gathered: {len(self.scores)} samples'
        else:
            text = f'Distance mode, to change press (e)\nYou have gathered: {len(self.scores)} samples'

        self.label.text = text

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def callback(self, start_time, size, distance):
        def add_score(instance):
            d = {SIZE_LABEL: size * WINDOW_SIZE, DISTANCE_LABEL: distance, TIME_LABEL: (time.time() - start_time) * 1000}
            self.scores.append(d)
            self.remove_widget(self.button)
            self.btn_created = False
            self.set_label_text()

        return add_score

    def generate_random_parameters(self):
        if self.test_size:
            size = MAX_SIZE * random() + 0.05
            dist = MAX_DISTANCE // 1.5
        elif self.test_distance:
            size = .2
            dist = int(MAX_DISTANCE * random()) + 50
        else:
            dist = MAX_DISTANCE
            size = MAX_SIZE

        if random() > .5:
            dist *= -1

        r = random()
        r += 0.01
        dx = dist * r
        dy = dist * (1. - r)

        size_in_pixels = size * WINDOW_SIZE
        if dx < 0:
            if self.cursor_x + dx < size_in_pixels:
                dx = -self.cursor_x + size_in_pixels
        else:
            if self.cursor_x + dx > WINDOW_SIZE - size_in_pixels:
                dx = WINDOW_SIZE - self.cursor_x - size_in_pixels

        if dy < 0:
            if self.cursor_y + dy < size_in_pixels:
                dy = -self.cursor_y + size_in_pixels
        else:
            if self.cursor_y + dy > WINDOW_SIZE - size_in_pixels:
                dy = WINDOW_SIZE - self.cursor_y - size_in_pixels

        dist = int(sqrt(dx ** 2 + dy ** 2))
        pos = self.cursor_x + dx, self.cursor_y + dy

        return size, dist + size_in_pixels//2, pos

    def show_plot(self):
        df = pd.DataFrame(self.scores)
        add_fitts_data_to_df(df)

        df.to_csv(FILENAME)

        if self.test_size:
            plot_sizes(df)
        else:
            plot_distances(df)

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        key = keycode[1]

        if key == 'spacebar':
            if self.btn_created:
                return

            size, distance, pos = self.generate_random_parameters()

            call = self.callback(time.time(), size, distance)

            color = (random() + .1, random() + .1, random() + .1, 1)
            self.button = Button(text='Click', size_hint=(size, size), pos=pos, on_press=call, background_color=color)
            self.add_widget(self.button)
            self.btn_created = True

        elif key == 'escape':
            self.show_plot()

        elif key == 'e':
            self.test_size = not self.test_size
            self.test_distance = not self.test_distance

            self.show_plot()

            self.scores.clear()
            self.set_label_text()

        return True


class FittsApp(App):
    def build(self):
        Window.size = (WINDOW_SIZE, WINDOW_SIZE)
        return FittsWidget()


if __name__ == '__main__':
    FittsApp().run()
