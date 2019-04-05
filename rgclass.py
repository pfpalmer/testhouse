from itertools import count
from typing import Dict
import subprocess
from subprocess import check_output

from selenium.webdriver.common.by import By

from selenium.common.exceptions import NoSuchElementException


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
from email.message import EmailMessage
from datetime import datetime


#  Apple path for wifi info
# /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I

nvg_info: Dict[str, Dict[str, str]] = {"228946241148656": {'model': 'nvg599', 'device_access_code': "*<#/53#1/2", 'magic': 'kjundhkdxlxr',
                                     'mac2g': 'd0:39:b3:60:56:f1', 'mac5g': 'd0:39:b3:60:56:f4',
                                     'wiFi': 'c2cmybt25dey', 'ssid': 'ATTqbrAnYs'},
            "277427577103760": {'model': 'nvg599', 'device_access_code': '<<01%//4&/', 'magic': 'ggtxstgwipcg',
                                     'mac2g': 'fc:51:a4:2f:25:90', 'mac5g': 'fc:51:a4:2f:25:94',
                                     'wiFi': 'nsrmpr59rxwv', 'ssid': 'ATTqbrAnYs'}}


NON_DFS_CHANNELS = {36, 40, 44, 48, 149, 153, 157, 161, 165}
DFS_CHANNELS     = {52, 56, 60, 64, 100, 104, 108, 112, 116, 132, 136, 140, 144}


class GatewayClass:
    def __init__(self):
        self.magic = None
        self.up_time = None
        self.ip = None
        self.serial_number = None

    def email_test_results(self, text_file):

        now = datetime.today().isoformat()
        print('now')
        subject_title = 'Test results:' + str(now)
        print('subject title', subject_title)

        with open("results_file.txt") as fp:
            # Create a text/plain message
            msg = EmailMessage()
            msg.set_content(fp.read())

        print('in email_test_results1')
        # me == the sender's email address
        # you == the recipient's email address
        msg['Subject'] = 'Test results'
        # msg['Subject'] = subject_title

        msg['From'] = 'leandertesthouse@gmail.com'
        msg['To'] = 'pfpalmer@gmail.com'
        gmail_password = "1329brome"
        gmail_user = 'leandertesthouse@gmail.com'

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp_server:
            smtp_server.ehlo()
            smtp_server.starttls()
            smtp_server.login(gmail_user, gmail_password)
            smtp_server.send_message(msg)

        print('message sent successfully')

# this version has no subject when received
    def email_test_results_deprecated(self, text_file):
        print('in email_test_results')
#        gmail_password="arris123"
        gmail_password = "1329brome"

        gmail_user = 'leandertesthouse@gmail.com'
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
            # email_text = 'Subject:{}\n\nbody'.format(subject)
            server.sendmail(sent_from, to, email_text)
            sleep(2)
            server.quit()
            print("im the email section ====================")
        except:
            print('failed to send email')


class Nvg599Class(GatewayClass):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.ip = "192.168.1.254"
        self.device_access_code = None
        self.model_number = None
        self.session = None
        self.init_info = False
        self.telnet_cli_session = None
        global nvg_info
        # The DAC must be read from the actual device., so it is stored in a dictionary of all the test house nvg599s
        self.get_ui_system_information()
        self.device_access_code = nvg_info[self.serial_number]['device_access_code']
        print("in Nvg599Class__init")
        self.init_info = True
        # self.webDriver.find_element_by_link_text("Settings").click()

    def ui_get_device_list(self):
        global nvg_info
        print("in ui_get_device_list ")
        home_link = self.session.find_element_by_link_text("Device")
        home_link.click()
        status_link = self.session.find_element_by_link_text("Device List")
        status_link.click()
        soup = BeautifulSoup(self.session.page_source, 'html.parser')
        table = soup.find("table", {"class": "table100"})

        for table_row in table.find_all("tr"):
            try:
                # header_text = table_row.th.text
                # print("table_row header:" +  table_row.th.text + " table_td_text:" + table_row.td.text, end='')
                print("table_row header:",end ='')
                print(table_row.th.text,end= '')
                print(" table_td_text:",end= '')
                print(table_row.td.text,end='')
            # except NoSuchElementException:
            except AttributeError:
                print('--------------------------------\n')
                continue
        exit()
        for table_rows in table.find_all("tr"):
            for row_header in table_rows:
                td = row_header.find_all('td')
                print("Name    ", td.text)

        exit()

        soup = BeautifulSoup(self.session.page_source, 'html.parser')
        tables = soup.findChildren('table')
        # five tables on this page
        table = tables[4]
        # table = soup.find("table100", {"class": "table100"})
        # print ("table is",table)
        table_rows = table.find_all('tr')
        for tr in table_rows:
            td = tr.find_all('td')
            tc = td.find_all('class')
            if tc.text == "reshr":
                continue
            row = [i.text for i in td]
            # print("length is:",len(row))
            # print("type",type(row))
            print("row text", row)
            # for th in this:
            #   if th.text == "Model Number":
            #      print("model:", th.next_sibling.next_sibling.text)
            #       self.modelNumber = th.next_sibling.next_sibling.text
            #   if th.text == "Serial Number":
            #       self.serial_number = th.next_sibling.next_sibling.text
            #      print("serial Number is:", self.serial_number)
            #      # print ("nvg serial number dict",nvg_info[self.serial_number])
            #       # print("nvg access code", nvg_info[self.serial_number]['device_access_code'])
            #       # tmp_dac = nvg_info[self.serial_number]['device_access_code']
            #        # self.device_access_code = tmp_dac
            #       self.device_access_code = nvg_info[self.serial_number]['device_access_code']
            #       print("dac is:", self.device_access_code)
            #   if th.text == "Software Version":
            #      print(th.next_sibling.next_sibling.text)
            #        self.software_version = th.next_sibling.next_sibling.text
            # handle being asked for password
            # self.session = self.check_if_password_required()
            # we might need this
            # self.check_if_password_required()

    def check_if_password_required(self):
        try:
            # Select(browser.find_element_by_id("selectMonth")).select_by_visible_text("%s" % (month))
            sleep(5)
            dac_access_challenge = self.session.find_element_by_link_text("Forgot your Access Code?")
            print('we found the request for password screen')
            print('sending dac', self.device_access_code)
            dac_entry = self.session.find_element_by_id("password")
            dac_entry.send_keys(self.device_access_code)
            submit = self.session.find_element_by_name("Continue")
            submit.click()
            sleep(5)
        except NoSuchElementException:
            print('we are not seeing the password screen')
            pass

    def get_sh_wi_clients_cli(self):
        session = self.login_nvg_599_cli()
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
        g2_string = mo1.group(1)
        # G2RegEx = re.compile(r'([0-9a-fA-F]:?){12}', re.DOTALL)
        g2_reg_ex = re.compile(r'(?:[0-9a-fA-F]:?){12}.*?\n.*\n.*\n.*\n')
        # G2RegEx = re.compile(r'(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w.*?)*', re.DOTALL)
        # mo1 = G2RegEx.findall(G2string)
        g2_string_list = re.findall(g2_reg_ex, g2_string)

        number_of_g2_entries = len(g2_string_list)
        print("--------------------------------------the 2g list has :",number_of_g2_entries)
        my_range = range(0,number_of_g2_entries)

        for i in my_range:
            print("entrie:", g2_string_list[i])
            print("-------------------------")
#
# showWiClientsRegEx = re.compile(r'Model\s(\w+)\s+\w+/\w+.*number\s+(\w+).*Uptime\s+(\d\d:\d\d:\d\d:\d\d)',re.DOTALL)
# showWiClientsRegEx = re.compile(r'((:?[0-9a-fA-F]:?){12}).*State=(\w+)' , re.DOTALL)
# showWiClientsRegEx = re.compile(r'(([0-9a-fA-F]{2}:{5})([0-9a-fA-F]{2}))(.*State=(\w+))' , re.DOTALL)
# showWiClientsRegEx = re.compile(r'.*State=(\w+).*SSID=(\w+).*PSMod=(\w+).*NMode=(\w+).*Rate=(\w+\s\w+).*ON for (\w+).*TxPkt=(\w+).*TxErr=(\w+).*RxUni=(\w+).*RxMul=(\w+).*RxErr=(\w+).*RSSI=(\w+\s\w+)',re.DOTALL)
# showWiClientsRegEx = re.compile(r'.*State=(\w+).*SSID=(\w+).*PSMod=(\w+).*NMode=(\w+).*Rate=(\w+\s\w+)',re.DOTALL)
            showWiClientsRegEx = re.compile(r'.*State=(\w+).*SSID=(\w+).*PSMod=(\w+).*NMode=(\w+).*Rate=(\w+\s\w+).*ON\sfor\s(\w+\s\w+).*TxPkt=(\w+).*TxErr=(\w+).*RxUni=(\w+).*RxMul=(\w+).*RxErr=(\w+).*RSSI=-(\w+)',re.DOTALL)
#     r'.*ON for (\w+).*TxPkt=(\w+).*TxErr=(\w+).*RxUni=(\w+).*RxMul=(\w+).*RxErr=(\w+).*RSSI=(\w+\s\w+)',re.DOTALL)
# showWiClientsRegEx = re.compile((r'.*State=(\w+).*SSID=(\w+).*PSMOD=(\w+)'),re.DOTALL|re.DOTALL)

            print(g2_string_list[i])
            g2_string_list_split = g2_string_list[i].split()
            print("mac is ---------------------------------------------------------", g2_string_list_split[0])
            mac_2g = g2_string_list_split[0]

            show_wi_client_groups = showWiClientsRegEx.search(g2_string_list[i])

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
            print('state--------------------------------------------- ', show_wi_client_groups.group(1))
            state_2g = show_wi_client_groups.group(1)
            print('SSID--------------------------------------------- ', show_wi_client_groups.group(2))
            ssid_2g = show_wi_client_groups.group(2)
            print('PSMOD--------------------------------------------- ', show_wi_client_groups.group(3))
            psmod_2g = show_wi_client_groups.group(3)
            print('NMMOD--------------------------------------------- ', show_wi_client_groups.group(4))
            nmmod_2g = show_wi_client_groups.group(4)
            print('Rate--------------------------------------------- ', show_wi_client_groups.group(5))
            rate_2g = show_wi_client_groups.group(5)
            print('on--------------------------------------------- ', show_wi_client_groups.group(6))
            uptime_2g = show_wi_client_groups.group(6)
            print('txpkt--------------------------------------------- ', show_wi_client_groups.group(7))
            txpkt_2g = show_wi_client_groups.group(7)
            print('txerr--------------------------------------------- ', show_wi_client_groups.group(8))
            txerr_2g = show_wi_client_groups.group(8)
            print('rxuni-------------------------------------------- ', show_wi_client_groups.group(9))
            rxuni_2g = show_wi_client_groups.group(9)
            print('rxmul--------------------------------------------- ', show_wi_client_groups.group(10))
            rxmul_2g = show_wi_client_groups.group(10)
            print('rxerr--------------------------------------------- ', show_wi_client_groups.group(11))
            rxerr_2g = show_wi_client_groups.group(11)
            print('rssi--------------------------------------------- ', show_wi_client_groups.group(12))
            rssi_2g = show_wi_client_groups.group(12)

            self.showWiClientsDict[mac_2g] = {}
            self.showWiClientsDict[mac_2g]["State"] = state_2g
            self.showWiClientsDict[mac_2g]["SSID"] = ssid_2g
            self.showWiClientsDict[mac_2g]["PSMOD"] = psmod_2g
            self.showWiClientsDict[mac_2g]["NMMOD"] = nmmod_2g
            self.showWiClientsDict[mac_2g]["Rate"] = rate_2g
            self.showWiClientsDict[mac_2g]["Uptime"] = uptime_2g
            self.showWiClientsDict[mac_2g]["txpkt"] = txpkt_2g
            self.showWiClientsDict[mac_2g]["txerr"] = txerr_2g
            self.showWiClientsDict[mac_2g]["rxuni"] = rxuni_2g
            self.showWiClientsDict[mac_2g]["rxmul"] = rxmul_2g
            self.showWiClientsDict[mac_2g]["rxerr"] = rxerr_2g
            self.showWiClientsDict[mac_2g]["rssi"] = rssi_2g

            self.session.close()
        return self.showWiClientsDict

    def factory_reset_rg(self):
        global nvg_info
        url = 'http://192.168.1.254/'
        browser = webdriver.Chrome()
        browser.get(url)
        browser.find_element_by_xpath("//*[@id='main-content']/div[2]/div[2]/div/h1.text")
        dianostics_link = browser.find_element_by_link_text("Diagnostics")
        dianostics_link.click()
        sleep(2)
        resets_link = browser.find_element_by_link_text("Resets")
        resets_link.click()
        sleep(2)

        print('Resetting to factory defaults now')
        factory_reset = browser.find_element_by_name("Reset")
        factory_reset.click()
        sleep(5)
        print('in factory_reset_rg')
        start = time.time()
        print("starting timer")

        cmd = 'ping -c1 192.168.1.254'
        result = os.system(cmd)
        while result == 0:
            print("waiting 10 for RG to reboot")
            sleep(10)
            result = os.system(cmd)
        end = time.time()
        print("duration in seconds:", end - start)
        sleep(2)

    def get_ui_home_network_status_value(self, value_requested):
        print('in get_ui_home_network_status_value)')
        global nvg_info
        # ui_channel_5g = None
        # ui_channel_2g = None
        # self.ui_system_information()
        print("self.serialNumer:", self.serial_number)
        # we need the serial number to refernce the DAC which is in our local dicitonary
        # The DAC must be read from the actual device., so it is stored in a dictionary of all the test house nvg599s
        self.device_access_code = nvg_info[self.serial_number]['device_access_code']
        print("dac", self.device_access_code)
        # url = 'http://192.168.1.254/cgi-bin/wconfig.ha'
        # url = 'http://192.168.1.254/'
        # session = webdriver.Chrome()
        # session.get(url)

        status_link = self.session.find_element_by_link_text("Home Network")
        status_link.click()
        sleep(2)
        # self.session = session
        # status_link = browser.find_element_by_link_text("Status")
        # status_link.click()
        # sleep(2)
        soup = BeautifulSoup(self.session.page_source, 'html.parser')
        tables = soup.findChildren('table')
# five tables on this page
        table = tables[4]
        # table = soup.find("table100", {"class": "table100"})
        # print ("table is",table)
        table_rows = table.find_all('tr')
        for tr in table_rows:
            td = tr.find_all('td')
            row = [i.text for i in td]

            # print("length is:",len(row))
            # print("type",type(row))
            print("row text", row)

            if len(row) == 0:
                continue

            if row[0] == "Bandwidth":
                # print("Bandwidth:",row[1],"5G channel:,row[2]")
                if value_requested == 'ui_bandwidth_2g':
                    print("2G Bandwidth:", row[1])
                    ui_bandwidth_2g = row[1]
                    return ui_bandwidth_2g

                # print("5G bandwidth:", row[2])
                # ui_bandwidth_5g = row[2]
                if value_requested == 'ui_bandwidth_5g':
                    print("5G Bandwidth:", row[2])
                    ui_bandwidth_5g = row[2]
                    return ui_bandwidth_5g

            if row[0] == "Current Radio Channel":
                # print("2G channel:",row[1],"5G channel:,row[2]")
                # print("2G channel:",row[1])
                # ui_channel_2g = row[1]
                # print("Ban dwidth:",row[1],"5G channel:,row[2]")
                print("2G -dbg channel:", row[1])
                if value_requested == 'ui_channel_2g':
                    print("2G Channel:", row[1])
                    ui_channel_2g = row[1]
                    return ui_channel_2g

                print("5G -dbg channel:", row[2])
#                # ui_channel_5g = row[2]
                if value_requested == 'ui_channel_5g':
                    print("5G Channel:", row[2])
                    ui_channel_5g = row[2]
                    return ui_channel_5g

#        sleep(2)
#       session.quit()
#        homeNetworkLink = browser.find_element_by_link_text("Home Network")
#        homeNetworkLink.click()
#        sleep(2)
#        homeNetworkLink = browser.find_element_by_link_text("Wi-Fi")
#        homeNetworkLink.click()
#        sleep(2)
        # exit()
        # soup = BeautifulSoup(browser.page_source, 'html.parser')
        # print(" ------------access code ----------------")
        # print(soup.find(id="password"))
        # print(" ------------access code ----------------")
#        device_access_code = browser.find_element_by_id("password")
#       device_access_code.send_keys(self.device_access_code)
#        submit = browser.find_element_by_name("Continue")
#        submit.click()
#        advancedOptionsLink = browser.find_element_by_link_text("Advanced Options")
#        sleep(2)
#       advancedOptionsLink.click()
#       sleep(20)
#       browser.quit()
# we need the band (2g or 5g) because both bands could be automatic which would be ambiguous
#nvg_599_dut.ui_set_bw_channel('g2', 40, 2)


    def ui_set_band_bandwith_channel(self,band,bandwidth,channel):
        global nvg_info

        # band_selected = band
        # channel_selected = channel
        # bandwidth_selected = bandwidth
        # if (not self.init_info):
        #   self.ui_system_information()
        #   print("self.serialNumer:", self.serial_number)
        # we need the serial number to refernce the DAC which is in our local dicitonary
        # The DAC must be read from the actual device., so it is stored in a dictionary of all the test house nvg599s
        #    self.device_access_code = nvg_info[self.serial_number]['device_access_code']
        #    print("dac", self.device_access_code)
        #   print("in ui_home_network_status  init if")

        print("in ui_set_band_bandwith_channel ")
        # url = 'http://192.168.1.254/'
        # session = webdriver.Chrome()
        # session.get(url)
        # session = self.session
        home_link = self.session.find_element_by_link_text("Device")
        home_link.click()
        status_link = self.session.find_element_by_link_text("Home Network")
        status_link.click()
        sleep(2)
        wifi_link = self.session.find_element_by_link_text("Wi-Fi")
        wifi_link.click()

        # handle being asked for password
        #self.session = self.check_if_password_required()
        self.check_if_password_required()

        sleep(10)
        advanced_options_link = self.session.find_element_by_link_text("Advanced Options")
        advanced_options_link.click()
        sleep(2)
# nvg_599_dut.ui_set_bw_channel('g2', 40, 2)
#        if band_selected == '2g' :
        if band == '2g':
            bandwidth_select = self.session.find_element_by_id("obandwidth")
            print('found obandwidth')
            print('bandwidth',bandwidth)
            #bandwidth_select.select_by_value(bandwidth)
            for option in bandwidth_select.find_elements_by_tag_name('option'):
                if option.text == bandwidth:
                   option.click()

            channel_select = self.session.find_element_by_id("ochannelplusauto")
            print('found ochannel')
            print('channel',channel)
            #bandwidth_select.select_by_value(bandwidth)
            for option in channel_select.find_elements_by_tag_name('option'):
                if option.text == channel:
                   option.click()

        if band == '5g':
            bandwidth_select = self.session.find_element_by_id("tbandwidth")
            print('found obandwidth')
            print('bandwidth', bandwidth)
            # bandwidth_select.select_by_value(bandwidth)
            for option in bandwidth_select.find_elements_by_tag_name('option'):
                if option.text == bandwidth:
                    option.click()

            channel_select = self.session.find_element_by_id("tchannelplusauto")
            print('tchannel 5g', channel)
            # bandwidth_select.select_by_value(bandwidth)
            for option in channel_select.find_elements_by_tag_name('option'):
                if option.text == channel:
                    option.click()
                    print('5g channel changed to channel:', channel)
            sleep(2)
#            ui_start_status_ = self.session.find_element_by_link_text("Device")
#            ui_start_status_()
#            sleep(2)
            return self.session

    def ui_get_wifi_info(self):
        print('in ui_get_wifi_info')
        url = 'http://192.168.1.254/'
        session = webdriver.Chrome()
        session.get(url)

        status_link = session.find_element_by_link_text("Home Network")
        status_link.click()
        sleep(2)

        home_network_link = session.find_element_by_link_text("Wi-Fi")
        home_network_link.click()
        sleep(2)

        handles = session.window_handles
        size = len(handles)
        print('size:',size)

        for x in range(size):
            session.switch_to.window(handles[x])
            print("title", session.title)
            print("handle", handles[x])

        self.check_if_password_required()
        print('tada2)')

        # try:
        #    #dac_access_challenge = browser.find_element_by_link_text("Forgot your Access Code")
        #    dac_access_challenge = session.find_element_by_xpath('//*[@id="main-content"]/div[2]/div[2]/div/h1').text
        #   print('dac challenge',dac_access_challenge)
        # #   dac_entry = session.find_element_by_id("password")
        #  print('dac_access',self.device_access_code)
        #   dac_entry.send_keys(self.device_access_code)
        #   submit = session.find_element_by_name("Continue")
        #   submit.click()
        #   sleep(20)
        # except NoSuchElementException:
        #   pass


    def get_ui_system_information(self):
        print('in get_ui_system_information)')
        global nvg_info
        url = 'http://192.168.1.254/'
        # session = self.session
        self.session = webdriver.Chrome()
        self.session.get(url)
        status_link = self.session.find_element_by_link_text("System Information")
        status_link.click()
        sleep(2)
        soup = BeautifulSoup(self.session.page_source, 'html.parser')
        sleep(5)
        this = soup.find_all('th')
        for th in this:
            if th.text == "Model Number":
                print("model:", th.next_sibling.next_sibling.text)
                self.model_number = th.next_sibling.next_sibling.text
            if th.text == "Serial Number":
                self.serial_number = th.next_sibling.next_sibling.text
                print ("serial Number is:",self.serial_number)
                # print ("nvg serial number dict",nvg_info[self.serial_number])
                # print("nvg access code", nvg_info[self.serial_number]['device_access_code'])
                # tmp_dac = nvg_info[self.serial_number]['device_access_code']
                # self.device_access_code = tmp_dac
                self.device_access_code = nvg_info[self.serial_number]['device_access_code']
                print("dac is:",self.device_access_code)
            if th.text == "Software Version":
                print(th.next_sibling.next_sibling.text)
                self.software_version = th.next_sibling.next_sibling.text
            if th.text == "MAC Address":
                print(th.next_sibling.next_sibling.text)
                self.mac_address = th.next_sibling.next_sibling.text
            if th.text == "Time Since Last Reboot":
                print(th.next_sibling.next_sibling.text)
                self.last_reboot_time = th.next_sibling.next_sibling.text
            if th.text == "Current Date/Time":
                print(th.next_sibling.next_sibling.text)
                self.current_date = th.next_sibling.next_sibling.text
            if th.text == "Hardware Version":
                print(th.next_sibling.next_sibling.text)
                self.hardware_version = th.next_sibling.next_sibling.text

        sleep(2)

# 2.4 bw possibilities 20,40
# 5 bw possibilities 20,40,80
# InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.BSSID fc:51:a4:2f:25:94
# InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.AutoChannelEnable 0
# InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.X_0000C5_BandLock X_0000   C5_5.0GHz


# tr69 GetParameterValues  InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.X_0000C5_Bandwidth
# tr69 SetParameterValues  InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.X_0000C5_Bandwidth=X_0000C5_80MHz
# tr69 SetParameterValues  InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.X_0000C5_Bandwidth=X_0000C5_40MHz
# InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.X_0000C5_Bandwidth X_0000C5_80MH

    def channelTest(self,b2G,b5G,bw2G,bw5G):
        for ib2G in b2G:
            for ib5G in b5G:
                for ibw in b2G:
                    print("2G:" + ib2G + " 5G:" + ib5G + "bandwidth" + ibw)

    def get_4920_inf_from_ui(self):
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


#    def get_sn_from_ui(self):
#         self.webDriver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
#       # driver.get('http://www.google.com')
#        self.webDriver.get('http://192.168.1.254')
#        self.webDriver.implicitly_wait(20)
        # driver.find_elements_by_tag_name("Settings") // this is for 599

    def run_speed_test_cli(self,speed_test_ip):

        print('in run_speedtest_cli')
        #speed_test_ip = "192.168.1.255"
        #ddd = f"{speed_test_ip} is a test"
        #print (ddd)
        #exit()
        #ssh_session = pexpect.spawn("ssh arris@192.168.1.239", encoding='utf-8',timeout=120)
        ssh_session = pexpect.spawn("ssh arris@" + speed_test_ip, encoding='utf-8',timeout=120)

        ssh_session.expect("ord:")
        ssh_session.sendline('arris123')
        print('after sendline\n')
        ssh_session.expect("\$")
        print('1',ssh_session.before)
        sleep(2)

        ssh_session.sendline('date')
        ssh_session.expect("\$")
        print('2', ssh_session.before)

        ssh_session.sendline('speedtest-cli')
        sleep(10)
        # ssh_session.expect(".*Mbits.*Mbits\/s")
        ssh_session.sendline()
        ssh_session.expect("\$")
        print('3',ssh_session.before)

        speed_test_ouput = ssh_session.before

        # speed_test_regex = re.compile(r'.*Download:\s+(\w+)\s+.*Upload:\s+(\w+)',re.DOTALL)
        speed_test_regex = re.compile(r'(Download:\s+\w+\.\w+\s+\w+).*(Upload:\s+\w+\.\w+\s+\w+)',re.DOTALL)

        speed_test_groups = speed_test_regex.search(speed_test_ouput)
        print(speed_test_groups.group(1))
        print(speed_test_groups.group(2))
        down_load_speed = speed_test_groups.group(1)
        up_load_speed  = speed_test_groups.group(2)

        return down_load_speed,up_load_speed

        # exit()
        # statusInfoRegEx = re.compile(r'Model\s(\w+)')
        # mo1 = statusInfoRegEx.search(statusOutput)


        # print('in_speedtest_cli')
        # cmd='ping -c1 192.168.1.254'
        # result = os.system(cmd)
        # print ('result:',result)
        # start = time.time()
        # print("hello")
        # end = time.time()
        # print(end - start)

    def ping_from_local_host(self,remote_ip):
        print('in ping_test')
        # out = subprocess.Popen("ping  -c3 localhost",stdout=subprocess.PIPE,stderr=subprocess.STDOUT, shell=True)
        # out = subprocess.Popen(["ping ", "-c3"," localhost"], stdout=subprocess.PIPE)
        # out, err = out.communicate()
        # out = check_output(["ping ", "-c3 ", "localhost"]).decode("utf-8")
        # out = check_output(["ls -la"].decode("utf-8").shell=True)
        out = subprocess.check_output("ping -c10 " + remote_ip ,shell = True).decode("utf-8")
        # cmd = 'ping -c1 192.168.1.254'
        # result = os.system(cmd)
        # pprint('resut from ping pipe',(out.communicate()))
        print('out===========\n',out)
        print('endout1===========\n')
        # exit()
        # pingInfoRegEx = re.compile(r'.*=\s(\w+)/(\w+)/(\w+)/(\w+)',re.DOTALL)
        pingInfoRegEx = re.compile(r'rtt.*?=\s(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)')

        #pingInfoRegEx = re.compile(r'.*?rtt/s+=/s+(/d+/./d+)',re.DOTALL)

        mo1 = pingInfoRegEx.search(out)
        # print('mo1',mo1)
        minimum = mo1.group(1)
        print('mnext--just a value', min)
        minimum = mo1.group(1)
        avg = mo1.group(2)
        max = mo1.group(3)
        mdev = mo1.group(4)
        return minimum,avg,max,mdev

    def connect_to_console(self):
        print('I am in console')
        cmd =' ping -c1 192.168.1.254'
        result = os.system(cmd)
        print ('result:',result)
        start = time.time()
        print("hello")
        end = time.time()
        print(end - start)

    def login_nvg_599_cli(self):
        print('In login_nvg_cli')
        self.telnet_cli_session = pexpect.spawn("telnet 192.168.1.254", encoding='utf-8')
        self.telnet_cli_session.expect("ogin:")
        self.telnet_cli_session.sendline('admin')
        self.telnet_cli_session.expect("ord:")
        self.telnet_cli_session.sendline('<<01%//4&/')
        self.telnet_cli_session.expect(">")
        self.telnet_cli_session.sendline('magic')
        self.telnet_cli_session.expect(">")
        self.telnet_cli_session.sendline('nsh')
        self.telnet_cli_session.expect("(nsh)")
        self.telnet_cli_session.sendline('set security.ext-wifi-protection off')
        self.telnet_cli_session.expect("(nsh)")
        self.telnet_cli_session.sendline('save')
        self.telnet_cli_session.expect("(nsh)")
        self.telnet_cli_session.sendline('apply')
        self.telnet_cli_session.expect("(nsh)")
        self.telnet_cli_session.sendline('exit')
        self.telnet_cli_session.expect(">")
        return self.telnet_cli_session

#    def login_4920(self,ip_4920):
#        print('In login_4920')
#        self.telnet_cli_session = pexpect.spawn("telnet" + ip_4920, encoding='utf-8')
#        self.telnet_cli_session.expect("ogin:")
#        self.telnet_cli_session.sendline('root')
#        self.telnet_cli_session.expect("#")
#        self.telnet_cli_session.sendline('<<01%//4&/')
#        self.telnet_cli_session.expect(">")
#        return telnet_cli_session
    
    def connect_cli(self, ip):
        self.IP = ip
        #cls.ssh = pexpect.spawn('ssh ' + name)
        print('in connect_cli')
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
        self.session = self.login_nvg_599_cli()
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

    def turn_off_supplicant_cli(self):
        self.telnet_cli_session = self.login_nvg_599_cli()
        self.telnet_cli_session.sendline('magic')
        self.telnet_cli_session.expect("UNLOCKED>")
        print('turning on ssh')
        self.telnet_cli_session.sendline('tr69 set InternetGatewayDevice.X_0000C5_Debug.SshdEnabled=1')
        self.telnet_cli_session.expect("successful.*>")
        self.telnet_cli_session.sendline('conf')
        self.telnet_cli_session.expect("top\)>>")
        self.telnet_cli_session.sendline('system supplicant')
        self.telnet_cli_session.expect("\(system supplicant\)>>")
        #self.session.expect(">>")
        self.telnet_cli_session.sendline('set')
        self.telnet_cli_session.expect("]:")
        self.telnet_cli_session.sendline('off')
        self.telnet_cli_session.expect("\(system supplicant\)>>")
        self.telnet_cli_session.sendline('save')
            # should check for "Configuration data saved.  as well
            # NOS/277427577103760 (system supplicant)>>
        self.telnet_cli_session.expect("\(system supplicant\)>>")
        self.telnet_cli_session.sendline('exit')
        self.telnet_cli_session.expect("UNLOCKED>")
        self.telnet_cli_session.sendline('exit all')
        print('telnet_cli turned off system supplicant')
        self.telnet_cli_session.close()

    def print_me(self):
        print('I am an NVG599 object')

    def get_rg_serial_number_cli(self):
        self.login_nvg_599_cli()
        self.telnet_cli.sendline('status')
        self.telnet_cli.expect('>')
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

    def get_rg_sh_ip_lan_info_cli(self):
        #session=self.login_nvg_599_cli()
        # I think these should all be telnet cli
        self.telnet_cli.sendline("show ip lan")
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
            # print("input line:", ipLanOutput[i])
            # mo1 = statusInfoRegEx.match(ipLanOutput[i])
            ipLanOutputSplit = (ipLanOutput[i]). split()
            # print ("connectedDeviceName",ipLanOutputSplit[0])
            # self.connectedDeviceName = ipLanOutputSplit[0]
            connectedDeviceName = ipLanOutputSplit[0]

            # if "ATT_4920" in ipLanOutputSplit[0]:
            #    print("this is an airties device!")
            print ("connectedDeviceIP", ipLanOutputSplit[1])
            connectedDeviceIP = ipLanOutputSplit[1]

            print ("connectedDeviceMac",ipLanOutputSplit[2])
            connectedDeviceMac = ipLanOutputSplit[2]
            print ("connectedDeviceStatus",ipLanOutputSplit[3])
            connectedDeviceStatus = ipLanOutputSplit[3]
            print ("connectedDeviceDHCP",ipLanOutputSplit[4])
            connectedDeviceDHCP = ipLanOutputSplit[4]
            print ("connectedDeviceSSIDNumber",ipLanOutputSplit[5])
            connectedDeviceSSIDNumber = ipLanOutputSplit[5]
            #self.showIPLanDict[connectedDeviceName] = {}
            self.showIPLanDict[connectedDeviceMac] = {}

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

