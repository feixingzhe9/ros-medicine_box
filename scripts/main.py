#!/usr/bin/env python
# coding=utf-8

import rospy
import threading
import Queue
import serial
import time
import sys
import numpy as np

dev_com = "/dev/ttyUSB0"
ser_handle = None

rcv_queue = None

FRAME_HEADER = 0x5A
FRAME_FOOTER = 0xA5

def open_com():
    global ser_handle
    global dev_com
    ser_handle = serial.Serial(dev_com, 9600, timeout = 0.3)


def com_send(data):
    global ser_handle
    #ser_handle.write(data)
    ser_handle.write('1234567890')


def com_rcv(cnt):
    global ser_handle
    return ser_handle.read(cnt)


def send_thread(tmp):
    while 1:
        #com_send("send test")
        #print "send"
        time.sleep(0.5)

def rcv_thread(tmp):
    global rcv_queue
    while 1:
        read_data = com_rcv(255)
        for i in read_data:
             #print i
             rcv_queue.put(ord(i))

        #print read_data 
        time.sleep(0.1)

class RcvOpt(object):
    def __init__(self):
        self.start_flag = False
        self.end_flag = False
        self.data_len = 0
        self.rcv_cnt = 0
        self.rcv_buf = []
        for i in range(0, 255):
            self.rcv_buf.append(0)
        print self.rcv_buf

def check_frame_sum(data, data_len):
    data_sum = 0
    for i in range(0, data_len):
       data_sum = data_sum + data[i]
    return data_sum

def protocol_proc_thread(tmp):
    global rcv_queue
    data_tmp = 0
    wireless_rcv_com_opt = RcvOpt()
    wireless_rcv_com_opt.__init__()
    while 1:
        time.sleep(0.1)
        while not rcv_queue.empty():
            data_tmp = rcv_queue.get()
            wireless_rcv_com_opt.rcv_buf[wireless_rcv_com_opt.rcv_cnt] = data_tmp
            if wireless_rcv_com_opt.start_flag == True:
                #print "header ready"
                #print " wireless_rcv_com_opt.rcv_cnt :", str(wireless_rcv_com_opt.rcv_cnt)
                if wireless_rcv_com_opt.rcv_cnt == 1:
                    wireless_rcv_com_opt.data_len = data_tmp
                    #print "wireless_rcv_com_opt.data_len :", str(wireless_rcv_com_opt.data_len)


                if wireless_rcv_com_opt.rcv_cnt == wireless_rcv_com_opt.data_len - 1:
                    #print "get wireless_rcv_com_opt.rcv_cnt == wireless_rcv_com_opt.data_len - 1"
                    if wireless_rcv_com_opt.rcv_buf[wireless_rcv_com_opt.rcv_cnt] == FRAME_FOOTER:
                        #print "get footer"
                        wireless_rcv_com_opt.end_flag = True
                        wireless_rcv_com_opt.start_flag = False
                        wireless_rcv_com_opt.rcv_cnt = 0
                        if check_frame_sum(wireless_rcv_com_opt.rcv_buf, wireless_rcv_com_opt.data_len - 1):
                            #frame_proc(&wireless_rcv_com_opt.rcv_buf[2], wireless_rcv_com_opt.data_len - 4)
                            print "hello here"
                        else:
                            print "frame check sum error !"
                            wireless_rcv_com_opt.end_flag = False
                            wireless_rcv_com_opt.start_flag = False
                            wireless_rcv_com_opt.rcv_cnt = 0
                        break
                    else:
                        print "frame len and frame tail is not right"
                        wireless_rcv_com_opt.end_flag = False
                        wireless_rcv_com_opt.start_flag = False
                        wireless_rcv_com_opt.rcv_cnt = 0
            else:
                #print "not ready"
                if data_tmp == FRAME_HEADER:
                    print "get HEADER"
                    wireless_rcv_com_opt.start_flag = True
                    wireless_rcv_com_opt.end_flag = False

                wireless_rcv_com_opt.rcv_cnt = 0
    
            wireless_rcv_com_opt.rcv_cnt =  wireless_rcv_com_opt.rcv_cnt + 1
            if wireless_rcv_com_opt.rcv_cnt >= 255 - 1:
                wireless_rcv_com_opt.start_flag = False
                wireless_rcv_com_opt.end_flag = False
                wireless_rcv_com_opt.rcv_cnt = 0


def main():
    
    rospy.init_node("medicine_box", anonymous=True)
    open_com()
    global rcv_queue
    rcv_queue = Queue.Queue()
    thread_send = threading.Thread(target = send_thread, args = (0,))
    thread_rcv = threading.Thread(target = rcv_thread, args = (0,))
    thread_protocol_proc = threading.Thread(target = protocol_proc_thread, args = (0,))

    #thread_send.setDaemon(True)
    #thread_rcv.setDaemon(True)

    thread_send.start()
    thread_rcv.start()
    thread_protocol_proc.start()
    #thread_send.join()
    #thread_rcv.join()
    print "join test"
    rospy.spin()

if __name__ == "__main__":
    try:
        main()
    except Exception: #rospy.ROSInterruptException:
        #thread_send.stop()
        #thread_rcv.stop()
        rospy.logerr(sys.exc_info())
        rospy.loginfo("lost connect")
        exit(1)


