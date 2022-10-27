##################################################

#           P26 ----> Relay_Ch1
#			P20 ----> Relay_Ch2
#			P21 ----> Relay_Ch3

##################################################
#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time
import smbus

Relay_Ch1 = 26
Relay_Ch2 = 20
Relay_Ch3 = 21

SPT1_Ch1 = 5
SPT1_Ch2 = 6

SPT2_Ch1 = 23
SPT2_Ch2 = 24

SPT3_Ch1 = 17
SPT3_Ch2 = 27

# SPT4_Ch1 = 13
# SPT4_Ch2 = 19

SPT4_Ch1 = 16
SPT4_Ch2 = 20

SPT5_Ch1 = 14
SPT5_Ch2 = 15

i2c_relay = True

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

if not i2c_relay:
    GPIO.setup(Relay_Ch1, GPIO.OUT)
    GPIO.setup(Relay_Ch2, GPIO.OUT)
    GPIO.setup(Relay_Ch3, GPIO.OUT)

print("Setup The Relay Module is [success]")

GPIO.setup(SPT1_Ch1, GPIO.OUT)
GPIO.setup(SPT1_Ch2, GPIO.OUT)

print("Setup SPT1 Module is [success]")

GPIO.setup(SPT2_Ch1, GPIO.OUT)
GPIO.setup(SPT2_Ch2, GPIO.OUT)

print("Setup SPT2 Module is [success]")

GPIO.setup(SPT3_Ch1, GPIO.OUT)
GPIO.setup(SPT3_Ch2, GPIO.OUT)

print("Setup SPT3 Module is [success]")

GPIO.setup(SPT4_Ch1, GPIO.OUT)
GPIO.setup(SPT4_Ch2, GPIO.OUT)

print("Setup SPT4 Module is [success]")

GPIO.setup(SPT5_Ch1, GPIO.OUT)
GPIO.setup(SPT5_Ch2, GPIO.OUT)

print("Setup SPT5 Module is [success]")

def all_relay_off():
    if i2c_relay:
        device_bus = 1
        device_addr = 0x10
        bus = smbus.SMBus(device_bus)
        for i in range(1,5):
            bus.write_byte_data(device_addr, i, 0x00)
    else:
        GPIO.output(Relay_Ch1,GPIO.HIGH)
        GPIO.output(Relay_Ch2,GPIO.HIGH)
        GPIO.output(Relay_Ch3,GPIO.HIGH)

def set_relay(num):
    if i2c_relay:
        device_bus = 1
        device_addr = 0x10
        bus = smbus.SMBus(device_bus)

        for i in range(1,5):
            bus.write_byte_data(device_addr, i, 0x00)

        bus.write_byte_data(device_addr, num, 0xFF)


    else:
        if num == 1:
            GPIO.output(Relay_Ch1,GPIO.LOW)
            print("Channel 1:The Common Contact is access to the Normal Open Contact!")
            GPIO.output(Relay_Ch2,GPIO.HIGH)
            GPIO.output(Relay_Ch3,GPIO.HIGH)
            time.sleep(0.2)
        elif num == 2:
            GPIO.output(Relay_Ch2,GPIO.LOW)
            print("Channel 2:The Common Contact is access to the Normal Open Contact!")
            GPIO.output(Relay_Ch1,GPIO.HIGH)
            GPIO.output(Relay_Ch3,GPIO.HIGH)
            time.sleep(0.2)
        elif num == 3:
            GPIO.output(Relay_Ch3,GPIO.LOW)
            print("Channel 3:The Common Contact is access to the Normal Closed Contact!\n")
            GPIO.output(Relay_Ch1,GPIO.HIGH)
            GPIO.output(Relay_Ch2,GPIO.HIGH)
            time.sleep(0.2)

def set_spt1(num):
    """
    num = {1, 2, 3, 4}
    p1:  5 low, 6 high
    p2:  5 low, 6 low
    p3: 5 high, 6 high
    p4: 5 hight 6 low
    """

    ch1 = SPT1_Ch1
    ch2 = SPT1_Ch2

    try:
        if num == 1:
            GPIO.output(ch1, GPIO.LOW)
            GPIO.output(ch2, GPIO.HIGH)
        elif num == 2:
            GPIO.output(ch1, GPIO.LOW)
            GPIO.output(ch2, GPIO.LOW)
        elif num == 3:
            GPIO.output(ch1, GPIO.HIGH)
            GPIO.output(ch2, GPIO.HIGH)
        elif num == 4:
            GPIO.output(ch1, GPIO.HIGH)
            GPIO.output(ch2, GPIO.LOW)

        return True
    except:
        return False


def set_spt2(num):
    """
    num = {1, 2, 3, 4}
    """
    try:
        if num == 4:
            GPIO.output(SPT2_Ch1, GPIO.LOW)
            GPIO.output(SPT2_Ch2, GPIO.HIGH)
        elif num == 2:
            GPIO.output(SPT2_Ch1, GPIO.LOW)
            GPIO.output(SPT2_Ch2, GPIO.LOW)
        elif num == 3:
            GPIO.output(SPT2_Ch1, GPIO.HIGH)
            GPIO.output(SPT2_Ch2, GPIO.HIGH)
        elif num == 1:
            GPIO.output(SPT2_Ch1, GPIO.HIGH)
            GPIO.output(SPT2_Ch2, GPIO.LOW)
        return True
    except:
        return False

def set_spt3(num):
    """
    num = {1, 2, 3, 4}
    """
    ch1 = SPT3_Ch1
    ch2 = SPT3_Ch2

    if num == 4:
        GPIO.output(ch1, GPIO.LOW)
        GPIO.output(ch2, GPIO.HIGH)
    elif num ==2:
        GPIO.output(ch1, GPIO.LOW)
        GPIO.output(ch2, GPIO.LOW)
    elif num ==3:
        GPIO.output(ch1, GPIO.HIGH)
        GPIO.output(ch2, GPIO.HIGH)
    elif num == 1:
        GPIO.output(ch1, GPIO.HIGH)
        GPIO.output(ch2, GPIO.LOW)



def set_spt4(num):
    """
    num = {1, 2, 3, 4}
    """
    ch1 = SPT4_Ch1
    ch2 = SPT4_Ch2

    if num == 4:
        GPIO.output(ch1, GPIO.LOW)
        GPIO.output(ch2, GPIO.HIGH)
    elif num ==2:
        GPIO.output(ch1, GPIO.LOW)
        GPIO.output(ch2, GPIO.LOW)
    elif num ==3:
        GPIO.output(ch1, GPIO.HIGH)
        GPIO.output(ch2, GPIO.HIGH)
    elif num == 1:
        GPIO.output(ch1, GPIO.HIGH)
        GPIO.output(ch2, GPIO.LOW)


def set_spt5(num):
    """
    num = {1, 2, 3, 4}
    """
    ch1 = SPT5_Ch1
    ch2 = SPT5_Ch2

    if num == 4:
        GPIO.output(ch1, GPIO.LOW)
        GPIO.output(ch2, GPIO.HIGH)
    elif num ==2:
        GPIO.output(ch1, GPIO.LOW)
        GPIO.output(ch2, GPIO.LOW)
    elif num ==3:
        GPIO.output(ch1, GPIO.HIGH)
        GPIO.output(ch2, GPIO.HIGH)
    elif num == 1:
        GPIO.output(ch1, GPIO.HIGH)
        GPIO.output(ch2, GPIO.LOW)


if __name__ == "__main__":
    set_spt1(1)
    set_spt2(1)
    # set_relay(2)

    # all_relay_off()
    # set_relay(2)
    # set_spt3(4)
    # set_spt4(1)

    # for Zhang 80DB
    # set_relay(2)
    # set_spt2(3)
    # set_spt3(4)
    # set_spt4(3)

    # for Zang 60DB
    # set_relay(2)
    # set_spt2(3)
    # set_spt3(1)
    # set_spt4(1)

    # for Guo 80DB myself

    # set_relay(3)
    # set_spt2(4)
    # set_spt4(2)

    # set_spt5(4)

    # for Guo 80DB one

    # set_relay(1)
    # set_spt2(1)
    # set_spt4(4)

    # set_relay(3)
