from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# import itertools
import pprint
# import global.py
# import time
# from  pprint import pprint

# import requests
# from bs4 import BeautifulSoup
# import requests
# from selenium import webdriver
# import urllib3
import re
import smtplib
import sys
from time import sleep
from datetime import datetime

import pexpect
from rgclass import Nvg599Class
# from rgclass import NON_DFS_CHANNELS
# from rgclass import DFS_CHANNELS
# from rgclass import  test_house_devices_static_info

NON_DFS_CHANNELS = {36,40,44,48,149,153,157,161,165}
DFS_CHANNELS     = {52,56,60,64,100,104,108,112,116,132,136,140,144}

# from rgclass import  NON_DFS_CHANNELS
# from rgclass import  DFS_CHANNELS
# Find the current channel used for 5G
# Check the 5G channel used. If none DFS , set to DFS and note the setting
# enter the command to simulate radar detection
# verify that the channel changes to a non DFS channel
def test_dfs(nvg_599_dut,results_file):
    global NON_DFS_CHANNELS
    global DFS_CHANNELS
    print('in test_dfs')
    now = datetime.today().isoformat()
    results_file.write("Test Title:tst_dfs Execution time:")
    results_file.write(now)
    results_file.write("\n")

    session = nvg_599_dut.session
    home_link = session.find_element_by_link_text("Device")
    home_link.click()
    #nvg_599_dut.session = home_link

    current_5g_channel = nvg_599_dut.get_ui_home_network_status_value("ui_channel_5g")
    if current_5g_channel in DFS_CHANNELS:
        result = "Current 5G:" + current_5g_channel + " is a DFS channel\n"
        result_str = str(result)
        results_file.write(result_str)
        print('this is a DFS channel')
    else:
        print('this is a non DFS Changing to DFS channel 100')
        #def ui_set_bw_channel(self, band, bandwidth, channel):
        result = "Current 5G:" + current_5g_channel + " is not a DFS channel\n"
        #result_str = str(result)
        results_file.write("Changing to DFS channel 100, bandwidth 80\n")

        nvg_599_dut.ui_set_band_bandwith_channel('5g', 80, 100)
        print('setting channel to DFS channel 100')

    nvg_599_dut.login_nvg_599_cli()
    nvg_599_dut.telnet_cli_session.sendline()
    nvg_599_dut.telnet_cli_session.expect(">")
    nvg_599_dut.telnet_cli_session.sendline("telnet 192.168.1.1")
    nvg_599_dut.telnet_cli_session.expect("#")
    nvg_599_dut.telnet_cli_session.sendline("wl -i eth1 radar 2")
    sleep(10)

    current_5g_channel = nvg_599_dut.get_ui_home_network_status_value("ui_channel_5g")
    current_5g_channel = int(current_5g_channel)

    print('current_5g_channel',current_5g_channel)
    # after the test we expect the channel to have been changed to a non DFS channel

    if current_5g_channel in NON_DFS_CHANNELS:
        results_file.write("5G channel changed to non DFS channel: ")
        results_file.write(str(current_5g_channel))
        results_file.write("\n")

        print("Channel change to non DFS  Passed\n")
        print("Setting back to DFS\n")
        nvg_599_dut.ui_set_band_bandwith_channel('5g', 80, 100)

        current_5g_channel = nvg_599_dut.get_ui_home_network_status_value("ui_channel_5g")
        if current_5g_channel in DFS_CHANNELS:
            result = "Current 5G:" + current_5g_channel + " is a DFS channel\n"
            print("Setting back to DFS passed\n")

        results_file.write("Test Passed\n")
    else:
        print('test failed:Channel found:',current_5g_channel,' expected non DFS channel')
        print('current_5g_channel', current_5g_channel)
        #exit()
        result = "Current 5G:" + str(current_5g_channel) + " is a DFS channel\n"
        #result_str = str(result)

        print("result string  -dbg",result)
        #results_file.write("Current 5G:" ,current_5g_channel," is not a DFS channel\n")
        results_file.write(result)

# def tst_599_nvg_init():
#     nvg_599_dut = Nvg599Class()
#     url = 'http://192.168.1.254/'
#     nvg_599_dut.session = webdriver.Chrome()
#     nvg_599_dut.session.get(url)
#     return nvg_599_dut

def tst_speed_test(nvg_599_dut,results_file,test_ip):
    print('in tst_speed_test')
    now = datetime.today().isoformat()
    results_file.write("Test Title:tst_speed_tst Execution time:")
    results_file.write(now)
    results_file.write("\n")
    down_load_speed,up_load_speed = nvg_599_dut.speed_test_cli(test_ip)
    print('Download speed:', down_load_speed, 'Upload speed:', up_load_speed)
    speed = 'Download speed:' + down_load_speed + ' Upload speed:' + up_load_speed
    results_file.write(speed)
    results_file.write("\n")

    gw_serial_number = nvg_599_dut.serial_number
    gw_info = 'NVG 599 serial number:' + gw_serial_number
    results_file.write(gw_info)
    results_file.write("\n")
    software_version = 'Software Version:' + nvg_599_dut.software_version
    results_file.write(software_version)
    results_file.write("\n")
    results_file.write("\n")
    results_file.write("\n")

def tst_ping_ip(nvg_599_dut,ping_history_file, remote_ip):
    print('in tst_ping')
    #ping_history_file  = open('ping_history_file.txt', 'a+')
    ping_history_file  = open(ping_history_file, 'a+')
    now = datetime.today().isoformat()
    ping_history_file.write("Test Title:tst_ping Execution time:")
    ping_history_file.write(now)
    ping_history_file.write("\n")
    min,avg,max,mdev = nvg_599_dut.ping_from_local_host(remote_ip)
    min_str = 'Min time: '+ min
    ping_history_file.write(min_str)

    ping_history_file.write("\n")
    avg_str = 'Avg time: '+ avg
    ping_history_file.write(avg_str)

    ping_history_file.write("\n")
    max_str = 'Max time:'+ max
    ping_history_file.write(max_str)

    ping_history_file.write("\n")
    mdev_str = 'mdev time:'+ mdev
    ping_history_file.write(mdev_str)

    ping_history_file.write("\n")
    print('min: ', min)
    print('avg: ', avg)
    print('max: ', max)
    print('mdev:',mdev)

def test_ping_device_name(device_name_to_ping):
#    sh_ip_lan_dict = Nvg599Class.get_rg_sh_ip_lan_info_cli('arris-Latitude-MBR')
    sh_ip_lan_dict = Nvg599Class.get_rg_sh_ip_lan_info_cli()

    print('dict type' + str(type(sh_ip_lan_dict)))
    for key in sh_ip_lan_dict:
        #print('key----------------------------------------------' + key)
        if sh_ip_lan_dict[key]['Name']== device_name_to_ping:
            print('found it ' + sh_ip_lan_dict[key]['Name'])
            print('IP is: ' + sh_ip_lan_dict[key]['IP'])
            # we use the  mac from the IP table to get the radio band
            sh_wi_cl_dict = Nvg599Class.cli_sh_wi_all_clients()
            nvg_599_dut.ping_from_local_host(sh_ip_lan_dict[key]['IP'])

            # nvg_599_dut.cli_sh_wi_clients()
    # def cli_sh_wi_clients(self):
    # print('dict is ' + str(sh_ip_lan_dict))


# nvg_599_dut = Nvg599Class()
#remote_driver = nvg_599_dut.remote_webserver()
#remote_driver.get("http://www.firefox.com")
#nvg_599_dut.enable_sshd_ssh_cli()
#nvg_599_dut.turn_off_supplicant_cli()
#nvg_599_dut.conf_tr69_eco_url()
#url_to_check = "http://192.168.1.254/cgi-bin/home.ha"
#nvg_599_dut.factory_reset_rg(url_to_check)
# nvg_599_dut.enable_parental_control()
#nvg_599_dut.turn_off_wi_fi_security_protection_cli()
#dfs_file = open('dfs_file.txt','a')
#test_dfs(nvg_599_dut,dfs_file)
# Nvg599Class.factory_test()
#dfs_file.close()
# nvg_599_dut.poc_for_youtube()
exit()

ssid_band5 = "ATTqbrAnYs"
ssid_guest = "ATTqbrAnYs_Guest"
ssid_band2 = "ATTqbrAnYs"

nvg_599_dut.set_ui_ssid(ssid_band5,ssid_guest,ssid_band2)

band2, guest, band5 = nvg_599_dut.get_ui_ssid()
print('band 2: '+ band2 + '  guest: '+ guest + '  band5: ' + band5)

exit()
show_ip_lan_dict = nvg_599_dut.get_rg_sh_ip_lan_info_cli()

print(type(show_ip_lan_dict))
pprint.pprint(show_ip_lan_dict, width = 1)
exit()
#down_load_speed, up_load_speed = nvg_599_dut.run_speed_test_cli(test_ip)

# url_to_check = "http://192.168.1.254/cgi-bin/home.ha"

# nvg_599_dut.factory_reset_rg(url_to_check)

# nvg_599_dut.enable_sshd_ssh_cli()

# nvg_599_dut.conf_tr69_eco_url()

# nvg_599_dut.turn_off_supplicant_cli()

# nvg_599_dut.ping_from_local_host('192.1681.228')

print('1' + str(nvg_599_dut.get_airties_ip('airties_1_5g')))
print('2' + str(nvg_599_dut.get_airties_ip('airties_2_5g')))
print('3' + str(nvg_599_dut.get_airties_ip('airties_3_5g')))

results_str ="1234 abcd \n 1234 5678"
nvg_599_dut.email_test_results(results_str)

# ui_dict = nvg_599_dut.ui_get_device_list()



#for key in ui_dict:
#    print(key)

exit()

# tst_ping(nvg_599_dut,results_file,"192.168.1.239")

# tst_speed_test(nvg_599_dut,results_file,"192.168.1.239")

# dfs_file = open('dfs_file.txt','a')

# test_dfs(nvg_599_dut,dfs_file)

# dfs_file.close()

# nvg_599_dut.get_rg_sh_ip_lan_info_cli()

# Nvg599Class.get_rg_sh_ip_lan_info_cli('arris-Latitude-MBR')

# results_str = open('results_file.txt','r').read()
# nvg_599_dut.email_test_results(results_str)
# exit()

#print('dog' + str(DFS_CHANNELS))
#print ('dict' + str(test_house_devices_static_info))
#exit()


#nvg_599_dut.cli_sh_wi_all_clients()


#test_ping_device_name('arris-Latitude-MBR')

#
#
# for element in itertools.product(xa2Gch,xa2Gbw,xb5Gch,xb5Gbw):
#     print(element)
# exit()
#
#
# #statusInfoRegEx = re.compile(r'Model\s(\w+)\s+Serial\s+Number\s+(\d+)')
#statusInfoRegEx = re.compile(r'Model\s(\w+)\s+\w+/\w+\s+AnnexA\s+(\w+)',re.DOTALL)
#statusInfoRegEx = re.compile(r'Model\s(\w+)\s+\w+/\w+.*completed\s+(\w+)',re.DOTALL)
#statusInfoRegEx = re.compile(r'Model\s(\w+)\s+\w+/\w+.*number\s+(\w+).*Uptime\s+(\d\d:\d\d:\d\d:\d\d)',re.DOTALL)
#statusInfoRegEx = re.compile(r'Model\s(\w+).*Serial Number\s+(\d+)',re.DOTALL)
#statusInfoRegEx = re.compile(r'Model\s(\w+)')
#mo1 = statusInfoRegEx.search(statusOutput)

#print(mo1)
#print ('model ', mo1.group(1))

#print ('Serial Number', mo1.group(2))
#print ('Uptime ', mo1.group(3))

#exit()

#rgModel= mo1.group(1)
#serialNumber= mo1.group(2)
#addition

#if rgModel=='NVG599':
#    print('we are going to instantiate an NVG599')
#    nvg599DUT = Nvg599Class()
#    nvg599DUT.printme()
#    nvg599DUT.turnOffSupplicant()


#else:
#    print('what  to instantiate an NVG599')
#
#exit()


#airTiesTerm = pexpect.spawn("telnet 192.168.1.67")
#sleep(1)
#airTiesTerm.expect("ogin:")
#airTiesTerm.sendline('root')
#airTiesTerm.expect("#")

#airTiesTerm.sendline('wl -i wl0 chanspec')
#airTiesTerm.expect("#")
#airTies2GResult=airTiesTerm.before
#print(airTies2GResult)
#airTies2GChannel = airTies2GResult.split()[-2]
#print("2G",airTies2GChannel)
#print("")
#airTiesTerm.sendline('wl -i wl1 chanspec')
#irTiesTerm.expect("#")
#airTies5GResult=airTiesTerm.before
#airTies5GChannelInfo = airTies5GResult.split()[-2]
#print("5GInfo",airTies5GChannelInfo)
#airTies5GChannel =airTies5GChannelInfo.split("/")[0]
#print("5G Channel,airTies5GChannel)
#airTies5GBandwidth =airTies5GChannelInfo.split("/")[1]
#print("5G Bandwidth",airTies5GBandwidth)
#resultFile.close()
print("###############################################################################")
print("###############################################################################")

#Channel = myresult.split()[-2]

list2G=[1,2,3,4,5,6,7,8,9,10,11]
list5G=[36,40,44,48,52,56,60,64,100,104,108,112,116,1132,136,140,144,149,153,161]
list2GLite=[1]
list5GLite=[36]

airTiesTerm = pexpect.spawn("telnet 192.168.1.67",encoding='utf-8')
airTiesTerm.expect("ogin:")
airTiesTerm.sendline('root')
airTiesTerm.expect("#")

airTiesTerm.logfile= sys.stdout


#channelResultFP = open('channelResult.txt', 'w+')


# for l2g in list2GLite:
#     for i in list5GLite:
#         print("Config RG channel="+str(i))
#         output = rgTerm.sendline('tr69 SetParameterValues InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.Channel=' + str(i))
#         rgTerm.expect("UNLOCKED>")
#         # re-telnet into the airTies each time because the telnet session gets hung when channel is reset
#         print("Checking airTies for channel match: "+str(i))
#         # I think we want to wait before trying to login to the airtiesssh-add ~/.ssh/id_rsa
#         sleep(200)
#         airTiesTerm = pexpect.spawn("telnet 192.168.1.67", encoding='utf-8')
#         sleep(1)
#         airTiesTerm.expect("ogin")
#         airTiesTerm.sendline('root')
#         airTiesTerm.expect("#")
#         airTiesTerm.sendline('wl -i wl0 chanspec')
#         airTiesTerm.expect("#")
#         airTies2GResult = airTiesTerm.before
#         print("airties result " + str(airTies2GResult))
#         airTies2GChannel = airTies2GResult.split()[-2]
#         airTies2GChannel = airTies2GChannel.split()[-1]
#
#         print("AirTies 2G = ", airTies2GChannel)
#         print("")
#         sleep(2)
#
#         # airTiesTerm.sendline('wl -i wl1 status')   // we want this
#         airTiesTerm.sendline('wl -i wl1 chanspec')
#         airTiesTerm.expect("#")
#         airTies5GResult = airTiesTerm.before
#         airTies5GChannelInfo = airTies5GResult.split()[-2]
#         print("5G Info ", airTies5GChannelInfo)
#
#         sleep(2)
#         #airTies5GChannel = airTies5GChannelInfo.split("/")[-2]
#         airTies5GChannel = airTies5GChannelInfo.split("/")[0]
#
#         print("5G Channel = ", airTies5GChannel)
#         airTies5GBandWidth = airTies5GChannelInfo.split("/")[-1]  # type: object
#         print("5G Bandwidth = ", airTies5GBandWidth)
#
#         airTiesTerm.sendline('exit')
#         airTiesTerm.sendline("\x1b\r")
#         airTiesTerm.terminate(force=True)
#
#         sleep(10)
#
#         #print (type(i))
#         #print ("airTies5GChannel is of type "+ type(airTies5GChannel))
#
#
#         if i == int(airTies5GChannel):
#             channelResultFP.write(" \n")
#             channelResultFP.write(" 2G = "+ str(l2g) + " RG channel= "+ str(i) + " airTies5GChannel = " + airTies5GChannel  +  "  Passed" )
#             #channelResultFP.write("\r\n 2G = "+ str(l2g) + " RG channel= "+ str(i) + " airTies5GChannel = " + airTies5GChannel  +  "Passed" + "\r\n")
#
#             channelResultFP.write("\n ")
#
#             print(">> 2G = " + str(l2g) + " RG channel= "+ str(i) + " airTies5GChannel = " + airTies5GChannel  +  " Passed")
#             print ("----l2g--------------------------------------------- -------------------")
#         else:
#             channelResultFP.write(" ")
#             #channelResultFP.write("\r\n 2G = " + str(l2g) + "RG channel= "+ str(i) + " airTies5GChannel = " + airTies5GChannel  +  " Failed" + "\r\n")
#             channelResultFP.write(" 2G = " + str(l2g) + "RG channel= "+ str(i) + " airTies5GChannel = " + airTies5GChannel  +  " Failed  ")
#
#             channelResultFP.write(" ")
#
#         sleep(30)
#
#
#
#
# ### this used to work
# channelResultFP.seek(0)
# channelResultContents = channelResultFP.read()
# channelResultFP.close()

#resultFile.close()
#sleep(1)

# Note that, for Python 3 compatibility reasons, we are using spawnu and
# importing unicode_literals (above). spawnu accepts Unicode input and
# unicode_literals makes all string literals in this script Unicode by default.
p = pexpect.spawnu('uptime')

# This parses uptime output into the major groups using regex group matching.
p.expect(
    r'up\s+(.*?),\s+([0-9]+) users?,\s+load averages?: ([0-9]+\.[0-9][0-9]),?\s+([0-9]+\.[0-9][0-9]),?\s+([0-9]+\.[0-9][0-9])')
duration, users, av1, av5, av15 = p.match.groups()

# The duration is a little harder to parse because of all the different
# styles of uptime. I'm sure there is a way to do this all at once with
# one single regex, but I bet it would be hard to read and maintain.
# If anyone wants to send me a version using a single regex I'd be happy to see it.
days = '0'
hours = '0'
mins = '0'
if 'day' in duration:
    p.match = re.search(r'([0-9]+)\s+day', duration)
    days = str(int(p.match.group(1)))
if ':' in duration:
    p.match = re.search('([0-9]+):([0-9]+)', duration)
    hours = str(int(p.match.group(1)))
    mins = str(int(p.match.group(2)))
if 'min' in duration:
    p.match = re.search(r'([0-9]+)\s+min', duration)
    mins = str(int(p.match.group(1)))

# Print the parsed fields in CSV format.
# print('days, hours, minutes, users, cpu avg 1 min, cpu avg 5 min, cpu avg 15 min')
# print('%s, %s, %s, %s, %s, %s, %s' % (days, hours, mins, users, av1, av5, av15))
exit()

from time import sleep
from selenium import webdriver

# driver = webdriverhttps://www.waketech.edu/programs-courses/credit/electrical-systems-technology/degrees-pathways.Chrome('/usr/local/bin/chromedriver')
driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
# driver.get('http://www.google.com')
driver.get('http://192.168.1.254/cgi-bin/sysinfo.ha')
driver.implicitly_wait(20)
# driver.find_elements_by_tag_name("Settings") // this is for 599
driver.find_element_by_link_text("Settings").click()

# driver.findElement(By.linkText("Home Network")).click()
driver.implicitly_wait(20)

driver.find_element_by_link_text("LAN").click()
driver.implicitly_wait(20)
# driver.maximize_window()

driver.find_element_by_link_text("Wi-Fi").click()
driver.implicitly_wait(20)

password = driver.find_element_by_id("ADM_PASSWORD")

password.send_keys("8>1769&295")

driver.find_element_by_class_name('button').click()
# driver.find_element_by_xpath("//button[@value='Submit']").click()
# button.click()

driver.implicitly_wait(20)

# ENter device access code

sleep(30)
driver.quit()

child = pexpect.spawn("ssh root@192.168.1.254")
sleep(1)
# exit()

from time import sleep
from selenium import webdriver

import pexpect
import re
#import serial

# driver = webdriverhttps://www.waketech.edu/programs-courses/credit/electrical-systems-technology/degrees-pathways.Chrome('/usr/local/bin/chromedriver')
driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
# driver.get('http://www.google.com')
driver.get('http://192.168.1.254')
driver.implicitly_wait(20)
# driver.find_elements_by_tag_name("Settings") // this is for 599
driver.find_element_by_link_text("Settings").click()

# driver.findElement(By.linkText("Home Network")).click()
driver.implicitly_wait(20)

driver.find_element_by_link_text("LAN").click()
driver.implicitly_wait(20)
# driver.maximize_window()

driver.find_element_by_link_text("Wi-Fi").click()
driver.implicitly_wait(20)

password = driver.find_element_by_id("ADM_PASSWORD")

password.send_keys("8>1769&295")

driver.find_element_by_class_name('button').click()
# driver.find_element_by_xpath("//button[@value='Submit']").click()
# button.click()

driver.implicitly_wait(20)

# ENter device access code

sleep(30)
driver.quit()

child = pexpect.spawn("ssh root@192.168.1.254")
sleep(1)
# exit()


child.expect("assword:")
child.sendline('alcatel')
# child.sendline('*<#/53#1/2')
print("logged in to host")
child.expect("#")
child.sendline('exit')
sleep(5)
# driver.webdriver.quit()
exit()
# driver = webdriver.firefox('/home/palmer/.local/lib/python2.7/site-packages/chromedriver')
# driver = webdriver.chrome()
# browser.get('https://www.google.com')

#ain.
# If anyone wants to send me a version using a single regex I'd be happy to see it.
days = '0'
hours = '0'
mins = '0'
if 'day' in duration:
    p.match = re.search(r'([0-9]+)\s+day', duration)
    days = str(int(p.match.group(1)))
if ':' in duration:
    p.match = re.search('([0-9]+):([0-9]+)', duration)
    hours = str(int(p.match.group(1)))
    mins = str(int(p.match.group(2)))
if 'min' in duration:
    p.match = re.search(r'([0-9]+)\s+min', duration)
    mins = str(int(p.match.group(1)))

# Print the parsed fields in CSV format.
# print('days, hours, minutes, users, cpu avg 1 min, cpu avg 5 min, cpu avg 15 min')
# print('%s, %s, %s, %s, %s, %s, %s' % (days, hours, mins, users, av1, av5, av15))


print("Turning off supplicant")
ip = "192.168.1.254"
password = '<#/53#1/2'
child = pexpect.spawn("telnet " "192.168.1.254")
sleep(1)
# exit()
child.expect("ogin:")
child.sendline("admin")

child.expect("assword:")
child.sendline('*<#/53#1/2')
child.expect(">")

child.sendline('magic')
child.expect(">")

child.sendline('conf')
child.expect(">>")

child.sendline('system supplicant')
child.expect(">>")

child.sendline('set')
child.expect(" off | on ]:")

child.sendline('off')
child.expect(">>")

child.sendline('save')
child.expect(">>")

child.sendline("view")
child.expect(">>")

out = child.before
print(out)
#
child.expect("assword:")
child.sendline('alcatel')
# child.sendline('*<#/53#1/2')
print("logged in to host")

from time import sleep
from selenium import webdriver

import pexpect
import re

# driver = webdriverhttps://www.waketech.edu/programs-courses/credit/electrical-systems-technology/degrees-pathways.Chrome('/usr/local/bin/chromedriver')
driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
# driver.get('http://www.google.com')
driver.get('http://192.168.1.254')
driver.implicitly_wait(20)
# driver.find_elements_by_tag_name("Settings") // this is for 599
driver.find_element_by_link_text("Settings").click()

# driver.findElement(By.linkText("Home Network")).click()
driver.implicitly_wait(20)

driver.find_element_by_link_text("LAN").click()
driver.implicitly_wait(20)
# driver.maximize_window()

driver.find_element_by_link_text("Wi-Fi").click()
driver.implicitly_wait(20)

password = driver.find_element_by_id("ADM_PASSWORD")

password.send_keys("8>1769&295")

driver.find_element_by_class_name('button').click()
# driver.find_element_by_xpath("//button[@value='Submit']").click()
# button.click()

driver.implicitly_wait(20)

# ENter device access code

sleep(30)
driver.quit()

child = pexpect.spawn("ssh root@192.168.1.254")
sleep(1)
# exit()


child.expect("assword:")
child.sendline('alcatel')
# child.sendline('*<#/53#1/2')
print("logged in to host")
child.expect("#")
child.sendline('exit')
sleep(5)
# driver.webdriver.quit()
exit()
# driver = webdriver.firefox('/home/palmer/.local/lib/python2.7/site-packages/chromedriver')
# driver = webdriver.chrome()
# browser.get('https://www.google.com')

#
# importing unicode_literals (above). spawnu accepts Unicode input and
# unicode_literals makes all string literals in this script Unicode by default.
p = pexpect.spawnu('uptime')

# This parses uptime output into the major groups using regex group matching.
p.expect(
    r'up\s+(.*?),\s+([0-9]+) users?,\s+load averages?: ([0-9]+\.[0-9][0-9]),?\s+([0-9]+\.[0-9][0-9]),?\s+([0-9]+\.[0-9][0-9])')
duration, users, av1, av5, av15 = p.match.groups()


days = '0'
hours = '0'
mins = '0'
if 'day' in duration:
    p.match = re.search(r'([0-9]+)\s+day', duration)
    days = str(int(p.match.group(1)))
if ':' in duration:
    p.match = re.search('([0-9]+):([0-9]+)', duration)
    hours = str(int(p.match.group(1)))
    mins = str(int(p.match.group(2)))
if 'min' in duration:
    p.match = re.search(r'([0-9]+)\s+min', duration)
    mins = str(int(p.match.group(1)))

# Print the parsed fields in CSV format.
# print('days, hours, minutes, users, cpu avg 1 min, cpu avg 5 min, cpu avg 15 min')
# print('%s, %s, %s, %s, %s, %s, %s' % (days, hours, mins, users, av1, av5, av15))


print("Turning off supplicant")
ip = "192.168.1.254"
password = '<#/53#1/2'
child = pexpect.spawn("telnet " "192.168.1.254")
sleep(1)
# exit()
child.expect("ogin:")
child.sendline("admin")

child.expect("assword:")
child.sendline('*<#/53#1/2')
child.expect(">")

child.sendline('magic')
child.expect(">")

child.sendline('conf')
child.expect(">>")

child.sendline('system supplicant')
child.expect(">>")

child.sendline('set')
child.expect(" off | on ]:")

child.sendline('off')
child.expect(">>")

child.sendline('save')
child.expect(">>")

child.sendline("view")
child.expect(">>")

out = child.before
print(out)
#

child.expect("#")
child.sendline('exit')
sleep(5)
# driver.webdriver.quit()
exit()
# driver = webdriver.firefox('/home/palmer/.local/lib/python2.7/site-packages/chromedriver')
# driver = webdriver.chrome()
# browser.get('https://www.google.com')



# Note that, for Python 3 compatibility reasons, we are using spawnu and
# importing unicode_literals (above). spawnu accepts Unicode input and
# unicode_literals makes all string literals in this script Unicode by default.
p = pexpect.spawnu('uptime')

# This parses uptime output into the major groups using regex group matching.
p.expect(
    r'up\s+(.*?),\s+([0-9]+) users?,\s+load averages?: ([0-9]+\.[0-9][0-9]),?\s+([0-9]+\.[0-9][0-9]),?\s+([0-9]+\.[0-9][0-9])')
duration, users, av1, av5, av15 = p.match.groups()

# The duration is a little harder to parse because of all the different
# styles of uptime. I'm sure there is a way to do this all at once with
# one single regex, but I bet it would be hard to read and maintain.
# If anyone wants to send me a version using a single regex I'd be happy to see it.
days = '0'
hours = '0'
mins = '0'
if 'day' in duration:
    p.match = re.search(r'([0-9]+)\s+day', duration)
    days = str(int(p.match.group(1)))
if ':' in duration:
    p.match = re.search('([0-9]+):([0-9]+)', duration)
    hours = str(int(p.match.group(1)))
    mins = str(int(p.match.group(2)))
if 'min' in duration:
    p.match = re.search(r'([0-9]+)\s+min', duration)
    mins = str(int(p.match.group(1)))

# Print the parsed fields in CSV format.
# print('days, hours, minutes, users, cpu avg 1 min, cpu avg 5 min, cpu avg 15 min')
# print('%s, %s, %s, %s, %s, %s, %s' % (days, hours, mins, users, av1, av5, av15))

#
# print("Turning off supplicant")
# ip = "192.168.1.254"
# password = '<#/53#1/2'
# child = pexpect.spawn("telnet " "192.168.1.254")
# sleep(1)
# # exit()
# child.expect("ogin:")
# child.sendline("admin")
#
# child.expect("assword:")
# child.sendline('*<#/53#1/2')
# child.expect(">")
#
# child.sendline('magic')
# child.expect(">")
#
# child.sendline('conf')
# child.expect(">>")
#
# child.sendline('system supplicant')
# child.expect(">>")
#
# child.sendline('set')
# child.expect(" off | on ]:")
#
# child.sendline('off')
#
# from time import sleep
# from selenium import webdriver
#
# import pexpect
# import re
#
# # driver = webdriverhttps://www.waketech.edu/programs-courses/credit/electrical-systems-technology/degrees-pathways.Chrome('/usr/local/bin/chromedriver')
# driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
# # driver.get('http://www.google.com')
# driver.get('http://192.168.1.254')
# driver.implicitly_wait(20)
# # driver.find_elements_by_tag_name("Settings") // this is for 599
# driver.find_element_by_link_text("Settings").click()
#
# # driver.findElement(By.linkText("Home Network")).click()
# driver.implicitly_wait(20)
#
# driver.find_element_by_link_text("LAN").click()
# driver.implicitly_wait(20)
# # driver.maximize_window()
#
# driver.find_element_by_link_text("Wi-Fi").click()
# driver.implicitly_wait(20)
#
# password = driver.find_element_by_id("ADM_PASSWORD")
#
# password.send_keys("8>1769&295")
#
# driver.find_element_by_class_name('button').click()
# # driver.find_element_by_xpath("//button[@value='Submit']").click()
# # button.click()
#
# driver.implicitly_wait(20)
#
# # ENter device access code
#
# sleep(30)
# driver.quit()
#
# exit()
#
# # child = pexpect.spawn("ssh root@192.168.1.254")
# sleep(1)
# # exit()
#
#
# child.expect("assword:")
# child.sendline('alcatel')
# # child.sendline('*<#/53#1/2')
# print("logged in to host")
# child.expect("#")
# child.sendline('exit')
# sleep(5)
# # driver.webdriver.quit()
# exit()
# # driver = webdriver.firefox('/home/palmer/.local/lib/python2.7/site-packages/chromedriver')
# #
# # unicode_literals makes all string literals in this script Unicode by default.
# p = pexpect.spawnu('uptime')
#
# # This parses uptime output into the major groups using regex group matching.
# p.expect(
#     r'up\s+(.*?),\s+([0-9]+) users?,\s+load averages?: ([0-9]+\.[0-9][0-9]),?\s+([0-9]+\.[0-9][0-9]),?\s+([0-9]+\.[0-9][0-9])')
# duration, users, av1, av5, av15 = p.match.groups()
#
# # The duration is a little harder to parse because of all the different
# # styles of uptime. I'm sure there is a way to do this all at once with
# # one single regex, but I bet it would be hard to read and maintain.
# # # If anyone wants to send me a version using a single regex I'd be happy to see it.
# # days = '0'
# # hours = '0'
# # mins = '0'
# # if 'day' in duration:
# #     p.match = re.search(r'([0-9]+)\s+day', duration)
# #     days = str(int(p.match.group(1)))
# # if ':' in duration:
#     p.match = re.search('([0-9]+):([0-9]+)', duration)
#     hours = str(int(p.match.group(1)))
#     mins = str(int(p.match.group(2)))
# if 'min' in duration:
#     p.match = re.search(r'([0-9]+)\s+min', duration)
#     mins = str(int(p.match.group(1)))
#
# # Print the parsed fields in CSV format.
# # print('days, hours, minutes, users, cpu avg 1 min, cpu avg 5 min, cpu avg 15 min')
# # print('%s, %s, %s, %s, %s, %s, %s' % (days, hours, mins, users, av1, av5, av15))
