from config import *

def rgb_to_hex():
    colors = color_list
    for note_index in range(len(colors)):
        for color_index in range(len(colors[note_index])):
            color_setting = colors[note_index][color_index]
            colors[note_index][color_index] = "{0:x}".format(color_setting)
    return(colors)
