from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# import itertools
import pprint
import pickle
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
# from datetime import datetime
import datetime


import pexpect
from rgclass import Nvg599Class
# from rgclass import NON_DFS_CHANNELS
# from rgclass import DFS_CHANNELS
# from rgclass import  test_house_devices_static_info

NON_DFS_CHANNELS = {36,40,44,48,149,153,157,161,165}
DFS_CHANNELS     = {52,56,60,64,100,104,108,112,116,132,136,140,144}
ALL_BAND5_CHANNELS = {36, 40, 44, 48,52, 56, 60, 64, 100, 104, 108, 112, 116, 132, 136, 140, 144, 149, 153, 157, 161, 165}



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
    # nvg_599_dut.session = home_link

    current_5g_channel = nvg_599_dut.get_ui_home_network_status_value("ui_channel_5g")
    if current_5g_channel in DFS_CHANNELS:
        result = "Current 5G:" + current_5g_channel + " is a DFS channel\n"
        result_str = str(result)
        results_file.write(result_str)
        print('this is a DFS channel')
    else:
        print('this is a non DFS Changing to DFS channel 100')
        # def ui_set_bw_channel(self, band, bandwidth, channel):
        result = "Current 5G:" + current_5g_channel + " is not a DFS channel\n"
        # result_str = str(result)
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
    mdev_str = 'mdev time:' + mdev
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

def test_channel_channelband_combinations(band5_channel_list, band5_bandwidth_list,ip_to_ping, result_file_name):
    nvg_599_dut = Nvg599Class()

    # ui_set_band_bandwith_channel(self, band, bandwidth, channel):
    channel_band_file = open(result_file_name, 'a')
    now = datetime.today().isoformat()
    channel_band_file.write("\" + ""Test Title:Channel/Channel band test:" + "\n")
    channel_band_file.write(now + "\n")
    software_version = nvg_599_dut.software_version
    channel_band_file.write("NVG599 Firmware:" + software_version + "\n")

    for band5_channel in range(len(band5_channel_list)):
        for band5_bandwidth in range(len(band5_bandwidth_list)):
            print(' ')
            print('band bandwidth channel: ' + str(band5_channel_list[band5_channel]) + "  "  + str(band5_bandwidth_list[band5_bandwidth]))
            print(' ')
            sleep(30)
            nvg_599_dut.ui_set_band_bandwith_channel('5g', band5_bandwidth_list[band5_bandwidth], band5_channel_list[band5_channel])

            sleep(60)
            ping_results = nvg_599_dut.ping_check(ip_to_ping)
            # ping_results = nvg_599_dut.ping_check('192.168.1.80')

            print('Channel:' + str(band5_channel_list[band5_channel]) + " Bandwidth:"  + str(band5_bandwidth_list[band5_bandwidth]) + ' Ping result:' + str(ping_results))
        #min_ping, avg_ping, max_ping, mdev_ping = nvg_599_dut.ping_from_local_host('192.168.1.77')
        #print('min_ping:'+  ping_file = open('ping_file.txt', 'a') min_ping + ' avg_ping:' + avg_ping + ' max_ping:' + max_ping)

            channel_band_file.writelines('Channel:' + str(band5_channel_list[band5_channel]) + " Bandwidth:"  + str(band5_bandwidth_list[band5_bandwidth]) + ' Ping result:' + str(ping_results) + '\n')
        #                     self.serial_number + '  min_ping:' + min_ping + '  avg_ping:' +
        #                     '  max_ping:' + max_ping + '  max dev:' + mdev_ping)
        #ping_file.writelines('\n')
    channel_band_file.close()

#
# firmware_599_available =['/home/palmer/Downloads/nvg599-9.2.2h12d9_1.1.bin',
#     '/home/palmer/Downloads/nvg599-9.2.2h12d9_1.1.bin'
#     '/home/palmer/Downloads/nvg599-9.2.2h12d10_1.1.bin',
#     '/home/palmer/Downloads/nvg599-9.2.2h12d13_1.1.bin',
#     '/home/palmer/Downloads/nvg599-9.2.2h13d1_1.1.bin'
#     '/home/palmer/Downloads/nvg599-9.2.2h13d2_1.1.bin'
#     '/home/palmer/Downloads/nvg599-9.2.2h13d3_1.1.bin'
#     '/home/palmer/Downloads/nvg599-9.2.2h13d4_1.1.bin'
#
#                          ]
#
firmware_599_names_test =[
'nvg599-9.2.2h12d9_1.1',
'nvg599-9.2.2h13d4_1.1']
#
#                          ]

#upgrade_file = 'sadf'


def test_comprehension(firmware_599_available):
    i = 0
    for i in range (len(firmware_599_available)):
        print('list:',str(firmware_599_available[i]))


    upper_case = [item.upper() for item in firmware_599_available]
    print('upper case:', upper_case)
    result = []

def test_rg_upgrade(nvg_599_dut, firmware_599_available):
    upgrade_status = nvg_599_dut.update_rg(firmware_599_available)
    #nvg_599_dut.ping_from_local_host('192.168.1.67')
    # nvg_599_dut.ping_from_local_host('192.168.1.67')

#def test_rg_upgrade(nvg_599_dut(nvg_599_dut, upgrade_file):#    pass
#     print('in test_rg_upgrade')
#     upgrade_status = nvg_599_dut.update_rg(upgrade_file)


# x = 13.73333
# x_round = round(x)
# print('x_round:',x_round)
# exit()

#
#
# nvg_599_dut = Nvg599Class()
# #
# test_rg_upgrade(nvg_599_dut, firmware_599_available[1])
# exit(

#-------------------------------------------

import matplotlib.pyplot as plt
import matplotlib.image as img

#
# note8_file.write("Speedtest results for Samsung Note 8:" + "\n")
# note8_file.write(now + "\n")
# tablet_file.write("Speedtest results for Samsung Tablet:" + "\n")
# tablet_file.write(now + "\n")
# #note8_file.write("\" + Speedtest  + "\n")
# #channel_band_file.write(now + "\n")
#
# speed_test_result_list_tablet= []
# speed_test_result_list_tablet_download= []
# speed_test_result_list_tablet_upload= []
#
# speed_test_result_list_note8 = []
# speed_test_result_list_note8_download= []
# speed_test_result_list_note8_upload= []

# pfp
import matplotlib.pyplot as plt
import numpy as np
# import matplotlib.pyplot as plt
from pylab import *

#
def test_rg_upgrade_speedtest(nvg_599_dut, firmware_599_available, firmware_599_names):
    now = datetime.today().isoformat()
    start_time = datetime.today().strftime("%b-%d-%Y--%H:%M")
    # x = [1, 2, 3, 4, 5, 6, 7, 8]
    note8_file_name = "note8_" + start_time +'.txt'
    tablet_file_name = "tablet_" + start_time +'.txt'

    # note8_file = open('note_file.txt', 'a')
    # tablet_file = open('tablet_file.txt', 'a')
    note8_file = open(note8_file_name, 'a')
    tablet_file = open(tablet_file_name, 'a')
    tablet_file.write(start_time + "\n")
    note8_file.write(start_time + "\n")
    note8_file.close()
    tablet_file.close()


    tablet_ping_list = []
    note8_ping_list = []
    tablet_download_list = []
    tablet_upload_list = []
    note8_download_list = []
    note8_upload_list = []

    for firmware in firmware_599_available:
        print('in firmware loop ******************* firmware' + str(firmware))
        nvg_599_dut.update_rg(firmware)
        sleep(300)
        #.67 is  the tablet
        #speed_test_result_tuple_tablet = Nvg599Class.run_speed_test_from_android_termux("192.168.1.67")
        ping_results = nvg_599_dut.ping_check('192.168.1.67')
        a,b = Nvg599Class.run_speed_test_from_android_termux("192.168.1.67")
        print('Tablet ---------------------------------------------firmware:' + str(firmware))

        # print("speed_test_result_tuple:", speed_test_result_tuple_tablet)
        #for a, b in speed_test_result_tuple_tablet:
        print('tablet download speed: ' + a + ' Upload speed:' + b)
        tablet_download_list.append(a)
        tablet_upload_list.append(b)
        pickle.dump(tablet_download_list, open("tabletdownloadpickle.p", "wb"))
        pickle.dump(tablet_upload_list, open("tabletuploadpickle.p", "wb"))
        tablet_file = open(tablet_file_name, 'a')
        tablet_file.write("firmware:" + str(firmware) + "Download:" + a + " Upload:" + b + "\n")
        tablet_file.close()
        sleep(30)
        # mina, avga, maxa, mdeva = nvg_599_dut.ping_from_local_host("192.168.1.67")
        # print('192.168.1.67 - min:' + str(mina) + ' max:' + str(maxa) + ' avg: ' + avga)
        # for a, b in speed_test_result_tuple_tablet:
        #     print('tablet download speed: ' + a + ' Upload speed:' + b)
        #     tablet_download_list.append(a)
        #     tablet_upload_list.append(b)
        #     tablet_file.write("firmware:" + str(firmware) + "download:" + a + "Upload:" + b + "\n")
        #     sleep(60)

        # speed_test_result_tuple_note8 = Nvg599Class.run_speed_test_from_android_termux("192.168.1.70")
        ping_results = nvg_599_dut.ping_check('192.168.1.70')
        a,b = Nvg599Class.run_speed_test_from_android_termux("192.168.1.70")
        #for a, b in speed_test_result_tuple_note8:
        print('Note 8 ---------------------------------------------firmware:' + str(firmware))
        print('Note 8 download speed: ' + a + ' Upload speed:' + b)
        note8_download_list.append(a)
        note8_upload_list.append(b)
        pickle.dump(note8_download_list, open("note8downloadpickle.p", "wb"))
        pickle.dump(note8_upload_list, open("note8uploadpickle.p", "wb"))

        note8_file = open(note8_file_name, 'a')
        note8_file.write("firmware:" + str(firmware) + "Download:" + a + " Upload:" + b + "\n")
        note8_file.close()
        sleep(200)

        # # post pone this for now
        # mina, avga, maxa, mdeva = nvg_599_dut.ping_from_local_host("192.168.1.70")
        # print('192.168.1.70 - min:' + str(mina) + ' max:' + str(maxa) + ' avg: ' + avga)
        #

        # for a, b in speed_test_result_tuple_note8:
        # #for a, b in speed_test_result_tuple_note8:
        #     print('Note 8 download speed: ' + a + ' Upload speed:' + b)
        #     note8_download_list.append(a)
        #     note8_upload_list.append(b)
        #     note8_file.write("firmware:" + str(firmware) + "download:" + a + "Upload:" + b + "\n")
        #     sleep(60)

    # note8_file.close()
    # tablet_file.close()
    # tablet_download_list
    # note8_download_list
    plt.figure("Test House Speedtest results for NVG 599 ", figsize=(8, 7))
    ty = arange(1.0, 12.0, 1)
#    ty = arange(1.0, 10.0, 1)

    #
    subplot(2, 1, 1)
    plt.ylabel('Speed in MBPS')
    title('NVG 599 Download Speed')
    plot(ty, tablet_download_list, 'g')
    plot(ty, note8_download_list, 'b')
    plt.grid()
    #
    subplot(2, 1, 2)
    title('NVG 599 Upload Speed')
    plt.ylabel('Speed in MBPS')
    plt.xlabel('Firmware')
    plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9,10], firmware_599_names, rotation='vertical')

    plot(ty, tablet_upload_list, 'b', label='Tablet')
    plot(ty, note8_upload_list, 'g', label='Note8')
    plt.legend(bbox_to_anchor=(1, -1.2), ncol=1)

    plt.grid()
    plt.tight_layout()
    plt.subplots_adjust(left=0.1, right=0.9, bottom=0.2, top=0.9)
    now = datetime.today().isoformat()
    plt.savefig("/home/palmer/Downloads/speedtest:" + start_time)
    plt.savefig("thisisit")

    show()
    return tablet_download_list, tablet_upload_list, note8_download_list, note8_upload_list

#
# #
# def test_tuple():
#      tuple = 1.2,3.4
#      return tuple
# #
# #
# a,b = test_tuple()
# #
# print('a:',a,' b:',b)
# exit()

# now = datetime.today().isoformat()
# start_time = datetime.today().strftime("%b-%d-%Y--%H:%M")
# x = [1, 2, 3, 4, 5, 6, 7, 8]
# note8_file_name = "note8_" + start_time +'.txt'
# tablet_file_name = "tablet" + start_time +'.txt'
# print('fn:',note8_file_name)
# exit()

firmware_599_names = [
        '9.2.2h12d9',
        '9.2.2h12d10',
        '9.2.2h12d13',
        '9.2.2h13d1',
        '9.2.2h13d2',
        '9.2.2h13d3',
        '9.2.2h13d4',
        '9.2.2h13d5',
        '9.2.2h13d6',
        '9.2.2h13d7',
        '9.2.2h13d7'
        ]

firmware_599_available = ['/home/palmer/Downloads/nvg599-9.2.2h12d9_1.1.bin',
                        '/home/palmer/Downloads/nvg599-9.2.2h12d10_1.1.bin',
                        '/home/palmer/Downloads/nvg599-9.2.2h12d13_1.1.bin',
                        '/home/palmer/Downloads/nvg599-9.2.2h13d1_1.1.bin',
                        '/home/palmer/Downloads/nvg599-9.2.2h13d2_1.1.bin',
                        '/home/palmer/Downloads/nvg599-9.2.2h13d3_1.1.bin',
                        '/home/palmer/Downloads/nvg599-9.2.2h13d4_1.1.bin',
                        '/home/palmer/Downloads/nvg599-9.2.2h13d5_1.1.bin',
                        '/home/palmer/Downloads/nvg599-9.2.2h13d6_1.1.bin',
                        '/home/palmer/Downloads/nvg599-9.2.2h13d7_1.1.bin',
                        '/home/palmer/Downloads/nvg599-9.2.2h13d8_1.1.bin',
                          ]

# from string
# mystring = '{
#   "bssid": "fc:51:a4:2f:25:90",
#   "frequency_mhz": 2437,
#   "ip": "192.168.1.67",
#   "link_speed_mbps": 72,
#   "mac_address": "02:00:00:00:00:00",
#   "network_id": 22,
#   "rssi": -43,
#   "ssid": "ATTqbrAnYs",
#   "ssid_hidden": false,
#   "supplicant_state": "COMPLETED""
# }'

#Nvg599Class.run_speed_test_from_android_termux('192.168.1.67')
#Nvg599Class.get_wifi_info_from_android_termux('192.168.1.70')

#exit()

#Nvg599Class.wait_for_ssh_to_be_ready('192.168.1.70', '8022', '20', '1')
#exit()

# def pickle_test():
#     note8_upload_list = [2.1, 2.1, 2.0, 2.1, 2.4, 2.1, 2.01, 2.1, 2.2, 1.9]
#     pickle.dump(note8_upload_list, open("mypickle.p","wb"))
#     new_pickle= pickle.load( open("mypickle.p","rb"))
#     print('new_pickle',new_pickle)
#
#
#
# pickle_test()
# print('done')
# exit()

from datetime import datetime

#date = datetime.datetime.strptime(date,"%m%d%Y")

def datetimetest():
    now = datetime.today().isoformat()


# datetimetest()
# exit()
# return min_ping, avg_ping, max_ping, mdev_ping
#mina, avga, maxa, mdeva  =  nvg_599_dut.ping_from_local_host("192.168.1.70")
#print('min:' + str(mina) + ' max:' + str(maxa) +  ' avg: ' + avga)
#exit()


nvg_599_dut = Nvg599Class()


#device_dict = nvg_599_dut.ui_get_device_list()
#print('device_dict:', device_dict)

#nvg_599_dut.disable_enable_wifi_2_4_and_5g_wifi()
#exit()
#nvg_599_dut.enable_parental_control()
#nvg_599_dut.enable_guest_network_and_set_password_ssid()
#nvg_599_dut.factory_reset_rg()
nvg_599_dut.turn_off_supplicant_cli()
#nvg_599_dut.enable_guest_network_and_set_password_ssid()
#Nvg599Class().run_speed_test_from_android_termux("192.168.1.70")
#test_rg_upgrade_speedtest(nvg_599_dut,firmware_599_available,firmware_599_names)
exit()















#import datetime
#date = datetime.datetime.strptime(date, "%m%d%Y")
# from pylab import *
tablet_download_list = [27.7, 28.9, 27.6, 27.1, 30.1 ,29.2 ,30.6, 28.1, 29.0, 26.2]
note8_download_list =  [55.3, 54.4, 50.1, 58.2, 48.8, 41.1, 44.0, 44.0, 50.5, 51.7]
tablet_upload_list =   [2.4, 2.3 ,2.4, 2.4, 2.1, 2.3, 2.1, 2.2, 2.4, 2.1]
note8_upload_list =    [2.1, 2.1, 2.0, 2.1, 2.4, 2.1, 2.01, 2.1, 2.2, 1.9]
plt.figure("Test House Speedtest results for NVG 599",figsize=(8, 7))
# x_label_list = ['9.2.2h12d9','9.2.2h12d10','9.2.2h12d13','9.2.2h13d1 ', '9.2.2h13d2','9.2.2h13d3', '9.2.2h13d4','9.2.2h13d5','9.2.2h13d6']
# start number,stop number, steps
ty =  arange(1.0, 11.0, 1)
# tx =  arange(1.0, 10.0, 1)
# plt.xticks([1,2,3,4,5,6,7,8,9])
# plt.xticks([1,2,3,4,5,6,7,8,9],x_label_list,rotation='vertical')
#plt.subplots(2,1,sharey=True)

subplot(2,1,1)
plt.ylabel('Speed in MBPS')
title('NVG 599 Download Speed')
plt.ylim([10,70])
plot(ty,tablet_download_list,'g')
plot(ty,note8_download_list,'b')
plt.grid()
#
#plt.legend(bbox_to_anchor=(1, -1.2), ncol=1)
#plt.legend(bbox_to_anchor=(1, -1.2), ncol=1)

subplot(2,1,2)
title('NVG 599 Upload Speed')
plt.ylabel('Speed in MBPS')
plt.xlabel('Firmware')
plt.xticks([1,2,3,4,5,6,7,8,9,10],firmware_599_names,rotation='vertical')

plt.ylim([0,4])

plot(ty,tablet_upload_list,'b', label = "Samsung Note8 5 G")
plot(ty,note8_upload_list,'g', label = "Samsung Tablet 2.4 G")
plt.legend(bbox_to_anchor=(1,-1.0), ncol=1)
plt.grid()
#plt.tight_layout()
plt.subplots_adjust(left=0.1, right=0.9, bottom=0.4, top=0.9, hspace=0.4)
plt.legend(bbox_to_anchor=(1, -1.2), ncol=1)
#now = datetime.today().isoformat()
# now = datetime.today().isoformat()
#channel_band_file.write(now + ""Test Title:Channel/Channel band test:" +"\n")
plt.savefig("/home/palmer/Downloads/speedtest:")
show()
exit()

speed_test_result_list = []
# download, upload = Nvg599Class.run_speed_test_from_android_termux("192.168.1.70")
for i in  range(4):
    print('loop:' + str(i))
    speed_test_result_tuple  = Nvg599Class.run_speed_test_from_android_termux("192.168.1.70")
    speed_test_result_list.append(speed_test_result_tuple)

down_load = []
up_load= []

for a,b in speed_test_result_list:
    print('download speed: ' + a + ' Upload speed:' + b)
    down_load.append(a)
    up_load.append(b)

import matplotlib.pyplot as plt
nvg_599_dut = Nvg599Class()
test_rg_upgrade("/home/palmer/Downloads/nvg599-9.2.2h13d5_1.1.bin")
exit()
#nvg_599_dut.factory_test()
#exit()
#nvg_599_dut.enable_sshd_ssh_cli()
#nvg_599_dut.turn_off_supplicant_cli()
#nvg_599_dut.conf_tr69_eco_url()
#url_to_check = "http://192.168.1.254/cgi-bin/home.ha"
nvg_599_dut.factory_reset_rg()
#nvg_599_dut.enable_parental_control()
#nvg_599_dut.turn_off_wi_fi_security_protection_cli()
#dfs_file = open('dfs_file.txt','a')
#nvg_599_dut.factory_reset_rg()
exit()

# the default  url is "http://192.168.1.254/cgi-bin/home.ha"
# nvg_599_dut.factory_reset_rg()
# security, current_password = nvg_599_dut.ui_get_wifi_password()
# print('current pasword:' + current_password)
# print('security:' + security + ' new pasword:' + current_password)
# wpa or defwpa
default_security = "Default Password"
custom_security = "Custom Password"

# too long >  63
password_too_short_7 = "1234567"
password_max_63 = "000000000011111111112222222222333333333344444444445555555555666"
password_too_long_64 = "0000000000111111111122222222223333333333444444444455555555556666"
password_too_long_65 = "00000000001111111111222222222233333333334444444444555555555566666"
password_too_long_66 = "000000000011111111112222222222333333333344444444445555555555666666"
password_too_long_67 = "0000000000111111111122222222223333333333444444444455555555556666666"
password_too_long_68 = "00000000001111111111222222222233333333334444444444555555555566666666"
password_too_long_69 = "000000000011111111112222222222333333333344444444445555555555666666666"
password_too_long_70 = "0000000000111111111122222222223333333333444444444455555555556666666666"
password_too_long_71 = "00000000001111111111222222222233333333334444444444555555555566666666666"

# set_wifi_return_code = nvg_599_dut.ui_set_wifi_password(custom_security, password_too_long_64)
# print('******** set_wifi_return_code: ' + set_wifi_return_code)
# print('############################################')
# set_wifi_return_code = nvg_599_dut.ui_set_wifi_password(custom_security, password_too_long_65)
# print('******** set_wifi_return_code: ' + set_wifi_return_code)
# print('############################################')
# set_wifi_return_code = nvg_599_dut.ui_set_wifi_password(custom_security, password_too_long_66)
# print('******** set_wifi_return_code: ' + set_wifi_return_code)
# print('############################################')
# set_wifi_return_code = nvg_599_dut.ui_set_wifi_password(custom_security, password_too_long_67)
# print('******** set_wifi_return_code: ' + set_wifi_return_code)
# print('############################################')
# set_wifi_return_code = nvg_599_dut.ui_set_wifi_password(custom_security, password_too_long_68)
# print('******** set_wifi_return_code: ' + set_wifi_return_code)
# print('############################################')
# set_wifi_return_code = nvg_599_dut.ui_set_wifi_password(custom_security, password_too_long_69)
# print('******** set_wifi_return_code: ' + set_wifi_return_code)
# print('############################################')
# set_wifi_return_code = nvg_599_dut.ui_set_wifi_password(custom_security, password_too_long_70)
# print('******** set_wifi_return_code: ' + set_wifi_return_code)
# print('############################################')
# set_wifi_return_code = nvg_599_dut.ui_set_wifi_password(custom_security, password_too_long_71)
# print('******** set_wifi_return_code: ' + set_wifi_return_code)
# print('############################################')
# exit()

# min chars is 8

# max chars is 63
#password_just_right ="000000000011111111112222222222333333333344444444445555555555666"
update_rg ='/home/palmer/Downloads/nvg599-9.2.2h13d4_1.1.bin'
nvg_599_dut.update_rg(update_rg)
exit()

set_wifi_return_code = nvg_599_dut.ui_set_wifi_password(custom_security, password_too_long_64)
print('******** set_wifi_return_code: ' + set_wifi_return_code)
print('############################################')
set_wifi_return_code = nvg_599_dut.ui_set_wifi_password(custom_security, password_too_short_7)
print('******** set_wifi_return_code: ' + str(set_wifi_return_code))
print('############################################')
set_wifi_return_code = nvg_599_dut.ui_set_wifi_password(custom_security, password_max_63)
print('******** set_wifi_return_code: ' + str(set_wifi_return_code))
print('############################################')


dfs_file = open('dfs_file.txt','a')
test_dfs(nvg_599_dut,dfs_file)

exit()


# test_channel_channelband_combinations(band5_channel_list, band5_bandwidth_list,ip_to_ping, result_file_name)
xALL_BAND5_CHANNELS = [52, 56]
xALL_BAND5_BANDWIDTHS= [20, 40]

ip_to_ping = '192.168.1.80'

test_channel_channelband_combinations(xALL_BAND5_CHANNELS, xALL_BAND5_BANDWIDTHS, ip_to_ping, 'tc_chan_tm.txt')

exit()

ALL_BAND5_CHANNELS = [104, 108, 112, 116, 132, 136, 140, 144, 149, 153, 157, 161, 165]
#ALL_BAND5_CHANNELS = [36, 40, 44, 48,52, 56, 60, 64, 100, 104, 108, 112, 116, 132, 136, 140, 144, 149, 153, 157, 161, 165]
ALL_BAND5_BANDWIDTHS= [20,40,80]
xALL_BAND5_CHANNELS = [52, 56]
xALL_BAND5_BANDWIDTHS= [20, 40]


# ui_set_band_bandwith_channel(self, band, bandwidth, channel):
channel_band_file = open('channel_band_file_to_4920.txt', 'a')
now = datetime.today().isoformat()
channel_band_file.write("\" + ""Test Title:Channel/Channel band test:" +"\n")
channel_band_file.write(now + "\n")
software_version = nvg_599_dut.software_version
channel_band_file.write("NVG599 Firmware:"+ software_version + "\n")
for band5_channel in range(len(ALL_BAND5_CHANNELS)):
    for band5_bandwidth in range(len(ALL_BAND5_BANDWIDTHS)):
        print(' ')
        print('band bandwidth channel: ' + str(ALL_BAND5_CHANNELS[band5_channel]) + "  "  + str(ALL_BAND5_BANDWIDTHS[band5_bandwidth]))
        print(' ')
        sleep(30)
        nvg_599_dut.ui_set_band_bandwith_channel('5g', ALL_BAND5_BANDWIDTHS[band5_bandwidth], ALL_BAND5_CHANNELS[band5_channel])

        sleep(60)
        ping_results = nvg_599_dut.ping_check('192.168.1.80')
        print('Channel:' + str(ALL_BAND5_CHANNELS[band5_channel]) + " Bandwidth:"  + str(ALL_BAND5_BANDWIDTHS[band5_bandwidth]) + ' Ping result:' + str(ping_results))
        #min_ping, avg_ping, max_ping, mdev_ping = nvg_599_dut.ping_from_local_host('192.168.1.77')
        #print('min_ping:'+  ping_file = open('ping_file.txt', 'a') min_ping + ' avg_ping:' + avg_ping + ' max_ping:' + max_ping)

        channel_band_file.writelines('Channel:' + str(ALL_BAND5_CHANNELS[band5_channel]) + " Bandwidth:"  + str(ALL_BAND5_BANDWIDTHS[band5_bandwidth]) + ' Ping result:' + str(ping_results) + '\n')
        #                     self.serial_number + '  min_ping:' + min_ping + '  avg_ping:' +
        #                     '  max_ping:' + max_ping + '  max dev:' + mdev_ping)
        #ping_file.writelines('\n')
channel_band_file.close()
# nvg_599_dut.ui_set_band_bandwith_channel('5g', band5_bandwidth, band5_channel)

exit()
#remote_driver = nvg_599_dut.remote_webserver()
#remote_driver.get("http://www.firefox.com")
#nvg_599_dut.enable_sshd_ssh_cli()
#nvg_599_dut.turn_off_supplicant_cli()
#nvg_599_dut.conf_tr69_eco_url()
#url_to_check = "http://192.168.1.254/cgi-bin/home.ha"
#nvg_599_dut.factory_reset_rg(url_to_check)
#nvg_599_dut.enable_parental_control()
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

#url_to_check = "http://192.168.1.254/cgi-bin/home.ha"

nvg_599_dut.factory_reset_rg()
# These are now part of standard factory reset.
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
# statusInfoRegEx = re.compile(r'Model\s(\w+)\s+\w+/\w+\s+AnnexA\s+(\w+)',re.DOTALL)
# statusInfoRegEx = re.compile(r'Model\s(\w+)\s+\w+/\w+.*completed\s+(\w+)',re.DOTALL)
# statusInfoRegEx = re.compile(r'Model\s(\w+)\s+\w+/\w+.*number\s+(\w+).*Uptime\s+(\d\d:\d\d:\d\d:\d\d)',re.DOTALL)
# statusInfoRegEx = re.compile(r'Model\s(\w+).*Serial Number\s+(\d+)',re.DOTALL)
# statusInfoRegEx = re.compile(r'Model\s(\w+)')
# mo1 = statusInfoRegEx.search(statusOutput)

# print(mo1)
# print ('model ', mo1.group(1))

# print ('Serial Number', mo1.group(2))
# print ('Uptime ', mo1.group(3))

 # exit()

# rgModel= mo1.group(1)
# serialNumber= mo1.group(2)
# addition

# if rgModel=='NVG599':
#    print('we are going to instantiate an NVG599')
#    nvg599DUT = Nvg599Class()
#    nvg599DUT.printme()
#    nvg599DUT.turnOffSupplicant()


# else:
#    print('what  to instantiate an NVG599')
#
# exit()


# airTiesTerm = pexpect.spawn("telnet 192.168.1.67")
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
