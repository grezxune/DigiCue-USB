class OptionList_Command_MacAddr(object):
    def __init__(self, parent):
        self.parent = parent

    def set(self, value):  # run when option list is changed
        print "Selected MAC Address " + value
        self.parent.macaddrs.set(value)
        self.parent.macaddr = value
        self.parent.dcb.macaddr_filter = value