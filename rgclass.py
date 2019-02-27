import pexpect
import sys
from time import sleep


nvgInfo = { "228946241148656" : {'model':'nvg599','dac':"*<#/53#1/2", 'magic': 'kjundhkdxlxr','mac2g': 'd0:39:b3:60:56:f1','mac5g':'d0:39:b3:60:56:f4', 'wiFi': 'c2cmybt25dey','ssid': 'ATTqbrAnYs'},
               "277427577103760" : {'model':'nvg599','dac': '<<01%//4&/','magic': "ggtxstgwipcg", 'mac2g': 'fc:51:a4:2f:25:90', 'mac5g': 'fc:51:a4:2f:25:94', 'wiFi': 'nsrmpr59rxwv', 'ssid' : 'ATTqbrAnYs'}}

class  gateway:
    serialNumer=None
    magic=None

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

