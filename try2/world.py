
import maps as mapz

class World:
    def __init__(self, maps = []):
        "A world"
        if not maps or len(maps) == 0:
            maps = [mapz.random()]
        this.current_map = maps[0]
        this.maps = maps
