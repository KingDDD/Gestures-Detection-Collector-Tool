#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   Launches a Graphical User Interface to facilitate simple gesture video data
#   collection
#   Created on November 20, 2017
#-------------------------------------------------------------------------------
#   Copyright (c) 201x Magic Leap, Inc. (COMPANY) All Rights Reserved.
#   Magic Leap, Inc. Confidential and Proprietary
#
#   NOTICE:  All information contained herein is, and remains the property
#   of COMPANY. The intellectual and technical concepts contained herein
#   are proprietary to COMPANY and may be covered by U.S. and Foreign
#   Patents, patents in process, and are protected by trade secret or
#   copyright law.  Dissemination of this information or reproduction of
#   this material is strictly forbidden unless prior written permission is
#   obtained from COMPANY.  Access to the source code contained herein is
#   hereby forbidden to anyone except current COMPANY employees, managers
#   or contractors who have executed Confidentiality and Non-disclosure
#   agreements explicitly covering such access.
#
#   The copyright notice above does not evidence any actual or intended
#   publication or disclosure  of  this source code, which includes
#   information that is confidential and/or proprietary, and is a trade
#   secret, of  COMPANY.   ANY REPRODUCTION, MODIFICATION, DISTRIBUTION,
#   PUBLIC  PERFORMANCE, OR PUBLIC DISPLAY OF OR THROUGH USE  OF THIS
#   SOURCE CODE  WITHOUT THE EXPRESS WRITTEN CONSENT OF COMPANY IS
#   STRICTLY PROHIBITED, AND IN VIOLATION OF APPLICABLE LAWS AND
#   INTERNATIONAL TREATIES.  THE RECEIPT OR POSSESSION OF  THIS SOURCE
#   CODE AND/OR RELATED INFORMATION DOES NOT CONVEY OR IMPLY ANY RIGHTS
#   TO REPRODUCE, DISCLOSE OR DISTRIBUTE ITS CONTENTS, OR TO MANUFACTURE,
#   USE, OR SELL ANYTHING THAT IT  MAY DESCRIBE, IN WHOLE OR IN PART.
#-------------------------------------------------------------------------------
#   This will ask for username, handedness, and PEQ s/n
#   upon "Submit":
#
#   	Show Gesture Image
#   	Record the User
#   	Stop Recording
#   	Next Gesture Image
#	repeat
#
#   "Pull Recordings" downloads the recordings off the PEQ
#   "Clear Device" clears the PEQ's recordings folder
#   "New Collection" restarts the GUI ready for a new user
#   "Connect" attempts to pair PEQ with Computer through Wifi
#
#   USAGE:
#   ./GUI.py
#
#   Created on November 20, 2017
#   author="Damian Lopez"

from subprocess import *
import subprocess
import os
from Tkinter import *
import tkFont
from PIL import ImageTk, Image
import random
import datetime
import tempfile
import shutil
import sys


# These lines set the working directory for the Gesture GUI
# As well as which gesture study to be recorded.
# The dict_config_*.txt will define which gesture demonstration files
# will be loaded into the image dictionary
install_path = os.getcwd()
base_path = install_path[:-33]
thread_path = os.path.join("{}/gestures/data-collection/images/".format(base_path))
#print thread_path

os.chdir("{}".format(thread_path))


file = open("{}/gestures/data-collection/dict_config.txt".format(base_path),"r")

# Image_DN creates a dictionary of the gesture names as keys and their values
# are the images associated with that key.

IMAGE_DN = {}
for line in file:
    x = line.split(',')
    a=x[0]
    b=x[1]
    c=len(b)-1
    b=b[0:c]
    IMAGE_DN[a]=b

STATIC_GESTURES=list(IMAGE_DN.keys())
random.shuffle(STATIC_GESTURES)

# we run datetime to get the correct date, as the date is used as a searchable
# tag on datasets WebUI

dt = datetime.datetime.now()

date = dt.strftime("%Y%m%d")

class Window(Frame):

    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master.resizable(False, False)
        self.configure(background="#A7B8BF")

        self.master = master

        self.init_window()

    def init_window(self):
        self.master.title("Gesture GUI")

        global count
        count = 0

        global current_gesture
        current_gesture = StringVar()

        global current_image
        current_image = StringVar()

        nameEnt= StringVar()
        handEnt= StringVar()
        peqEnt= StringVar()
        show= StringVar()
        log= StringVar()
        log =  "Enter Information & Submit"

        #gestures = [STATIC_GESTURES]
        #images = [IMAGE_FILES]

        label1 = Label(root, text="Name", font=goth10, bg="#A7B8BF", fg="black")
        label1.place(x=50, y=20)

        label2 = Label(root, text="Handedness", font=goth10, bg="#A7B8BF", fg="black")
        label2.place(x=11, y=40)

        label3 = Label(root, text="PEQ #", font=goth10, bg="#A7B8BF", fg="black")
        label3.place(x=47,y=60)

        labelLog = Label(root, text=log, font=goth12, bg="#A7B8BF", fg="black")
        labelLog.place(x=15,y=200)
        self.labelLog=labelLog

        entry1 = Entry(root, bg="thistle1")
        entry1.place(x=95,y=20)
        self.entry1=entry1
        #self.entry1.configure(state=DISABLED)

        entry2 = Entry(root, bg="thistle1")
        entry2.place(x=95,y=40)
        self.entry2=entry2
        #self.entry2.configure(state=DISABLED)

        entry3 = Entry(root, bg="thistle1")
        entry3.place(x=95,y=60)
        self.entry3=entry3
        #self.entry3.configure(state=DISABLED)


        load = Image.open('{}/gestures/data-collection/images/leaper.png'.format(base_path))
        img = ImageTk.PhotoImage(load)

        logo = Label(self, image=img)
        logo.image = img
        logo.place(x=252,y=10)

        self.pack(padx=10, pady=10, fill=BOTH, expand=1)

        self.master.bind('<Escape>', self.client_exit)
        self.master.bind('<Return>', self.submit_field)


        subButton = Button(self, text="Submit", font=goth10, bg="#bad6d8", command=self.submit_field)
        subButton.place(x=176,y=75)
        self.subButton=subButton
        #self.subButton.configure(state=DISABLED)
        #for gesture_list in STATIC_GESTURES:

        startButton = Button(self, text="Show Image", font=goth10, bg="#bad6d8", command=self.show_image)
        startButton.place(x=5,y=110)
        self.startButton=startButton
        #self.startButton.configure(state=DISABLED)

        recButton = Button(self, text="Start REC.", font=goth10, bg="#bad6d8", command=self.start_rec)
        recButton.place(x=120,y=110)
        self.recButton=recButton
        #self.recButton.configure(state=DISABLED)

        stopButton = Button(self, text="Stop REC.", font=goth10, bg="#bad6d8", command=self.stop_rec)
        stopButton.place(x=219,y=110)
        self.stopButton=stopButton
        #self.stopButton.configure(state=DISABLED)

        nextButton = Button(self, text="Next Image", font=goth10, bg="#bad6d8", command=self.next_gest)
        nextButton.place(x=318,y=110)
        self.nextButton=nextButton
        #self.nextButton.configure(state=DISABLED)

        shellButton = Button(self, text="Launch Terminal", font=goth10, bg="#bad6d8", command=self.open_terminal)
        shellButton.place(x=5,y=145)
        self.shellButton=shellButton
        #self.shellButton.configure(state=DISABLED)

        pullButton = Button(self, text="Pull Recordings", font=goth10, bg="#bad6d8", command=self.pull_data)
        pullButton.place(x=152,y=145)
        self.pullButton=pullButton
        self.pullButton.configure(state=DISABLED)

        delButton = Button(self, text="Clear Device", font=goth10, bg="#bad6d8", command=self.delete_recs)
        delButton.place(x=299,y=145)
        self.delButton=delButton
        #self.delButton.configure(state=DISABLED)

        resButton = Button(self, text="New Collection", font=goth10, bg="#bad6d8", command=self.reset_gui)
        #resButton.place(x=5,y=75)
        self.resButton=resButton
	self.resButton.configure(state=DISABLED)

        wrlsButton = Button(self, text="⚡Connect⚡", font=goth10, bg="#bad6d8", command=self.connect)
        wrlsButton.place(x=320,y=180)
        self.wrlsButton=wrlsButton
	self.wrlsButton.configure(state=DISABLED)


    def open_terminal(self):
        subprocess.call("gnome-terminal", shell=True)


    def connect(self, event=None):
        os.chdir("{}/gestures/data-collection/utils/".format(base_path))
        cnct_cmd = 'bash wificonnect.sh'
        fnull = open(os.devnull, 'w')
        subprocess.call(cnct_cmd.split(), stdout=fnull, stderr=subprocess.STDOUT)
        os.chdir("{}".format(z))

    def start_rec(self, event=None):
        cmd = 'mldb shell mal_recorder_control -start --depth --wcams --imus'
        # Suppress verbose logs from mal_recorder_control
        fnull = open(os.devnull, 'w')
        subprocess.call(cmd.split(), stdout=fnull, stderr=subprocess.STDOUT)
        log = "Currently RECORDING...."
        self.labelLog.configure(text=log)
        #self.recButton.configure(state=DISABLED)
        #self.stopButton.configure(state=NORMAL)
        #self.pullButton.configure(state=NORMAL)
        #self.delButton.configure(state=NORMAL)

    def stop_rec(self, event=None):
        cmd = 'mldb shell mal_recorder_control -stop'
        # Suppress verbose logs from mal_recorder_control
        fnull = open(os.devnull, 'w')
        subprocess.call(cmd.split(), stdout=fnull, stderr=subprocess.STDOUT)
        log = "RECORDING Stopped // Data Saved"
        self.labelLog.configure(text=log)

        person_id = nameEnt
        peq_id = peqEnt
        gesture = current_gesture

        rename(person_id, peq_id, gesture)
        #self.stopButton.configure(state=DISABLED)
        #self.nextButton.configure(state=NORMAL)

    def next_gest(self, event=None):
        global count
        count += 1
        loop_func(self)
        log = "Show Next Image"
        self.labelLog.configure(text=log)
        #self.nextButton.configure(state=DISABLED)
        #self.startButton.configure(state=NORMAL)


    def reset_gui(self, event=None):
        os.execv(__file__, sys.argv)

    def client_exit(self, event=None):
        global root
        root.destroy()

    def submit_field(self, event=None):
        global nameEnt, handEnt, peqEnt, log

        nameEnt = self.entry1.get()
        handEnt = self.entry2.get()
        peqEnt = self.entry3.get()
        log = "Info Collected ........ Show First Image"

        self.entry1.configure(state=DISABLED)
        self.entry2.configure(state=DISABLED)
        self.entry3.configure(state=DISABLED)
        self.subButton.configure(state=DISABLED)
        #self.startButton.configure(state=NORMAL)
        #self.pullButton.configure(state=DISABLED)
        #self.delButton.configure(state=DISABLED)

        loop_func(self)
        self.labelLog.configure(text=log)

    def show_image(self):
        top = Toplevel()
        top.title("Image Window")
        log = "Start The Recording........."
        self.labelLog.configure(text=log)

        button = Button(top, text="Dismiss", command=top.destroy)
        button.pack()
        photo = ImageTk.PhotoImage(Image.open(IMAGE_DN[current_gesture]))

        l = Label(top, image = photo)
        l.image = photo
        l.pack()
        #self.startButton.configure(state=DISABLED)
        #self.recButton.configure(state=NORMAL)

    def pull_data(self):
        log = "Pulling User Data..........."
        self.labelLog.configure(text=log)
        self.grab_recordings
        log = "Data Migration Complete"
        self.labelLog.configure(text=log)
        self.pullButton.configure(state=DISABLED)

    def grab_recordings(self):


        pull_from_dir = os.path.join('/data/local/tmp/recordings', date, nameEnt)
    	pull_to_dir = os.path.join('{}/gestures/data-collection/recordings'.format(base_path), date)
    	recording_dir = os.path.join(pull_to_dir, nameEnt)
    	get_recordings(pull_from_dir, pull_to_dir)
    	get_cal_file(pull_from_dir, recording_dir)

    def test_func(self):

        print(current_gesture)

    def delete_recs(self):
        pull_from_dir = os.path.join('/data/local/tmp/recordings')
        rm_cmd = 'mldb shell rm -rf {}'.format(pull_from_dir)
        subprocess.call(rm_cmd.split())
        mk_cmd = 'mldb shell mkdir {}'.format(pull_from_dir)
        subprocess.call(mk_cmd.split())
        log = "Device Has Been Cleared"
        self.labelLog.configure(text=log)

def rename(person_id, peq_id, gesture):

    default_dir = '/data/local/tmp/recordings/'

    date = datetime.datetime.now().strftime("%Y%m%d")
    new_dir = os.path.join(default_dir, date, person_id)
    mkdir_cmd = 'mldb shell mkdir -p {}'.format(new_dir)
    subprocess.call(mkdir_cmd.split())

    recording = peq_list_files(default_dir)
    if len(recording) == 1:
        recording = recording[0]
        fname = make_file_name(person_id, peq_id, gesture, new_dir)
        cmd = 'mldb shell mv {} {}'.format(recording, fname)

        subprocess.call(cmd.split())


def file_exists(new_dir, file_name):

    path = os.path.join(new_dir, file_name)

    cmd = 'mldb shell test -f {} ; echo $?'.format(path)
    output = subprocess.check_output(cmd.split())

    return output[0] == '0'

def make_file_name(person_id, peq_id, gesture, new_dir):

    date = datetime.datetime.now().strftime("%Y%m%d")

    i = 0
    file_name = '{}_{}_{}_{}_{}.RECORDING'.format(date, peq_id, person_id,
                                                  gesture, str(i))

    while file_exists(new_dir, file_name):
        i += 1
        file_name = '{}_{}_{}_{}_{}.RECORDING'.format(date, peq_id, person_id,
                                                      gesture, str(i))
    file_name = os.path.join(new_dir, file_name)
    return file_name

def peq_list_files(default_dir):

    cmd = 'mldb shell find %s -name \"*.RECORDING\" -maxdepth 1' % default_dir

    result = subprocess.check_output(cmd.split())
    result = result.split('\n')

    rec_file = []
    for recording in result:
        if '.RECORDING' in recording:
            rec_file.append(recording)
    return rec_file


def get_recordings(pull_from, pull_to):
    root_cmd = 'mldb root'
    subprocess.call(root_cmd.split())
    mkdir_cmd = 'mkdir {}'.format(pull_to)
    subprocess.call(mkdir_cmd.split())
    pull_cmd = 'mldb pull {} {}'.format(pull_from,pull_to)
    subprocess.call(pull_cmd.split())

def get_cal_file(pull_from, pull_to):
    pull_wearable_rig_cmd = 'mldb pull /persist/wearable_cal/wearable.rig {}'.format(pull_to)
    subprocess.call(pull_wearable_rig_cmd.split())

def loop_func(self, event=None):
    global current_gesture
    global current_image
    current_gesture = STATIC_GESTURES[count]
    current_image = IMAGE_DN[current_gesture]
    print(current_gesture)
    print(current_image)
    print(IMAGE_DN)
    print(STATIC_GESTURES)









root = Tk()
goth10 = tkFont.Font(family='MS Gothic', size=10)
goth12 = tkFont.Font(family='MS Gothic', size=12)

root.geometry("450x235")

app = Window(root)


root.mainloop()
