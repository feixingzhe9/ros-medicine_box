#!/usr/bin/env python
# coding=utf-8

import Queue
import time
import uart_rcv
import uart_send
import protocol_param
ack_queue = Queue.Queue()


class RcvOpt(object):
    def __init__(self):
        self.start_flag = False
        self.end_flag = False
        self.data_len = 0
        self.rcv_cnt = 0
        self.rcv_buf = []
        for i in range(0, protocol_param.FRAME_LEN_MAX):
            self.rcv_buf.append(0)
        #print self.rcv_buf


def cal_frame_sum(data, data_len):
    data_sum = 0
    for i in range(0, data_len):
       data_sum = data_sum + data[i]
    return data_sum & 0x00ff

def protocol_proc_thread(tmp):
    data_tmp = 0
    wireless_rcv_com_opt = RcvOpt()
    #wireless_rcv_com_opt.__init__()
    while 1:
        time.sleep(0.1)
        while not uart_rcv.rcv_queue.empty():
            data_tmp = uart_rcv.rcv_queue.get()
            wireless_rcv_com_opt.rcv_buf[wireless_rcv_com_opt.rcv_cnt] = data_tmp
            if wireless_rcv_com_opt.start_flag == True:
                if wireless_rcv_com_opt.rcv_cnt == 1:
                    wireless_rcv_com_opt.data_len = data_tmp

                if wireless_rcv_com_opt.rcv_cnt == wireless_rcv_com_opt.data_len - 1:
                    if wireless_rcv_com_opt.rcv_buf[wireless_rcv_com_opt.rcv_cnt] == protocol_param.FRAME_FOOTER:
                        wireless_rcv_com_opt.end_flag = True
                        wireless_rcv_com_opt.start_flag = False
                        wireless_rcv_com_opt.rcv_cnt = 0
                        #if check_frame_sum(wireless_rcv_com_opt.rcv_buf, wireless_rcv_com_opt.data_len - 1):
                        if cal_frame_sum(wireless_rcv_com_opt.rcv_buf, wireless_rcv_com_opt.data_len - 2) == wireless_rcv_com_opt.rcv_buf[wireless_rcv_com_opt.data_len - 2]:
                            proc_frame(wireless_rcv_com_opt.rcv_buf[2:], wireless_rcv_com_opt.data_len - 4)
                            print "process frame protocol"
                        else:
                            print "frame check sum error !"
                            print "cal check sum is: ", cal_frame_sum(wireless_rcv_com_opt.rcv_buf, wireless_rcv_com_opt.data_len - 1)
                            print "get check sum is: ", wireless_rcv_com_opt.rcv_buf[wireless_rcv_com_opt.data_len - 2]
                            print "rcv buf :", wireless_rcv_com_opt.rcv_buf
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
                if data_tmp == protocol_param.FRAME_HEADER:
                    print "get HEADER"
                    wireless_rcv_com_opt.start_flag = True
                    wireless_rcv_com_opt.end_flag = False

                wireless_rcv_com_opt.rcv_cnt = 0

            wireless_rcv_com_opt.rcv_cnt =  wireless_rcv_com_opt.rcv_cnt + 1
            if wireless_rcv_com_opt.rcv_cnt >= protocol_param.FRAME_LEN_MAX - 1:
                wireless_rcv_com_opt.start_flag = False
                wireless_rcv_com_opt.end_flag = False
                wireless_rcv_com_opt.rcv_cnt = 0


class AckInfo(object):
    def __init__(self):
        self.protocol_class = 0
        self.protocol_type = 0
        self.ack_mcu_id = 0
        self.serial_num = 0
        self.proc_status = 0
        self.data = []
        for i in range(0, protocol_param.FRAME_LEN_MAX):
            self.data.append(0)
    def clear(self):
        self.protocol_class = 0
        self.protocol_type = 0
        self.ack_mcu_id = 0
        self.serial_num = 0
        self.proc_status = 0
        for i in range(0, protocol_param.FRAME_LEN_MAX):
            self.data[i] = 0

def proc_frame(frame, frame_len):
    global ack_queue
    ack_info = AckInfo()
    frame_class = frame[0]
    frame_type = frame[1]
    if frame_len >= protocol_param.FRAME_LEN_MAX - 4:
        return -1
    if not protocol_param.is_protocol_class(frame_class):
        return -1
    serial_num = 0
    ack_id = 0
    ack_id = frame[5]
    ack_id |= frame[4] << 8
    ack_id |= frame[3] << 16
    ack_id |= frame[2] << 24
    serial_num = frame[9]
    serial_num |= frame[8] << 8
    serial_num |= frame[7] << 16
    serial_num |= frame[6] << 24

    print "frame type: ", str(frame_type)
    print "get ack id: ", str(ack_id)
    print "get serial num: ", str(serial_num)
    if frame_class == protocol_param.PROTOCOL_CLASS_COMMON:
        if not protocol_param.is_common_frame_type(frame_type):
            return -1
        if frame_type == protocol_param.FRAME_COMMON_HEART_BEAT:
            rcv_id = 0
            print "get id: ", hex(rcv_id)

            heart_beat_cnt = 0
            heart_beat_cnt = frame[9]
            heart_beat_cnt |= frame[8] << 8
            heart_beat_cnt |= frame[7] << 16
            heart_beat_cnt |= frame[6] << 24
            print "get heart beat cnt: ", str(heart_beat_cnt)
            ack_info.clear()
            ack_info.protocol_class = protocol_param.PROTOCOL_CLASS_COMMON
            ack_info.protocol_type = protocol_param.FRAME_COMMON_HEART_BEAT
            ack_info.data[0] = ack_id
            ack_info.data[1] = heart_beat_cnt

            ack_queue.put(ack_info)

        if frame_type == protocol_param.FRAME_COMMON_UNLOCK:
            ack_info.clear()
            ack_info.protocol_class = protocol_param.PROTOCOL_CLASS_COMMON
            ack_info.protocol_type = protocol_param.FRAME_COMMON_UNLOCK
            ack_info.serial_num = serial_num
            ack_info.ack_mcu_id = ack_id
            ack_queue.put(ack_info)

    elif frame_class == protocol_param.PROTOCOL_CLASS_FP:
        if not protocol_param.is_fp_frame_type(frame_type):
            return -1

        if frame_type == protocol_param.FRAME_FP_DEL_ALL_USER:
            ack_info.clear()
            ack_info.protocol_class = protocol_param.PROTOCOL_CLASS_FP
            ack_info.protocol_type = protocol_param.FRAME_FP_DEL_ALL_USER
            ack_info.serial_num = serial_num
            ack_info.ack_mcu_id = ack_id
            ack_info.proc_status = frame[10]
            ack_queue.put(ack_info)

        if frame_type == protocol_param.FRAME_FP_ADD_FP_BY_PRESS:
            ack_info.clear()
            ack_info.protocol_class = protocol_param.PROTOCOL_CLASS_FP
            ack_info.protocol_type = protocol_param.FRAME_FP_ADD_FP_BY_PRESS
            ack_info.serial_num = serial_num
            ack_info.ack_mcu_id = ack_id
            status = frame[10]
            ack_info.data[0] = status
            ack_queue.put(ack_info)


    elif frame_class == protocol_param.PROTOCOL_CLASS_DISPLAY:
        if not protocol_param.is_fp_frame_type(frame_type):
            return -1

        if frame_type == protocol_param.FRAME_DISPLAY_SHOW_CONTENT:
            ack_info.clear()
            ack_info.protocol_class = protocol_param.PROTOCOL_CLASS_DISPLAY
            ack_info.protocol_type = protocol_param.FRAME_DISPLAY_SHOW_CONTENT
            ack_info.serial_num = serial_num
            ack_info.ack_mcu_id = ack_id
            ack_info.proc_status = frame[10]
            ack_queue.put(ack_info)

        if frame_type == protocol_param.FRAME_FP_ADD_FP_BY_PRESS:
            ack_info.clear()
            ack_info.protocol_class = protocol_param.PROTOCOL_CLASS_FP
            ack_info.protocol_type = protocol_param.FRAME_FP_ADD_FP_BY_PRESS
            ack_info.serial_num = serial_num
            ack_info.ack_mcu_id = ack_id
            status = frame[10]
            ack_info.data[0] = status
            ack_queue.put(ack_info)

def __main__():
    pass
