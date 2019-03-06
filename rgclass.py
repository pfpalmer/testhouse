from itertools import count

import pexpect
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from bs4 import BeautifulSoup
import smtplib

import sys
from time import sleep

nvgInfo = { "228946241148656" : {'model':'nvg599','dac':"*<#/53#1/2", 'magic': 'kjundhkdxlxr','mac2g': 'd0:39:b3:60:56:f1','mac5g':'d0:39:b3:60:56:f4', 'wiFi': 'c2cmybt25dey','ssid': 'ATTqbrAnYs'},
               "277427577103760" : {'model':'nvg599','dac': '<<01%//4&/','magic': "ggtxstgwipcg", 'mac2g': 'fc:51:a4:2f:25:90', 'mac5g': 'fc:51:a4:2f:25:94', 'wiFi': 'nsrmpr59rxwv', 'ssid' : 'ATTqbrAnYs'}}

class gatewayClass():


    def __init__(self):
        self.magic = None
        self.upTime = None
        self.IP = None


    def emailTestResults(selfself,textFile):
        gmail_password="arris123"
        gmail_user= 'leandertesthouse@gmail.com'
        to = 'pfpalmer@gmail.com'
        sent_from = 'leandertesthouse:'
        subject ='Test results'
 #       body = "Results:" + channelResultContents
        body = "Results:" + textFile
        email_text = """
        From:%s
        To:%s
        Subject:%s

        %s 
        """ % (sent_from, to, subject, body)

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_password)
            server.sendmail(sent_from, to, email_text)
            sleep(2)
            server.quit()
            print("im the email section ====================")
        except:
            print('failed to send email')



class nvg599Class(gatewayClass):
    def __init__(self):
        #rg599 = pexpect.spawn("telnet 192.168.1.254")
        #sleep(1)
        self.IP ="192.168.1.254"
        self.serialNumer = None

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


    def getdeviceInfoFromUI(self):
        global nvgInfo
        url = 'http://192.168.1.254/cgi-bin/sysinfo.ha'
        browser = webdriver.Chrome()
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, 'html.parser')

        this = soup.find_all('th')
        for th in this:
            if th.text == "Model Number":
                print(th.next_sibling.next_sibling.text)
                self.modelNumber = th.next_sibling.next_sibling.text
            if th.text == "Serial Number":
                print(th.next_sibling.next_sibling.text)
                self.serialNumber = th.next_sibling.next_sibling.text

                self.DAC= nvgInfo[self.serialNumber]['dac']
                print("dac is:",self.DAC)
            if th.text == "Software Version":
                print(th.next_sibling.next_sibling.text)
                self.softwareVersion = th.next_sibling.next_sibling.text
            if th.text == "MAC Address":
                print(th.next_sibling.next_sibling.text)
                self.macAddress = th.next_sibling.next_sibling.text
            if th.text == "Time Since Last Reboot":
                print(th.next_sibling.next_sibling.text)
                self.macAddress = th.next_sibling.next_sibling.text
            if th.text == "Current Date/Time":
                print(th.next_sibling.next_sibling.text)
                self.macAddress = th.next_sibling.next_sibling.text
            if th.text == "Hardware Version":
                print(th.next_sibling.next_sibling.text)
                self.macAddress = th.next_sibling.next_sibling.text

        sleep(5)

        browser.quit()

# 2.4 bw possibilities 20,40
# 5 bw possibilities 20,40,80
# InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.BSSID fc:51:a4:2f:25:94
#  InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.AutoChannelEnable 0
#  InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.X_0000C5_BandLock X_0000   C5_5.0GHz


#tr69 GetParameterValues  InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.X_0000C5_Bandwidth
#tr69 SetParameterValues  InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.X_0000C5_Bandwidth=X_0000C5_80MHz
    # tr69 SetParameterValues  InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.X_0000C5_Bandwidth=X_0000C5_40MHz

    # InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.X_0000C5_Bandwidth X_0000C5_80MHz




    def channelTest(self,b2G,b5G,bw2G,bw5G):
        for ib2G in b2G:
            for ib5G in b5G:
                for ibw in bw:
                    print("2G:" + ib2G + " 5G:" + ib5G + "bandwidth" + ibw)


    def get4920IPFromUI(self):
        global nvgInfo
        url = 'http://192.168.1.254/cgi-bin/devices.ha'

        browser = webdriver.Chrome()

        browser.get(url)
        soup = BeautifulSoup(browser.page_source, 'html.parser')

        this = soup.find_all('th')
        for th in this:
            if th.text == "IPv4 Address / Name":
                #print(th.next_sibling.next_sibling.text)
                print("derp    ",th.text)
                print("derp1",th.next_sibling.text)
            else:
                print("no derp")

        sleep(5)

        browser.quit()

    #   def createWebdriver(self):
  #      self.webDriver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
        # driver.get('http://www.google.com')
  #      self.webDriver.get('http://192.168.1.254')
  #      self.webDriver.implicitly_wait(20)
        # driver.find_elements_by_tag_name("Settings") // this is for 599

    def getSNFromUI(self):
        self.webDriver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
        # driver.get('http://www.google.com')
        self.webDriver.get('http://192.168.1.254')
        self.webDriver.implicitly_wait(20)
        # driver.find_elements_by_tag_name("Settings") // this is for 599


    def loginNVG599(self):
        print('I am in login')
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


    def login4920(self,IP4920):
        print('I am in login')
        self.session = pexpect.spawn("telnet" + IP4920, encoding='utf-8')
        self.session.expect("ogin:")
        self.session.sendline('root')
        self.session.expect("#")
        self.session.sendline('<<01%//4&/')
        self.session.expect(">")
        return self.session
    
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
        self.session.close()



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
        session=self.loginNVG599()
        session.sendline("show ip lan")
        self.session.expect('>')
        ipLanOutput = self.session.before
        print("type:",type(ipLanOutput))
        ipLanOutputx = ipLanOutput.split('\n\r')
        print("count:", len(ipLanOutputx))
        dog =  ipLanOutputx

        print("-------------------------------------")

        count = len(dog)
        print("count",count)
        count = 2
        print("count-(1)", count)

        #for i  in range(count,len(dog)):
        #    print(dog[i])

         #print("-------------------------------------")

        dog1 = dog[2:-1]

        for i  in range(len(dog1)):
            statusInfoRegEx = re.compile(r'\b(\w+)\b(\w+)')
            #print(dog1[i])
            mo1 = statusInfoRegEx.search(dog1[i])
            print(mo1.group[0])
            #print(mo1.group[1])
        exit()
        print('i am IPLANOutput ' + ipLanOutput)
        IPLanInfoRegEx = re.compile(r'(ATT_4920.*)\s')
        mo1 = IPLanInfoRegEx.search(ipLanOutput)
        print(mo1)
        self.session.close()

    def login(self):
        pass

class nvg5268Class(gatewayClass):
    def __init__(self):
        self.name="abc"
        rg5268 = pexpect.spawn("telnet 192.168.1.254")
        sleep(1)


class airTies4920():
    pass

