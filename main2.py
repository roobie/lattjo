#!/usr/bin/python2
#
#
# THE MAIN MODULE
#
#

import libtcodpy as libtcod
from fysom import Fysom

import entities as entity_types
import constants
import game_types
import ai_types
import mapping

global_state = game_types.World()

color_dark_wall = libtcod.Color(0, 0, 100)
color_light_wall = libtcod.Color(130, 110, 50)
color_dark_ground = libtcod.Color(50, 50, 150)
color_light_ground = libtcod.Color(200, 180, 50)

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

def render_all():
    global con
    global color_dark_wall, color_light_wall
    global color_dark_ground, color_light_ground

    #draw all global_state.map.entities in the list, except the player. we want it to
    #always appear over all other global_state.map.entities! so it's drawn later.
    for entity in global_state.map.entities:
        entity.draw(con)

    #blit the contents of "con" to the root console
    libtcod.console_blit(con, 0, 0, constants.MAP_WIDTH, constants.MAP_HEIGHT, 0, 0, 0)

    for y in range(constants.MAP_HEIGHT):
        for x in range(constants.MAP_WIDTH):
                wall = global_state.map.tiles[x][y].block_sight
                #if it's not visible right now, the player can only see it if it's explored
                if wall:
                    libtcod.console_set_char_background(con, x, y, color_dark_wall, libtcod.BKGND_SET )
                else:
                    libtcod.console_set_char_background(con, x, y, color_dark_ground, libtcod.BKGND_SET )
                    #since it's visible, explore it

    #prepare to render the GUI panel
    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    #print the game messages, one line at a time
    y = 1
    for (line, color) in global_state.messages:
        libtcod.console_set_default_foreground(panel, color)
        libtcod.console_print_ex(panel, constants.MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
        y += 1

    #display names of global_state.map.entities under the mouse
    libtcod.console_set_default_foreground(panel, libtcod.light_gray)
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT, get_names_under_mouse())

    #blit the contents of "panel" to the root console
    libtcod.console_blit(panel, 0, 0, constants.SCREEN_WIDTH, constants.PANEL_HEIGHT, 0, 0, constants.PANEL_Y)


def get_names_under_mouse():
    global mouse
    #return a string with the names of all global_state.map.entities under the mouse

    (x, y) = (mouse.cx, mouse.cy)

    #create a list with the names of all global_state.map.entities at the mouse's coordinates and in FOV
    names = [obj.name for obj in global_state.map.entities
             if obj.x == x and obj.y == y]

    #join the names, separated by commas
    names = ', '.join(names)
    return names.capitalize()


def handle_keys():
    global key, mouse, game_state

    def toggle_pause():
        if game_state.isstate('paused'):
            game_state.play()
        else:
            game_state.pause()

    if key.vk == libtcod.KEY_ESCAPE:
        #exit game
        return 'exit'
    elif key.vk == libtcod.KEY_SPACE:
        toggle_pause()
    else:
        #test for other keys
        key_char = chr(key.c)

        if key_char == 'p':
            toggle_pause()

    return 'didnt-do-anything'

def place_entities(entities, room):
    for i in range(4):
        x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
        y = libtcod.random_get_int(0, room.y1+1, room.y2-1)

        entities.append(entity_types.get('human', global_state, x=x, y=y))


def populate_map(map):
    for i in range(len(map.rooms)):
        place_entities(map.entities, map.rooms[i])

def initialise():
    global_state.map = mapping.make_map();
    populate_map(global_state.map)


def run_game():
    global key, mouse, con, game_state

    player_action = None

    game_state.play()

    mouse = libtcod.Mouse()
    key = libtcod.Key()

    #main loop
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
        #render the screen
        render_all()

        libtcod.console_flush()

        #erase all global_state.map.entities at their old locations, before they move
        for entity in global_state.map.entities:
            entity.clear(con)

        #handle keys and exit game if needed
        player_action = handle_keys()
        if player_action == 'exit':
            #save_game()
            break

        #let monsters take their turn
        if game_state.isstate('playing'):
            for entity in global_state.map.entities:
                if entity.ai:
                    entity.ai.update()

def bootstrap():
    initialise()
    run_game()

libtcod.console_set_custom_font(
    'arial10x10.png',
    libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

libtcod.console_init_root(
    constants.SCREEN_WIDTH,
    constants.SCREEN_HEIGHT,
    'python/libtcod tutorial',
    False)

libtcod.sys_set_fps(constants.LIMIT_FPS)
con = libtcod.console_new(constants.MAP_WIDTH, constants.MAP_HEIGHT)
panel = libtcod.console_new(constants.SCREEN_WIDTH, constants.PANEL_HEIGHT)

bootstrap()
