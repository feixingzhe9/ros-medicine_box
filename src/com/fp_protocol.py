#!/usr/bin/env python
# coding=utf-8

import time
import Queue
import sys
import uart_driver
import uart_send
import parse_uart
import protocol_param

reload(sys)
sys.setdefaultencoding('utf-8')

file_ = sys._getframe().f_code.co_filename
func_ = sys._getframe().f_code.co_name

#line_ = 'sys._getframe().f_lineno'

serial_num = 0


def fill_mcu_id_and_serial_num(data, mcu_id, seiral_num):
#    data[0] = (mcu_id >> 24) & 0xff
#    data[1] = (mcu_id >> 16) & 0xff
#    data[2] = (mcu_id >> 8) & 0xff
#    data[3] = mcu_id & 0xff
#    data[4] = (serial_num >> 24) & 0xff
#    data[5] = (serial_num >> 16) & 0xff
#    data[6] = (serial_num >> 8) & 0xff
#    data[7] = serial_num & 0xff

    data[4] = (mcu_id >> 24) & 0xff
    data[5] = (mcu_id >> 16) & 0xff
    data[6] = (mcu_id >> 8) & 0xff
    data[7] = mcu_id & 0xff
    data[8] = (serial_num >> 24) & 0xff
    data[9] = (serial_num >> 16) & 0xff
    data[10] = (serial_num >> 8) & 0xff
    data[11] = serial_num & 0xff

def del_all_user(mcu_id):
    global serial_num
    serial_num = serial_num + 1
    data_len = 14 
    send_data = uart_send.SendData()
    send_data.clear()
    send_data.data[0] = protocol_param.FRAME_HEADER
    send_data.data[1] = data_len
    send_data.data[2] = protocol_param.PROTOCOL_CLASS_FP
    send_data.data[3] = protocol_param.FRAME_FP_DEL_ALL_USER

    fill_mcu_id_and_serial_num(send_data.data, mcu_id, serial_num)

    send_data.data[12] = parse_uart.cal_frame_sum(send_data.data, data_len - 2)
    send_data.data[13] = protocol_param.FRAME_FOOTER

    send_data.len = data_len
    uart_send.send_queue.put(send_data)

    cnt = 0
    while 1:
        if not parse_uart.ack_queue.empty():
            ack = parse_uart.ack_queue.get()
            print 'my serial num: ', serial_num
            print 'ack serial num: ', ack.serial_num
            print 'my mcu id: ', mcu_id
            print 'get mcu id: ', ack.ack_mcu_id
            print 'get status: ', ack.proc_status
            if ack.serial_num == serial_num and ack.ack_mcu_id  == mcu_id and ack.proc_status == 1 and \
               ack.protocol_type == protocol_param.FRAME_FP_DEL_ALL_USER and \
               ack.protocol_class == protocol_param.PROTOCOL_CLASS_FP:  # do we need ack.proc_status == 1 ?
                print file_, sys._getframe().f_code.co_name, sys._getframe().f_lineno, " get right ack"
                uart_send.send_queue.queue.clear()  #clear send queue cause we get right ack
                break
        time.sleep(0.1)
        cnt = cnt + 1
        if cnt % 5 == 4:
            uart_send.send_queue.put(send_data)
        if cnt > 5 * 5:
            print file_, sys._getframe().f_code.co_name, sys._getframe().f_lineno, "Error: del_all_user failed ! !"
            return -1

def add_fp_by_pressing(mcu_id, fp_id, fp_permission):
    if fp_permission >= protocol_param.FP_PERMISSION_MAX or fp_permission <= protocol_param.FP_PERMISSION_MIN or fp_id > 0xffff:
        print file_, sys._getframe().f_code.co_name, sys._getframe().f_lineno, " ERROR: param error !"
        print fp_permission

    global serial_num
    serial_num = serial_num + 1
    data_len = 17
    send_data = uart_send.SendData()
    send_data.clear()
    send_data.data[0] = protocol_param.FRAME_HEADER
    send_data.data[1] = data_len
    send_data.data[2] = protocol_param.PROTOCOL_CLASS_FP
    send_data.data[3] = protocol_param.FRAME_FP_ADD_FP_BY_PRESS
    fill_mcu_id_and_serial_num(send_data.data, mcu_id, serial_num)
    send_data.data[12] = (fp_id << 8) & 0xff
    send_data.data[13] = fp_id & 0xff
    send_data.data[14] = fp_permission & 0xff
    send_data.data[15] = parse_uart.cal_frame_sum(send_data.data, data_len - 2)
    send_data.data[16] = protocol_param.FRAME_FOOTER

    send_data.len = data_len
    uart_send.send_queue.put(send_data)

    cnt = 0
    while 1:
        if not parse_uart.ack_queue.empty():
            ack = parse_uart.ack_queue.get()
            print 'my serial num: ', serial_num
            print 'ack serial num: ', ack.serial_num
            if ack.serial_num == serial_num and ack.ack_mcu_id  == mcu_id and ack.proc_status == 0 and\
               ack.protocol_type == protocol_param.FRAME_FP_ADD_FP_BY_PRESS and ack.protocol_class == protocol_param.PROTOCOL_CLASS_FP:
                print file_, sys._getframe().f_code.co_name, sys._getframe().f_lineno, " get right ack"
                uart_send.send_queue.queue.clear()  #clear send queue cause we get right ack and do not need to send anything
                break
        time.sleep(0.1)
        cnt = cnt + 1
        if cnt % 25 == 4:
            uart_send.send_queue.put(send_data)
        if cnt > 25 * 20:
            print ''
            print file_, sys._getframe().f_code.co_name, sys._getframe().f_lineno, "Error: del_all_user failed ! !"
            return -1


def unlock(mcu_id):

    global serial_num
    serial_num = serial_num + 1
    data_len = 14
    send_data = uart_send.SendData()
    send_data.clear()
    send_data.data[0] = protocol_param.FRAME_HEADER
    send_data.data[1] = data_len
    send_data.data[2] = protocol_param.PROTOCOL_CLASS_COMMON
    send_data.data[3] = protocol_param.FRAME_COMMON_UNLOCK
    fill_mcu_id_and_serial_num(send_data.data, mcu_id, serial_num)
    send_data.data[12] = parse_uart.cal_frame_sum(send_data.data, data_len - 2)
    send_data.data[13] = protocol_param.FRAME_FOOTER

    send_data.len = data_len
    uart_send.send_queue.put(send_data)

    cnt = 0
    while 1:
        if not parse_uart.ack_queue.empty():
            ack = parse_uart.ack_queue.get()
            print 'my serial num: ', serial_num
            print 'ack serial num: ', ack.serial_num
            if ack.serial_num == serial_num and ack.ack_mcu_id  == mcu_id and ack.proc_status == 0 and\
               ack.protocol_type == protocol_param.FRAME_COMMON_UNLOCK and ack.protocol_class == protocol_param.PROTOCOL_CLASS_COMMON:
                print file_, sys._getframe().f_code.co_name, sys._getframe().f_lineno, " get right ack"
                uart_send.send_queue.queue.clear()  #clear send queue cause we get right ack and do not need to send anything
                break
        time.sleep(0.1)
        cnt = cnt + 1
        if cnt % 5 == 4:
            uart_send.send_queue.put(send_data)
        if cnt > 5 * 8:
            print ''
            print file_, sys._getframe().f_code.co_name, sys._getframe().f_lineno, "Error: unlock failed ! !"
            return -1



def show_content(mcu_id, start_x, start_y, content, content_len, resolution, color, layer):
    if start_x >= protocol_param.DISPLAY_X_MAX or start_y >=protocol_param.DISPLAY_Y_MAX:
        print file_, sys._getframe().f_code.co_name, sys._getframe().f_lineno, " ERROR: param error !"
        print 'start_x: ', start_x, ' start_y: ', start_y

    global serial_num
    str_len = len(content)
    serial_num = serial_num + 1
    data_len = str_len + 24

    send_data = uart_send.SendData()

    send_data.clear()
    send_data.data[0] = protocol_param.FRAME_HEADER
    send_data.data[1] = data_len
    send_data.data[2] = protocol_param.PROTOCOL_CLASS_DISPLAY
    send_data.data[3] = protocol_param.FRAME_DISPLAY_SHOW_CONTENT
    fill_mcu_id_and_serial_num(send_data.data, mcu_id, serial_num)
    send_data.data[12] = (start_x << 8) & 0xff
    send_data.data[13] = start_x & 0xff
    send_data.data[14] = (start_y << 8) & 0xff
    send_data.data[15] = start_y & 0xff
    send_data.data[16] = (content_len << 8) & 0xff
    send_data.data[17] = content_len & 0xff
    send_data.data[18] = (color << 8) & 0xff
    send_data.data[19] = color & 0xff
    send_data.data[20] = resolution & 0xff
    send_data.data[21] = layer & 0xff

    #content = content.encode('gb18030')
    for i in range(0, str_len):
        send_data.data[22 + i] = ord(content[i]) & 0xff

    send_data.data[22 + str_len] = parse_uart.cal_frame_sum(send_data.data, data_len - 2)
    send_data.data[23 + str_len] = protocol_param.FRAME_FOOTER

    send_data.len = data_len
    uart_send.send_queue.put(send_data)

    cnt = 0
    while 1:
        if not parse_uart.ack_queue.empty():
            ack = parse_uart.ack_queue.get()
            print 'my serial num: ', serial_num
            print 'ack serial num: ', ack.serial_num
            if ack.serial_num == serial_num and ack.ack_mcu_id  == mcu_id and ack.proc_status == 1 and\
               ack.protocol_type == protocol_param.FRAME_DISPLAY_SHOW_CONTENT and ack.protocol_class == protocol_param.PROTOCOL_CLASS_DISPLAY:
                print file_, sys._getframe().f_code.co_name, sys._getframe().f_lineno, " get right ack"
                uart_send.send_queue.queue.clear()  #clear send queue cause we get right ack and do not need to send anything
                break
        time.sleep(0.1)
        cnt = cnt + 1
        if cnt % 25 == 4:
            uart_send.send_queue.put(send_data)
        if cnt > 25 * 20:
            print ''
            print file_, sys._getframe().f_code.co_name, sys._getframe().f_lineno, "Error: show content failed ! !"
            return -1
