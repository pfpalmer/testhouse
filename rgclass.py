import pexpect
import sys
from time import sleep

class  gateway:
    serialNumer=None

class nvg599(gateway):
    def __init__(self):
        rg599 = pexpect.spawn("telnet 192.168.1.254")
        sleep(1)
        self.name="abc"
        airtiesIPList=[]
        rgClientList=[]

    def getRGStatusInfo(self):
        pass

    def get4920Info(self):
        sn4920=None
        fw4920=None

    def login(self):
        pass

class nvg5268(gateway):
    def __init__(self):
        self.name="abc"
        rg5268 = pexpect.spawn("telnet 192.168.1.254")
        sleep(1)


class airTies4920():
    pass

