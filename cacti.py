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

def till_and_plant(cacti):
    if get_ground_type() != Grounds.Soil:
        till()
    helpers.harvest_if_possible()
    plant(Entities.Cactus)
    cacti[(get_pos_x(), get_pos_y())] = measure()

def sort_cacti(cacti):
    swaps_made = True
    world_size = get_world_size()
    
    while swaps_made:
        number_of_swaps_made_this_loop = 0
        # Go through the cacti array, each entry stores the size at the x,y
        for x in range(world_size):
            for y in range(world_size):
                # Check the cactus to the right
                if x+1 < world_size and cacti[(x,y)] > cacti[(x+1,y)]:
                    helpers.move_to_coords(x,y)
                    swap(East)
                    temp_cactus = cacti[(x,y)]
                    cacti[(x,y)] = cacti[(x+1,y)]
                    cacti[(x+1,y)] = temp_cactus
                    number_of_swaps_made_this_loop += 1
                
                # Check the cactus above
                if y+1 < world_size and cacti[(x,y)] > cacti[(x,y+1)]:
                    helpers.move_to_coords(x,y)
                    swap(North)
                    temp_cactus = cacti[(x,y)]
                    cacti[(x,y)] = cacti[(x,y+1)]
                    cacti[(x,y+1)] = temp_cactus
                    number_of_swaps_made_this_loop += 1
        
        if number_of_swaps_made_this_loop == 0:
            swaps_made = False

def harvest_cacti(cacti):
    for x in range(get_world_size()):
        for y in range(get_world_size()):
            till_and_plant(cacti)
            move(North)
        move(East)
    
    sort_cacti(cacti)
    
    helpers.harvest_if_possible()