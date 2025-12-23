import helpers
import hay

# Trees are a better way to get wood than bushes. They give 5 wood each. Like bushes, they can be planted on grass or soil.

# Trees like to have some space and planting them right next to each other will slow down their growth. The growing time is doubled for each tree that is on a tile directly to the north, east, west or south of it. So if you plant trees on every tile, they will take 2*2*2*2 = 16 times longer to grow.

def till_and_plant():
    if get_ground_type() != Grounds.Grassland:
        till()
    if get_entity_type() == Entities.Tree or get_entity_type() == Entities.Bush:
        helpers.harvest_if_possible()
        plant(Entities.Tree)
    else:
        helpers.harvest_if_possible()
        plant(Entities.Tree)

def harvest_wood():
    for x in range(get_world_size()):
        for y in range(get_world_size()):
            if helpers.is_even(get_pos_x()) and helpers.is_even(get_pos_y()):
                till_and_plant()
            elif helpers.is_odd(get_pos_x()) and helpers.is_odd(get_pos_y()):
                till_and_plant()
            else:
                hay.till_and_plant()
            move(North)
        move(East)