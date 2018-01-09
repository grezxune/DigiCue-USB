import sys
import helptext

if sys.version_info[0] < 3:
    import Tkinter as Tk
    import ttk
else:
    import tkinter as Tk
    from tkinter import ttk

from scorebars import ScoreBars
from option_list_command_mac_addr import OptionList_Command_MacAddr

VERSION = "1.0.0"

class GUI(object):
    def __init__(self, master, dcb):
        # All variables from DigiCue Blue are exposed through class variables
        # in dcb

        self.dcb = dcb
        self.packet_count = dcb.packet_count
        self.master = master
        master.after(500, self.timer)  # register timer
        master.title("DigiCue Blue BLED112 GUI - Version %s" % VERSION)

        self.tabs = ttk.Notebook(master)
        self.tab1 = Tk.Frame(self.tabs, padx=10, pady=10)
        self.tab3 = Tk.Frame(self.tabs, padx=10, pady=10)
        self.tab5 = Tk.Frame(self.tabs, padx=10, pady=10)
        self.tabs.add(self.tab1, text='Shots')
        self.tabs.add(self.tab3, text='Configure')
        self.tabs.add(self.tab5, text='Help')
        self.tabs.pack(fill=Tk.BOTH, expand=Tk.YES)

        # Help tab
        message = helptext.help
        frame = Tk.Frame(self.tab5)
        text = Tk.Text(frame, height=30, width=100, wrap=Tk.WORD)
        text.insert(Tk.END, message)
        scroll = Tk.Scrollbar(frame)
        text.configure(yscrollcommand=scroll.set)
        text.pack(side=Tk.LEFT)
        scroll.pack(side=Tk.RIGHT, fill=Tk.Y)
        frame.pack(side=Tk.TOP)
        text.config(state=Tk.DISABLED)

        # Mac addr select
        frame = Tk.Frame(self.tab3)
        frame.pack(fill=Tk.X)
        self.macaddr = None
        self.macaddrs_list = []
        self.macaddr_commands = []
        lbl = Tk.Label(frame, text="DigiCue Blue MAC Address", width=25)
        lbl.pack(side=Tk.LEFT)
        self.macaddrs = Tk.StringVar(frame)
        self.macaddrs.set("<Auto Detect>")
        self.macaddrs_combo = Tk.OptionMenu(
            frame, self.macaddrs, "<Auto Detect>")
        self.macaddrs_combo.pack(side=Tk.LEFT)

        # Configuration selection
        frame = Tk.Frame(self.tab3)
        frame.pack(fill=Tk.X)
        label = Tk.Label(frame, text="Configure")
        label.pack(side=Tk.LEFT)

        self.options_configig = {}
        fbox = Tk.Frame(self.tab3, relief=Tk.GROOVE, bd=2)
        fbox.pack(fill=Tk.X)
        for label, modes in dcb.config_options:
            frame = Tk.Frame(fbox)
            frame.pack(fill=Tk.X)
            lbl = Tk.Label(frame, text=label, width=25)
            lbl.pack(side=Tk.LEFT)
            v = Tk.StringVar()
            b = Tk.Radiobutton(
                frame,
                text="Off",
                variable=v,
                value=-1,
                indicatoron=0,
                width=10,
                command=self.check_setting_config)
            b.pack(side=Tk.LEFT)
            for text, mode in modes:
                if text <> "Off":
                    b = Tk.Radiobutton(
                        frame,
                        text=text,
                        variable=v,
                        value=mode,
                        indicatoron=0,
                        width=10,
                        command=self.check_setting_config)
                    b.pack(side=Tk.LEFT)
            self.options_configig[label] = v
        frame = Tk.Frame(fbox, pady=10)
        frame.pack(fill=Tk.X)
        lbl = Tk.Label(frame, text="", width=25)
        lbl.pack(side=Tk.LEFT)
        self.sync_label = Tk.StringVar(frame)
        self.sync_label.set("Press button on DigiCue Blue once to detect")
        lbl = Tk.Label(frame, textvariable=self.sync_label)
        lbl.pack(side=Tk.LEFT)

        # Shots tab
        self.scorebars = ScoreBars(self.tab1, dcb)

    def refresh_setting_config(self):
        self.options_configig["Shot Interval"].set(
            self.dcb.threshset_shotpause if self.dcb.setting_shotpause else -1)
        self.options_configig["Backstroke Pause"].set(
            self.dcb.threshset_bspause if self.dcb.setting_bspause else -1)
        self.options_configig["Jab"].set(
            self.dcb.threshset_jab if self.dcb.setting_jab else -1)
        self.options_configig["Follow Through"].set(
            self.dcb.threshset_followthru if self.dcb.setting_followthru else -1)
        self.options_configig["Tip Steer"].set(
            self.dcb.threshset_steering if self.dcb.setting_steering else -1)
        self.options_configig["Straightness"].set(
            self.dcb.threshset_straightness if self.dcb.setting_straightness else -1)
        self.options_configig["Finesse"].set(
            self.dcb.threshset_power if self.dcb.setting_power else -1)
        self.options_configig["Finish"].set(
            self.dcb.threshset_freeze if self.dcb.setting_freeze else -1)
        self.options_configig["Vibrate On Pass"].set(
            self.dcb.setting_vop if self.dcb.setting_vop else -1)
        self.options_configig["Disable All Vibrations"].set(
            self.dcb.setting_dvibe if self.dcb.setting_dvibe else -1)
        self.check_setting_config()

    def check_setting_config(self):

        configuration = {}
        for key in self.options_configig:
            configuration[key] = self.options_configig[key].get()
        self.dcb.set_config(configuration)

        if not self.check_setting_config_test():
            self.sync_label.set("Press button on DigiCue Blue twice to sync")
        else:
            self.sync_label.set("Configuration matches DigiCue Blue")

    def check_setting_config_test(self):

        a = 0

        def val(x): return -2 if len(x) == 0 else x

        tmp = int(val(self.options_configig["Shot Interval"].get()))
        if self.dcb.setting_shotpause:
            a += int(tmp == self.dcb.threshset_shotpause)
        else:
            a += int(tmp == -1)

        tmp = int(val(self.options_configig["Backstroke Pause"].get()))
        if self.dcb.setting_bspause:
            a += int(tmp == self.dcb.threshset_bspause)
        else:
            a += int(tmp == -1)

        tmp = int(val(self.options_configig["Jab"].get()))
        if self.dcb.setting_jab:
            a += int(tmp == self.dcb.threshset_jab)
        else:
            a += int(tmp == -1)

        tmp = int(val(self.options_configig["Follow Through"].get()))
        if self.dcb.setting_followthru:
            a += int(tmp == self.dcb.threshset_followthru)
        else:
            a += int(tmp == -1)

        tmp = int(val(self.options_configig["Tip Steer"].get()))
        if self.dcb.setting_steering:
            a += int(tmp == self.dcb.threshset_steering)
        else:
            a += int(tmp == -1)

        tmp = int(val(self.options_configig["Straightness"].get()))
        if self.dcb.setting_straightness:
            a += int(tmp == self.dcb.threshset_straightness)
        else:
            a += int(tmp == -1)

        tmp = int(val(self.options_configig["Finesse"].get()))
        if self.dcb.setting_power:
            a += int(tmp == self.dcb.threshset_power)
        else:
            a += int(tmp == -1)

        tmp = int(val(self.options_configig["Finish"].get()))
        if self.dcb.setting_freeze:
            a += int(tmp == self.dcb.threshset_freeze)
        else:
            a += int(tmp == -1)

        tmp = int(val(self.options_configig["Vibrate On Pass"].get()))
        if self.dcb.setting_vop:
            a += int(tmp == self.dcb.setting_vop)
        else:
            a += int(tmp == -1)

        tmp = int(val(self.options_configig["Disable All Vibrations"].get()))
        if self.dcb.setting_dvibe:
            a += int(tmp == self.dcb.setting_dvibe)
        else:
            a += int(tmp == -1)

        return a == 10

    def refresh_macaddrs(self):
        self.macaddrs.set('')
        self.macaddrs_combo['menu'].delete(0, 'end')
        self.macaddr_commands = []
        for choice in self.macaddrs_list:
            optioncmd = OptionList_Command_MacAddr(self)
            self.macaddr_commands.append(optioncmd)
            command = Tk._setit(optioncmd, choice)
            self.macaddrs_combo['menu'].add_command(
                label=choice, command=command)

    def timer(self):
        if self.dcb.macaddr not in self.macaddrs_list:
            if self.dcb.macaddr <> None:
                # Only add DigiCue Blue devices / correct manuf. ID
                self.macaddrs_list.append(self.dcb.macaddr)
                if self.macaddr is None:
                    self.macaddr = self.dcb.macaddr
                    self.dcb.macaddr_filter = self.macaddr
                self.refresh_macaddrs()
                self.macaddrs.set(self.macaddr)

        if self.packet_count <> self.dcb.packet_count:
            self.packet_count = self.dcb.packet_count

            # Update configuration
            self.refresh_setting_config()

            # Update graphics here
            if self.dcb.data_type == 0:  # Version packet
                pass
            elif self.dcb.data_type == 1:  # update gui if data packet
                self.scorebars.update()

        self.master.after(500, self.timer)
