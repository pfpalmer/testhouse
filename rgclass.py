from itertools import count
from selenium.webdriver.common.by import By

import pexpect
import re
import pprint
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from bs4 import BeautifulSoup
import smtplib
from collections import defaultdict
import sys
from time import sleep
import time

nvgInfo = { "228946241148656" : {'model':'nvg599','deviceAccessCode':"*<#/53#1/2", 'magic': 'kjundhkdxlxr','mac2g': 'd0:39:b3:60:56:f1','mac5g':'d0:39:b3:60:56:f4', 'wiFi': 'c2cmybt25dey','ssid': 'ATTqbrAnYs'},
              "277427577103760" : {'model':'nvg599','deviceAccessCode': '<<01%//4&/','magic': "ggtxstgwipcg", 'mac2g': 'fc:51:a4:2f:25:90', 'mac5g': 'fc:51:a4:2f:25:94', 'wiFi': 'nsrmpr59rxwv', 'ssid' : 'ATTqbrAnYs'}}

NON_DFS_CHANNELS = {36,40,44,48,149,153,157,161,165}
DFS_CHANNELS     = {52,56,60,64,100,104,108,112,116,132,136,140,144}

#class GatewayClass():


class GatewayClass:

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
 #      body = "Results:" + channelResultContents
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


class Nvg599Class(GatewayClass):
    def __init__(self):
        super(self.__class__,self).__init__()
        #rg599 = pexpect.spawn("telnet 192.168.1.254")
        #sleep(1)
        self.IP ="192.168.1.254"


        self.getdeviceInfoFromUI()
        print("self.serialNumer:",self.serialNumber)

        self.nvgInfo = {"228946241148656": {'model': 'nvg599', 'deviceAccessCode': "*<#/53#1/2", 'magic': 'kjundhkdxlxr',
                                       'mac2g': 'd0:39:b3:60:56:f1', 'mac5g': 'd0:39:b3:60:56:f4',
                                       'wiFi': 'c2cmybt25dey', 'ssid': 'ATTqbrAnYs'},
                   "277427577103760": {'model': 'nvg599', 'deviceAccessCode': '<<01%//4&/', 'magic': "ggtxstgwipcg",
                                       'mac2g': 'fc:51:a4:2f:25:90', 'mac5g': 'fc:51:a4:2f:25:94',
                                       'wiFi': 'nsrmpr59rxwv', 'ssid': 'ATTqbrAnYs'}}

        # The DAC must be read from the actual device., so it is stored in a dictionary of all the test house nvg599s

        self.devAccessCode = self.nvgInfo[self.serialNumber]['deviceAccessCode']
        print("dac",self.devAccessCode)
        print("in NVG599 init")
        #exit()
        # show IP Lan  dicitonary dicitionary
        self.showIPLanDict = {}
        # show wi client dicitionary
        self.showWiClientsDict = {}
        airtiesIPList=[]
        rgClientList=[]
        # driver = webdriverhttps://www.waketech.edu/programs-courses/credit/electrical-systems-technology/degrees-pathways.Chrome('/usr/local/bin/chromedriver')

        #self.webDriver.find_element_by_link_text("Settings").click()

    def getShWiClients(self):
        session = self.loginNVG599()
        self.session.sendline("show wi clients")
        self.session.expect('>')
        shWiClientsOutput = self.session.before
        print("-------------------------------------")
        #shWifiClinetRegEx = re.compile(r'Model\s(\w+)\s+\w+/\w+.*number\s+(\w+).*Uptime\s+(\d\d:\d\d:\d\d:\d\d)',re.DOTALL)
        # need to consider the case where there is no entries either in the 2.$GHZ, the 5GHZ oe both
        # the regex returns all the chars before the match and all the chars including the "CLients connected at 5GH" and after
        shWifiClinetRegEx = re.compile(r'(^.*?)(Clients connected on 5.0 GHz.*)',re.DOTALL)
        print(shWiClientsOutput)
        mo1 = shWifiClinetRegEx.search(shWiClientsOutput)
        print(mo1)
        print('2.4G ', mo1.group(1))
        print('------------------------------------------------------')
        print('5G ', mo1.group(2))
        G5String= mo1.group(2)
        G2string = mo1.group(1)
        #G2RegEx = re.compile(r'([0-9a-fA-F]:?){12}', re.DOTALL)
        G2RegEx = re.compile(r'(?:[0-9a-fA-F]:?){12}.*?\n.*\n.*\n.*\n')
        #G2RegEx = re.compile(r'(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w.*?)*', re.DOTALL)
        #mo1 = G2RegEx.findall(G2string)
        #mo1 = G2RegEx.findall(G2string)
        G2stringlist = re.findall(G2RegEx,G2string)

        numberOfG2Entries = len(G2stringlist)

        print("--------------------------------------the 2g list has :",numberOfG2Entries)

        myRange = range(0,numberOfG2Entries)

        for i in myRange:
            print("entrie:",G2stringlist[i])
            print("-------------------------")
            #
            #showWiClientsRegEx = re.compile(r'Model\s(\w+)\s+\w+/\w+.*number\s+(\w+).*Uptime\s+(\d\d:\d\d:\d\d:\d\d)',re.DOTALL)

            #showWiClientsRegEx = re.compile(r'((:?[0-9a-fA-F]:?){12}).*State=(\w+)' , re.DOTALL)
            #showWiClientsRegEx = re.compile(r'(([0-9a-fA-F]{2}:{5})([0-9a-fA-F]{2}))(.*State=(\w+))' , re.DOTALL)
            #showWiClientsRegEx = re.compile(r'.*State=(\w+).*SSID=(\w+).*PSMod=(\w+).*NMode=(\w+).*Rate=(\w+\s\w+).*ON for (\w+).*TxPkt=(\w+).*TxErr=(\w+).*RxUni=(\w+).*RxMul=(\w+).*RxErr=(\w+).*RSSI=(\w+\s\w+)',re.DOTALL)
            #showWiClientsRegEx = re.compile(r'.*State=(\w+).*SSID=(\w+).*PSMod=(\w+).*NMode=(\w+).*Rate=(\w+\s\w+)',re.DOTALL)
            showWiClientsRegEx = re.compile(r'.*State=(\w+).*SSID=(\w+).*PSMod=(\w+).*NMode=(\w+).*Rate=(\w+\s\w+).*ON\sfor\s(\w+\s\w+).*TxPkt=(\w+).*TxErr=(\w+).*RxUni=(\w+).*RxMul=(\w+).*RxErr=(\w+).*RSSI=-(\w+)',re.DOTALL)

                                       #     r'.*ON for (\w+).*TxPkt=(\w+).*TxErr=(\w+).*RxUni=(\w+).*RxMul=(\w+).*RxErr=(\w+).*RSSI=(\w+\s\w+)',re.DOTALL)
            #showWiClientsRegEx = re.compile((r'.*State=(\w+).*SSID=(\w+).*PSMOD=(\w+)'),re.DOTALL|re.DOTALL)

            print (G2stringlist[i])
            G2stringlistSplit = G2stringlist[i].split()
            print ("mac is ---------------------------------------------------------", G2stringlistSplit[0])
            mac2G = G2stringlistSplit[0]

            showWiClientGroups = showWiClientsRegEx.search(G2stringlist[i])

            self.showWiClientsDict = {}

            #self.showIPLanDict[connectedDeviceName]: {}
            #self.showIPLanDict = {connectedDeviceName : {}}
            #self.showIPLanDict[connectedDeviceName] = {}

            #print("-------------->",connectedDeviceName)
            #print("-------------->", connectedDeviceName)

            #self.showIPLanDict= {"connectedDeviceName"}
            #self.showIPLanDict[connectedDeviceName]["IP"] = connectedDeviceIP
            #self.showIPLanDict[connectedDeviceName]["MAC"] = connectedDeviceMac
            #self.showIPLanDict[connectedDeviceName]["Status"] = connectedDeviceStatus
            #self.showIPLanDict[connectedDeviceName]["DHCP"] = connectedDeviceDHCP

            #print(mo1)
            print('state--------------------------------------------- ', showWiClientGroups.group(1))
            state2G = showWiClientGroups.group(1)
            print('SSID--------------------------------------------- ', showWiClientGroups.group(2))
            SSID2G = showWiClientGroups.group(2)
            print('PSMOD--------------------------------------------- ', showWiClientGroups.group(3))
            PSMOD2G = showWiClientGroups.group(3)
            print('NMMOD--------------------------------------------- ', showWiClientGroups.group(4))
            NMMOD2G = showWiClientGroups.group(4)
            print('Rate--------------------------------------------- ', showWiClientGroups.group(5))
            Rate2G= showWiClientGroups.group(5)
            print('on--------------------------------------------- ', showWiClientGroups.group(6))
            uptime2G = showWiClientGroups.group(6)
            print('txpkt--------------------------------------------- ', showWiClientGroups.group(7))
            txpkt2G= showWiClientGroups.group(7)
            print('txerr--------------------------------------------- ', showWiClientGroups.group(8))
            txerr2G= showWiClientGroups.group(8)
            print('rxuni-------------------------------------------- ', showWiClientGroups.group(9))
            rxuni2G = showWiClientGroups.group(9)
            print('rxmul--------------------------------------------- ', showWiClientGroups.group(10))
            rxmul2G= showWiClientGroups.group(10)
            print('rxerr--------------------------------------------- ', showWiClientGroups.group(11))
            rxerr2G = showWiClientGroups.group(11)
            print('rssi--------------------------------------------- ', showWiClientGroups.group(12))
            rssi2G = showWiClientGroups.group(12)

            self.showWiClientsDict[mac2G]={}
            self.showWiClientsDict[mac2G]["State"] = state2G
            self.showWiClientsDict[mac2G]["SSID"] = SSID2G
            self.showWiClientsDict[mac2G]["PSMOD"] = PSMOD2G
            self.showWiClientsDict[mac2G]["NMMOD"] = NMMOD2G
            self.showWiClientsDict[mac2G]["Rate"] = Rate2G
            self.showWiClientsDict[mac2G]["Uptime"] = uptime2G
            self.showWiClientsDict[mac2G]["txpkt"] = txpkt2G
            self.showWiClientsDict[mac2G]["txerr"] = txerr2G
            self.showWiClientsDict[mac2G]["rxuni"] = rxuni2G
            self.showWiClientsDict[mac2G]["rxmul"] = rxmul2G
            self.showWiClientsDict[mac2G]["rxerr"] = rxerr2G
            self.showWiClientsDict[mac2G]["rssi"] = rssi2G

            #print('-----------------------------------------end model')
            self.session.close()
        return self.showWiClientsDict

#-------pfp-----------------------------

    def factory_reset_rg(self):
        global nvgInfo
        #self.getdeviceInfoFromUI()
        #print("self.serialNumer:",self.serialNumber)
        # we need the serial number to refernce the DAC which is in our local dicitonary
        # The DAC must be read from the actual device., so it is stored in a dictionary of all the test house nvg599s
        #self.deviceAccessCode = self.nvgInfo[self.serialNumber]['deviceAccessCode']
        #print("dac",self.deviceAccessCode)
        #print("in accessWiFiInfo ")
        #url = 'http://192.168.1.254/cgi-bin/wconfig.ha'

        # we should be doing this
        url = 'http://192.168.1.254/'

        browser = webdriver.Chrome()
        browser.get(url)

        dianostics_link = browser.find_element_by_link_text("Diagnostics")
        dianostics_link.click()
        sleep(2)

        resets_link = browser.find_element_by_link_text("Resets")
        resets_link.click()
        sleep(2)

        #device_access_link = browser.find_element_by_id("password")
        #device_access_link.send_keys(self.devAccessCode)
        #submit = browser.find_element_by_name("Continue")
        #submit.click()
        print('I01')
        factory_reset = browser.find_element_by_name("Reset")
        factory_reset.click()
        sleep(5)
        print('I1')
        factory_reset = browser.find_element_by_name("Reset")
        factory_reset.click()
        sleep(12)

        print('I am in factory reset ')

        #result = os.system(cmd)
        #print('result:', result)
        start = time.time()
        print("starting timer")

        cmd = 'ping -c1 192.168.1.254'
        result = os.system(cmd)
        while result == 0:
            print("waiting 10 for RG to reboot")
            sleep(10)
            result = os.system(cmd)

        while  (result == 0):
                print("waiting 10 for RG to come back into service")
                sleep(10)
                result = os.system(cmd)

        end = time.time()
        print("duration in seconds:", end - start)

        sleep(2)



    def enter_dac_convenience(self,sesion):
        pass

    def accessUIWiFiInfo(self):
        global nvgInfo
        #self.getdeviceInfoFromUI()
        print("self.serialNumer:",self.serialNumber)
        # we need the serial number to refernce the DAC which is in our local dicitonary
        # The DAC must be read from the actual device., so it is stored in a dictionary of all the test house nvg599s
        self.deviceAccessCode = self.nvgInfo[self.serialNumber]['deviceAccessCode']
        print("dac",self.deviceAccessCode)
        print("in accessWiFiInfo ")
        #url = 'http://192.168.1.254/cgi-bin/wconfig.ha'

        # we should be doing this
        url = 'http://192.168.1.254/'

        browser = webdriver.Chrome()
        browser.get(url)

        status_link = browser.find_element_by_link_text("Home Network")
        status_link.click()
        sleep(2)

        #status_link = browser.find_element_by_link_text("Status")
        #status_link.click()
        #sleep(2)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        tables = soup.findChildren('table')
#five tables on this page
        table = tables[4]
        #table = soup.find("table100", {"class": "table100"})
        print ("table is",table)
        table_rows = table.find_all('tr')
        for tr in table_rows:
            td = tr.find_all('td')
            row = [i.text for i in td]

            print("length is:",len(row))
            print("type",type(row))
            exit()
            print("----------------------------")
            if len(row !=0 and row[0]=="Current Radio Channel"):
                #print("2G channel:",row[1],"5G channel:,row[2]")
                print("2G channel:]")

                sleep(2)
                browser.quit()
                exit()


        sleep(20)
        browser.quit()
        exit()
        homeNetworkLink = browser.find_element_by_link_text("Home Network")
        homeNetworkLink.click()
        sleep(2)
        homeNetworkLink = browser.find_element_by_link_text("Wi-Fi")
        homeNetworkLink.click()
        sleep(2)
        #exit()
        #soup = BeautifulSoup(browser.page_source, 'html.parser')
        #print(" ------------access code ----------------")
        #print(soup.find(id="password"))
        #print(" ------------access code ----------------")
        deviceAccessCode = browser.find_element_by_id("password")
        deviceAccessCode.send_keys(self.devAccessCode)
        submit = browser.find_element_by_name("Continue")
        submit.click()
        advancedOptionsLink = browser.find_element_by_link_text("Advanced Options")
        sleep(2)
        advancedOptionsLink.click()
        sleep(20)
        browser.quit()


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

                self.DAC= nvgInfo[self.serialNumber]['deviceAccessCode']
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

        sleep(2)

        browser.quit()

# 2.4 bw possibilities 20,40
# 5 bw possibilities 20,40,80
# InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.BSSID fc:51:a4:2f:25:94
# InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.AutoChannelEnable 0
# InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.X_0000C5_BandLock X_0000   C5_5.0GHz


#tr69 GetParameterValues  InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.X_0000C5_Bandwidth
#tr69 SetParameterValues  InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.X_0000C5_Bandwidth=X_0000C5_80MHz
# tr69 SetParameterValues  InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.X_0000C5_Bandwidth=X_0000C5_40MHz
# InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.X_0000C5_Bandwidth X_0000C5_80MH

    def channelTest(self,b2G,b5G,bw2G,bw5G):
        for ib2G in b2G:
            for ib5G in b5G:
                for ibw in b2G:
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
                print("Name    ",th.text)
                print("Name1",th.next_sibling.text)
            else:
                print("no derp")

        sleep(5)

        browser.quit()


    def getSNFromUI(self):
        self.webDriver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
        # driver.get('http://www.google.com')
        self.webDriver.get('http://192.168.1.254')
        self.webDriver.implicitly_wait(20)
        # driver.find_elements_by_tag_name("Settings") // this is for 599


    def connect_to_console(self):
        print('I am in console')
        cmd='ping -c1 192.168.1.254'
        result = os.system(cmd)
        print ('result:',result)
        start = time.time()
        print("hello")
        end = time.time()
        print(end - start)

        if (result != 0):
            print("waiting 10 seconds")
            sleep(10)
        exit()

    def loginNVG599(self):
        print('I am in 599 login')
        self.session = pexpect.spawn("telnet 192.168.1.254", encoding='utf-8')
        self.session.expect("ogin:")
        self.session.sendline('admin')
        self.session.expect("ord:")
        self.session.sendline('<<01%//4&/')
        self.session.expect(">")
        return self.session

    def login_4920(self,IP4920):
        print('I am in 4920 login')
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
        print('i am in connect cli')
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

    def printme(self):
        print('I am an NVG599 object')

    def getRGSerialNumber(self):
        self.loginNVG599()
        self.session.sendline('status')
        self.session.expect('>')
        statusOutput = self.session.before
        print('Getting getSerialnumber')
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

    def getRGShIPLanInfo(self):
        session=self.loginNVG599()
        session.sendline("show ip lan")
        self.session.expect('>')
        ipLanOutput = self.session.before
        ipLanOutput = ipLanOutput.split('\n\r')
        print("-------------------------------------")
        count = len(ipLanOutput)

        # discard first two lines of the output
        print("count",count)
        ipLanOutput = ipLanOutput[2:-1]
        # I think the length minus 1 is what we want // need to check this
        for i  in range(len(ipLanOutput)):
            #print("input line:", ipLanOutput[i])
            #mo1 = statusInfoRegEx.match(ipLanOutput[i])
            ipLanOutputSplit = (ipLanOutput[i]).split()
            #print ("connectedDeviceName",ipLanOutputSplit[0])
            #self.connectedDeviceName = ipLanOutputSplit[0]
            connectedDeviceName = ipLanOutputSplit[0]

            #if "ATT_4920" in ipLanOutputSplit[0]:
            #    print("this is an airties device!")
            print ("connectedDeviceIP",ipLanOutputSplit[1])
            connectedDeviceIP = ipLanOutputSplit[1]

            print ("connectedDeviceMac",ipLanOutputSplit[2])
            connectedDeviceMac = ipLanOutputSplit[2]
            print ("connectedDeviceStatus",ipLanOutputSplit[3])
            connectedDeviceStatus = ipLanOutputSplit[3]
            print ("connectedDeviceDHCP",ipLanOutputSplit[4])
            connectedDeviceDHCP = ipLanOutputSplit[4]
            print ("connectedDeviceSSIDNumber",ipLanOutputSplit[5])
            connectedDeviceSSIDNumber = ipLanOutputSplit[5]
            #-----------------change to use mac as key instead of device name-------------------pfp
            #self.showIPLanDict[connectedDeviceName] = {}
            self.showIPLanDict[connectedDeviceMac] = {}
            #-----------------end change here-------------------pfp

            self.showIPLanDict[connectedDeviceMac]["IP"] = connectedDeviceIP
            self.showIPLanDict[connectedDeviceMac]["Name"] = connectedDeviceName
            self.showIPLanDict[connectedDeviceMac]["Status"] = connectedDeviceStatus
            self.showIPLanDict[connectedDeviceMac]["DHCP"] = connectedDeviceDHCP
            self.showIPLanDict[connectedDeviceMac]["SSIDNumber"] = connectedDeviceSSIDNumber
            self.session.close()
        return self.showIPLanDict


    def login(self):
        pass

class Nvg5268Class(GatewayClass):
    def __init__(self):
        self.name="abc"
        rg5268 = pexpect.spawn("telnet 192.168.1.254")
        sleep(1)


class airTies4920():
    pass

