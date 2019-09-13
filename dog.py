from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from   rgclass import test_house_devices_static_info
# import itertools
import pprint
import wget
from datetime import datetime
# from selenium.webdriver.support.ui import WebDriverWait

import pickle
# import global.py
# import time
# from  pprint import pprint
from openpyxl import Workbook
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

NON_DFS_CHANNELS = {36, 40, 44, 48, 149, 153, 157, 161, 165}
DFS_CHANNELS     = {52, 56, 60, 64, 100, 104, 108, 112, 116, 132, 136, 140, 144}
ALL_BAND5_CHANNELS = {36, 40, 44, 48, 52, 56, 60, 64, 100, 104, 108, 112,
                      116, 132, 136, 140, 144, 149, 153, 157, 161, 165}

# from rgclass import  NON_DFS_CHANNELS
# from rgclass import  DFS_CHANNELS
# Find the current channel used for 5G
# Check the 5G channel used. If none DFS , set to DFS and note the setting
# enter the command to simulate radar detection
# verify that the channel changes to a non DFS channel

# def execute_factory_reset(nvg_599_dut,rf,rfa, test_name):
#     test_status = "Pass"
#     rf.write('Test ' + test_name + '\n')
#     print('Test:' + test_name + '\n')
def test_dfs(nvg_599_dut,rf, rfa, test_name ):
    global NON_DFS_CHANNELS
    global DFS_CHANNELS
    test_status = "Pass"
    rf.write('Test ' + test_name + '\n')
    print('Test:' + test_name + '\n')
    # now = datetime.today().isoformat()
    now = datetime.today().strftime("%B %d, %Y,%H:%M")
    # dfs_results_file = open('dfs_file.txt', 'a')
    # dfs_results_file.write("Test Title:tst_dfs Execution time:")
    # dfs_results_file.write(now)
    # dfs_results_file.write("\n")

    session = nvg_599_dut.session
    home_link = session.find_element_by_link_text("Device")
    home_link.click()
    current_5g_channel = nvg_599_dut.get_ui_home_network_status_value("ui_channel_5g")
    if current_5g_channel in DFS_CHANNELS:
        result = "Current 5G:" + current_5g_channel + " is a DFS channel\n"
        result_str = str(result)
        rf.write('    ' + result_str + '\n')
        print('this is a DFS channel')
    else:
        print('this is a non DFS Changing to DFS channel 100')
        # def ui_set_bw_channel(self, band, bandwidth, channel):
        result = "Current 5G:" + current_5g_channel + " is not a DFS channel\n"
        # result_str = str(result)
        # dfs_results_file.write("Changing to DFS channel 100, bandwidth 80\n")
        rf.write('    ' + 'Changing to DFS channel 100, bandwidth 80\n')

        nvg_599_dut.ui_set_band_bandwith_channel('5g', 80, 100)
        print('setting channel to DFS channel 100')

    nvg_599_dut.login_nvg_599_cli()
    nvg_599_dut.telnet_cli_session.sendline()
    nvg_599_dut.telnet_cli_session.expect(">")
    # this is the IP used for build prior to corvus3 d13/d11
    # nvg_599_dut.telnet_cli_session.sendline("telnet 192.168.1.1")
    nvg_599_dut.telnet_cli_session.sendline("telnet 203.0.113.2")
    nvg_599_dut.telnet_cli_session.expect("#")
    nvg_599_dut.telnet_cli_session.sendline("wl -i eth1 radar 2")
    sleep(10)

    current_5g_channel = nvg_599_dut.get_ui_home_network_status_value("ui_channel_5g")
    current_5g_channel = int(current_5g_channel)

    print('current_5g_channel', current_5g_channel)
    # after the test we expect the channel to have been changed to a non DFS channel

    if current_5g_channel in NON_DFS_CHANNELS:
        #rf.write('    ' + "5G channel changed to non DFS channel: " + '\n')
        # test_status = "Fail"
        rf.write("    5G channel changed to non DFS channel:" + str(current_5g_channel) + " Pass \n" )
        #dfs_results_file.write(str(current_5g_channel))
        #dfs_results_file.write("\n")

        print("Channel change to non DFS  Passed\n")
        print("Setting back to DFS\n")
        rf.write("    Changing back to DFS channel: 100 \n" )

        nvg_599_dut.ui_set_band_bandwith_channel('5g', 80, 100)

        current_5g_channel = nvg_599_dut.get_ui_home_network_status_value("ui_channel_5g")
        if current_5g_channel in DFS_CHANNELS:
            result = "Current 5G:" + current_5g_channel + " is a DFS channel\n"
            rf.write("    Changing back to DFS channel: 100   Pass\n")
            print("Setting back to DFS passed\n")
        # dfs_results_file.write("Test Passed\n")
    else:
        print('test failed:Channel found:', current_5g_channel, ' expected non DFS channel')
        print('current_5g_channel', current_5g_channel)
        result = "Current 5G:" + str(current_5g_channel) + " is a DFS channel\n"
        print("result string  -dbg",result)
        rf.write("    Channel found:" +  str(current_5g_channel) +  'expected non DFS channel    Fail\n')
        test_status = "Fail"
        #results_file.write("Current 5G:" ,current_5g_channel," is not a DFS channel\n")
    return test_status
    # dfs_results_file.write(result)


def tst_speed_test(nvg_599_dut, results_file, test_ip):
    print('in tst_speed_test')
    now = datetime.today().isoformat()
    results_file.write("Test Title:tst_speed_tst Execution time:")
    results_file.write(now)
    results_file.write("\n")
    down_load_speed, up_load_speed = nvg_599_dut.speed_test_cli(test_ip)
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

def tst_ping_ip(nvg_599_dut, ping_history_file, remote_ip):
    print('in tst_ping')
    # ping_history_file  = open('ping_history_file.txt', 'a+')
    ping_history_file = open(ping_history_file, 'a+')
    now = datetime.today().isoformat()
    ping_history_file.write("Test Title:tst_ping Execution time:")
    ping_history_file.write(now)
    ping_history_file.write("\n")
    min_ping,avg_ping,max_ping,mdev_ping = nvg_599_dut.ping_from_local_host(remote_ip)
    min_str = 'Min time: ' + min
    ping_history_file.write(min_str)

    ping_history_file.write("\n")
    avg_str = 'Avg time: ' + avg_ping
    ping_history_file.write(avg_str)

    ping_history_file.write("\n")
    max_str = 'Max time:' + max_ping
    ping_history_file.write(max_str)

    ping_history_file.write("\n")
    mdev_str = 'mdev time:' + mdev_ping
    ping_history_file.write(mdev_str)

    ping_history_file.write("\n")
    print('min: ', min_ping)
    print('avg: ', avg_ping)
    print('max: ', max_ping)
    print('mdev:', mdev_ping)
    return "Pass"

def test_ping_device_name(nvg_599_dut, device_name_to_ping):
    sh_ip_lan_dict = Nvg599Class.cli_sh_rg_ip_lan_info(nvg_599_dut)
    print('dict type' + str(type(sh_ip_lan_dict)))
    for key in sh_ip_lan_dict:
        # print('key----------------------------------------------' + key)
        if sh_ip_lan_dict[key]['Name'] == device_name_to_ping:
            print('found it ' + sh_ip_lan_dict[key]['Name'])
            print('IP is: ' + sh_ip_lan_dict[key]['IP'])
            # we use the  mac from the IP table to get the radio band
            # sh_wi_cl_dict = Nvg599Class.cli_sh_wi_all_clients()
            nvg_599_dut.ping_from_local_host(sh_ip_lan_dict[key]['IP'])

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
            print('band bandwidth channel: ' + str(band5_channel_list[band5_channel]) +
                  "  "  + str(band5_bandwidth_list[band5_bandwidth]))
            print(' ')
            sleep(30)
            nvg_599_dut.ui_set_band_bandwith_channel('5g', band5_bandwidth_list[band5_bandwidth],
                                                     band5_channel_list[band5_channel])
            sleep(60)
            ping_results = nvg_599_dut.ping_check(ip_to_ping)
            print('Channel:' + str(band5_channel_list[band5_channel]) + " Bandwidth:"  +
                  str(band5_bandwidth_list[band5_bandwidth]) + ' Ping result:' + str(ping_results))
        # min_ping, avg_ping, max_ping, mdev_ping = nvg_599_dut.ping_from_local_host('192.168.1.77')
        # print('min_ping:'+  ping_file = open('ping_file.txt', 'a') min_ping + ' avg_ping:' + avg_ping + ' max_ping:' + max_ping)

            channel_band_file.writelines('Channel:' + str(band5_channel_list[band5_channel]) + " Bandwidth:" +
                                         str(band5_bandwidth_list[band5_bandwidth]) + ' Ping result:' + str(ping_results) + '\n')
        #                     self.serial_number + '  min_ping:' + min_ping + '  avg_ping:' +
        #                     '  max_ping:' + max_ping + '  max dev:' + mdev_ping)
    channel_band_file.close()

# experimental
def test_comprehension(firmware_599_available):
    i = 0
    for i in range(len(firmware_599_available)):
        print('list:', str(firmware_599_available[i]))
    upper_case = [item.upper() for item in firmware_599_available]
    print('upper case:', upper_case)


##################################################################################
# use of round function example
# x = 13.73333
# x_round = round(x)
# print('x_round:',x_round)
##################################################################################
import matplotlib.pyplot as plt
import matplotlib.image as img
#
# firmware_599_available =['/home/palmer/Downloads/nvg599-9.2.2h12d9_1.1.bin',
#     '/home/palmer/Downloads/nvg599-9.2.2h12d9_1.1.bin'
#     '/home/palmer/Downloads/nvg599-9.2.2h12d10_1.1.bin',
#     '/home/palmer/Downloads/nvg599-9.2.2h12d13_1.1.bin',
#     '/home/palmer/Downloads/nvg599-9.2.2h13d1_1.1.bin'
#     '/home/palmer/Downloads/nvg599-9.2.2h13d2_1.1.bin'
#     '/home/palmer/Downloads/nvg599-9.2.2h13d3_1.1.bin'
#     '/home/palmer/Downloads/nvg599-9.2.2h13d4_1.1.bin'                         ]


def speed_test_graph_2_devices_plt():
    tablet_download_list = [27.7, 28.9, 27.6, 27.1, 30.1, 29.2, 30.6, 28.1, 29.0, 26.2]
    note8_download_list = [55.3, 54.4, 50.1, 58.2, 48.8, 41.1, 44.0, 44.0, 50.5, 51.7]
    tablet_upload_list = [2.4, 2.3, 2.4, 2.4, 2.1, 2.3, 2.1, 2.2, 2.4, 2.1]
    note8_upload_list = [2.1, 2.1, 2.0, 2.1, 2.4, 2.1, 2.01, 2.1, 2.2, 1.9]
    plt.figure("Test House Speedtest results for NVG 599", figsize=(8, 7))
    # x_label_list = ['9.2.2h12d9','9.2.2h12d10','9.2.2h12d13','9.2.2h13d1 ',
    # '9.2.2h13d2','9.2.2h13d3', '9.2.2h13d4','9.2.2h13d5','9.2.2h13d6']
    # start number,stop number, steps
    ty = arange(1.0, 11.0, 1)
    # tx =  arange(1.0, 10.0, 1)
    # plt.xticks([1,2,3,4,5,6,7,8,9])
    # plt.xticks([1,2,3,4,5,6,7,8,9],x_label_list,rotation='vertical')
    # plt.subplots(2,1,sharey=True)

    subplot(2, 1, 1)
    plt.ylabel('Speed in MBPS')
    title('NVG 599 Download Speed')
    plt.ylim([10, 70])
    plot(ty, tablet_download_list, 'g')
    plot(ty, note8_download_list, 'b')
    plt.grid()
    #
    # plt.legend(bbox_to_anchor=(1, -1.2), ncol=1)
    # plt.legend(bbox_to_anchor=(1, -1.2), ncol=1)

    subplot(2, 1, 2)
    title('NVG 599 Upload Speed')
    plt.ylabel('Speed in MBPS')
    plt.xlabel('Firmware')
    plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], firmware_599_names, rotation='vertical')

    plt.ylim([0, 4])

    plot(ty, tablet_upload_list, 'b', label="Samsung Note8 5 G")
    plot(ty, note8_upload_list, 'g', label="Samsung Tablet 2.4 G")
    plt.legend(bbox_to_anchor=(1, -1.0), ncol=1)
    plt.grid()
    # plt.tight_layout()
    plt.subplots_adjust(left=0.1, right=0.9, bottom=0.4, top=0.9, hspace=0.4)
    plt.legend(bbox_to_anchor=(1, -1.2), ncol=1)
    # now = datetime.today().isoformat()
    # now = datetime.today().isoformat()
    # channel_band_file.write(now + ""Test Title:Channel/Channel band test:" +"\n")
    plt.savefig("/home/palmer/Downloads/speedtest:")
    show()

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
# import matplotlib.pyplot as plt
# import numpy as np
# import matplotlib.pyplot as plt
from pylab import *

# used with plt graphing
def test_rg_upgrade_speedtest(nvg_599_dut, firmware_599_available, firmware_599_names):
    ''' returns tablet_download_list, tablet_upload_list, note8_download_list, note8_upload_list'''
    now = datetime.today().isoformat()
    start_time = datetime.today().strftime("%b-%d-%Y--%H:%M")
    # x = [1, 2, 3, 4, 5, 6, 7, 8]
    note8_file_name = "note8_" + start_time + '.txt'
    tablet_file_name = "tablet_" + start_time + '.txt'

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
        # .67 is  the tablet
        # speed_test_result_tuple_tablet = Nvg599Class.run_speed_test_from_android_termux("192.168.1.67")
        ping_results = nvg_599_dut.ping_check('192.168.1.67')
        # a,b = Nvg599Class.run_speed_test_from_android_termux("192.168.1.67")
        a,b = nvg_599_dut.execute_speed_test_from_android_termux("192.168.1.67")
        print('Tablet ---------------------------------------------firmware:' + str(firmware))
        # print("speed_test_result_tuple:", speed_test_result_tuple_tablet)
        # for a, b in speed_test_result_tuple_tablet:
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
        a,b = nvg_599_dut.execute_speed_test_from_android_termux("192.168.1.70")
        # for a, b in speed_test_result_tuple_note8:
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

    # tablet_file.close()
    # tablet_download_list
    # note8_download_list
    plt.figure("Test House Speedtest results for NVG 599 ", figsize=(8, 7))
    ty = arange(1.0, 12.0, 1)
#    ty = arange(1.0, 10.0, 1)
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
    plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], firmware_599_names, rotation='vertical')

    plot(ty, tablet_upload_list, 'b', label='Tablet')
    plot(ty, note8_upload_list, 'g', label='Note8')
    plt.legend(bbox_to_anchor=(1, -1.2), ncol=1)

    plt.grid()
    plt.tight_layout()
    plt.subplots_adjust(left=0.1, right=0.9, bottom=0.2, top=0.9)
    plt.savefig("/home/palmer/Downloads/speedtest:" + start_time)
    plt.savefig("thisisit")
    show()
    return tablet_download_list, tablet_upload_list, note8_download_list, note8_upload_list

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
        '9.2.2h13d8'
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

# Nvg599Class.run_speed_test_from_android_termux('192.168.1.67')
# Nvg599Class.get_wifi_info_from_android_termux('192.168.1.70')


# Nvg599Class.wait_for_ssh_to_be_ready('192.168.1.70', '8022', '20', '1')
# exit()

# def pickle_test():
#     note8_upload_list = [2.1, 2.1, 2.0, 2.1, 2.4, 2.1, 2.01, 2.1, 2.2, 1.9]
#     pickle.dump(note8_upload_list, open("mypickle.p","wb"))
#     new_pickle= pickle.load( open("mypickle.p","rb"))
#     print('new_pickle',new_pickle)
# pickle_test()
# print('done')
# exit()

# return min_ping, avg_ping, max_ping, mdev_ping
#mina, avga, maxa, mdeva  =  nvg_599_dut.ping_from_local_host("192.168.1.70")
#print('min:' + str(mina) + ' max:' + str(maxa) +  ' avg: ' + avga)
#exit()
# ################  This is the one I want
# now = datetime.today().strftime("%B %d, %Y,%H:%M")
# ########################################

def tst_ping_rg_power_level(nvg_599_dut, remote_ip, number_of_pings):
# def tst_ping_rg_power_level(nvg_599_dut, remote_ip, number_of_pings):
    ping_file = open('tst_ping_with_power_change.txt', 'a')
    ping_file.writelines('tst_ping_rg_power_level' + '\n')
    now = datetime.today().strftime("%B %d, %Y,%H:%M")
    ping_file.writelines('Date:' + now + '  599 FW Ver:' + nvg_599_dut.software_version + '  Ser. No:' + nvg_599_dut.serial_number + '\n\n')

    nvg_599_dut.disable_enable_wifi_2_4g('On')
    sleep(60)
    nvg_599_dut.disable_enable_wifi_5g('On')
    sleep(60)
    nvg_599_dut.set_wifi_power_level('band2', '100')
    nvg_599_dut.set_wifi_power_level('band5', '100')

    nvg_599_dut.disable_enable_wifi_5g('Off')
    sleep(120)
    min_ping, avg_ping, max_ping, mdev_ping, sent, received, loss = nvg_599_dut.ping_from_local_host(remote_ip,number_of_pings)
    print('min:' + min_ping + ' max:' + max_ping)

    ping_file.writelines('Band:' + 'band2' + '  Ping: ' + remote_ip + '  RG Pwr: 100%' +
                     '  Sent:' + sent + '  Received:' + received + '  Percent loss:' + loss + '%\n')

    ping_file.writelines('Minimum:' + min_ping + '  Average::' + avg_ping + '  Maximum:' + max_ping + ' Max dev:' + mdev_ping + '\n')
    ping_file.writelines('\n')
    print('xx2')
    nvg_599_dut.set_wifi_power_level('band2', '50')
    sleep(120)
    min_ping, avg_ping, max_ping, mdev_ping, sent, received, loss = nvg_599_dut.ping_from_local_host(remote_ip,number_of_pings)

    ping_file.writelines('Band:' + 'band2' + '  Ping: ' + remote_ip + '  RG Pwr: 50%' +
                      '  Sent:' + sent + '  Received:' + received + '  Percent loss:' + loss + '%\n')
    ping_file.writelines('Minimum:' + min_ping + '  Average::' + avg_ping + '  Maximum:' + max_ping + ' Max dev:' + mdev_ping + '\n')

    print('xx2')
    # restore  band2
    ping_file.writelines('\n')
    # nvg_599_dut.disable_enable_wifi_2_4g('On')
    nvg_599_dut.set_wifi_power_level('band2', '100')
    sleep(120)
    # 5g section (band 5)
    # nvg_599_dut.disable_enable_wifi_5g('On')
    nvg_599_dut.disable_enable_wifi_5g('On')
    sleep(120)
    nvg_599_dut.set_wifi_power_level('band5', '100')
    sleep(120)
    nvg_599_dut.disable_enable_wifi_2_4g('Off')
    sleep(120)

    min_ping, avg_ping, max_ping, mdev_ping, sent, received, loss = nvg_599_dut.ping_from_local_host(remote_ip,number_of_pings)
    print('min:' + min_ping + ' max:' + max_ping)

    ping_file.writelines('Band:' + 'band5' + '  Ping: ' + remote_ip + '  RG Pwr: 100%' +
                     '  Sent:' + sent + '  Received:' + received + '  Percent loss:' + loss + '%\n')
    ping_file.writelines(
        'Minimum:' + min_ping + '  Average::' + avg_ping + '  Maximum:' + max_ping + ' Max dev:' + mdev_ping + '\n')
    ping_file.writelines('\n')
    print('xxx3')
    nvg_599_dut.set_wifi_power_level('band5', '50')
    sleep(120)
    min_ping, avg_ping, max_ping, mdev_ping, sent, received, loss = nvg_599_dut.ping_from_local_host(remote_ip, number_of_pings)

    ping_file.writelines('Band:' + 'band5' + '  Ping: ' + remote_ip + '  RG Pwr: 50%' +
                     '  Sent:' + sent + '  Received:' + received + '  Percent loss:' + loss + '%\n')
    ping_file.writelines('Minimum:' + min_ping + '  Average::' + avg_ping + '  Maximum:' + max_ping + ' Max dev:' + mdev_ping + '\n')
    ping_file.writelines('\n')
    print('xxx4')
    nvg_599_dut.set_wifi_power_level('band5', '100')
    # sleep(90)

    ping_file.writelines('-----------------------------------------------------------------------------------' + '\n')
    ping_file.writelines('----------------------------------------------------------------------------------' + '\n')

    ping_file.writelines('\n')
    ping_file.close()

    nvg_599_dut.disable_enable_wifi_5g('On')
    nvg_599_dut.disable_enable_wifi_2_4g('On')
    # band = 'band5'
    # percentage = 100
    nvg_599_dut.set_wifi_power_level('band2', '100')
    # band = 'band2'
    nvg_599_dut.set_wifi_power_level('band5', '100')

def tst_android_speed_test(nvg_599_dut, remote_ip):
    # this test logins to the remote android device and executes a speed test
    # def tst_ping_rg_power_level(nvg_599_dut, remote_ip, number_of_pings):
    tst_android_speed_file = open('tst_android_speed_test.txt', 'a')
    tst_android_speed_file.writelines('tst_android_speed_test: Remote IP:' + remote_ip + '\n')
    now = datetime.today().strftime("%B %d, %Y,%H:%M")
    tst_android_speed_file.writelines('Date:' + now + '  599 FW Ver:' + nvg_599_dut.software_version +
        '  Ser. No:' + nvg_599_dut.serial_number + '\n')
    nvg_599_dut.disable_enable_wifi_5g('Off')
    sleep(120)
    #down_load_speed, up_load_speed = Nvg599Class().execute_speed_test_from_android_termux(remote_ip)
    down_load_speed, up_load_speed = nvg_599_dut.execute_speed_test_from_android_termux(remote_ip)

    tst_android_speed_file.writelines(
        'Band 2 Download Speed:' + down_load_speed + 'Band 2 Upload speed:' + up_load_speed + '\n\n')

    nvg_599_dut.disable_enable_wifi_5g('On')
    sleep(120)

    # Band 5
    nvg_599_dut.disable_enable_wifi_2_4g('Off')
    sleep(120)

    down_load_speed, up_load_speed = Nvg599Class().run_speed_test_from_android_termux(remote_ip)
    tst_android_speed_file.writelines(
        'Band 5 Download Speed:' + down_load_speed + 'Band 5 Upload speed:' + up_load_speed + '\n\n')

    nvg_599_dut.disable_enable_wifi_2_4g('On')
    sleep(120)
    tst_android_speed_file.writelines('-----------------------------------------------------------------------' + '\n')
    tst_android_speed_file.writelines('-----------------------------------------------------------------------' + '\n')
    tst_android_speed_file.writelines('\n')
    tst_android_speed_file.close()

# -pfp-
# deprecated
############################## DEPRECATED   ####################################################################################################
# def tst_ping_rg_power_level_orig(nvg_599_dut, band, percentage, remote_ip, number_of_pings):
#     print('testing ping after power level changes')
#
#     if band == 'band2':
#         nvg_599_dut.disable_enable_wifi_2_4g('On')
#         nvg_599_dut.disable_enable_wifi_5g('Off')
#     else:
#         # this is band 5
#         nvg_599_dut.disable_enable_wifi_5g('On')
#         nvg_599_dut.disable_enable_wifi_2_4g('Off')
#     nvg_599_dut.set_wifi_power_level(band, percentage)
#     min_ping, avg_ping, max_ping, mdev_ping, sent, received, loss = nvg_599_dut.ping_from_local_host(remote_ip,
#                                                     number_of_pings)
#     print('min:' + min_ping + ' max:' + max_ping)
#     ping_file = open('ping_file_with_power_change_test.txt', 'a')
#     now = datetime.today().strftime("%B %d, %Y,%H:%M")
#     ping_file.writelines('Date:' + now + '  599 FW Ver:' + nvg_599_dut.software_version + '  Ser. No:' + nvg_599_dut.serial_number + '\n')
#     ping_file.writelines('Band:' + band + '  Ping: ' + remote_ip + '  RG Pwr:' + str(percentage) + '%' +
#                          '  Sent:' + sent + '  Received:' + received + '  Percent loss:' + loss + '%\n')
#     ping_file.writelines(
#         'Minimum:' + min_ping + '  Average::' + avg_ping + '  Maximum:' + max_ping + ' Max dev:' + mdev_ping + '\n')
#     ping_file.writelines('\n')
#     ping_file.close()
#     nvg_599_dut.disable_enable_wifi_5g('On')
#     nvg_599_dut.disable_enable_wifi_2_4g('On')
#     band = 'band5'
#     percentage = 100
#     nvg_599_dut.set_wifi_power_level(band, percentage)
#     band = 'band2'
#     nvg_599_dut.set_wifi_power_level(band, percentage)
from datetime import datetime

def test_auto_ssid_default_tr69_values(nvg_599_dut, ssid, rf, rfa):
    default_tr69_auto_ssid_values = nvg_599_dut.get_tr69_auto_ssid(ssid)
    test_status = "Pass"
    if (default_tr69_auto_ssid_values.find('.' + ssid + '.Enable 0') != -1):
        print('Pass ssid:' + ssid + ' Default set to 0')
        rf.write('    Pass ssid:' + ssid + ' Default set to 0 \n')
    else:
        print('Fail ssid:' + ssid + ' default not set to 0')
        rf.write('    Fail ssid:' + ssid + ' default not set to 0 \n')
        test_status = "Fail"
        # return("Fail", "Default Enable not set to 0")

    if default_tr69_auto_ssid_values.find('.' + ssid + '.Status Disabled 0') != -1:
        print('Pass ssid:' + ssid + ' Default Status set to Disabled')
        rf.write('    Pass ssid:' + ssid + ' Default Status set to Disabled \n')
    else:
        print('Fail ssid:' + ssid + ' Default Status not set to Disabled')
        rf.write('    Fail ssid:' + ssid + ' Default Status not set to Disabled \n')
        test_status = "Fail"
        # return ("Fail: SSID:" + ssid + " Status not set to Disabled")

    if default_tr69_auto_ssid_values.find('.' + ssid + '.SSID TBD') != -1:
        print('Pass ssid:' + ssid + ' Default SSID set to TBD')
        rf.write('    Pass ssid:' + ssid + ' Default SSID set to TBD \n')
    else:
        print('Fail ssid:' + ssid + ' Default SSID not set to TBD')
        rf.write('    Fail ssid:' + ssid + ' Default SSID not set to TBD \n')
        test_status = "Fail"
        # return ('Fail: SSID:' + ssid + ' Default SSID not set to TBD')
    if default_tr69_auto_ssid_values.find('.' + ssid + '.X_0000C5_DefaultSSID TBD') != -1:
        print('Pass ssid:' + ssid + ' Default SSID set to TBD')
        rf.write('Pass ssid:' + ssid + ' Default SSID set to TBD \n')
    else:
        print('Fail ssid:' + ssid + ' Default SSID not set to TBD')
        rf.write('    Fail ssid:' + ssid + ' Default SSID not set to TBD \n')
        test_status = "Fail"
        # return ('Fail: SSID:' + ssid + ' Default SSID not set to TBD')
    if default_tr69_auto_ssid_values.find('.' + ssid + '.SSID TBD') != -1:
        print('Pass ssid:' + ssid + '  SSID set to TBD')
        rf.write('    Pass ssid:' + ssid + '  SSID set to TBD \n')
    else:
        print('Fail ssid:' + ssid + ' SSID not set to TBD')
        rf.write('    Fail ssid:' + ssid + ' SSID not set to TBD \n')
        test_status = "Fail"
        # return ('Fail: SSID:' + ssid + '  SSID not set to TBD')
    if (default_tr69_auto_ssid_values.find('.' + ssid + '.X_0000C5_Encryption AESEncryption') != -1):
        print('Pass ssid:' + ssid + ' Encryption set to AESEncryption')
        rf.write('    Pass ssid:' + ssid + ' Encryption set to AESEncryption \n')
    else:
        print('Fail ssid:' + ssid + ' Default Encryption not set to AESEncryption')
        rf.write('    Fail ssid:' + ssid + ' Default Encryption not set to AESEncryption \n')
        test_status = "Fail"
        # return ('Fail: SSID:' + ssid + '  Encryption not set to AESEncryption')
    if (default_tr69_auto_ssid_values.find('.' + ssid + '.X_0000C5_Authentication WPA2PSKAuthentication') != -1):
        print('Pass ssid:' + ssid + ' Authentication set to WPA2PSKAuthentication')
        rf.write('    Pass ssid:' + ssid + ' Authentication set to WPA2PSKAuthentication \n')
    else:
        print('Fail ssid:' + ssid + ' Default Authentication not set to WPA2PSKAuthentication')
        rf.write('    Fail ssid:' + ssid + ' Default Authentication not set to WPA2PSKAuthentication \n')
        test_status = "Fail"
        # return ('Fail: SSID:' + ssid + ' Default Authentication not set to WPA2PSKAuthentication')
    if (default_tr69_auto_ssid_values.find('.' + ssid + '.X_0000C5_KePasysphrase TBD') != -1):
        print('Pass ssid:' + ssid + ' Default KeyPassphrase set to TBD')
        rf.write('    Pass ssid:' + ssid + ' Default KeyPassphrase set to TBD \n')
    else:
        print('Fail ssid:' + ssid + ' Default KeyPassphrase not set to TBD')
        rf.write('    Fail ssid:' + ssid + ' Default KeyPassphrase not set to TBD \n')
        test_status = "Fail"
        #return ('Fail: SSID:' + ssid + ' Default KeyPassphrase not set to BD')
    if (default_tr69_auto_ssid_values.find('.' + ssid + '.X_0000C5_MaxClients 3') != -1):
        print('Pass ssid:' + ssid + ' Default MaxClients set to 3')
        rf.write('    Pass ssid:' + ssid + ' Default MaxClients set to 3 \n')
    else:
        print('Fail ssid:' + ssid + ' Default MaxClients not set to 3')
        rf.write('    Fail ssid:' + ssid + ' Default MaxClients not set to 3 \n')
        test_status = "Fail"
    if (default_tr69_auto_ssid_values.find('.' + ssid + '.SSIDAdvertisementEnabled 0') != -1):
        print('Pass ssid:' + ssid + ' Default SSIDAdvertisementEnabled set to 0')
        rf.write('    Pass ssid:' + ssid + ' Default SSIDAdvertisementEnabled set to 0 \n')
    else:
        print('Fail ssid:' + ssid + ' Default SSIDAdvertisementEnabled not set to 0')
        rf.write('    Fail ssid:' + ssid + ' Default SSIDAdvertisementEnabled not set to 0 \n')
        test_status = "Fail"
        # return ('Fail: SSID:' + ssid + ' Default KepPassphrase not set to BD')
    return test_status

def get_upgrade_file_from_my_win10(nvg_599_dut,win10_laptop, test_house_devices_static_info,  rf, rfa ):
    print('get_upgrade_file_from win10_laptop')
    rf.write('get_upgrade_file_from win10_laptop' + '\n')



# test_house_devices_static_info = {
#     '88:41:FC:86:64:D6': {'device_type': 'airties_4920', 'oper_sys': 'tbd', 'radio': 'abg', 'band': '2',
#                           'state': 'None',
#                           'address_type': 'None', 'port': 'None', 'ssid': 'None', 'rssi': 'None', 'ip': 'None',
#                           'device_test_name': 'airties_1_2g', 'name': 'ATT_4920_8664D4', 'location': 'master_bedroom'},



# def test_speedtest_from_android(nvg_599_dut,device, test_house_devices_static_info, test_name,  rf, rfa ):
def test_speedtest_from_android(nvg_599_dut, device_name, test_house_devices_static_info, test_name, rf, rfa):

    print('in android speed test   device name  is:' + str(device_name))
    rf.write('Test ' + test_name +  '  Device:' + device_name + '\n')
    print('Test:' + test_name + '  Device name:' + device_name + '\n')
    # rf.write('test_speedtest_from_android' + '\n')

    # if device == 'Galaxy-Note8':
    # first get the mac of the device from the dict of known test house devices
    # I had this idea that we could use a device type and then select the first availabe device of that type
    # I decided to abandon that approach and use the device name. We want to know what device we are going to use

    # for key in test_house_devices_static_info:
    #     print('key :' + str(key) + 'device: ' + str(test_house_devices_static_info[key]['device_type']))
    #
    #     if test_house_devices_static_info[key]['device_type'] == device:
    #         device_mac = key
    #         print('device mac:' + str(device_mac))
    #         break

    nvg_599_dut.login_nvg_599_cli()
    ip_lan_info_dict = nvg_599_dut.cli_sh_rg_ip_lan_info()
    # first translate the device name to a mac using the

    for x, y in ip_lan_info_dict.items():
        print(x, y)

    device_ip = "0.0.0.0"

    for device_mac in ip_lan_info_dict:
        if device_name == ip_lan_info_dict[device_mac]['Name']:
            device_ip = ip_lan_info_dict[device_mac]['IP']

    # if 'b8:d7:af:aa:27:c3' in ip_lan_info_dict:
    # if device_mac in ip_lan_info_dict:
    if device_ip != "0.0.0.0" :
        # note_8_ip = ip_lan_info_dict['b8:d7:af:aa:27:c3']['IP']
        # device_ip = ip_lan_info_dict[device_mac]['IP']
        rf.write('    Android device IP  present in cli command sh ip lan: ' + device_ip )

        print('device is present :' + str(device_ip))
    else:
        rf.write('    Android device IP not present in cli command sh ip lan, Aborting test')
        print('Android device IP not present in cli command sh ip lan')
        return "Fail"
    nvg_599_dut.execute_speedtest_from_android_termux(device_ip, rf, rfa)
    return "Pass"


# def upgrade_rg_cli(self, tftp_server_name, install_bin_file, rf, rfa, test_name):
def test_rg_upgrade(nvg_599_dut, tftp_server_name , install_bin_file,  rf, rfa, test_name):
    #upgrade_rg_file = '/home/palmer/Downloads/nvg599-9.2.2h13d23_1.1.bin'
    rf.write('Test ' + test_name + '\n')
    test_status = nvg_599_dut.upgrade_rg_cli(tftp_server_name, install_bin_file, rf, rfa)
    if test_status == "Fail":
        rf.write('    Fail: Upgrade failed')
        # nvg_599_dut.session_cleanup()
        return "Fail"
    else:
        rf.write('    Pass: RG upgraded to:' + upgrade_file_path)
        sleep(300)
        return "Pass"
# we don't expect factory reset to to fail, it should always return a duration
def execute_factory_reset(nvg_599_dut,rf,rfa, test_name):
    test_status = "Pass"
    rf.write('Test ' + test_name + '\n')
    print('Test:' + test_name + '\n')
    reset_duration = nvg_599_dut.factory_reset_rg(rf, rfa)
    if reset_duration == "Fail":
        #rf.write('    Fail: Factory reset failed')
        print('Test:' + test_name + ":" + reset_duration + '\n\n')
        rf.write('     Test:' + test_name + ":" + reset_duration + '\n\n')
        nvg_599_dut.session_cleanup()
        return "Fail"
    else:
        sleep(200)
        print('Test:' + test_name + ":" + reset_duration + '\n\n')
        rf.write('     Test:' + test_name + ":" + reset_duration + '\n\n')
        return "Pass"

def setup_auto_ssid_via_tr69(nvg_599_dut,ssid, max_clients,  rf, rfa, test_name):
    rf.write('Test ' + test_name + " " + ssid + '\n')
    print('Test:' + test_name + " " +  ssid + '\n')
    setup_status = nvg_599_dut.set_auto_setup_ssid_via_tr69_cli(ssid, rf, rfa)
    if setup_status == "Fail":
        rf.write('    Fail: Auto setup ssid' + str(ssid) + 'failed\n')
    print('Test:' + test_name + " " + ssid + ":" + setup_status + '\n')
    rf.write('     Test:' + test_name + " " + ssid + ":" + setup_status + '\n\n')

def verify_auto_info_not_present_in_ui(nvg_599_dut, rf, rfa, test_name):
    status_page = nvg_599_dut.get_ui_home_network_status_page_source()
    rf.write('Test ' + test_name  + '\n')
    print('Test:' + test_name  + '\n')
    # default_tr69_auto_ssid_values = nvg_599_dut.get_tr69_auto_ssid(ssid)
    verify_auto_info_status = "Pass"
    if (status_page.find('172.16') == -1):
        print('Pass: 172.16 not found in status page')
        rf.write('     172.16 not found in status page:OK\n')
    else:
        print('Fail: 172.16  found in status page')
        rf.write('     172.16  found in status page:Fail\n')
        verify_auto_info_status = "Fail"
    status_page = nvg_599_dut.get_home_network_ip_allocation_page_source()

    if (status_page.find('172.16') == -1):
        print('Pass: 172.16.x.x  not found in IP allocation page')
        rf.write('     172.16.x.x  not found in IP allocation page:OK\n')
    else:
        print('Fail: 172.16.x.x  found in IP allocation page')
        rf.write('     172.16  found in status page:Fail\n')
        verify_auto_info_status = "Fail"
        # return("Fail", "Default Enable not set to 0")
    print('Test:' + test_name + ":" + verify_auto_info_status + '\n\n')
    rf.write('     Test:' + test_name + ":" + verify_auto_info_status + '\n\n')
    return "Fail"

def verify_auto_ssid_defaults_via_tr69(nvg_599_dut, auto_ssid_number, default_ssid, default_pass_phrase,  rf, rfa, test_name):
    tr69_output = nvg_599_dut.get_tr69_parameters_for_ssid(auto_ssid_number, rf, rfa)
    auto_ssid_defaults_status = "Pass"
    rf.write('Test ' + test_name + " " + "SSID:" + auto_ssid_number + '\n')
    print('Test:' + test_name + " " + auto_ssid_number + '\n')

    if 'WLANConfiguration.' + auto_ssid_number + '.Enable 0' in  tr69_output:
        rf.write('     Found WLANConfiguration.' + auto_ssid_number + '.Enable 0:OK\n')
        print('Found WLANConfiguration.' + str(auto_ssid_number) + '.Enable 0:OK')
    else:
        rf.write('     Found WLANConfiguration.' + str(auto_ssid_number) + '.Enable 0: Not Found\n')
        auto_ssid_defaults_status = "Fail"


    #if 'WLANConfiguration.' + auto_ssid_number + '.SSID' + default_ssid' in  tr69_output:
    #if 'WLANConfiguration.' + auto_ssid_number + '.SSID ATT4ujR48s_REPLACEME_' in  tr69_output:

    if 'WLANConfiguration.' + auto_ssid_number + '.SSID ' + default_ssid in  tr69_output:
        #rf.write('     Found SSID ATT4ujR48s_REPLACEME_:OK\n')

        rf.write('     Found ' + default_ssid + ':OK\n')
        print('Found ' + default_ssid + ':OK\n')
    else:
        rf.write('     Default ssid ' + default_ssid + ':Not found\n')
        print('Not found ' + default_ssid + ':Fail\n')

        #rf.write('     SSID ATT4ujR48s_REPLACEME_: Not Found\n')
        auto_ssid_defaults_status = "Fail"

    if "KeyPassphrase " + default_pass_phrase in  tr69_output:
        rf.write('     Found KeyPassphrase ' + default_pass_phrase + ':OK\n')
        print('Found KeyPassphrase ' + default_pass_phrase + ':OK')
    else:
        rf.write('     KeyPassphrase ' + default_pass_phrase + ': Not Found\n')
        print('Not Found KeyPassphrase ' + default_pass_phrase + ':Fail')

        auto_ssid_defaults_status = "Fail"

    if "Authentication WPA2PSKAuthentication" in tr69_output:
        rf.write('     WPA2PSKAuthentication:OK\n')
        print('Found WPA2PSKAuthentication:OK\n')
    else:
        rf.write('     WPA2PSKAuthentication: Not Found\n')
        print('Not Found WPA2PSKAuthentication:Fail\n')

        auto_ssid_defaults_status = "Fail"

    if "MaxClients 3" in  tr69_output:
        rf.write('     MaxClients 3:OK\n')
        print('Found MaxClients 3:OK')
    else:
        rf.write('     MaxClients 3: Not Found\n')
        auto_ssid_defaults_status = "Fail"
        print('Not Found MaxClients 3:Fail')

    rf.write('     Test:' + test_name + " " + auto_ssid_number + ":" + auto_ssid_defaults_status + '\n\n')
    print('Test:' + test_name + " " + auto_ssid_number + ":" + auto_ssid_defaults_status + '\n')

    return auto_ssid_defaults_status

def ping_gw_from_4920(nvg_599_dut,rf,rfa, test_name, airties_ip = 'Default'):
    test_status = "Pass"
    rf.write('Test ' + test_name + '\n')
    print('Test:' + test_name + '\n')
    # we ip_of_airties = None then we get the first associated 4920 IP.
    # this is not needed here
    ip_4920 = "None"
    if airties_ip == 'Default':
        ip_lan_dict = nvg_599_dut.cli_sh_rg_ip_lan_info()
        for dict_key in ip_lan_dict:
            if ("ATT_49" in ip_lan_dict[dict_key]['Name']) and (ip_lan_dict[dict_key]['State'] == "on"):
                ip_4920 = ip_lan_dict[dict_key]["IP"]
                print('using this is 4920 ip =:' + str(ip_lan_dict[dict_key]["IP"]))

        if ip_4920 == "None":
             rf.write('    No Airties devices in IP lan: Fail\n')
             print('No Airties devices in IP lan: Fail\n')
             # No point in continuing
             return "Fail"
    else:
        ip_4920 = airties_ip

    airties_session = nvg_599_dut.static_login_4920(ip_4920)
    airties_session.sendline('ping -c 4 192.168.1.254')
    airties_session.expect('#')
    ping_output = airties_session.before
    print('ping output' + str(ping_output))

    if "0% packet loss" in ping_output:
        print('ping from  airties:' + str(ip_4920) + 'to RG succeeded' + str(ping_output))
        rf.write('     ping from airties:' + str(ip_4920) + ' to RG 192.168.1.254 0% packet loss:OK\n\n')
    else:
        print('ping failed')
        rf.write('     ping 192.168.1.254 failed:Fail\n\n')
        test_status = "Fail"

    airties_session.sendline('exit')
    #
    # nvg_599_dut.telnet_cli_session.close
    return test_status

def ping_airties_from_rg(nvg_599_dut,rf, rfa, test_name, airties_ip = 'Default'):
    test_status = "Pass"
    rf.write('Test ' + test_name + '\n')
    print('Test:' + test_name + '\n')
    # we ip_of_airties = None then we get the first associated 4920 IP.
    # this is not needed here
    ip_4920 = "None"
    if airties_ip == 'Default':
        ip_lan_dict = nvg_599_dut.cli_sh_rg_ip_lan_info()
        for dict_key in ip_lan_dict:
            if ("ATT_49"  in ip_lan_dict[dict_key]['Name']) and (ip_lan_dict[dict_key]['State'] == "on"):
                ip_4920 = ip_lan_dict[dict_key]["IP"]
                print('using this is 4920 ip =:' + str(ip_lan_dict[dict_key]["IP"]))

        if ip_4920 == "None":
            rf.write('    No Airties devices in IP lan: Fail\n')
            print('No Airties devices in IP lan: Fail\n')
            # No point in continuing
            return "Fail"
    else:
        ip_4920 = airties_ip
    nvg_cli_session = nvg_599_dut.login_nvg_599_cli()
    # airties_session = nvg_599_dut.static_login_4920(ip_4920)
    nvg_cli_session.sendline('ping -c 4 ' + ip_4920)
    nvg_cli_session.expect("MAGIC/UNLOCKED>")
    ping_output = nvg_cli_session.before
    print('ping output pinging 4920 frm gw' + str(ping_output))

    if "0% packet loss" in ping_output:
        print('ping airties:' + str(ip_4920) + 'from RG succeeded' + str(ping_output))
        rf.write('     ping to airties:' + str(ip_4920) + ' from RG 192.168.1.254 0% packet loss:OK\n\n')
    else:
        print('ping failed')
        rf.write('     ping  to airties' + str(ip_4920) + 'from RG 192.168.1.254 failed:Fail\n\n')
        test_status = "Fail"
    nvg_cli_session.sendline('exit')
    return test_status

def verify_airties_build_versions(nvg_599_dut,rf, rfa, test_name, default_2g_fw = 'AT.922.13.3.73', default_5g_fw = 'AT.922.13.3.74'):
    test_status = "Pass"
    rf.write('Test ' + test_name + '\n')
    print('Test:' + test_name + '\n')
    nvg_599_dut.login_nvg_599_cli()
    nvg_599_dut.telnet_cli_session.sendline('!')
    nvg_599_dut.telnet_cli_session.expect('#')
    nvg_599_dut.telnet_cli_session.sendline('cat /airties/etc/buildversion')
    nvg_599_dut.telnet_cli_session.expect('#')
    fw_2g_output = nvg_599_dut.telnet_cli_session.before
    print('2g>'+ str(fw_2g_output) + '<')
    if default_2g_fw in fw_2g_output:
        rf.write('     Airties build vers. 2g matches default:' + default_2g_fw + ':OK\n')
    else:
        rf.write('     Airties build vers. 2g build mismatch:' + default_2g_fw + ':Fail\n')
        test_status = "Fail"

    nvg_599_dut.telnet_cli_session.sendline('telnet 203.0.113.2')
    nvg_599_dut.telnet_cli_session.expect('#')
    nvg_599_dut.telnet_cli_session.sendline('/airties/usr/bin/fwversion')
    nvg_599_dut.telnet_cli_session.expect('#')
    fw_5g_output = nvg_599_dut.telnet_cli_session.before
    print('5g>'+ str(fw_5g_output) + '<')
    if default_5g_fw in fw_5g_output:
        rf.write('     Airties build vers. 5g matches default:' + default_5g_fw + ':OK\n')
    else:
        rf.write('     Airties build vers. 5g build mismatch:' + default_5g_fw + ':Fail\n')
        test_status = "Fail"
    rf.write('\n')

    nvg_599_dut.telnet_cli_session.sendline('exit')
    nvg_599_dut.telnet_cli_session.expect('#')
    nvg_599_dut.telnet_cli_session.sendline('exit')
    nvg_599_dut.telnet_cli_session.expect('>')
    nvg_599_dut.telnet_cli_session.sendline('exit')
    # nvg_599_dut.telnet_cli_session.close
    return test_status

def verify_airties_hello_packet_count_increasing(nvg_599_dut,rf, rfa, test_name, airties_ip = 'Default'):
    test_status = "Pass"
    rf.write('Test ' + test_name + '\n')
    print('Test:' + test_name + '\n')
    # we ip_of_airties = None then we get the first associated 4920 IP.
    # this is not needed here
    ip_4920 = "None"
    if airties_ip == 'Default':
        ip_lan_dict = nvg_599_dut.cli_sh_rg_ip_lan_info()
        for dict_key in ip_lan_dict:
            if ("ATT_49"  in ip_lan_dict[dict_key]['Name']) and (ip_lan_dict[dict_key]['State'] == "on"):
                ip_4920 = ip_lan_dict[dict_key]["IP"]
                print('using this is 4920 ip =:' + str(ip_lan_dict[dict_key]["IP"]))

        if ip_4920 == "None":
             rf.write('    No Airties devices in IP lan: Fail\n')
             print('No Airties devices in IP lan: Fail\n')
             # No point in continuing
             return "Fail"
    else:
        ip_4920 = airties_ip
    airties_session = nvg_599_dut.static_login_4920(ip_4920)
    airties_session.sendline('cat /proc/mesh-ng-topology | grep hello')
    airties_session.expect('#')
    hello_output = airties_session.before
    print('hello output' + str(hello_output))
    hello_count_reg_ex = re.compile(r'hello:\s+(\d+)')
    mo1 = hello_count_reg_ex.search(hello_output)
    first_count = int(mo1.group(1))
    # first_count = str(mo1.group(1))

    print('count is:' + str(mo1.group(1)))
    sleep(5)

    airties_session.sendline('cat /proc/mesh-ng-topology | grep hello')
    airties_session.expect('#')
    hello_output = airties_session.before
    print('hello output' + str(hello_output))
    hello_count_reg_ex = re.compile(r'hello:\s+(\d+)')
    mo1 = hello_count_reg_ex.search(hello_output)
    # second_count = str(mo1.group(1))
    second_count = int(mo1.group(1))

    if (second_count - first_count > 0):
        print('checking hellos on airties: second hello count:' + str(second_count) + ' is greater than first hello count ' + str(first_count) + ':OK')
        rf.write('     Hellos on airties: second hello count: ' + str(second_count) + ' is greater than first hello count: ' + str(first_count) + ':OK\n\n')
    else:
        print(' hellos on airties: second hello count:' + str(second_count) + ' not greater than first hello count' + str(
            first_count) + ':Fail')
        rf.write('     Hellos on airties: second hello count: ' + str(second_count) + ' not greater than first hello count: ' + str(
            first_count) + ':Fail\n\n')
        test_status = "Fail"
    airties_session.sendline('exit')
    return test_status

def verify_google_ping_from_rg_5g(nvg_599_dut,rf,rfa, test_name):
    test_status = "Pass"
    rf.write('Test ' + test_name + '\n')
    print('Test:' + test_name + '\n')
    nvg_599_dut.login_nvg_599_band5_cli()
    nvg_599_dut.telnet_cli_session.sendline('ping -c 4 8.8.8.8')
    nvg_599_dut.telnet_cli_session.expect('#')
    ping_output = nvg_599_dut.telnet_cli_session.before

    if "0% packet loss" in ping_output:
        print('ping succeeded'+ str(ping_output))
        rf.write('     ping google (8.8.8.8) from GW 5g 0% packet loss:OK\n\n')
    else:
        print('ping failed')
        rf.write('     ping 8.8.8.8 failed:Fail\n\n')

    nvg_599_dut.telnet_cli_session.sendline('exit')
    nvg_599_dut.telnet_cli_session.expect('>')
    #
    # nvg_599_dut.telnet_cli_session.close
    return test_status


from rgclass import nvg_info

def url_att_topology_smoke(nvg_599_dut, url_to_return, rf, rfa, test_name):
    test_status = "Pass"
    rf.write('Test ' + test_name + '\n')
    print('Test:' + test_name + '\n')
    decoded_html = nvg_599_dut.urllib_get_rg_file(url_to_return, rf, rfa)
    rg_serial_number = nvg_599_dut.serial_number
    nvg_5g_mac = nvg_info[rg_serial_number]['mac5g']
    print ('nvg_mac_5g: ' + str(nvg_5g_mac) + '\n')
    print ('decoded: ' + str(decoded_html) +  '>end_decoded \n')
    ip_5g_side = "203.0.113.2"
    #topology_regex = re.compile(r'(ownaddr=.*?ipaddr={})'.format(ip_5g_side))
    topology_regex = re.compile(r'ownaddr=(\w+:\w+:\w+:\w+:\w+:\w+).*?(ipaddr={})'.format(ip_5g_side))
    topology_text =   topology_regex.search(decoded_html)
    print('rg_mac:' + topology_text.group(1))
    rg_mac = topology_text.group(1)
    print('ip:' + topology_text.group(2))
    ip_5g = topology_text.group(2)
    if topology_text == None:
         print('topology file fails test')
         rf.write('     topology file strings:ownaddr=' + rg_mac + 'and 5g side IP:' + ip_5g + 'not found:Fail\n\n')
         test_status = "Fail"
    else:
        print(topology_text)
        rf.write('     topology file strings:ownaddr=' + rg_mac + 'and 5g side IP:' + ip_5g + ' found :Pass\n\n')
    return test_status

def url_att_route_smoke(nvg_599_dut, url_to_return, rf, rfa, test_name):
    test_status = "Pass"
    rf.write('Test ' + test_name + '\n')
    print('Test:' + test_name + '\n')
    # decoded_html = nvg_599_dut.urllib_get_rg_file("http://192.168.1.254/ATT/topology", rf, rfa)
    decoded_html = nvg_599_dut.urllib_get_rg_file(url_to_return, rf, rfa)
    rg_serial_number = nvg_599_dut.serial_number
    nvg_5g_mac = nvg_info[rg_serial_number]['mac5g']
    print('nvg_mac_5g: ' + str(nvg_5g_mac) + '\n')
    print('decoded: ' + str(decoded_html) + '>end_decoded \n')
    route_regex = re.compile(r'ownaddr=(\w+:\w+:\w+:\w+:\w+:\w+).*?(dest=\w+:\w+:\w+:\w+:\w+:\w+)')
    route_text = route_regex.search(decoded_html)
    print('rg_mac:' + route_text.group(1))
    rg_mac = route_text.group(1)
    print('ip:' + route_text.group(2))
    dest_mac = route_text.group(2)
    if route_text == None:
        print('route file fails test')
        rf.write('     route file strings:ownaddr=' + rg_mac + 'and dest mac::' + dest_mac + 'not found:Fail\n\n')
        test_status = "Fail"
    else:
        print(route_text)
        rf.write('     route file strings:ownaddr=' + rg_mac + 'and dest mac:' + dest_mac + ' found :Pass\n\n')
    return test_status

def url_att_friendly_info_smoke(nvg_599_dut, url_to_return, rf, rfa, test_name):
    test_status = "Pass"
    rf.write('Test ' + test_name + '\n')
    print('Test:' + test_name + '\n')
    # decoded_html = nvg_599_dut.urllib_get_rg_file("http://192.168.1.254/ATT/topology", rf, rfa)
    decoded_html = nvg_599_dut.urllib_get_rg_file(url_to_return, rf, rfa)
    rg_serial_number = nvg_599_dut.serial_number
    nvg_5g_mac = nvg_info[rg_serial_number]['mac5g']
    print('nvg_mac_5g: ' + str(nvg_5g_mac) + '\n')
    print('decoded: ' + str(decoded_html) + '>end_decoded \n')
    friendly_regex = re.compile(r'ownaddr=(\w+:\w+:\w+:\w+:\w+:\w+).*?(friendlyname=\w+)')
    friendly_text = friendly_regex.search(decoded_html)

    print('rg_mac:' + friendly_text.group(1))

    rg_mac = friendly_text.group(1)
    print('ip:' + friendly_text.group(2))
    friendlyname = friendly_text.group(2)
    if friendly_text == None:
        print('friendly-info file fails test')
        rf.write('     friendly-info file strings:ownaddr=' + rg_mac + 'and friendly name::' + friendlyname + 'not found:Fail\n\n')
        test_status = "Fail"
    else:
        print(friendly_text)
        rf.write('     friendly-info file strings:ownaddr=' + rg_mac + 'and friendly name:' + friendlyname + ' found :Pass\n\n')
    return test_status

def url_att_cca5g_smoke(nvg_599_dut, url_to_return, rf, rfa, test_name):
    test_status = "Pass"
    rf.write('Test ' + test_name + '\n')
    print('Test:' + test_name + '\n')
    # decoded_html = nvg_599_dut.urllib_get_rg_file("http://192.168.1.254/ATT/topology", rf, rfa)
    # nvg_599_dut = WebDriverWait(nvg_599_dut, 10)
    decoded_html = nvg_599_dut.urllib_get_rg_file(url_to_return, rf, rfa)
    decoded_html = re.escape(decoded_html)
    rg_serial_number = nvg_599_dut.serial_number
    nvg_5g_mac = nvg_info[rg_serial_number]['mac5g']
    print('nvg_mac_5g: ' + str(nvg_5g_mac) + '\n')
    print('decoded: ' + str(decoded_html) + '>end_decoded \n')
    cca5g_regex = re.compile(r'label.*?(data)')
    cca5g_text = cca5g_regex.search(decoded_html)
    #print('rg_mac:' + cca5g_text.group(1))
    # cca5g = cca5g_text.group(1)
    #print('ip:' + cca5g_text.group(2))
    #friendlyname = friendly_text.group(2)
    if cca5g_text == None:
        print('cca5g file strings: "label" and "data" :not found:Fail')
        rf.write('     cca5g file strings: "label" and "data" :not found:Fail\n\n')
        test_status = "Fail"
    else:
        print('cca5g text:' + cca5g_text.group(1))
        cca5g = cca5g_text.group(1)
        print('cca5g file strings: "label" and "data" : found:Pass')
        rf.write('     cca5g file strings:' + cca5g + ':found:Pass\n\n')
    return test_status

def url_att_steer_smoke(nvg_599_dut, url_to_return, rf, rfa, test_name):
    test_status = "Pass"
    rf.write('Test ' + test_name + '\n')
    print('Test:' + test_name + '\n')
    # decoded_html = nvg_599_dut.urllib_get_rg_file("http://192.168.1.254/ATT/topology", rf, rfa)
    # nvg_599_dut = WebDriverWait(nvg_599_dut, 10)
    decoded_html = nvg_599_dut.urllib_get_rg_file(url_to_return, rf, rfa)
    #decoded_html = re.escape(decoded_html)
    rg_serial_number = nvg_599_dut.serial_number
    nvg_5g_mac = nvg_info[rg_serial_number]['mac5g']
    print('steer: ' + str(nvg_5g_mac) + '\n')
    print('decoded: ' + str(decoded_html) + '>end_decoded \n')
    steer_regex = re.compile(r'ownaddr=(\w+:\w+:\w+:\w+:\w+:\w+).*?(steering)')
    steer_text = steer_regex.search(decoded_html)
    # print('rg_mac:' + cca5g_text.group(1))
    # cca5g = cca5g_text.group(1)
    # print('ip:' + cca5g_text.group(2))
    # friendlyname = friendly_text.group(2)
    if steer_text == None:
        print('steer file  :not found:Fail')
        rf.write('     steer file strings :not found:Fail\n\n')
        test_status = "Fail"
    else:
        print('steer:' + steer_text.group(1))
        print('steer file strings:' + steer_text.group(1) + ' ' + steer_text.group(2) + 'found:Pass')
        rf.write('     steer file strings:' + steer_text.group(1) + ' ' + steer_text.group(2) +':found:Pass\n\n')
    return test_status

def band5_peers_cleared_after_reset(nvg_599_dut, rf, rfa, test_name):
    test_status = "Pass"
    rf.write('Test ' + test_name + '\n')
    print('Test:' + test_name + '\n')
    # decoded_html = nvg_599_dut.urllib_get_rg_file("http://192.168.1.254/ATT/topology", rf, rfa)
    # nvg_599_dut = WebDriverWait(nvg_599_dut, 10)
    # band5_cli_session  = nvg_599_dut.login_nvg_599_5g_cli()
    peer_list = nvg_599_dut.get_rg_airties_band5_wds_links(rf, rfa)
    if len(peer_list) == 0:
        print('peer list empty  :found :Pass')
        rf.write('     peer list empty  ::Pass\n\n')
    else:
        print('peer list not empty  :found ' + str(peer_list) + ':Fail')
        rf.write('     peer list not empty  :found ' + str(peer_list) + ':Fail\n\n')
        test_status = "Fail"
    print(str(peer_list))

    return test_status

def band5_peers_set_after_airties_association(nvg_599_dut, rf, rfa, test_name):
    test_status = "Pass"
    rf.write('Test ' + test_name + '\n')
    print('Test:' + test_name + '\n')
    # decoded_html = nvg_599_dut.urllib_get_rg_file("http://192.168.1.254/ATT/topology", rf, rfa)
    # nvg_599_dut = WebDriverWait(nvg_599_dut, 10)
    # band5_cli_session  = nvg_599_dut.login_nvg_599_5g_cli()
    peer_list = nvg_599_dut.get_rg_airties_band5_wds_links(rf, rfa)
    if len(peer_list) == 0:
        print('peer list empty  :found :Fail')
        rf.write('     peer list empty, expected wds mac(s)  ::Fail\n\n')
        test_status = "Fail"
    else:
        print('peer list not empty  :found ' + str(peer_list) + ':Pass')
        rf.write('     peer list not empty  :found ' + str(peer_list) + ':Pass\n\n')
    print(str(peer_list))

    return test_status

# this test should be reset airties to factory default and then rejoin RG SSID via WPS
# use one of the available 4920s (ATT_4290_866D4 or ATT_4920_C356C0
def airties_wps_connection_after_airties_factory_reset(nvg_599_dut, airties_ssid, rf, rfa, test_name):
    test_status = "Pass"
    rf.write('Test ' + test_name + '\n')
    print('Test:' + test_name + '\n')
    # check that airties device is in RG SSID by ping
    # login to the cli and execute sh ip lan to look for the airties devie name and get it's IP

    nvg_599_dut.wps_pair_default_airties(airties_ssid)

    # we want to pass in a remote file source  in case we are getting  files from somewhere else-- do I need a put?
    # def tftp_get_file_cli(self, remote_file_source, *source_device_list):
    # def tftp_get_file_cli(self, remote_file_source, firmware_to_get):

# rg_firmware nvg599-11.5.0h0d1_1.1.bin"
def tftp_rg_firmware_and_install(nvg_599_dut, tftp_server_name, rg_firmware, rf, rfa, test_name):
    test_status = "Pass"
    rf.write('Test ' + test_name + '\n')
    # If we cant get the file there is no point in continuing
    test_status = nvg_599_dut.install_rg_cli(tftp_server_name, rg_firmware, rf, rfa)
    if test_status == "Pass":
        rf.write('    Successfully loaded:' + str(rg_firmware) + ' :Pass\n')
    else:
        print('Firmware load  failed')
        rf.write('     Firmware load:' + str(rg_firmware) + ' :Failed\n\n')
        return test_status
        # test_status = "Fail"
    # make sure we can access the UI
    test_status = nvg_599_dut.check_for_system_info_page()
    if test_status == "Pass":
        print('UI check  found Pass')

        rf.write('     UI check OK)     :Pass\n\n')
    else:
        print('UI check not found  failed')
        rf.write('    UI check not found)     :Fail\n\n')
        # return test_status
    return test_status

def conf_auto_setup_ssid_via_tr69_cli(nvg_599_dut, ssid_number, max_clients, rf, rfa, test_name):
    rf.write('Test ' + test_name + '\n')
    test_status = nvg_599_dut.set_auto_setup_ssid_via_tr69_cli(ssid_number, max_clients, rf, rfa)
    if test_status == "Pass":
        rf.write('     Auto SSID:'  + str(ssid_number) + 'Successfully configured :Pass\n\n')
    else:
        print('auto ssid conf fail ')
        rf.write('     Auto SSID:'  + str(ssid_number) + 'Failed configured :Fail\n\n')
    return test_status

def local_to_remote_ping(nvg_599_dut, rf, rfa, remote_ip, test_name, number_of_pings=20):
    #  = remote_ip
    rf.write('Test ' + str(test_name) + '\n')
    test_status = "Passed"
    min_ping, avg_ping, max_ping, mdev_ping, sent, received, loss = nvg_599_dut.ping_from_local_host(remote_ip, number_of_pings=20)
    if received == "0":
        rf.write('     Local to remote ping failed)     :Fail\n')
        rf.write('     min:' + min_ping + '  avg:' + avg_ping + '  max:' + max_ping + '  mdev:' + mdev_ping  + '\n')
        rf.write('     sent:' + sent + '  received:' + received + '  loss:' + loss +  '\n\n')
        print('     sent:' + str(sent) + 'received:' + str(received) + 'loss:' + str(loss) +  '\n')
        test_status = "Fail"
    else:
        rf.write('     Local to remote ping pass     :Pass\n')
        rf.write('     min:' + min_ping + ' avg:' + avg_ping + ' max:' + max_ping + ' mdev:' + mdev_ping  + '\n')
        rf.write('     sent:' + sent + ' received:' + received + ' loss:' + loss +  '\n\n')
        print('     sent:' + str(sent) + ' received:' + str(received) + ' loss:' + str(loss) +  '\n')
    return test_status
    # test_status = nvg_599_dut.set_auto_setup_ssid_via_tr69_cli(ssid_number, max_clients, rf, rfa)
    # return min_ping, avg_ping, max_ping, mdev_ping, sent, received, loss
        # test_status = "Fail"
    # make sure we can access the UI
    #test_status = nvg_599_dut.check_for_system_info_page()
# ssid = 3
# nvg_599_dut.set_auto_setup_ssid_via_tr69_cli(ssid)
# results_file.write("Test Title: Auto SSID 3 setup: Pass")
# results_file_archive.write("Test Title: Auto SSID 3 setup: Pass")
#
# ssid = 4
# nvg_599_dut.set_auto_setup_ssid_via_tr69_cli(ssid)
# results_file.write("Test Title: Auto SSID 4 setup: Pass")
# results_file_archive.write("Test Title: Auto SSID 4 setup: Pass")
# results_file.close()
# results_file_archive.close()
# nvg_599_dut.email_test_results(results_file)
# sleep(30)
# def ui_set_wifi_password(self, security, password):

#def cli_sh_rg_ip_lan_info(self):
#ip_lan_connections_dict_cli
# Galaxy-S9

def xxremote_android_speed_test(nvg_599_dut, rf, rfa, remote_device, test_name):
    #  = remote_ip
    rf.write('Test ' + str(test_name) + '\n')
    # get the ip of the device
    speed_test_ip = "192.168.1.77"
    nvg_599_dut.execute_speedtest_from_android_termux(speed_test_ip, rf, rfa)
    print('execute_speedtest_from_android_termux')
    # rfa = "future"
    # excel_cell = rfa
    # prompt = '\$\s+'
    test_status = "Passed"

def install_airties_firmware(nvg_599_dut, rf, rfa, test_name, airties_firmware, remote_device_name = "Any"):
    #  = remote_ip
    rf.write('Test ' + str(test_name) + '\n')
    # remote device name is any then get the first available airties
    # else use the one provided, if not on the loal lan then error.
    # get the ip of the device from the name
    print('execute_speedtest_from_android_termux')

    test_status = "Passed"



with open('results_file.txt', mode = 'w', encoding = 'utf-8') as rf, \
    open('resultsa_file.txt', mode='w', encoding='utf-8') as rfa :
    now = datetime.today().strftime("%B %d, %Y,%H:%M")

    send_email = 1
    nvg_599_dut = Nvg599Class()

    nvg_599_dut.enable_monitor_mode()
    # exit()
    nvg_599_dut.nmcli_set_connection('Wired', 'up')



    # test_speedtest_from_android(nvg_599_dut, 'Galaxy-Note8', test_house_devices_static_info, 'test_speedtest_from_android ', rf, rfa)
    # def execute_speedtest_from_android_termux(speed_test_ip, rf, rfa):
    # nvg_599_dut.execute_speedtest_from_android_termux("192.168.1.77",rf, rfa)
    rf.write('RG Test run Firmware:' +  nvg_599_dut.software_version + '  Date:' + now + ' ' '\n\n')
    rfa.write(now + '\n')
    sleep(2)


    connection_list, active_connection_list  = nvg_599_dut.nmcli_get_connections()
    print('connect:' + str(connection_list) + '\n')
    print('active:' + str(active_connection_list) + '\n')

    #nvg_599_dut.nmcli_set_connection(nmcli_connection_name, command):

    for  connection in active_connection_list:
        nvg_599_dut.nmcli_set_connection(connection, 'down')

    # nvg_599_dut.nmcli_set_connection('Wired', 'down')
    # nvg_599_dut.nmcli_set_connection('ATT4ujR48s', 'down')
    print('turn down the active connections' + '\n')
    print('ping expected to fail' + '\n')
    nvg_599_dut.ping_check('192.168.1.254')

    # turn on wifi only
    # print('turn up the wifi connections only ' + '\n')
    default_wifi_active = 0
    for  connection in active_connection_list:
        if connection == 'Wired':
            continue
        else:
            default_wifi_active = connection
            nvg_599_dut.nmcli_set_connection(connection, 'up')
            print('turned up the wifi connections only ' + str(connection) + '\n')

    # nvg_599_dut.nmcli_set_connection('ATT4ujR48s', 'up')
    print('ping1 expected to pass' + '\n')
    nvg_599_dut.ping_check('192.168.1.254')

    print('turned down the wifi default ' + str(default_wifi_active) + '\n')
    nvg_599_dut.nmcli_set_connection(default_wifi_active, 'down')

    print('turned up  the wifi ATT4ujR48s_Guest \n')
    nvg_599_dut.nmcli_set_connection('ATT4ujR48s_Guest', 'up')
    print('ping expected to fail should not be able to ping RG from guest network' + '\n')

    nvg_599_dut.ping_check('192.168.1.254')
    print('turned down  the wifi ATT4ujR48s_Guest \n')
    nvg_599_dut.nmcli_set_connection('ATT4ujR48s_Guest', 'down')

    print('restoring active connections \n')
    for connection in active_connection_list:
        nvg_599_dut.nmcli_set_connection(connection, 'up')

    #nvg_599_dut.nmcli_set_connection('ATT4ujR48s', 'up')
    print('ping   should  be able to ping RG from main network' + '\n')
    nvg_599_dut.ping_check('192.168.1.254')

    exit()


    tftp_rg_firmware_and_install(nvg_599_dut, "LP-PPALMER", "nvg599-11.5.0h0d8_1.1.bin", rf, rfa, "tftp_rg_firmware_and_install")
    # exit()
    # this works
    # nvg_599_dut.tftp_get_file_cli('LP-PPALMER', 'AirTies_7381.bin', rf, rfa)
    #nvg_599_dut.install_airties_firmware('192.168.1.68', '/home/palmer/Downloads/AirTies_Air4920US-AL_FW_2.49.2.18.7197_FullImage.bin', rf, rfa)
    # nvg_599_dut.install_airties_firmware('192.168.1.68', '/home/palmer/Downloads/AirTies_7381.bin', rf, rfa)
    # nvg_599_dut.install_airties_firmware('192.168.1.68', '/home/palmer/Downloads/airties_telnet_preinstall.bin', rf, rfa)
    # exit()
    # install_airties_firmware(rf, rfa, "install_airties_firmware", '/home/palmer/Downloads/airties_telnet_preinstall.bin', "ATT_4920_8664D4")
    url_att_friendly_info_smoke(nvg_599_dut, 'http://192.168.1.254/ATT/friendly-info', rf, rfa, 'url_att_friendly_info_smoke')

    ping_gw_from_4920(nvg_599_dut, rf, rfa, "ping_gw_from_4920")
    ping_airties_from_rg(nvg_599_dut, rf, rfa, "ping_airties_from_RG")
    verify_airties_hello_packet_count_increasing(nvg_599_dut, rf, rfa, "verify_airties_hello_packet_count_increasing")
    verify_airties_build_versions(nvg_599_dut, rf, rfa, 'verify_airties_build_versions')
    url_att_topology_smoke(nvg_599_dut, 'http://192.168.1.254/ATT/topology', rf, rfa, 'url_att_topology_smoke')
    url_att_route_smoke(nvg_599_dut, 'http://192.168.1.254/ATT/route', rf, rfa, 'url_att_route_smoke')
    url_att_friendly_info_smoke(nvg_599_dut, 'http://192.168.1.254/ATT/friendly-info', rf, rfa,
                                'url_att_friendly_info_smoke')
    band5_peers_set_after_airties_association(nvg_599_dut, rf, rfa, "band5_peers_set_after_airties_associationn")
    # nvg_599_dut.tftp_get_file_cli(source_device_name, "nvg599-9.2.2h13d24_1.1.bin","nvg599-9.2.2h13d22_1.1.bin","nvg599-9.2.2h13d20_1.1.bin","nvg599-9.2.2h13d18_1.1.bin","nvg599-9.2.2h13d16_1.1.bin","nvg599-9.2.2h13d14_1.1.bin","nvg599-9.2.2h13d12_1.1.bin","nvg599-9.2.2h13d10_1.1.bin")
    url_att_steer_smoke(nvg_599_dut, 'http://192.168.1.254/ATT/steer', rf, rfa, 'url_att_steer_smoke')

    # def test_speedtest_from_android(nvg_599_dut, device_name, test_house_devices_static_info, test_name, rf, rfa):

    test_speedtest_from_android(nvg_599_dut, 'Galaxy-Note8', test_house_devices_static_info, 'test_speedtest_from_android ', rf, rfa)

    # tftp_rg_firmware_and_install(nvg_599_dut, "LP-PPALMER", "nvg599-11.5.0h0d4_1.1.bin", rf, rfa,
    #                            "tftp_rg_firmware_and_install")
    verify_auto_ssid_defaults_via_tr69(nvg_599_dut, '3', 'ZipKey-PSK', 'Cirrent1',  rf, rfa, "verify_auto_ssid_defaults_via_tr69" )
    verify_auto_ssid_defaults_via_tr69(nvg_599_dut, '4', 'ATTPOC', 'Ba1tshop', rf, rfa, "verify_auto_ssid_defaults_via_tr69" )
    verify_auto_info_not_present_in_ui(nvg_599_dut, rf, rfa, "verify_auto_info_not_present_in_ui" )
    verify_google_ping_from_rg_5g(nvg_599_dut, rf, rfa, "verify_google_ping_from_rg_5g")
    url_att_topology_smoke(nvg_599_dut, 'http://192.168.1.254/ATT/topology', rf, rfa, 'url_att_topology_smoke')
    url_att_route_smoke(nvg_599_dut, 'http://192.168.1.254/ATT/route', rf, rfa, 'url_att_route_smoke')
    # # execute_factory_reset(nvg_599_dut, rf, rfa, 'execute_factory_reset')
    local_to_remote_ping(nvg_599_dut,rf, rfa,  '192.168.1.69',  "local_to_remote_ping")
    test_dfs(nvg_599_dut, rf, rfa, "test_dfs")
if send_email == 1:
    nvg_599_dut.email_test_results(rf, nvg_599_dut.software_version)

    # we want to get the SSID becaause we have to reconnect to it
    # wl_status_info_dict = nvg_599_dut.get_rg_band2_status_cli()
    # rg_ssid = wl_status_info_dict['ssid']
    # print('rg ssid is:'+ str(rg_ssid))

    # then we want to get the specific IP of the named airties device
    # so we would get the dict which is keyed on macs then when we find the name = to the named device we
    # can get the  state and the current ip. If the state is off then the device may be powered off or it is
    #has been factory reset.
    # at that point we have to check the available wireless networks to see if the Airties is in AP mode by
    # looking for its default network.
    # if we find it then we connect to the network as a "sta" enter the basbaglan command,
    # change back to the Rg network and call the click wps method.


# nvg_599_dut.static_reset_4920('192.168.1.70')
#
#     tftp_rg_firmware_and_install(nvg_599_dut, "LP-PPALMER", "nvg599-11.5.0h0d3_1.1.bin", rf, rfa, "tftp_rg_firmware_and_install")
#     execute_factory_reset(nvg_599_dut, rf, rfa, "execute_factory_reset")
#     verify_auto_ssid_defaults_via_tr69(nvg_599_dut, '3', 'ZipKey-PSK', 'Cirrent1',  rf, rfa, "verify_auto_ssid_defaults_via_tr69" )
#     verify_auto_ssid_defaults_via_tr69(nvg_599_dut, '4', 'ATTPOC', 'Ba1tshop', rf, rfa, "verify_auto_ssid_defaults_via_tr69" )
#     verify_auto_info_not_present_in_ui(nvg_599_dut, rf, rfa, "verify_auto_info_not_present_in_ui" )
#     verify_google_ping_from_rg_5g(nvg_599_dut, rf, rfa, "verify_google_ping_from_rg_5g")
#     url_att_topology_smoke(nvg_599_dut, 'http://192.168.1.254/ATT/topology', rf, rfa, 'url_att_topology_smoke')
#     url_att_route_smoke(nvg_599_dut, 'http://192.168.1.254/ATT/route', rf, rfa, 'url_att_route_smoke')
#
#     #
#     # url_att_friendly_info_smoke(nvg_599_dut, 'http://192.168.1.254/ATT/friendly-info', rf, rfa,
#     #                         'url_att_friendly_info_smoke')
#     conf_auto_setup_ssid_via_tr69_cli(nvg_599_dut, '3', '3', rf, rfa, 'conf_auto_setup_ssid_via_tr69_cli')
#     conf_auto_setup_ssid_via_tr69_cli(nvg_599_dut, '4', '4', rf, rfa, 'conf_auto_setup_ssid_via_tr69_cli')

exit()

from openpyxl.styles import Color,PatternFill, Font, Border
wb = Workbook()
ws = wb.active
ws1 = wb.create_sheet("Mysheet") # insert at the end (default)
# ws2 = wb.create_sheet("Mysheet", 0) # insert at first position
ws.title = "nvg599 11.5 d1"
ws['A7'] = "Commments"
ws['B7'] = "New"
ws['C7'] = "Test ID "
ws['D7'] = "Test Title"
ws['E7'] = "Purpose/Objective"
ws['F7'] = "Steps"
ws['G7'] = "Results"

ws['A8'] = "Book 1 in Docx File"
ws['A9'] = ""
ws['C10'] = ""



for cell in ws["7:7"]:
    # cell.fill = PatternFill(bgColor = "FEF5A8", fill_type = "solid")
    cell.fill = PatternFill(start_color = "FEF5A8", end_color = "FEF5A8", fill_type = "solid")

    #cell.font = red_font
wb.save('myworkbook.xlsx')
exit()
# wb.save(filename=file)
# >>> source = wb.active
# >>> target = wb.copy_worksheet(source)
# create copies of  a worksheet


#tree = ET.parse('/home/palmer/tmp/config00.xml')
#import xml.etree.ElementTree as ETree
from  xml.etree.ElementTree import  fromstring, ElementTree

#send_email = 1
rf = open('results_file.txt', mode = 'w', encoding = 'utf-8')
rfa  = open('results_file.txt', mode = 'a', encoding = 'utf-8')
#now = datetime.today().strftime("%B %d, %Y,%H:%M")
# rf.write('RG Test run:' + now + '\n')
# rfa.write(now + '\n')
send_email = 1
nvg_599_dut = Nvg599Class()

nvg_599_dut.tftp_rg_firmware_and_install("LP-PPALMER", "nvg599-11.5.0h0d2_1.1.bin", rf, rfa)
exit()
execute_factory_reset(nvg_599_dut, rf, rfa, 'execute_factory_reset')
if send_email == 1:
    nvg_599_dut.email_test_results(rf)
rf.close()
rfa.close()
exit()



#def tftp_get_file_cli(self,remote_file, *source_device_list):
# AirTies_7084.bin
#remote_file = "nvg589-2.2h13d24.bin"
# note that when we re-install the telnet bin, the ip is assumed to be 192.168.2.254  which is what it would be after a factory reset.
# also we assume that we are connected to the AP's default SSID


# remote_file = rg_firmware nvg599-11.5.0h0d1_1.bin"
remote_file = "nvg599-2.2h13d26.bin"
tftp_rg_firmware_and_install(nvg_599_dut, "LP-PPALMER",remote_file, rf,rfa ,"tftp_rg_firmware_and_install")

remote_file = "nvg599-2.2h13d25.bin"
tftp_rg_firmware_and_install(nvg_599_dut, "LP-PPALMER",remote_file, rf,rfa ,"tftp_rg_firmware_and_install")

remote_file = "nvg599-2.2h13d26.bin"
tftp_rg_firmware_and_install(nvg_599_dut, "LP-PPALMER",remote_file, rf,rfa ,"tftp_rg_firmware_and_install")

#tftp_rg_firmware_and_install(nvg_599_dut, "LP-PPALMER","nvg599-11.5.0h0d1_1.1.bin", rf,rfa ,"tftp_rg_firmware_and_install")
#                                                      nvg599-11.5.0h0d1_1.1.bin
#airties_wps_connection_after_airties_factory_reset(nvg_599_dut,"dog", rf, rfa, "airties_wps_connection_after_airties_factory_reset")

exit()


# this looks to be installing into an airties in AP mode
# do I need this, when installing neww firmware or only on factory reset?
nvg_599_dut.install_4920_firmware('192.168.2.254', '/home/palmer/Downloads/airties_telnet_preinstall.bin', rf, rfa)



rf.close()
rfa.close()
exit()
source_device_name = "LP-PPALMER"
remote_file = "airties_telnet_preinstall.bin"
nvg_599_dut.tftp_get_file_cli(source_device_name, "airties_telnet_preinstall.bin")
band5_peers_cleared_after_reset(nvg_599_dut, rf, rfa,"band5_peers_cleared_after_reset")
band5_peers_set_after_airties_association(nvg_599_dut, rf, rfa, "band5_peers_set_after_airties_associationn")
# nvg_599_dut.tftp_get_file_cli(source_device_name, "nvg599-9.2.2h13d24_1.1.bin","nvg599-9.2.2h13d22_1.1.bin","nvg599-9.2.2h13d20_1.1.bin","nvg599-9.2.2h13d18_1.1.bin","nvg599-9.2.2h13d16_1.1.bin","nvg599-9.2.2h13d14_1.1.bin","nvg599-9.2.2h13d12_1.1.bin","nvg599-9.2.2h13d10_1.1.bin")
url_att_steer_smoke(nvg_599_dut,'http://192.168.1.254/ATT/steer',rf,rfa, 'url_att_steer_smoke')
rf.close()
rfa.close()
if send_email == 1:
    nvg_599_dut.email_test_results(rf)
exit()

#execute_factory_reset(nvg_599_dut, rf, rfa, 'execute_factory_reset')
#verify_auto_ssid_defaults_via_tr69(nvg_599_dut, '3', 'ZipKey-PSK', 'Cirrent1',  rf, rfa, "verify_auto_ssid_defaults_via_tr69" )
#verify_auto_ssid_defaults_via_tr69(nvg_599_dut, '4', 'ATTPOC', 'Ba1tshop', rf, rfa, "verify_auto_ssid_defaults_via_tr69" )
#verify_auto_info_not_present_in_ui(nvg_599_dut, rf, rfa, "verify_auto_info_not_present_in_ui" )
verify_google_ping_from_rg_5g(nvg_599_dut, rf, rfa, "verify_google_ping_from_rg_5g")

url_att_topology_smoke(nvg_599_dut,'http://192.168.1.254/ATT/topology',rf, rfa, 'url_att_topology_smoke')
url_att_route_smoke(nvg_599_dut,'http://192.168.1.254/ATT/route',rf,rfa, 'url_att_route_smoke')
url_att_friendly_info_smoke(nvg_599_dut,'http://192.168.1.254/ATT/friendly-info',rf,rfa, 'url_att_friendly_info_smoke')
#url_att_cca5g_smoke(nvg_599_dut,'http://192.168.1.254/ATT/cca5g',rf,rfa, 'url_att_cca5g_smoke')
url_att_steer_smoke(nvg_599_dut,'http://192.168.1.254/ATT/steer',rf,rfa, 'url_att_steer_smoke')
rf.close()
rfa.close()
if send_email == 1:
    nvg_599_dut.email_test_results(rf)
exit()

run_file = open('results_file.txt', mode = 'w', encoding = 'utf-8')
run_file_db  = open('test.txt', mode = 'w', encoding = 'utf-8')
now = datetime.today().strftime("%B %d, %Y,%H:%M")
run_file.write('RG Test run:' + now + '\n')
nvg_599_dut = Nvg599Class()

# peers_xml = band5_att_peers_smoke(nvg_599_dut,'present', run_file, run_file_db, 'band5_att_peers_smoke')

print('outside of func' + str(peers_xml))
exit()

# tree = ElementTree(fromstring(peers_xml))
# #tree = ETree.fromstring(peers_xml)
# print(str(tree))
# print('1--------------------\n')
# #print(ETree.tostring(tree.getroot()))
# root = tree.getroot()
# print('2---:' +  root.tag + '\n')
# peer_list = []
# for peer in root.iter('peer'):
#     print(str(peer.attrib['address']))
#     peer_list.append(peer.attrib['address'])
# print(peer_list)
# run_file.close()
# run_file_db.close()
# exit()

# parser = ETree.XMLParser(encoding="utf-8")
# tree = ETree.parse("/home/palmer/tmp/config00.xml")
#   root = ET.fromstring(country_data_as_string)
# this routine could use a max lients option
# setup_auto_ssid_via_tr69(nvg_599_dut, '3', '4', rf, rfa, "setup_auto_ssid_via_tr69")
# setup_auto_ssid_via_tr69(nvg_599_dut, '4', rf, rfa, "setup_auto_ssid_via_tr69")
# print(ETree.tostring(tree.getroot()))
# mytreeroot = tree.getroot()
# mytree = ETree.tostring(tree)
# print('1--------------------\n')
# print(ETree.tostring(tree.getroot()))
# root = tree.getroot()
# print('2---:' +  root.tag + '\n')
# peer_list = []
# for peer in root.iter('peer'):
#     print(str(peer.attrib['address']))
#     peer_list.append(peer.attrib['address'])
# print(peer_list)
# exit()



band_5_wl_status_dict = nvg_599_dut.get_rg_band5_status_cli()
print('---------------band_5_wl_status_dict:' + str(band_5_wl_status_dict['bssid']))
print('---------------band_5_wl_st channel:' + str(band_5_wl_status_dict['channel']))
print('---------------band_5_wl_stat--bw:' + str(band_5_wl_status_dict['bandwidth']))


exit()
# set the file at to the file to use
# source_device_name = "LP-PPALMER"
# nvg_599_dut.tftp_get_file_cli(source_device_name, "nvg599-9.2.2h13d26_1.1.bin","nvg589-9.2.2h13d26_1.1.bin")
#
# test_rg_upgrade(nvg_599_dut, '/home/palmer/Downloads/nvg599-9.2.2h13d26_1.1.bin', rf, rfa)
execute_factory_reset(nvg_599_dut, rf, rfa, 'execute_factory_reset')
verify_auto_ssid_defaults_via_tr69(nvg_599_dut, '3', 'ZipKey-PSK', 'Cirrent1',  rf, rfa, "verify_auto_ssid_defaults_via_tr69" )
verify_auto_ssid_defaults_via_tr69(nvg_599_dut, '4', 'ATTPOC', 'Ba1tshop', rf, rfa, "verify_auto_ssid_defaults_via_tr69" )
verify_auto_info_not_present_in_ui(nvg_599_dut, rf, rfa, "verify_auto_info_not_present_in_ui" )
verify_google_ping_from_rg_5g(nvg_599_dut, rf, rfa, "verify_google_ping_from_rg_5g")

# need to make sure 4920s are associated first
ping_gw_from_4920(nvg_599_dut,rf,rfa, "ping_gw_from_4920")
ping_airties_from_rg(nvg_599_dut, rf, rfa, "ping_airties_from_RG")
verify_airties_hello_packet_count_increasing(nvg_599_dut, rf, rfa, "verify_airties_hello_packet_count_increasing")
verify_airties_build_versions(nvg_599_dut, rf, rfa, 'verify_airties_build_versions')

#airties_ap_net = "AirTies_SmartMesh_4PNF"
#nvg_599_dut.wps_pair_default_airties(airties_ap_net)

rf.close()
rfa.close()
if send_email == 1:
    nvg_599_dut.email_test_results(rf)
exit()


#def tftp_get_file_cli(self,remote_file, *source_device_list):

#remote_file = "nvg589-2.2h13d24.bin"
#source_device_name = "LP-PPALMER"
#remote_file = "a1.txt"
#nvg_599_dut.tftp_get_file_cli(source_device_name, "nvg599-9.2.2h13d24_1.1.bin","nvg599-9.2.2h13d22_1.1.bin","nvg599-9.2.2h13d20_1.1.bin","nvg599-9.2.2h13d18_1.1.bin","nvg599-9.2.2h13d16_1.1.bin","nvg599-9.2.2h13d14_1.1.bin","nvg599-9.2.2h13d12_1.1.bin","nvg599-9.2.2h13d10_1.1.bin")

# we first get the IP of an associated 4920.
# if none availabe then exit with fail message
# # self.ip_lan_connections_dict_cli[connected_device_mac] = {}
# ip_lan_connections_dict_cli[connected_device_mac] = {}
# ip_lan_connections_dict_cli[connected_device_mac]["IP"] = connected_device_ip
# ip_lan_connections_dict_cli[connected_device_mac]["Name"] = connected_device_name
# ip_lan_connections_dict_cli[connected_device_mac]["State"] = connected_device_status
# ip_lan_connections_dict_cli[connected_device_mac]["DHCP"] = connected_device_dhcp
# ip_lan_connections_dict_cli[connected_device_mac]["Port"] = connected_device_port
# verify_auto_ssid_defaults_via_tr69(nvg_599_dut, '3', rf, rfa, "verify_auto_ssid_defaults_via_tr69" )
# print(' verify_auto_ssid_defaults_via_tr69 ssid:'  + status)
######################################################### end test area, clean up the junk below
# set the file at to the file to use
# test_rg_upgrade(nvg_599_dut, '/home/palmer/Downloads/nvg599-9.2.2h13d25_1.1.bin', rf, rfa)

verify_auto_ssid_defaults_via_tr69(nvg_599_dut, '4', rf, rfa, "verify_auto_ssid_defaults_via_tr69")
#print('verify_auto_ssid_defaults_via_tr69 ssid:' + status)

setup_auto_ssid_via_tr69(nvg_599_dut, '3', rf, rfa, "setup_auto_ssid_via_tr69")

setup_auto_ssid_via_tr69(nvg_599_dut, '4', rf, rfa, "setup_auto_ssid_via_tr69")

verify_auto_info_not_present_in_ui(nvg_599_dut, rf, rfa, "verify_auto_info_not_present_in_ui")
#status = nvg_599_dut.set_auto_setup_ssid_via_tr69_cli(nvg_599_dut, "3", rf, rfa, 'nvg_599_dut.set_auto_setup_ssid_via_tr69_cli')
# status = nvg_599_dut.set_auto_setup_ssid_via_tr69_cli("4", rf, rfa)

#status = nvg_599_dut.set_auto_setup_ssid_via_tr69_cli(nvg_599_dut, "4", rf, rfa, 'nvg_599_dut.set_auto_setup_ssid_via_tr69_cli')



rf.close()
rfa.close()
exit()

# upgrade_rg_file ='/home/palmer/Downloads/nvg599-9.2.2h13d23_1.1.bin'
# These android devices should be able to run the cli speed test
# Galaxy-Note8,Galaxy-S9,Galaxy-Tab-A
#test_rg_upgrade(nvg_599_dut, '/home/palmer/Downloads/nvg599-9.2.2h13d25_1.1.bin', rf, rfa)
# test_factory_reset(nvg_599_dut, rf, rfa)
# test_setup_auto_ssid_via_tr69(nvg_599_dut,ssid,rf,rfa)
# nvg_599_dut.set_auto_setup_ssid_via_tr69_cli(3, rf, rfa)
# rf.write("Test Title: Auto SSID 3 setup: Pass")
# rfa.write("Test Title: Auto SSID 3 setup: Pass")
#ssid = 4
test_speedtest_from_android(nvg_599_dut, 'Galaxy-Note8', test_house_devices_static_info, rf, rfa)
rf.close()
rfa.close()
if send_email == 1:
    nvg_599_dut.email_test_results(rf)

exit()


######################################################################################################
######################  Experimental code  below #####################
nmcli_connection = "Wired"
nvg_599_dut.nmcli_set_connection(nmcli_connection, "down")
sleep(5)
nvg_599_dut.nmcli_set_connection(nmcli_connection, "up")


now = datetime.today().strftime("%B %d, %Y,%H:%M")
rf = open('results_file.txt', mode = 'w', encoding = 'utf-8')
rfa  = open('results_file.txt', mode = 'a', encoding = 'utf-8')
rf.write(now + '\n')
rfa.write(now + '\n')
rf.write('Test title:test_auto_ssid_3_default_tr69_values \n')
test_status = test_auto_ssid_default_tr69_values(nvg_599_dut,"3",rf,rfa)
rf.write('    ' + test_status + '\n')
print('    Test Status:' + test_status + '\n')
rf.write('\n')
print('\n')

rf.write('Test title:test_auto_ssid_4_default_tr69_values \n')
test_status = test_auto_ssid_default_tr69_values(nvg_599_dut,"4",rf,rfa)
rf.write('    ' + test_status + '\n')
print('    Test Status:' + test_status + '\n')
rf.write('\n')
print('\n')

rf.write('Test title:test_verify_auto_ssid_info_not_present_in_ui \n')
test_status = verify_auto_info_not_present_in_ui(nvg_599_dut,rf,rfa)
rf.write(test_status + '\n')

rf.close()
rfa.close()
sleep(20)
nvg_599_dut.email_test_results(rf)
exit()

status_page = nvg_599_dut.get_ui_home_network_status_page()
print(status_page)
exit()
#
# default_tr69_auto_ssid_values = nvg_599_dut.get_tr69_auto_ssid(ssid)
# # print(default_tr69_auto_ssid_values)
# #exit()
# if (default_tr69_auto_ssid_values.find('.' + ssid + '.Enable 0') != -1):
#     print('Pass ssid:' + ssid + ' default set to 0')
# else:
#     print('Fail ssid:' + ssid + ' default not set to 0')
#
# exit()

now = datetime.today().strftime("%B %d, %Y,%H:%M")
results_file = open('results_file.txt', mode = 'w', encoding = 'utf-8')

rf = open('results_file.txt', mode = 'w', encoding = 'utf-8')
rfa  = open('results_file.txt', mode = 'a', encoding = 'utf-8')
rf.write(now + '\n')
rfa.write(now + '\n')

results_file_archive=open('results_file.txt', mode ='a', encoding='utf-8')
results_file.write(now + '\n')
results_file_archive.write(now + '\n')

nvg_599_dut = Nvg599Class()

upgrade_rg_file ='/home/palmer/Downloads/nvg599-9.2.2h13d26_1.1.bin'
#test_status, duration = nvg_599_dut.upgrade_rg(upgrade_rg_file, rf, rfa)
test_status, duration = nvg_599_dut.upgrade_rg('/home/palmer/Downloads/nvg599-9.2.2h13d26_1.1.bin', rf, rfa)

sleep(300)
results_file.write("Test Title: RG Upgrade :" + upgrade_rg_file + " Test case " + test_status  + "Duration:" + duration  +'\n')
results_file_archive.write("Test Title: RG Upgrade :" + upgrade_rg_file + " Test case " + test_status  + "Duration:" + duration  +'\n')
#results_file_archive.write("Test Title: RG Upgrade:" + upgrade_rg_file + " Pass " + '\n')
# nvg_599_dut.factory_reset_rg()
#
# ssid = 3
# nvg_599_dut.set_auto_setup_ssid_via_tr69_cli(ssid)
# results_file.write("Test Title: Auto SSID 3 setup: Pass")
# results_file_archive.write("Test Title: Auto SSID 3 setup: Pass")
#
# ssid = 4
# nvg_599_dut.set_auto_setup_ssid_via_tr69_cli(ssid)
# results_file.write("Test Title: Auto SSID 4 setup: Pass")
# results_file_archive.write("Test Title: Auto SSID 4 setup: Pass")
# results_file.write("Test Title: RG Factory Reset:" + " Pass " + '\n')
# results_file_archive.write("Test Title: RG Factory Reset:" + " Pass " + '\n')
#
# results_file.write("Test Title: RG Factory Reset: turn_off_supplicant_cli(): Pass \n")
# results_file_archive.write("Test Title: RG Factory Reset: turn_off_supplicant_cli(): Pass \n")
#
# results_file.write("Test Title: RG Factory Reset: enable_sshd_ssh_cli(): Pass \n")
# results_file_archive.write("Test Title: RG Factory Reset: enable_sshd_ssh_cli(): Pass \n")
#
# results_file.write("Test Title: RG Factory Reset: conf_tr69_eco_url(): Pass \n")
# results_file_archive.write("Test Title: RG Factory Reset: conf_tr69_eco_url(): Pass \n")
#
# results_file.write("Test Title: RG Factory Reset: turn_off_wi_fi_security_protection_cli(): Pass \n")
# results_file_archive.write("Test Title: RG Factory Reset: turn_off_wi_fi_security_protection_cli(): Pass \n")
#
# results_file.write("Test Title: RG Factory Reset: enable_parental_control():Pass \n")
# results_file_archive.write("Test Title: RG Factory Reset: enable_parental_control(): \n")
exit()
ssid = 3
nvg_599_dut.set_auto_setup_ssid_via_tr69_cli(ssid)
results_file.write("Test Title: Auto SSID 3 setup: Pass")
results_file_archive.write("Test Title: Auto SSID 3 setup: Pass")

ssid = 4
nvg_599_dut.set_auto_setup_ssid_via_tr69_cli(ssid)
results_file.write("Test Title: Auto SSID 4 setup: Pass")
results_file_archive.write("Test Title: Auto SSID 4 setup: Pass")
results_file.close()
results_file_archive.close()
nvg_599_dut.email_test_results(results_file)
sleep(30)

exit()


nvg_599_dut.nmcli_get_connections()
exit()

# start = time.time()
# sleep(10)
# end = time.time()
#
# # round_dog = round(start)
# #print('time: ' + str(time.time()))
# print('time: ' + str(round(end - start)))

upgrade_rg_file ='/home/palmer/Downloads/nvg599-9.2.2h13d22_1.1.bin'
# upgrade_rg_file ='/home/palmer/Downloads/nvg599-9.2.2h12d15_1.1.bin'
# upgrade_rg_file ='/home/palmer/Downloads/nvg599-9.2.2h2d23_1.1.bin'

# airties_ap_net = "AirTies_Air4920_33N3"
# nvg_599_dut.wps_pair_default_airties(airties_ap_net)
exit()
# nvg_599_dut.ui_set_band_bandwith_channel('5g', 80, 36)
# this will go in factory reset once ribust enough
airties_ap_net = "AirTies_SmartMesh_4PNF"
nvg_599_dut.wps_pair_default_airties(airties_ap_net)
sleep(300)
airties_ap_net = "AirTies_Air4920_33N3"
nvg_599_dut.wps_pair_default_airties(airties_ap_net)
# wps_pair_default_airties(airties_ap_net)

# nvg_599_dut.ui_set_band_bandwith_channel('5g', 80, 100)
nvg_599_dut.ui_set_band_bandwith_channel('5g', 80, 36)

exit()
upgrade_rg_file ='/home/palmer/Downloads/nvg599-9.2.2h13d17_1.1.bin'
nvg_599_dut.upgrade_rg(upgrade_rg_file)
sleep(300)
nvg_599_dut.factory_reset_rg()
sleep(300)
nvg_599_dut.enable_guest_network_and_set_password_ssid()

#nvg_599_dut.enable_guest_network_and_set_password_ssid()
rg_url = 'http://192.168.1.254/'
nvg_599_dut.wps_button_click(rg_url)
airties_ap_net = "AirTies_SmartMesh_4PNF"
nvg_599_dut.wps_pair_default_airties(airties_ap_net)

sleep(300)
nvg_599_dut.wps_button_click(rg_url)
airties_ap_net = "AirTies_Air4920_33N3"

# nvg_599_dut.ui_set_band_bandwith_channel('5g', 80, 100)
nvg_599_dut.ui_set_band_bandwith_channel('5g', 80, 36)


# test_dfs(nvg_599_dut)
# tst_ping_rg_power_level(nvg_599_dut, '192.168.1.94', '20')
# nvg_599_dut.ui_enable_guest_network_and_set_password_ssid()
# exit()
# wifi_password_script = "1111111111"
# custom_security = "Custom Password"
# set_wifi_return_code = nvg_599_dut.ui_set_wifi_password(custom_security, wifi_password_script)
# print('******** set_wifi_return_code: ' + set_wifi_return_code)
# min_ping, avg_ping, max_ping, mdev_ping, sent, received, loss  = nvg_599_dut.ping_from_local_host(remote_ip, number_of_pings)
# print('min:'+ min_ping + ' max:' + max_ping)
ping_file = open('ping_file_with_power_change_test.txt', 'a')
# now = datetime.today().isoformat()
now = datetime.today().strftime("%B %d, %Y,%H:%M")
# ping_file.writelines('Ping ' + remote_ip + ' RG Pwr %:' + str(percentage) +  ' Sent:' + sent + ' Received:' + received + ' Percent loss:' + loss + '%' + ' Date:' + now + '\n')
ping_file.writelines('Date:' + now + '599 FW Ver:' + nvg_599_dut.software_version + ' Ser. No:' + nvg_599_dut.serial_number + '\n')
# ping_file.writelines('Ping ' + remote_ip + ' RG Pwr %:' + str(percentage) +  ' Sent:' + sent + ' Received:' + received + ' Percent loss:' + loss + '%\n')
# ping_file.writelines('Date:' + now + ' Ping ' + remote_ip + ' RG Pwr %:' + str(percentage) +  ' Sent:' + sent + ' Received:' + received + ' Percent loss:' + loss + '%\n')

# ping_file.writelines("599 FW Ver:" + nvg_599_dut.software_version + " Ser. No:" +
#                      nvg_599_dut.serial_number + '  min_ping:' + min_ping + '  avg_ping:' + avg_ping +
#                      '  max_ping:' + max_ping + '  max dev:' + mdev_ping +'\n')

# ping_file.writelines('Minimum:' + min_ping + ' Average::' + avg_ping + ' Maximum:' + max_ping + ' max dev:' + mdev_ping +'\n')

# ping_file.writelines('Date:' + now + " 599 FW Ver:" + nvg_599_dut.software_version + " Ser. No:" +
#                      nvg_599_dut.serial_number + '  min_ping:' + min_ping + '  avg_ping:' + avg_ping +
#                      '  max_ping:' + max_ping + '  max dev:' + mdev_ping)
ping_file.writelines('\n')
ping_file.close()
Nvg599Class.nmcli_test()
exit()
########################################################################################################3
# evice_dict = nvg_599_dut.ui_get_device_list()
# print('device_dict:', device_dict)
# nvg_599_dut.disable_enable_wifi_2_4_and_5g_wifi()
# exit()
# nvg_599_dut.enable_parental_control()
# nvg_599_dut.enable_guest_network_and_set_password_ssid()
# nvg_599_dut.factory_reset_rg()
# nvg_599_dut.turn_off_supplicant_cli()
# nvg_599_dut.set_fixed_ip_allocation()
# nvg_599_dut.enable_guest_network_and_set_password_ssid()
# Nvg599Class().run_speed_test_from_android_termux("192.168.1.70")
# test_rg_upgrade_speedtest(nvg_599_dut,firmware_599_available,firmware_599_names)


# import datetime
# date = datetime.datetime.strptime(date, "%m%d%Y")
# from pylab import *

speed_test_result_list = []
# download, upload = Nvg599Class.run_speed_test_from_android_termux("192.168.1.70")
for i in  range(4):
    print('loop:' + str(i))
    speed_test_result_tuple  = Nvg599Class.run_speed_test_from_android_termux("192.168.1.70")
    speed_test_result_list.append(speed_test_result_tuple)

down_load = []
up_load = []

for a,b in speed_test_result_list:
    print('download speed: ' + a + ' Upload speed:' + b)
    down_load.append(a)
    up_load.append(b)

import matplotlib.pyplot as plt
# nvg_599_dut.enable_sshd_ssh_cli()
# nvg_599_dut.turn_off_supplicant_cli()
# nvg_599_dut.conf_tr69_eco_url()
# url_to_check = "http://192.168.1.254/cgi-bin/home.ha"
# nvg_599_dut.factory_reset_rg()
# nvg_599_dut.enable_parental_control()
# nvg_599_dut.turn_off_wi_fi_security_protection_cli()
# dfs_file = open('dfs_file.txt','a')
# nvg_599_dut.factory_reset_rg()

# the default  url is "http://192.168.1.254/cgi-bin/home.ha"
# nvg_599_dut.factory_reset_rg()
# security, current_password = nvg_599_dut.ui_get_wifi_password()
# print('current pasword:' + current_password)
# print('security:' + security + ' new pasword:' + current_password)
# wpa or defwpa
default_security = "Default Password"
custom_security = "Custom Password"

# too long >  63
wifi_password_script = "1111111111"
set_wifi_return_code = nvg_599_dut.ui_set_wifi_password(custom_security, wifi_password_script)
print('******** set_wifi_return_code: ' + set_wifi_return_code)

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
update_rg ='/home/palmer/Downloads/nvg599-9.2.2h13d10_1.1.bin'
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
# remote_driver = nvg_599_dut.remote_webserver()
# remote_driver.get("http://www.firefox.com")
# nvg_599_dut.enable_sshd_ssh_cli()
# nvg_599_dut.turn_off_supplicant_cli()
# nvg_599_dut.conf_tr69_eco_url()
# url_to_check = "http://192.168.1.254/cgi-bin/home.ha"
# nvg_599_dut.factory_reset_rg(url_to_check)
# nvg_599_dut.enable_parental_control()
# nvg_599_dut.turn_off_wi_fi_security_protection_cli()
# dfs_file = open('dfs_file.txt','a')
# test_dfs(nvg_599_dut,dfs_file)
# Nvg599Class.factory_test()
# dfs_file.close()
# nvg_599_dut.poc_for_youtube()
exit()

ssid_band5 = "ATTqbrAnYs"
ssid_guest = "ATTqbrAnYs_Guest"
ssid_band2 = "ATTqbrAnYs"

nvg_599_dut.set_ui_ssid(ssid_band5,ssid_guest,ssid_band2)

band2, guest, band5 = nvg_599_dut.get_ui_ssid()
print('band 2: '+ band2 + '  guest: '+ guest + '  band5: ' + band5)

exit()
show_ip_lan_dict = nvg_599_dut.cli_sh_rg_ip_lan_info_cli()

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
# sleep(1)
# airTiesTerm.expect("ogin:")
# airTiesTerm.sendline('root')
# airTiesTerm.expect("#")

# airTiesTerm.sendline('wl -i wl0 chanspec')
# airTiesTerm.expect("#")
# airTies2GResult=airTiesTerm.before
# print(airTies2GResult)
# airTies2GChannel = airTies2GResult.split()[-2]
# print("2G",airTies2GChannel)
# print("")
# airTiesTerm.sendline('wl -i wl1 chanspec')
# airTiesTerm.expect("#")
# airTies5GResult=airTiesTerm.before
# airTies5GChannelInfo = airTies5GResult.split()[-2]
# print("5GInfo",airTies5GChannelInfo)
# airTies5GChannel =airTies5GChannelInfo.split("/")[0]
# print("5G Channel,airTies5GChannel)
# airTies5GBandwidth =airTies5GChannelInfo.split("/")[1]
# print("5G Bandwidth",airTies5GBandwidth)
# resultFile.close()
print("###############################################################################")
print("###############################################################################")


list2G = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
list5G = [36, 40, 44, 48, 52, 56, 60, 64, 100, 104, 108, 112, 116, 1132, 136, 140, 144, 149, 153, 161]
list2GLite = [1]
list5GLite = [36]

airTiesTerm = pexpect.spawn("telnet 192.168.1.67",encoding='utf-8')
airTiesTerm.expect("ogin:")
airTiesTerm.sendline('root')
airTiesTerm.expect("#")

airTiesTerm.logfile= sys.stdout
# channelResultFP = open('channelResult.txt', 'w+')
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

# resultFile.close()
# sleep(1)

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

# driver = webdriverhttps://www.waketech.edu/programs-courses/credit/electrical-systems-technology/degrees-pathways.
# Chrome('/usr/local/bin/chromedriver')
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

