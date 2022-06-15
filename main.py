# -*- coding: utf-8 -*-
"""
Created on Thu May  6 13:15:37 2021

@author: Ale
"""

import os
from tkinter import Tk, Button, Label, Checkbutton, BooleanVar
from edition import crop_frame, open_video, process

os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"


class MyClass():

    temp_folder_path = 'data/'
    fullPathFile = None
    baseNameFile = None
    formatFile = None
    dirFile = None
    videoparts = 0
    pathFolder = None
    right_clicks = list()
    cropped = False
    totalframes = 0
    framerate = 0
    count = 0
    frameCount = 0
    frameExtracted = 0
    videoExtracted = 0
    running = True
    frameStatus = ''
    width = ''
    height = ''
    newWidth = ''
    dsize = ''


def open_videos():
    open_video(MyClass, lbl_open_video, lbl_frames____, lbl_frameRate_)


def crop_frames():
    crop_frame(MyClass, draw_square=chk_state2.get())


def main():
    process(MyClass, window, lbl_framecount, lbl_frameExtra, lbl_videoGener,
            lbl_progress__, replace=chk_state.get())


window = Tk()
window.title('Crop Video')
window.geometry('400x300')

btn_open_video = Button(window, text='Open Video File', command=open_videos)
btn_open_video.grid(column=0, row=0)
btn_crop_video = Button(window, text='Pick Crop area', command=crop_frames)
btn_crop_video.grid(column=0, row=1)
btn_extractmer = Button(window, text='Convert Video', command=main)
btn_extractmer.grid(column=0, row=2)
lbl_open_video = Label(window, text="")
lbl_open_video.grid(column=0, row=3)
lbl_frames____ = Label(window, text="")
lbl_frames____.grid(column=0, row=4)
lbl_frameRate_ = Label(window, text="")
lbl_frameRate_.grid(column=0, row=5)
lbl_framecount = Label(window, text="")
lbl_framecount.grid(column=0, row=6)
lbl_frameExtra = Label(window, text="")
lbl_frameExtra.grid(column=0, row=7)
lbl_videoGener = Label(window, text="")
lbl_videoGener.grid(column=0, row=8)
lbl_progress__ = Label(window, text="")
lbl_progress__.grid(column=0, row=9)
lbl_deviation_ = Label(window, text='')
lbl_deviation_.grid(column=0, row=10)
chk_state = BooleanVar()
chk = Checkbutton(window, text='Replace Original File', var=chk_state)
chk.grid(column=0, row=11)
chk_state.set(0)
chk_state2 = BooleanVar()
chk2 = Checkbutton(window, text='Draw grid', var=chk_state2)
chk2.grid(column=1, row=1)
chk_state2.set(0)

window.mainloop()
