import pexpect
import sys
from time import sleep

class  gateway:
    serialNumer=0

class nvg599(gateway):
    def __init__(self):
        rg599 = pexpect.spawn("telnet 192.168.1.254")
        sleep(1)
        self.name="abc"

    def login(self):
        pass

class nvg5268(gateway):
    def __init__(self):
        self.name="abc"
        rg5268 = pexpect.spawn("telnet 192.168.1.254")
        sleep(1)

