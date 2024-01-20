import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Line, Color, Rectangle
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
kivy.require('2.3.0')

sound_file = 'metronomekort.wav'  # "metronome-85688.wav"  # downloaded from https://pixabay.com/nl/sound-effects/search/metronoom/

class KeyboardButton(Button):
    key_height = 60

    def on_press_keyboard(self):
        self.canvas.before.children[0].rgba = [0.835, 0.714, 0.871, 1.0]
        tag = self.tag
        my_widget.navigate(self.parent.parent.parent.parent, tag)

    def on_release_keyboard(self):
        self.canvas.before.children[0].rgba = [0.835 * 1.1, 0.714 * 1.1, 0.871 * 1.1, 1]


class NotationImage(Image):
    pass


class MyW(RelativeLayout):
    top_bar_height = 118
    note_height = 60
    key_height = 60
    number_of_keyrows = 4
    keyboard_height = number_of_keyrows * (key_height + 10 + 10)  # 220
    message_height = 30
    tick_line_offset = 46
    window_height = Window.height
    window_width = Window.width
    keyboard_position = NumericProperty(-keyboard_height - message_height - 10)
    is_keyboard_on = False
    notation_start_height = Window.height - top_bar_height - note_height
    tick_line_base_x = window_width
    tick_line_base_y = window_height - top_bar_height - tick_line_offset
    slider_event = None
    notation = ObjectProperty(None)
    cursor_pos = 0
    sound = ObjectProperty(None, allownone=True)
    volume = NumericProperty(1.0)
    element_index = 0
    times = []
    start = 0
    stop = 0

    def __init__(self, **kwargs):
        super(MyW, self).__init__(**kwargs)
        ## todo initial button highlites
        self.is_Keyboard_on = None
        self.tuple_size = 3
        self.buffer_size = 1
        self.pressed_group = 1
        self.music_element = {'group': 1, 'duration': 1. / 4, 'rest': False, 'bar': False, 'position': 0}
        self.tickline = []
        self.keyboard_close = True
        self.sound = SoundLoader.load(sound_file)
        self.index = 0

    def re_play(self):
        self.element_index = 0
        self.times = []
        self.sound.play()
        for n in range(len(self.ids['notation'].children)):
            self.times.append(self.ids['notation'].children[-1 - n].duration)
        self.play(0)

    def play(self, dt):
        # self.sound.stop()
        self.sound.seek(0)
        #self.sound.play()
        if self.element_index < len(self.times):
            t = self.times[self.element_index]
            self.element_index += 1
            Clock.schedule_once(self.play, t)

    def hide_keyboards(self):
        self.keyboard_close = True
        self.slider_event = Clock.schedule_interval(self.keyboard_slider, 0.01)
        # self.ids['notation'].children[-1].source = './images/note_64.png'
        # del (self.ids['notation'].children[-2 - 1])
        # for n in range(3):
        #    self.ids['notation'].children[-3 - n].canvas.before.children[0].rgba = (
        #        0.835 * 1.1, 0.714 * 1.1, 0.871 * 1.1, 1)

    def open_notation_keyboard(self):
        self.keyboard_close = False
        self.slider_event = Clock.schedule_interval(self.keyboard_slider, 0.01)

    def keyboard_slider(self, dt=0.01):
        if self.keyboard_close:
            self.keyboard_position -= 12
            if self.keyboard_position <= -self.keyboard_height - self.message_height - 10:
                self.keyboard_position = -self.keyboard_height - self.message_height - 10
                Clock.unschedule(self.slider_event)
        else:
            self.is_Keyboard_on = True
            self.keyboard_position += 12
            if self.keyboard_position >= 0:
                self.keyboard_position = 0
                Clock.unschedule(self.slider_event)

    def on_screen_touch(self, touch):
        self.open_notation_keyboard()

    def add_tickline(self):
        stack_layout = self.ids['notation']
        with stack_layout.children[0].canvas.before:
            Color(1, 1, 1, 1)
            Rectangle(pos=stack_layout.children[0].pos, size=stack_layout.children[0].size)

        with stack_layout.children[0].canvas.after:
            Color(0, 0, 0, 1)
            Line(points=[stack_layout.children[0].x, stack_layout.children[0].y + 14,
                         stack_layout.children[0].x + stack_layout.children[0].width, stack_layout.children[0].y + 14])

    def insert_element(self, source, duration):
        im = Image(source=source)
        self.ids['notation'].add_widget(im)
        stack_layout = self.ids['notation']
        stack_layout.children[0].size_hint = None, None
        stack_layout.children[0].size = stack_layout.children[0].norm_image_size
        stack_layout.children[0].duration = 4.0 / duration
        Clock.schedule_once(lambda *args: self.add_tickline())

    def navigate(self, tag):
        match tag:
            case 'n1':
                self.insert_element('./images/note_1.png', 1)
            case 'n2':
                self.insert_element('./images/note_2.png', 2)
            case 'n4':
                self.insert_element('./images/note_4.png', 4)
            case 'n8':
                self.insert_element('./images/note_8.png', 8)
            case 'n16':
                self.insert_element('./images/note_16.png', 16)
            case 'n32':
                self.insert_element('./images/note_32.png', 32)
            case 'n64':
                self.insert_element('./images/note_64.png', 64)
            case 's1':
                self.insert_element('./images/silent_1.png')
            case 's2':
                self.insert_element('./images/silent_2.png')
            case 's4':
                self.insert_element('./images/silent_4.png')
            case 's8':
                self.insert_element('./images/silent_8.png')
            case 's16':
                self.insert_element('./images/silent_16.png')
            case 's32':
                self.insert_element('./images/silent_32.png')
            case 's64':
                self.insert_element('./images/silent_64.png')
            case 'go right':
                self.move_cursor(1)
            case 'go left':
                self.move_cursor(-1)
            case 'go up':
                row, column = self.cursor2row_column(self.cursor_pos)
                if row > 0:
                    row -= 1
                cur_pos = self.row_column2cursor(row, column)
                self.move_cursor(cur_pos - self.cursor_pos)
            case 'go down':
                row, column = self.cursor2row_column(self.cursor_pos)
                row += 1
                cur_pos = self.row_column2cursor(row, column)
                self.move_cursor(cur_pos - self.cursor_pos)
            case _:
                print('not implemented yet')

    def move_cursor(self, delta):
        if (((delta > 0) and (len(self.ids['notation'].children) > self.cursor_pos + delta)) or
                ((delta < 0) and (self.cursor_pos > -delta - 1))):
            del (self.ids['notation'].children[-self.cursor_pos - 1].canvas.after.children[-1])
            self.cursor_pos += delta
            size = self.ids['notation'].children[-self.cursor_pos - 1].size
            x = self.ids['notation'].children[-self.cursor_pos - 1].pos[0]
            y = self.ids['notation'].children[-self.cursor_pos - 1].pos[1]
            with self.ids['notation'].children[-self.cursor_pos - 1].canvas.after:
                Color(rgba=[0, 0, 0, 1])
                Line(points=[x, y + 2, x, y + size[1] - 2], width=2)

    def cursor2row_column(self, cur_pos):
        y = self.ids['notation'].children[-self.cursor_pos - 1].y
        y0 = self.ids['notation'].children[-1].y
        y_pos = y
        row = 0
        cur_pos_ = cur_pos
        column = cur_pos_
        if y != y0:
            while (y_pos == y) and cur_pos_ > 0:
                cur_pos_ -= 1
                y_pos = self.ids['notation'].children[-cur_pos_ - 1].y
                row = int((y0 - y) / 60)
                column = self.cursor_pos - cur_pos_ - 1
        return row, column

    def row_column2cursor(self, row, column):
        y0 = self.ids['notation'].children[-1].y
        row_ = -1
        cursor0 = -1
        cursor = 0
        while row_ < row:
            cursor0 += 1
            row_ = int((y0 - self.ids['notation'].children[-cursor0 - 1].y) / 60)
        cursor = cursor0 + column
        row_ = int((y0 - self.ids['notation'].children[-cursor - 1].y) / 60)
        while row_ > row:  ## in case column position not available on found row
            cursor -= 1
            row_ = int((y0 - self.ids['notation'].children[-cursor - 1].y) / 60)
        return cursor

    def add_note_rest(self, n):
        for index in range(int(n)):
            self.tickline.append(dict(self.music_element))
            self.music_element['position'] += 100 * (1 / .16 + self.music_element['duration'] / .16)
        self.write_music()

    def write_music(self):
        pass


class MetronomeApp(App):
    icon = 'icon.png'
    title = 'click track metronome'

    # Window.top = -500
    # Window.left = -1000

    def __init__(self, **kwargs):
        super(MetronomeApp, self).__init__(**kwargs)

    def build(self):
        return my_widget()


Builder.load_file('metronome_mobile.kv')

if __name__ == '__main__':
    my_widget = MyW
    MetronomeApp().run()
