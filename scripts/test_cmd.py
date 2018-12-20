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


test_show_content_pub = None

def pub_content():
    global test_show_content_pub
    #content_tmp =u"zhongewenhanzi中文汉字"
    #content = content_tmp.decode('GBK').encode('gb18030')
    #content = content_tmp.encode('gb2312')
    content_list = []
    #content = content_tmp.encode('gb18030')
    #content_tmp = 'zhongewenhanzi中文汉字'.encode('gb18030')
    content_tmp = 'Hello  <(诺亚医院物流机器人)>  world'.encode('gb18030')

    for i in range(0,len(content_tmp)):
        tmp = ord(content_tmp[i])
        if tmp >= 0x100:
            print tmp
            content_list.append(tmp >> 8)
            content_list.append(tmp & 0xff)
        else:
            content_list.append(tmp)
    print content_list
    msg = {}
    msg['start_x'] = 10
    msg['start_y'] = 250
    msg['color'] = 32
    msg['period'] = 3000
    msg['content'] = content_list
    print 'start to pub ...'
    test_show_content_pub.publish(json.dumps(msg))
    print 'pub finished'


if __name__ == '__main__':
    global test_show_content_pub
    rospy.init_node("driver_medicine_box_test_node", anonymous=True)
    test_show_content_pub = rospy.Publisher("driver_medicine_box/test_display", String, queue_size = 10)
    time.sleep(1)
    pub_content()
