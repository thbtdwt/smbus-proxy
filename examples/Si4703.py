# -*- coding: utf-8 -*-

"""
This is an example of smbus-proxy-client
"""

import RPi.GPIO as GPIO
from smbus_proxy import proxy_client
import time

_reset_pin = 11
_en_pin = 7
i2c_address = 0x10

bus = proxy_client.ProxyClient('localhost:50051', 1)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(_reset_pin, GPIO.OUT)
GPIO.setup(_en_pin, GPIO.OUT)
time.sleep(1)
GPIO.output(_reset_pin, GPIO.LOW)
GPIO.output(_en_pin, GPIO.HIGH)
GPIO.output(_reset_pin, GPIO.HIGH)
time.sleep(1)

try:
    # dump all registers
	i = 0
	data = bus.read_i2c_block_data(i2c_address,0x0A)
	for r in [ "0x0A", "0x0B", "0x0C", "0x0D", "0x0E", "0x0F", "0x00", "0x01", "0x02", "0x03", "0x04", "0x05", "0x06", "0x07", "0x08", "0x09"]:
		up = data[i]
		low = data[i+1]
		print("%s = %02x %02x" % (r,up,low))
		i += 2
finally:
	GPIO.cleanup()
