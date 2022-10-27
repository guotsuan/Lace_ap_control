#! /usr/bin/env python3
# vim:fenc=utf-8
#
# Copyright © 2022 gq <gq@laceap1>
#
# Distributed under terms of the MIT license.

"""
timing and logging
"""
import socket
from io import BytesIO
import pynmea2
from pynmea2 import ParseError
from socket import error as socket_error
import sys


def get_gps_coord():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect(("192.168.1.111", 4001))
    except socket_error:
        print("Cannot connect to the GPS/NTP server")
        print("Please wait for the GPS/NTP server to power up... or we have",
              " a serious problem.")
        sys.exit()

    get_coord = False

    with BytesIO() as buffer:
        while not get_coord:
            # Read in some number of bytes -- balance this
            ff = s.recv(2048)
            buffer.write(ff)
            buffer.seek(0)
            for line in buffer.readlines():
                if line == '':
                    break

                try:
                    msg = pynmea2.parse(line.decode())
                except ParseError:
                    pass
                else:
                    if hasattr(msg, "lat"):
                        lat = msg.lat
                        full_lat = msg.lat_dir + lat[0:2] + \
                            u"\N{DEGREE SIGN}" + lat[2:] + "'"

                        lon = msg.lon
                        full_lon = msg.lon_dir + lon[0:3] + \
                            u"\N{DEGREE SIGN}" + lon[3:] + "'"
                        s.close()
                        get_coord = True

                        return full_lat, full_lon

if __name__ == "__main__":
    print(get_gps_coord())
