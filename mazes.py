import helpers

# Items.Weird_Substance, which is obtained by fertilizing plants, has a strange effect on bushes. If the drone is over a bush and you call use_item(Items.Weird_Substance, amount) the bush will grow into a maze of hedges.
# The size of the maze depends on the amount of Items.Weird_Substance used (the second argument of the use_item() call).
# Without maze upgrades, using n Items.Weird_Substance will result in a nxn maze. Each maze upgrade level doubles the treasure, but it also doubles the amount of Items.Weird_Substance needed. 
# So to make a full field maze:

# plant(Entities.Bush)
# substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
# use_item(Items.Weird_Substance, substance)


# For some reason the drone can't fly over the hedges, even though they don't look that high.

# There is a treasure hidden somewhere in the hedge. Use harvest() on the treasure to receive gold equal to the area of the maze. (For example, a 5x5 maze will yield 25 gold.)

# If you use harvest() anywhere else the maze will simply disappear.

# get_entity_type() is equal to Entities.Treasure if the drone is over the treasure and Entities.Hedge everywhere else in the maze.

# Mazes do not contain any loops unless you reuse the maze (see below how to reuse a maze). So there is no way for the drone to end up in the same position again without going back.

# You can check if there is a wall by trying to move through it. 
# move() returns True if it succeeded and False otherwise.

# can_move() can be used to check if there is a wall without moving.

# If you have no idea how to get to the treasure, take a look at Hint 1. It shows you how to approach a problem like this.

# Using measure() anywhere in the maze returns the position of the treasure.
# x, y = measure()

# For an extra challenge you can also reuse the maze by using the same amount of Items.Weird_Substance on the treasure again. 
# This will collect the treasure and spawn a new treasure at a random position in the maze.

# Each time the treasure is moved, some of the maze's walls may be randomly removed. So reused mazes can contain loops.

# Note that loops in the maze make it much more difficult because it means that you can get to the same location again without moving back.
# Reusing a maze doesn't give you more gold than just harvesting and spawning a new maze.
# This is 100% an extra challenge that you can just skip.
# It's only worth it if the extra information and the shortcuts help you solve the maze faster.

# The treasure can be relocated up to 300 times. After that, using weird substance on the treasure won't increase the gold in it anymore and it won't move anymore.

# ---

# Here's a general approach to solving the problem:

# Create a maze and imagine that you are the drone.

# Think about how you would try to find the treasure if you were in the maze.

# Write down your strategy step by step so that someone else could follow it without thinking.

# Now try translating your steps into code.

# As long as there are no loops: All the walls are really just one large connected wall. If you follow the wall, it will lead you through the whole maze.
# This approach requires very little code and you do not need to keep track of where you have already been. Around 10 lines of code is all you need.

# Instead of moving the drone in absolute directions like east or west it can be very useful to move the drone in relative directions like "turn right" or "turn left". To do this you need to keep track of which way the drone is currently moving. The drone never actually rotates, but you can still keep a "virtual" rotation in code.
# The following index trick is helpful for this:

# directions = [North, East, South, West]
# index = 0

# Use % 4 to allow it to rotate "around the circle", so that after West it wraps back to North.
# # turn right
# index = (index + 1) % 4

# # turn left
# index = (index - 1) % 4

# move(directions[index])

# If you can't solve it, you can always make your life easy and do it less efficiently. 
# Solving a 1x1 maze is trivial.

visited_cells = {} # maze[(x, y)] = entity type
path_back = [] # stack of previous positions to backtrack to

directions = [North, East, South, West]
direction_index = 0

treasure_not_yet_found = True

def reset_state():
    global visited_cells
    global path_back
    global direction_index
    global treasure_not_yet_found
    
    visited_cells = {}
    path_back = []
    direction_index = 0
    treasure_not_yet_found = True

def record_current_cell_visited():
    visited_cells[(get_pos_x(), get_pos_y())] = get_entity_type()


def attempt_move(direction):
    # Returns True if moved, False otherwise.
    return move(direction)


def not_yet_visited_cell(direction):
    (x, y) = helpers.get_coords_from_direction(direction)
    position = (x, y)
    if position in visited_cells:
        return False
    return True


def can_move_in_direction(dir_index_offset):
    # Use % 4 to allow it to rotate "around the circle", so that after West it wraps back to North.
    d = directions[(direction_index + dir_index_offset) % 4]
    return can_move(d) and not_yet_visited_cell(d)


def can_move_forward():
    return can_move_in_direction(0)


def can_move_left():
    return can_move_in_direction(-1)


def can_move_right():
    return can_move_in_direction(1)


def plant_maze():
    plant(Entities.Bush)
    substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
    use_item(Items.Weird_Substance, substance)

def check_cell_for_treasure():
    global treasure_not_yet_found

    # get_entity_type() is equal to Entities.Treasure if the drone is over the treasure and Entities.Hedge everywhere else in the maze.
    if get_entity_type() == Entities.Treasure:
        harvest()
        treasure_not_yet_found = False


def move_explore(dir_index_offset):
    # Move into an unvisited neighbor (exploration) and push current position onto stack before moving, so we can backtrack later
    global direction_index
    global path_back

    # Save where we are so we can come back
    path_back.append((get_pos_x(), get_pos_y()))

    # Turn (virtually) and move
    direction_index = (direction_index + dir_index_offset) % 4
    moved = attempt_move(directions[direction_index])

    if moved:
        record_current_cell_visited()
    else:
        # Move failed unexpectedly; undo the push
        path_back.pop()


def backtrack_one_step():
    # Go back to the previous position on the current path

    global path_back
    global direction_index

    if not path_back:
        # Nowhere left to go
        return False

    (x, y) = path_back.pop()

    # Set direction_index to face the target before moving there
    cx = get_pos_x()
    cy = get_pos_y()

    if x == cx and y == cy + 1:
        direction_index = 0  # North
    elif x == cx + 1 and y == cy:
        direction_index = 1  # East
    elif x == cx and y == cy - 1:
        direction_index = 2  # South
    elif x == cx - 1 and y == cy:
        direction_index = 3  # West
    else:
        # Fallback
        helpers.move_to_coords(x, y)
        record_current_cell_visited()
        return True

    moved = attempt_move(directions[direction_index])
    if moved:
        record_current_cell_visited()
    return moved


def navigate_maze():
    global treasure_not_yet_found
    
    clear()
    reset_state()

    plant_maze()
    record_current_cell_visited()
    check_cell_for_treasure()

    while treasure_not_yet_found:
        if can_move_forward():
            move_explore(0)
        elif can_move_left():
            move_explore(-1)
        elif can_move_right():
            move_explore(1)
        else:
            # No unvisited neighbors so backtrack
            if not backtrack_one_step():
                print('Explored everything reachable and did not find treasure')
                break

        check_cell_for_treasure()