#!/usr/bin/env python
# coding=utf-8


FRAME_HEADER = 0x5A
FRAME_FOOTER = 0xA5

FRAME_LEN_MAX = 255



#### protocol class define ####
PROTOCOL_CLASS_MIN = 0
PROTOCOL_CLASS_COMMON = 1
PROTOCOL_CLASS_FP = 2
PROTOCOL_CLASS_DIS = 3
PROTOCOL_CLASS_MAX = 4


#### protocol common class type define ####
FRAME_COMMON_TYPE_MIN = 0
FRAME_COMMON_HEART_BEAT = 1
FRAME_COMMON_TYPE_MAX = 2

#### protocol fingerprint class type define ####
FRAME_FP_TYPE_MIN = 0
FRAME_FP_DEL_ALL_USER = 1
FRAME_FP_ADD_FP_BY_PRESS = 2
FRAME_FP_TYPE_MAX = 3


#### fingerprint permmison level ####
FP_PERMISSION_MIN = 0
FP_PERMISSION_1 = 1
FP_PERMISSION_2 = 2
FP_PERMISSION_3 = 3
FP_PERMISSION_MAX =4


#### fingerprint errcode ####
FINGERPRINT_ACK_SUCCESS       =  0x00  #	successful
FINGERPRINT_ACK_FAIL          =  0x01  #	failure
FINGERPRINT_ACK_FULL          =  0x04  #	fingerprint lib is full !
FINGERPRINT_ACK_NO_USER       =  0x05  #	no such user
FINGERPRINT_ACK_USER_OCCUPIED =  0x06  #
FINGERPRINT_ACK_USER_EXIST    =  0x07  #
FINGERPRINT_ACK_TIMEOUT       =  0x08  #	operation timeout


def is_protocol_class(protocol_class):
    if protocol_class > PROTOCOL_CLASS_MIN and protocol_class < PROTOCOL_CLASS_MAX:
        return True
    return False

def is_common_frame_type(frame_type):
    if frame_type > FRAME_COMMON_TYPE_MIN and frame_type < FRAME_COMMON_TYPE_MAX:
        return True
    return False

def is_fp_frame_type(frame_type):
    if frame_type > FRAME_FP_TYPE_MIN and frame_type < FRAME_FP_TYPE_MAX:
        return True
    return False
