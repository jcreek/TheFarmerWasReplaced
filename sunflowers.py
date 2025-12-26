import helpers

# Sunflowers collect the power of the sun. You can harvest that power. 

# Planting them works exactly like planting carrots or pumpkins. 

# Harvesting a grown sunflower yields power.
# If there are at least 10 sunflowers on the farm and you harvest the one with the 
# largest number of petals you get 8 times more power!
# If you harvest a sunflower while there is another sunflower with more petals, the 
# next sunflower you harvest will also only give you the normal amount of power (not the 8x bonus).

# measure() returns the number of petals of the sunflower under the drone.
# Sunflowers have at least 7 and at most 15 petals.
# They can already be measured before they are fully grown.

# Several sunflowers can have the same number of petals so there can also be several sunflowers with 
# the largest number of petals. In this case, it doesn't matter which one of them you harvest.

# As long as you have power the drone will use it to run twice as fast. 
# It consumes 1 power every 30 actions (like moves, harvests, plants...)
# Executing other code statements can also use power but a lot less than drone actions.

# In general, everything that is sped up by speed upgrades is also sped up by power.
# Anything sped up by power also uses power proportional to the time it takes to execute it, ignoring speed upgrades.

initial_planting_performed = False

def till_and_plant(sunflowers):
    if get_ground_type() != Grounds.Soil:
        till()
    use_item(Items.Fertilizer)
    plant(Entities.Sunflower)
    sunflowers[(get_pos_x(), get_pos_y())] = measure()
    
def find_sunflower_with_most_petals_and_harvest(sunflowers):
    best_petals = -1
    best_pos = None

    for pos in sunflowers:
        petals = sunflowers[pos]
        if petals > best_petals:
            best_petals = petals
            best_pos = pos

    if best_pos == None:
        print('best_pos is None')
        return

    best_x = best_pos[0]
    best_y = best_pos[1]

    helpers.move_to_coords(best_x, best_y)
    helpers.harvest_if_possible()

    sunflowers.pop(best_pos)
    till_and_plant(sunflowers)

def handle_initial_planting(sunflowers):
    for x in range(2):
        for y in range(5):
            till_and_plant(sunflowers)
            move(North)
        
        move(East)
        for i in range(5):
            move(South)

def harvest_sunflowers(sunflowers):
    global initial_planting_performed # Needed to be able to use the variable from the module
    
    if initial_planting_performed == False:
        handle_initial_planting(sunflowers)
        initial_planting_performed = True

    for _ in range(100000):
        find_sunflower_with_most_petals_and_harvest(sunflowers)