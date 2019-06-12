# from itertools import count
# from typing import Dict
import subprocess
from pexpect import pxssh
from socket import timeout
# from subprocess import check_output
# from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import urllib.request
from urllib.error import URLError, HTTPError
# import url
import urllib3
# import requests
# import httplib2
import pexpect
import re
import socket
import paramiko
# from paramiko_expect import SSHClientInteraction

# import os
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support.ui import WebDriverWai
from selenium import webdriver
from selenium.webdriver.support.ui import Select
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import smtplib
# from collections import defaultdict
# import sys
from time import sleep
import time
from email.message import EmailMessage
from datetime import datetime

#  Apple path for wifi info
# /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I

nvg_info = {"228946241148656": {'model': 'nvg599', 'device_access_code': "*<#/53#1/2", 'magic': 'kjundhkdxlxr',
                                'mac2g': 'd0:39:b3:60:56:f1', 'mac5g': 'd0:39:b3:60:56:f4', 'wiFi': 'c2cmybt25dey',
                                'ssid': 'xxxxxx'},
            "277427577103760": {'model': 'nvg599', 'device_access_code': '<<01%//4&/', 'magic': 'ggtxstgwipcg',
                                'mac2g': 'fc:51:a4:2f:25:90', 'mac5g':
                                'fc:51:a4:2f:25:94', 'wiFi': 'nsrmpr59rxwv', 'ssid': 'ATTqbrAnYs'},
            "35448081188192":   {'model': 'nvg599', 'device_access_code': '9==5485?6<', 'magic': 'pqomxqikedca',
                                 'mac2g': '20:3d:66:49:85:61', 'mac5g': '11:22:33:44:55:66', 'wifi': 'eeh4jxmh7q26',
                                 'ssid': 'ATT4ujR48s'}}

test_house_devices_static_info = {
    '88:41:FC:86:64:D6': {'device_type': 'airties_4920', 'oper_sys': 'tbd', 'radio': 'abg', 'band': '2',
                          'state': 'Nonne',
                          'address_type': 'None', 'port': 'None', 'ssid': 'None', 'rssi': 'None', 'ip': 'None',
                          'device_test_name': 'airties_1_2g', 'name': 'ATT_4920_8664D4', 'location': 'master_bedroom'},
    '88:41:FC:86:64:D4': {'device_type': 'airties_4920', 'oper_sys': 'tbd', 'radio': 'abg', 'band': '5',
                          'state': 'None',
                          'address_type': 'None', 'port': 'None', 'ssid': 'None',  'rssi': 'None', 'ip': 'None',
                          'device_test_name': 'airties_1_5g', 'name': 'ATT_4920_8664D4', 'location': 'master_bedroom'},
    '88:41:FC:C3:56:C2': {'device_type': 'airties_4920', 'oper_sys': 'tbd', 'radio': 'abg', 'band': '2',
                          'state': 'None',
                          'address_type': 'None', 'port': 'None', 'ssid': 'None', 'rssi': 'None', ' ip': 'None',
                          'device_test_name': 'airties_2_2g', 'name': 'ATT_4920_C356C0', 'location': 'master_bedroom'},
    '88:41:FC:C3:56:C0': {'device_type': 'airties_4920', 'oper_sys': 'tbd',  'radio': 'abg', 'band': '5',
                          'state': 'None',
                          'address_type': 'None', 'port ': 'None', 'ssid': 'None', 'rssi': 'None', 'ip': 'None',
                          'device_test_name': 'airties_2_5g', 'name': 'ATT_4920_C356C0', 'location': 'master_bedroom'},
    '4C:BB:58:68:BD:F6': {'device_type': 'ubuntu_laptop', 'oper_sys': 'tbd', 'radio': 'bg', 'band': '5',
                          'state': 'None',
                          'address_type': 'None', 'port': 'None', 'ssid': 'None', 'rssi': 'None', 'ip': 'None',
                          'device_test_name': 'ubuntu_1', 'name': 'arris-Latitude-MBR', 'location': 'tbd'},

    'F4:5C:89:9D:F1:4F': {'device_type': 'macbook_pro', 'oper_sys': 'tbd', 'radio': 'abg', 'band': '5',
                          'state': 'None',
                          'address_type': 'None', 'port': 'None', 'ssid': 'None', 'rssi': 'None', 'ip': 'None',
                          'device_test_name': 'mac_book_1', 'name': 'macbook-mbr', 'location': 'master_bedroom'},

    '34:E6:D7:2B:CD:7C': {'device_type': 'ubuntu_laptop', 'oper_sys': '18.04',  'radio': 'abg', 'band': '5',
                          'state': 'None',
                          'address_type': 'None', 'port': 'None', 'ssid': 'None', 'rssi': 'None', 'ip': 'None',
                          'device_test_name': 'mac_book_1', 'name': 'palmer_Latitude-E5450',
                          'location': 'tbd'},

    'E4:58:E7:02:14:D6': {'device_type': 'Galaxy-Tab-A', 'oper_sys': 'Andoid 9', 'radio': 'abg', 'band': '5',
                          'state': 'None',
                          'address_type': 'fixed', 'port': 'None', 'ssid': 'None', 'rssi': 'None', 'ip': '192.168.1.65',
                          'device_test_name': 'fixed_taba', 'name': 'palmer_Latitude-E5450',
                          'location': 'tdb'},
    'F8:F1:B6:69:91:A3': {'device_type': 'Moto X', 'oper_sys': 'Android 5.1', 'radio': 'abg', 'band': '5',
                          'state': 'None',
                          'address_type': 'fixed', 'port': 'None', 'ssid': 'None', 'rssi': 'None', 'ip': '192.168.1.66',
                          'device_test_name': 'fixed_motox', 'name': 'palmer_Latitude-E5450', 'location': 'tbd'},
    'B8:D7:AF:AA:27:C3': {'device_type': 'Galaxy-Note8', 'oper_sys': 'Android 9', 'radio': 'abg', 'band': '5',
                          'state': 'None',
                          'address_type': 'fixed', 'port': 'None', 'ssid': 'None', 'rssi': 'None', 'ip': '192.168.1.67',
                          'device_test_name': 'fixed_note8', 'name': 'palmer_Latitude-E5450',
                          'location': 'tdb'},
    '8C:45:00:9F:82:9D': {'device_type': ' Galaxy-S9', 'oper_sys': 'Android 9', 'radio': 'abg', 'band': '5',
                          'state': 'None',
                          'address_type': 'fixed', 'port': 'None', 'ssid': 'None', 'rssi': 'None', 'ip': '192.168.1.67',
                          'device_test_name': 'fixed_s9', 'name': 'palmer_Latitude-E5450',
                          'location': 'tbd'},
}

# lsb_release -a to get ubuntu release

NON_DFS_CHANNELS = {36, 40, 44, 48, 149, 153, 157, 161, 165}
DFS_CHANNELS = {52, 56, 60, 64, 100, 104, 108, 112, 116, 132, 136, 140, 144}
ALL_BAND5_CHANNELS = {36, 40, 44, 48, 52, 56, 60, 64, 100, 104, 108, 112, 116, 132,
                      136, 140, 144, 149, 153, 157, 161, 165}


class GatewayClass:
    def __init__(self):
        self.magic = None
        self.up_time = None
        self.ip = None
        self.serial_number = None

    @staticmethod
    def email_test_results(text_file):
        now = datetime.today().isoformat()
        print('now')
        subject_title = 'Test results:' + str(now)
        print('subject title', subject_title)
        if text_file is None:
            pass
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

        try:

            with smtplib.SMTP('smtp.gmail.com', 587) as smtp_server:
                smtp_server.ehlo()
                smtp_server.starttls()
                smtp_server.login(gmail_user, gmail_password)
                smtp_server.send_message(msg)
                print('message sent successfully')
        except smtplib.SMTPException as e:
            print('failed to send email' + str(e))

# this version has no subject when received
#     def email_test_results_deprecated(self, text_file):
#         print('in email_test_results')
# #        gmail_password="arris123"
#         gmail_password = "1329brome"
#
#         gmail_user = 'leandertesthouse@gmail.com'
#         to = palmer@gmail.com'
#         sent_from = 'leandertesthouse:'
#         subject = 'Test results'
# #      body = "Results:" + channelResultContents
#         body = "Results:" + text_file
#         email_text = """
#         From:%s
#         To:%s
#         Subject:%s
#
#         %s
#         """ % (sent_from, to, subject, body)
#
#         try:
#             server = smtplib.SMTP('smtp.gmail.com', 587)
#             server.ehlo()
#             server.starttls()
#             server.login(gmail_user, gmail_password)
#             # email_text = 'Subject:{}\n\nbody'.format(subject)
#             server.sendmail(sent_from, to, email_text)
#             sleep(2)
#             server.quit()
#             print("im the email section ====================")
#         except smtplib.SMTPException as e:
#             print('failed to send email' + str(e))


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
        self.software_version = None
        self.mac_address = None
        self.last_reboot_time = None
        self.current_date = None
        self.hardware_version = None
        self.serial_number = None
        self.factory_reset = None
        # self.cli_rg_connected_clients_dict = {}
        # self.ui_rg_connected_clients_dict = {}
        self.ip_lan_connections_dict_cli = {}
        self.get_ui_system_information()
        self.device_access_code = nvg_info[self.serial_number]['device_access_code']
        print("in Nvg599Class__init")
        self.init_info = True
        self.mesh_connected_clents = {}

    def remote_webserver(self):
        pass

# pfp
    def set_fixed_ip_allocation(self):
        # dianostics_link = browser.find_element_by_link_text("Diagnostics")
        home_network_link = self.session.find_element_by_link_text("Home Network")
        home_network_link.click()
        sleep(2)
        wi_fi_link = self.session.find_element_by_link_text("IP Allocation")
        wi_fi_link.click()
        sleep(2)
        self.check_if_dac_required()
        test_mac = '5c:f8:a1:a6:6b:b2'
        # allocate_link = self.session.find_element_by_xpath("//tr//td//td[name()='Allocate_7c:64:56:b8:2f:30']/..")
        # allocate_link = self.session.find_element_by_xpath("//td[text()='Allocate_7c:64:56:b8:2f:30']")
        # allocate_link = self.session.find_element_by_xpath("//table[@class='grid table100']//tr[contains(td[2],
        # 'Allocate_7c:64:56:b8:2f:30')]")

        # allocate_link = self.session.find_element_by_xpath("//table[@class='grid table100']//td")
        table_rows = self.session.find_elements_by_xpath("//table[@class='grid table100']/tbody//tr")
        # table_rows = self.session.find_element_by_xpath("//table//r[@class='a']")

        print('row', table_rows[1].text)
        for tr in table_rows:
            # mac = tr.find_elements_by_xpath(".//td[1]/text()")
            name = tr.find_elements_by_xpath(".//td")[0].text
            mac = (tr.find_elements_by_xpath(".//td")[1].text).upper()
            status = tr.find_elements_by_xpath(".//td")[2].text
            allocation = tr.find_elements_by_xpath(".//td")[3].text
            action = tr.find_elements_by_xpath(".//td")[4].click()
            # wi_fi_link.navigate.refresh()
            alloc = self.session.find_element_by_id("alloc")
            # for fixed in alloc:

            for option in alloc.find_elements_by_tag_name('option'):
                print('option', option.text)
                # if option.text == "192.168.1.68":
                if "192.168.1.68" in option.text:
                    print('clicked 192.168.1.68')
                    option.click()
                    sleep(5)
                    submit = self.session.find_element_by_name("Save")
                    submit.click()
                    break

            exit()
            print('name:', name)
            print('mac:', mac)
            print('status:', status)
            print('allocation:', allocation)
            print('action type:', type(action))
            sleep(10)
            exit()

            # cells = tr.findAll('td')
            # print('cells:', cells)
            # print('cell1:', cells[1].get_text())
            # print('cell2:', cells[2].get_text())
            # print('cell3:', cells[3].get_text())
            # print('cell4:', cells[4].get_text())
        exit()

        soup = BeautifulSoup(self.session.page_source, 'html.parser')
        tables = soup.findChildren('table')
        # five tables on this page
        # table = tables[0]
        table_body_rows = tables[0].tbody.findAll('tr')

        for tr in table_body_rows:
            # print("table body row is", table_body_rows[0])
            #print("table body row is", tr)
            cells = tr.findAll('td')
            print('cells:',cells)
            print('cell1:', cells[1].get_text())
            print('cell2:', cells[2].get_text())
            print('cell3:', cells[3].get_text())
            print('cell4:', cells[4].get_text())
            # print('cell4:',cells[4].find(attrs={type : "submit"}))
            submit_button = cells[4].find(attrs={type: 'submit'})
            submit_button.click()
            # print('submit_button',submit_button)
            exit()

        exit()
        # table = soup.find("table100", {"class": "table100"})
        print("table body row is", table_body_rows[0])
        exit()

        for tr in table_rows:
            # we are looking at each row
            print('tr:', tr)
            cells = tr.find_all("td")
            exit()

            cells= tr.find_all("td")
            # print('cells:',cells)
            # print('cell1:',cells[1].text())
            # print('cell2:',cells[2].get_text())
            # print('cell3:',cells[3].get_text())
            # print('cell4:',cells[4].get_text())
            # exit()

            # print('cells[1]------', cells)
            # I am sure there is a better way to do this
            # we add a number to each row
            # probable a way
            i = 0
            mac_present_static_info = test_house_devices_static_info.get(wifi_ui_mac_present)
            if mac_present_static_info:
                # this is where we want to do everything
                my_row = tr.find("td")
                print('my_row', my_row)
                exit()

            for cell in cells:

                # parse all  the info from each row  if the mac is present in th satic_info_table
                # This means that we may have to update the UI IP to match the staitc IP in the table
                mac_present_static_info = test_house_devices_static_info.get(wifi_ui_mac_present)

                if i==1:
                    print('cell mac from ui is:>' + cell.text + '<')
                    wifi_ui_mac_present = (cell.text).upper()
                    print('wifi_mac_present:', wifi_ui_mac_present)
                    # if the key is present it means that the device is known.
                    for key in test_house_devices_static_info.keys():
                        # print('key:', key)
                        if key == wifi_ui_mac_present:
                            print('device_test_name', test_house_devices_static_info[wifi_ui_mac_present]['device_test_name'])
                            print('device_test_name', test_house_devices_static_info[wifi_ui_mac_present]['ip'])
                            test_house_ip = test_house_devices_static_info[wifi_ui_mac_present]['ip']
                            print('th', test_house_ip)
                    break
                i = i+1
            print('----------------------------------------')
    # '8C:45:00:9F:82:9D': {'device_type': ' Galaxy-S9', 'oper_sys': 'Android 9', 'radio': 'abg', 'band': '5',
    #                       'state': 'None',
    #                       'address_type': 'fixed', 'port': 'None', 'ssid': 'None', 'rssi': 'None', 'ip': '192.168.1.67',
    #                       'device_test_name': 'fixed_s9', 'name': 'palmer_Latitude-E5450',
    #                       'location': 'tbd'},

    def enable_guest_network_and_set_password_ssid(self):
        print('in enable_guest_network_and_set_password_ssid')
        # dianostics_link = browser.find_element_by_link_text("Diagnostics")
        home_network_link = self.session.find_element_by_link_text("Home Network")
        home_network_link.click()
        sleep(10)
        # resets_link = browser.find_element_by_link_text("Resets")
        wi_fi_link = self.session.find_element_by_link_text("Wi-Fi")
        wi_fi_link.click()
        sleep(2)
        self.check_if_dac_required()
        guest_id_enable = self.session.find_element_by_name("gssidenable")
        guest_id_enable.click()

        for option in guest_id_enable.find_elements_by_tag_name('option'):
            if option.text == "On":
                option.click()
        guest_id_password = self.session.find_element_by_id("gssidpassword")
        guest_id_password.send_keys("1111111111")

        submit = self.session.find_element_by_name("Save")
        submit.click()
        self.check_for_wifi_warning()

    """ I should use this function to get the information for a specific band /guest SSID
    This would make the test case logic  easier to follow"""
    def get_ui_ssid_info(self):
        # dianostics_link = browser.find_element_by_link_text("Diagnostics")
        home_network_link = self.session.find_element_by_link_text("Home Network")
        home_network_link.click()
        sleep(2)
        # resets_link = browser.find_element_by_link_text("Resets")
        wi_fi_link = self.session.find_element_by_link_text("Wi-Fi")
        wi_fi_link.click()
        sleep(2)
        self.check_if_dac_required()
        wi_fi_link = self.session.find_element_by_link_text("Advanced Options")
        wi_fi_link.click()

        band5_ssid_entry = self.session.find_element_by_name("tssidname")
        band5_ssid = band5_ssid_entry.get_attribute('value')

        band5_password_entry = self.session.find_element_by_name("tkey1")
        band5_password = band5_password_entry.get_attribute('value')

        guest_ssid_entry = self.session.find_element_by_name("gssidname2")
        guest_ssid = guest_ssid_entry.get_attribute('value')
        guest_password_entry = self.session.find_element_by_name("okey2")
        guest_password = guest_password_entry.get_attribute('value')

        band2_ssid_entry = self.session.find_element_by_name("ossidname")
        band2_ssid = band2_ssid_entry.get_attribute('value')
        band2_password_entry = self.session.find_element_by_name("okey1")
        band2_password = band2_password_entry.get_attribute('value')
        return band2_ssid, guest_ssid, band5_ssid, band2_password

    def set_ui_ssid(self, ssid_band5, ssid_guest, ssid_band2):
        # dianostics_link = browser.find_element_by_link_text("Diagnostics")
        home_network_link = self.session.find_element_by_link_text("Home Network")
        home_network_link.click()
        sleep(2)
        # resets_link = browser.find_element_by_link_text("Resets")
        wi_fi_link = self.session.find_element_by_link_text("Wi-Fi")
        wi_fi_link.click()
        sleep(2)
        self.check_if_dac_required()
        wi_fi_link = self.session.find_element_by_link_text("Advanced Options")
        wi_fi_link.click()
        sleep(2)
        if ssid_band5:
            print("changing band 5 SSID: " + ssid_band5)
            band5_ssid_entry = self.session.find_element_by_name("tssidname")
            self.session.find_element_by_name("tssidname").clear()
            band5_ssid_entry.send_keys(ssid_band5)
            submit = self.session.find_element_by_name("Save")
            submit.click()
            sleep(2)
            self.check_for_wifi_warning()
        else:
            print("ssid_band5 unchanged")

        if ssid_guest:
            print("changing guest SSID: " + ssid_guest)
            guest_ssid_entry = self.session.find_element_by_name("ossidname2")
            self.session.find_element_by_name("ossidname2").clear()
            guest_ssid_entry.send_keys(ssid_guest)
            submit = self.session.find_element_by_name("Save")
            submit.click()
            sleep(2)
            self.check_for_wifi_warning()
        else:
            print("ssid_guest unchanged")

        if ssid_band2:
            print("changing band 2 SSID: " + ssid_band2)
            band2_ssid_entry = self.session.find_element_by_name("ossidname")
            self.session.find_element_by_name("ossidname").clear()
            band2_ssid_entry.send_keys(ssid_band2)
            submit = self.session.find_element_by_name("Save")
            submit.click()
            sleep(2)
        self.check_for_wifi_warning()

    # we want to use the same session but the dict of connected devices is a temporary value subject to change
    def ui_get_device_list(self):
        global nvg_info
        global test_house_devices_static_info
        ui_rg_connected_clients_dict = {}
        print("in ui_get_device_list ")
        home_link = self.session.find_element_by_link_text("Device")
        home_link.click()
        status_link = self.session.find_element_by_link_text("Device List")
        status_link.click()
        # soup = BeautifulSoup(self.session.page_source, 'html.parser')
        soup = BeautifulSoup(self.session.page_source, 'lxml')
        table = soup.find("table", {"class": "table100"})

        for table_row in table.find_all("tr"):

            if table_row.td.has_attr('colspan'):
                # print('colspan ------------skipping-------:' + table_row.td.attrs['colspan'] + '\n\n')
                continue

            if table_row.th.text == "MAC Address":
                # print("table mac:" + table_row.td.text.strip() + ":test")

                mac = (table_row.td.text.strip()).upper()
                # if mac in test_house_devices_static_info:
                if 1 == 1:
                    ui_rg_connected_clients_dict[mac] = {}

                    table_row = table_row.find_next_sibling()
                    if table_row.th.text == "IPv4 Address / Name":
                        # print('name:' + (table_row.th.text).strip() + ':this is the ip and name' )
                        ip_and_name_str = table_row.td.text.strip()
                        ip_and_name_list = ip_and_name_str.split(" / ")
                        ip = ip_and_name_list[0]
                        ip = (str(ip).strip())
                        name = ip_and_name_list[1]
                        name = str(name)
                        # print('ip is:' + ip + ' : name is:' + name)
                        ui_rg_connected_clients_dict[mac]['ip'] = ip
                        ui_rg_connected_clients_dict[mac]['name'] = name

                    table_row = table_row.find_next_sibling()
                    if table_row.th.text == "Last Activity":
                        # print('Last Activty row :' + table_row.th.text.strip())
                        last_activity = table_row.td.text.strip()
                        # print('last activity:' + last_activity)
                        ui_rg_connected_clients_dict[mac]['last_activity'] = last_activity

                    table_row = table_row.find_next_sibling()
                    if table_row.th.text == "Status":
                        # print('status:' + (table_row.th.text).strip() + ':status')
                        status = table_row.td.text.strip()
                        # print('last status:' + status + ':end status')
                        ui_rg_connected_clients_dict[mac]['status'] = status

                    table_row = table_row.find_next_sibling()
                    if table_row.th.text == "Allocation":
                        # print('status:' + (table_row.th.text).strip() + ':status')
                        allocation = table_row.td.text.strip()
                        # print('allocation:' + allocation)
                        ui_rg_connected_clients_dict[mac]['allocation'] = allocation

                        table_row = table_row.find_next_sibling()
                    if table_row.th.text == "Connection Type":
                        connection_type = table_row.td.text
                        connection_type_str = str(connection_type)
                        # print('connecttype dtr before split:' + connection_type_str)

                        if re.search(r'.*Ethernet', connection_type_str) is not None:
                            ui_rg_connected_clients_dict[mac]['Connection_Type'] = 'Ethernet'
                            # print('connecttype ethernet: Ethernet')
                            continue

                        # sample input string
                        # Wi-Fi2.4 GHzType: HomeName: ATTqbrAnYs
                        if re.search(r'.*Wi-Fi(\w+)', connection_type_str) is not None:
                            wifi_band = re.search(r'.*Wi-Fi(\d\.?\d?)', connection_type_str)
                            # print('wifi_band:' + str(wifi_band.group(1)))
                            ui_rg_connected_clients_dict[mac]['wi_fi_band'] = wifi_band.group(1)

                        # to simplify parsing the Type is assumed to be Home
                        if re.search(r'.*HomeName:\s(\w+)', connection_type_str) is not None:
                            network_name = re.search(r'.*HomeName:\s(\w+)', connection_type_str)
                            # print('Network name:' + str(network_name.group(1)))
                            ui_rg_connected_clients_dict[mac]['network_name'] = network_name.group(1)

                        # print('td_con str:' + td_connection_string + '\n')
                        # img = table_row.td.find_all('img')
                        ui_rg_connected_clients_dict[mac]['strength'] = 'Not_present_in_ui'

                        for img in table_row.td.find_all('img'):
                            alt_entry = img['alt']
                            alt_entry_sting = str(alt_entry)
                            # alt_entry_sting = str(img)
                            alt_entry_list = alt_entry_sting.split()
                            # print('strength out of 5 is:' + alt_entry_list[1])
                            ui_rg_connected_clients_dict[mac]['strength'] = alt_entry_list[1]

        return ui_rg_connected_clients_dict

    def check_for_wifi_security_and_regular_warning(self):
        print('in check_for_wifi_warning ')
        # warning = self.session.find_element_by_name("ReturnWarned")
        # we get this warning every time so we don't have to check for no such exception
        try:
            wi_fi_warning = self.session.find_element_by_class_name("warning")
        except NoSuchElementException:
            return_string = "Wi-Fi Warning not detcted."
            return return_string

        if wi_fi_warning:
            print("Wi-Fi Warning displayed ")
            # submit = self.session.find_element_by_name("ReturnWarned")

            displayed_text = self.session.page_source
            sleep(5)
            if "Wi-Fi security that is not recommended." in displayed_text:
                submit = self.session.find_element_by_name("ReturnWarned")
                submit.click()
                return_string = "wi-fi security change... Continue"
                print("wi-fi security change... Continue")
                return return_string

            if "You have made a change to your Wi-Fi configuration" in displayed_text:
                submit = self.session.find_element_by_name("Continue")
                submit.click()
                return_string = "wi-fi regular warning change... Continue"
                print("wi-fi regular warning change... Continue")
                return return_string

# I think this shoudl only be used for the password testcases
    def check_for_wifi_warning(self):
        print('in check_for_wifi_warning ')
        # warning = self.session.find_element_by_name("ReturnWarned")
        # we get this warning every time so we don't have to check for no such exception
        try:
            wi_fi_warning = self.session.find_element_by_class_name("warning")
        except NoSuchElementException:
            return_string = "No changes detected. Save not performed"
            return return_string

        if wi_fi_warning:
            print("got wifi warning")
            # submit = self.session.find_element_by_name("ReturnWarned")
            submit = self.session.find_element_by_name("Continue")
            submit.click()
            sleep(5)
            return_string = "password changed successfully"

            displayed_text = self.session.page_source
            sleep(5)
            if "The Password is too long" in displayed_text:
                submit = self.session.find_element_by_name("Cancel")
                print('Password too long, Cancelling change')
                submit.click()
                return_string = "password too long"
                return return_string
            if "must contain 8-63" in displayed_text:
                submit = self.session.find_element_by_name("Cancel")
                print('Password length not in range 8-63')
                submit.click()
                return_string = "password length not in range 8-63"
                return return_string
            return return_string
            #
            #
            # print('text' + displayed_text)
            # exit()
            # elem = self.session.find_elements_by_xpath("//*[@id='content-sub']
            # /div[3]/form/table[2]/tbody/tr[5]/th/label/em")
            # print('No password xxxx - Continuing' + str(elem[0]))
            # print('No password too short warning - Continuing' + str(elem[0]))
            # try:
            #     # self.session.find_elements_by_xpath("//*[contains(text(), 'must contain 8-63')]")
            #     #elem = self.session.find_elements_by_xpath("//label[@for='password][contains(text(),
            #     'must contain 8-63'")
            #     #elem = self.session.find_element_by_xpath("//*label[@for='password]")
            #     elem = self.session.find_elements_by_xpath
            #     ("//*[@id='content-sub']/div[3]/form/table[2]/tbody/tr[5]/th/label/em")
            #     #wi_fi_warning = self.session.find_element_by_class_name("special bad")
            #
            #     #elem = self.session.find_element_by_xpath("//*id="content-sub"]
            #     /div[3]/form/table[2]/tbody/tr[5]/th/label/em")
            #
            #     print('elem' + str(elem))
            #     exit()
            #     print('special_bad_warning too short' + wi_fi_warning)
            #     submit = self.session.find_element_by_name("Cancel")
            #     print('Password too short, Cancelling change')
            #     submit.click()
            #     return_string = "password too short"
            #     return return_string
            # except NoSuchElementException:
            #     print('No password too short warning - Continuing' + str(elem))
            #
            # return return_string
            # #   print('No Input errors displayed- Continuing')
            # #if(self.session.page_source().contains("too long")):
            # #    print("too long")
            # try:
            #    special_bad_warning = self.session.find_element_by_class_name('special bad')
            #   if special_bad_warning:
            #       print('special_bad_warning' + special_bad_warning)
            #
            # except NoSuchElementException:
            #   print('No Input errors displayed- Continuing')

            #            submit = self.session.find_element_by_name("Continue")
            #           submit.click()
            #          sleep(2)
            # else:
            #   try:
            #       special_bad_warning = self.session.find_element_by_class_name("special bad").getText()
            #       if special_bad_warning:
            #          print('special_bad_warning' + special_bad_warning)
            #  except NoSuchElementException:
            #      print('No Input errors displayed- Continuing')

    def update_rg(self, update_bin_file):
        print('in update_rg')
        print("in ui_get_device_list ")
        home_link = self.session.find_element_by_link_text("Diagnostics")
        home_link.click()
        status_link = self.session.find_element_by_link_text("Update")
        status_link.click()
        self.check_if_dac_required()
        sleep(5)
        # firm_ware_element = self.session.find_element_by_name("uploadfile")
        firm_ware_element = self.session.find_element_by_xpath("//*[@id='firmware']")
        # session = webdriver.Chrome()
        firm_ware_element.send_keys(update_bin_file)
        submit = self.session.find_element_by_name("Update")
        submit.click()

        start = time.time()
        print("starting upgrade timer:" + str(start))
        loop = 1
        while loop == 1:
            try:
                test_req = urllib.request.Request("http://192.168.1.254/")
                urllib.request.urlopen(test_req, timeout=60)
                # response.read().decode("utf-8", 'ignore')
                end = time.time()
                print("Duration timer:", str(end - start))
                sleep(20)
                break
            # except:
            # need to check if this works
            except TimeoutError:
                print('Not ready, sleeping 10 seconds')
                sleep(10)
                print('time' + str(time.time()))
                continue

            except (HTTPError, URLError) as e:
                print('HTTP Error: ' + str(e))
                sleep(10)
                print('time' + str(time.time()))
                continue
            except timeout:
                print('Socket timeout error')

        end = time.time()
        print("upgrade duration in seconds:", round(end - start))
        sleep(2)

        return "Upgrade compete"

    def check_if_dac_required(self):
        try:
            # dac_access_challenge = self.session.find_element_by_link_text("Forgot your Access Code?")
            self.session.find_element_by_link_text("Forgot your Access Code?")
            print('we found the request for DAC')
            print('sending DAC', self.device_access_code)
            dac_entry = self.session.find_element_by_id("password")
            dac_entry.send_keys(self.device_access_code)
            submit = self.session.find_element_by_name("Continue")
            submit.click()
            sleep(4)
        except NoSuchElementException:
            print('DAC challenge not displayed- Continuing')
    #        # browser.find_element_by_xpath("//*[@id='main-content']/div[2]/div[2]/div/h1.text")

    def check_if_wifi_warning_displayed(self):
        print('in check_if_wifi_warning_displayed')
        try:
            sleep(4)
            self.session.find_element_by_xpath('//*[@id="content-sub"]/div[1]/h1')
            print('WiFi warning displayed')
            print('Clicking on Continue')
            submit = self.session.find_element_by_name("Continue")
            submit.click()
            sleep(10)
        except NoSuchElementException:
            print('Wi-Fi warning not displayed - Continuing')
        try:
            sleep(4)
            self.session.find_element_by_xpath('//*[@id="error-message-text"]')
            print('Changes Saved')
        except NoSuchElementException:
            print('No save confirmation')
#         print("in cli_sh_wi_clients")
#         self.telnet_cli_session = self.login_nvg_599_cli()
#         self.telnet_cli_session.sendline("show wi clients")
#         self.telnet_cli_session.expect('OCKED>')
#         show_wi_client_str = self.telnet_cli_session.before
#         self.telnet_cli_session.close()
#         print('------------------------------------------------------\n')
#         print('------------------------------------------------------\n')
#         # dividing on macs
#         wi_reg_ex = re.compile(r'(?:[0-9a-fA-F]:?){12}.*?\n.*\n.*\n.*\n')
#         client_string_list = re.findall(wi_reg_ex, show_wi_client_str)
#
#         number_of_entries = len(client_string_list)
#         print("The list has :", number_of_entries)
#
#         client_entries = range(0, number_of_entries)
#
#         for client_list_entry in client_entries:
#             print("entry:", client_string_list[client_list_entry])
#             print("-------------------------")
#
#             client_string_list_split = client_string_list[client_list_entry].split()
#
#             mac = client_string_list_split[0]
#             mac = mac.upper()
#             mac = mac[:-1]
#             print('modified 2g mac', mac)
#             cli_rg_connected_clients_dict = {}
#             if mac in test_house_devices_static_info:
#                 # self.cli_rg_connected_clients_dict[mac] = {}
#                 cli_rg_connected_clients_dict[mac] = {}
#
#                 print('mac found in lab dict', mac)
#
#                 # self.cli_rg_connected_clients_dict[mac]['band'] = test_house_devices_static_info[mac]['band']
#                 # print('setting band to:',  self.cli_rg_connected_clients_dict[mac]['band'])
#
#                 cli_rg_connected_clients_dict[mac]['band'] = test_house_devices_static_info[mac]['band']
#                 print('setting band to:', cli_rg_connected_clients_dict[mac]['band'])
#
#
#                 if re.search(r'.*State=(\w+),', client_string_list[client_list_entry]) is not None:
#                     wi_state_search = re.search(r'.*State=(\w+)', client_string_list[client_list_entry])
#                     # self.cli_rg_connected_clients_dict[mac]['wi_state'] = wi_state_search.group(1)
#                     cli_rg_connected_clients_dict[mac]['wi_state'] = wi_state_search.group(1)
#                     print('Seting wi_state to ', wi_state_search.group(1))
#                 else:
#                     # self.cli_rg_connected_clients_dict[mac]['wi_state'] = "Not found or State value missing"
#                     cli_rg_connected_clients_dict[mac]['wi_state'] = "Not found or State value missing"
#                     print('Seting wi_state to Not Found or value missing ')
#
#                 if re.search(r'.*IP:\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',
#                     client_string_list[client_list_entry]) is not None:
#                     wi_state_search = re.search(r'.*IP:\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',
#                     client_string_list[client_list_entry])
#                     # self.cli_rg_connected_clients_dict[mac]['ip'] = wi_state_search.group(1)
#                     cli_rg_connected_clients_dict[mac]['ip'] = wi_state_search.group(1)
#                     print('Seting ip to ', wi_state_search.group(1))
#                 else:
#                     #self.cli_rg_connected_clients_dict[mac]['ip'] = "Not found or State value missing"
#                     cli_rg_connected_clients_dict[mac]['ip'] = "Not found or State value missing"
#                     print('Seting ip to Not Found or value missing ')
#
#                 if re.search(r'.*SSID=(\w+)', client_string_list[client_list_entry]) is not None:
#                     wi_state_search = re.search(r'.*SSID=(\w+)', client_string_list[client_list_entry])
#                     #self.cli_rg_connected_clients_dict[mac]['ip'] = wi_state_search.group(1)
#                     cli_rg_connected_clients_dict[mac]['ip'] = wi_state_search.group(1)
#                     print('Seting SSID to ', wi_state_search.group(1))
#                 else:
#                     # self.cli_rg_connected_clients_dict[mac]['ssid'] = "Not found or State value missing"
#                     cli_rg_connected_clients_dict[mac]['ssid'] = "Not found or State value missing"
#                     print('Seting ssid to Not Found or value missing ')
#
#                 if re.search(r'.*PSMod=(\w+)', client_string_list[client_list_entry]) is not None:
#                     wi_state_search = re.search(r'.*PSMod=(\w+)', client_string_list[client_list_entry])
#                     # self.cli_rg_connected_clients_dict[mac]['psmod'] = wi_state_search.group(1)
#                     cli_rg_connected_clients_dict[mac]['psmod'] = wi_state_search.group(1)
#                     print('Seting psmod to ', wi_state_search.group(1))
#                 else:
#                     # self.cli_rg_connected_clients_dict[mac]['psmod'] = "Not found or value missing"
#                     cli_rg_connected_clients_dict[mac]['psmod'] = "Not found or value missing"
#                     print('Seting psmod to Not Found or value missing ')
#
#                 if re.search(r'.*NMod=(\w+)', client_string_list[client_list_entry]) is not None:
#                     wi_state_search = re.search(r'.*NMod=(\w+)', client_string_list[client_list_entry])
#                     # self.cli_rg_connected_clients_dict[mac]['nmod'] = wi_state_search.group(1)
#                     cli_rg_connected_clients_dict[mac]['nmod'] = wi_state_search.group(1)
#                     print('Seting psmod to ', wi_state_search.group(1))
#                 else:
#                     # self.cli_rg_connected_clients_dict[mac]['nmod'] = "Not found or value missing"
#                     cli_rg_connected_clients_dict[mac]['nmod'] = "Not found or value missing"
#                     print('Seting nmmod to Not Found or value missing ')
#
#                 if re.search(r'.*WMMEn=(\w+)', client_string_list[client_list_entry]) is not None:
#                     wi_state_search = re.search(r'.*WMMEn=(\w+)', client_string_list[client_list_entry])
#                     # self.cli_rg_connected_clients_dict[mac]['wmmen'] = wi_state_search.group(1)
#                     self.cli_rg_connected_clients_dict[mac]['wmmen'] = wi_state_search.group(1)
#                     print('Seting psmod to ', wi_state_search.group(1))
#                 else:
#                     # self.cli_rg_connected_clients_dict[mac]['wmmen'] = "Not found or value missing"
#                     cli_rg_connected_clients_dict[mac]['wmmen'] = "Not found or value missing"
#                     print('Seting wmmen to Not Found or value missing ')
#
#                 if re.search(r'.*Rate=(\w+\s\w+)', client_string_list[client_list_entry]) is not None:
#                     wi_state_search = re.search(r'.*Rate=(\w+\s\w+)', client_string_list[client_list_entry])
#                     # self.cli_rg_connected_clients_dict[mac]['wmmen'] = wi_state_search.group(1)
#                     cli_rg_connected_clients_dict[mac]['wmmen'] = wi_state_search.group(1)
#                     print('Seting rate to ', wi_state_search.group(1))
#                 else:
#                     # self.cli_rg_connected_clients_dict[mac]['rate'] = "Not found or value missing"
#                     self.cli_rg_connected_clients_dict[mac]['rate'] = "Not found or value missing"
#                     print('Seting rate to Not Found or value missing ')
#
#                 if re.search(r'.*ON\sfor\s(\w+\s\w+)', client_string_list[client_list_entry]) is not None:
#                     wi_state_search = re.search(r'.*ON\sfor\s(\w+\s\w+)', client_string_list[client_list_entry])
#                     # self.cli_rg_connected_clients_dict[mac]['ontime'] = wi_state_search.group(1)
#                     cli_rg_connected_clients_dict[mac]['ontime'] = wi_state_search.group(1)
#                     print('Seting ontime to ', wi_state_search.group(1))
#                 else:
#                     # self.cli_rg_connected_clients_dict[mac]['ontime'] = "Not found or value missing"
#                     cli_rg_connected_clients_dict[mac]['ontime'] = "Not found or value missing"
#
#                     print('Seting On Time to Not Found or value missing ')
#
#                 if re.search(r'.*TxPkt=(\w+)', client_string_list[client_list_entry]) is not None:
#                     wi_state_search = re.search(r'.*TxPkt=(\w+)', client_string_list[client_list_entry])
#                     # self.cli_rg_connected_clients_dict[mac]['txpkt'] = wi_state_search.group(1)
#                     cli_rg_connected_clients_dict[mac]['txpkt'] = wi_state_search.group(1)
#                     print('Seting txpkt to ', wi_state_search.group(1))
#                 else:
#                     # self.cli_rg_connected_clients_dict[mac]['txpkt'] = "Not found or value missing"
#                     cli_rg_connected_clients_dict[mac]['txpkt'] = "Not found or value missing"
#                     print('Seting txpkt to Not Found or value missing ')
#
#                 if re.search(r'.*TxErr=(\w+)', client_string_list[client_list_entry]) is not None:
#                     wi_state_search = re.search(r'.*TxErr=(\w+)', client_string_list[client_list_entry])
#                     # self.cli_rg_connected_clients_dict[mac]['txerr'] = wi_state_search.group(1)
#                     cli_rg_connected_clients_dict[mac]['txerr'] = wi_state_search.group(1)
#                     print('Seting txerr to ', wi_state_search.group(1))
#                 else:
#                     # self.cli_rg_connected_clients_dict[mac]['txerr'] = "Not found or value missing"
#                     cli_rg_connected_clients_dict[mac]['txerr'] = "Not found or value missing"
#                     print('Seting txerr to Not Found or value missing ')
#
#                 if re.search(r'.*RxUni=(\w+)', client_string_list[client_list_entry]) is not None:
#                     wi_state_search = re.search(r'.*RxUni=(\w+)', client_string_list[client_list_entry])
#                     # self.cli_rg_connected_clients_dict[mac]['rxuni'] = wi_state_search.group(1)
#                     cli_rg_connected_clients_dict[mac]['rxuni'] = wi_state_search.group(1)
#                     print('Seting rxuni to ', wi_state_search.group(1))
#                 else:
#                     # self.cli_rg_connected_clients_dict[mac]['rxuni'] = "Not found or value missing"
#                     cli_rg_connected_clients_dict[mac]['rxuni'] = "Not found or value missing"
#                     print('Seting rxuni to Not Found or value missing ')
#
#                 if re.search(r'.*RxMul=(\w+)', client_string_list[client_list_entry]) is not None:
#                     wi_state_search = re.search(r'.*RxMul=(\w+)', client_string_list[client_list_entry])
#                     # self.cli_rg_connected_clients_dict[mac]['rxmul'] = wi_state_search.group(1)
#                     cli_rg_connected_clients_dict[mac]['rxmul'] = wi_state_search.group(1)
#                     print('Seting rxmul to ', wi_state_search.group(1))
#                 else:
#                     # self.cli_rg_connected_clients_dict[mac]['rxuni'] = "Not found or value missing"
#                     cli_rg_connected_clients_dict[mac]['rxuni'] = "Not found or value missing"
#                     print('Seting rxmul to Not Found or value missing ')
#
#                 if re.search(r'.*RxErr=(\w+)', client_string_list[client_list_entry]) is not None:
#                     wi_state_search = re.search(r'.*RxErr=(\w+)', client_string_list[client_list_entry])
#                     # self.cli_rg_connected_clients_dict[mac]['rxerr'] = wi_state_search.group(1)
#                     cli_rg_connected_clients_dict[mac]['rxerr'] = wi_state_search.group(1)
#                     print('Seting rxerr to ', wi_state_search.group(1))
#                 else:
#                     # self.cli_rg_connected_clients_dict[mac]['rxerr'] = "Not found or value missing"
#                     cli_rg_connected_clients_dict[mac]['rxerr'] = "Not found or value missing"
#                     print('Seting rxerr to Not Found or value missing ')
#
#                 if re.search(r'.*RSSI=-(\w+)', client_string_list[client_list_entry]) is not None:
#                     wi_state_search = re.search(r'.*RSSI=-(\w+)', client_string_list[client_list_entry])
#                     # self.cli_rg_connected_clients_dict[mac]['rxerr'] = wi_state_search.group(1)
#                     cli_rg_connected_clients_dict[mac]['rxerr'] = wi_state_search.group(1)
#                     print('Seting rssi to ', wi_state_search.group(1))
#                 else:
#                     # self.cli_rg_connected_clients_dict[mac]['rssi'] = "Not found or value missing"
#                     cli_rg_connected_clients_dict[mac]['rssi'] = "Not found or value missing"
#                     print('Seting rssi to Not Found or value missing ')
#
#         return cli_rg_connected_clients_dict
#
#         # show_wi_clients_reg_ex = re.compile(r'.*State=(\w+).*IP:\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).
    #         *SSID=(\w+).*PSMod=(\w+)?,.*NMode=(\w+)?,.*WMMEn=(\w+)?,.*Rate=(\w+\s\w+).*ON\sfor\s(\w+\s\w+)?.
    #         *TxPkt=(\w+).*TxErr=(\w+).*RxUni=(\w+).*RxMul=(\w+).*RxErr=(\w+).*RSSI=-(\w+)?', re.DOTALL)
#         # show_wi_clients_reg_ex = re.compile(r'.*State=(\w+).*IP:(\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(\w+).
    #         *RxUni=(\w+).*RxMul=(\w+).*RxErr=(\w+).*RSSI=-(\w+)', re.DOTALL)
#         # not sure if I need to return this if the dictionary is alread bound to the instance
#         return cli_rg_connected_clients_dict

    # @staticmethod  not static because we use the UI
    def get_airties_ip(self, airties_test_name):
        # test_device_mac = None
        current_ui_rg_connected_clients_dict = self.ui_get_device_list()
        # for key, value in current_ui_rg_connected_clients_dict.items():
        #    print('mac in ui_rg_connected_clients_dict>' + key + '<')
        # print(type(key))
        #    print('entry: ' + current_ui_rg_connected_clients_dict[key]['ip'] )
        # print('ip is :' + current_ui_rg_connected_clients_dict[key])
        airties_ip = None
        for key, value in test_house_devices_static_info.items():
            if test_house_devices_static_info[key]['device_test_name'] == airties_test_name:
                print('mac isqq>' + key + '<')
                test_device_mac = key
                # print('ip is :' + current_ui_rg_connected_clients_dict[test_device_mac]['ip'])
                # print(type(key))
                # print('test_house_static_info>' + key + '<')

                # print('ip is :' + current_ui_rg_connected_clients_dict['88:41:FC:86:64:D7'])
                # print('ip is :' + str(current_ui_rg_connected_clients_dict[key]['ip']))
                if test_device_mac in current_ui_rg_connected_clients_dict:
                    print('ip is :' + str(current_ui_rg_connected_clients_dict[test_device_mac]['ip']) + ' Name: '
                          + test_house_devices_static_info[key]['device_test_name'])
                    return current_ui_rg_connected_clients_dict[test_device_mac]['ip']
                else:
                    print('Device not present in UI device list')
                    return None

                    # for key, value in current_ui_rg_connected_clients_dict.items():
            # else:
                # print('not this one: ' + test_house_devices_static_info[key]['device_test_name'])
            #    airties_ip = None

            # or key, value in current_ui_rg_connected_clients_dict.items():
                # print('key:' + str(key) + ' the value:' + str(value))
            #    print('test name:' + current_ui_rg_connected_clients_dict[key]['test_name'])
        print('Name not present in test house device dictionary')
        return airties_ip

    @staticmethod
    def cli_sh_wi_all_clients():
        global test_house_devices_static_info
        print("In cli_sh_wi_all_clients")
        # Nvg599Class
        # self.telnet_cli_session = self.login_nvg_599_cli()
        telnet_cli_session = Nvg599Class.static_login_nvg_599_cli()

        telnet_cli_session.sendline("show wi clients")
        telnet_cli_session.expect('OCKED>')
        show_wi_client_str = telnet_cli_session.before
        cli_rg_connected_clients_dict = {}
        g2_and_g5_list = show_wi_client_str.split('5.0 GHz')
        print('g2_list:' + g2_and_g5_list[0])
        print('g5_list:' + g2_and_g5_list[1])
        telnet_cli_session.close()
        print('------------------------------------------------------\n')
        # dividing on macs
        wi_reg_ex = re.compile(r'(?:[0-9a-fA-F]:?){12}.*?\n.*\n.*\n.*\n')
        client_string_list = re.findall(wi_reg_ex, show_wi_client_str)

        total_number_of_entries = len(client_string_list)
        print("The  whole list has :", total_number_of_entries)

        g2_client_string_list = re.findall(wi_reg_ex, g2_and_g5_list[0])
        g5_client_string_list = re.findall(wi_reg_ex, g2_and_g5_list[1])

        number_of_entries_2g = len(g2_client_string_list)
        print("The 2G list has :", number_of_entries_2g)

        number_of_entries_5g = len(g5_client_string_list)
        print("The 5G list has :", number_of_entries_5g)

        # client_entries_2G = range(0, number_of_entries_2G)
        client_entries = range(0, total_number_of_entries)
        # client_string_list = re.findall(wi_reg_ex, g2_and_g5_list[0])

        for client_list_entry in client_entries:
            print("entry:", client_string_list[client_list_entry])
            print("-------------------------")

            client_string_list_split = client_string_list[client_list_entry].split()

            mac = client_string_list_split[0]
            mac = mac.upper()
            mac = mac[:-1]
            print('modified 2g mac', mac)

            cli_rg_connected_clients_dict[mac] = {}
            print('mac:', mac)
            print('g2_client_str_list:' + str(g2_client_string_list))
            print('client_list_entry' + str(client_string_list[client_list_entry]))
            if client_string_list[client_list_entry] in g2_client_string_list:
                cli_rg_connected_clients_dict[mac]['connected_band'] = '2.4 HGz'
                print('setting band to 2.4GHz')
            else:
                cli_rg_connected_clients_dict[mac]['connected_band'] = '5.0 HGz'
                print('setting band to 5.0 GHz')

            if re.search(r'.*State=(\w+),', client_string_list[client_list_entry]) is not None:
                wi_state_search = re.search(r'.*State=(\w+)', client_string_list[client_list_entry])
                cli_rg_connected_clients_dict[mac]['wi_state'] = wi_state_search.group(1)
                print('Seting wi_state to ', wi_state_search.group(1))
            else:
                cli_rg_connected_clients_dict[mac]['wi_state'] = "Not found or State value missing"
                print('Seting wi_state to Not Found or value missing ')

            if re.search(r'.*IP:\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',
                         client_string_list[client_list_entry]) is not None:
                wi_state_search = re.search(r'.*IP:\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',
                                            client_string_list[client_list_entry])
                cli_rg_connected_clients_dict[mac]['ip'] = wi_state_search.group(1)
                print('Seting ip to ', wi_state_search.group(1))
            else:
                cli_rg_connected_clients_dict[mac]['ip'] = "Not found or State value missing"
                print('Seting ip to Not Found or value missing ')

            if re.search(r'.*SSID=(\w+)', client_string_list[client_list_entry]) is not None:
                wi_state_search = re.search(r'.*SSID=(\w+)', client_string_list[client_list_entry])
                cli_rg_connected_clients_dict[mac]['ip'] = wi_state_search.group(1)
                print('Seting SSID to ', wi_state_search.group(1))
            else:
                cli_rg_connected_clients_dict[mac]['ssid'] = "Not found or State value missing"
                print('Seting ssid to Not Found or value missing ')

            if re.search(r'.*PSMod=(\w+)', client_string_list[client_list_entry]) is not None:
                wi_state_search = re.search(r'.*PSMod=(\w+)', client_string_list[client_list_entry])
                cli_rg_connected_clients_dict[mac]['psmod'] = wi_state_search.group(1)
                print('Seting psmod to ', wi_state_search.group(1))
            else:
                cli_rg_connected_clients_dict[mac]['psmod'] = "Not found or value missing"
                print('Seting psmod to Not Found or value missing ')

            if re.search(r'.*NMod=(\w+)', client_string_list[client_list_entry]) is not None:
                wi_state_search = re.search(r'.*NMod=(\w+)', client_string_list[client_list_entry])
                cli_rg_connected_clients_dict[mac]['nmod'] = wi_state_search.group(1)
                print('Seting psmod to ', wi_state_search.group(1))
            else:
                cli_rg_connected_clients_dict[mac]['nmod'] = "Not found or value missing"
                print('Seting nmmod to Not Found or value missing ')

            if re.search(r'.*WMMEn=(\w+)', client_string_list[client_list_entry]) is not None:
                wi_state_search = re.search(r'.*WMMEn=(\w+)', client_string_list[client_list_entry])
                cli_rg_connected_clients_dict[mac]['wmmen'] = wi_state_search.group(1)
                print('Seting psmod to ', wi_state_search.group(1))
            else:
                cli_rg_connected_clients_dict[mac]['wmmen'] = "Not found or value missing"
                print('Seting wmmen to Not Found or value missing ')

            if re.search(r'.*Rate=(\w+\s\w+)', client_string_list[client_list_entry]) is not None:
                wi_state_search = re.search(r'.*Rate=(\w+\s\w+)', client_string_list[client_list_entry])
                cli_rg_connected_clients_dict[mac]['wmmen'] = wi_state_search.group(1)
                print('Seting rate to ', wi_state_search.group(1))
            else:
                cli_rg_connected_clients_dict[mac]['rate'] = "Not found or value missing"
                print('Seting rate to Not Found or value missing ')

            if re.search(r'.*ON\sfor\s(\w+\s\w+)', client_string_list[client_list_entry]) is not None:
                wi_state_search = re.search(r'.*ON\sfor\s(\w+\s\w+)', client_string_list[client_list_entry])
                cli_rg_connected_clients_dict[mac]['ontime'] = wi_state_search.group(1)
                print('Seting ontime to ', wi_state_search.group(1))
            else:
                cli_rg_connected_clients_dict[mac]['ontime'] = "Not found or value missing"
                print('Seting On Time to Not Found or value missing ')

            if re.search(r'.*TxPkt=(\w+)', client_string_list[client_list_entry]) is not None:
                wi_state_search = re.search(r'.*TxPkt=(\w+)', client_string_list[client_list_entry])
                cli_rg_connected_clients_dict[mac]['txpkt'] = wi_state_search.group(1)
                print('Seting txpkt to ', wi_state_search.group(1))
            else:
                cli_rg_connected_clients_dict[mac]['txpkt'] = "Not found or value missing"
                print('Seting txpkt to Not Found or value missing ')

            if re.search(r'.*TxErr=(\w+)', client_string_list[client_list_entry]) is not None:
                wi_state_search = re.search(r'.*TxErr=(\w+)', client_string_list[client_list_entry])
                cli_rg_connected_clients_dict[mac]['txerr'] = wi_state_search.group(1)
                print('Seting txerr to ', wi_state_search.group(1))
            else:
                cli_rg_connected_clients_dict[mac]['txerr'] = "Not found or value missing"
                print('Seting txerr to Not Found or value missing ')

            if re.search(r'.*RxUni=(\w+)', client_string_list[client_list_entry]) is not None:
                wi_state_search = re.search(r'.*RxUni=(\w+)', client_string_list[client_list_entry])
                cli_rg_connected_clients_dict[mac]['rxuni'] = wi_state_search.group(1)
                print('Seting rxuni to ', wi_state_search.group(1))
            else:
                cli_rg_connected_clients_dict[mac]['rxuni'] = "Not found or value missing"
                print('Seting rxuni to Not Found or value missing ')

            if re.search(r'.*RxMul=(\w+)', client_string_list[client_list_entry]) is not None:
                wi_state_search = re.search(r'.*RxMul=(\w+)', client_string_list[client_list_entry])
                cli_rg_connected_clients_dict[mac]['rxmul'] = wi_state_search.group(1)
                print('Seting rxmul to ', wi_state_search.group(1))
            else:
                cli_rg_connected_clients_dict[mac]['rxuni'] = "Not found or value missing"
                print('Seting rxmul to Not Found or value missing ')

            if re.search(r'.*RxErr=(\w+)', client_string_list[client_list_entry]) is not None:
                wi_state_search = re.search(r'.*RxErr=(\w+)', client_string_list[client_list_entry])
                cli_rg_connected_clients_dict[mac]['rxerr'] = wi_state_search.group(1)
                print('Seting rxerr to ', wi_state_search.group(1))
            else:
                cli_rg_connected_clients_dict[mac]['rxerr'] = "Not found or value missing"
                print('Seting rxerr to Not Found or value missing ')

            if re.search(r'.*RSSI=-(\w+)', client_string_list[client_list_entry]) is not None:
                wi_state_search = re.search(r'.*RSSI=-(\w+)', client_string_list[client_list_entry])
                cli_rg_connected_clients_dict[mac]['rxerr'] = wi_state_search.group(1)
                print('Seting rssi to ', wi_state_search.group(1))
            else:
                cli_rg_connected_clients_dict[mac]['rssi'] = "Not found or value missing"
                print('Seting rssi to Not Found or value missing ')
                # show_wi_clients_reg_ex = re.compile(r'.*State=(\w+).*IP:\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).
                # *SSID=(\w+).*PSMod=(\w+)?,.*NMode=(\w+)?,.*WMMEn=(\w+)?,.*Rate=(\w+\s\w+).*ON\sfor\s(\w+\s\w+)?.
                # *TxPkt=(\w+).*TxErr=(\w+).*RxUni=(\w+).*RxMul=(\w+).*RxErr=(\w+).*RSSI=-(\w+)?', re.DOTALL)
                # show_wi_clients_reg_ex = re.compile(r'.*State=(\w+).*IP:(\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(\w+).
                # *RxUni=(\w+).*RxMul=(\w+).*RxErr=(\w+).*RSSI=-(\w+)', re.DOTALL)
            # not sure if I need to return this if the dictionary is alread bound to the instance
            return cli_rg_connected_clients_dict

    @staticmethod
    def factory_test():
        loop = 1
        start = time.time()
        while loop == 1:
            try:
                test_req = urllib.request.Request("http://192.168.1.254/")
                urllib.request.urlopen(test_req, timeout=120)
                end = time.time()
                print("Duration timer:", str(end - start))
                break
            # except:
            # need to check if this works
            except TimeoutError:
                print('Not ready, sleeping 10 seconds')
                sleep(10)
                print('time' + str(time.time()))
                continue

            except HTTPError as e:
                print('HTTP Error: ' + str(e))
                sleep(10)
                print('time' + str(time.time()))
                continue

            except URLError as e:
                print('URL Error: ' + str(e))
                sleep(10)
                print('time' + str(time.time()))
                continue
        print('done')
    # @staticmethod
    # def factory_reset_rg(self, rg_url="http://192.168.1.254/cgi-bin/home.ha"):
    # we have to assume that the default RG IP is 192.168.1.254

    def factory_reset_rg(self):
        # the default is the usual default RG IP
        self.factory_reset = 1
        # url = 'http://192.168.1.254/'
        # browser = webdriver.Chrome()
        # browser.get(url)
        # browser.find_element_by_xpath("//*[@id='main-content']/div[2]/div[2]/div/h1.text")
        # dianostics_link = browser.find_element_by_link_text("Diagnostics")
        dianostics_link = self.session.find_element_by_link_text("Diagnostics")
        dianostics_link.click()
        sleep(2)
        # resets_link = browser.find_element_by_link_text("Resets")
        resets_link = self.session.find_element_by_link_text("Resets")
        resets_link.click()
        sleep(2)
        self.check_if_dac_required()
        factory_reset = self.session.find_element_by_name("Reset")
        factory_reset.click()
        sleep(5)
        print('Final screen')
        factory_reset2 = self.session.find_element_by_name("Reset")
        factory_reset2.click()
        # self.session.find_element_by_css_selector(".cssbtn[value='Reset Device...']").click()
        print('Resetting to factory defaults now')
        sleep(10)
        start = time.time()
        print("starting timer:" + str(start))
        loop = 1
        while loop == 1:
            try:
                test_req = urllib.request.Request("http://192.168.1.254/")
                urllib.request.urlopen(test_req, timeout=60)
                # response.read().decode("utf-8", 'ignore')
                end = time.time()
                print("Duration timer:", str(end - start))
                sleep(20)
                break
            # except:
            # need to check if this works
            except TimeoutError:
                print('Not ready, sleeping 10 seconds')
                sleep(10)
                print('time' + str(time.time()))
                continue

            except (HTTPError, URLError) as e:
                print('HTTP Error: ' + str(e))
                sleep(10)
                print('time' + str(time.time()))
                continue
            except timeout:
                print('Socket timeout error')

                # except URLError as e:
                #   print('URL Error: ' + str(e))
                #   sleep(10)
                #   print('time' + str(time.time()))
                #   continue

        end = time.time()
        print("in outer duration in seconds:", end - start)
        #
        sleep(120)
        self.turn_off_supplicant_cli()
        self.enable_sshd_ssh_cli()
        self.conf_tr69_eco_url()
        self.turn_off_wi_fi_security_protection_cli()
        self.enable_parental_control()
        self.enable_guest_network_and_set_password_ssid()

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
        # session = driver.Chrome()
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
        print("in ui_set_band_bandwith_channel ")
        # we assume that this
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
        # self.session = self.check_if_dac_required()
        self.check_if_dac_required()

        sleep(5)
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
                if option.text == str(bandwidth):
                    option.click()
                    print('bandwidth changed to:' + str(bandwidth))

                else:
                    pass
                    print('did not find bandwidth')

            channel_select = self.session.find_element_by_id("tchannelplusauto")
            print('tchannel 5g', channel)
            # bandwidth_select.select_by_value(bandwidth)
            for option in channel_select.find_elements_by_tag_name('option'):
                if option.text == str(channel):
                    option.click()
                    print('5g channel changed to channel:', channel)
                else:
                    pass
                    # print('did not find channel')
            sleep(2)

            submit = self.session.find_element_by_name("Save")
            submit.click()

            self.check_if_wifi_warning_displayed()

            return self.session

# pfp
    def disable_enable_wifi_2_4_and_5g_wifi(self):
        print('in disable_enable_wifi_2_4_and_5g_wifi')
        rg_url = 'http://192.168.1.254/'
        # session = webdriver.Chrome()
        self.session.get(rg_url)
        status_link = self.session.find_element_by_link_text("Home Network")
        status_link.click()
        sleep(2)
        home_network_link = self.session.find_element_by_link_text("Wi-Fi")
        home_network_link.click()
        sleep(2)
        self.check_if_dac_required()
        advanced_options_link = self.session.find_element_by_link_text("Advanced Options")
        advanced_options_link.click()
        sleep(2)

        wi_fi_2_4 = self.session.find_element_by_name("owl80211on")

        for option in wi_fi_2_4.find_elements_by_tag_name('option'):
            # this is problematic line
            if option.text == "Off":
                option.click()
                break
        sleep(10)
        self.session.implicitly_wait(5)
        wi_fi_5_g = self.session.find_element_by_name("twl80211on")
        # wi_fi_5_g.click()
        for option in wi_fi_5_g.find_elements_by_tag_name('option'):
            if option.text == "Off":
                option.click()
                break
        submit = self.session.find_element_by_name("Save")
        sleep(10)
        submit.click()

        self.check_for_wifi_security_and_regular_warning()
        self.session.implicitly_wait(5)
        wi_fi_2_4 = self.session.find_element_by_name("owl80211on")
        wi_fi_2_4.click()

        for option in wi_fi_2_4.find_elements_by_tag_name('option'):
            if option.text == "On":
                option.click()
                break

        wi_fi_5_g = self.session.find_element_by_name("twl80211on")
        wi_fi_5_g.click()

        for option in wi_fi_5_g.find_elements_by_tag_name('option'):
            if option.text == "On":
                option.click()
                break
        submit = self.session.find_element_by_name("Save")
        sleep(10)
        submit.click()
        self.check_for_wifi_security_and_regular_warning()
        # self.check_for_wifi_warning()

    def ui_get_wifi_password(self):
        print('in ui_get_wifi_password')
        rg_url = 'http://192.168.1.254/'
        # session = webdriver.Chrome()
        self.session.get(rg_url)
        status_link = self.session.find_element_by_link_text("Home Network")
        status_link.click()
        sleep(2)
        home_network_link = self.session.find_element_by_link_text("Wi-Fi")
        home_network_link.click()
        sleep(2)
        self.check_if_dac_required()
        ussidsecurity = self.session.find_element_by_id("ussidsecurity")
        # print('ussidsecurity is: ' + ussidsecurity.get_attribute("value"))
        print('ussidsecurity_value is: ' + str(ussidsecurity.get_attribute("value")))
        ussidsecurity_value = str(ussidsecurity.get_attribute("value"))
        # print('ussidsecurity is: ' + str(ussidsecurity.select_by_index(1)))
        password_input = self.session.find_element_by_id("password")
        print('password is: ' + password_input.get_attribute("value"))
        default_password = str(password_input.get_attribute("value"))
        # password_input.set_attribute("value","12345678")
        # print('tada2)')
        return ussidsecurity_value, default_password

    def ui_set_wifi_password(self, security, password):
        print('in ui_set_password')
        rg_url = 'http://192.168.1.254/'
        # session = webdriver.Chrome()
        self.session.get(rg_url)
        status_link = self.session.find_element_by_link_text("Home Network")
        status_link.click()
        sleep(2)
        home_network_link = self.session.find_element_by_link_text("Wi-Fi")
        home_network_link.click()
        sleep(2)
        self.check_if_dac_required()
        ussidsecurity_select = Select(self.session.find_element_by_id("ussidsecurity"))

        # for options in ussidsecurity_select.options:
        #    print('option:' + str(options.text))
        #    print('security:' + security)
        # sleep(10)
        # ussidsecurity_select.select_by_value(security)
        ussidsecurity_select.select_by_visible_text(security)
        if security == "Custom Password":
            password_input = self.session.find_element_by_id("password")
            password_input.clear()
            password_input.send_keys(password)
        submit = self.session.find_element_by_name("Save")
        sleep(10)
        submit.click()
        print('password len before check:' + str(len(password)))
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        self.check_for_wifi_warning()
        return_str = self.check_for_wifi_warning()
        return return_str

        # selected = ussidsecurity_value.option.value(security)
        # for options in ussidsecurity_select.options:
        #     print('option:' + str(options.text))
        #     #if options.text == security:
        #     #    options.click()
        # # ussidsecurity_select.select_by_index(0)
        # # ussidsecurity_select.options
        # password_input = self.session.find_element_by_id("password")
        # password_input.clear()
        # password_input.send_keys(password)
        # submit = self.session.find_element_by_name("Save")
        # sleep(10)
        # submit.click()
        # print('password before check:' + str(len(password)))
        # print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        # self.check_for_wifi_warning()
        #
        # exit()

        # for option in ussidsecurity_select.find_elements_by_tag_name('option'):
        #     print('text:' + str(option.text))
        #     if option.text == security:
        #         option.click()
        # sleep(10)
        # exit()
        # for option in ussidsecurity_select.find_elements_by_tag_name('option'):
        #     print('text:' + str(option.text))
        #     # if option.text == "Default Password":
        #     if option.text == "Default Password":
        #         option.click()
        #         # if the text is not Defaut Password then it must be Custom Password
        #         # logic is simpler is we set the option to Custom Password
        #         # I think by clicking on it it is selected
        # password_input = self.session.find_element_by_id("password")
        # password_input.clear()
        # password_input.send_keys(password)
        #
        # submit = self.session.find_element_by_name("Save")
        # sleep(10)
        # submit.click()
        # self.check_for_wifi_warning()

        # print('current password is: ' + password_input.get_attribute("value"))
        # default_password = password_input.get_attribute("value")
        # java_script = 'document.getElementsById("ussidsecurity").setAttribute("value","1234567890")'
        # java_script = 'document.getElementsByName("security")[0].click()'
        # self.session.execute_script(java_script)
        # exit()

        # if we are setting the password then we have to make sure that the use default is not set
        # channel_select = self.session.find_element_by_id("ochannelplusauto")
        # print('found ochannel')
        # print('channel', channel)
        # bandwidth_select.select_by_value(bandwidth)
        # for option in channel_select.find_elements_by_tag_name('option'):
        #   if option.text == channel:
        #       option.click()
        # self.session.execute_script('document.getElementsById("password").setAttribute("value","1234567890")')
        # password_input.set_attribute("value","12345678")
        # print('new password is: ' + password_input.get_attribute("value"))
        # new_password = password_input.get_attribute("value")
        # submit = self.session.find_element_by_name("Save")
        # submit.click()
        # return new_password

    def ui_get_wifi_info(self):
        print('in ui_get_wifi_info')
        rg_url = 'http://192.168.1.254/'
        session = webdriver.Chrome()
        session.get(rg_url)

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

        self.check_if_dac_required()
        print('tada2)')

    def get_ui_system_information(self):
        print('in get_ui_system_information)')
        global nvg_info
        rg_url = 'http://192.168.1.254/'
        # session = self.session
        self.session = webdriver.Chrome()
        self.session.get(rg_url)
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
    @staticmethod
    def wait_for_ssh_to_be_ready(host, port, timeout, retry_interval):
        print('in wait_for_ssh_to_be_read')
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        retry_interval = float(retry_interval)
        my_timeout = int(timeout)
        timeout_start = time.time()
        while time.time() < timeout_start + my_timeout:
            time.sleep(retry_interval)
            try:
                # client.connect(host, int(port), allow_agent=False, look_for_keys=False)
                client.connect(host, int(port))

            except paramiko.ssh_exception.SSHException as e:
                # socket is open but SSH has not responded
                if str(e) == 'Error reading SSH protocol banner':
                    print('SSH Error reading ssh banner - ')
                    print(e)
                    continue
                print('SSH transport is available!')
                break
            except paramiko.ssh_exception.NoValidConnectionsError as e:
                print('SSH transport not ready...', e)
                sleep(5)
                continue

    def run_speed_test_cli(self, speed_test_ip):
        print('in run_speedtest_cli')
        # speed_test_ip = "192.168.1.255"
        # ddd = f"{speed_test_ip} is a test"
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
# possible check out netmiko
    @staticmethod
    def get_wifi_info_from_android_termux(wifi_info_ip):
        print('in get_wifi_connection_info_from_android_termux')
        ssh_client = pxssh.pxssh(timeout=100, encoding='ascii', maxread=5000, options={"StrictHostKeyChecking": "no"})
        ssh_client.PROMPT='r[#$]'
        # ssh_client.login(wifi_info_ip, username='None', port=8022, auto_prompt_reset='False', sync_multiplier=5)
        ssh_client.login(wifi_info_ip, username='None', port=8022, original_prompt=r'[#$]', auto_prompt_reset=False, sync_multiplier=5, quiet=False,login_timeout=10)
        # ssh_client.PROMPT='\$
        ssh_client.prompt()
        # ssh_client.expect(".*x11-repo")
        ssh_client.expect_exact("issues")
        print('1', ssh_client.before)

        sleep(2)
        ssh_client.sendline('termux-wifi-connectioninfo')
        # ssh_client.expect('termux-wifi-connectioninfo')
        # ssh_client.sendline('help')
        # ssh_client.sendline('\n')
        ssh_client.expect_exact("COMPLETED")
        # ssh_client.prompt()
        # print('logfile', ssh_client.logfile_read )

        #ssh_client.expect(".*\$ ")
        # print('2', ssh_client.before)

        # ssh_client.prompt()
        #  speed_test_output_b = ssh_client.before
        # wifi_info_output = ssh_client.before
        print('wifi op---------------', ssh_client.before)
        ssh_client.logout()
        #
        #  exit()
        #  # wifi_info_regex = re.compile(r'bssid":\s+(\w+\.\d+)\s+\w+.*Upload:\s+(\d+\.\d+)\s+\w+', re.DOTALL)
        #
        #  print('after', wifi_info_output)
        #
        #  #speed_test_regex = re.compile(r'Download:\s+(\d+\.\d+)\s+\w+.*Upload:\s+(\d+\.\d+)\s+\w+', re.DOTALL)
        #  # wifi_info_regex = re.compile(r'\s*bssid\":\s+\"(\w+:\w+:\w+:\w+:\w+:\w+)\"\s+\"frequency_mhz\":
        #  \s+(\w+)\"ip\":\s+(\d+:\d+:\d+:\d+)\"',re.DOTALL)
        #  wifi_info_regex = re.compile(r'\s*\"(bssid)\"',re.DOTALL)
        #
        #  exit()
        #  wifi_info_groups = wifi_info_regex.search(wifi_info_output)
        #  print('bssid:', wifi_info_groups.group(1))
        # # print('frequency:', wifi_info_groups.group(2))
        # # print('ip:', wifi_info_groups.group(3))
        #
        #  #down_load_speed = wifi_info_groups.group(1)
        #  #up_load_speed = wifi_info_groups.group(2)

    @staticmethod
    def run_speed_test_from_android_termux(speed_test_ip):
        print('in run_speed_test_from_android_termux')
        # prompt = '\$\s+'
        # prompt = '\$'
        # sort of works-----------
        # ssh_client = paramiko.SSHClient()
        # ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # sleep(10)
        # -------------------------------------
        # ssh_client= pxssh.pxssh()
        # ssh_client = pxssh.pxssh(options={"StrictHostKeyChecking": "no","AutoPromptReset": "True"})
        # not sure if this is defined like this
        # ssh_client = pxssh.pxssh(timeout=200, encoding='utf-8',options={"StrictHostKeyChecking": "no","AutoPromptReset": "True"})
        # ssh_client = pxssh.pxssh(timeout=200, encoding='utf-8')

        ssh_client = pxssh.pxssh(timeout=300, encoding='utf-8', options={"StrictHostKeyChecking": "no"})
        hostname = speed_test_ip
        ssh_client.login(hostname, username=None, port=8022)
        ssh_client.prompt()
        ssh_client.sendline('speedtest  --server 5024')
        ssh_client.prompt()
        # speed_test_output_b = ssh_client.before
        speed_test_output = ssh_client.before
        # print(ssh_client.before)
        print('after conversion ti string', speed_test_output)
        # exit()
        # ssh.connect(hostname=speed_test_ip, username=UN, password=PW)
        # ssh_client.connect(hostname=speed_test_ip, port = 8022,  timeout=30)
        # ssh_client.connect(hostname=speed_test_ip, port = 8022,  timeout=30)
# sort of works-----------
#         Nvg599Class.wait_for_ssh_to_be_ready(speed_test_ip, '8022', '220', '10')
#         ssh_client.connect(hostname=speed_test_ip, port=8022, timeout=120)
        #  -------------------------------------
        # loop = 1
        # while loop == 1:
        #     try:
        #         ssh_client.connect(hostname=speed_test_ip, port = 8022,  timeout=120)
        #     except socket.timeout as error:
        #         print('socket timeout..',error)
        #         continue
        # ---------sort of works
        # ssh_session = SSHClientInteraction(ssh_client, timeout=200, display=True)
        # ssh_session.expect(prompt, timeout=200)
        # Austin speedtest server is 5024, check speedtest --list for a complete listing
        #
        # ssh_session.send('speedtest  --server 5024')
        # sleep(2)
        # ssh_session.expect(prompt, timeout=200)
        # speed_test_output = ssh_session.current_output_clean
# sort of works
        # ssh_client.sendline('speedtest  --server 5024')
        # print('speedtest_output:   ',speed_test_output )
        # speed_test_regex = re.compile(r'.*Download:\s+(\w+)\s+.*Upload:\s+(\w+)',re.DOTALL)
        # speed_test_regex = re.compile(r'(Download:\s+\w+\.\w+\s+\w+).*(Upload:\s+\w+\.\w+\s+\w+)', re.DOTALL)
        speed_test_regex = re.compile(r'Download:\s+(\d+\.\d+)\s+\w+.*Upload:\s+(\d+\.\d+)\s+\w+', re.DOTALL)
        speed_test_groups = speed_test_regex.search(speed_test_output)
        print('download:', speed_test_groups.group(1))
        print('upload:', speed_test_groups.group(2))
        down_load_speed = speed_test_groups.group(1)
        up_load_speed = speed_test_groups.group(2)
        return down_load_speed, up_load_speed

        # ssh_session = pexpect.spawn("ssh -p 8022 " + speed_test_ip, encoding='utf-8', timeout=120)
        # rint('speedtestip',speed_test_ip)
        # exit()
        # out = subprocess.check_output("ssh -p -t -t 8022  " + speed_test_ip + ' bash -s', shell=True).decode("utf-8")
        # result = os.system(cmd)
        # print('out===========\n', out)
        # exit()
        #
        # ssh_session.expect("$")
        # print('1', ssh_session.before)
        # sleep(2)
        #
        # ssh_session.sendline('date')
        # #self.device_access_code = None
        #
        # ssh_session.expect("$")
        # print('2', ssh_session.before)
        #
        # ssh_session.sendline('speedtest')
        # sleep(10)
        # # ssh_session.expect(".*Mbits.*Mbits\/s")
        # ssh_session.sendline()
        # ssh_session.expect("$")
        # print('3', ssh_session.before)
        # speed_test_ouput = ssh_session.before
        # # speed_test_regex = re.compile(r'.*Download:\s+(\w+)\s+.*Upload:\s+(\w+)',re.DOTALL)
        # speed_test_regex = re.compile(r'(Download:\s+\w+\.\w+\s+\w+).*(Upload:\s+\w+\.\w+\s+\w+)', re.DOTALL)
        # speed_test_groups = speed_test_regex.search(speed_test_ouput)
        # print(speed_test_groups.group(1))
        # print(speed_test_groups.group(2))
        # down_load_speed = speed_test_groups.group(1)
        # up_load_speed = speed_test_groups.group(2)
        # ssh_session.close()

        # return down_load_speed, up_load_speed
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

    # @staticmethod
    def ping_from_local_host(self, remote_ip, number_of_pings=20):
        # def ping_from_local_host(remote_ip):
        min_ping, avg_ping, max_ping, mdev_ping = 0
        print('In ping_from_local_host')
        ping_file = open('ping_file.txt', 'a')
        # out = subprocess.Popen("ping  -c3 localhost",stdout=subprocess.PIPE,stderr=subprocess.STDOUT, shell=True)
        # out = subprocess.Popen(["ping ", "-c3"," localhost"], stdout=subprocess.PIPE)
        # out, err = out.communicate()
        # out = check_output(["ping ", "-c3 ", "localhost"]).decode("utf-8")
        # out = check_output(["ls -la"].decode("utf-8").shell=True)
        out = subprocess.check_output("ping -c20 " + remote_ip, shell=True).decode("utf-8")
        # result = os.system(cmd)
        print('out===========\n', out)
        print('endout1===========\n')
        # pingInfoRegEx = re.compile(r'.*=\s(\w+)/(\w+)/(\w+)/(\w+)',re.DOTALL)
        ping_info_reg_ex = re.compile(r'rtt.*?=\s(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)')
        # pingInfoRegEx = re.compile(r'.*?rtt/s+=/s+(/d+/./d+)',re.DOTALL)
        mo1 = ping_info_reg_ex.search(out)
        # print('mo1',mo1)
        # minimum = mo1.group(1)
        # print('mnext--just a value', minimum)
        min_ping = mo1.group(1)
        avg_ping = mo1.group(2)
        max_ping = mo1.group(3)
        mdev_ping = mo1.group(4)
        # ping_file.write('test' )
        # self.software_version
        now = datetime.today().isoformat()
        ping_file.writelines('Date:' + now + " 599 Software Vers:" + self.software_version + " Serial No:" +
                             self.serial_number + '  min_ping:' + min_ping + '  avg_ping:' +
                             '  max_ping:' + max_ping + '  max dev:' + mdev_ping)
        ping_file.writelines('\n')
        ping_file.close()
        return min_ping, avg_ping, max_ping, mdev_ping

    def ping_check(self, remote_ip):
        print('In ping_check')
        # out = subprocess.check_output("ping -c10 " + remote_ip, shell=True).decode("utf-8")
        try:
            out = subprocess.check_output("ping -c10 " + remote_ip, shell=True).decode("utf-8")
            ping_info_reg_ex = re.compile(r'(\d+.*loss)')
            ping_status = ping_info_reg_ex.search(out)
            print('ping result:', ping_status.group(1))

            return ping_status.group(1)
        except subprocess.CalledProcessError as e:
            print('ping error:', e.output)
            e.returncode = 0
            ping_fail_str = str(e.output)
            ping_fail_return = "Ping_failed:" + ping_fail_str
            print('ping failed:')

            return ping_fail_return

    def login_nvg_599_cli(self):
        print('In login_nvg_cli')

        self.telnet_cli_session = pexpect.spawn("telnet 192.168.1.254", encoding='utf-8')
        self.telnet_cli_session.expect("ogin:")
        self.telnet_cli_session.sendline('admin')
        self.telnet_cli_session.expect("ord:")
        #  self.telnet_cli_session.sendline('<<01%//4&/')
        #  self.telnet_cli_session.sendline('9==5485?6<')
        nvg_dac = self.device_access_code
        self.telnet_cli_session.sendline(nvg_dac)
        self.telnet_cli_session.expect(">")
        self.telnet_cli_session.sendline('magic')
        self.telnet_cli_session.expect(">")
        return self.telnet_cli_session

    @staticmethod
    def static_login_nvg_599_cli():
        print('In login_nvg_cli')
        telnet_cli_session = pexpect.spawn("telnet 192.168.1.254", encoding='utf-8')
        telnet_cli_session.expect("ogin:")
        telnet_cli_session.sendline('admin')
        telnet_cli_session.expect("ord:")
        telnet_cli_session.sendline('<<01%//4&/')
        telnet_cli_session.expect(">")
        telnet_cli_session.sendline('magic')
        telnet_cli_session.expect("UNLOCKED>")
        return telnet_cli_session

    @staticmethod
    def static_login_4920(ip_4920):
        print('In login_4920')
        cli_session = pexpect.spawn("telnet" + ip_4920, encoding='utf-8')
        cli_session.expect("ogin:")
        cli_session.sendline('admin')
        cli_session.expect("#")
        return cli_session

    @staticmethod
    def get_4920_ssid(ip_4920):
        print('In get_4920_ssid')
        cli_session = pexpect.spawn("telnet" + ip_4920, encoding='utf-8')
        cli_session.expect("ogin:")
        cli_session.sendline('admin')
        cli_session.expect("#")
        cli_session.sendline('wl -i wl1 status')
        cli_session.expect("#")
        status_output = cli_session.before
        status_info_reg_ex = re.compile(r'Model\s(\w+)\s+\w+/\w+.*number\s+(\w+).*Uptime\s+(\d\d:\d\d:\d\d:\d\d)',
                                        re.DOTALL)
        # statusInfoRegEx = re.compile(r'Model\s(\w+).*Serial Number\s+(\d+)',re.DOTALL)
        # status InfoRegEx = re.compile(r'Model\s(\w+)')
        mo1 = status_info_reg_ex.search(status_output)
        return mo1

    def cli_rg_status(self, ip):
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
        status_info_reg_ex = re.compile(r'Model\s(\w+)\s+\w+/\w+.*number\s+(\w+).*Uptime\s+(\d\d:\d\d:\d\d:\d\d)',
                                        re.DOTALL)
        # statusInfoRegEx = re.compile(r'Model\s(\w+).*Serial Number\s+(\d+)',re.DOTALL)
        # status InfoRegEx = re.compile(r'Model\s(\w+)')
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
        print('tr69 enbled for ECO')
        self.session.close()

    def enable_sshd_ssh_cli(self):
        self.telnet_cli_session = self.login_nvg_599_cli()
        self.telnet_cli_session.sendline('magic')
        self.telnet_cli_session.expect("UNLOCKED>")
        self.telnet_cli_session.sendline('tr69 SetParameterValues InternetGatewayDevice.X_0000C5_Debug.SshdEnabled=1')
        self.telnet_cli_session.expect("successful.*>")
        print('Enabled tr69 SshdEnabled=1')
        self.telnet_cli_session.close()

    @staticmethod
    def check_if_url_is_up(url_to_check):
        start = time.time()
        print("starting timer:" + str(start))
        loop = 1
        while loop == 1:
            try:
                urllib.request.urlopen(url_to_check, timeout=3)
                end = time.time()
                print("Duration timer:", str(end - start))
                return

            except TimeoutError:
                print('Not ready, sleeping 10 seconds')
                sleep(10)
                print('time' + str(time.time()))
                continue

# incomplete there are profiles to add
    def enable_parental_control(self):
        print("Enabled_parental_contol")
        self.telnet_cli_session = self.login_nvg_599_cli()
        self.telnet_cli_session.sendline('magic')
        self.telnet_cli_session.sendline("tr69 set InternetGatewayDevice.LANDevice.1.X_ATT_PC.Enable=1")
        self.telnet_cli_session.expect("successful.*UNLOCKED>")
        self.telnet_cli_session.sendline("tr69 set InternetGatewayDevice.LANDevice.1.X_ATT_PC.TOD.TODEnable=1")
        self.telnet_cli_session.expect("successful.*UNLOCKED>")
        self.telnet_cli_session.sendline("tr69 set InternetGatewayDevice.LANDevice.1.X_ATT_PC.TOD."
                                         "Profile.9.RestrictionType=TimeSlot")
        self.telnet_cli_session.expect("successful.*UNLOCKED>")
        self.telnet_cli_session.sendline("tr69 set InternetGatewayDevice.LANDevice.1.X_ATT_PC.TOD."
                                         "Profile.9.Apps=67137536,218163712")
        self.telnet_cli_session.expect("successful.*UNLOCKED>")
        self.telnet_cli_session.sendline("tr69 set InternetGatewayDevice.LANDevice.1.X_ATT_PC.TOD.Profile."
                                         "9.UsageThreshold=10000")
        self.telnet_cli_session.expect("successful.*UNLOCKED>")
        self.telnet_cli_session.sendline("tr69 set InternetGatewayDevice.LANDevice.1.X_ATT_PC.TOD."
                                         "Profile.9.Scheduler.1.Days=1000000")
        self.telnet_cli_session.expect("successful.*UNLOCKED>")
        self.telnet_cli_session.sendline("tr69 set InternetGatewayDevice.LANDevice.1.X_ATT_PC.TOD."
                                         "Profile.9.Scheduler.1.TimeSlots=11111111111111111111111111111111111111111"
                                         "1111111000000000000000000000000000011111111111111111111")
        self.telnet_cli_session.expect("successful.*UNLOCKED>")
        self.telnet_cli_session.sendline("tr69 set InternetGatewayDevice.LANDevice.1.X_ATT_PC.TOD."
                                         "Profile.9.Scheduler.1.UsageDuration=86400")
        self.telnet_cli_session.expect("successful.*UNLOCKED>")
        self.telnet_cli_session.sendline("tr69 set InternetGatewayDevice.LANDevice.1.X_ATT_PC.TOD."
                                         "Profile.9.Scheduler.2.Days=0100000")
        self.telnet_cli_session.expect("successful.*UNLOCKED>")
        self.telnet_cli_session.sendline("tr69 set InternetGatewayDevice.LANDevice.1.X_ATT_PC.TOD."
                                         "Profile.9.Scheduler.2.TimeSlots=111111111111111111111111111111111111111111"
                                         "111111000000000000000000000000000011111111111111111111")
        self.telnet_cli_session.expect("successful.*UNLOCKED>")
        self.telnet_cli_session.sendline("tr69 set InternetGatewayDevice.LANDevice.1.X_ATT_PC.TOD."
                                         "Profile.9.Scheduler.2.UsageDuration=86400")
        self.telnet_cli_session.expect("successful.*UNLOCKED>")
        self.telnet_cli_session.sendline("tr69 set InternetGatewayDevice.LANDevice.1.X_ATT_PC.TOD."
                                         "Profile.9.Scheduler.3.Days=0010000")
        self.telnet_cli_session.expect("successful.*UNLOCKED>")
        self.telnet_cli_session.sendline("tr69 set InternetGatewayDevice.LANDevice.1.X_ATT_PC.TOD."
                                         "Profile.9.Scheduler.3.TimeSlots=111111111111111111111111111111111111111111"
                                         "111111000000000000000000000000000011111111111111111111")
        self.telnet_cli_session.expect("successful.*UNLOCKED>")
        self.telnet_cli_session.sendline("tr69 set InternetGatewayDevice.LANDevice.1.X_ATT_PC.TOD."
                                         "Profile.9.Scheduler.3.UsageDuration=86400")
        self.telnet_cli_session.expect("successful.*UNLOCKED>")
        self.telnet_cli_session.sendline("tr69 set InternetGatewayDevice.LANDevice.1.X_ATT_PC.TOD."
                                         "Profile.9.Scheduler.4.Days=0001000")
        self.telnet_cli_session.expect("successful.*UNLOCKED>")
        self.telnet_cli_session.sendline("tr69 set InternetGatewayDevice.LANDevice.1.X_ATT_PC.TOD."
                                         "Profile.9.Scheduler.4.TimeSlots=1111111111111111111111111111111111111111"
                                         "11111111000000000000000000000000000011111111111111111111")
        self.telnet_cli_session.expect("successful.*UNLOCKED>")
        self.telnet_cli_session.sendline("tr69 set InternetGatewayDevice.LANDevice.1.X_ATT_PC.TOD."
                                         "Profile.9.Scheduler.4.UsageDuration=86400")
        self.telnet_cli_session.expect("successful.*UNLOCKED>")
        self.telnet_cli_session.sendline("tr69 set InternetGatewayDevice.LANDevice.1.X_ATT_PC.TOD."
                                         "Profile.9.Scheduler.5.Days=0000100")
        self.telnet_cli_session.expect("successful.*UNLOCKED>")
        self.telnet_cli_session.sendline("tr69 set InternetGatewayDevice.LANDevice.1.X_ATT_PC.TOD."
                                         "Profile.9.Scheduler.5.TimeSlots=1111111111111111111111111111111111111111"
                                         "11111111000000000000000000000000000011111111111111111111")
        self.telnet_cli_session.expect("successful.*UNLOCKED>")
        self.telnet_cli_session.sendline("tr69 set InternetGatewayDevice.LANDevice.1.X_ATT_PC.TOD."
                                         "Profile.9.Scheduler.5.UsageDuration=86400")
        self.telnet_cli_session.expect("successful.*UNLOCKED>")
        self.telnet_cli_session.sendline("tr69 set InternetGatewayDevice.LANDevice.1.X_ATT_PC.TOD."
                                         "Profile.9.Scheduler.6.Days=0000010")
        self.telnet_cli_session.expect("successful.*UNLOCKED>")
        self.telnet_cli_session.sendline("tr69 set InternetGatewayDevice.LANDevice.1.X_ATT_PC.TOD."
                                         "Profile.9.Scheduler.6.TimeSlots=1111111111111111111111111111111111111111"
                                         "11111111000000000000000000000000000011111111111111111111")
        self.telnet_cli_session.expect("successful.*UNLOCKED>")
        self.telnet_cli_session.sendline("tr69 set InternetGatewayDevice.LANDevice.1.X_ATT_PC.TOD."
                                         "Profile.9.Scheduler.6.UsageDuration=86400")
        self.telnet_cli_session.expect("successful.*UNLOCKED>")
        self.telnet_cli_session.sendline("tr69 set InternetGatewayDevice.LANDevice.1.X_ATT_PC.TOD."
                                         "Profile.9.Scheduler.7.Days=0000001")
        self.telnet_cli_session.expect("successful.*UNLOCKED>")
        self.telnet_cli_session.sendline("tr69 set InternetGatewayDevice.LANDevice.1.X_ATT_PC.TOD."
                                         "Profile.9.Scheduler.7.TimeSlots=11111111111111111111111111111111111111"
                                         "1111111111000000000000000000000000000011111111111111111111")
        self.telnet_cli_session.expect("successful.*UNLOCKED>")
        self.telnet_cli_session.sendline("tr69 set InternetGatewayDevice.LANDevice.1.X_ATT_PC.TOD."
                                         "Profile.9.Scheduler.7.UsageDuration=86400")
        self.telnet_cli_session.expect("successful.*UNLOCKED>")

    def conf_tr69_eco_url(self):
        self.telnet_cli_session = self.login_nvg_599_cli()
        self.telnet_cli_session.sendline('magic')
        self.telnet_cli_session.expect("UNLOCKED>")
        self.telnet_cli_session.sendline('conf')
        self.telnet_cli_session.expect("\\(top\\)>>")
        self.telnet_cli_session.sendline('manage cwmp')
        self.telnet_cli_session.expect("\\(management cwmp\\)>>")
        self.telnet_cli_session.sendline('set')
        self.telnet_cli_session.expect("]:")
        self.telnet_cli_session.sendline('on')
        self.telnet_cli_session.expect("\\):")
        self.telnet_cli_session.sendline('http://arris1.arriseco.com')
        # this has some numbers
        self.telnet_cli_session.expect("\\):")
        self.telnet_cli_session.sendline()
        self.telnet_cli_session.expect("\\): ")
        self.telnet_cli_session.sendline()
        self.telnet_cli_session.expect("\\): ")
        self.telnet_cli_session.sendline()
        self.telnet_cli_session.expect(" 65535 ]:")
        self.telnet_cli_session.sendline()
        self.telnet_cli_session.expect("\\) : ")
        self.telnet_cli_session.sendline()
        self.telnet_cli_session.expect("\\):")
        self.telnet_cli_session.sendline()
        self.telnet_cli_session.expect("255 ]:")
        self.telnet_cli_session.sendline()
        self.telnet_cli_session.expect("0 - 7 ]: ")
        self.telnet_cli_session.sendline()
        self.telnet_cli_session.expect("\\):")
        self.telnet_cli_session.sendline()
        self.telnet_cli_session.expect("on ]:")
        self.telnet_cli_session.sendline()
        self.telnet_cli_session.expect("600 ]:")
        self.telnet_cli_session.sendline()
        self.telnet_cli_session.expect("on ]:")
        self.telnet_cli_session.sendline()
        self.telnet_cli_session.expect(">>")
        self.telnet_cli_session.sendline('save')
        self.telnet_cli_session.expect(">>")
        print('Configured TR068 ECO url')
        self.telnet_cli_session.close()

    def turn_off_supplicant_cli(self):
        self.telnet_cli_session = self.login_nvg_599_cli()
        self.telnet_cli_session.sendline('magic')
        self.telnet_cli_session.expect("UNLOCKED>")
        self.telnet_cli_session.sendline('conf')
        self.telnet_cli_session.expect('\\(top\\)>>')
        self.telnet_cli_session.sendline('system supplicant')
        self.telnet_cli_session.expect("\\(system supplicant\\)>>")
        self.telnet_cli_session.sendline('set')
        self.telnet_cli_session.expect("]:")
        self.telnet_cli_session.sendline('off')
        self.telnet_cli_session.expect("\\(system supplicant\\)>>")
        self.telnet_cli_session.sendline('save')
        self.telnet_cli_session.expect("\\(system supplicant\\)>>")
        self.telnet_cli_session.sendline('exit')
        self.telnet_cli_session.expect("UNLOCKED>")
        self.telnet_cli_session.sendline('exit all')
        print('Turned off system supplicant')
        self.telnet_cli_session.close()

    def turn_off_wi_fi_security_protection_cli(self):
        self.telnet_cli_session = self.login_nvg_599_cli()
        self.telnet_cli_session.sendline('magic')
        self.telnet_cli_session.expect("UNLOCKED>")
        self.telnet_cli_session.sendline('nsh')
        self.telnet_cli_session.expect("\\(nsh\\) ")
        self.telnet_cli_session.sendline('set security.ext-wifi-protection off')
        self.telnet_cli_session.expect("\\(nsh\\) ")
        self.telnet_cli_session.sendline('save')
        self.telnet_cli_session.expect("\\(nsh\\) ")
        self.telnet_cli_session.sendline('apply')
        self.telnet_cli_session.expect("\\(nsh\\) ")
        self.telnet_cli_session.sendline('exit all')
        print('Turned off WiFi security protection')
        self.telnet_cli_session.close()

    def get_rg_serial_number_cli(self):
        self.login_nvg_599_cli()
        self.telnet_cli_session.sendline('status')
        self.telnet_cli_session.expect('>')
        status_output = self.session.before
        print('Getting getSerialnumber')
        status_info_reg_ex = re.compile(r'Model\s(\w+)\s+\w+/\w+.*number\s+(\w+).*Uptime\s+(\d\d:\d\d:\d\d:\d\d)',
                                        re.DOTALL)
        mo1 = status_info_reg_ex.search(status_output)
        return mo1.group(2)

    @staticmethod
    def get_rg_sh_ip_lan_info_cli():
        # telnet_cli_session =self.login_nvg_599_cli()
        telnet_cli_session = Nvg599Class.static_login_nvg_599_cli()
        # self.telnet_cli_session. sendline("show ip lan")
        telnet_cli_session. sendline("show ip lan")
        # self.telnet_cli_session.expect('>')
        telnet_cli_session.expect('>')
        # ip_lan_output = self.telnet_cli_session.before
        ip_lan_output = telnet_cli_session.before
        ip_lan_output = ip_lan_output.split('\n\r')
        lan_output_count = len(ip_lan_output)
        # discard first two lines of the output
        print("count", lan_output_count)
        ip_lan_output = ip_lan_output[2:-1]
        # I think the length minus 1 is what we want // need to check this
        # This must be outside the for loop
        ip_lan_connections_dict_cli = {}
        for i in range(len(ip_lan_output)):
            # print("input line:", ipLanOutput[i])
            # mo1 = statusInfoRegEx.match(ipLanOutput[i])
            ip_lan_output_split = (ip_lan_output[i]).split()
            # print ("connectedDeviceName",ipLanOutputSplit[0])
            # self.connectedDeviceName = ipLanOutputSplit[0]
            connected_device_name = ip_lan_output_split[0]
            # if "ATT_4920" in ipLanOutputSplit[0]:
            #    print("this is an airties device!")
            # print("connectedDeviceIP", ip_lan_output_split[1])
            connected_device_ip = ip_lan_output_split[1]
            # print("connected_device_mac", ip_lan_output_split[2])
            connected_device_mac = ip_lan_output_split[2]
            # print("connectedDeviceStatus", ip_lan_output_split[3])
            connected_device_status = ip_lan_output_split[3]
            # print("connectedDeviceDHCP", ip_lan_output_split[4])
            connected_device_dhcp = ip_lan_output_split[4]
            # print("connectedDeviceSSIDNumber", ip_lan_output_split[5])
            connected_device_port = ip_lan_output_split[5]
            # This dict uses the mac as the primary key
            # self.ip_lan_connections_dict_cli[connected_device_mac] = {}
            ip_lan_connections_dict_cli[connected_device_mac] = {}
            ip_lan_connections_dict_cli[connected_device_mac]["IP"] = connected_device_ip
            ip_lan_connections_dict_cli[connected_device_mac]["Name"] = connected_device_name
            ip_lan_connections_dict_cli[connected_device_mac]["State"] = connected_device_status
            ip_lan_connections_dict_cli[connected_device_mac]["DHCP"] = connected_device_dhcp
            ip_lan_connections_dict_cli[connected_device_mac]["Port"] = connected_device_port
            # self.telnet_cli_session.close()
        telnet_cli_session.close()
        return ip_lan_connections_dict_cli

# class Nvg_5268_Class(GatewayClass):
#     def __init__(self):
#         self.name = "Nvg_5268"
#      # rg5268 = pexpect.spawn("telnet 192.168.1.254")

