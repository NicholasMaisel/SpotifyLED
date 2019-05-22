from config import *

def rgb_to_hex():
    color_list = color_list
    for note_index in range(len(color_list)):
        for color_index in range(len(color_list[note_index])):
            color_setting = color_list[note_index][color_index]
            color_list[note_index][color_index] = "{0:x}".format(color_setting)
    return(color_list)
