#!/usr/bin/env python
# coding=utf-8

import rospy
import threading
import Queue
import sys
import numpy as np
import time
import json
from com import uart_driver
from com import uart_rcv
from com import uart_send
from com import parse_uart
from com import fp_protocol
from com import protocol_param
from std_msgs.msg import String

def __add_fp_by_press_test_callback(msg):
    cmd = json.loads(msg.data)
    fp_id = 0
    if cmd['fp_id'] is not 0:
        fp_id = cmd['fp_id']
        print 'fp_id is: ', fp_id
    print 'callback get fp id: ', fp_id
    fp_protocol.add_fp_by_pressing(0x12345678, fp_id, 2)

def __del_user_test_callback(msg):
    cmd = json.loads(msg.data)
    fp_id = 0
    if cmd['del_user'] is not 0:
        fp_id = cmd['del_user']
        print 'fp_id is: ', fp_id
    print 'callback get fp id: ', fp_id
    fp_protocol.del_all_user(mcu_id = 0x12345678)

def __common_unlock_test_callback(msg):
    cmd = json.loads(msg.data)
    lock_num = 0
    if cmd['unlock'] is not 0:
        lock_num = cmd['unlock']
        print 'fp_id is: ', fp_id
    print 'callback get lock_num id: ', lock_num
    fp_protocol.unlock(mcu_id = 0x12345678)

def __display_test_callback(msg):
    cmd = json.loads(msg.data)
    print 'test display callback'
    print cmd
    start_x = cmd['start_x']
    start_y = cmd['start_y']
    #resolution = cmd['resolution']
    color = cmd['color']
    period = cmd['period']
    content = cmd['content']
    print 'start_x: ', start_x
    print 'start_y: ', start_y
    print 'period: ', period
    content_gb = content.encode('gb18030')
#    for i in content_gb:
#        print 'content_gb: ', hex(i)
#    print 'content_gb: ', content_gb
    content_gb = content
    fp_protocol.show_content(0x12345678, start_x, start_y, content_gb, len(content_gb),\
                             protocol_param.DISPLAY_RESOLUTION_ASCII_8X16_NORMAL, protocol_param.DISPLAY_COLOR_RED, 1)

def main():
    
    rospy.init_node("medicine_box", anonymous=True)

    rospy.Subscriber("driver_medicine_box/test_add_fp_by_press",String , __add_fp_by_press_test_callback, None, 5)
    rospy.Subscriber("driver_medicine_box/test_fp_del_all_users",String , __del_user_test_callback, None, 5)
    rospy.Subscriber("driver_medicine_box/test_common_unlock",String , __common_unlock_test_callback, None, 5)
    rospy.Subscriber("driver_medicine_box/test_display",String , __display_test_callback, None, 5)

    uart_driver.open_com()
    thread_send = threading.Thread(target = uart_send.send_thread, args = (0,))
    thread_rcv = threading.Thread(target = uart_rcv.rcv_thread, args = (0,))
    thread_protocol_proc = threading.Thread(target = parse_uart.protocol_proc_thread, args = (0,))

    #thread_send.setDaemon(True)
    #thread_rcv.setDaemon(True)

    thread_send.start()
    thread_rcv.start()
    thread_protocol_proc.start()
    #thread_send.join()
    #thread_rcv.join()
    print "join test"
    #### test code start ####
    #fp_protocol.del_all_user(mcu_id = 0x12345678)
    #fp_protocol.add_fp_by_pressing(0x12345678, 0xb2, 2)
    fp_protocol.unlock(0x12345678)
    #content_str = '诺亚医院物流机器人'
    content_gb = 'Hello 诺亚医院物流机器人 world'.encode('gb18030')
    #content_str.encode("gb18030")
    #content_gb = content_str.encode('gb18030')
    #fp_protocol.show_content(0x12345678, 50, 10, content_gb, len(content_gb),\
    #                         protocol_param.DISPLAY_RESOLUTION_ASCII_8X16_NORMAL, protocol_param.DISPLAY_COLOR_RED, 1)
    rospy.spin()

if __name__ == "__main__":
    try:
        main()
    except Exception: #rospy.ROSInterruptException:
        #thread_send.stop()
        #thread_rcv.stop()
        #thread_protocol_proc.stop()
        rospy.logerr(sys.exc_info())
        rospy.loginfo("lost connect")
        exit(1)
