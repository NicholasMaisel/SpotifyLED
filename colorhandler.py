from config import *

def rgb_to_hex():
    colors_config = color_list
    colors = [x.split(' ') for x in colors_config]
    for note_index in range(len(colors)):
        for color_index in range(len(colors[note_index])):
            color_setting = colors[note_index][color_index]
            colors[note_index][color_index] = "{0:x}".format(int(color_setting))
    return(colors)
