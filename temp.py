#! /usr/bin/env python3
# vim:fenc=utf-8
#
# Copyright © 2022 gq <gq@laceap1>
#
# Distributed under terms of the MIT license.

"""
detect the temp
"""

import sys
import smbus


def get_temp(address=0x48):
    bus = smbus.SMBus(1)
    raw = bus.read_word_data(address, 0)
    raw = ((raw<<8) & 0XFF00) + (raw >> 8)
    temp = (raw/32.0)/8.0
    return temp

if __name__ == "__main__":
    print(get_temp)
