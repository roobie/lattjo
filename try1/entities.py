
import libtcodpy as libtcod
import game_types
import ai_types

libtcod.namegen_parse('data/namegen/jice_celtic.cfg')

def get(what, world, x=0, y=0, name=None, gender=None):
    if gender is None:
        if libtcod.random_get_int(0, 0, 1) == 1:
            gender = 'female'
            if name is None:
                name = libtcod.namegen_generate('Celtic female')
        else:
            gender = 'male'
            if name is None:
                name = libtcod.namegen_generate('Celtic male')

    if what == 'human':
        return game_types.Entity(
            x, y, 'H', name, libtcod.white,
            blocks=True,
            gender=gender,
            fighter=game_types.Fighter(
                hp=100, defense=1, power=2, xp=0, death_function=None),
            ai=ai_types.BasicAI(world))
