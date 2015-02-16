
import constants

class TileMap:
    def __init__(self, width = 0, height = 0, tiles = None):
        "A tile map"
        self.width = width
        self.height = height
        self.tiles = tiles or [[ Tile((x, y), [])
                                 for y in range(height) ]
                               for x in range(width) ]

        def __getitem__(self, key):
            (x, y) = key
            return self.tiles[x][y]

        def __getitem__(self, key, value):
            (x, y) = key
            self.tiles[x][y] = value


class Tile:
    def __init__(self, pos, blocking=True, data = []):
        "A tile"
        self.pos = pos
        self.data = data
