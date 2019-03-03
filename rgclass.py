import pexpect
import re
from selenium import webdriver
import sys
from time import sleep

nvgInfo = { "228946241148656" : {'model':'nvg599','dac':"*<#/53#1/2", 'magic': 'kjundhkdxlxr','mac2g': 'd0:39:b3:60:56:f1','mac5g':'d0:39:b3:60:56:f4', 'wiFi': 'c2cmybt25dey','ssid': 'ATTqbrAnYs'},
               "277427577103760" : {'model':'nvg599','dac': '<<01%//4&/','magic': "ggtxstgwipcg", 'mac2g': 'fc:51:a4:2f:25:90', 'mac5g': 'fc:51:a4:2f:25:94', 'wiFi': 'nsrmpr59rxwv', 'ssid' : 'ATTqbrAnYs'}}

class  gatewayClass():
    def __init__(self):
        self.serialNumer = None
        self.magic = None
        self.upTime = None
        self.IP = None

class nvg599Class(gatewayClass):
    def __init__(self):
        #rg599 = pexpect.spawn("telnet 192.168.1.254")
        #sleep(1)
        self.IP ="192.168.1.254"


        global nvgInfo


        self.session = None

        airtiesIPList=[]
        rgClientList=[]

        #self.session = pexpect.spawn("telnet 192.168.1.254", encoding='utf-8')
        #self.session.expect("ogin:")
        #self.session.sendline('admin')
        #self.session.expect("ord:")
        #self.session.sendline('<<01%//4&/')
        #self.session.expect(">")
        #print('i am init')

        # driver = webdriverhttps://www.waketech.edu/programs-courses/credit/electrical-systems-technology/degrees-pathways.Chrome('/usr/local/bin/chromedriver')

        #self.webDriver.find_element_by_link_text("Settings").click()


    def createWebdriver(self):
        self.webDriver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
        # driver.get('http://www.google.com')
        self.webDriver.get('http://192.168.1.254')
        self.webDriver.implicitly_wait(20)
        # driver.find_elements_by_tag_name("Settings") // this is for 599

    def getSNFromUI(self):
        self.webDriver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
        # driver.get('http://www.google.com')
        self.webDriver.get('http://192.168.1.254')
        self.webDriver.implicitly_wait(20)
        # driver.find_elements_by_tag_name("Settings") // this is for 599


    def loginNVG599(self):
        print('i am in login')
        self.session = pexpect.spawn("telnet 192.168.1.254", encoding='utf-8')
        self.session.expect("ogin:")
        self.session.sendline('admin')
        self.session.expect("ord:")
        self.session.sendline('<<01%//4&/')
        self.session.expect(">")
        return self.session
 #       self.session.sendline('status')
 #       self.session.expect(">")

  #      statusOutput = self.session.before
  #      print(statusOutput)



    #    statusInfoRegEx = re.compile(r'Model\s(\w+)\s+\w+/\w+.*number\s+(\w+).*Uptime\s+(\d\d:\d\d:\d\d:\d\d)',re.DOTALL)
        # statusInfoRegEx = re.compile(r'Model\s(\w+).*Serial Number\s+(\d+)',re.DOTALL)
        # statusInfoRegEx = re.compile(r'Model\s(\w+)')
    #    mo1 = statusInfoRegEx.search(statusOutput)
     #   print(mo1)
    #    print('model ', mo1.group(1))
    #    print('Serial Number', mo1.group(2))
    #    print('Uptime ', mo1.group(3))
    #    self.serialNumber = mo1.group(2)
     #   self.upTime = mo1.group(1)

    #    @classmethod

    def connectCLI(self, ip):
        self.IP = ip
        #cls.ssh = pexpect.spawn('ssh ' + name)
        print('i am iconnect')
        session = pexpect.spawn("telnet 192.168.1.254", encoding='utf-8')
        session.expect("ogin:")
        session.sendline('admin')
        session.expect("ord:")
        session.sendline('<<01%//4&/')
        session.expect(">")
        session.sendline('status')
        session.expect('>')
        statusOutput = session.before
        statusInfoRegEx = re.compile(r'Model\s(\w+)\s+\w+/\w+.*number\s+(\w+).*Uptime\s+(\d\d:\d\d:\d\d:\d\d)',re.DOTALL)
            # statusInfoRegEx = re.compile(r'Model\s(\w+).*Serial Number\s+(\d+)',re.DOTALL)
            # statusInfoRegEx = re.compile(r'Model\s(\w+)')
        mo1 = statusInfoRegEx.search(statusOutput)
        print(mo1)
        print('model ', mo1.group(1))
        print('Serial Number', mo1.group(2))
        print('Uptime ', mo1.group(3))
        self.serialNumber =  mo1.group(2)
        self.upTime = mo1.group(1)



    def turnOffSupplicant(self):

        self.session = self.loginNVG599()
        self.session.sendline('magic')
        self.session.expect("UNLOCKED>")
        self.session.sendline('conf')
        self.session.expect("top\)>>")
        self.session.sendline('system supplicant')
        self.session.expect("\(system supplicant\)>>")
        #self.session.expect(">>")
        self.session.sendline('set')
        self.session.expect("]:")
        self.session.sendline('off')
        self.session.expect("\(system supplicant\)>>")
        self.session.sendline('save')
            # should check for "Configuration data saved.  as well
            # NOS/277427577103760 (system supplicant)>>
        self.session.expect("\(system supplicant\)>>")
        self.session.sendline('exit')
        self.session.expect("UNLOCKED>")
        self.session.sendline('exit all')
        print('hello from inside turn off supplicant')
        self.session.close()

        exit()

        #cls.ssh.expect('password:')
        #.ssh.sendline('*****')
        #cls.ssh.expect('> ')
        #print
        #.ssh.before, cls.ssh.after
        #.Is_connected = True


    def printme(self):
        print('I am an NVG599 object')

    def getRGSerialNumber(self):
        self.session.sendline('status')
        self.session.expect('>')
        statusOutput = self.session.before
        print('i am getSerialnumber')
        statusInfoRegEx = re.compile(r'Model\s(\w+)\s+\w+/\w+.*number\s+(\w+).*Uptime\s+(\d\d:\d\d:\d\d:\d\d)',
                                     re.DOTALL)
        # statusInfoRegEx = re.compile(r'Model\s(\w+).*Serial Number\s+(\d+)',re.DOTALL)
        # statusInfoRegEx = re.compile(r'Model\s(\w+)')
        mo1 = statusInfoRegEx.search(statusOutput)
        #print(mo1)
        #print('model ', mo1.group(1))

        #print('Serial Number', mo1.group(2))
        #print('Uptime ', mo1.group(3))
        return mo1.group(2)


    def get4920Info(self):
        sn4920=None
        fw4920=None

    def login(self):
        pass

class nvg5268Class(gatewayClass):
    def __init__(self):
        self.name="abc"
        rg5268 = pexpect.spawn("telnet 192.168.1.254")
        sleep(1)


class airTies4920():
    pass

