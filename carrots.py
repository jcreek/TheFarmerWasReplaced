import helpers

# Before you can plant carrots with plant(Entities.Carrot), you have to till the soil. This will change the ground to Grounds.Soil. To till the soil, simply call till(). Calling till() again will change it back to Grounds.Grassland.

# Planting carrots costs wood and hay. These items will be automatically removed when calling plant(Entities.Carrot).

def till_and_plant():
    if get_ground_type() != Grounds.Soil:
        till()
    if get_entity_type() == Entities.Carrot:
        helpers.harvest_if_possible()
        plant(Entities.Carrot)
    else:
        plant(Entities.Carrot)

def harvest_carrots():
    for x in range(get_world_size()):
        for y in range(get_world_size()):
            till_and_plant()
            move(North)
        move(East)