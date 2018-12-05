#!/usr/bin/env python
# coding=utf-8

import time
import Queue
import uart_driver

#rcv_queue = None
rcv_queue = Queue.Queue()

def rcv_thread(tmp):
    global rcv_queue
    global ack_queue
    while 1:
        read_data = uart_driver.com_rcv(20)
        for i in read_data:
             rcv_queue.put(ord(i))
        time.sleep(0.1)


def __main__():
    pass