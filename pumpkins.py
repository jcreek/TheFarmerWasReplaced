import helpers

# Pumpkins grow like carrots on tilled soil. Planting them costs carrots.

# When all the pumpkins in a square are fully grown, they will grow together to form a giant pumpkin. Unfortunately, pumpkins have a 20% chance of dying once they are fully grown, so you will need to replant the dead ones if you want them to merge. 

# When a pumpkin dies, it leaves behind a dead pumpkin that won't drop anything when harvested. Planting a new plant in its place automatically removes the dead pumpkin, so there is no need to harvest it. can_harvest() always returns False on dead pumpkins.

# The yield of a giant pumpkin depends on the size of the pumpkin.

# A 1x1 pumpkin yields 1*1*1 = 1 pumpkins.
# A 2x2 pumpkin yields 2*2*2 = 8 pumpkins instead of 4.
# A 3x3 pumpkin yields 3*3*3 = 27 pumpkins instead of 9.
# A 4x4 pumpkin yields 4*4*4 = 64 pumpkins instead of 16.
# A 5x5 pumpkin yields 5*5*5 = 125 pumpkins instead of 25.
# A nxn pumpkin yields n*n*6 pumpkins for n >= 6.

# It's a good idea to get at least 6x6 size pumpkins to get the full multiplier. 

# This means that even if you plant a pumpkin on every tile in a square, one of the pumpkins may die and prevent the mega pumpkin from growing.

def till_and_plant():
    if get_ground_type() != Grounds.Soil:
        till()
    if get_entity_type() == Entities.Pumpkin:
        helpers.harvest_if_possible()
        plant(Entities.Pumpkin)
    else:
        helpers.harvest_if_possible()
        plant(Entities.Pumpkin)

def clear_bad_pumpkins():
    for x in range(get_world_size()):
        for y in range(get_world_size()):
            if get_entity_type() == Entities.Dead_Pumpkin:
                # Planting a new plant in its place automatically removes the dead pumpkin, so there is no need to harvest it. 
                plant(Entities.Pumpkin)
            move(North)
        move(East)
        
def harvest_pumpkins():
    for x in range(get_world_size()):
        for y in range(get_world_size()):
            till_and_plant()
            move(North)
        move(East)

    for i in range(5):
        # 5 because the decay rate is 20% so 5 passes should usually clear all bad pumpkinks to maximise harvest
        clear_bad_pumpkins()

def harvest_pumpkin_columns():
    columns_per_drone = get_world_size() / max_drones()
    start_x = get_pos_x()
    for x in range(columns_per_drone):
        for y in range(get_world_size()):
            till_and_plant()
            move(North)
        move(East)
    
    helpers.move_to_coords(start_x, 0)
    for i in range(5):
        # 5 because the decay rate is 20% so 5 passes should usually clear all bad pumpkinks to maximise harvest
        clear_bad_pumpkin_columns()
    

def clear_bad_pumpkin_columns():
    columns_per_drone = get_world_size() / max_drones()
    for x in range(columns_per_drone):
        for y in range(get_world_size()):
            if get_entity_type() == Entities.Dead_Pumpkin:
                # Planting a new plant in its place automatically removes the dead pumpkin, so there is no need to harvest it. 
                plant(Entities.Pumpkin)
            move(North)
        move(East)

def spawn_drones():
    world_size = get_world_size()
    
    columns_per_drone = world_size / max_drones()
    
    i = 0
    while i < world_size:
        helpers.move_to_coords(i,0)
        spawn_drone(harvest_pumpkin_columns)
        i += columns_per_drone
    
def harvest_pumpkins_with_multiple_drones():
    spawn_drones()
    harvest_pumpkin_columns()