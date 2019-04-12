# from itertools import count
# from typing import Dict
import subprocess
# from subprocess import check_output

# from selenium.webdriver.common.by import By

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

# nvg_info: Dict[str, Dict[str, str]] = {"228946241148656": {'model': 'nvg599', 'device_access_code': "*<#/53#1/2", 'magic': 'kjundhkdxlxr',
nvg_info = {"228946241148656": {'model': 'nvg599', 'device_access_code': "*<#/53#1/2", 'magic': 'kjundhkdxlxr',
                                     'mac2g': 'd0:39:b3:60:56:f1', 'mac5g': 'd0:39:b3:60:56:f4',
                                     'wiFi': 'c2cmybt25dey', 'ssid': 'ATTqbrAnYs'},
            "277427577103760": {'model': 'nvg599', 'device_access_code': '<<01%//4&/', 'magic': 'ggtxstgwipcg',
                                     'mac2g': 'fc:51:a4:2f:25:90', 'mac5g': 'fc:51:a4:2f:25:94',
                                     'wiFi': 'nsrmpr59rxwv', 'ssid': 'ATTqbrAnYs'}}

test_house_devices_static_info = {
    '88:41:FC:86:64:D4': {'device_type': 'airties4920', 'radio': 'abg', 'band': 'base', 'state': 'None',
                          'address_type': 'None', 'port': 'None','ssid': 'None', 'rssi': 'None', 'ip': 'None', 'test_name': 'airties_1',
                          'host_name': 'ATT_4920_8664D4'},
    '88:41:FC:86:64:D7':{'device_type':'airties4920','radio':'abg','band' :'5g','state':'None','address_type':'None','port':'None',
                         'ssid':'None','rssi':'None','ip':'None','test_name':'airties_1','host_name':'ATT_4920_8664D4'},
    '88:41:FC:C3:56:C0':{'device_type':'airties4920','radio':'abg','band' :'base','state':'None','address_type':'None','port':'None',
                         'ssid':'None','rssi': 'None','ip': 'None',' test_name': 'airties_2', 'host_name': 'ATT_4920_C356C0'},
    '88:41:FC:C3:56:C3': {'device_type': 'airties4920', 'radio': 'abg', 'band': '5g', 'state': 'None',
                          'address_type': 'None', 'port': 'None','ssid': 'None', 'rssi': 'None', 'ip': 'None', ' test_name': 'airties_2',
                          'host_name': 'ATT_4920_C356C0'},
    '4C:BB:58:68:BD:F6':{'device_type':'ubuntu_laptop','radio':'bg','band' :'5g','state':'None','address_type':'None','port':'None',
                         'ssid' : 'None', 'rssi' : 'None', 'ip' : 'None', 'test_name' : 'ubuntu_1', 'host_name':'arris-Latitude-MBR'},
    'F4:5C:89:9D:F1:4F':{'device_type' : 'macbook_pro', 'radio' : 'abg','band' : '5g', 'state' : 'None', 'address_type' : 'None', 'port' : 'None',
                         'ssid' :'None','rssi' :'None', 'ip' : 'None', 'test_name' : 'mac_book_1', 'host_name' : 'macbook-mbr'},
    '5C:E0:C5:D9:8E:BF': {'device_type' : 'ubuntu_laptop', 'radio' : 'abg', 'band' :'5g', 'state' : 'None', 'address_type' : 'None',
                          'port' : 'None', 'ssid' : 'None', 'rssi' : 'None', 'ip' : 'None', 'test_name' : 'mac_book_1','host_name' : 'palmer_Latitude-E5450'},

}

# 5c:e0:c5:d9:8e:bf

NON_DFS_CHANNELS = {36, 40, 44, 48, 149, 153, 157, 161, 165}
DFS_CHANNELS = {52, 56, 60, 64, 100, 104, 108, 112, 116, 132, 136, 140, 144}


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
        self.model = None
        self.session = None
        self.init_info = False
        self.telnet_cli_session = None
        global nvg_info
        # The DAC must be read from the actual device., so it is stored in a dictionary of all the test house nvg599s
        print("Device Access Code:", self.device_access_code)
        self.software_version = None
        self.mac_address = None
        self.last_reboot_time = None
        self.current_date = None
        self.hardware_version = None
        self.serial_number = None
        self.factory_reset = None
        self.cli_rg_connected_clients_dict = {}
        self.ui_rg_connected_clients_dict = {}
        self.ip_lan_connections_dict_cli = {}

        self.get_ui_system_information()
        self.device_access_code = nvg_info[self.serial_number]['device_access_code']
        print("in Nvg599Class__init")
        self.init_info = True

        self.mesh_connected_clents = {}

    def ui_get_device_list(self):
        global nvg_info
        global test_house_devices_static_info
        print("in ui_get_device_list ")
        home_link = self.session.find_element_by_link_text("Device")
        home_link.click()
        status_link = self.session.find_element_by_link_text("Device List")
        status_link.click()
        #soup = BeautifulSoup(self.session.page_source, 'html.parser')
        soup = BeautifulSoup(self.session.page_source, 'lxml')
        table = soup.find("table", {"class": "table100"})

        for table_row in table.find_all("tr"):

            if table_row.td.has_attr('colspan'):
                print('colspan ------------skipping-----------------------------:' + table_row.td.attrs['colspan'] + '\n\n')
                continue

            if table_row.th.text == "MAC Address":
                #print("table header:" + (table_row.th.text).strip() + ":test")
                print("table mac:" + table_row.td.text.strip() + ":test")

                mac = (table_row.td.text.strip()).upper()
                if mac in test_house_devices_static_info:
                    print('macx found in lab dict', mac)
                    self.ui_rg_connected_clients_dict[mac] = {}

                    table_row = table_row.find_next_sibling()
                    if table_row.th.text == "IPv4 Address / Name":
                        #print('name:' + (table_row.th.text).strip() + ':this is the ip and name' )
                        ip_and_name_str = (table_row.td.text).strip()
                        ip_and_name_list = ip_and_name_str.split(" / ")
                        ip = ip_and_name_list[0]
                        ip = str(ip)
                        name = ip_and_name_list[1]
                        name = str(name)
                        print( 'ip is:'+ ip +':name is:' + name)
                        self.ui_rg_connected_clients_dict[mac]['ip'] = ip
                        self.ui_rg_connected_clients_dict[mac]['name'] = name

                    table_row = table_row.find_next_sibling()
                    if table_row.th.text == "Last Activity":
                        print('Last Activty:' + table_row.th.text.strip() + ':Last Activity' )
                        last_activity = table_row.td.text.strip()
                        print( 'last activity:'+ last_activity +':end last activity')
                        self.ui_rg_connected_clients_dict[mac]['last_activity'] = last_activity

                    table_row = table_row.find_next_sibling()
                    if table_row.th.text == "Status":
                        # print('status:' + (table_row.th.text).strip() + ':status')
                        status = table_row.td.text.strip()
                        print('last status:' + status + ':end status')
                        self.ui_rg_connected_clients_dict[mac]['status'] = status

                    table_row = table_row.find_next_sibling()
                    if table_row.th.text == "Allocation":
                        # print('status:' + (table_row.th.text).strip() + ':status')
                        allocation = (table_row.td.text).strip()
                        print('allocation:' + allocation + '\n')
                        self.ui_rg_connected_clients_dict[mac]['allocation'] = allocation

                    table_row = table_row.find_next_sibling()
                    if table_row.th.text == "Connection Type":
                        # print('status:' + (table_row.th.text).strip() + ':status')
                        connection_type = table_row.td.text
                        connection_type_str = str(connection_type)
                        print('connecttype dtr before split:',connection_type_str)
                        connection_list = connection_type_str.split()
                        # connection_list = re.split(' |\n',connection_type_str)

                        #connection_list = [s.strip() for s in connection_type_str.splitlines()]


                        print('aftersplit0:' + connection_list[0] + '\n')
                        print('aftersplit1:' + connection_list[1] + '\n')
                        print('aftersplit2:' + connection_list[2] + '\n')
                        print('aftersplit3:' + connection_list[3] + '\n')
                        network_type = (connection_list[3])[0:4]
                        print('Network Type',network_type)
                        print('aftersplit4:' + connection_list[4] + '\n')
                        network_name = (connection_list[4])
                        print('Network Name',network_name)



                        exit()
                        #connection_list = split('\n|\s',connection_type_str)

                        print('conn type str:', connection_type_str)

                        print('conn0:'+ (connection_list[0]) + '\n')
                        print('Connection Eth/Wi-FI:',connection_list[0])

                        if connection_list[0].find("Ethernet") is not -1:
                            print('con list 0:',connection_list[0])
                            self.ui_rg_connected_clients_dict[mac]['connect_type_eth_wifi'] = connection_list[0]
                            continue

                        self.ui_rg_connected_clients_dict[mac]['connect_type_eth_wifi'] = connection_list[0]
                        #print('Type wifi or eth:'+ (connection_list[0])[0:4] + '\n')



                        print('exit con list 0GHZ:'+ connection_list[0] + '\n')
                        exit()
                        print('conn1:'+ connection_list[1] + '\n')


                        conn_2 = connection_list[2]
                        print('this is conn 2:' + conn_2 + '\n')
                        print('Type:'+ (connection_list[3])[0:4] + '\n')
                        #self.ui_rg_connected_clients_dict[mac]['connect_speed'] = connection_list[1]
                        conn_4 = connection_list[4]
                        print('Name:  ' + conn_4 + '\n')

                        #conn_4 = connection_list[4]
                        #print('conn4_str:  ' + conn_4 + '\n')


                        #self.ui_rg_connected_clients_dict[mac]['wi_fi_band'] = connection_list[2]

                        #conn_2_str = str(conn_2)
                        #print('connection Type:',conn_2_str[0:4])
                        #conn_2_list = re.split('\n|\s', conn_2_str)
                        #print('Connection Type:',conn_2_str[0:4])
                        #print('Home name is:'+ conn_2_list[1])

                        #type_str_list = conn_2.split()
                        #print ('type is:' + type_str_list[0] + '\n')
                        #print ('list 1 is:' + type_str_list[1] + '\n')
                        #print ('list 2 is:' + type_str_list[2] + '\n')


                        #print('type',connection_list[2])
                        #name_str = str(connection_list[3])
                        #name_str_list = name_str.split(' ','"')

                        #print(re.split('\n|\s',name_str))

                        #name_str_list = re.split('\n| ', name_str)

                        #name_str_list = name_str.split(' ','"')

                        #print ('Connection Name:'+ name_str_list[0]+'\n')

                        #self.ui_rg_connected_clients_dict[mac]['connection_type_name'] = name_str_list[0]


                        #print('is this the link' + str(table_row.td) + '\n')
                        #td_connection_string = str(table_row.td)
                        #print('td_con str:' + td_connection_string + '\n')


                        for img in table_row.td.find_all('img'):
                            #print('is this it', img['alt'])
                            alt_entry = img['alt']
                            alt_entry_sting = str(alt_entry)
                            alt_entry_list = alt_entry_sting.split()
                            print('strength out of 5 is:' + alt_entry_list[1]+ '\n')

                        self.ui_rg_connected_clients_dict[mac]['strength'] = alt_entry_list[1]




            #     exit()
            #
            # #continue
            #
            #
            # if not table_row.has_attr('th'):
            #     print('in header = 0 \n')
            #     print("table_row:",table_row, end = '')
            #
            # if table_row.th.text == "MAC Address":
            #     print ('mac is &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&x'+ (table_row.td.text).strip() + 'x*******************')
            #     mac = ((table_row.td.text).strip()).upper()
            #     if mac in test_house_devices_static_info:
            #         self.cli_rg_connected_clients_dict[mac] = {}
            #         print('               macx found in lab dict', mac)
            #         self.ui_rg_connected_clients_dict[mac] = mac
            #         ip_sibling = table_row.nextSibling
            #         print('              sibling type',type(ip_sibling))
            #         print('              ip sibling in as expected' + ip_sibling.findNext.th.text + 'end pf sibling expected\n')
            #         print('              ----')
            #         print('\n')
            #         print('\n')
            #         print('\n')
            #         exit()
            #         if ip_sibling.th.text == "IPv4 Address / Name":
            #             ip_name =ip_sibling.th.text
            #             print('ip found in as ex[ected' + ip_name + " end of expected \n")
            #
            #         else:
            #             print('ip_ heading', ip_sibling.th.text)
            #
            #             print('')
            #             print('')
            #             print('')
            #             continue

        # exit()
        # for table_rows in table.find_all("tr"):
        #     for row_header in table_rows:
        #         td = row_header.find_all('td')
        #         print("Name    ", td.text)
        # exit()
        #
        # soup = BeautifulSoup(self.session.page_source, 'html.parser')
        # tables = soup.findChildren('table')
        # # five tables on this page
        # table = tables[4]
        # # table = soup.find("table100", {"class": "table100"})
        # # print ("table is",table)
        # table_rows = table.find_all('tr')
        # for tr in table_rows:
        #     td = tr.find_all('td')
        #     tc = td.find_all('class')
        #     if tc.text == "reshr":
        #         continue
        #     row = [i.text for i in td]
        #     # print("length is:",len(row))
        #     # print("type",type(row))
        #     print("row text", row)


    def check_if_password_required(self):
        try:
            # dac_access_challenge = self.session.find_element_by_link_text("Forgot your Access Code?")
            self.session.find_element_by_link_text("Forgot your Access Code?")
            print('we found the request for password screen')
            print('sending dac', self.device_access_code)
            dac_entry = self.session.find_element_by_id("password")
            dac_entry.send_keys(self.device_access_code)
            submit = self.session.find_element_by_name("Continue")
            submit.click()
            sleep(5)
        except NoSuchElementException:
            print('password challenge screen not displayed- OK')

    def cli_sh_wi_clients(self):
        global test_house_devices_static_info
        print("in cli_sh_wi_clients")
        self.telnet_cli_session = self.login_nvg_599_cli()
        self.telnet_cli_session.sendline("show wi clients")
        self.telnet_cli_session.expect('OCKED>')
        show_wi_client_str = self.telnet_cli_session.before
        self.telnet_cli_session.close()
        print('------------------------------------------------------\n')
        print('------------------------------------------------------\n')
        # dividing on macs
        wi_reg_ex = re.compile(r'(?:[0-9a-fA-F]:?){12}.*?\n.*\n.*\n.*\n')
        client_string_list = re.findall(wi_reg_ex, show_wi_client_str)

        number_of_entries = len(client_string_list)
        print("The list has :", number_of_entries)

        client_entries = range(0, number_of_entries)

        for client_list_entry in client_entries:
            print("entry:", client_string_list[client_list_entry])
            print("-------------------------")

            client_string_list_split = client_string_list[client_list_entry].split()

            mac = client_string_list_split[0]
            mac = mac.upper()
            mac = mac[:-1]
            print('modified 2g mac', mac)

            if mac in test_house_devices_static_info:
                self.cli_rg_connected_clients_dict[mac] = {}
                print('mac found in lab dict', mac)

                self.cli_rg_connected_clients_dict[mac]['band'] = test_house_devices_static_info[mac]['band']
                print('setting nband to:',  self.cli_rg_connected_clients_dict[mac]['band'])

                if re.search(r'.*State=(\w+),', client_string_list[client_list_entry]) is not None:
                    wi_state_search = re.search(r'.*State=(\w+)', client_string_list[client_list_entry])
                    self.cli_rg_connected_clients_dict[mac]['wi_state'] = wi_state_search.group(1)
                    print('Seting wi_state to ', wi_state_search.group(1))
                else:
                    self.cli_rg_connected_clients_dict[mac]['wi_state'] = "Not found or State value missing"
                    print('Seting wi_state to Not Found or value missing ')

                if re.search(r'.*IP:\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', client_string_list[client_list_entry]) is not None:
                    wi_state_search = re.search(r'.*IP:\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', client_string_list[client_list_entry])
                    self.cli_rg_connected_clients_dict[mac]['ip'] = wi_state_search.group(1)
                    print('Seting ip to ', wi_state_search.group(1))
                else:
                    self.cli_rg_connected_clients_dict[mac]['ip'] = "Not found or State value missing"
                    print('Seting ip to Not Found or value missing ')

                if re.search(r'.*SSID=(\w+)', client_string_list[client_list_entry]) is not None:
                    wi_state_search = re.search(r'.*SSID=(\w+)', client_string_list[client_list_entry])
                    self.cli_rg_connected_clients_dict[mac]['ip'] = wi_state_search.group(1)
                    print('Seting SSID to ', wi_state_search.group(1))
                else:
                    self.cli_rg_connected_clients_dict[mac]['ssid'] = "Not found or State value missing"
                    print('Seting ssid to Not Found or value missing ')

                if re.search(r'.*PSMod=(\w+)', client_string_list[client_list_entry]) is not None:
                    wi_state_search = re.search(r'.*PSMod=(\w+)', client_string_list[client_list_entry])
                    self.cli_rg_connected_clients_dict[mac]['psmod'] = wi_state_search.group(1)
                    print('Seting psmod to ', wi_state_search.group(1))
                else:
                    self.cli_rg_connected_clients_dict[mac]['psmod'] = "Not found or value missing"
                    print('Seting psmod to Not Found or value missing ')

                if re.search(r'.*NMod=(\w+)', client_string_list[client_list_entry]) is not None:
                    wi_state_search = re.search(r'.*NMod=(\w+)', client_string_list[client_list_entry])
                    self.cli_rg_connected_clients_dict[mac]['nmod'] = wi_state_search.group(1)
                    print('Seting psmod to ', wi_state_search.group(1))
                else:
                    self.cli_rg_connected_clients_dict[mac]['nmod'] = "Not found or value missing"
                    print('Seting nmmod to Not Found or value missing ')

                if re.search(r'.*WMMEn=(\w+)', client_string_list[client_list_entry]) is not None:
                    wi_state_search = re.search(r'.*WMMEn=(\w+)', client_string_list[client_list_entry])
                    self.cli_rg_connected_clients_dict[mac]['wmmen'] = wi_state_search.group(1)
                    print('Seting psmod to ', wi_state_search.group(1))
                else:
                    self.cli_rg_connected_clients_dict[mac]['wmmen'] = "Not found or value missing"
                    print('Seting wmmen to Not Found or value missing ')

                if re.search(r'.*Rate=(\w+\s\w+)', client_string_list[client_list_entry]) is not None:
                    wi_state_search = re.search(r'.*Rate=(\w+\s\w+)', client_string_list[client_list_entry])
                    self.cli_rg_connected_clients_dict[mac]['wmmen'] = wi_state_search.group(1)
                    print('Seting rate to ', wi_state_search.group(1))
                else:
                    self.cli_rg_connected_clients_dict[mac]['rate'] = "Not found or value missing"
                    print('Seting rate to Not Found or value missing ')

                if re.search(r'.*ON\sfor\s(\w+\s\w+)', client_string_list[client_list_entry]) is not None:
                    wi_state_search = re.search(r'.*ON\sfor\s(\w+\s\w+)', client_string_list[client_list_entry])
                    self.cli_rg_connected_clients_dict[mac]['ontime'] = wi_state_search.group(1)
                    print('Seting ontime to ', wi_state_search.group(1))
                else:
                    self.cli_rg_connected_clients_dict[mac]['ontime'] = "Not found or value missing"
                    print('Seting On Time to Not Found or value missing ')

                if re.search(r'.*TxPkt=(\w+)', client_string_list[client_list_entry]) is not None:
                    wi_state_search = re.search(r'.*TxPkt=(\w+)', client_string_list[client_list_entry])
                    self.cli_rg_connected_clients_dict[mac]['txpkt'] = wi_state_search.group(1)
                    print('Seting txpkt to ', wi_state_search.group(1))
                else:
                    self.cli_rg_connected_clients_dict[mac]['txpkt'] = "Not found or value missing"
                    print('Seting txpkt to Not Found or value missing ')

                if re.search(r'.*TxErr=(\w+)', client_string_list[client_list_entry]) is not None:
                    wi_state_search = re.search(r'.*TxErr=(\w+)', client_string_list[client_list_entry])
                    self.cli_rg_connected_clients_dict[mac]['txerr'] = wi_state_search.group(1)
                    print('Seting txerr to ', wi_state_search.group(1))
                else:
                    self.cli_rg_connected_clients_dict[mac]['txerr'] = "Not found or value missing"
                    print('Seting txerr to Not Found or value missing ')

                if re.search(r'.*RxUni=(\w+)', client_string_list[client_list_entry]) is not None:
                    wi_state_search = re.search(r'.*RxUni=(\w+)', client_string_list[client_list_entry])
                    self.cli_rg_connected_clients_dict[mac]['rxuni'] = wi_state_search.group(1)
                    print('Seting rxuni to ', wi_state_search.group(1))
                else:
                    self.cli_rg_connected_clients_dict[mac]['rxuni'] = "Not found or value missing"
                    print('Seting rxuni to Not Found or value missing ')

                if re.search(r'.*RxMul=(\w+)', client_string_list[client_list_entry]) is not None:
                    wi_state_search = re.search(r'.*RxMul=(\w+)', client_string_list[client_list_entry])
                    self.cli_rg_connected_clients_dict[mac]['rxmul'] = wi_state_search.group(1)
                    print('Seting rxmul to ', wi_state_search.group(1))
                else:
                    self.cli_rg_connected_clients_dict[mac]['rxuni'] = "Not found or value missing"
                    print('Seting rxmul to Not Found or value missing ')

                if re.search(r'.*RxErr=(\w+)', client_string_list[client_list_entry]) is not None:
                    wi_state_search = re.search(r'.*RxErr=(\w+)', client_string_list[client_list_entry])
                    self.cli_rg_connected_clients_dict[mac]['rxerr'] = wi_state_search.group(1)
                    print('Seting rxerr to ', wi_state_search.group(1))
                else:
                    self.cli_rg_connected_clients_dict[mac]['rxerr'] = "Not found or value missing"
                    print('Seting rxerr to Not Found or value missing ')

                if re.search(r'.*RSSI=-(\w+)', client_string_list[client_list_entry]) is not None:
                    wi_state_search = re.search(r'.*RSSI=-(\w+)', client_string_list[client_list_entry])
                    self.cli_rg_connected_clients_dict[mac]['rxerr'] = wi_state_search.group(1)
                    print('Seting rssi to ', wi_state_search.group(1))
                else:
                    self.cli_rg_connected_clients_dict[mac]['rssi'] = "Not found or value missing"
                    print('Seting rssi to Not Found or value missing ')
            print("-------------------------")
            print("-------------------------")

            ##########################################################################################################################################

        # show_wi_clients_reg_ex = re.compile(r'.*State=(\w+).*IP:\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*SSID=(\w+).*PSMod=(\w+)?,.*NMode=(\w+)?,.*WMMEn=(\w+)?,.*Rate=(\w+\s\w+).*ON\sfor\s(\w+\s\w+)?.*TxPkt=(\w+).*TxErr=(\w+).*RxUni=(\w+).*RxMul=(\w+).*RxErr=(\w+).*RSSI=-(\w+)?', re.DOTALL)
        # show_wi_clients_reg_ex = re.compile(r'.*State=(\w+).*IP:(\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(\w+).*RxUni=(\w+).*RxMul=(\w+).*RxErr=(\w+).*RSSI=-(\w+)', re.DOTALL)

        return self.cli_rg_connected_clients_dict

    def factory_reset_rg(self):
        global nvg_info
        self.factory_reset = 1
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
        self.turn_off_supplicant_cli()
        self.enable_sshd_ssh_cli()

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
#        we need the band (2g or 5g) because both bands could be automatic which would be ambiguous
#        nvg_599_dut.ui_set_bw_channel('g2', 40, 2)

    def ui_set_band_bandwith_channel(self, band, bandwidth, channel):
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
        # self.session = self.check_if_password_required()
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
            print('bandwidth', bandwidth)
            # bandwidth_select.select_by_value(bandwidth)
            for option in bandwidth_select.find_elements_by_tag_name('option'):
                if option.text == bandwidth:
                    option.click()

            channel_select = self.session.find_element_by_id("ochannelplusauto")
            print('found ochannel')
            print('channel', channel)
            # bandwidth_select.select_by_value(bandwidth)
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
        print('size:', size)

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
                self.model = th.next_sibling.next_sibling.text
            if th.text == "Serial Number":
                self.serial_number = th.next_sibling.next_sibling.text
                print("serial Number is:", self.serial_number)
                # print ("nvg serial number dict",nvg_info[self.serial_number])
                # print("nvg access code", nvg_info[self.serial_number]['device_access_code'])
                # tmp_dac = nvg_info[self.serial_number]['device_access_code']
                # self.device_access_code = tmp_dac
                self.device_access_code = nvg_info[self.serial_number]['device_access_code']
                print("dac is:", self.device_access_code)
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

    def channel_test(self, b2g, b5g, bw2g, bw5g):
        for ib2g in b2g:
            for ib5G in b5g:
                for ibw in b2g:
                    print("2G:" + ib2g + " 5G:" + ib5G + "bandwidth" + ibw)

# not sure we want to open a new session
    def get_4920_inf_from_ui(self):
        global nvg_info
        url = 'http://192.168.1.254/cgi-bin/devices.ha'
        browser = webdriver.Chrome()
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, 'html.parser')

        this = soup.find_all('th')
        for th in this:
            if th.text == "IPv4 Address / Name":
                # print(th.next_sibling.next_sibling.text)
                print("Name    ", th.text)
                print("Name1", th.next_sibling.text)
            else:
                print("no derp")



    def run_speed_test_cli(self, speed_test_ip):

        print('in run_speedtest_cli')
        # speed_test_ip = "192.168.1.255"
        # ddd = f"{speed_test_ip} is a test"
        # print (ddd)
        # exit()
        # ssh_session = pexpect.spawn("ssh arris@192.168.1.239", encoding='utf-8',timeout=120)
        ssh_session = pexpect.spawn("ssh arris@" + speed_test_ip, encoding='utf-8', timeout=120)

        ssh_session.expect("ord:")
        ssh_session.sendline('arris123')
        print('after sendline\n')
        ssh_session.expect("$")
        print('1', ssh_session.before)
        sleep(2)

        ssh_session.sendline('date')
        self.device_access_code = None

        ssh_session.expect("$")
        print('2', ssh_session.before)

        ssh_session.sendline('speedtest-cli')
        sleep(10)
        # ssh_session.expect(".*Mbits.*Mbits\/s")
        ssh_session.sendline()
        ssh_session.expect("$")
        print('3', ssh_session.before)
        speed_test_ouput = ssh_session.before
        # speed_test_regex = re.compile(r'.*Download:\s+(\w+)\s+.*Upload:\s+(\w+)',re.DOTALL)
        speed_test_regex = re.compile(r'(Download:\s+\w+\.\w+\s+\w+).*(Upload:\s+\w+\.\w+\s+\w+)', re.DOTALL)
        speed_test_groups = speed_test_regex.search(speed_test_ouput)
        print(speed_test_groups.group(1))
        print(speed_test_groups.group(2))
        down_load_speed = speed_test_groups.group(1)
        up_load_speed = speed_test_groups.group(2)
        return down_load_speed, up_load_speed
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

    def ping_from_local_host(self, remote_ip):
        print('in ping_test')
        # out = subprocess.Popen("ping  -c3 localhost",stdout=subprocess.PIPE,stderr=subprocess.STDOUT, shell=True)
        # out = subprocess.Popen(["ping ", "-c3"," localhost"], stdout=subprocess.PIPE)
        # out, err = out.communicate()
        # out = check_output(["ping ", "-c3 ", "localhost"]).decode("utf-8")
        # out = check_output(["ls -la"].decode("utf-8").shell=True)
        out = subprocess.check_output("ping -c10 " + remote_ip, shell=True).decode("utf-8")
        # cmd = 'ping -c1 192.168.1.254'
        # result = os.system(cmd)
        # pprint('resut from ping pipe',(out.communicate()))
        print('out===========\n', out)
        print('endout1===========\n')
        # exit()
        # pingInfoRegEx = re.compile(r'.*=\s(\w+)/(\w+)/(\w+)/(\w+)',re.DOTALL)
        ping_info_reg_ex = re.compile(r'rtt.*?=\s(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)')
        # pingInfoRegEx = re.compile(r'.*?rtt/s+=/s+(/d+/./d+)',re.DOTALL)
        mo1 = ping_info_reg_ex.search(out)
        # print('mo1',mo1)
        minimum = mo1.group(1)
        print('mnext--just a value', minimum)
        min_ping = mo1.group(1)
        avg_ping = mo1.group(2)
        max_ping = mo1.group(3)
        mdev_ping = mo1.group(4)
        return min_ping, avg_ping, max_ping, mdev_ping

    def connect_to_console(self):
        print('in connect_to_console')
        cmd = ' ping -c1 192.168.1.254'
        result = os.system(cmd)
        print('result:', result)
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
        # put this stuff us a soearate factory defaults routine
        # self.telnet_cli_session.sendline('nsh')
        # self.telnet_cli_session.expect("(nsh)")
        # self.telnet_cli_session.sendline('set security.ext-wifi-protection off')
        # self.telnet_cli_session.expect("(nsh)")
        # self.telnet_cli_session.sendline('save')
        # self.telnet_cli_session.expect("(nsh)")
        # self.telnet_cli_session.sendline('apply')
        # self.telnet_cli_session.expect("(nsh)")
        # self.telnet_cli_session.sendline('quit')
        # self.telnet_cli_session.expect(">")
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
        self.ip = ip
        # cls.ssh = pexpect.spawn('ssh ' + name)
        print('in connect_cli')
        session = pexpect.spawn("telnet 192.168.1.254", encoding='utf-8')
        session.expect("ogin:")
        session.sendline('admin')
        session.expect("ord:")
        session.sendline('<<01%//4&/')
        session.expect(">")
        session.sendline('status')
        session.expect('>')
        status_output = session.before
        status_info_reg_ex = re.compile(r'Model\s(\w+)\s+\w+/\w+.*number\s+(\w+).*Uptime\s+(\d\d:\d\d:\d\d:\d\d)', re.DOTALL)
        # statusInfoRegEx = re.compile(r'Model\s(\w+).*Serial Number\s+(\d+)',re.DOTALL)
        # statusInfoRegEx = re.compile(r'Model\s(\w+)')
        mo1 = status_info_reg_ex.search(status_output)
        print(mo1)
        print('Model: ', mo1.group(1))
        print('Serial Number:', mo1.group(2))
        print('Uptime: ', mo1.group(3))
        self.model = mo1.group(1)
        self.serial_number = mo1.group(2)
        self.up_time = mo1.group(3)
        self.session.close()

    def setup_tr69_url(self):
        self.session = self.login_nvg_599_cli()
        self.session.sendline('magic')
        self.session.expect("UNLOCKED>")
        self.session.sendline('conf')
        self.session.expect("top)>>")
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

    def enable_sshd_ssh_cli(self):
        self.telnet_cli_session = self.login_nvg_599_cli()
        self.telnet_cli_session.sendline('magic')
        self.telnet_cli_session.expect("UNLOCKED>")
        print('turning on ssh via tr69 cli command')
        self.telnet_cli_session.sendline('tr69 set InternetGatewayDevice.X_0000C5_Debug.SshdEnabled=1')
        self.telnet_cli_session.expect("successful.*>")
        print('telnet_cli enabled sshd system supplicant')
        self.telnet_cli_session.close()

    def conf_tr69_eco_url(self):
        self.telnet_cli_session = self.login_nvg_599_cli()
        self.telnet_cli_session.sendline('magic')
        self.telnet_cli_session.expect("UNLOCKED>")
        self.telnet_cli_session.sendline('conf')
        self.telnet_cli_session.expect("\(top\)>>")
        self.telnet_cli_session.sendline('manage cwmp')
        self.telnet_cli_session.expect("\(management cwmp\)>>")
        self.telnet_cli_session.sendline('set')
        self.telnet_cli_session.expect("]:")
        self.telnet_cli_session.sendline('on')
        self.telnet_cli_session.expect("\):")
        self.telnet_cli_session.sendline('http://arris1.arriseco.com')
        self.telnet_cli_session.expect("\):") # this has some numbers
        self.telnet_cli_session.sendline()
        self.telnet_cli_session.expect("\*\*\*\"\): ")
        self.telnet_cli_session.sendline()
        self.telnet_cli_session.expect("xml\"\): ")
        self.telnet_cli_session.sendline()
        self.telnet_cli_session.expect(" 65535 \]:")
        self.telnet_cli_session.sendline()
        self.telnet_cli_session.expect("\"\"\) : ")
        self.telnet_cli_session.sendline()
        self.telnet_cli_session.expect("F2BQ\"\):")
        self.telnet_cli_session.sendline()
        self.telnet_cli_session.expect("255 \]:")
        self.telnet_cli_session.sendline()
        self.telnet_cli_session.expect("0 - 7 \]: ")
        self.telnet_cli_session.sendline()
        self.telnet_cli_session.expect("EE\"\):")
        self.telnet_cli_session.sendline()
        self.telnet_cli_session.expect("on ]:")
        self.telnet_cli_session.sendline()
        self.telnet_cli_session.expect("600 \]:")
        self.telnet_cli_session.sendline()
        self.telnet_cli_session.expect("on \]:")
        self.telnet_cli_session.sendline()
        self.telnet_cli_session.expect(">>")
        self.telnet_cli_session.sendline('save')
        self.telnet_cli_session.expect(">>")

        print('configure TR068 ECO url')



        self.telnet_cli_session.close()

    def turn_off_supplicant_cli(self):
        self.telnet_cli_session = self.login_nvg_599_cli()
        self.telnet_cli_session.sendline('magic')
        self.telnet_cli_session.expect("UNLOCKED>")
        self.telnet_cli_session.sendline('conf')
        self.telnet_cli_session.expect("top)>>")
        self.telnet_cli_session.sendline('system supplicant')
        self.telnet_cli_session.expect("\(system supplicant\)>>")
        # self.session.expect(">>")
        self.telnet_cli_session.sendline('set')
        self.telnet_cli_session.expect("]:")
        self.telnet_cli_session.sendline('off')
        self.telnet_cli_session.expect("\(system supplicant\)>>")
        self.telnet_cli_session.sendline('save')
        # should check for "Configuration data saved.  as well
        # NOS/277427577103760 (system supplicant)>>
        self.telnet_cli_session.expect("(system supplicant)>>")
        self.telnet_cli_session.sendline('exit')
        self.telnet_cli_session.expect("UNLOCKED>")
        self.telnet_cli_session.sendline('exit all')
        print('telnet_cli turned off system supplicant')
        self.telnet_cli_session.close()

    def get_rg_serial_number_cli(self):
        self.login_nvg_599_cli()
        self.telnet_cli_session.sendline('status')
        self.telnet_cli_session.expect('>')
        status_output = self.session.before
        print('Getting getSerialnumber')
        status_info_reg_ex = re.compile(r'Model\s(\w+)\s+\w+/\w+.*number\s+(\w+).*Uptime\s+(\d\d:\d\d:\d\d:\d\d)', re.DOTALL)
        # statusInfoRegEx = re.compile(r'Model\s(\w+).*Serial Number\s+(\d+)',re.DOTALL)
        # statusInfoRegEx = re.compile(r'Model\s(\w+)')
        mo1 = status_info_reg_ex.search(status_output)
        # print('model ', mo1.group(1))
        # print('Serial Number', mo1.group(2))
        # print('Uptime ', mo1.group(3))
        return mo1.group(2)

    def get_rg_sh_ip_lan_info_cli(self):
        # session=self.login_nvg_599_cli()
        self.telnet_cli_session. sendline("show ip lan")
        self.session.expect('>')
        ip_lan_output = self.session.before
        ip_lan_output = ip_lan_output.split('\n\r')
        print("-------------------------------------")
        lan_output_count = len(ip_lan_output)

        # discard first two lines of the output
        print("count", lan_output_count)
        ip_lan_output = ip_lan_output[2:-1]
        # I think the length minus 1 is what we want // need to check this
        for i in range(len(ip_lan_output)):
            # print("input line:", ipLanOutput[i])
            # mo1 = statusInfoRegEx.match(ipLanOutput[i])
            ip_lan_output_split = (ip_lan_output[i]).split()
            # print ("connectedDeviceName",ipLanOutputSplit[0])
            # self.connectedDeviceName = ipLanOutputSplit[0]
            connected_device_name = ip_lan_output_split[0]
            # if "ATT_4920" in ipLanOutputSplit[0]:
            #    print("this is an airties device!")
            print("connectedDeviceIP", ip_lan_output_split[1])
            connected_device_ip = ip_lan_output_split[1]
            print("connected_device_mac", ip_lan_output_split[2])
            connected_device_mac = ip_lan_output_split[2]
            print("connectedDeviceStatus", ip_lan_output_split[3])
            connected_device_status = ip_lan_output_split[3]
            print("connectedDeviceDHCP", ip_lan_output_split[4])
            connected_device_dhcp = ip_lan_output_split[4]
            print("connectedDeviceSSIDNumber", ip_lan_output_split[5])
            connected_device_ssid_number = ip_lan_output_split[5]
            # This dict uses the mac as the primary key
            self.ip_lan_connections_dict_cli[connected_device_mac] = {}
            self.ip_lan_connections_dict_cli[connected_device_mac]["IP"] = connected_device_ip
            self.ip_lan_connections_dict_cli[connected_device_mac]["Name"] = connected_device_name
            self.ip_lan_connections_dict_cli[connected_device_mac]["Status"] = connected_device_status
            self.ip_lan_connections_dict_cli[connected_device_mac]["DHCP"] = connected_device_dhcp
            self.ip_lan_connections_dict_cli[connected_device_mac]["SSIDNumber"] = connected_device_ssid_number
            self.session.close()
        return self.ip_lan_connections_dict_cli

    def login(self):
        pass

    # class Nvg_5268_Class(GatewayClass):
    #     def __init__(self):
    #         self.name = "Nvg_5268"
    #      # rg5268 = pexpect.spawn("telnet 192.168.1.254")
    #         sleep(1)
    #


