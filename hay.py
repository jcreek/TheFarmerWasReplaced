import helpers

def till_and_plant():
    if get_ground_type() != Grounds.Grassland:
        till()
    if get_entity_type() == Entities.Grass:
        helpers.harvest_if_possible()

def harvest_hay():
    for x in range(get_world_size()):
        for y in range(get_world_size()):
            till_and_plant()
            move(North)
        move(East)