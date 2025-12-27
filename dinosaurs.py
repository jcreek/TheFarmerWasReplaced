import helpers

# Dinosaurs are ancient, majestic creatures that can be farmed for ancient bones.

# Unfortunately dinosaurs have gone extinct a long time ago, so the best we can do now is dressing up as one.
# For this purpose you have received the new dinosaur hat.

# The hat can be equipped with
# change_hat(Hats.Dinosaur_Hat)

# Unfortunately it doesn't quite look like on the advertisement...

# If you equip the dinosaur hat and have enough cactus, an apple will automatically be purchased and placed 
# under the drone.
# When the drone is over an apple and moves again, it will eat the apple and grow its tail by one. If you can 
# afford it, a new apple will be purchased and placed in a random location.
# The apple cannot spawn if something else is planted where it wants to be.

# The tail of the dinosaur will be dragged behind the drone filling the previous tiles the drone moved over. 
# If a drone tries to move on top of the tail move() will fail and return False. 
# The last segment of the tail will move out of the way during the move, so you can move onto it. However, 
# if the snake fills out the whole farm, you will not be able to move anymore. So you can check if the snake 
# is fully grown by checking if you can't move anymore.
# While wearing the dinosaur hat, the drone can't move over the farm border to get to the other side.

# Using measure() on an apple will return the position of the next apple as a tuple.

# next_x, next_y = measure()

# When the hat is unequipped again by equipping a different hat, the tail will be harvested.
# You will receive bones equal to the tail length squared. So for a tail of length n you will receive n**2 Items.Bone. 
# For Example:
# length 1 => 1 bone
# length 2 => 4 bones
# length 3 => 9 bones
# length 4 => 16 bones
# length 16 => 256 bones
# length 100 => 10000 bones

# The Dinosaur Hat is very heavy, so if you equip it, it will make move() take 400 ticks instead of 200. However, 
# each time you pick up an apple, the number of ticks used by move() is reduced by 3% (rounded down), because a 
# longer tail can help you move.

# The following loop prints the number of ticks used by move() after any number of apples:

# ticks = 400
# for i in range(100):
#     print("ticks after ", i, " apples: ", ticks)
#     ticks -= ticks * 0.03 // 1

# You only have one dinosaur hat, so only one drone can wear it.

# If you keep moving along the same path that covers the whole field, you can easily get a snake that covers the 
# whole field every time. It's not very efficient, but it works.
# Fully traversing a very large farm can take a long time and you might not actually need that many bones. Feel 
# free to use set_world_size() to change the size of the farm to something more convenient.

dumb_mode = True

last_move = None
next_x = -1
next_y = -1

OPPOSITE = {
    North: South,
    South: North,
    East: West,
    West: East
}

tail = []
tail_length = 0

def any_other_move_available():
    for d in [North, East, South, West]:
        if last_move != None and d == OPPOSITE[last_move]:
            continue
        if can_move(d):
            return True
    return False


def reset():
    global last_move
    global next_x
    global next_y
    global tail
    global tail_length

    last_move = None
    next_x = -1
    next_y = -1
    tail = []
    tail_length = 0

def safe_move(direction):
    global last_move
    global tail
    global tail_length

    # Prevent immediate reversal only if some other move exists
    if last_move != None and direction == OPPOSITE[last_move]:
        if any_other_move_available():
            return False

    if not can_move(direction):
        return False

    moved = move(direction)
    if moved:
        last_move = direction

        tail.insert(0, (get_pos_x(), get_pos_y()))
        if len(tail) > tail_length:
            tail.pop()

        return True

    return False


def flood_can_reach_tail(head, simulated_tail):
    # Breadth First Search - can head reach tail end if tail (except last) is blocked?
    world = get_world_size()

    if len(simulated_tail) == 0:
        return True

    blocked = set(simulated_tail[:-1])
    target = simulated_tail[-1]

    queue = [head]
    visited = {head}

    while queue:
        x, y = queue.pop(0)
        if (x, y) == target:
            return True

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < world and 0 <= ny < world:
                pos = (nx, ny)
                if (pos not in blocked) and (pos not in visited):
                    visited.add(pos)
                    queue.append(pos)

    return False


def move_one_step_towards(tx, ty):
    # A tiny greedy stepper to head toward a target (helps get unstuck)
    cx = get_pos_x()
    cy = get_pos_y()
    dx = tx - cx
    dy = ty - cy

    preferred = []

    if abs(dx) >= abs(dy):
        if dx > 0:
            preferred.append(East)
        elif dx < 0:
            preferred.append(West)
        if dy > 0:
            preferred.append(North)
        elif dy < 0:
            preferred.append(South)
    else:
        if dy > 0:
            preferred.append(North)
        elif dy < 0:
            preferred.append(South)
        if dx > 0:
            preferred.append(East)
        elif dx < 0:
            preferred.append(West)

    for d in preferred + [North, East, South, West]:
        if safe_move(d):
            return True

    return False


def clear_grid():
    columns_per_drone = get_world_size() // max_drones()
    for _ in range(columns_per_drone):
        for _ in range(get_world_size()):
            till()
            safe_move(North)
        safe_move(East)

def move_to_coords_avoiding_tail(x, y):
    if get_pos_x() == x and get_pos_y() == y:
        return

    while True:
        cx = get_pos_x()
        cy = get_pos_y()

        dx = x - cx
        dy = y - cy

        moved = False
        preferred = []

        if abs(dx) >= abs(dy):
            if dx > 0:
                preferred.append(East)
            elif dx < 0:
                preferred.append(West)

            if dy > 0:
                preferred.append(North)
            elif dy < 0:
                preferred.append(South)
        else:
            if dy > 0:
                preferred.append(North)
            elif dy < 0:
                preferred.append(South)

            if dx > 0:
                preferred.append(East)
            elif dx < 0:
                preferred.append(West)

        # Try the preferred direction, then any direction
        for d in preferred + [North, East, South, West]:
            if safe_move(d):
                moved = True
                break

        if not moved:
            # If we still have a tail, see if we can reach the tail end.
            if tail_length > 1 and len(tail) > 0:
                head = (get_pos_x(), get_pos_y())
                can_escape = flood_can_reach_tail(head, tail)

                if can_escape:
                    # We're not truly stuck, our greedy choices boxed us in.
                    # Unstick by walking toward the tail end a few steps.
                    tx, ty = tail[-1]
                    for _ in range(10):
                        if move_one_step_towards(tx, ty):
                            break
                    continue

            # Truly stuck sp let's harvest and restart
            change_hat(Hats.Straw_Hat)
            reset()
            change_hat(Hats.Dinosaur_Hat)
            return

        if get_pos_x() == x and get_pos_y() == y:
            return

def do_dumb():
    global tail_length
    
    # 32x32 grid 
    world_size = get_world_size()
    moving_up = True
    
    move(North)
    
    for x in range(world_size):
        for y in range(world_size - 2):
            if get_entity_type() == Entities.Apple:
                tail_length = tail_length + 1

            if moving_up:
                move(North)
                if get_entity_type() == Entities.Apple:
                    tail_length = tail_length + 1
            else: 
                move(South)
                if get_entity_type() == Entities.Apple:
                    tail_length = tail_length + 1
        move(East)
        if get_entity_type() == Entities.Apple:
            tail_length = tail_length + 1
        moving_up = not moving_up
    
    # now move back to 0,0
    move(South)
    if get_entity_type() == Entities.Apple:
            tail_length = tail_length + 1
    for x in range(world_size):
        move(West)
        if get_entity_type() == Entities.Apple:
            tail_length = tail_length + 1
    
    if tail_length > 900:
        harvest()

def process():
    global tail_length
    global dumb_mode

    reset()

    world_size = get_world_size()
    columns_per_drone = world_size // max_drones()
    i = 0

    while i < world_size:
        helpers.move_to_coords(i, 0)
        spawn_drone(clear_grid)
        i += columns_per_drone

    clear_grid()

    change_hat(Hats.Dinosaur_Hat)
    tail_length = 1
    
    if dumb_mode:
        while True:
            do_dumb()
    else:
        while True:
            next_x, next_y = measure()

            # Apple is eaten on the next move, tail grows by 1
            tail_length = tail_length + 1

            safe_move(North)
            move_to_coords_avoiding_tail(next_x, next_y)