import hay
import wood
import carrots
import pumpkins
import sunflowers
import cacti
import mazes

sunflowers_array = {} # sunflowers_array[(x, y)] = petals
cactus_array = {} # cactus_array[(x, y)] = size

num_loops = 10

def run_loop(number_of_loops, label, fn):
    clear()
    for i in range(number_of_loops):
        # print(label, i+1)
        fn()

def harvest_sunflowers_wrapper():
    # this wrapper function is needed as the game doesn't support llambdas,
    # which are needed as we're passing an argument into the function
    sunflowers.harvest_sunflowers(sunflowers_array)

def harvest_cacti_wrapper():
    # this wrapper function is needed as the game doesn't support llambdas,
    # which are needed as we're passing an argument into the function
    cacti.harvest_cacti(cactus_array)

clear()

while True:
    run_loop(num_loops, 'hay', hay.harvest_hay_with_multiple_drones)
    run_loop(num_loops, 'wood', wood.harvest_wood)
    run_loop(num_loops * 20, 'carrots', carrots.harvest_carrots)
    run_loop(num_loops, 'pumpkins', pumpkins.harvest_pumpkins)
    sunflowers.initial_planting_performed = False
    run_loop(num_loops * 50, 'sunflowers', harvest_sunflowers_wrapper)
    run_loop(1, 'cacti', harvest_cacti_wrapper)
    run_loop(1, "maze", mazes.navigate_maze)
