# from itertools import count
import subprocess
from subprocess import Popen, PIPE
from openpyxl import Workbook
from pexpect import pxssh
from socket import timeout
# from subprocess import check_output
from selenium.webdriver.common.by import By
from selenium.webdriver import DesiredCapabilities


from selenium import webdriver

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select

import urllib.request

from xml.etree.ElementTree import fromstring, ElementTree

from urllib.error import URLError, HTTPError
# import url
# import urllib3
import pexpect
import re
import socket
import paramiko
# from paramiko_expect import SSHClientInteraction
# import wget
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
# dictionary with the serial number as the key

nvg_info = {"228946241148656": {'model': 'nvg599', 'device_access_code': "*<#/53#1/2", 'magic': 'kjundhkdxlxr',
                                'mac2g': 'd0:39:b3:60:56:f1', 'mac5g': 'd0:39:b3:60:56:f4', 'ssid_def_pw': 'c2cmybt25dey',
                                'ssid_def': 'xxxxxx', 'ssid_3': 'ZipKey-PSK', 'ssid_3_pw': 'Cirrent1',
                                'ssid_4': 'ATTPOC', 'ssid_4_pw': 'Ba1tshop'},

            "277427577103760": {'model': 'nvg599', 'device_access_code': '<<01%//4&/', 'magic': 'ggtxstgwipcg',
                                'mac2g': 'fc:51:a4:2f:25:90', 'mac5g': 'fc:51:a4:2f:25:94', 'ssid_def_pw': 'nsrmpr59rxwv',
                                'ssid_def': 'ATTqbrAnYs', 'ssid_3': 'ZipKey-PSK', 'ssid_3_pw': 'Cirrent1',
                                'ssid_4': 'ATTPOC', 'ssid_2_pw': 'Ba1tshop'},

            "35448081188192": {'model': 'nvg599', 'device_access_code': '9==5485?6<', 'magic': 'pqomxqikedca',
                               'mac2g': '20:3d:66:49:85:61', 'mac5g': '20:3d:66:49:85:64', 'ssid_def_pw': 'eeh4jxmh7q26',
                               'ssid_def': 'ATT4ujR48s', 'ssid_3': 'ZipKey-PSK', 'ssid_3_pw': 'Cirrent1',
                               'ssid_4': 'ATTPOC', 'ssid_4_pw': 'Ba1tshop'}}
# *7<#56*2<2
# outside of func['88:41:fc:86:64:d7', '88:41:fc:c3:56:c3']
airties_4920_defaults = {
    '88:41:FC:86:64:D6': {'device_type': 'airties_4920', 'oper_sys': 'tbd', 'radio': 'abg', 'band': '2',
                          'state': 'None', 'default_ssid': 'AirTies_SmartMesh_4PNF', 'default_pw': 'kykfmk8997',
                          'address_type': 'None', 'port': 'None', 'ssid': 'None', 'rssi': 'None', 'ip': 'None',
                          'device_test_name': 'airties_1_2g', 'name': 'ATT_4920_8664D4', 'location': 'master_bedroom'},
    '88:41:FC:86:64:D4': {'device_type': 'airties_4920', 'oper_sys': 'tbd', 'radio': 'abg', 'band': '5',
                          'state': 'None', 'default_ssid': 'AirTies_SmartMesh_4PNF', 'default_pw': 'kykfmk8997',
                          'address_type': 'None', 'port': 'None', 'ssid': 'None', 'rssi': 'None', 'ip': 'None',
                          'device_test_name': 'airties_1_5g', 'name': 'ATT_4920_8664D4', 'location': 'master_bedroom'},
    '88:41:FC:C3:56:C2': {'device_type': 'airties_4920', 'oper_sys': 'tbd', 'radio': 'abg', 'band': '2',
                          'state': 'None', 'default_ssid': 'AirTies_Air4920_33N3', 'default_pw': 'wthchc7344',
                          'address_type': 'None', 'port': 'None', 'ssid': 'None', 'rssi': 'None', ' ip': 'None',
                          'device_test_name': 'airties_2_2g', 'name': 'ATT_4920_C356C0', 'location': 'master_bedroom'},
    '88:41:FC:C3:56:C0': {'device_type': 'airties_4920', 'oper_sys': 'tbd', 'radio': 'abg', 'band': '5',
                          'state': 'None', 'default_ssid': 'AirTies_Air4920_33N3', 'default_pw': 'wthchc7344',
                          'address_type': 'None', 'port ': 'None', 'ssid': 'None', 'rssi': 'None', 'ip': 'None',
                          'device_test_name': 'airties_2_5g', 'name': 'ATT_4920_C356C0',
                          'location': 'master_bedroom'}, }

test_house_devices_static_info = {
    '88:41:FC:86:64:D6': {'device_type': 'airties_4920', 'oper_sys': 'tbd', 'radio': 'abg', 'band': '2',
                          'state': 'None',
                          'address_type': 'None', 'port': 'None', 'ssid': 'None', 'rssi': 'None', 'ip': 'None',
                          'device_test_name': 'airties_1_2g', 'name': 'ATT_4920_8664D4', 'location': 'master_bedroom'},
    '88:41:FC:86:64:D4': {'device_type': 'airties_4920', 'oper_sys': 'tbd', 'radio': 'abg', 'band': '5',
                          'state': 'None',
                          'address_type': 'None', 'port': 'None', 'ssid': 'None', 'rssi': 'None', 'ip': 'None',
                          'device_test_name': 'airties_1_5g', 'name': 'ATT_4920_8664D4', 'location': 'master_bedroom'},
    '8:41:fc:c3:56:c2': {'device_type': 'airties_4920', 'oper_sys': 'tbd', 'radio': 'abg', 'band': '2',
                         'state': 'None',
                         'address_type': 'None', 'port': 'None', 'ssid': 'None', 'rssi': 'None', ' ip': 'None',
                         'device_test_name': 'airties_2_2g', 'name': 'ATT_4920_C356C0', 'location': 'master_bedroom'},
    '88:41:fc:c3:56:c0': {'device_type': 'airties_4920', 'oper_sys': 'tbd', 'radio': 'abg', 'band': '5',
                          'state': 'None',
                          'address_type': 'None', 'port ': 'None', 'ssid': 'None', 'rssi': 'None', 'ip': 'None',
                          'device_test_name': 'airties_2_5g', 'name': 'ATT_4920_C356C0', 'location': 'master_bedroom'},
    '4c:bb:58:68:bd:f6': {'device_type': 'ubuntu_laptop', 'oper_sys': 'tbd', 'radio': 'bg', 'band': '5',
                          'state': 'None',
                          'address_type': 'None', 'port': 'None', 'ssid': 'None', 'rssi': 'None', 'ip': 'None',
                          'device_test_name': 'ubuntu_1', 'name': 'arris-Latitude-MBR', 'location': 'tbd'},
    'f4:5c:89:9d:f1:4f': {'device_type': 'macbook_pro', 'oper_sys': 'tbd', 'radio': 'abg', 'band': '5',
                          'state': 'None',
                          'address_type': 'None', 'port': 'None', 'ssid': 'None', 'rssi': 'None', 'ip': 'None',
                          'device_test_name': 'mac_book_1', 'name': 'macbook-mbr', 'location': 'master_bedroom'},
    '34:e6:d7:2b:cd:7c': {'device_type': 'ubuntu_laptop', 'oper_sys': '18.04', 'radio': 'abg', 'band': '5',
                          'state': 'None',
                          'address_type': 'None', 'port': 'None', 'ssid': 'None', 'rssi': 'None', 'ip': 'None',
                          'device_test_name': 'mac_book_1', 'name': 'palmer_Latitude-E5450',
                          'location': 'tbd'},

    'e4:58:e7:02:14:d6': {'device_type': 'Galaxy-Tab-A', 'oper_sys': 'Andoid 9', 'radio': 'abg', 'band': '5',
                          'state': 'None',
                          'address_type': 'fixed', 'port': 'None', 'ssid': 'None', 'rssi': 'None', 'ip': '192.168.1.65',
                          'device_test_name': 'fixed_taba', 'name': 'palmer_Latitude-E5450',
                          'location': 'tdb'},
    'f8:f1:b6:69:91:a3': {'device_type': 'Moto X', 'oper_sys': 'Android 5.1', 'radio': 'abg', 'band': '5',
                          'state': 'None',
                          'address_type': 'fixed', 'port': 'None', 'ssid': 'None', 'rssi': 'None', 'ip': '192.168.1.66',
                          'device_test_name': 'fixed_motox', 'name': 'palmer_Latitude-E5450', 'location': 'tbd'},
    'b8:d7:af:aa:27:c3': {'device_type': 'Galaxy-Note8', 'oper_sys': 'Android 9', 'radio': 'abg', 'band': '5',
                          'state': 'None',
                          'address_type': 'fixed', 'port': 'None', 'ssid': 'None', 'rssi': 'None', 'ip': '192.168.1.67',
                          'device_test_name': 'fixed_note8', 'name': 'palmer_Latitude-E5450',
                          'location': 'tdb'},
    '8c:45:00:9f:82:9d': {'device_type': 'Galaxy-S9', 'oper_sys': 'Android 9', 'radio': 'abg', 'band': '5',
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
        self.ip = "192.168.1.254"
        self.device_access_code = None
        self.model = None
        self.session = None
        self.init_info = False
        self.telnet_cli_session = None
        self.airties_ap_cli_session = None
        global nvg_info
        # The DAC must be read from the actual device., so it is stored in a dictionary of all the test house nvg599s
        self.software_version = None
        self.mac_address = None
        self.last_reboot_time = None
        self.current_date = None
        self.hardware_version = None
        self.serial_number = None
        self.factory_reset = None
        # self.ip_lan_connections_dict_cli = {}

        print("in Nvg599Class__init")
        self.init_info = True
        self.mesh_connected_clents = {}
        self.rg_url = 'http://192.168.1.254/'

    @staticmethod
    def email_test_results(text_file, firmware):
        now = datetime.today().strftime("%B %d, %Y,%H:%M")
        # now = datetime.today().isoformat()
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
        msg['Subject'] = 'NVG 599 test results:' + firmware
        # msg['Subject'] = subject_title

        msg['From'] = 'leandertesthouse@gmail.com'
        msg['To'] = 'pfpalmer@gmail.com'
        # gmail_password = "1329brome"
        gmail_password = "%%45A7A&akBc"
        # %%45A7A&akBc
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


class Nvg599Class(GatewayClass):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.ip = "192.168.1.254"
        self.device_access_code = None
        self.model = None
        self.session = None
        self.init_info = False
        self.telnet_cli_session = None
        self.airties_ap_cli_session = None
        self.air_cli_session = None
        global nvg_info
        # # The DAC must be read from the actual device., so it is stored in a dictionary of all the test house nvg599s
        self.software_version = None
        self.mac_address = None
        self.last_reboot_time = None
        self.current_date = None
        self.hardware_version = None
        self.serial_number = None
        self.factory_reset = None
        self.rg_url = 'http://192.168.1.254/'
        self.get_ui_system_information()
        self.device_access_code = nvg_info[self.serial_number]['device_access_code']
        self.default_rg_ssid = nvg_info[self.serial_number]['ssid_def']

    def remote_webserver(self):
        pass

    def webdrivertest(self):
        self.session = webdriver.Chrome()
        self.session = WebDriverWait(self.session, 4)

    def get_ui_system_information(self):
        print('in get_ui_system_information)')
        global nvg_info
        rg_url = 'http://192.168.1.254/'
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

    def check_for_system_info_page(self):
        print('in check_for_system_info_page)')
        return_string = "Pass"
        rg_url = 'http://192.168.1.254/'
        self.session = webdriver.Chrome()
        self.session.get(rg_url)
        # status_link = self.session.find_element_by_link_text("System Information")
        try:
            # wi_fi_warning = self.session.find_element_by_class_name("warning")
            self.session.find_element_by_link_text("System Information")
        except NoSuchElementException:
            print('Problem with Status link assuming UI is not up, ')
            return_string = "Fail"
            self.session.close()
            return return_string
        return return_string

    def login_nvg_cli(self):
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


    # Should combine these two methods
    def set_all_4920s_to_factory_default(self):
        # show_ip_lan_dict = self.get_rg_sh_ip_lan_info_cli()
        show_ip_lan_dict = Nvg599Class.cli_sh_rg_ip_lan_info(self)
        # airties_4920_ip_list = []
        for ip_lan_entry in show_ip_lan_dict:
            if "ATT_4920" in show_ip_lan_dict[ip_lan_entry]["Name"]:
                # print(ip_lan_entry)
                # add this to a list which airties_4920
                print('in for loop' + show_ip_lan_dict[ip_lan_entry]["IP"])
                # airties_4920_ip_list.append(show_ip_lan_dict[ip_lan_entry]["IP"])
                # self.set_4920_to_factory_default(show_ip_lan_dict[ip_lan_entry]["IP"])
                airties_ip = show_ip_lan_dict[ip_lan_entry]["IP"]
                # Nvg599Class.set_4920_to_factory_default(show_ip_lan_dict[ip_lan_entry]["IP"])
                Nvg599Class.set_4920_to_factory_default(self, airties_ip)

    # patches1

    def login_eco(self):
        # print('setting 4920 with ip:' + ip_of_4920 + ' to factory default' )
        print('url is http://arris1.arriseco.com/manage/login')
        #global nvg_info
        # capabilities = DesiredCapabilities.CHROME.copy()
        #capabilities = DesiredCapabilities.CHROME.copy()
        desired_capabilities = DesiredCapabilities.FIREFOX.copy()
        desired_capabilities['acceptInsecureCerts'] = True
        eco_url = 'https://arris1.arriseco.com/manage/login/'
        print('eco session' + str(eco_url))
        #options = webdriver.ChromeOptions()
        # options.add_argument("--disable-web-security")
        #options.add_argument("--ignore-certificate-errors")
        #options.add_argument("--allow-running-insecure-content")
        #capabilities = options.to_capabilities()
        # eco_session = webdriver.Firefox(capabilities=desired_capabilities)
        eco_session = webdriver.Firefox()

        # eco_session = webdriver.Chrome(eco_url, capabilities)
        eco_session.get(eco_url)
        sleep(320)


    def set_4920_to_factory_default(self, ip_of_4920):
        # print('setting 4920 with ip:' + ip_of_4920 + ' to factory default' )
        print('setting 4920 with ip:' + ip_of_4920 + ' to factory default')
        global nvg_info
        airties_url = 'http://' + ip_of_4920 + '/'
        print('airties_url' + airties_url)
        airties_session = webdriver.Chrome()
        airties_session.get(airties_url)
        session_id = airties_session.session_id
        print(str(session_id))
        # airties_session.implicitly_wait(10)
        # // *[ @ id = "mainlevel"] / li[3] / a
        # # advanced_settings_link = airties_session.find_element_by_xpath('// *[ @ id = "mainlevel"] / li[3] / a')
        airties_session.switch_to.frame(airties_session.find_element_by_css_selector("frame[name=menuFrame"))
        wait = WebDriverWait(airties_session, 10)
        # advanced_link = wait.until(EC.element_to_be_clickable((By.XPATH,'// *[ @ id = "mainlevel"] / li[3] /a')))
        wait.until(EC.element_to_be_clickable((By.XPATH, '// *[ @ id = "mainlevel"] / li[3] /a'))).click()
        # sleep(20)
        # advanced_link.click()
        # advanced_settings_link = airties_session.find_element_by_partial_link_text("ADVANCED")
        sleep(10)
        # html > frameset > frameset > frame: nth - child(2)
        # advanced_settings_link = airties_session.find_element_by_link_text("ADVANCED SETTINGS")
        tools_link = airties_session.find_element_by_link_text("TOOLS")
        tools_link.click()
        sleep(10)
        airties_session.switch_to.default_content()
        airties_session.switch_to.frame(airties_session.find_element_by_css_selector("frame[name=mainFrame"))
        # airties_session.refresh()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__ML_restore_factory_defaults"]'))).click()
        #alert = airties_session.switch_to_alert()
        alert = airties_session.switch_to.alert()

        alert.accept()
        sleep(200)
        # restore_factory_defaults = airties_session.find_element_by_xpath
        # ('//*[@id="__ML_restore_factory_defaults"]')       # pfp1

        # should we close the seesion?--------------------------------
        airties_session.close()

    def install_airties_firmware(self, airties_ip, update_bin_file, rf, rfa):
        # print('setting 4920 with ip:' + ip_of_airties + ' to factory default' )
        print('setting 4920 with ip:' + airties_ip + ' upgrading firmware:' + update_bin_file)
        global nvg_info
        airties_url = 'http://' + airties_ip + '/'
        print('airties_url' + airties_url)
        airties_session = webdriver.Chrome()
        airties_session.get(airties_url)
        session_id = airties_session.session_id
        print(str(session_id) + '\n\n')
        airties_session.implicitly_wait(10)
        airties_session.switch_to.default_content()

        window_before = airties_session.window_handles[0]
        airties_session.switch_to.frame(airties_session.find_element_by_css_selector("frame[name=menuFrame"))

        # we need to click on this
        # //*[@id="mainlevel"]/li[3]/a this is "advanced settings"
        advanced_settings_link = airties_session.find_element_by_xpath('// *[ @ id = "mainlevel"] / li[3] / a')
        advanced_settings_link.click()
        sleep(5)
        print('click on advanced settings \n\n ')

        # i think this is tools  //*[@id="mainlevel"]/li[3]/ul/li[2]/ul/li/a
        # advanced_settings_link = airties_session.find_element_by_xpath('// *[ @ id = "mainlevel"] / li[3] / a')
        # advanced_settings_link.click()

        # this is the tools link
        tools_link = airties_session.find_element_by_xpath('// *[ @ id = "mainlevel"] / li[3] / ul / li[2] / a')
        tools_link.click()
        print('click on tools \n\n ')

        sleep(5)

        # # firm_ware_element = self.session.find_element_by_name("uploadfile")
        # firm_ware_element = self.session.find_element_by_xpath("//*[@id='firmware']")
        # firm_ware_element.send_keys(update_bin_file)
        # submit = self.session.find_element_by_name("Update")
        # submit.click()
        # airties_session.refresh()
        # firmware update link // *[ @ id = "mainlevel"] / li[3] / ul / li[2] / ul / li / a
        # window_before = airties_session.window_handles[0]
        firmware_update_link = airties_session.find_element_by_xpath(
            '// *[ @ id = "mainlevel"] / li[3] / ul / li[2] / ul / li / a')
        firmware_update_link.click()
        print('click on firmware update \n\n ')
        # airties_session.refresh()
        sleep(5)
        # window_before = airties_session.window_handles[0]
        # airties_session.switch_to.default_content()
        # handles = airties_session.window_handles
        # print('number of handles is:' + str(len(handles)))
        print(' no more handles talk')
        # // *[ @ id = "__ML_uiUpgrade"]
        # wait = WebDriverWait(airties_session, 10)
        # wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="_UploadFWFile_"]'))).click()
        airties_session.switch_to.default_content()
        sleep(5)
        airties_session.switch_to.frame(airties_session.find_element_by_css_selector("frame[name=mainFrame"))
        sleep(5)
        choose_file = airties_session.find_element_by_xpath('//*[@id="_UploadFWFile_"]')
        choose_file.send_keys(update_bin_file)

        upgrade = airties_session.find_element_by_name("upgrade")
        upgrade.click()

        WebDriverWait(airties_session, 600).until(EC.invisibility_of_element_located((By.ID, "progressbar")))
        sleep(300)
        # exit()
        # wait = WebDriverWait(airties_session, 10)
        # wait.until(EC.element_to_be_clickable((By.XPATH, '// *[ @ id = "mainlevel"] / li[3] /a'))).click()
        # exit()
        # window_after = airties_session.window_handles[1]
        # airties_session.switch_to_window(window_after)
        # airties_session.refresh()
        # start = time.time()
        # # print("starting 4920 upgrade  timer:" + str(start))
        # print("starting switching")
        # airties_session.switch_to.frame(airties_session.find_element_by_css_selector("frame[name=mainFrame"))
        # sleep(60)
        # exit()
        # loop = 1
        # while loop == 1:
        #     try: airties_session.switch_to_window(window_after)
        #     except NoSuchElementException:
        #         break
        #     else:
        #         sleep(30)
        #         print('sleeping30 secs')
        #         continue
        airties_session.switch_to.default_content()


    def set_4920_ip_list_to_factory_default(self):
        # air_ties_ip_list = []
        #show_ip_lan_dict = Nvg599Class.cli_sh_rg_ip_lan_info(self)
        show_ip_lan_dict = self.cli_sh_rg_ip_lan_info()

        # airties_4920_ip_list = []
        for ip_lan_entry in show_ip_lan_dict:
            if "ATT_4920" in show_ip_lan_dict[ip_lan_entry]["Name"]:
            # print(ip_lan_entry)
                #add this to a list which airties_4920
                print('in for loop' + show_ip_lan_dict[ip_lan_entry]["IP"])
                # airties_4920_ip_list.append(show_ip_lan_dict[ip_lan_entry]["IP"])
                self.set_4920_to_factory_default(show_ip_lan_dict[ip_lan_entry]["IP"])
                # Nvg599Class.set_4920_to_factory_default(show_ip_lan_dict[ip_lan_entry]["IP"])

        #     # self.ip_lan_connections_dict_cli[connected_device_mac] = {}
        #     ip_lan_connections_dict_cli[connected_device_mac] = {}
        #     ip_lan_connections_dict_cli[connected_device_mac]["IP"] = connected_device_ip
        #     ip_lan_connections_dict_cli[connected_device_mac]["Name"] = connected_device_name
        #     ip_lan_connections_dict_cli[connected_device_mac]["State"] = connected_device_status
        #     ip_lan_connections_dict_cli[connected_device_mac]["DHCP"] = connected_device_dhcp
        #     ip_lan_connections_dict_cli[connected_device_mac]["Port"] = connected_device_port
        #     # self.telnet_cli_session.close()
        # telnet_cli_session.close()
        # return ip_lan_connections_dict_cli
        # '88:41:FC:86:64:D4': {'device_type': 'airties_4920', 'oper_sys': 'tbd', 'radio': 'abg', 'band': '5',
        #                       'state': 'None', 'default_ssid': 'AirTies_SmartMesh_4PNF', 'default_pw': 'kykfmk8997',
        #                       'address_type': 'None', 'port': 'None', 'ssid': 'None', 'rssi': 'None', 'ip': 'None',
        #                       'device_test_name': 'airties_1_5g', 'name': 'ATT_4920_8664D4',
        #                       'location': 'master_bedroom'},
        # '88:41:FC:C3:56:C2': {'device_type': 'airties_4920', 'oper_sys': 'tbd', 'radio': 'abg', 'band': '2',
        #                       'state': 'None', 'default_ssid': 'AirTies_Air4920_33N3', 'default_pw': 'wthchc7344',
        #                       'address_type': 'None', 'port': 'None', 'ssid': 'None', 'rssi': 'None', ' ip': 'None',
        #                       'device_test_name': 'airties_2_2g', 'name': 'ATT_4920_C356C0',
        #                       'location': 'master_bedroom'},

# the only names are:  ATT_4920_C356C0  or ATT_4920_8664D4
# patches1
    def get_connected_airties_ip_from_name(self,airties_name):
        show_ip_lan_dict = self.cli_sh_rg_ip_lan_info()
        airties_4920_ip_list = []
        for ip_lan_entry in show_ip_lan_dict:
            # names are:  ATT_4920_C356C0  or ATT_4920_8664D4
            if (airties_name  ==  show_ip_lan_dict[ip_lan_entry][airties_name]) and (show_ip_lan_dict[ip_lan_entry]['State'] == "on"):
                airties_ip = show_ip_lan_dict[ip_lan_entry]["IP"]
                return airties_ip
            # this is the one we want
            else:
                print('named airties device:' + str(airties_name) + 'not assciated to RG \n')
                return "0.0.0.0"

    def get_ip_list_of_4920s(self):
        show_ip_lan_dict = self.cli_sh_rg_ip_lan_info()
        airties_4920_ip_list = []
        for ip_lan_entry in show_ip_lan_dict:
            if ("ATT_49" in show_ip_lan_dict[ip_lan_entry]['Name']) and (show_ip_lan_dict[ip_lan_entry]['State'] == "on"):
            #if "ATT_4920" in show_ip_lan_dict[ip_lan_entry]["Name"]:
                # print(ip_lan_entry)
                # add this to a list which airties_4920
                print('in for loop' + show_ip_lan_dict[ip_lan_entry]["IP"])
                airties_4920_ip_list.append(show_ip_lan_dict[ip_lan_entry]["IP"])
                #self.set_4920_to_factory_default(show_ip_lan_dict[ip_lan_entry]["IP"])
                # Nvg599Class.set_4920_to_factory_default(show_ip_lan_dict[ip_lan_entry]["IP"])
        return airties_4920_ip_list

    # review this incomplete method
    def set_fixed_ip_allocation(self):
        # dianostics_link = browser.find_element_by_link_text("Diagnostics")
        home_network_link = self.session.find_element_by_link_text("Home Network")
        home_network_link.click()
        sleep(2)
        wi_fi_link = self.session.find_element_by_link_text("IP Allocation")
        wi_fi_link.click()
        sleep(2)
        self.check_if_dac_required()
        # test_mac = '5c:f8:a1:a6:6b:b2'
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
            mac = tr.find_elements_by_xpath(".//td")[1].text.upper()
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

            print('name:', name)
            print('mac:', mac)
            print('status:', status)
            print('allocation:', allocation)
            print('action type:', type(action))
            sleep(10)
            # exit()
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
            # print("table body row is", tr)
            cells = tr.findAll('td')
            print('cells:', cells)
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
            cells = tr.find_all("td")
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

                if i == 1:
                    print('cell mac from ui is:>' + cell.text + '<')
                    wifi_ui_mac_present = cell.text.upper()
                    print('wifi_mac_present:', wifi_ui_mac_present)
                    # if the key is present it means that the device is known.
                    for key in test_house_devices_static_info.keys():
                        # print('key:', key)
                        if key == wifi_ui_mac_present:
                            print('device_test_name',
                                  test_house_devices_static_info[wifi_ui_mac_present]['device_test_name'])
                            print('device_test_name', test_house_devices_static_info[wifi_ui_mac_present]['ip'])
                            test_house_ip = test_house_devices_static_info[wifi_ui_mac_present]['ip']
                            print('th', test_house_ip)
                    break
                i = i + 1

    def adv_configure_guest_network(self, rf, rfa, enable_disable_param, guest_ssid_param = "default_guest", guest_ssid_password_param = "disabled"):
        print('in adv_configure_guest_network')
        print('enable_disable_param:' + enable_disable_param + '\n')
        home_network_link = self.session.find_element_by_link_text("Home Network")
        home_network_link.click()
        sleep(2)
        wi_fi_link = self.session.find_element_by_link_text("Wi-Fi")
        wi_fi_link.click()
        sleep(2)
        self.check_if_dac_required()
        sleep(5)
        advanced_options_link = self.session.find_element_by_link_text("Advanced Options")
        advanced_options_link.click()
        sleep(2)
        guest_ssid_enable = Select(self.session.find_element_by_id("ogssidenable"))
        current_guest_enable_state = guest_ssid_enable.first_selected_option.text
        print('selected option.text:' + str(current_guest_enable_state) + '\n')
        # selected_option = guest_ssid_enable.first_selected_option.value
        print('selected option.value:' + str(current_guest_enable_state) + '\n')
        # current_selected_option = str(current_guest_enable_state)
        if current_guest_enable_state == "off" and enable_disable_param == "off":
            # I think we are always done in this state
            print('we are done')
        else:
            # simplifies logic if is on then we just set everything again
            if enable_disable_param == 'on':
                guest_ssid_enable = Select(self.session.find_element_by_id("ogssidenable"))
                guest_ssid_enable.select_by_value('on')
                # if user enable_disable is on and the current state is on we still have to check for  password changes
                print('enable disable is on:' + enable_disable_param)
                sleep(2)
                # set the guest ssid
                guest_ssid = self.session.find_element_by_id("ossidname2")
                guest_ssid.clear()
                guest_ssid.send_keys(guest_ssid_param)

                guest_ssid_password = self.session.find_element_by_id("okey2")
                guest_ssid_password.clear()
                guest_ssid_password.send_keys(guest_ssid_password_param)

                submit = self.session.find_element_by_name("Save")
                submit.click()
                self.check_for_wifi_warning()
            else:
                guest_ssid_enable = Select(self.session.find_element_by_id("ogssidenable"))
                guest_ssid_enable.select_by_value('off')
                # lets clear the guest id password when we disable the guest_ssid
                # maybe not , it gets set when we enable the guest_ssid
                # guest_ssid_password = self.session.find_element_by_id("okey2")
                # guest_ssid_password.clear()
                submit = self.session.find_element_by_name("Save")
                submit.click()
                self.check_for_wifi_warning()

    #def conf_quest_network_ssid_and_password(self, rf, rfa, enable_disable_ssid_password, guest_ssid_password):
    def org_conf_quest_network_ssid_and_password(self, rf, rfa, enable_disable, guest_ssid, guest_password):
        # print('in enable_guest_network_and_set_password_ssid')
        # # dianostics_link = browser.find_element_by_link_text("Diagnostics")
        # home_network_link = self.session.find_element_by_link_text("Home Network")
        # home_network_link.click()
        # sleep(10)
        # # resets_link = browser.find_element_by_link_text("Resets")
        # wi_fi_link = self.session.find_element_by_link_text("Wi-Fi")
        # wi_fi_link.click()
        # sleep(2)
        # self.check_if_dac_required()
        #
        # id_password = self.session.find_element_by_id("password")
        # self.session.find_element_by_id("password").clear()
        # id_password.send_keys(ssid_password)
        # rf.write('     Setting SSID password to:' + ssid_password + '\n')
        #
        # check_password = self.session.find_element_by_id("checkpassword")
        # self.session.find_element_by_id("checkpassword").clear()
        # check_password.send_keys(ssid_password)
        #
        # guest_id_enable = self.session.find_element_by_name("gssidenable")
        # guest_id_enable.click()
        # # this is an on - off drop down
        # for option in guest_id_enable.find_elements_by_tag_name('option'):
        #     if option.text == "On":
        #         option.click()
        #
        # guest_id_password = self.session.find_element_by_id("gssidpassword")
        # self.session.find_element_by_id("gssidpassword").clear()
        # guest_id_password.send_keys(guest_ssid_password)
        #
        # guest_id_password = self.session.find_element_by_id("checkguestpassword")
        # self.session.find_element_by_id("checkguestpassword").clear()
        # guest_id_password.send_keys(guest_ssid_password)

        submit = self.session.find_element_by_name("Save")
        submit.click()
        self.check_for_wifi_warning()

    # The logic here is that is the home_password is "default" then the Security is set to "Default Password"
    def conf_home_network_ssid_and_password(self, rf, rfa, home_ssid = "default", home_password = "default"):
        global nvg_info
        print('in conf_home_network_ssid_and_password')
        # dianostics_link = browser.find_element_by_link_text("Diagnostics")
        home_network_link = self.session.find_element_by_link_text("Home Network")
        home_network_link.click()
        sleep(10)
        # resets_link = browser.find_element_by_link_text("Resets")
        wi_fi_link = self.session.find_element_by_link_text("Wi-Fi")
        wi_fi_link.click()
        sleep(2)
        self.check_if_dac_required()
        # the option to enable disable is greyed out
        # if enable_disable == "off":
        #     guest_id_enable_select = Select(self.session.find_element_by_name("gssidenable"))
        #     guest_id_enable_select.select_by_value('off')
        #     submit = self.session.find_element_by_name("Save")
        ssid_text_box = self.session.find_element_by_id("ssid")
        ssid_text_box.clear()
        #
        # "35448081188192": {'model': 'nvg599', 'device_access_code': '9==5485?6<', 'magic': 'pqomxqikedca',
        #                    'mac2g': '20:3d:66:49:85:61', 'mac5g': '20:3d:66:49:85:64', 'ssid_def_pw': 'eeh4jxmh7q26',
        #                    'ssid_def': 'ATT4ujR48s', 'ssid_3': 'ZipKey-PSK', 'ssid_3_pw': 'Cirrent1',
        #                    'ssid_4': 'ATTPOC', 'ssid_4_pw': 'Ba1tshop'}}

        if home_ssid == "default":
            home_ssid_ui = nvg_info[self.serial_number]['ssid_def']
            print('home ssid:' + str(nvg_info[self.serial_number]['ssid_def'] + ':') + '\n')
            ssid_text_box.send_keys(nvg_info[self.serial_number]['ssid_def'])
        else:
            home_ssid_ui = home_ssid
            # if not the default then the user has entered a new ssid
            ssid_text_box.send_keys(home_ssid)
            print("setting home ssid to: " + str(home_ssid) + ':\n')

        if home_password == "default":
            # here we are setting the default security and  the password
            security_selection = Select(self.session.find_element_by_id("ussidsecurity"))
            # home_password = nvg_info[self.serial_number]['ssid_def_pw']
            security_selection.select_by_value('defwpa')
            submit = self.session.find_element_by_name("Save")
            submit.click()
            self.check_for_wifi_warning()
            print('setting security setting to:' + str(security_selection) + '\n')
            # security_selection = Select(self.session.find_element_by_id("ussidsecurity"))
            # exit()

        password_link = self.session.find_element_by_id("password")
        if home_password ==  "default":
            # pass
            # we don't need any of this
            # here we are setting the default security and  the password
            home_password_ui = nvg_info[self.serial_number]['ssid_def_pw']
            # don't have to do anything
            # security_selection.select_by_value('defwpa')
            # password_link = self.session.find_element_by_id("password")
            # password_link.clear()
            print("setting home password to default : " + str(home_password_ui) + ':\n')
            # password_link.send_keys(home_password_def)
            # sleep(3)
            # security_state = security_selection.first_selected_option.text
        else:
            home_password_ui = home_password
            password_link.clear()
            password_link.send_keys(home_password_ui)
            # security_selection.select_by_value('wpa')
            # sleep(3)
            print("setting home password to: " + str(home_password_ui) + ':\n')

        submit = self.session.find_element_by_name("Save")
        submit.click()
        self.check_for_wifi_warning()
        return home_ssid_ui, home_password_ui

    def conf_guest_network_ssid_and_password(self, rf, rfa, enable_disable, guest_ssid_parm, guest_password_parm):
        global nvg_info
        print('in enable_guest_network_and_set_password_ssid')
        # dianostics_link = browser.find_element_by_link_text("Diagnostics")
        home_network_link = self.session.find_element_by_link_text("Home Network")
        home_network_link.click()
        sleep(15)
        # resets_link = browser.find_element_by_link_text("Resets")
        wi_fi_link = self.session.find_element_by_link_text("Wi-Fi")
        wi_fi_link.click()
        sleep(2)
        self.check_if_dac_required()
        if enable_disable == "off":
            guest_id_enable_select = Select(self.session.find_element_by_name("gssidenable"))
            guest_id_enable_select.select_by_value('off')
            submit = self.session.find_element_by_name("Save")
            submit.click()
            self.check_for_wifi_warning()
            print("disabling guest ssid \n")
            # Nothing left to do if we are turning off the guest newtwork
            return
        # we are turning it on or it is already on
        print("guest ssid enabled.. contuing  \n")
        guest_id_enable_select = Select(self.session.find_element_by_name("gssidenable"))
        guest_id_enable_select.select_by_value('on')
        guest_ssid_link = self.session.find_element_by_id("gssid")
        self.session.find_element_by_id("gssid").clear()

        if guest_ssid_parm == "default":
            def_ssid = nvg_info[self.serial_number]['ssid_def']
            guest_ssid_parm = def_ssid + '_Guest'
            # uest_ssid_link.send_keys(tmp_string)
            guest_ssid_link.send_keys(guest_ssid_parm)
            print('setting ssid to default ssid:' + str(guest_ssid_parm))
        else:
            # if not the default then the user has entered a new ssid
            guest_ssid_link.send_keys(guest_ssid_parm)
            print("setting guest ssid to:" + str(guest_ssid_parm) + '\n')
        # if we get here we know that he guest network is enabled  so a password is needed.
        guest_id_password_link = self.session.find_element_by_id("gssidpassword")
        self.session.find_element_by_id("gssidpassword").clear()
        guest_id_password_link.send_keys(guest_password_parm)
        print('guest password>>>>>>>>>>>>>>' + str(guest_password_parm))
        submit = self.session.find_element_by_name("Save")
        submit.click()
        self.check_for_wifi_warning()

        return guest_ssid_parm, guest_password_parm

    """ I should use this function to get the information for a specific band /guest SSID
    This would make the test case logic  easier to follow"""

    def get_ui_ssid_and_password_values(self):
        global nvg_info
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

        guest_ssid_entry = self.session.find_element_by_name("ossidname2")
        guest_ssid = guest_ssid_entry.get_attribute('value')
        guest_password_entry = self.session.find_element_by_name("okey2")
        guest_password = guest_password_entry.get_attribute('value')

        band2_ssid_entry = self.session.find_element_by_name("ossidname")
        band2_ssid = band2_ssid_entry.get_attribute('value')
        band2_password_entry = self.session.find_element_by_name("okey1")
        band2_password = band2_password_entry.get_attribute('value')

        ssid_pw_dict = {}
        ssid_pw_dict['band2'] = {}
        ssid_pw_dict['band2']['ssid'] = band2_ssid
        ssid_pw_dict['band2']['password'] = band2_password

        ssid_pw_dict['band5'] = {}
        ssid_pw_dict['band5']['ssid'] = band5_ssid
        ssid_pw_dict['band5']['password'] = band5_password

        ssid_pw_dict['guest'] = {}
        ssid_pw_dict['guest']['ssid'] = guest_ssid
        ssid_pw_dict['guest']['password'] = guest_password

        # return band2_ssid, guest_ssid, band5_ssid, band2_password, guest_password, band5_password
        return ssid_pw_dict

    def get_home_network_ip_allocation_page_source(self):
        # dianostics_link = browser.find_element_by_link_text("Diagnostics")
        home_network_link = self.session.find_element_by_link_text("Home Network")
        home_network_link.click()
        status_link = self.session.find_element_by_link_text("Wi-Fi")
        status_link.click()
        self.check_if_dac_required()
        status_link = self.session.find_element_by_link_text("IP Allocation")
        status_link.click()
        sleep(30)
        return self.session.page_source

    def get_home_network_mac_filtering_page_source(self):
        # dianostics_link = browser.find_element_by_link_text("Diagnostics")
        home_network_link = self.session.find_element_by_link_text("Home Network")
        home_network_link.click()
        status_link = self.session.find_element_by_link_text("Wi-Fi")
        status_link.click()
        self.check_if_dac_required()
        status_link = self.session.find_element_by_link_text("MAC Filtering")
        status_link.click()
        sleep(30)
        return self.session.page_source

    def get_ui_device_status_page_source(self):
        # dianostics_link = browser.find_element_by_link_text("Diagnostics")
        home_network_link = self.session.find_element_by_link_text("Device")
        home_network_link.click()
        status_link = self.session.find_element_by_link_text("Source")
        status_link.click()
        sleep(30)
        return self.session.page_source

    def get_ui_device_list_page_source(self):
        # dianostics_link = browser.find_element_by_link_text("Diagnostics")
        home_network_link = self.session.find_element_by_link_text("Device")
        home_network_link.click()
        status_link = self.session.find_element_by_link_text("Device List")
        status_link.click()
        sleep(30)
        return self.session.page_source

    def get_ui_home_network_status_page_source(self):
        # dianostics_link = browser.find_element_by_link_text("Diagnostics")
        home_network_link = self.session.find_element_by_link_text("Home Network")
        home_network_link.click()
        status_link = self.session.find_element_by_link_text("Status")
        status_link.click()
        sleep(30)
        return self.session.page_source

    def set_ui_ssid(self, ssid_band5, ssid_band2, ssid_guest):
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
    # super dog band2 method
    def adv_conf_band2_radio_ui(self, rf, rfa, band2_enable_disable_parm, mode, bandwidth, channel, power):
        mode_values = {"n-only", "b-only", "bg", "bgn", "gn"}
        bandwidth_values = {"20", "40"}
        channel_values = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"}
        power_level_int = int(power)
        power_level_range = range(0, 100)

        if mode not in mode_values:
            print('invalid mode parameter:' + mode + " cannot continue")
            return "Fail"
        if bandwidth not in bandwidth_values:
            print('invalid bandwidth parameter:' + mode + " cannot continue")
            return "Fail"
        if channel not in channel_values:
            print('invalid channel parameter:' + mode + " cannot continue")
            return "Fail"
        if power_level_int not in power_level_range:
            print('invalid power level parameter:' + mode + " cannot continue")
            return "Fail"
        # dianostics_link = browser.find_element_by_link_text("Diagnostics")
        home_network_link = self.session.find_element_by_link_text("Home Network")
        home_network_link.click()
        sleep(2)
        # resets_link = browser.find_element_by_link_text("Resets")
        wi_fi_link = self.session.find_element_by_link_text("Wi-Fi")
        wi_fi_link.click()
        sleep(2)
        print("dog0 \n")
        self.check_if_dac_required()
        print("dog1 \n")
        advanced_options_link = self.session.find_element_by_link_text("Advanced Options")
        advanced_options_link.click()
        sleep(2)
        print("dog2 \n")

        band2_enable_disable = Select(self.session.find_element_by_id("owl80211on"))
        band2_enable_disable_state = band2_enable_disable.first_selected_option.text
        print('selected option.text:' + str(band2_enable_disable_state) + '\n')
        # selected_option = guest_ssid_enable.first_selected_option.value
        # print('selected option.value:' + str(current_guest_enable_state) + '\n')
        # current_selected_option = str(current_guest_enable_state)

        print('band2_enable_disable_state:' + str(band2_enable_disable_state) + ' band2_enable_disable_parm:' + str(
            band2_enable_disable_parm) + '\n')

        if band2_enable_disable_state == "off" and band2_enable_disable_parm == "off":
            # I think we are always done in this state
            print('off and off')
            return "Pass"
        else:
            # simplifies logic if it is on then we just set everything again
            if band2_enable_disable_parm == 'on':
                band2_enable_disable_selection = Select(self.session.find_element_by_id("owl80211on"))
                band2_enable_disable_selection.select_by_value('on')
                # if user enable_disable is on and the current state is on we still have to check for  password changes
                print('enable disable is on:' + str(band2_enable_disable_state))
                sleep(2)

                mode_selection = Select(self.session.find_element_by_id("ostandard"))
                # ostandard values n-only, b-only, bg, bgn, gn
                mode_selection.select_by_value(mode)
                # if user enable_disable is on and the current state is on we still have to check for  password changes
                print('mode is :' + str(mode))
                sleep(2)

                bandwidth_selection = Select(self.session.find_element_by_id("obandwidth"))
                # ostandard values n-only, b-only, bg, bgn, gn
                bandwidth_selection.select_by_value(bandwidth)
                # if user enable_disable is on and the current state is on we still have to check for other changes
                print('mode is :' + str(bandwidth))
                sleep(2)

                channel_selection = Select(self.session.find_element_by_id("ochannelplusauto"))
                # ostandard values n-only, b-only, bg, bgn, gn
                channel_selection.select_by_value(channel)
                # if user enable_disable is on and the current state is on we still have to check for other changes
                print('channel is :' + str(channel))
                sleep(2)

                power_level = self.session.find_element_by_id("opower")
                power_level.clear()
                power_level.send_keys(power)

                submit = self.session.find_element_by_name("Save")
                submit.click()
                sleep(2)
                self.check_for_wifi_warning()

            else:
                # to get here  the current state is on but the user has selected off
                # so we turn off and return pass
                band2_enable_disable_selection = Select(self.session.find_element_by_id("owl80211on"))
                band2_enable_disable_selection.select_by_value('off')
                # if user enable_disable is on and  current state is on we still have to check for any password changed

                submit = self.session.find_element_by_name("Save")
                submit.click()
                sleep(2)
                self.check_for_wifi_warning()

            return "Pass"

        # adv_conf band2 home

        # we want to use the same session but the dict of connected devices is a temporary value subject to change
        # super dog band2 method
    def adv_conf_band2_home(self, rf, rfa, band2_home_ssid_enable_disable_parm, ssid_name, hide_ssid_name, security, wpa_version, password, wpa_setup_on_off, max_clients):
        security_values = {"none", "wpa", "defwpa"}
        wpa_version_values = {"2", "both"}

        if security not in security_values:
            print('invalid security_values parameter:' + str(security) + " cannot continue")
            return "Fail"
        if wpa_version not in wpa_version_values:
            print('invalid security parameter:' + str(wpa_version) + " cannot continue")
            return "Fail"

        # dianostics_link = browser.find_element_by_link_text("Diagnostics")
        home_network_link = self.session.find_element_by_link_text("Home Network")
        home_network_link.click()
        sleep(2)
        # resets_link = browser.find_element_by_link_text("Resets")
        wi_fi_link = self.session.find_element_by_link_text("Wi-Fi")
        wi_fi_link.click()
        sleep(2)
        print("dog0 \n")
        self.check_if_dac_required()
        print("dog1 \n")
        advanced_options_link = self.session.find_element_by_link_text("Advanced Options")
        advanced_options_link.click()
        sleep(2)
        print("dog2 \n")

        band2_home_ssid_enable_disable = Select(self.session.find_element_by_id("oussidenable"))
        band2_home_ssid_enable_disable_state = band2_home_ssid_enable_disable.first_selected_option.text
        print('selected option.text:' + str(band2_home_ssid_enable_disable_state) + '\n')
        # selected_option = guest_ssid_enable.first_selected_option.value
        # print('selected option.value:' + str(current_guest_enable_state) + '\n')
        # current_selected_option = str(current_guest_enable_state)

        print('band2_enable_disable_state:' + str(band2_home_ssid_enable_disable_state) + ' band2_enable_disable_parm:' + str(band2_home_ssid_enable_disable_parm) + '\n')

        if band2_home_ssid_enable_disable_state == "off" and band2_home_ssid_enable_disable_parm == "off":
            # I think we are always done in this state
            print('off and off')
            return "Pass"
        else:
            # simplifies logic if it is on then we just set everything again
            if band2_home_ssid_enable_disable_parm == 'on':
                band2_home_ssid_enable_disable_selection = Select(self.session.find_element_by_id("oussidenable"))
                band2_home_ssid_enable_disable_selection.select_by_value('on')
                # if user enable_disable is on and the current state is
                # on we still have to check for any password changed
                print('home ssid enable=disable is on:' + str(band2_home_ssid_enable_disable_state))
                sleep(2)

                # ssid
                ssid_name_entry = self.session.find_element_by_id("ossidname")
                ssid_name_entry.clear()
                ssid_name_entry.send_keys(ssid_name)

                band2_home_hide_ssid_selection = Select(self.session.find_element_by_id("ohide"))
                band2_home_hide_ssid_selection.select_by_value(hide_ssid_name)
                # if user enable_disable is on and the current state is on we still have to check for  password changes
                print('hide home ssid:' + str(hide_ssid_name))

                security_selection = Select(self.session.find_element_by_id("osecurity"))
                security_selection.select_by_value(security)
                # if user enable_disable is on and the current state is on we still have to check for  password changes
                print('security selection:' + str(hide_ssid_name))

                wpa_version_selection = Select(self.session.find_element_by_id("owpaversion"))
                # ostandard values n-only, b-only, bg, bgn, gn
                wpa_version_selection.select_by_value(wpa_version)
                # if user enable_disable is on and the current state is on we still have to check for  password changes
                print('wpa version  is :' + str(wpa_version))
                sleep(2)

                # if the securiy is set to WPA Default password then we cannot change the password
                if security != 'defwpa':
                    password_entry = self.session.find_element_by_id("okey1")
                    password_entry.clear()
                    password_entry.send_keys(password)

                wpa_setup_on_off_selection = Select(self.session.find_element_by_id("owps"))
                # ostandard values n-only, b-only, bg, bgn, gn
                wpa_setup_on_off_selection.select_by_value(wpa_setup_on_off)
                # if user enable_disable is on and the current state is on we still have to check for  password changes
                print('wpa_setup_on_off:' + str(wpa_setup_on_off))
                sleep(2)
# wpa_setup_on_off, max_clients):
                # ssid
                max_clients_entry = self.session.find_element_by_id("omaxclients")
                max_clients_entry.clear()
                max_clients_entry.send_keys(max_clients)


                submit = self.session.find_element_by_name("Save")
                submit.click()
                sleep(2)
                self.check_for_wifi_warning()

            else:
                # to get here  the current state is on but the user has selected off
                # so we turn off and return pass
                band2_home_network_enable_disable_selection = Select(self.session.find_element_by_id("oussidenable"))
                band2_home_network_enable_disable_selection.select_by_value(band2_home_ssid_enable_disable_parm)
                # if user enable_disable is on and the current state is
                # on we still have to check for any password changed
                print('band2_home_ssid_enable_disable_selection:' + str(band2_home_ssid_enable_disable_parm))

                submit = self.session.find_element_by_name("Save")
                submit.click()
                sleep(2)
                self.check_for_wifi_warning()

            return "Pass"

    # config adv band2 home

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

    # was called  check_for_wifi_security_and_regular_warning(self):
    def check_for_wifi_warning(self):
        print('in check_for_wifi_warning ')
        # warning = self.session.find_element_by_name("ReturnWarned")
        # we get this warning every time so we don't have to check for no such exception
        try:
            wi_fi_warning = self.session.find_element_by_class_name("warning")
        except NoSuchElementException:
            return_string = "Wi-Fi Warning not detected."
            return return_string

        if wi_fi_warning:
            print("Wi-Fi Warning displayed ")
            # submit = self.session.find_element_by_name("ReturnWarned")
            # displayed_text = self.session.page_source
            # sleep(5)

            # submit = self.session.find_element_by_name("ReturnWarned")
            submit = self.session.find_element_by_name("Continue")

            submit.click()
            # return_string = "wi-fi security change... Continue"
            print("wi-fi security change... Continue")

            # not sure if we need this
            # just click if we get a warning

            # if "Wi-Fi security that is not recommended." in displayed_text:
            #     submit = self.session.find_element_by_name("ReturnWarned")
            #     submit.click()
            #     return_string = "wi-fi security change... Continue"
            #     print("wi-fi security change... Continue")
            #     return return_string

            # if "You have made a change to your Wi-Fi configuration" in displayed_text:
            #     submit = self.session.find_element_by_name("Continue")
            #     submit.click()
            #     return_string = "wi-fi regular warning change... Continue"
            #     print("wi-fi regular warning change... Continue")
            #     return return_string

    # I think this is only be used for the password testcases
    def xcheck_for_wifi_warning(self):
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

    def install_rg_cli(self, tftp_server_name, install_bin_file, rf, rfa):
        future = rfa
        print('in install_rg_cli: installing' + str(install_bin_file))
        test_status = 'Pass'
        telnet_cli_session = self.login_nvg_599_cli()
        # nvg_599_dut.login_nvg_599_cli()
        ip_lan_info_dict = self.cli_sh_rg_ip_lan_info()
        server_ip = "0.0.0.0"

        # ip_lan_connections_dict_cli[connected_device_mac] = {}
        # ip_lan_connections_dict_cli[connected_device_mac]["IP"] = connected_device_ip
        # ip_lan_connections_dict_cli[connected_device_mac]["Name"] = connected_device_name
        # ip_lan_connections_dict_cli[connected_device_mac]["State"] = connected_device_status
        # ip_lan_connections_dict_cli[connected_device_mac]["DHCP"] = connected_device_dhcp
        # ip_lan_connections_dict_cli[connected_device_mac]["Port"] = connected_device_port
        # self.telnet_cli_session.close()

        for device_mac in ip_lan_info_dict:
            # if tftp_server_name ==
            # ip_lan_info_dict[device_mac]['Name'] && ip_lan_info_dict[device_mac]["State"]=="on":
            if (ip_lan_info_dict[device_mac]["State"] == "on") \
                    and (ip_lan_info_dict[device_mac]['Name'] == tftp_server_name):
                print('inputname:' + tftp_server_name + '  name_from_dict:' +
                      ip_lan_info_dict[device_mac]['Name'] + '\n')
                server_ip = ip_lan_info_dict[device_mac]['IP']

        if server_ip != "0.0.0.0":
            # note_8_ip = ip_lan_info_dict['b8:d7:af:aa:27:c3']['IP']
            # device_ip = ip_lan_info_dict[device_mac]['IP']
            rf.write('    TFTP server IP  present in cli command sh ip lan: ' + server_ip)
            print('tftp server is present :' + str(server_ip))
        else:
            rf.write('    TFTP server IP not present in cli command sh ip lan, Aborting test')
            print('TFTP  server IP not present in cli command sh ip lan')
            test_status = "Fail"
            return test_status

        telnet_cli_session.sendline("install " + server_ip + " " + install_bin_file)
        telnet_cli_session.expect('confirm')
        telnet_cli_session.sendline("yes")
        # telnet_cli_session.expect('OCKED>')
        sleep(300)
        print('we woke up after 5 mins \n')

        return test_status

    def upgrade_rg(self, update_bin_file, rf, rfa):
        print('in upgrade_rg')
        sleep(10)
        # exit()
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
            except TimeoutError:
                print('Not ready, sleeping 10 seconds')
                sleep(10)
                print('time: ' + str(time.time()))
                continue

            except (HTTPError, URLError) as e:
                print('HTTP Error: ' + str(e))
                sleep(10)
                print('time' + str(time.time()))
                continue
            except timeout:
                print('Socket timeout error')
                return "Fail: socket timeout Error"

        end = time.time()
        duration = round(end - start)
        print("upgrade duration in seconds:", duration)
        rf.write("    RG  Upgrade to:" + update_bin_file + " Pass " + '\n')
        rfa.write("    RG  Upgrade to:" + update_bin_file + " Pass " + '\n')
        rf.write("        RG  Upgrade Duration:" + str(duration) + '\n')
        rfa.write("        RG  Upgrade Duration:" + str(duration) + '\n')
        sleep(200)
        return "Pass"

    def check_if_dac_required(self):
        try:
            # dac_access_challenge = self.session.find_element_by_link_text("Forgot your Access Code?")
            self.session.find_element_by_link_text("Forgot your Access Code?")
            print('DAC requested.. sending DAC')
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

        # self.login_4920('192.168.1.67')

        try:
            sleep(4)
            self.session.find_element_by_xpath('//*[@id="content-sub"]/div[1]/h1')
            print('session in check:' + str(self.session))
            print('WiFi warning displayed')
            print('Clicking on Continue')
            submit = self.session.find_element_by_name("Continue")

            # print('--in check_if_wifi  before click login')
            # airties_cli_session = self.login_4920('192.168.1.67')
            # print('session before:' + str(airties_cli_session) + '\n\n\n')
            #
            # print('basic session before session:' + str(self.session) + '\n\n\n')
            # print('basic session after:' + str(self.session) + '\n\n\n')
            # print('in ifconfig before click  click----------------------\n ')
            # sleep(5)
            # cmd = "route"
            # # cmd = "ping -c5 " + "192.168.1.67"
            # try:
            #     output = subprocess.check_output(cmd, shell=True)
            # except subprocess.CalledProcessError as e:
            #     print('errror ' + e.output)
            # else:
            #     print('these are the interface outputs' + str(output))
            #     print('just a test' + str(output) + '\n')
            # # cmd = "nmcli dev wifi"

            submit.click()

            # this is where it fails for some reason that I have not figured out

            # print('basic session after:' + str(self.session) + '\n\n\n')
            # print('in ifconfig after click \n')
            # print('---------------------------\n')
            # sleep(5)
            # cmd = "route"
            # # cmd = "ping -c5 " + "192.168.1.67"
            # try:
            #     output = subprocess.check_output(cmd, shell=True)
            # except subprocess.CalledProcessError as e:
            #     print('errror ' + e.output)
            # else:
            #     print('these are the interface outputs' + str(output))
            #     print('just a test' + str(output) + '\n')
            # # cmd = "nmcli dev wifi"
            # try:
            #     output = subprocess.check_output(cmd, shell=True)
            # except subprocess.CalledProcessError as e:
            #     print(e.output)
            # else:
            #     print('these are the xnetworks' + str(output))
            #     print('just a test' + str(output) + '\n')
        except NoSuchElementException:
            print('Wi-Fi warning not displayed - Continuing')
        try:
            sleep(2)
            self.session.find_element_by_xpath('//*[@id="error-message-text"]')
            print('in check_if_wifi  after changes saved')
        except NoSuchElementException:
            print('No save confirmation')

        # print('basic session after returning from try:' + str(self.session) + '\n\n\n')

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

    def rg_setup_without_factory_reset(self, rf, rfa):
        self.turn_off_supplicant_cli(rf, rfa)
        # sleep(120)
        self.enable_sshd_ssh_cli(rf, rfa)
        # sleep(120)
        self.conf_tr69_eco_url(rf, rfa)
        # sleep(120)
        self.turn_off_wi_fi_security_protection_cli(rf, rfa)
        sleep(20)
        # not sure why this failed
        self.enable_parental_control(rf, rfa)

        rg_url = 'http://192.168.1.254/'
        self.session = webdriver.Chrome()
        self.session.get(rg_url)
        # self.enable_guest_network_and_set_password_ssid(rf, rfa)
        # .session.close()

    @staticmethod
    def factory_test():
        loop = 1
        start = time.time()
        while loop == 1:
            try:
                test_req = urllib.request.Request("http://192.168.1.254/")
                urllib.request.urlopen(test_req, timeout=420)
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

    def factory_reset_rg(self, rf, rfa):
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

        self.session.close()
        start = time.time()
        print("starting timer:" + str(start))
        loop = 1
        while loop == 1:
            try:
                test_req = urllib.request.Request("http://192.168.1.254/")
                urllib.request.urlopen(test_req, timeout=300)
                # response.read().decode("utf-8", 'ignore')
                end = time.time()
                print("Duration time till login:", str(round(end - start)))
                sleep(20)
                break
            # except:
            # need to check if this works
            except TimeoutError:
                print('Not ready, sleeping 10 seconds')
                sleep(10)
                print('time: ' + str(time.time()))
                continue

            except (HTTPError, URLError) as e:
                print('HTTP Error: ' + str(e))
                sleep(10)
                print('time:' + str(round(time.time())))
                continue
            except timeout:
                print('Socket timeout error')

                # except URLError as e:
                #   print('URL Error: ' + str(e))
                #   sleep(10)
                #   print('time' + str(time.time()))
                #   continue

        end = time.time()
        duration = str(round(end - start))
        print("Duration in seconds:", str(round(end - start)))
        rf.write("  RG Factory Reset Duration:" + duration + '\n')
        rfa.write("  RG Factory Reset Duration:" + duration + '\n')
        duration = str(round(end - start))
        #
        sleep(300)
        self.turn_off_supplicant_cli(rf, rfa)
        # sleep(120)
        self.enable_sshd_ssh_cli(rf, rfa)
        # sleep(120)
        self.conf_tr69_eco_url(rf, rfa)
        # sleep(120)
        self.turn_off_wi_fi_security_protection_cli(rf, rfa)
        sleep(20)
        # not sure why this failed
        self.enable_parental_control(rf, rfa)

        rg_url = 'http://192.168.1.254/'
        self.session = webdriver.Chrome()
        self.session.get(rg_url)
        # self.enable_guest_network_and_set_passwords(rf, rfa)
        sleep(60)
        return duration

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
        print(' Airties5a \n')
        # handle being asked for password
        # self.session = self.check_if_dac_required()
        self.check_if_dac_required()
        sleep(5)
        advanced_options_link = self.session.find_element_by_link_text("Advanced Options")
        advanced_options_link.click()
        sleep(2)
        # print('after advanced options')
        # self.login_4920('192.168.1.67')
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
            print('in 5g')
            # self.login_4920('192.168.1.67')
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
            print('in 6g')
            submit = self.session.find_element_by_name("Save")
            submit.click()
            # print('in 7g')
            # self.login_4920('192.168.1.67')
            self.check_if_wifi_warning_displayed()
            return self.session

    # palmer@palmer-Latitude-E5450:~$ nmcli dev wifi | grep AirTies
    # I think I have to diable the wired connection on the RG. Then

    # super dog
    def get_nmcli_networks(self):
        print('in wps_pair_default_airties')
        # nmcli connection down id "Wired connection 1
        #  nmcli connection show --active
        nmcli_wifi_dict = {}
        cmd = ""
        try:
            output = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError as e:
            print(e.output)
        else:
            print('rescan')
            sleep(3)
        cmd = "nmcli dev wifi"
        try:
            output = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError as e:
            print(e.output)
        else:
            line_list = output.decode('utf-8').splitlines()
            # line_list = output.splitlines()
            for line in line_list:
                line = line.split()
                print('line:' + str(line))
                if line[0] == 'IN-USE':
                    continue

                if line[0] == '*':
                    active_ssid = nmcli_ssid = line[0]
                    print('active ssid' + str(active_ssid))
                    nmcli_ssid = line[1]
                    print('ssid' + str(nmcli_ssid) + '\n')
                    nmcli_mode = line[2]
                    # print("connectedDeviceStatus", ip_lan_output_split[3])
                    nmcli_chan = line[3]
                    # nmcli_ssid("connectedDeviceDHCP", ip_lan_output_split[4])
                    nmcli_rate = line[4]
                    print('rate' + str(nmcli_rate) + '\n')

                    # print("connectedDeviceSSIDNumber", ip_lan_output_split[5])
                    nmcli_rate_units = line[5]
                    nmcli_signal = line[6]
                    nmcli_security = line[8]
                    nmcli_wifi_dict[nmcli_ssid] = {}
                    # do I need the above?
                    nmcli_wifi_dict[nmcli_ssid]['MODE'] = nmcli_mode
                    nmcli_wifi_dict[nmcli_ssid]["CHAN"] = nmcli_chan
                    nmcli_wifi_dict[nmcli_ssid]["RATE"] = nmcli_rate
                    nmcli_wifi_dict[nmcli_ssid]["rate_units"] = nmcli_rate_units
                    nmcli_wifi_dict[nmcli_ssid]["SIGNAL"] = nmcli_signal
                    nmcli_wifi_dict[nmcli_ssid]["SECURITY"] = nmcli_security
                    continue
                    #    print("this is an airties device!")
                    # print("connectedDeviceIP", line[1])
                nmcli_ssid = line[0]
                print('ssid' + str(nmcli_ssid) + '\n')
                nmcli_mode = line[1]
                # print("connectedDeviceStatus", ip_lan_output_split[3])
                nmcli_chan = line[2]
                # nmcli_ssid("connectedDeviceDHCP", ip_lan_output_split[4])
                nmcli_rate = line[3]
                print('rate' + str(nmcli_rate) + '\n')

                # print("connectedDeviceSSIDNumber", ip_lan_output_split[5])
                nmcli_rate_units = line[4]
                nmcli_signal = line[5]
                nmcli_security = line[7]

                nmcli_wifi_dict[nmcli_ssid] = {}
                # do I need the above?
                nmcli_wifi_dict[nmcli_ssid]['MODE'] = nmcli_mode
                nmcli_wifi_dict[nmcli_ssid]["CHAN"] = nmcli_chan
                nmcli_wifi_dict[nmcli_ssid]["RATE"] = nmcli_rate
                nmcli_wifi_dict[nmcli_ssid]["rate_units"] = nmcli_rate_units
                nmcli_wifi_dict[nmcli_ssid]["SIGNAL"] = nmcli_signal
                nmcli_wifi_dict[nmcli_ssid]["SECURITY"] = nmcli_security

            return nmcli_wifi_dict
            # exit()
            # print('these are the networks' + str(output))

    def wps_pair_default_airties(self, airties_network):
        print('in wps_pair_default_airties')
        # nmcli connection down id "Wired connection 1
        #  nmcli connection show --active
        cmd = "nmcli dev wifi rescan"
        try:
            output = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError as e:
            print(e.output)
        else:
            print(output)
        cmd = "nmcli dev wifi"
        try:
            output = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError as e:
            print(e.output)
        else:
            print('these are the xnetworks' + str(output))

        #     '88:41:FC:86:64:D6': {'device_type': 'airties_4920', 'oper_sys': 'tbd', 'radio': 'abg', 'band': '2',
        #                           'state': 'None', 'default_ssid': 'AirTies_SmartMesh_4PNF',
        #                           'default_pw': 'kykfmk8997',
        #                           'address_type': 'None', 'port': 'None', 'ssid': 'None',
        #                           'rssi': 'None', 'ip': 'None',
        # we have to check to see if the airties network is present
        for key in airties_4920_defaults:
            if airties_4920_defaults[key]['default_ssid'] == airties_network:
                print(airties_4920_defaults[key]['default_pw'])
                cmd = "nmcli device wifi connect " + airties_network + " " + "password " + \
                      airties_4920_defaults[key]['default_pw']
                # may not need the password
                # cmd = "nmcli device wifi connect " + airties_network

                print('basbaglan dbg: ' + str(cmd))

                # may add this to all these calls to subprocess,check_output

                try:
                    output = subprocess.check_output(cmd, shell=True)
                except subprocess.CalledProcessError as e:
                    print(e.output)

                else:
                    for line in output.splitlines():
                        print('out1  ===========\n', line)
                    sleep(10)

        # cmd = "nmcli con down AirTies_SmartMesh_4PNF"

        # output = subprocess.check_output(['nmcli', 'r'],shell=True)
        # output = subprocess.check_output(cmd, shell=True)
        # for line in output.splitlines():
        #     print('out1  ===========\n', line)
        # sleep(10)
        # cmd = "nmcli con down ATTqbrAnYs"
        # cmd = "nmcli device wifi connect AirTies_SmartMesh_4PNF kykfmk8997"
        # use  the password from the table
        # cmd = "nmcli device wifi connect " + airties_network + " kykfmk8997"
        cmd = "nmcli connect up " + airties_network
        # output = subprocess.check_output(['nmcli', 'r'],shell=True)
        output = subprocess.check_output(cmd, shell=True)
        for line in output.splitlines():
            print('out2===========\n', line)
        sleep(10)
        # this is wrong becasue we want ot login to the airties not t he RG
        self.airties_ap_cli_session = pexpect.spawn("telnet 192.168.2.254", encoding='utf-8')
        self.airties_ap_cli_session.expect('ogin:')
        self.airties_ap_cli_session.sendline('root')
        self.airties_ap_cli_session.expect("#")
        self.airties_ap_cli_session.sendline('basbaglan')
        self.airties_ap_cli_session.expect("#")
        self.airties_ap_cli_session.sendline('exit')
        self.airties_ap_cli_session.close()
        cmd = "nmcli con down " + airties_network
        # cmd = "nmcli con down AirTies_SmartMesh_4PNF"
        output = subprocess.check_output(cmd, shell=True)

        print('output from SmartMesh down', output)
        # cmd = "nmcli device wifi connect ATTqbrAnYs ggtxstgwipcg"
        # how do I know this?
        cmd = "nmcli connect up ATTqbrAnYs"
        # -------------------------------------------------------???
        output = subprocess.check_output(cmd, shell=True)
        print('output from reconnect', output)
        print('Clicking on WPS button')
        # rg_url = 'http://192.168.1.254/'
        self.session.get(self.rg_url)
        status_link = self.session.find_element_by_link_text("Home Network")
        status_link.click()
        sleep(2)
        home_network_link = self.session.find_element_by_link_text("Wi-Fi")
        home_network_link.click()
        sleep(2)
        self.check_if_dac_required()
        wps_button = self.session.find_element_by_name("pb1")
        wps_button.click()
        sleep(30)

    def set_wifi_power_level(self, band, percentage):
        print('Adjusting ' + band + ' wifi power level to ' + str(percentage) + '%')
        rg_url = 'http://192.168.1.254/'
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

        if band == "band2":
            band2_power = self.session.find_element_by_id("opower")
            band2_power.clear()
            band2_power.send_keys(percentage)
            submit = self.session.find_element_by_name("Save")
            sleep(10)
            submit.click()
        else:
            # this is band5
            band2_power = self.session.find_element_by_id("tpower")
            band2_power.clear()
            band2_power.send_keys(percentage)
            submit = self.session.find_element_by_name("Save")
            sleep(10)
            submit.click()

        # submit = self.session.find_element_by_name("Save")
        # sleep(2)
        # submit.click()
        self.check_for_wifi_warning()
        # self.check_for_wifi_warning()

    # This needs an enable disable ar

    def disable_enable_wifi_2_4g(self, off_on):
        print('disable_enable_wifi_2_4, setting 2.4G to:' + off_on)
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
            # The value passed in would be either Off or On
            if option.text == off_on:
                option.click()
                break
        sleep(10)
        submit = self.session.find_element_by_name("Save")
        sleep(10)
        submit.click()
        self.check_for_wifi_warning()
        # self.session.implicitly_wait(5)
        # wi_fi_2_4 = self.session.find_element_by_name("owl80211on")
        # wi_fi_2_4.click()
        #
        # for option in wi_fi_2_4.find_elements_by_tag_name('option'):
        #     if option.text == "On":
        #         option.click()
        #         break
        #
        # wi_fi_5_g = self.session.find_element_by_name("twl80211on")
        # wi_fi_5_g.click()
        #
        # for option in wi_fi_5_g.find_elements_by_tag_name('option'):
        #     if option.text == "On":
        #         option.click()
        #         break
        # submit = self.session.find_element_by_name("Save")
        # sleep(10)
        # submit.click()
        # self.check_for_wifi_warning()
        # # self.check_for_wifi_warning()

    # parm must be Off or On with capitalized first letter
    def disable_enable_wifi_5g(self, off_on):
        # print('in disable_enable_wifi_2_4_and_5g_wifi')
        print('disable_enable_wifi_5g_wifi, setting 5G to:' + off_on)
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

        # wi_fi_2_4 = self.session.find_element_by_name("owl80211on")
        #
        # for option in wi_fi_2_4.find_elements_by_tag_name('option'):
        #     # this is problematic line
        #     if option.text == "Off":
        #         option.click()
        #         break
        # sleep(10)
        # self.session.implicitly_wait(5)
        wi_fi_5_g = self.session.find_element_by_name("twl80211on")
        # wi_fi_5_g.click()
        for option in wi_fi_5_g.find_elements_by_tag_name('option'):
            # if option.text == "Off":
            if option.text == off_on:
                option.click()
                break
        submit = self.session.find_element_by_name("Save")
        sleep(10)
        submit.click()

        # self.check_for_wifi_security_and_regular_warning()
        # self.session.implicitly_wait(5)
        # wi_fi_2_4 = self.session.find_element_by_name("owl80211on")
        # wi_fi_2_4.click()
        #
        # for option in wi_fi_2_4.find_elements_by_tag_name('option'):
        #     if option.text == "On":
        #         option.click()
        #         break
        #
        # wi_fi_5_g = self.session.find_element_by_name("twl80211on")
        # wi_fi_5_g.click()
        #
        # for option in wi_fi_5_g.find_elements_by_tag_name('option'):
        #     if option.text == "On":
        #         option.click()
        #         break
        # submit = self.session.find_element_by_name("Save")
        # sleep(10)
        # submit.click()
        self.check_for_wifi_warning()
        ################################################

    def ui_disable_enable_wifi_2_4_and_5g_wifi(self):
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

        self.check_for_wifi_warning()
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
        self.check_for_wifi_warning()
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
        print('Setting  pasword:  ui_set_password')
        rg_url = 'http://192.168.1.254/'
        self.session.get(rg_url)
        status_link = self.session.find_element_by_link_text("Home Network")
        status_link.click()
        sleep(2)
        home_network_link = self.session.find_element_by_link_text("Wi-Fi")
        home_network_link.click()
        sleep(2)
        self.check_if_dac_required()
        ussidsecurity_select = Select(self.session.find_element_by_id("ussidsecurity"))
        ussidsecurity_select.select_by_visible_text(security)
        if security == "Custom Password":
            password_input = self.session.find_element_by_id("password")
            password_input.clear()
            password_input.send_keys(password)
        submit = self.session.find_element_by_name("Save")
        sleep(10)
        submit.click()
        print('password len before check:' + str(len(password)))
        self.check_for_wifi_warning()
        return_str = self.check_for_wifi_warning()
        return return_str

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

    def xget_ui_system_information(self):
        print('in get_ui_system_information)')
        global nvg_info
        rg_url = 'http://192.168.1.254/'
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
    def wait_for_ssh_to_be_ready(host, port, timeout_parm, retry_interval):
        print('in wait_for_ssh_to_be_read')
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        retry_interval = float(retry_interval)
        my_timeout = int(timeout_parm)
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

    @staticmethod
    # this doesn't return anythin useful
    def get_wifi_info_from_android_termux(wifi_info_ip):
        print('in get_wifi_connection_info_from_android_termux')
        ssh_client = pxssh.pxssh(timeout=100, encoding='ascii', maxread=5000, options={"StrictHostKeyChecking": "no"})
        ssh_client.PROMPT = 'r[#$]'
        # ssh_client.login(wifi_info_ip, username='None', port=8022, auto_prompt_reset='False', sync_multiplier=5)
        ssh_client.login(wifi_info_ip, username='None', port=8022, original_prompt=r'[#$]',
                         auto_prompt_reset=False, sync_multiplier=5, quiet=False, login_timeout=10)
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

        # ssh_client.expect(".*\$ ")
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
    def execute_speedtest_from_android_termux(speed_test_ip, rf, rfa):
        print('execute_speedtest_from_android_termux')
        # rfa = "future"
        excel_cell = rfa
        # prompt = '\$\s+'
        # prompt = '\$'
        # sort of works-----------
        # ssh_client = paramiko.SSHClient()
        # ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # sleep(10)
        # ssh_client= pxssh.pxssh()
        # ssh_client = pxssh.pxssh(options={"StrictHostKeyChecking": "no","AutoPromptReset": "True"})
        # not sure if this is defined like this
        # ssh_client = pxssh.pxssh(timeout=200,
        # encoding='utf-8',options={"StrictHostKeyChecking": "no","AutoPromptReset": "True"})
        # ssh_client = pxssh.pxssh(timeout=200, encoding='utf-8')
        print('1')

        ssh_client = pxssh.pxssh(timeout=200, encoding='utf-8', options={"StrictHostKeyChecking": "no"})
        hostname = speed_test_ip
        # ssh_client.login(hostname, username=None, port=8022)
        try:
            # ssh_client.PROMPT='$'
            ssh_client.login(hostname, username=None, auto_prompt_reset=True, quiet=False, sync_multiplier=5, port=8022)
            rf.write('    Logged in to ' + speed_test_ip + '\n')
            print("logged in to note8 \n")

        except pxssh.ExceptionPxssh as e:
            print('pxssh failed to login')
            ssh_client.close()
            rf.write('    Failed to log in to: ' + speed_test_ip + '  Aborting test \n')
            rf.write('    Error:' + str(e) + '\n')
            print(str(e))
            return "Fail"
        print('2')
        print('2.5')
        ssh_client.prompt()
        print('3')
        ssh_client.sendline('speedtest  --server 5024')
        print('4')
        ssh_client.prompt()
        print('5')
        # speed_test_output_b = ssh_client.before
        speed_test_output = ssh_client.before
        # print(ssh_client.before)
        print('after conversion to string', speed_test_output)
        # this is waht I added
        ssh_client.sendline('exit')
        down_load_speed, up_load_speed = 0, 0
        speed_test_regex = re.compile(r'Download:\s+(\d+\.\d+)\s+\w+.*Upload:\s+(\d+\.\d+)\s+\w+', re.DOTALL)
        speed_test_groups = speed_test_regex.search(speed_test_output)
        try:
            print('download:', speed_test_groups.group(1))
            print('upload:', speed_test_groups.group(2))
            down_load_speed = speed_test_groups.group(1)
            rf.write('    Download speed ' + down_load_speed + '\n')
            up_load_speed = speed_test_groups.group(2)
            rf.write('    Upload speed ' + up_load_speed + '\n\n')

        except AttributeError:
            print("something wrong- closing ssh_client session")
            down_load_speed = 'Fail'
            up_load_speed = 'Fail'
            # return down_load_speed, up_load_speed
        finally:
            ssh_client.close()
            return down_load_speed, up_load_speed

    # nmcli connection delete id xATT2anR4b8
    #  nmcli connection show
    #  nmcli connection show --active
    # nmcli con down "Wired connection 1"

    # @staticmethod
    # def nmcli_get_active_connections():
    #     # command = 'nmcli c'
    #     # cmd = "nmcli r all"
    #     cmd = "nmcli connection show --active "
    #     # output = subprocess.check_output(['nmcli', 'r'],shell=True)
    #     output = subprocess.check_output(cmd, shell=True)
    #     connection_list = []
    #     active_connection_list = []
    #     # output = output.decode('utf-8')
    #     # tmp_list = []
    #     for line in output.splitlines():
    #         line = line.decode('utf-8')
    #         tmp_list = line.split()
    #         if tmp_list[0] == 'NAME':
    #             continue

    @staticmethod
    def nmcli_get_active_connections():
        cmd = "nmcli connection show --active"
        output = subprocess.check_output(cmd, shell=True)
        active_connection_list = []
        for line in output.splitlines():
            line = line.decode('utf-8')
            tmp_list = line.split()
            if tmp_list[0] == 'NAME':
                continue
            active_connection_list.append(tmp_list[0])
        print('active connection list', *active_connection_list)
        return active_connection_list
        # print(tmp_list[0])
        # sleep(10)
        # cmd = "nmcli con down ATTqbrAnYs"
        # cmd = "nmcli device wifi connect AirTies_SmartMesh_4PNF kykfmk8997"

    @staticmethod
    def nmcli_get_connections():
        cmd = "nmcli connection show "
        # output = subprocess.check_output(['nmcli', 'r'],shell=True)
        output = subprocess.check_output(cmd, shell=True)
        connection_list = []
        active_connection_list = []
        for line in output.splitlines():
            line = line.decode('utf-8')
            nmcli_active_dict = {}
            tmp_list = line.split()
            if tmp_list[0] == 'NAME':
                continue
            if tmp_list[0] == 'Wired':
                wired_name = tmp_list[0] + " " + tmp_list[1] + " " + tmp_list[2]
                print('wired_name:', wired_name)
                connection_list.append(wired_name)
                if tmp_list[3] == "--":
                    continue
                else:
                    active_connection_list.append(tmp_list[0])
            else:
                connection_list.append(tmp_list[0])
                if tmp_list[3] == "--":
                    continue
                else:
                    active_connection_list.append(tmp_list[0])

        # print('connection list', *connection_list)
        # print('active connection list', *active_connection_list)
        return connection_list, active_connection_list
        # print(tmp_list[0])
        # sleep(10)
        # cmd = "nmcli con down ATTqbrAnYs"
        # cmd = "nmcli device wifi connect AirTies_SmartMesh_4PNF kykfmk8997"

    @staticmethod
    def nmcli_set_connection(cmd):
        # command = 'nmcli c'
        # cmd = "nmcli r all"
        # cmd = "nmcli con " + command + " " + nmcli_connection_name +  " password " + password
        # cmd = "nmcli device wifi  " + command + " " + nmcli_ssid +  " password " + nmcli_password
        # output = subprocess.check_output(['nmcli', 'r'],shell=True)
        # out = check_output(["ls -la"].decode("utf-8").shell=True)
        try:
            # out = subprocess.check_output("ping -c" + str(number_of_pings) + " " +
            #                             remote_ip, shell=True).decode("utf-8")
            output = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError as e:
            print('nmcli command error:' + str(cmd), e)
            output = "ping fail"
            return output

        print('nmcli command pass:' + str(cmd))

        # output = subprocess.check_output(cmd, shell=True)
        for line in output.splitlines():
            print('cmd output', line)
        sleep(3)
        # exit()
        # # cmd = "nmcli con down ATTqbrAnYs"
        # cmd = "nmcli device wifi connect AirTies_SmartMesh_4PNF kykfmk8997"
        # # output = subprocess.check_output(['nmcli', 'r'],shell=True)
        # output = subprocess.check_output(cmd, shell=True)
        # for line in output.splitlines():
        #     print('out  nmcli test  ===========\n', line)

        # 'AirTies_SmartMesh_4PNF', 'default_pw': 'kykfmk8997',
        # this command lists all the visble APS
        # iwlist wlp2s0 s
        # this command turns off the current Wfi connect
        # this command connects to the wifi , it generates an 802.1x supplicant fail message but seems to work
        # sudo nmcli device wifi connect AirTies_Air4920_33N3 wthchc7344

    @staticmethod
    def nmcli_get_connections_test():
        global nvg_info

        # nmcli connection show - -active
        # command = 'nmcli c'
        # cmd = "nmcli r all"
        cmd = "nmcli con show"
        # output = subprocess.check_output(['nmcli', 'r'],shell=True)
        output = subprocess.check_output(cmd, shell=True)
        for line in output.splitlines():
            print('out  dog  ===========\n', line)
        sleep(10)
        # cmd = "nmcli con down ATTqbrAnYs"
        # cmd = "nmcli device wifi connect AirTies_SmartMesh_4PNF kykfmk8997"
        # output = subprocess.check_output(['nmcli', 'r'],shell=True)
        output = subprocess.check_output(cmd, shell=True)

        return output
        # for line in output.splitlines():
        # 'AirTies_SmartMesh_4PNF', 'default_pw': 'kykfmk8997',
        # this command lists all the visble APS
        # iwlist wlp2s0 s
        # this command turns off the current Wfi connect
        # this command connects to the wifi , it generates an 802.1x supplicant fail message but seems to work
        # sudo nmcli device wifi connect AirTies_Air4920_33N3 wthchc7344

    @staticmethod
    def nmcli_test():
        # nmcli connection show - -active
        # command = 'nmcli c'
        # cmd = "nmcli r all"
        cmd = "nmcli con down ATTqbrAnYs"
        # output = subprocess.check_output(['nmcli', 'r'],shell=True)
        output = subprocess.check_output(cmd, shell=True)
        for line in output.splitlines():
            print('out  dog  ===========\n', line)
        sleep(10)
        # cmd = "nmcli con down ATTqbrAnYs"
        cmd = "nmcli device wifi connect AirTies_SmartMesh_4PNF kykfmk8997"
        # output = subprocess.check_output(['nmcli', 'r'],shell=True)
        output = subprocess.check_output(cmd, shell=True)
        for line in output.splitlines():
            print('out  nmcli test  ===========\n', line)

        # 'AirTies_SmartMesh_4PNF', 'default_pw': 'kykfmk8997',
        # this command lists all the visble APS
        # iwlist wlp2s0 s
        # this command turns off the current Wfi connect
        # this command connects to the wifi , it generates an 802.1x supplicant fail message but seems to work
        # sudo nmcli device wifi connect AirTies_Air4920_33N3 wthchc7344

    @staticmethod
    def ping_from_local_host(remote_ip, number_of_pings=10):
        print('ping ' + remote_ip + ' from_local_host')
        try:
            out = subprocess.check_output("ping -c" + str(number_of_pings) + " " +
                                          remote_ip, shell=True).decode("utf-8")
        except subprocess.CalledProcessError as e:
            print('ping error', e)
            return '0', '0', '0', '0', '0', '0', '0'
        # result = os.system(cmd)
        print('out===========\n', out)
        # ping_statistics = re.compile(r'statistics ---.*(\d+)\spackets\.*(\d+)\sreceived',re.DOTALL)
        # don't need .DOTALL because everythin is on one line
        ping_info_reg_ex = re.compile(r'rtt.*?=\s(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)')
        print('out2===========\n', out)
        print('endout2===========\n')
        # pingInfoRegEx = re.compile(r'.*?rtt/s+=/s+(/d+/./d+)',re.DOTALL)
        mo1 = ping_info_reg_ex.search(out)
        min_ping = mo1.group(1)
        print('min:' + min_ping + '\n')
        avg_ping = mo1.group(2)
        print('avg:' + avg_ping + '\n')
        max_ping = mo1.group(3)
        print('max:' + max_ping + '\n')
        mdev_ping = mo1.group(4)
        print('mdev:' + mdev_ping + '\n')
        ping_statistics = re.compile(r'statistics ---\s(\d+)\spackets.*\s(\d+)\sreceived,\s(\d+)%')
        stats = ping_statistics.search(out)
        try:
            print('sent:>' + stats.group(1) + ' received:' + stats.group(2) + 'loss:' + stats.group(3))
        except AttributeError:
            print("something wrong - aborting")
            return 0, 0, 0, 0, 0, 0, 0
            # return down_load_speed, up_load_speed
        # print('sent:>' + stats.group(1) + ' received:' + stats.group(2) + 'loss:' + stats.group(3))
        sent = stats.group(1)
        print('sent:' + sent + '\n')
        # sleep(10)
        received = stats.group(2)
        print('rec:' + received + '\n')
        # sleep(10)
        loss = stats.group(3)
        print('loss:' + loss + '\n')
        # sleep(10)
        return min_ping, avg_ping, max_ping, mdev_ping, sent, received, loss

    @staticmethod
    def ping_check(remote_ip):
        print('In ping_check')
        # out = subprocess.check_output("ping -c10 " + remote_ip, shell=True).decode("utf-8")
        try:
            out = subprocess.check_output("ping -c10 " + remote_ip, shell=True).decode("utf-8")
            print('ping out:' + out + '\n')
            ping_info_reg_ex = re.compile(r'(\d+.*loss)')
            ping_status = ping_info_reg_ex.search(out)
            print('ping result:', ping_status.group(1))
            return "Pass"
        except subprocess.CalledProcessError as e:
            print('ping error:', e.output)
            # e.returncode = 0
            ping_fail_str = str(e.output)
            ping_fail_return = "Ping_failed  ping fail str:" + ping_fail_str
            print('ping failed:' + ping_fail_str)

            return "Fail"

    # experiemtntal
    def tftp_list_test(self, *file_list):
        for x in file_list:
            print(x)

    # we want to pass in a remote file source in case we are getting  files from somewhere else-- do I need a put?
    # def tftp_get_file_cli(self, remote_file_source, *source_device_list):

    def tftp_get_file_cli(self, tftp_server_name, firmware_to_get, rf, rfa):
        result = "Pass"
        print('in tftp_get_file \n\n')
        show_ip_lan_dict = self.cli_sh_rg_ip_lan_info()
        print('show_ip_lan_dict:' + str(show_ip_lan_dict) + '\n\n')
        # show_ip_lan_dict = Nvg599Class.cli_sh_rg_ip_lan_info(self)
        source_device_ip = 0
        for ip_lan_entry in show_ip_lan_dict:
            print('remote_source: ' + str(tftp_server_name) + 'Name:' + str(
                show_ip_lan_dict[ip_lan_entry]["Name"]) + '\n\n')

            if tftp_server_name == show_ip_lan_dict[ip_lan_entry]["Name"]:
                # print(ip_lan_entry)
                print('*****************dbg for loop' + show_ip_lan_dict[ip_lan_entry]["IP"] + '\n\n')
                source_device_ip = show_ip_lan_dict[ip_lan_entry]["IP"]
        if source_device_ip == 0:
            print('in didnt get the IP, should never happen \n\n')
            result = "Fail"

        # remote_file_source
        tftp_session = pexpect.spawn("tftp " + str(source_device_ip), encoding="utf-8", cwd="/home/palmer/Downloads")
        # tftp_session = pexpect.spawn("tftp " + remote_file_source, encoding="utf-8", cwd="/home/palmer/Downloads")
        #
        print('in tftp_get_file1: ' + str(source_device_ip) + '\n\n')

        tftp_session.expect("tftp>")
        print('in tftp_get_file2 \n\n')

        tftp_session.sendline("get " + firmware_to_get)
        print('in tftp_get_file3 \n\n')

        tftp_session.expect("tftp>", timeout=60)
        sleep(4)
        print('remote 3:' + str(tftp_session.before) + '\n')
        tftp_session.close()
        return result


    # pfp ******  moved to parent class forget it for now
    def xxlogin_nvg_599_cli(self):
        print('In login_nvg_5g_cli')
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

    def tftp_rg_firmware_from_cli(self):
        print('In login_nvg_5g_cli')
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

    def login_nvg_599_band5_cli(self):
        print('In login_nvg_5g_cli')
        self.telnet_cli_session = pexpect.spawn("telnet 192.168.1.254", encoding='utf-8')
        self.telnet_cli_session.expect("ogin:")
        self.telnet_cli_session.sendline('admin')
        self.telnet_cli_session.expect("ord:")
        nvg_dac = self.device_access_code
        self.telnet_cli_session.sendline(nvg_dac)
        self.telnet_cli_session.expect(">")
        self.telnet_cli_session.sendline('magic')
        self.telnet_cli_session.expect(">")
        self.telnet_cli_session.sendline('telnet 203.0.113.2')
        self.telnet_cli_session.expect('#')
        self.telnet_cli_session.sendline('export LD_LIBRARY_PATH=/lib:/airties/lib')
        self.telnet_cli_session.expect("#")
        self.telnet_cli_session.sendline('export PATH=$PATH:/airties/usr/sbin')
        self.telnet_cli_session.expect("#")
        return self.telnet_cli_session

    # super pfp
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

    # def login_nvg_cli_ssh(self):
    def xlogin_nvg_599_cli(self):
        print('In xlogin_nvg_cli, enabling airties lib')
        ssh_cli_session = pexpect.spawn("ssh remotessh@192.168.1.254", encoding='utf-8')
        ssh_cli_session.expect("ord:")
        ssh_cli_session.sendline('alcatel')
        ssh_cli_session.expect(">")
        ssh_cli_session.sendline('magic')
        ssh_cli_session.expect(">")
        return ssh_cli_session

    @staticmethod
    def static_login_nvg_599_cli():
        print('In static_login_nvg_cli')
        telnet_cli_session = pexpect.spawn("telnet 192.168.1.254", encoding='utf-8')
        telnet_cli_session.expect("ogin:")
        telnet_cli_session.sendline('admin')
        telnet_cli_session.expect("ord:")
        telnet_cli_session.sendline('<<01%//4&/')
        telnet_cli_session.expect(">")
        telnet_cli_session.sendline('magic')
        telnet_cli_session.expect("UNLOCKED>")
        sleep(120)
        return telnet_cli_session

    def login_4920(self, ip_4920):
        print('In login_4920' + '\n')
        self.telnet_cli_session = pexpect.spawn("telnet " + ip_4920, encoding='utf-8')
        self.telnet_cli_session.expect("ogin:")
        self.telnet_cli_session.sendline('root')
        self.telnet_cli_session.expect("#")
        #self.telnet_cli_session.sendline('wl -i wl1 status')
        #self.telnet_cli_session.expect("#")
        #status_output = self.telnet_cli_session.before
        # print(status_output)
        return self.telnet_cli_session
        # exit()
        # airties_wl_dict = {}
        # air_cli_session = pexpect.spawn("telnet " + ip_4920, encoding='utf-8')
        #self.telnet_cli_session = pexpect.spawn("telnet 192.168.1.254", encoding='utf-8')
        print("===============  this is the command telnet " + str(ip_4920) + '\n')
        # session = pexpect.spawn("telnet 192.168.1.254", encoding='utf-8')
        self.air_cli_session = pexpect.spawn("telnet " + ip_4920, encoding = 'utf-8')
        # self.air_cli_session.sendline('\n')
        sleep(1)
        print('1')
        self.air_cli_session.expect("ogin:")
        print('2')
        self.air_cli_session.sendline('root')
        print('3')
        self.air_cli_session.expect("#")
        print('4')
        status_output = self.air_cli_session.before
        print(status_output)
        return self.air_cli_session

    @staticmethod
    def static_reset_4920(ip_4920):
        print('In static_reset_4920')
        cli_session = pexpect.spawn("telnet " + ip_4920, encoding='utf-8')
        cli_session.expect("ogin:")
        cli_session.sendline('root')
        cli_session.expect("#")
        cli_session.sendline('defaults')
        cli_session.expect("Responses")
        sleep(20)
        cli_session.close()

    def get_4920_uptime(self, ip_airties):
        print('In get_4920_uptime')
        print('ip is:' + str(ip_airties))

        cli_session = pexpect.spawn("telnet " + ip_airties, encoding='utf-8')
        cli_session.expect("ogin:")
        cli_session.sendline('root')
        cli_session.expect("#")
        cli_session.sendline('uptime')
        cli_session.expect("#")
        status_output = cli_session.before
        print(str(status_output))
        return status_output

    def get_4920_ssid(self, ip_4920):
        print('In get_4920_ssid')
        cli_session = pexpect.spawn("telnet " + ip_4920, encoding='utf-8')
        cli_session.expect("ogin:")
        cli_session.sendline('root')
        cli_session.expect("#")
        cli_session.sendline('wl -i wl1 status')
        cli_session.expect("#")
        status_output = cli_session.before
        # print(status_output)
        airties_wl_dict = {}
        # #status_info_reg_ex = re.compile(r'SSID:\s+\"(\w+)Model\s(\w+)\s+\w+/\w+.*number\s+(\w+).
        # *Uptime\s+(\d\d:\d\d:\d\d:\d\d)',re.DOTALL)
        # status_info_reg_ex = re.compile(r'SSID:\s+\"(\w+)',re.DOTALL)
        status_info_reg_ex = re.compile(r'SSID:\s"(\w+)"\s*?Mode:\s(\w+)\s*?RSSI:\s(\d+).*?noise:\s-(\d+).*?Channel:\s(\d+).*?BSSID:\s(\w+:\w+:\w+:\w+:\w+:\w+)',re.DOTALL)
        # print('status_output' + str(status_output) + '\n')
        mo1 = status_info_reg_ex.search(status_output)
        print('ssid:' + str(mo1.group(1)) + '\n')
        print('Mode:' + str(mo1.group(2)) + '\n')
        print('RSSI:' + str(mo1.group(3)) + '\n')
        print('noise:' + str(mo1.group(4)) + '\n')
        print('channel:' + str(mo1.group(5)) + '\n')
        print('BSSID:' + (str(mo1.group(6)).lower()) + '\n')
        sleep(5)
        # mo1 = status_info_reg_ex.search(status_output)
        airties_wl_dict['ssid'] = str(mo1.group(1))
        airties_wl_dict['mode'] = str(mo1.group(2))
        airties_wl_dict['rssi'] = str(mo1.group(3))
        airties_wl_dict['noise'] = str(mo1.group(4))
        airties_wl_dict['channel'] = str(mo1.group(5))
        airties_wl_dict['bssid'] = str(mo1.group(6)).lower()
        cli_session.close()
        return airties_wl_dict

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

    #     @staticmethod
    #     def get_tr69_ssid_status_cli(ssid):
    #         telnet_cli_session = login_nvg_599_cli()
    #         telnet_cli_session.sendline('magic')
    #         telnet_cli_session.expect("UNLOCKED>")
    #         telnet_cli_session.sendline('tr69 tr69 GetParameterValues InternetGatewayDevice.
    #         LANDevice.1.WLANConfiguration.' + ssid + '.Enable')
    #         telnet_cli_session.expect(".*UNLOCKED>")
    #         status_output = telnet_cli_session.before
    #         status_info_reg_ex = re.compile(r'Enable\s(\d)')
    #         status = status_info_reg_ex.search(status_output)
    #         print('returning SSID:' + ssid + ' Status:' + status )
    #         telnet_cli_session.close()
    #

    def get_tr69_auto_setup_ssid_status_cli(self, ssid):
        self.telnet_cli_session = self.login_nvg_599_cli()
        self.telnet_cli_session.sendline('magic')
        self.telnet_cli_session.expect("MAGIC/UNLOCKED>")
        self.telnet_cli_session.sendline('tr69 GetParameterValues InternetGatewayDevice.LANDevice.1.WLANConfiguration.'
                                         + str(ssid) + '.Enable')
        self.telnet_cli_session.expect("MAGIC/UNLOCKED>")
        status_output = self.telnet_cli_session.before
        print('status_output:' + status_output)
        status_info_reg_ex = re.compile(r'Enable\s(\d)')
        status = status_info_reg_ex.search(status_output)
        status1 = status.group(1)
        print('returning SSID:' + str(ssid) + ' Status:' + str(status1))
        self.telnet_cli_session.close()
        return str(status)

    def get_auto_setup_ssid_via_tr69_cli_authentication(self, ssid, expected_authentication_type):
        self.telnet_cli_session = self.login_nvg_599_cli()
        self.telnet_cli_session.sendline('magic')
        self.telnet_cli_session.expect("MAGIC/UNLOCKED>")
        self.telnet_cli_session.sendline('tr69 GetParameterValues InternetGatewayDevice.LANDevice.1.'
                                         'WLANConfiguration.3.X_0000C5_Authentication')
        self.telnet_cli_session.expect("MAGIC/UNLOCKED>")
        print('Getting ssid:' + str(ssid) + ' authentication type')

        status_output = self.telnet_cli_session.before
        status_info_reg_ex = re.compile(r'Authentication\s(\w+)', re.DOTALL)
        authentication_type = status_info_reg_ex.search(status_output)
        # print('tr69 authentication_type:' + str(authentication_type))
        print('expected Authentication type:' + str(expected_authentication_type))
        tr69_auth_type = authentication_type.group(1)
        print('tr69 Authentication type:' + str(tr69_auth_type))
        if tr69_auth_type == expected_authentication_type:
            print('Pass-------------------')
        self.telnet_cli_session.close()
        return tr69_auth_type

    def get_tr69_parameters_for_ssid(self, ssid_number):
        self.telnet_cli_session = self.login_nvg_599_cli()
        self.telnet_cli_session.sendline('magic')
        self.telnet_cli_session.expect("MAGIC/UNLOCKED>")
        self.telnet_cli_session.sendline('tr69 GetParameterValues InternetGatewayDevice.LANDevice.1.'
                                         'WLANConfiguration.' + ssid_number + '.')
        self.telnet_cli_session.expect("MAGIC/UNLOCKED>")
        tr69_output = self.telnet_cli_session.before
        self.telnet_cli_session.close()
        return tr69_output

    def set_auto_setup_ssid_via_tr69_cli(self, ssid_number, max_clients, rf, rfa):
        future = rfa
        print('Enabling tr69 auto_setup for ssid number:' + str(ssid_number))
        self.telnet_cli_session = self.login_nvg_599_cli()
        self.telnet_cli_session.sendline('magic')
        self.telnet_cli_session.expect("MAGIC/UNLOCKED>")
        self.telnet_cli_session.sendline('tr69 SetParameterValues InternetGatewayDevice.LANDevice.1.WLANConfiguration.'
                                         + str(ssid_number) + '.Enable = 1')
        rf.write('     Set Enable.' + ssid_number + '.Enable 0:OK\n')
        self.telnet_cli_session.expect("MAGIC/UNLOCKED>")
        self.telnet_cli_session.sendline('tr69 SetParameterValues InternetGatewayDevice.LANDevice.1.WLANConfiguration.'
                                         + str(ssid_number) + '.BeaconAdvertisementEnabled = 1')
        rf.write('     Enable.' + ssid_number + 'BeaconAdvertisementEnabled:OK\n')
        self.telnet_cli_session.expect("MAGIC/UNLOCKED>")
        self.telnet_cli_session.sendline('tr69 SetParameterValues InternetGatewayDevice.LANDevice.1.WLANConfiguration.'
                                         + str(ssid_number) + '.SSIDAdvertisementEnabled= 1')
        rf.write('     Enable.' + ssid_number + 'SSIDAdvertisementEnabled:OK\n')
        self.telnet_cli_session.expect("MAGIC/UNLOCKED>")
        self.telnet_cli_session.sendline('tr69 SetParameterValues InternetGatewayDevice.LANDevice.1.WLANConfiguration.'
                                         + str(ssid_number) + '.X_0000C5_MaxClients=' + max_clients)
        # InternetGatewayDevice.LANDevice.1.WLANConfiguration.4..X_0000C5_MaxClients
        # rf.write("    Enabled auto ssid " + str(ssid_number) + '\n')
        rf.write('     Enable auto ssid' + ssid_number + ':OK\n')
        self.telnet_cli_session.close()
        return "Pass"

    # IPV6 is not currently available in the test house
    @staticmethod
    def enable_ipv6_via_tr69_cli(self):
        self.telnet_cli_session = self.login_nvg_599_cli()
        self.telnet_cli_session.sendline('magic')
        self.telnet_cli_session.expect("UNLOCKED>")
        self.telnet_cli_session.sendline('tr69 SetParameterValues InternetGatewayDevice.IP.X_ATT_IPv6EnableLAN=TRUE')
        self.telnet_cli_session.expect("successful.*>")

        self.telnet_cli_session.sendline('tr69 SetParameterValues InternetGatewayDevice.WANDevice.1.'
                                         'WANConnectionDevice.1.WANIPConnection.2.DNSServers=10.8.200.16,10.8.50.251')
        self.telnet_cli_session.expect("successful.*>")

        self.telnet_cli_session.sendline('tr69 SetParameterValues InternetGatewayDevice.WANDevice.1.'
                                         'WANConnectionDevice.1.WANIPConnection.2.DNSOverrideAllowed=FALSE')
        self.telnet_cli_session.expect("successful.*>")

        self.telnet_cli_session.sendline('tr69 SetParameterValues InternetGatewayDevice.IP.IPv6Enable=1')
        self.telnet_cli_session.expect("successful.*>")

        self.telnet_cli_session.sendline('tr69 SetParameterValues InternetGatewayDevice.IPv6rd.Enable=1')
        self.telnet_cli_session.expect("successful.*>")

        self.telnet_cli_session.sendline('tr69 SetParameterValues InternetGatewayDevice.IPv6rd.'
                                         'InterfaceSetting.1.SPIPv6Prefix=2001:470:8c13::/48')
        self.telnet_cli_session.expect("successful.*>")

        self.telnet_cli_session.sendline('tr69 SetParameterValues InternetGatewayDevice.IPv6rd'
                                         '.InterfaceSetting.1.IPv4MaskLength=20')
        self.telnet_cli_session.expect("successful.*>")

        self.telnet_cli_session.sendline('tr69 SetParameterValues InternetGatewayDevice.IPv6rd'
                                         '.InterfaceSetting.1.BorderRelayIPv4Addresses=10.8.50.126')
        self.telnet_cli_session.expect("successful.*>")

        self.telnet_cli_session.sendline('tr69 SetParameterValues InternetGatewayDevice.IPv6rd''.'
                                         'InterfaceSetting.1.AllTrafficToBorderRelay=1')
        self.telnet_cli_session.expect("successful.*>")

        self.telnet_cli_session.sendline('tr69 SetParameterValues InternetGatewayDevice.IPv6rd.'
                                         'InterfaceSetting.1.X_ATT_ConfigurationSource=CWMP')
        self.telnet_cli_session.expect("successful.*>")

        print('Enabled IPV6 via cli tr69')
        self.telnet_cli_session.close()

    def enable_sshd_ssh_cli(self, rf, rfa):
        self.telnet_cli_session = self.login_nvg_599_cli()
        self.telnet_cli_session.sendline('magic')
        self.telnet_cli_session.expect("UNLOCKED>")
        self.telnet_cli_session.sendline('tr69 SetParameterValues InternetGatewayDevice.X_0000C5_Debug.SshdEnabled=1')
        self.telnet_cli_session.expect("successful.*>")
        rf.write("    Enabled Sshd" + '\n')
        rfa.write("    Enabled Sshd" + '\n')
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
    def enable_parental_control(self, rf, rfa):
        self.telnet_cli_session = self.login_nvg_599_cli()
        self.telnet_cli_session.sendline('magic')
        self.telnet_cli_session.expect("UNLOCKED>")
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
        rf.write("    Enabled parental control" + '\n')
        rfa.write("    Enabled parental control" + '\n')
        print("Enabled_parental_contol")

    def conf_tr69_eco_url(self, rf, rfa):
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
        rf.write("    Configured TR69 ECO" + '\n')
        rfa.write("    Configured TR69 ECO" + '\n')
        print('Configured TR069 ECO url')
        self.telnet_cli_session.close()

    def turn_off_supplicant_cli(self, rf, rfa):
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
        rf.write("    Turned off supplicant" + '\n')
        rfa.write("    Turned off supplicant" + " Pass " + '\n')
        print('Turned off system supplicant')
        self.telnet_cli_session.close()

    def turn_off_wi_fi_security_protection_cli(self, rf, rfa):
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
        rf.write("    Turned off WiFi security protection" + '\n')
        rfa.write("    Turned off WiFi security protection" + '\n')
        print('Turned off WiFi security protection')
        self.telnet_cli_session.close()

    def get_rg_band2_status_cli(self):
        print('in get_rg_band2_status_cli\n')
        self.telnet_cli_session = self.login_nvg_599_cli()
        self.telnet_cli_session.sendline('wl status')
        self.telnet_cli_session.expect('>')
        status_output = self.telnet_cli_session.before
        band2_cli_dict = {}
        status_info_reg_ex = re.compile(
            r'SSID:\s"(\w+)"\s*?Mode:\s(\w+)\s*?RSSI:\s(\d+).*?noise:\s-(\d+).*?Channel:\s(\d+).*?BSSID:\s(\w+:\w+:\w+:\w+:\w+:\w+)',
            re.DOTALL)
        print('status_output' + str(status_output) + '\n')
        mo1 = status_info_reg_ex.search(status_output)
        # print('ssid:' + str(mo1.group(1)) + '\n')
        # print('Mode:' + str(mo1.group(2)) + '\n')
        # print('RSSI:' + str(mo1.group(3)) + '\n')
        # print('noise:' + str(mo1.group(4)) + '\n')
        # print('channel:' + str(mo1.group(5)) + '\n')
        # print('BSSID:' + (str(mo1.group(6)).lower()) + '\n')
        # sleep(5)
        # exit()
        mo1 = status_info_reg_ex.search(status_output)
        band2_cli_dict['ssid'] = str(mo1.group(1))
        band2_cli_dict['mode'] = str(mo1.group(2))
        band2_cli_dict['rssi'] = str(mo1.group(3))
        band2_cli_dict['noise'] = str(mo1.group(4))
        band2_cli_dict['channel'] = str(mo1.group(5))
        band2_cli_dict['bssid'] = str(mo1.group(6)).lower()
        self.telnet_cli_session.close()
        return band2_cli_dict

    def get_rg_band5_status_cli(self):
        print('in get_rg_band5_status_cli\n')
        self.telnet_cli_session = self.login_nvg_599_band5_cli()
        band5_cli_dict = {}
        self.telnet_cli_session.sendline('wl status')
        self.telnet_cli_session.expect('#')
        status_output = self.telnet_cli_session.before
        status_info_reg_ex = re.compile(
            r'SSID:\s"(\w+)"\s*?Mode:\s(\w+)\s*?RSSI:\s(\d+).*?noise:\s-(\d+).*?Channel:\s(\d+)/(\d+).*?BSSID:\s(\w+:\w+:\w+:\w+:\w+:\w+)',
            re.DOTALL)
        print('status_output' + str(status_output) + '\n')
        mo1 = status_info_reg_ex.search(status_output)
        band5_cli_dict['ssid'] = str(mo1.group(1))
        band5_cli_dict['mode'] = str(mo1.group(2))
        band5_cli_dict['rssi'] = str(mo1.group(3))
        band5_cli_dict['noise'] = str(mo1.group(4))
        band5_cli_dict['channel'] = str(mo1.group(5))
        band5_cli_dict['bandwidth'] = str(mo1.group(6))
        band5_cli_dict['bssid'] = str(mo1.group()).lower()
        self.telnet_cli_session.close()
        return band5_cli_dict

    def urllib_get_rg_file(self, rg_url_to_return, rf, rfa):
        print('in url get')
        # with urllib.request.urlopen('http://192.168.1.254/ATT/topology') as response:
        with urllib.request.urlopen(rg_url_to_return, data=None, timeout=3) as response:
            html_response = response.read()
            encoding = response.headers.get_content_charset('utf-8')
            decoded_html = html_response.decode(encoding)
            print('decoded_html:' + decoded_html)
            return decoded_html
            # with open('/home/palmer/Downloads/newdog.txt', 'w') as fd:
            #    fd.write(decoded_html)
            # print(response.read())
            # print('response.text' + response.text)
            # print(respprint(onse.content())
        # urllib.request.urlretrieve(rg_url, filename=url_temp_file)
        # urllib.request.urlretrieve(rg_url)

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

    def cli_sh_rg_ip_lan_info(self):
        telnet_cli_session =self.login_nvg_599_cli()
        # telnet_cli_session = Nvg599Class.static_login_nvg_599_cli()
        #  = Nvg599Class.login_nvg_599_cli(self)

        # self.telnet_cli_session. sendline("show ip lan")
        telnet_cli_session.sendline("show ip lan")
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

    def get_tr69_auto_ssid(self, ssid):
        self.telnet_cli_session = self.login_nvg_599_cli()
        self.telnet_cli_session.sendline('magic')
        self.telnet_cli_session.expect("UNLOCKED>")
        self.telnet_cli_session.sendline(
            'tr69 GetParameterValues InternetGatewayDevice.LANDevice.1.WLANConfiguration.' + ssid + '.')
        self.telnet_cli_session.expect("UNLOCKED>")
        tr69_auto_ssid_default = self.telnet_cli_session.before
        return tr69_auto_ssid_default

    from xml.etree.ElementTree import fromstring, ElementTree

    def get_rg_airties_band5_wds_links(self, rf, rfa):
        print('get_rg_airties_5g_wds_links')
        # with urllib.request.urlopen('http://192.168.1.254/ATT/topology') as response:
        band5_cli_session = self.login_nvg_599_band5_cli()
        band5_cli_session.sendline('cat /tmp/airtiesfs/aircdf-writable-config.xml.00')
        band5_cli_session.expect('#')
        status_output = band5_cli_session.before
        status_info_reg_ex = re.compile(r'(<config\sversion.*?</config>)', re.DOTALL)
        mo1 = status_info_reg_ex.search(status_output)
        # print(mo1.group())
        tree = ElementTree(fromstring(mo1.group()))
        # tree = ETree.fromstring(peers_xml)
        # print(str(tree))
        # print('1--------------------\n')
        # print(ETree.tostring(tree.getroot()))
        root = tree.getroot()
        print('2---:' + root.tag + '\n')
        peer_list = []
        for peer in root.iter('peer'):
            print(str(peer.attrib['address']))
            peer_list.append(peer.attrib['address'])
            # print(peer_list)
            # rf.close()
            # rfa.close()
            # exit()
            # rfa.write(mo1.group())
            # return mo1.group()
        return peer_list
        # print('decoded_html:' + decoded_html)
        # return decoded_html
        # with open('/home/palmer/Downloads/newdog.txt', 'w') as fd:
        #    fd.write(decoded_html)
        # print(response.read())
        # print('response.text' + response.text)
        # print(respprint(onse.content())
        # urllib.request.urlretrieve(rg_url, filename=url_temp_file)
        # urllib.request.urlretrieve(rg_url)

    def session_cleanup(self):
        pass

    def enable_monitor_mode(self):
        print('in enable monitor mode')

        password = "pfpalmer"
        proc = Popen("sudo -S  /etc/init.d/network-manager  start".split(), stdin=PIPE, stdout=PIPE, stderr=PIPE)
        proc.communicate(password.encode())
        stdout = proc.communicate()[0]
        print('stdout' + stdout)

#        cmd = "sudo /etc/init.d/network-manager  stop"
#         try:
#             output = subprocess.check_output(cmd, shell=True)
#         except subprocess.CalledProcessError as e:
#             print(e.output)
#         else:
#             print(output)
#
#         cmd = "nmcli dev wifi"
# palmer@palmer-Latitude-E5450:~$ sudo /etc/init.d/network-manager  stop
# [sudo] password for palmer:
# [ ok ] Stopping network-manager (via systemctl): network-manager.service.
# palmer@palmer-Latitude-E5450:~$ sudo ifconfig wlp2s0 down

# palmer@palmer-Latitude-E5450:~$ sudo iwconfig wlp2s0 mode monitor
# palmer@palmer-Latitude-E5450:~$ sudo ifconfig wlp2s0 up
# palmer@palmer-Latitude-E5450:~$ sudo ifconfig wlp2s0 channel 40
# ^C
# palmer@palmer-Latitude-E5450:~$ sudo iwconfig wlp2s0 channel 100
# palmer@palmer-Latitude-E5450:~$ sudo /etc/init.d/network-manager  stop
# [sudo] password for palmer:
# [ ok ] Stopping network-manager (via systemctl): network-manager.service.
# palmer@palmer-Latitude-E5450:~$ sudo ifconfig wlp2s0 down
# palmer@palmer-Latitude-E5450:~$ sudo ifconfig wlp2s0 mode monitor
# mode: Unknown host
# ifconfig: `--help' gives usage information.
# palmer@palmer-Latitude-E5450:~$ sudo iwconfig wlp2s0 mode monitor
# palmer@palmer-Latitude-E5450:~$ sudo ifconfig wlp2s0 up
# palmer@palmer-Latitude-E5450:~$ sudo ifconfig wlp2s0 channel 40
# ^C
# palmer@palmer-Latitude-E5450:~$ sudo iwconfig wlp2s0 channel 40
# palmer@palmer-Latitude-E5450:~$ sudo iwconfig wlp2s0 channel 100
# sudo /etc/init.d/network-manager  stop
# palmer@palmer-Latitude-E5450:~$ sudo /etc/init.d/network-manager  stop
# [ ok ] Stopping network-manager (via systemctl): network-manager.service.
# palmer@palmer-Latitude-E5450:~$
# palmer@palmer-Latitude-E5450:~$ sudo iwconfig wlp2s0 mode managed
# Error for wireless request "Set Mode" (8B06) :
#     SET failed on device wlp2s0 ; Device or resource busy.
# palmer@palmer-Latitude-E5450:~$ sudo ifconfig  wlan down
# wlan: ERROR while getting interface flags: No such device
# palmer@palmer-Latitude-E5450:~$ sudo iwconfig  wlan down
# iwconfig: unknown command "down"
# palmer@palmer-Latitude-E5450:~$ sudo ifconfig  wlp2s0 down
# palmer@palmer-Latitude-E5450:~$ sudo iwconfig wlp2s0 mode managed
# palmer@palmer-Latitude-E5450:~$ sudo ifconfig  wlp2s0 up
# palmer@palmer-Latitude-E5450:~$ sudo iwconfig  wlan up
# iwconfig: unknown command "up"
# palmer@palmer-Latitude-E5450:~$ sudo ifconfig  wlan up
# wlan: ERROR while getting interface flags: No such device
# palmer@palmer-Latitude-E5450:~$ sudo iwconfig  wlan up
# iwconfig: unknown command "up"
# palmer@palmer-Latitude-E5450:~$ sudo iwconfig  wlp2s0  up
# iwconfig: unknown command "up"
# palmer@palmer-Latitude-E5450:~$ sudo ifconfig  wlp2s0  up
# palmer@palmer-Latitude-E5450:~$ sudo /etc/init.d/network-manager  start
# [ ok ] Starting network-manager (via systemctl): network-manager.service.
# palmer@palmer-Latitude-E5450:~$
