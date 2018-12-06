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
FRAME_FP_TYPE_MAX = 2


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