import libtcodpy as libtcod
import textwrap

import constants

def message(new_msg, color = libtcod.white, game_msgs = []):
    #split the message if necessary, among multiple lines
    new_msg_lines = textwrap.wrap(new_msg, constants.MSG_WIDTH)

    for line in new_msg_lines:
        #if the buffer is full, remove the first line to make room for the new one
        if len(game_msgs) == constants.MSG_HEIGHT:
            del game_msgs[0]

        #add the new line as a tuple, with the text and the color
        game_msgs.append( (line, color) )
