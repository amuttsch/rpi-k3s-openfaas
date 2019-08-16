""" Display eth1 ip and cluster health on lcd monitor
"""

import fcntl
import os
import struct
import socket
import time

from kubernetes import client, config

import lcd_i2c as lcd

DISPLAY_DELAY = 10

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config(os.path.join(os.environ["HOME"], '.kube/config'))

k_v1 = client.CoreV1Api()

def print_cluster_info():
    lcd.lcd_string('k3s OpenFaaS RPi', lcd.LCD_LINE_1)
    lcd.lcd_string('running! :-)', lcd.LCD_LINE_2)

def print_number_of_nodes():
    ret = k_v1.list_node(watch=False)
    nodes_ready = 0
    nodes_total = len(ret.items)

    for node in ret.items:
        for condition in node.status.conditions:
            if condition.type == 'Ready' and condition.status == 'True':
                nodes_ready += 1

    lcd.lcd_string('k3s nodes:', lcd.LCD_LINE_1)
    lcd.lcd_string(str(nodes_ready) + ' / ' + str(nodes_total), lcd.LCD_LINE_2)

def print_pods_in_openfaas():
    ret = k_v1.list_namespaced_pod("openfaas-fn", watch=False)
    lcd.lcd_string('OpenFaaS pods:', lcd.LCD_LINE_1)
    lcd.lcd_string(str(len(ret.items)), lcd.LCD_LINE_2)

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack(b'256s', ifname[:15].encode('utf-8'))
    )[20:24])


def print_ip():
    lcd.lcd_string('eth1:', lcd.LCD_LINE_1)
    try:
        lcd.lcd_string(get_ip_address('eth1'), lcd.LCD_LINE_2)
    except:
        lcd.lcd_string('Not connected', lcd.LCD_LINE_2)


try:
    lcd.lcd_init()

    print_cluster_info()
    time.sleep(DISPLAY_DELAY)

    while True:
        print_ip()
        time.sleep(DISPLAY_DELAY)

        print_number_of_nodes()
        time.sleep(DISPLAY_DELAY)

        print_pods_in_openfaas()
        time.sleep(DISPLAY_DELAY)

except KeyboardInterrupt:
    pass
finally:
    lcd.lcd_byte(0x01, lcd.LCD_CMD)

