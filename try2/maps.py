import libtcodpy as libtcod

from map_types import Rect
import tiles as tilez
import constants

class Map:
    def __init__(self, tile_map = None, rooms = [], entities = [], fov_map = None):
        "A map"
        self.tile_map = tile_map or tilez.TileMap(constants.MAP_WIDTH, constants.MAP_HEIGHT)
        self.rooms = rooms
        self.entities = entities
        self.fov_map = fov_map or libtcod.map_new(constants.MAP_WIDTH, constants.MAP_HEIGHT)
        self.path_map = libtcod.path_new_using_map(self.fov_map)

    def create_room(self, room):
        tiles = self.tile_map.tiles
        fov_map = self.fov_map

        self.rooms.append(room)

        #go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                tiles[x][y].blocked = False
                tiles[x][y].block_sight = False
                libtcod.map_set_properties(fov_map, x, y, True, True)

    def create_h_tunnel(self, x1, x2, y):
        tiles = self.tile_map.tiles
        fov_map = self.fov_map
        #horizontal tunnel. min() and max() are used in case x1>x2
        for x in range(min(x1, x2), max(x1, x2) + 1):
            tiles[x][y].blocked = False
            tiles[x][y].block_sight = False
            libtcod.map_set_properties(fov_map, x, y, True, True)

    def create_v_tunnel(self, y1, y2, x):
        tiles = self.tile_map.tiles
        fov_map = self.fov_map
        #vertical tunnel
        for y in range(min(y1, y2), max(y1, y2) + 1):
            tiles[x][y].blocked = False
            tiles[x][y].block_sight = False
            libtcod.map_set_properties(fov_map, x, y, True, True)



def random():
    m = Map()
    tiles = m.tile_map.tiles
    fov_map = m.fov_map
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
        for other_room in m.rooms:
            if new_room.intersect(other_room):
                failed = True
                break

        if not failed:
            #this means there are no intersections, so this room is valid

            #"paint" it to the the_map's tiles
            m.create_room(new_room)

            if num_rooms == 0:
                num_rooms += 1
                continue

            #center coordinates of new room, will be useful later
            (new_x, new_y) = new_room.center()

            #all rooms after the first:
            #connect it to the previous room with a tunnel

            #center coordinates of previous room
            (prev_x, prev_y) = m.rooms[num_rooms-1].center()

            if libtcod.random_get_int(0, 0, 1) == 1:
                #first move horizontally, then vertically
                m.create_h_tunnel(prev_x, new_x, prev_y, self.tiles, self.fov_map)
                m.create_v_tunnel(prev_y, new_y, new_x, self.tiles, self.fov_map)
            else:
                #first move vertically, then horizontally
                m.create_v_tunnel(prev_y, new_y, prev_x, self.tiles, self.fov_map)
                m.create_h_tunnel(prev_x, new_x, new_y, self.tiles, self.fov_map)

            #finally, append the new room to the list

            num_rooms += 1

    # return the map instance
    return m
