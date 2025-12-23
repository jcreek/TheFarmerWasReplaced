def is_even(n):
    return n % 2 == 0

def is_odd(n):
    return not is_even(n)

def harvest_if_possible():
    if num_items(Items.Water) > 1:
         use_item(Items.Water)
    if can_harvest():
            harvest()

def move_to_coords(x, y):
    current_x = get_pos_x()
    current_y = get_pos_y()
    
    if current_x == x and current_y == y:
        return
    
    move_east = True
    move_north = True
    
    if current_x > x:
        move_east = False
    if current_y > y:
        move_north = False
    
    for _ in range(abs(current_x - x)):
        if move_east:
            move(East)
        else:
            move(West)
    
    for _ in range(abs(current_y - y)):
        if move_north:
            move(North)
        else:
            move(South)