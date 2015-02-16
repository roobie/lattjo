
import libtcodpy as libtcod

import global_state
import constants

from map_types import Tile, Rect

stairs = None

def create_room(room, the_map, fov_map):
    #go through the tiles in the rectangle and make them passable
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            the_map[x][y].blocked = False
            the_map[x][y].block_sight = False
            libtcod.map_set_properties(fov_map, x, y, True, True)

def create_h_tunnel(x1, x2, y, the_map, fov_map):
    #horizontal tunnel. min() and max() are used in case x1>x2
    for x in range(min(x1, x2), max(x1, x2) + 1):
        the_map[x][y].blocked = False
        the_map[x][y].block_sight = False
        libtcod.map_set_properties(fov_map, x, y, True, True)

def create_v_tunnel(y1, y2, x, the_map, fov_map):
    #vertical tunnel
    for y in range(min(y1, y2), max(y1, y2) + 1):
        the_map[x][y].blocked = False
        the_map[x][y].block_sight = False
        libtcod.map_set_properties(fov_map, x, y, True, True)


class Map:
    def __init__(self, tiles = [], rooms = [], entities = [], fov_map = None):
        self.tiles = tiles
        self.rooms = rooms
        self.entities = entities
        self.fov_map = fov_map
        if self.fov_map is None:
            self.fov_map = libtcod.map_new(constants.MAP_WIDTH, constants.MAP_HEIGHT)

        self.path_map = libtcod.path_new_using_map(self.fov_map)

    def create(self):
        self.tiles = [[ Tile(True)
                        for y in range(constants.MAP_HEIGHT) ]
                      for x in range(constants.MAP_WIDTH) ]

        rooms = self.rooms
        num_rooms = 0

        for r in range(constants.MAX_ROOMS):
            #random width and height
            w = libtcod.random_get_int(0, constants.ROOM_MIN_SIZE, constants.ROOM_MAX_SIZE)
            h = libtcod.random_get_int(0, constants.ROOM_MIN_SIZE, constants.ROOM_MAX_SIZE)
            #random position without going out of the boundaries of the the_map
            x = libtcod.random_get_int(0, 0, constants.MAP_WIDTH - w - 1)
            y = libtcod.random_get_int(0, 0, constants.MAP_HEIGHT - h - 1)

            #"Rect" class makes rectangles easier to work with
            new_room = Rect(x, y, w, h)

            #run through the other rooms and see if they intersect with this one
            failed = False
            for other_room in rooms:
                if new_room.intersect(other_room):
                    failed = True
                    break

            if not failed:
                #this means there are no intersections, so this room is valid

                #"paint" it to the the_map's tiles
                create_room(new_room, self.tiles, self.fov_map)

                if num_rooms == 0:
                    rooms.append(new_room)
                    num_rooms += 1
                    continue

                #center coordinates of new room, will be useful later
                (new_x, new_y) = new_room.center()

                #all rooms after the first:
                #connect it to the previous room with a tunnel

                #center coordinates of previous room
                (prev_x, prev_y) = rooms[num_rooms-1].center()

                #draw a coin (random number that is either 0 or 1)
                if libtcod.random_get_int(0, 0, 1) == 1:
                    #first move horizontally, then vertically
                    create_h_tunnel(prev_x, new_x, prev_y, self.tiles, self.fov_map)
                    create_v_tunnel(prev_y, new_y, new_x, self.tiles, self.fov_map)
                else:
                    #first move vertically, then horizontally
                    create_v_tunnel(prev_y, new_y, prev_x, self.tiles, self.fov_map)
                    create_h_tunnel(prev_x, new_x, new_y, self.tiles, self.fov_map)

                    #finally, append the new room to the list

                rooms.append(new_room)
                num_rooms += 1


    def get_random_position(self, blocked=False):
        x = libtcod.random_get_int(0, 0, constants.MAP_WIDTH - 1)
        y = libtcod.random_get_int(0, 0, constants.MAP_HEIGHT - 1)
        if self.tiles[x][y].blocked != blocked:
            return self.get_random_position(blocked)
        return (x, y)

    def is_blocked(self, x, y):
        #first test the the_map tile
        if self.tiles[x][y].blocked:
            return True

        #now check for any blocking entities
        for entity in self.entities:
            if entity.blocks and entity.x == x and entity.y == y:
                return True

        return False


def make_map():
    global stairs

    #fill the_map with "blocked" tiles
    the_map = Map()

    the_map.create()


    return the_map
