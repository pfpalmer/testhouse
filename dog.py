from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import rgclass
import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from email.mime.text import MIMEText


from email.message import EmailMessage

import os
import smtplib,ssl
import pexpect
import re
import sys


###fp = open("channel.txt",'a+')Creating a token

###fp.write("1test and so on and so forth " + "\n")
###fp.seek(0)
###fpcontents = fp.read()
###print(fpcontents)
###.close()
#exit()
#exit()
#msg['Subject'] = 'From the test house'

###from email.MIMEMultipart import MIMEMultipart
###from email.MIMEText import MIMEText


###port = 587  # For SSL
###smtp_server = "smtp.gmail.com"
###sender_email = "leandertesthouse@gmail.com"  # Enter your address
###receiver_email = "paul.palmer@arris.com"  # Enter receiver address
#password = input("Type your password and press enter: ")
#password = raw_input("type password and enter")
###password = "arris123"

##mybody ="These are the test results and they all look good. this includes the mybody"

###msg = MIMEMultipart()

###msg['From']="leandertesthouse@gmail.com"
###msg['To']= "paul.palmer@arris.com"
###msg['Subject']="Test results"

#body = mybody
###body = fpcontents

###msg.attach(MIMEText(body,'plain'))

###msg = msg.as_string()
#context = ssl.create_default_context()
#server = smtplib.SMTP_SSL(smtp_server,port,context)
###server = smtplib.SMTP_SSL(smtp_server)
###server.ehlo()
#server.starttls()
###server.login(sender_email,password)
#server.sendmail(sender_email,msg,receiver_email)
###server.sendmail(sender_email,receiver_email,msg)

###server.quit()

# driver = webdriverhttps://www.waketech.edu/programs-courses/credit/electrical-systems-technology/degrees-pathways.Chrome('/usr/local/bin/chromedriver')
# driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
# driver.get('http://www.google.com')
# driver.get('http://192.168.1.254')
# .implicitly_wait(20)
# driver.find_elements_by_tag_name("Settings") // this is for 599
# driver.find_element_by_link_text("Settings").click()

# driver.findElement(By.linkText("Home Network")).click()
# driver.implicitly_wait(20)

# driver.find_element_by_link_text("LAN").click()
# driver.implicitly_wait(20)
# driver.maximize_window()

# driver.find_element_by_link_text("Wi-Fi").click()
# .implicitly_wait(20)

# password = driver.find_element_by_id("ADM_PASSWORD")

# password.send_keys("8>1769&295")

# driver.find_element_by_class_name('button').click()
# driver.find_element_by_xpath("//button[@value='Submit']").click()
# button.click()

# driver.implicitly_wait(20)

# ENter device access code

# sleep(30)
# driver.quit()



#channelResultFile.write("2G =  RG channel= + str(i) +  airTies5GChannel =  + airTies5GChannel  +  Passed + \n")

#exit()

#pfp

rgTerm = pexpect.spawn("telnet 192.168.1.254")
sleep(1)



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
#print("5G Channel",airTies5GChannel)
#airTies5GBandwidth =airTies5GChannelInfo.split("/")[1]
#print("5G Bandwidth",airTies5GBandwidth)

#resultFile.close()


print("###############################################################################")
print("###############################################################################")
print("###############################################################################")

rgTerm.expect("ogin:")
rgTerm.sendline('admin')

rgTerm.expect("assword:")
# child.sendline('alcatel')
rgTerm.sendline('*<#/53#1/2')

rgTerm.expect("UNLOCKED>")
rgTerm.sendline('magic')
rgTerm.expect("UNLOCKED>")

output = rgTerm.sendline('tr69 get InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.Channel')
#rgTerm.expect("MAGIC>")
rgTerm.expect("UNLOCKED>")

#result=rgTerm.after
result=rgTerm.before

#Channel = myresult.split()[-2]

list2G=[1,2,3,4,5,6,7,8,9,10,11]
list5G=[36,40,44,48,52,56,60,64,100,104,108,112,116,1132,136,140,144,149,153,161]
list2GLite=[1,2,3,9,11]
list5GLite=[36,40,44,136]

airTiesTerm = pexpect.spawn("telnet 192.168.1.67",encoding='utf-8')
airTiesTerm.expect("ogin:")
airTiesTerm.sendline('root')
airTiesTerm.expect("#")

airTiesTerm.logfile= sys.stdout

## new comment -pfp-
#add another comment
#channelResultFile = open('/tmp/channelResult.txt', "a+")
channelResultFP = open('channelResult.txt', 'w+')


for l2g in list2GLite:
    for i in list5GLite:
        print("Config RG channel="+str(i))
        output = rgTerm.sendline('tr69 SetParameterValues InternetGatewayDevice.LANDevice.1.WLANConfiguration.5.Channel=' + str(i))
        rgTerm.expect("UNLOCKED>")
        # re-telnet into the airTies each time because the telnet session gets hung when channel is reset
        print("Checking airTies for channel match: "+str(i))
        # i think we want to wait before trying to login to the airtiesssh-add ~/.ssh/id_rsa
        sleep(200)
        airTiesTerm = pexpect.spawn("telnet 192.168.1.67", encoding='utf-8')
        sleep(1)
        airTiesTerm.expect("ogin")
        airTiesTerm.sendline('root')
        airTiesTerm.expect("#")
        airTiesTerm.sendline('wl -i wl0 chanspec')
        airTiesTerm.expect("#")
        airTies2GResult = airTiesTerm.before
        print("airties result " + str(airTies2GResult))
        airTies2GChannel = airTies2GResult.split()[-2]
        airTies2GChannel = airTies2GChannel.split()[-1]

        print("AirTies 2G = ", airTies2GChannel)
        print("")
        sleep(2)


        airTiesTerm.sendline('wl -i wl1 chanspec')
        airTiesTerm.expect("#")
        airTies5GResult = airTiesTerm.before
        airTies5GChannelInfo = airTies5GResult.split()[-2]
        print("5G Info ", airTies5GChannelInfo)

        sleep(2)
        #airTies5GChannel = airTies5GChannelInfo.split("/")[-2]
        airTies5GChannel = airTies5GChannelInfo.split("/")[0]

        print("5G Channel = ", airTies5GChannel)
        airTies5GBandWidth = airTies5GChannelInfo.split("/")[-1]  # type: object
        print("5G Bandwidth = ", airTies5GBandWidth)


        airTiesTerm.sendline('exit')
    #    airTiesTerm.sendline("^]")
        airTiesTerm.sendline("\x1b\r")
     #   airTiesTerm.send("close")
        airTiesTerm.terminate(force=True)

        sleep(10)

        #print("what?"+ str(i))

        #print (type(i))
        #print ("airTies5GChannel is of type "+ type(airTies5GChannel))


        if i == int(airTies5GChannel):
            channelResultFP.write(" \n")
            channelResultFP.write(" 2G = "+ str(l2g) + " RG channel= "+ str(i) + " airTies5GChannel = " + airTies5GChannel  +  "  Passed" )
            #channelResultFP.write("\r\n 2G = "+ str(l2g) + " RG channel= "+ str(i) + " airTies5GChannel = " + airTies5GChannel  +  "Passed" + "\r\n")

            channelResultFP.write("\n ")

            print(">> 2G = " + str(l2g) + " RG channel= "+ str(i) + " airTies5GChannel = " + airTies5GChannel  +  " Passed")
            print ("----l2g--------------------------------------------- -------------------")
        else:
            channelResultFP.write(" ")
            #channelResultFP.write("\r\n 2G = " + str(l2g) + "RG channel= "+ str(i) + " airTies5GChannel = " + airTies5GChannel  +  " Failed" + "\r\n")
            channelResultFP.write(" 2G = " + str(l2g) + "RG channel= "+ str(i) + " airTies5GChannel = " + airTies5GChannel  +  " Failed  ")

            channelResultFP.write(" ")

        sleep(30)


#
#newlines=('/n')
#channelResultContents = open('channelResult.txt').read().split('\n')

# this next statement is sketchy

#channelResultContents = channelResultFP.newlines

#channelResultContents = channelResultFile.seek(0)

#channelResultFP = open('channelResult.txt', 'w+')

### this used to work
channelResultFP.seek(0)
channelResultContents = channelResultFP.read()
channelResultFP.close()

print ("-channelResultContents:" + channelResultContents)

#msg['From']="leandertesthouse@gmail.com"
#msg['To']= "paul.palmer@arris.com"
#msg['Subject']="Test results"
gmail_password="arris123"
gmail_user= 'leandertesthouse@gmail.com'

to = "paul.palmer@arris.com"
sent_from = 'gmail_user'
subject ="Test results"


body = "Results:" + channelResultContents
#body = channelResultContents
email_text = """
From:%s
To:%s
Subject:%s
%s 
""" % (sent_from, " ,".join(to),subject,body)

#msg.attach(MIMEText(html,'html'))
#msg = " test test"

#msg = msg.as_string()

#message = """\
#From: "leandertesthouse"
#To: "paul.palmer@arris.com"
#
#smtp_server = "smtp.gmail.com"
###smtp_server = "smtp.gmail.com"

try:
    server= smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    sleep(2)
    server.quit()

except:
    print ('Something went wrong')

#sender_email = "leandertesthouse@gmail.com"  # Enter your address
#receiver_email = "paul.palmer@arris.com"  # Enter recei
#smtp_server = "smtp.gmail.com"
#context = ssl.create_default_context()
#server = smtplib.SMTP_SSL(smtp_server,port,context)
##server = smtplib.SMTP_SSL(smtp_server)
#server = smtp_server

#server.ehlo()
#server.starttls()

#server.sendmail(sender_email,receiver_email,msg)
#server.send_msg(msg)


#with smtplib.SMTP(smtp_server, port) as server:
#    server.ehlo()  # Can be omitted
#    server.starttls(context=context)
#    server.ehlo()  # Can be omitted
#    server.login(sender_email, password)
#    server.sendmail(sender_email, receiver_email, message)

#exit()



#print ("1-------------------")
#print (Channel)
#print("1----------------------")
#exit()
#resultFile.write(str(result))
#rgTerm.sendline('exit')
#resultFile.close()
#sleep(1)
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


print("Turning off supplicant")
ip = "192.168.1.254"
password = '<#/53#1/2'
child = pexpect.spawn("telnet " "192.168.1.254")
sleep(1)

import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import os
import pexpect
import re
import serial

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

import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import os
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

# different styles of uptime results. I try to parse them all. Yeee!
# Examples from different machines:
# [x86] Linux 2.4 (Redhat 7.3)
#  2:06pm  up 63 days, 18 min,  3 users,  load average: 0.32, 0.08, 0.02
# [x86] Linux 2.4.18-14 (Redhat 8.0)
#  3:07pm  up 29 min,  1 user,  load average: 2.44, 2.51, 1.57
# [PPC - G4] MacOS X 10.1 SERVER Edition
# 2:11PM  up 3 days, 13:50, 3 users, load averages: 0.01, 0.00, 0.00
# [powerpc] Darwin v1-58.corefa.com 8.2.0 Darwin Kernel Version 8.2.0
# 10:35  up 18:06, 4 users, load averages: 0.52 0.47 0.36
# [Sparc - R220] Sun Solaris (8)
#  2:13pm  up 22 min(s),  1 user,  load average: 0.02, 0.01, 0.01
# [x86] Linux 2.4.18-14 (Redhat 8)
# 11:36pm  up 4 days, 17:58,  1 user,  load average: 0.03, 0.01, 0.00
# AIX jwdir 2 5 0001DBFA4C00
#  09:43AM   up  23:27,  1 user,  load average: 0.49, 0.32, 0.23
# OpenBSD box3 2.9 GENERIC#653 i386
#  6:08PM  up 4 days, 22:26, 1 user, load averages: 0.13, 0.09, 0.08

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
# child.interact()
# child.expect(pexpect.EOF)

# child.sendline("quit")
# child.expect(">")

# print("done")
# child.sendline("bye")


child.expect("assword:")
child.sendline('alcatel')
# child.sendline('*<#/53#1/2')
print("logged in to host")

import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import os
import pexpect
import re
import serial

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

# different styles of uptime results. I try to parse them all. Yeee!
# Examples from different machines:
# [x86] Linux 2.4 (Redhat 7.3)
#  2:06pm  up 63 days, 18 min,  3 users,  load average: 0.32, 0.08, 0.02
# [x86] Linux 2.4.18-14 (Redhat 8.0)
#  3:07pm  up 29 min,  1 user,  load average: 2.44, 2.51, 1.57
# [PPC - G4] MacOS X 10.1 SERVER Edition
# 2:11PM  up 3 days, 13:50, 3 users, load averages: 0.01, 0.00, 0.00
# [powerpc] Darwin v1-58.corefa.com 8.2.0 Darwin Kernel Version 8.2.0
# 10:35  up 18:06, 4 users, load averages: 0.52 0.47 0.36
# [Sparc - R220] Sun Solaris (8)
#  2:13pm  up 22 min(s),  1 user,  load average: 0.02, 0.01, 0.01
# [x86] Linux 2.4.18-14 (Redhat 8)
# 11:36pm  up 4 days, 17:58,  1 user,  load average: 0.03, 0.01, 0.00
# AIX jwdir 2 5 0001DBFA4C00
#  09:43AM   up  23:27,  1 user,  load average: 0.49, 0.32, 0.23
# OpenBSD box3 2.9 GENERIC#653 i386
#  6:08PM  up 4 days, 22:26, 1 user, load averages: 0.13, 0.09, 0.08

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
# child.interact()
# child.expect(pexpect.EOF)

# child.sendline("quit")
# child.expect(">")

# print("done")
# child.sendline("bye")

child.expect("#")
child.sendline('exit')
sleep(5)
# driver.webdriver.quit()
exit()
# driver = webdriver.firefox('/home/palmer/.local/lib/python2.7/site-packages/chromedriver')
# driver = webdriver.chrome()
# browser.get('https://www.google.com')

# different styles of uptime results. I try to parse them all. Yeee!
# Examples from different machines:
# [x86] Linux 2.4 (Redhat 7.3)
#  2:06pm  up 63 days, 18 min,  3 users,  load average: 0.32, 0.08, 0.02
# [x86] Linux 2.4.18-14 (Redhat 8.0)
#  3:07pm  up 29 min,  1 user,  load average: 2.44, 2.51, 1.57
# [PPC - G4] MacOS X 10.1 SERVER Edition
# 2:11PM  up 3 days, 13:50, 3 users, load averages: 0.01, 0.00, 0.00
# [powerpc] Darwin v1-58.corefa.com 8.2.0 Darwin Kernel Version 8.2.0
# 10:35  up 18:06, 4 users, load averages: 0.52 0.47 0.36
# [Sparc - R220] Sun Solaris (8)
#  2:13pm  up 22 min(s),  1 user,  load average: 0.02, 0.01, 0.01
# [x86] Linux 2.4.18-14 (Redhat 8)
# 11:36pm  up 4 days, 17:58,  1 user,  load average: 0.03, 0.01, 0.00
# AIX jwdir 2 5 0001DBFA4C00
#  09:43AM   up  23:27,  1 user,  load average: 0.49, 0.32, 0.23
# OpenBSD box3 2.9 GENERIC#653 i386
#  6:08PM  up 4 days, 22:26, 1 user, load averages: 0.13, 0.09, 0.08

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

import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import os
import pexpect
import re
import serial

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

exit()

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

# different styles of uptime results. I try to parse them all. Yeee!
# Examples from different machines:
# [x86] Linux 2.4 (Redhat 7.3)
#  2:06pm  up 63 days, 18 min,  3 users,  load average: 0.32, 0.08, 0.02
# [x86] Linux 2.4.18-14 (Redhat 8.0)
#  3:07pm  up 29 min,  1 user,  load average: 2.44, 2.51, 1.57
# [PPC - G4] MacOS X 10.1 SERVER Edition
# 2:11PM  up 3 days, 13:50, 3 users, load averages: 0.01, 0.00, 0.00
# [powerpc] Darwin v1-58.corefa.com 8.2.0 Darwin Kernel Version 8.2.0
# 10:35  up 18:06, 4 users, load averages: 0.52 0.47 0.36
# [Sparc - R220] Sun Solaris (8)
#  2:13pm  up 22 min(s),  1 user,  load average: 0.02, 0.01, 0.01
# [x86] Linux 2.4.18-14 (Redhat 8)
# 11:36pm  up 4 days, 17:58,  1 user,  load average: 0.03, 0.01, 0.00
# AIX jwdir 2 5 0001DBFA4C00
#  09:43AM   up  23:27,  1 user,  load average: 0.49, 0.32, 0.23
# OpenBSD box3 2.9 GENERIC#653 i386
#  6:08PM  up 4 days, 22:26, 1 user, load averages: 0.13, 0.09, 0.08

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


child.expect(">>")

child.sendline('save')
child.expect(">>")

child.sendline("view")
child.expect(">>")

out = child.before
print(out)
#
# child.interact()
# child.expect(pexpect.EOF)

# child.sendline("quit")
# child.expect(">")

# print("done")
# child.sendline("bye")

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
# child.interact()
# child.expect(pexpect.EOF)

# child.sendline("quit")
# child.expect(">")

# print("done")
# child.sendline("bye")
