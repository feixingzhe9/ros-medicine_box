#!/usr/bin/env python
# coding=utf-8


FRAME_HEADER = 0x5A
FRAME_FOOTER = 0xA5

FRAME_LEN_MAX = 255



#### protocol class define ####
PROTOCOL_CLASS_MIN = 0
PROTOCOL_CLASS_COMMON = 1
PROTOCOL_CLASS_FP = 2
PROTOCOL_CLASS_DISPLAY = 3
PROTOCOL_CLASS_MCU_UPLOAD = 4
PROTOCOL_CLASS_MAX = 5


#### protocol common class type define ####
FRAME_COMMON_TYPE_MIN = 0
FRAME_COMMON_HEART_BEAT = 1
FRAME_COMMON_UNLOCK = 2
FRAME_COMMON_TYPE_MAX = 3

#### protocol fingerprint class type define ####
FRAME_FP_TYPE_MIN = 0
FRAME_FP_DEL_ALL_USER = 1
FRAME_FP_ADD_FP_BY_PRESS = 2
FRAME_FP_TYPE_MAX = 3

FRAME_DISPLAY_MIN = 0
FRAME_DISPLAY_SHOW_CONTENT = 1


DISPLAY_X_MAX = 480
DISPLAY_Y_MAX = 320

DISPLAY_COLOR_WHITE     =      0xFFFF
DISPLAY_COLOR_BLACK     =      0x0000
DISPLAY_COLOR_BLUE      =      0x001F
DISPLAY_COLOR_BLUE2     =      0x051F
DISPLAY_COLOR_RED       =      0xF800
DISPLAY_COLOR_MAGENTA   =      0xF81F
DISPLAY_COLOR_GREEN     =      0x07E0
DISPLAY_COLOR_CYAN      =      0x7FFF
DISPLAY_COLOR_YELLOW    =      0xFFE0


DISPLAY_RESOLUTION_16X32_NORMAL      = 1
DISPLAY_RESOLUTION_ASCII_8X16_NORMAL = 2
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



DISPLAY_LINE_NUM_MAX    = 10


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
