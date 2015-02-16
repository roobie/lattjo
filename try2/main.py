#!/usr/bin/python2
#
#
# THE MAIN MODULE
#
#

import libtcodpy as libtcod
from fysom import Fysom

import constants
from world import World

game_state = Fysom({
    'initial': 'initialising',
    'events': [
        {'name': 'pause',
         'src': 'playing',
         'dst': 'paused'},
        {'name': 'play',
         'src': ['initialising', 'paused'],
         'dst': 'playing'}
    ]
})

def bootstrap():
    world = World()

libtcod.console_set_custom_font(
    'arial10x10.png',
    libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)


libtcod.console_init_root(
    constants.SCREEN_WIDTH,
    constants.SCREEN_HEIGHT,
    'Bjorn\'s freakish playground',
    False)


libtcod.sys_set_fps(constants.LIMIT_FPS)


con = libtcod.console_new(
    constants.MAP_WIDTH,
    constants.MAP_HEIGHT)


panel = libtcod.console_new(
    constants.SCREEN_WIDTH,
    constants.PANEL_HEIGHT)


if __name__ == '__main__':
    bootstrap()
