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

def harvest_hay_columns():
    columns_per_drone = get_world_size() / max_drones()
    for x in range(columns_per_drone):
        for y in range(get_world_size()):
            till_and_plant()
            move(North)
        move(East)

def spawn_drones():
    world_size = get_world_size()
    
    columns_per_drone = world_size / max_drones()
    
    i = 0
    while i < world_size:
        helpers.move_to_coords(i,0)
        spawn_drone(harvest_hay_columns)
        i += columns_per_drone
    
def harvest_hay_with_multiple_drones():
    spawn_drones()
    harvest_hay_columns()
