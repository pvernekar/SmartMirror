# smartmirror.py
# requirements
# requests, feedparser, traceback, Pillow

import json
import locale
import threading
import time
import traceback
from contextlib import contextmanager
from tkinter import *

import feedparser
import requests
from PIL import Image, ImageTk

LOCALE_LOCK = threading.Lock()

ui_locale = ''  # e.g. 'fr_FR' fro French, '' as default
time_format = 12  # 12 or 24
date_format = "%b %d, %Y"  # check python doc for strftime() for options
news_country_code = 'us'
weather_api_token = 'fdb842a885715370f65bbd5b29920007'  # create account at https://darksky.net/dev/
weather_lang = 'en'  # see https://darksky.net/dev/docs/forecast for full list of language parameters values
weather_unit = 'us'  # see https://darksky.net/dev/docs/forecast for full list of unit parameters values
latitude = None  # Set this if IP location lookup does not work for you (must be a string)
longitude = None  # Set this if IP location lookup does not work for you (must be a string)
xlarge_text_size = 94
large_text_size = 48
medium_text_size = 28
small_text_size = 18


@contextmanager
def setlocale(name):  # thread proof function to work with locale
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)

image_files = [
    'assets/red.jpg',
    'assets/Cloud.jpeg',
    'assets/gray.jpg',
    'assets/grayHoodie.jpg',
    'assets/skyBlue.jpg'
]


class SmartCarousel(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')

        self.config(bg='white')
        self.title = 'Try Out Your Looks'
        self.newsLbl = Label(self, text=self.title, font=('Helvetica', large_text_size), fg="black", bg="white")
        self.newsLbl.pack()
        self.delay = 3500

        image = Image.open("assets/red.jpg")
        image = image.resize((500, 500), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)

        self.picture_display = Label(self, bg='white', image=photo)
        self.picture_display.image = photo
        self.picture_display.pack(side=LEFT, anchor=N)

    def show_slides(self, imageCounter):

        buffImage = image_files[imageCounter]
        image = Image.open(buffImage)
        image = image.resize((500, 500), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)

        self.picture_display.image = photo
        self.picture_display.config(image=photo)
        self.picture_display.pack(side=LEFT, anchor=N)


class CarouselMirror(Frame):

    class FullscreenWindow:

        def __init__(self):
            self.tk = Tk()
            self.tk.configure(background='white')
            self.topFrame = Frame(self.tk, background='white')
            self.bottomFrame = Frame(self.tk, background='white')
            self.topFrame.pack(side=TOP, fill=BOTH, expand=YES)
            self.bottomFrame.pack(side=BOTTOM, fill=BOTH, expand=YES)
            self.state = False
            self.tk.bind("<Return>", self.toggle_fullscreen)
            self.tk.bind("<Escape>", self.end_fullscreen)
            self.sCarousel = SmartCarousel(parent=self.bottomFrame)
            self.sCarousel.pack(side=TOP)
            #self.sCarousel.show_slides()
            self.counter = 0
            button = Button(command=self.buttonClick)
            image = Image.open("assets/try-me.png")
            #image = image.resize((500, 500), Image.ANTIALIAS)
            image = image.convert('RGB')
            buttonIconImage = ImageTk.PhotoImage(image)
            button.image = buttonIconImage
            button.configure(image=buttonIconImage)
            button.pack(side=BOTTOM)

        def toggle_fullscreen(self, event=None):
            self.state = not self.state  # Just toggling the boolean
            self.tk.attributes("-fullscreen", self.state)
            return "break"

        def end_fullscreen(self, event=None):
            self.state = False
            self.tk.attributes("-fullscreen", False)
            return "break"

        def buttonClick(self):
            #print('hello button')
            self.counter = self.counter + 1

            if self.counter == 5:
                self.counter = 0
            self.sCarousel.show_slides(self.counter)

    if __name__ == '__main__':
        w = FullscreenWindow()
        w.tk.mainloop()
