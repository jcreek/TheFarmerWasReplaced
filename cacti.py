import helpers

# Like other plants, cacti can be grown on soil and harvested as usual.

# However, they come in various sizes and have a strange sense of order.

# If you harvest a fully-grown cactus and all neighboring cacti are in sorted 
# order, it will also harvest all neighboring cacti recursively.

# A cactus is considered to be in sorted order if all neighboring cacti to the 
# North and East are fully grown and larger or equal in size and all neighboring 
# cacti to the South and West are fully grown and smaller or equal in size.

# The harvest will only spread if all adjacent cacti are fully grown and in sorted order.
# This means that if a square of grown cacti is sorted by size and you harvest one 
# cactus, it will harvest the entire square.

# A fully grown cactus will appear brown if it is not sorted. Once sorted, it will t
# urn green again.

# You will receive cactus equal to the number of harvested cacti squared. So if you 
# harvest n cacti simultaneously you will receive n**2 Items.Cactus.

# The size of a cactus can be measured with measure().
# It is always one of these numbers: 0,1,2,3,4,5,6,7,8,9.

# You can also pass a direction into measure(direction) to measure the neighboring 
# tile in that direction of the drone.

# You can swap a cactus with its neighbor in any direction using the swap() command.
# swap(direction) swaps the object under the drone with the object one tile in the 
# direction of the drone.

# Examples
# In each of these grids, all the cacti are in sorted order and the harvest will 
# spread over the entire field:
# 3 4 5    3 3 3    1 2 3    1 5 9
# 2 3 4    2 2 2    1 2 3    1 3 8
# 1 2 3    1 1 1    1 2 3    1 3 4

# In this grid, only the lower left cactus is in sorted order, which is not enough 
# for it to spread:
# 1 5 3
# 4 9 7
# 3 3 2

local_cacti = {}

COLUMNS_PER_DRONE = 1


def till_and_plant():
    if get_ground_type() != Grounds.Soil:
        till()
    helpers.harvest_if_possible()
    plant(Entities.Cactus)

def sort_local_region(start_x, end_x):
    world_size = get_world_size()
    swaps_made = True

    while swaps_made:
        swaps_made = False

        for x in range(start_x, end_x):
            helpers.move_to_coords(x, 0)

            for y in range(world_size):

                current = measure()
                
                # Compare left
                if x - 1 > 0:
                    left = measure(West)

                    # Only compare fully-grown cacti
                    if current != None and left != None:
                        if current < left:
                            swap(West)
                            swaps_made = True
                            current = measure()  # refresh after swap

                # Compare right
                if x + 1 < world_size:
                    right = measure(East)

                    # Only compare fully-grown cacti
                    if current != None and right != None:
                        if current > right:
                            swap(East)
                            swaps_made = True
                            current = measure()  # refresh after swap

                # Compare up
                if y + 1 < world_size:
                    up = measure(North)

                    if current != None and up != None:
                        if current > up:
                            swap(North)
                            swaps_made = True

                move(North)


def harvest_cacti_columns():
    world_size = get_world_size()
    start_x = get_pos_x()
    end_x = min(start_x + COLUMNS_PER_DRONE, world_size)

    if start_x >= world_size:
        return

    # Plant owned columns
    for x in range(start_x, end_x):
        helpers.move_to_coords(x, 0)
        for _ in range(world_size):
            till_and_plant()
            move(North)
    sort_local_region(start_x, end_x)

def spawn_drones():
    global COLUMNS_PER_DRONE

    world_size = get_world_size()
    drones = max_drones()

    COLUMNS_PER_DRONE = world_size // drones
    if COLUMNS_PER_DRONE < 1:
        COLUMNS_PER_DRONE = 1

    start_x = 0
    while start_x < world_size:
        helpers.move_to_coords(start_x, 0)
        spawn_drone(harvest_cacti_columns)
        start_x += COLUMNS_PER_DRONE

    # Also run in main drone
    harvest_cacti_columns()
    
    # Finally harvest one cactus to trigger a full harvest
    helpers.harvest_if_possible()