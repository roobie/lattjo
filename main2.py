#!/usr/bin/python2
#
#
# THE MAIN MODULE
#
#

import libtcodpy as libtcod
import constants
import global_state
import game_types
import ai_types


color_dark_wall = libtcod.Color(0, 0, 100)
color_light_wall = libtcod.Color(130, 110, 50)
color_dark_ground = libtcod.Color(50, 50, 150)
color_light_ground = libtcod.Color(200, 180, 50)

def render_all():
    global con

    #draw all global_state.entities in the list, except the player. we want it to
    #always appear over all other global_state.entities! so it's drawn later.
    for entity in global_state.entities:
        entity.draw(con)

    #blit the contents of "con" to the root console
    libtcod.console_blit(con, 0, 0, constants.MAP_WIDTH, constants.MAP_HEIGHT, 0, 0, 0)


    #prepare to render the GUI panel
    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    #print the game messages, one line at a time
    y = 1
    for (line, color) in global_state.game_msgs:
        libtcod.console_set_default_foreground(panel, color)
        libtcod.console_print_ex(panel, constants.MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT,line)
        y += 1

    #display names of global_state.entities under the mouse
    libtcod.console_set_default_foreground(panel, libtcod.light_gray)
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT, get_names_under_mouse())

    #blit the contents of "panel" to the root console
    libtcod.console_blit(panel, 0, 0, constants.SCREEN_WIDTH, constants.PANEL_HEIGHT, 0, 0, constants.PANEL_Y)


def get_names_under_mouse():
    global mouse
    #return a string with the names of all global_state.entities under the mouse

    (x, y) = (mouse.cx, mouse.cy)

    #create a list with the names of all global_state.entities at the mouse's coordinates and in FOV
    names = [obj.name for obj in global_state.entities]

    #join the names, separated by commas
    names = ', '.join(names)
    return names.capitalize()


def handle_keys():
    global key, mouse

    if key.vk == libtcod.KEY_ESCAPE:
        return 'exit'  #exit game

    return 'didnt-do-anything'


def initialise():
    global_state.game_msgs = []
    global_state.entities = [
        game_types.Entity(
            20, 20, 'O', 'thing' + str(i), libtcod.white,
            blocks=True,
            fighter=game_types.Fighter(
                hp=100, defense=1, power=2, xp=0, death_function=None),
            ai=ai_types.BasicAI())
        for i in range(10)]




def run_game():
    global key, mouse, con

    player_action = None

    game_state = 'playing'

    mouse = libtcod.Mouse()
    key = libtcod.Key()

    #main loop
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
        #render the screen
        render_all()

        libtcod.console_flush()

        #erase all global_state.entities at their old locations, before they move
        for entity in global_state.entities:
            entity.clear(con)

        #handle keys and exit game if needed
        player_action = handle_keys()
        if player_action == 'exit':
            #save_game()
            break

        #let monsters take their turn
        if game_state == 'playing':
            for entity in global_state.entities:
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
