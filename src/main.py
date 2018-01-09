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


def main():
    try:
        f = open("comport.cfg", "r")
        comport = f.readline().strip(' ')
        f.close()
    except BaseException:
        # open comport selection gui
        serialport.launch_selection()
        return

    try:
        # open serial port and launch application
        print "Opening %s" % comport
        ser = serial.Serial(comport, 115200, timeout=1, writeTimeout=1)
        dcb = DigicueBlue(filename="data.csv", debugprint=False)
        app = App(dcb)
        bg = Bluegiga(dcb, ser, debugprint=True)
    except BaseException:
        print traceback.format_exc()
        try:
            ser.close()
        except BaseException:
            print 'Unable to open %s' % comport
        finally:
            # Exits all threads of the application
            os._exit(1)
        text = """Please make sure the BLED112 dongle is plugged into the COM port
                specified in comport.cfg, and that no other programs are using the port.
                Use the serialport GUI to help select the correct port."""
        text = text.replace('\n', ' ')
        text = text.replace('\t', '')
        print text
        serialport.launch_selection()


if __name__ == '__main__':
    main()
