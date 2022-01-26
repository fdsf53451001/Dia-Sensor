# -*- coding:utf-8 -*-
import smbus
from mlx90614 import MLX90614

# bus = smbus.SMBus(1)
address = 0x5a


if __name__ == '__main__':
    # for i in range(40):
    #     try:
    #         print(i,bus.read_byte_data(address,i))
    #     except Exception:
    #         print('Error happened!')
    thermo = MLX90614(address)
    print(thermo.get_obj_temp())