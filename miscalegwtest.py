#!/usr/bin/python3
from __future__ import print_function
import argparse
import binascii
import os
import sys
from bluepy import btle

height = 180 # height in cm

MISCALE_MAC = 'AA:BB:CC:DD'

global bmi
global water
global fat
global leanfat
bmi = 0.00
water = 0.00
fat = 0.00
leanfat = 0.00

if os.getenv('C', '1') == '0':
    ANSI_RED = ''
    ANSI_GREEN = ''
    ANSI_YELLOW = ''
    ANSI_CYAN = ''
    ANSI_WHITE = ''
    ANSI_OFF = ''
else:
    ANSI_CSI = "\033["
    ANSI_RED = ANSI_CSI + '31m'
    ANSI_GREEN = ANSI_CSI + '32m'
    ANSI_YELLOW = ANSI_CSI + '33m'
    ANSI_CYAN = ANSI_CSI + '36m'
    ANSI_WHITE = ANSI_CSI + '37m'
    ANSI_OFF = ANSI_CSI + '0m'


class ScanProcessor():

    def __init__(self):
        pass

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if dev.addr == MISCALE_MAC.lower() and isNewDev:
            print ('    Device: %s (%s), %d dBm %s. ' %
                   (
                       ANSI_WHITE + dev.addr + ANSI_OFF,
                       dev.addrType,
                       dev.rssi,
                       ('' if dev.connectable else '(not connectable)'))
                   , end='')
            for (sdid, desc, data) in dev.getScanData():
                if data.startswith('1b18') and sdid == 22:
                    measunit = data[4:6]
                    measured = int((data[28:30]+data[26:28]),16)*0.01
					#measured = int((data[8:10] + data[6:8]), 16) * 0.01
                    unit = ''

                    if measunit.startswith(('03', 'b3')): unit = 'lbs'
                    if measunit.startswith(('12', 'b2')): unit = 'jin'
                    if measunit == "02": unit = 'kg' ; measured = measured / 2
                    if measunit.startswith(('22', 'a2')): unit = 'kg' ; measured = measured / 2
                    bmi = (measured / (height*height))*10000
                    water = 0.72 * (-1.976 + 0.907 * measured)
                    fat = (1.281* bmi) - 10.13
                    leanfat = measured - fat

                    if unit:
                        print('')
                        self._publish(round(measured, 2), unit, bmi, water, fat, leanfat)
                    else:
                        print("Scale is sleeping.")

            if not dev.scanData:
                print ('\t(no data)')
            print

    def _publish(self, weight, unit, bmi, water, fat, leanfat):
        prefix = '{}/{}'.format('miscale/weight', unit)
        #self.mqtt_client.publish(prefix, weight, qos=1, retain=True)
        #self.mqtt_client.publish('miscale/bmi', bmi, qos=1, retain=True)
        #self.mqtt_client.publish('miscale/fat', fat, qos=1, retain=True)
        #self.mqtt_client.publish('miscale/water', water, qos=1, retain=True)
        #self.mqtt_client.publish('miscale/leanfat', leanfat, qos=1, retain=True)
        print('\tSent data to topic %s: %s %s' % (prefix, weight, unit))
        print('\tSent data to topic miscale/bmi: %s ' % (bmi))
        print('\tSent data to topic miscale/fat: %s ' % (fat))
        print('\tSent data to topic miscale/water: %s ' % (water))
        print('\tSent data to topic miscale/leanfat: %s ' % (leanfat))
        #print('BMI: %s' % (bmi))
        #print('Body fat: %s' % (fat))
        #print('Body water: %s' % (water))
        #print('Lean body mass: %s' % (leanfat))


def main():

    scanner = btle.Scanner().withDelegate(ScanProcessor())

    print (ANSI_RED + "Scanning for devices..." + ANSI_OFF)
    devices = scanner.scan(5)

if __name__ == "__main__":
    main()
