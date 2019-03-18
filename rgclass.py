from itertools import count
from typing import Dict

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

#nvg_info = { "228946241148656" : {'model':'nvg599','deviceAccessCode':"*<#/53#1/2", 'magic': 'kjundhkdxlxr','mac2g': 'd0:39:b3:60:56:f1','mac5g':'d0:39:b3:60:56:f4', 'wiFi': 'c2cmybt25dey','ssid': 'ATTqbrAnYs'},
#"277427577103760" : {'model':'nvg599','deviceAccessCode': '<<01%//4&/','magic': "ggtxstgwipcg", 'mac2g': 'fc:51:a4:2f:25:90', 'mac5g': 'fc:51:a4:2f:25:94', 'wiFi': 'nsrmpr59rxwv', 'ssid' : 'ATTqbrAnYs'}}

nvg_info: Dict[str, Dict[str, str]] = {"228946241148656": {'model': 'nvg599', 'device_access_code': "*<#/53#1/2", 'magic': 'kjundhkdxlxr',
                                     'mac2g': 'd0:39:b3:60:56:f1', 'mac5g': 'd0:39:b3:60:56:f4',
                                     'wiFi': 'c2cmybt25dey', 'ssid': 'ATTqbrAnYs'},
            "277427577103760": {'model': 'nvg599', 'device_access_code': '<<01%//4&/', 'magic': 'ggtxstgwipcg',
                                     'mac2g': 'fc:51:a4:2f:25:90', 'mac5g': 'fc:51:a4:2f:25:94',
                                     'wiFi': 'nsrmpr59rxwv', 'ssid': 'ATTqbrAnYs'}}


test_dict:{'e':{'e1':'1','e1':'2','e1':'e3'},'f':{'f1':'1','f1':'2','f1':'3'}}

NON_DFS_CHANNELS = {36,40,44,48,149,153,157,161,165}
DFS_CHANNELS     = {52,56,60,64,100,104,108,112,116,132,136,140,144}

#class GatewayClass():


class GatewayClass:

    def __init__(self):
        self.magic = None
        self.up_time = None
        self.ip = None
        self.serial_number = None

    def email_test_results(self, text_file):
        gmail_password="arris123"
        gmail_user= 'leandertesthouse@gmail.com'
        to = 'pfpalmer@gmail.com'
        sent_from = 'leandertesthouse:'
        subject = 'Test results'
#      body = "Results:" + channelResultContents
        body = "Results:" + text_file
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
        super(self.__class__, self).__init__()
        #rg599 = pexpect.spawn("telnet 192.168.1.254")
        #sleep(1)
        self.IP ="192.168.1.254"
        self.device_access_code = None
        #self.test = 41
        self.init_info = False
        global nvg_info

        self.ui_system_information()
# serial number set by prior call to ui_system_info
        print("self.serialNumer:",self.serial_number)

#       self.nvg_info = {"228946241148656": {'model': 'nvg599', 'device_access_code': "*<#/53#1/2", 'magic': 'kjundhkdxlxr',
#                                       'mac2g': 'd0:39:b3:60:56:f1', 'mac5g': 'd0:39:b3:60:56:f4',
#                                       'wiFi': 'c2cmybt25dey', 'ssid': 'ATTqbrAnYs'},
#                   "277427577103760": {'model': 'nvg599', 'device_access_code': "<<01%//4&/", 'magic': 'ggtxstgwipcg',
#                                       'mac2g': 'fc:51:a4:2f:25:90', 'mac5g': 'fc:51:a4:2f:25:94',
#                                       'wiFi': 'nsrmpr59rxwv', 'ssid': 'ATTqbrAnYs'}}

        # The DAC must be read from the actual device., so it is stored in a dictionary of all the test house nvg599s

        self.device_access_code = nvg_info[self.serial_number]['device_access_code']
        print("dac",self.device_access_code)
        print("in NVG599 init")
        self.init_info= True
        #exit()
        # show IP Lan  dicitonary dicitionary
        #self.showIPLanDict = {}
        # show wi client dicitionary
        #self.showWiClientsDict = {}
        #airtiesIPList=[]
        #rgClientList=[]
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
        g2_string_list = re.findall(G2RegEx,G2string)

        number_of_g2_entries = len(g2_string_list)

        print("--------------------------------------the 2g list has :",number_of_g2_entries)

        my_range = range(0,number_of_g2_entries)

        for i in my_range:
            print("entrie:", g2_string_list[i])
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

            print(g2_string_list[i])
            g2_string_list_split = g2_string_list[i].split()
            print("mac is ---------------------------------------------------------", g2_string_list_split[0])
            mac_2g = g2_string_list_split[0]

            showWiClientGroups = showWiClientsRegEx.search(g2_string_list[i])

            self.showWiClientsDict = {}

# #           #self.showIPLanDict[connectedDeviceName]: {}
# #           #self.showIPLanDict = {connectedDeviceName : {}}
# #           #self.showIPLanDict[connectedDeviceName] = {}
#
#            #print("-------------->",connectedDeviceName)
#            #print("-------------->", connectedDeviceName)

#            #self.showIPLanDict= {"connectedDeviceName"}
#            #self.showIPLanDict[connectedDeviceName]["IP"] = connectedDeviceIP
#            #self.showIPLanDict[connectedDeviceName]["MAC"] = connectedDeviceMac
#            #self.showIPLanDict[connectedDeviceName]["Status"] = connectedDeviceStatus
#            #self.showIPLanDict[connectedDeviceName]["DHCP"] = connectedDeviceDHCP

#            #print(mo1)
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

            self.showWiClientsDict[mac_2g]={}
            self.showWiClientsDict[mac_2g]["State"] = state2G
            self.showWiClientsDict[mac_2g]["SSID"] = SSID2G
            self.showWiClientsDict[mac_2g]["PSMOD"] = PSMOD2G
            self.showWiClientsDict[mac_2g]["NMMOD"] = NMMOD2G
            self.showWiClientsDict[mac_2g]["Rate"] = Rate2G
            self.showWiClientsDict[mac_2g]["Uptime"] = uptime2G
            self.showWiClientsDict[mac_2g]["txpkt"] = txpkt2G
            self.showWiClientsDict[mac_2g]["txerr"] = txerr2G
            self.showWiClientsDict[mac_2g]["rxuni"] = rxuni2G
            self.showWiClientsDict[mac_2g]["rxmul"] = rxmul2G
            self.showWiClientsDict[mac_2g]["rxerr"] = rxerr2G
            self.showWiClientsDict[mac_2g]["rssi"] = rssi2G

            #print('-----------------------------------------end model')
            self.session.close()
        return self.showWiClientsDict

#-------pfp----------------------------- this request further testing




    def factory_reset_rg(self):
        global nvg_info
        #self.getdeviceInfoFromUI()
        #print("self.serialNumer:",self.serialNumber)
        # we need the serial number to refernce the DAC which is in our local dicitonary
        # The DAC must be read from the actual device., so it is stored in a dictionary of all the test house nvg599s
        #self.device_access_code = self.nvgInfo[self.serialNumber]['device_ccess_code']
        #print("dac",self.device_access_code)
        #print("in accessWiFiInfo ")
        #url = 'http://192.168.1.254/cgi-bin/wconfig.ha'

        # we should be doing this
        url = 'http://192.168.1.254/'

        browser = webdriver.Chrome()
        browser.get(url)
#//*[@id="main-content"]/div[2]/div[2]/div/h1[text()='Access Code Required'
        #was this
        #browser.find_element_by_xpath("//*[@id='main-content']/div[2]/div[2]/div/h1")
        browser.find_element_by_xpath("//*[@id='main-content']/div[2]/div[2]/div/h1.text")


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

    def ui_get_home_network_information(self,value_requested):
        global nvgInfo
        ui_channel_5g = None
        ui_channel_2g = None
        self.ui_system_information()
        print("self.serialNumer:", self.serial_number)
        # we need the serial number to refernce the DAC which is in our local dicitonary
        # The DAC must be read from the actual device., so it is stored in a dictionary of all the test house nvg599s
        self.device_access_code = nvg_info[self.serial_number]['device_access_code']
        print("dac",self.device_access_code)
        print("in ui_get_home_network_information ")
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
        #print ("table is",table)
        table_rows = table.find_all('tr')
        for tr in table_rows:
            td = tr.find_all('td')
            row = [i.text for i in td]

            print("length is:",len(row))
            print("type",type(row))
            print("row text",row)
            print("----------------------------")
            #continue
            if (len(row)==0):
                continue

            if (row[0] == "Bandwidth"):
                # print("Bandwidth:",row[1],"5G channel:,row[2]")
                print("2G Bandwidth:", row[1])
                ui_bandwidth_2g = row[1]
                print("5G bandwidth:", row[2])
                ui_bandwidth_5g = row[2]

            if (row[0]=="Current Radio Channel"):
                #print("2G channel:",row[1],"5G channel:,row[2]")
                print("2G channel:",row[1])
                ui_channel_2g = row[1]
                print("25 channel:",row[2])
                ui_channel_5g = row[2]

                sleep(2)
             #   browser.quit()
             #   exit()
                if value_requested == "ui_channel_5g":
                    browser.quit()
                    return ui_channel_5g,ui_bandwidth_2g

                if value_requested == "ui_channel_2g":
                    browser.quit()
                    return ui_channel_2g,ui_bandwidth_5g


        sleep(2)
        browser.quit()
#        homeNetworkLink = browser.find_element_by_link_text("Home Network")
#        homeNetworkLink.click()
#        sleep(2)
#        homeNetworkLink = browser.find_element_by_link_text("Wi-Fi")
#        homeNetworkLink.click()
#        sleep(2)
        #exit()
        #soup = BeautifulSoup(browser.page_source, 'html.parser')
        #print(" ------------access code ----------------")
        #print(soup.find(id="password"))
        #print(" ------------access code ----------------")
        device_access_code = browser.find_element_by_id("password")
        device_access_code.send_keys(self.device_access_code)
        submit = browser.find_element_by_name("Continue")
        submit.click()
        advancedOptionsLink = browser.find_element_by_link_text("Advanced Options")
        sleep(2)
        advancedOptionsLink.click()
        sleep(20)
        browser.quit()

    def ui_set_bw_channel(self, value_requested):
        global nvgInfo
        ui_channel_5g = None
        ui_channel_2g = None
        self.ui_system_information()
        print("self.serialNumer:", self.serial_number)
        # we need the serial number to refernce the DAC which is in our local dicitonary
        # The DAC must be read from the actual device., so it is stored in a dictionary of all the test house nvg599s
        self.device_access_code = nvg_info[self.serial_number]['device_access_code']
        print("dac", self.device_access_code)
        print("in ui_get_home_network_information ")
        # url = 'http://192.168.1.254/cgi-bin/wconfig.ha'

        # we should be doing this
        url = 'http://192.168.1.254/'

        browser = webdriver.Chrome()

    def ui_system_information(self):
        global nvg_info
        url = 'http://192.168.1.254/cgi-bin/sysinfo.ha'
        print("derp----------cccc----------------------------------")
        test_dict = {'e': {'e1': '1', 'e2': '2', 'e3': 'e3'}, 'f': {'f1': '1', 'f2': '2', 'f3': '3'}}
        print("test_dict",test_dict['e']['e1'])
#       exit()
        browser = webdriver.Chrome()
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        sleep(5)
        this = soup.find_all('th')
        for th in this:
            if th.text == "Model Number":
                print("model:",th.next_sibling.next_sibling.text)
                self.modelNumber = th.next_sibling.next_sibling.text
            if th.text == "Serial Number":
                print("serial number:",th.next_sibling.next_sibling.text)
                self.serial_number = th.next_sibling.next_sibling.text

                print ("serial Number is:",self.serial_number)
                print('test is:', self.test)
                print ("nvg serial number dict",nvg_info[self.serial_number])
                print("nvg access code", nvg_info[self.serial_number]['device_access_code'])
                tmp_dac = nvg_info[self.serial_number]['device_access_code']
                print('tmp_dac:',tmp_dac)
                self.device_access_code = tmp_dac

                #tmp_serial_number = nvg_info[self.serial_number]
                #self.device_access_code = nvg_info[self.serial_number][self.device_access_code]
                #mp_device_access_code = nvg_info[tmp_serial_number]['device_access_code']

                print("dac is:",self.device_access_code)


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


    def setup_tr69_url(self):

        self.session = self.loginNVG599()
        self.session.sendline('magic')
        self.session.expect("UNLOCKED>")
        self.session.sendline('conf')
        self.session.expect("top\)>>")
        self.session.sendline('manage cwmp')
        self.session.expect(")>>")
        self.session.sendline('set')
        self.session.expect("enable.*]:")
        self.session.sendline('on')
        self.session.expect("):")
        self.session.sendline('http://arris1.arriseco.com')
        self.session.expect("acs-username.*):")
        self.session.sendline()
        self.session.expect("acs-password.*):")
        self.session.sendline()
        self.session.expect("cr-url.*):")
        self.session.sendline()
        self.session.expect("cr-port.*]:")
        self.session.sendline()
        self.session.expect("cr-ip.*:")
        self.session.sendline()
        self.session.expect("prov-code.*):")
        self.session.sendline()
        self.session.expect("qos-tos.*):")
        self.session.sendline()
        self.session.expect("qos-p.*):")
        self.session.sendline()
        self.session.expect("qos-marker.*):")
        self.session.sendline()
        self.session.expect("prefer.*):")
        self.session.sendline()
        self.session.expect("tr69.*]:")
        self.session.sendline()
        self.session.expect("log-spv.*]:")
        print('hello from turn on tr069')
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

