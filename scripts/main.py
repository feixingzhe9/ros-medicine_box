#!/usr/bin/env python
# coding=utf-8

import rospy
import threading
import Queue
import sys
import numpy as np
import time
from com import uart_driver
from com import uart_rcv
from com import uart_send
from com import parse_uart
from com import fp_protocol
from com import protocol_param

def main():
    
    rospy.init_node("medicine_box", anonymous=True)

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
    #fp_protocol.add_fp_by_pressing(0x12345678, 0xb1, 2)
    fp_protocol.unlock(0x12345678)
    content_str = '诺亚医院物流机器人'
    content_gb = 'Hello 诺亚医院物流机器人 world'.encode('gb18030')
    #content_str.encode("gb18030")
    #content_gb = content_str.encode('gb18030')
    fp_protocol.show_content(0x12345678, 50, 10, content_gb, len(content_gb),\
                             protocol_param.DISPLAY_RESOLUTION_ASCII_8X16_NORMAL, protocol_param.DISPLAY_COLOR_RED, 1)
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
