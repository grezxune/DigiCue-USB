#!/usr/bin/env python

# Nathan Rhoades 10/13/2017

from digicueblue import DigicueBlue
from bgapi import Bluegiga

import serial
import serialport
import traceback
import time
import threading
import sys
import os

from gui.main_gui import GUI

if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk


class App(threading.Thread):  # thread GUI to that BGAPI can run in background
    def __init__(self, dcb):
        self.dcb = dcb
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = Tk.Tk()
        self.gui = GUI(self.root, self.dcb)
        self.root.mainloop()


def read_comport():
    comport = None

    if os.path.isfile('comport.cfg'):
        f = open('comport.cfg', 'r')
        comport = f.readline().strip(' ')
        f.close()

    return comport


def select_comport():
    serialport.launch_selection(start_main_gui)


def start_main_gui(comport):
    try:
        print "Opening %s" % comport

        # Open serial port
        ser = serial.Serial(comport, 115200, timeout=1, writeTimeout=1)

        dcb = DigicueBlue(filename="data.csv", debugprint=False)

        # Launch main gui
        app = App(dcb)

        bg = Bluegiga(dcb, ser, debugprint=True)
    except BaseException:
        print traceback.format_exc()
        try:
            ser.close()
        except BaseException:
            print 'Unable to open %s' % comport
        finally:
            text = "Please make sure the BLED112 dongle is plugged into the COM port "
            text += "specified in comport.cfg, and that no other programs are using the port. "
            text += "Use the serialport GUI to help select the correct port."

            print text
            # Exits all threads of the application
            os._exit(1)


def main():
    comport = read_comport()

    if comport is None:
        select_comport()
    else:
        start_main_gui(comport)


if __name__ == '__main__':
    main()
