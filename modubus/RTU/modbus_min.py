#!/usr/bin/env python3

import serial
import minimalmodbus
from time import sleep

client1 = minimalmodbus.Instrument('COM4', 1, debug=False)  # port name, slave address (in decimal)
client1.serial.baudrate = 9600  # baudrate
client1.serial.bytesize = 8
client1.serial.parity   = serial.PARITY_NONE # serial.PARITY_EVEN
client1.serial.stopbits = 1
client1.serial.timeout  = 0.2      # seconds
client1.mode = minimalmodbus.MODE_RTU # rtu or ascii mode
client1.clear_buffers_before_each_transaction = True

client1.address         = 1        # this is the slave address number

print([
    client1.read_register(registeraddress=1,number_of_decimals=0,functioncode=4,signed=False),
    client1.read_register(registeraddress=2,number_of_decimals=0,functioncode=4,signed=False),
])

client1.close_port_after_each_call = True