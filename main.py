# -*- coding:utf-8 -*-

import smbus
bus = smbus.SMBus(1)
address = 0x5a


if __name__ == '__main__':
    for i in range(40):
        print(bus.read_byte_data(address,i))