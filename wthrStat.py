#!/usr/bin/env python

# import random
import sys
import argparse
import os
import pygame
import threading
import time
import signal

# sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import pygameui as ui

import logging
log_format = '%(asctime)-6s: %(name)s - %(levelname)s - %(message)s'
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(log_format))
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)

os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

LIST_WIDTH = 180
MARGIN = 20
SMALL_MARGIN = 5
degree_sign = u'\N{DEGREE SIGN}'



class SettingsScene(ui.Scene):
    def __init__(self):
        ui.Scene.__init__(self)



        self.greet_button = ui.Button(ui.Rect(
            140, 110, 40, 20), 'back')
        self.greet_button.on_clicked.connect(self.greet)
        self.add_child(self.greet_button)


    def greet(self, btn, mbtn):
        ui.scene.pop()
        ui.scene.push(mainScene)

    def layout(self):
        # ui.theme.current.set('Label', 'normal', 'padding', (6, 6))
        ui.kvc.set_value_for_keypath(self.greet_button, 'padding', (6, 6))
        self.greet_button.render()
        ui.Scene.layout(self)


class MainWthrScene(ui.Scene):
    def __init__(self):
        ui.Scene.__init__(self)

        # label1Size = 32
        # label2Size = 16

        # ui.theme.current.set('Label', 'normal', 'background_color', (100, 255, 255))  # useful for seeing labels better
        ui.theme.current.set('Label', 'normal', 'padding', (0, 0))
        label_height = ui.theme.current.label_height

        # frame = ui.Rect(MARGIN, MARGIN, 100, label_height)

        labels2 = [ui.Label(ui.Rect(0, 0, 100, label_height), 'Item %d' % (i + 1)) for i in range(10)]
        for l in labels2:
            l.halign = ui.LEFT
        self.select_view = ui.SelectView(ui.Rect(SMALL_MARGIN, SMALL_MARGIN, 180, label_height), labels2)
        # self.select_view.on_selection_changed.connect(self.selection_changed)
        self.add_child(self.select_view)

        #CURRENT DRYBULB
        self.lblDb = ui.Label(ui.Rect(0, label_height + 2 * SMALL_MARGIN, 320, 90), "100 " + degree_sign + "F", halign=ui.label.LEFT)
        self.add_child(self.lblDb)

        # HIGH PREDICTION
        self.lblHighDbLbl = ui.Label(ui.Rect(SMALL_MARGIN, self.lblDb.frame.bottom + SMALL_MARGIN, 40, label_height), "High: ",
                                     halign=ui.label.LEFT)
        self.add_child(self.lblHighDbLbl)

        self.lblHighDb = ui.Label(ui.Rect(40 + SMALL_MARGIN, self.lblHighDbLbl.frame.top, 50, label_height), "100 " + degree_sign +
                                  "F", halign=ui.label.LEFT)
        self.add_child(self.lblHighDb)

        # LOW PREDICTION
        self.lblLowDbLbl = ui.Label(ui.Rect(SMALL_MARGIN, self.lblHighDbLbl.frame.bottom + SMALL_MARGIN, 40, label_height), "Low: ",
                                     halign=ui.label.LEFT)
        self.add_child(self.lblLowDbLbl)

        self.lblLowDb = ui.Label(ui.Rect(40 + SMALL_MARGIN, self.lblLowDbLbl.frame.top, 50, label_height), "100 " + degree_sign +
                                  "F", halign=ui.label.LEFT)
        self.add_child(self.lblLowDb)


        # dispImg = ui.get_image('/home/pi/JDrive/Utility_Meter_Tracking/Server_Polling/wthrStat/resources/partlycloudy.gif')
        dispImg = pygame.image.load('resources/partlycloudy.png')
        self.wthrImg = ui.ImageView(ui.Rect(self.lblHighDb.frame.right + SMALL_MARGIN, self.lblDb.frame.bottom + SMALL_MARGIN, 50, 50), dispImg)
        self.add_child(self.wthrImg)

        # self.name_textfield = ui.TextField(frame, placeholder='Your name')
        # self.name_textfield.centerx = self.frame.centerx
        # self.add_child(self.name_textfield)

        # gridview = ui.GridView(ui.Rect(0, 0, 500, 500))
        # self.scroll_gridview = ui.ScrollView(ui.Rect(
        #     MARGIN, self.name_textfield.frame.bottom + MARGIN,
        #     200 - scrollbar_size, 250), gridview)
        # self.add_child(self.scroll_gridview)
        #
        # items = ['Apples', 'Bananas', 'Grapes', 'Cheese', 'Goats', 'Beer']
        # labels = [ui.Label(ui.Rect(0, 0, LIST_WIDTH, label_height), item, halign=ui.LEFT) for item in items]
        # list_view = ui.ListView(ui.Rect(0, 0, LIST_WIDTH, 400), labels)
        # list_view.on_selected.connect(self.item_selected)
        # list_view.on_deselected.connect(self.item_deselected)
        # self.scroll_list = ui.ScrollView(ui.Rect(
        #     MARGIN, self.scroll_gridview.frame.bottom + MARGIN,
        #     LIST_WIDTH, 80), list_view)
        # self.add_child(self.scroll_list)
        #
        self.greet_button = ui.Button(ui.Rect(self.lblHighDb.frame.right + SMALL_MARGIN, self.wthrImg.frame.bottom + SMALL_MARGIN, 0, 0), 'blank')
        self.greet_button.on_clicked.connect(self.greet)
        self.add_child(self.greet_button)
        #
        # self.image_view = ui.view_for_image_named('logo')
        # self.image_view.frame.right = self.frame.right - MARGIN
        # self.image_view.frame.top = MARGIN
        # self.add_child(self.image_view)
        #
        # self.checkbox = ui.Checkbox(ui.Rect(
        #     self.scroll_gridview.frame.right + MARGIN,
        #     self.scroll_gridview.frame.top,
        #     200, label_height), 'I eat food')
        # self.add_child(self.checkbox)
        #
        # self.checkbox1 = ui.Checkbox(ui.Rect(
        #     self.checkbox.frame.left,
        #     self.checkbox.frame.bottom + SMALL_MARGIN,
        #     200, label_height), 'I drink water')
        # self.add_child(self.checkbox1)
        #
        # self.checkbox2 = ui.Checkbox(ui.Rect(
        #     self.checkbox.frame.left,
        #     self.checkbox1.frame.bottom + SMALL_MARGIN,
        #     200, label_height), 'I exercise regularly')
        # self.add_child(self.checkbox2)
        #
        # info_image = ui.get_image('info')
        # self.info_button = ui.ImageButton(ui.Rect(
        #     self.checkbox2.frame.left,
        #     self.checkbox2.frame.bottom + MARGIN,
        #     0, 0), info_image)
        # self.info_button.on_clicked.connect(self.show_alert)
        # self.add_child(self.info_button)
        #
        # notify_image = ui.get_image('star')
        # self.notify_button = ui.ImageButton(ui.Rect(
        #     self.info_button.frame.right + MARGIN,
        #     self.info_button.frame.top,
        #     0, 0), notify_image)
        # self.notify_button.on_clicked.connect(self.show_notification)
        # self.add_child(self.notify_button)
        #
        # self.task_button = ui.Button(ui.Rect(
        #     self.info_button.frame.left,
        #     self.info_button.frame.bottom + MARGIN,
        #     0, 0), 'Consume!')
        # self.task_button.on_clicked.connect(self.run_fake_task)
        # self.add_child(self.task_button)
        #
        # self.running_task = False
        # self.progress_view = ui.ProgressView(ui.Rect(
        #     self.frame.right - MARGIN - 180,
        #     self.task_button.frame.centery - scrollbar_size // 2,
        #     180, scrollbar_size))
        # self.add_child(self.progress_view)
        # self.progress_view.hidden = True
        #
        
        #
        # self.hslider = ui.SliderView(ui.Rect(
        #     self.select_view.frame.left,
        #     self.select_view.frame.bottom + MARGIN*2,
        #     100, scrollbar_size), ui.HORIZONTAL, 0, 100)
        # self.hslider.on_value_changed.connect(self.value_changed)
        # self.add_child(self.hslider)
        #
        # self.vslider = ui.SliderView(ui.Rect(
        #     self.hslider.frame.right + SMALL_MARGIN,
        #     self.hslider.frame.centery,
        #     scrollbar_size, 100), ui.VERTICAL, 0, 100)
        # self.vslider.on_value_changed.connect(self.value_changed)
        # self.add_child(self.vslider)
        #
        # self.slider_value = ui.Label(ui.Rect(
        #     self.hslider.frame.centerx - 25,
        #     self.hslider.frame.bottom + MARGIN,
        #     50, label_height), '')
        # self.add_child(self.slider_value)
        #
        # self.spinner = ui.SpinnerView(ui.Rect(
        #     self.frame.right - MARGIN - ui.SpinnerView.size,
        #     self.frame.bottom - MARGIN - ui.SpinnerView.size,
        #     0, 0))
        # self.add_child(self.spinner)

    def layout(self):
        # self.checkbox.toggle()
        # self.checkbox1.toggle()
        ui.kvc.set_value_for_keypath(self.lblDb, 'font', ui.resource.get_font(100))
        ui.kvc.set_value_for_keypath(self.lblHighDb, 'background_color', (255, 200, 255))

        self.lblDb.render()
        self.lblHighDb.render()

        ui.Scene.layout(self)

    # def item_selected(self, list_view, item, index):
    #     item.state = 'selected'
    #
    # def item_deselected(self, list_view, item, index):
    #     item.state = 'normal'
    #
    # def selection_changed(self, selection_view, item, index):
    #     logger.info('new selection: %s' % str(item))
    #
    # def value_changed(self, slider_view, value):
    #     self.slider_value.text = '%d' % value
    #
    def greet(self, btn, mbtn):
        ui.scene.pop()
        ui.scene.push(settingsScene)
    #     name = self.name_textfield.text.strip()
    #     if len(name) == 0:
    #         name = 'uh, you?'
    #     ui.show_alert(title='Greetings!', message='Hello, %s' % name)
    #
    # def show_alert(self, btn, mbtn):
    #     msgs = [
    #         'This is an alert',
    #         'This is an alert with\na line break in it',
    #         'This is a rather long alert that should ' +
    #         'automatically word wrap to multiple lines',
    #         'This is an very long alert that should ' +
    #         'automatically word wrap to multiple lines...' +
    #         'is this not the best thing EVAR? wow, mindblowing...'
    #     ]
    #     msg = random.choice(msgs)
    #     ui.show_alert(msg)
    #
    # def show_notification(self, btn, mbtn):
    #     msgs = [
    #        'Achievement Unlocked! Notification!',
    #        'This is a notification\nwith a linebreak in it',
    #        'This notification is rather long and should ' +
    #        'automatically word wrap to multiple lines'
    #     ]
    #     msg = random.choice(msgs)
    #     ui.show_notification(msg)
    #
    # def run_fake_task(self, btn, mbtn):
    #     if not self.running_task:
    #         self.task_button.enabled = False
    #         self.progress_view.hidden = False
    #     self.progress_view.progress = 0
    #     self.running_task = True

    # def update(self, dt):
    #     ui.Scene.update(self, dt)
    #     if self.running_task:
    #         progress = min(1.0, self.progress_view.progress + 0.01)
    #         self.progress_view.progress = progress
    #         self.running_task = (self.progress_view.progress < 1.0)
    #         self.task_button.enabled = not self.running_task
    #         if self.task_button.enabled:
    #             ui.show_alert("I'M FINISHED!", title='Milkshake')
    #             self.progress_view.progress = 0
    #             self.progress_view.hidden = True
    def setTempLabel(self, temp):
        self.lblDb.text = '%.0f' % temp + degree_sign + 'F'

class GetWUdata():
    def __init__(self, mainScrn):
        self.mainScrn = mainScrn
        self.terminated = False

    def terminate(self):
        self.terminated = True

    def __call__(self, *args, **kwargs):
        startTime = time.time()
        while not self.terminated:
            if time.time() - startTime > 10:
                startTime = time.time()
                self.mainScrn.setTempLabel(40)



def signal_handler(signal, frame):
    wthrReader.terminate()
    sys.exit(0)

ui.init('pygameui - Weather Station', (480, 320))
pygame.mouse.set_visible(False)


mainScene = MainWthrScene()
settingsScene = SettingsScene()
wthrReader = GetWUdata(mainScene)
# threading.Thread(target=wthrReader).start()

signal.signal(signal.SIGINT, signal_handler)

ui.scene.push(mainScene)

ui.run()
