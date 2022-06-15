# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 15:53:18 2022

@author: Ale
"""

import os
import cv2
from natsort import natsorted
from moviepy.editor import VideoFileClip, concatenate_videoclips
from console import printnew
from draw import draw_squares
from tkinter import messagebox, filedialog
from utils import getBaseName, getFileFormatExtension, getFolderPath, deleteFilesInFolder
# from utils import deleteFilesInFolder
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"


def cleanVar(self):
    self.facefile = None
    self.baseNameFile = None
    self.videoparts = 0
    self.fullPathFile = None
    self.pathfacefile = None
    self.right_clicks = list()
    self.cropped = False
    self.totalframes = 0
    self.framerate = 0
    self.count = 0
    self.frameCount = 0
    self.frameExtracted = 0
    self.videoExtracted = 0
    self.running = True
    self.frameStatus = ''
    self.width = None
    self.height = None
    self.newWidth = ''
    self.dsize = None


def merge_videos(pathOut, name, replace=False, temp_folder='temp/'):
    print('Start to merge video files')
    if not replace:
        name = name + '_crop'
    L = []
    for file in natsorted(os.listdir(temp_folder)):
        if os.path.splitext(file)[1] == '.mp4':
            filePath = os.path.join(temp_folder, file)
            video = VideoFileClip(filePath)
            L.append(video)
            cap = cv2.VideoCapture(filePath)
            framerate = cap.get(cv2.CAP_PROP_FPS)
            cap.release()
    final_clip = concatenate_videoclips(L)
    final_clip.to_videofile(pathOut + name + ".mp4",
                            fps=framerate, remove_temp=True)
    video.close()


def configure(MyClass, window, lbl_framecount, lbl_frameExtra, lbl_videoGener, lbl_progress__):
    percentWorked = "[" + str(round(MyClass.frameCount *
                              100/MyClass.totalframes)) + " % worked] "
    frameProcess = "[Frame: " + str(MyClass.frameCount) + "] "
    printnew(percentWorked + MyClass.frameStatus + frameProcess)

    lbl_framecount.configure(text="Frame Process: " + str(MyClass.frameCount))
    lbl_frameExtra.configure(text="Frame Extracted: " +
                             str(MyClass.frameExtracted))
    lbl_videoGener.configure(
        text="Video part extracted: " + str(MyClass.videoExtracted))
    lbl_progress__.configure(text=percentWorked,
                             foreground="red")
    window.update()


def make_video_parts(MyClass, window, lbl_framecount, lbl_frameExtra, lbl_videoGener, lbl_progress__):


    cap = cv2.VideoCapture(MyClass.fullPathFile)
    frame = cap.read()[1]
    writer = None
    while True:
        ret, frame = cap.read()
        if ret is not True:
            writer.release()
            writer = None
            cap.release()
            break

        if writer is None:
            pathOutVideo = MyClass.temp_folder_path + \
                str(MyClass.videoExtracted + 1) + ".mp4"
            writer = cv2.VideoWriter(pathOutVideo, cv2.VideoWriter_fourcc(
                'X', 'V', 'I', 'D'), MyClass.framerate, MyClass.dsize)

        if ret is True:

            # Croppping image
            if MyClass.cropped == True:
                x1, y1 = MyClass.right_clicks[0]
                x2, y2 = MyClass.right_clicks[1]
                frame = frame[y1:y2, x1:x2]

            if writer is not None:
                writer.write(frame)
                MyClass.count = MyClass.count + 1
                MyClass.frameCount = MyClass.frameCount + 1
                MyClass.frameExtracted = MyClass.frameExtracted + 1

            if MyClass.count == 300:
                writer.release()
                writer = None
                MyClass.count = 0
                MyClass.videoExtracted = MyClass.videoExtracted + 1

            configure(MyClass, window, lbl_framecount,
                      lbl_frameExtra, lbl_videoGener, lbl_progress__)

    print('Finish Extract Video Parts!')
    lbl_progress__.configure(text="Merging videoparts..",
                             foreground="red")
    window.update()

def crop_frame(MyClass, draw_square=False):
    if MyClass.baseNameFile != None:

        def mouse_callback(event, x, y, flags, params):
            if event == 1:
                global right_clicks
                MyClass.right_clicks.append([x, y])
                if MyClass.right_clicks.__len__() == 2:
                    cv2.destroyAllWindows()
                    MyClass.cropped = True
                    x1, y1 = MyClass.right_clicks[0]
                    x2, y2 = MyClass.right_clicks[1]
                    roi = frame_aux[y1:y2, x1:x2]
                    MyClass.width = int(roi.shape[1])
                    MyClass.height = int(roi.shape[0])
                    MyClass.dsize = (MyClass.width, MyClass.height)
                    cv2.destroyAllWindows()

                if MyClass.right_clicks.__len__() == 1:
                    # cv2.destroyAllWindows()
                    frame_aux2 = frame.copy()
                    cv2.putText(frame_aux2, "Now, Pick Second Point", (20, 80),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
                    cv2.imshow("Temp", frame_aux2)
                    

        MyClass.right_clicks.clear()
        count = 0
        cap1 = cv2.VideoCapture(MyClass.fullPathFile)
        while True:
            count = 1
            _, frame = cap1.read()
            cv2.namedWindow('Temp', cv2.WINDOW_AUTOSIZE)
            
            if draw_square:
                draw_squares(frame, 20)
            frame_aux = frame.copy()
            cv2.putText(frame_aux, "Please Pick First Point", (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
            
            cv2.setMouseCallback('Temp', mouse_callback)
            cv2.imshow("Temp", frame_aux)
            cv2.waitKey(0)
            if count == 1:
                cap1.release
                cv2.destroyAllWindows()
                break
    else:
        messagebox.showerror(
            message="You must select a file first", title="Error")


def open_video(MyClass, lbl_open_video, lbl_frames____, lbl_frameRate_):

    def openfn():
        cleanVar(MyClass)
        filename = filedialog.askopenfilename(title='open')
        if filename == '':
            print('No selection')
            return 0

        if filename != '':
            MyClass.fullPathFile = filename
            MyClass.baseNameFile = getBaseName(filename)
            MyClass.formatFile = getFileFormatExtension(filename)
            MyClass.dirFile = getFolderPath(filename)
            return filename

    videofile = openfn()
    if videofile != 0:
        cap = cv2.VideoCapture(videofile)
        ret, frame = cap.read()
        height, width, _ = frame.shape
        MyClass.dsize = (int(width), int(height))
        MyClass.width = width
        MyClass.height = height
        MyClass.totalframes = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        MyClass.framerate = cap.get(cv2.CAP_PROP_FPS)
        MyClass.videoparts = round(
            MyClass.totalframes/(MyClass.framerate*10)) + 1
        cap.release
        lbl_open_video.configure(text=MyClass.baseNameFile)
        lbl_frames____.configure(
            text="Total frames: " + str(MyClass.totalframes))
        lbl_frameRate_.configure(
            text="Frame rate: " + str(round(MyClass.framerate, 2)))

        print("Name: ", MyClass.baseNameFile)
        print("Total Frames: ", MyClass.totalframes)
        print("Framerate: ", int(MyClass.framerate))
        print("Width:", MyClass.width)
        print("Height:", MyClass.height)


def process(MyClass, window, lbl_framecount, lbl_frameExtra, lbl_videoGener, lbl_progress__, replace=False):

    if MyClass.baseNameFile != None:
        make_video_parts(MyClass, window, lbl_framecount,
                         lbl_frameExtra, lbl_videoGener, lbl_progress__)

        merge_videos(pathOut=MyClass.dirFile,
                     name=MyClass.baseNameFile,
                     replace=replace,
                     temp_folder=MyClass.temp_folder_path)
        print('Final Video Created!')
        deleteFilesInFolder(MyClass.temp_folder_path)
        cleanVar(MyClass)
        lbl_progress__.configure(text="Done!",
                                 foreground='white',
                                 background='green'
                                 )
    else:
        messagebox.showerror(
            message="You must select a file first", title="Error")
