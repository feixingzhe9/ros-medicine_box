#!/usr/bin/env python
# coding=utf-8

import serial

dev_com = "/dev/ttyUSB0"
ser_handle = None


def open_com():
    global ser_handle
    global dev_com
    ser_handle = serial.Serial(dev_com, 9600, timeout = 0.1)


def com_send(data):
    global ser_handle
    #ser_handle.write(data)
    ser_handle.write('1234567890')

def com_rcv(cnt):
    global ser_handle
    return ser_handle.read(cnt)

