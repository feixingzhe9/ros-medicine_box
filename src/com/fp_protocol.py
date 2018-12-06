#!/usr/bin/env python
# coding=utf-8

import time
import Queue
import uart_driver
import uart_send
import parse_uart
import protocol_param


serial_num = 0
def del_all_user():
    global serial_num
    serial_num = serial_num + 1
    data_len = 10 
    send_data = uart_send.SendData()
    send_data.clear()
    send_data.data[0] = protocol_param.FRAME_HEADER
    send_data.data[1] = data_len
    send_data.data[2] = protocol_param.PROTOCOL_CLASS_FP
    send_data.data[3] = protocol_param.FRAME_FP_DEL_ALL_USER
    send_data.data[4] = (serial_num >> 24) & 0xff
    send_data.data[5] = (serial_num >> 16) & 0xff
    send_data.data[6] = (serial_num >> 8) & 0xff
    send_data.data[7] = serial_num & 0xff
    send_data.data[8] = parse_uart.cal_frame_sum(send_data.data, data_len - 2)
    send_data.data[9] = protocol_param.FRAME_FOOTER

    send_data.len = data_len
    uart_send.send_queue.put(send_data)

    cnt = 0
    while 1:
        if not parse_uart.ack_queue.empty():
            ack = parse_uart.ack_queue.get()
            print 'my serial num: ', serial_num
            print 'ack serial num: ', ack.serial_num
            if ack.serial_num == serial_num:
                print  'del_all_user: get right ack'
                cnt = 0
                uart_send.send_queue.queue.clear()  #clear send queue cause we get right ack
                break
            print 'ack ', hex(ack.data[0])
            print 'ack ', ack.data[1]
            print 'ack ', ack.data[2]
            print 'ack ', ack.data[3]
        time.sleep(0.1)
        cnt = cnt + 1
        if cnt >= 5:
            uart_send.send_queue.put(send_data)
            cnt = 0

