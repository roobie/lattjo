CONFUSE_NUM_TURNS = 10

import libtcodpy as libtcod

class BasicAI:
    def update(self):
        entity = self.owner
        self.owner.move(
                libtcod.random_get_int(0, -1, 1),
                libtcod.random_get_int(0, -1, 1))


class BasicMonster:
    #AI for a basic monster.
    def take_turn(self):
        #a basic monster takes its turn. if you can see it, it can see you
        monster = self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

            #move towards player if far away
            if monster.distance_to(player) >= 2:
                monster.move_towards(player.x, player.y)

            #close enough, attack! (if the player is still alive.)
            elif player.fighter.hp > 0:
                monster.fighter.attack(player)

class ConfusedMonster:
    #AI for a temporarily confused monster (reverts to previous AI after a while).
    def __init__(self, old_ai, num_turns=CONFUSE_NUM_TURNS):
        self.old_ai = old_ai
        self.num_turns = num_turns

    def take_turn(self):
        if self.num_turns > 0:  #still confused...
            #move in a random direction, and decrease the number of turns confused
            self.owner.move(
                libtcod.random_get_int(0, -1, 1),
                libtcod.random_get_int(0, -1, 1))
            self.num_turns -= 1

        else:
            #restore the previous AI
            self.owner.ai = self.old_ai
            message('The ' +
                    self.owner.name +
                    ' is no longer confused!',
                    libtcod.red)
