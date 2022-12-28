import os
import keyboard
import time
import random

def initialisation():
    refresh_time_init = 0.5
    apples_list = []
    walls_list = []
    score = 0
    level = 0
    apple_probability_init = 0.08
    wall_probability_init = 0.04

    return {'refresh_time_init': refresh_time_init, 
            'apples_list': apples_list,
            'walls_list': walls_list,
            'score': score,
            'level': level,
            'apple_probability_init': apple_probability_init,
            'wall_probability_init': wall_probability_init
            }


# show the start screen
def start_game():
    os.system("cls")

    with open('starting_page.txt', 'r') as f:
        print(f.read())
    
    while True:
        if keyboard.is_pressed("space"):
            break

# show the end screen
def end_game(snake_list, walls_list):
    
    restart = False
    
    if snake_list[0] in walls_list:
        os.system("cls")
    
        with open('end_page.txt', 'r') as f:
            print(f.read())
        
        while True:
            if keyboard.is_pressed("space"):
                restart = True        
                break
                
            if keyboard.is_pressed("escape"):
                exit()

    return restart
    


# calcul of probability
def probability(init, factor, difficulty):
    if factor > 0:
        return init*(factor+difficulty)
    else:
        return init

def element_positions(element_list, columns_number, element_probability):
    
    element_list_next_step = []
    
    for element_coor in element_list:
        if element_coor[1]-1 >= 0:
            element_list_next_step.append([element_coor[0], element_coor[1]-1])
    element_list = element_list_next_step

    for i in range(columns_number):
        if random.random() < element_probability:
            element_list += [[i, lines_number-1]]
    
    return element_list

def down_direction(snake_list, apples_list, apple_probability, walls_list, wall_probability, columns_number):
    
    snake_len = len(snake_list)
    snake_list[0] = [snake_list[0][0], snake_list[0][1]]
    for i in range (snake_len-1, 0, -1):
        snake_list[i] = [snake_list[i-1][0], snake_list[i-1][1]-1]
    
    apples_list = element_positions(apples_list, columns_number, apple_probability)
    walls_list = element_positions(walls_list, columns_number, wall_probability)
    
    return [snake_list, apples_list, walls_list]

def right_direction(snake_list):
    
    snake_len = len(snake_list)
    for i in range (snake_len-1, 0, -1):
        snake_list[i] = snake_list[i-1]
    snake_list[0] = [snake_list[0][0]+1, head_snake_y]

    snake_list = manage_borders(snake_list)

    return snake_list

def left_direction(snake_list):

    snake_len = len(snake_list)
    for i in range (snake_len-1, 0, -1):
        snake_list[i] = snake_list[i-1]
    snake_list[0] = [snake_list[0][0]-1, head_snake_y]
    
    snake_list = manage_borders(snake_list)

    return snake_list
    
def manage_borders(snake_list):
    if snake_list[0][0] > columns_number-1:
        snake_list[0][0] = 0
    
    if snake_list[0][0] < 0:
        snake_list[0][0] = columns_number-1
    
    return snake_list

def print_screen(lines_number, columns_number, snake_list, apples_list, walls_list, score, level):
    lines_list = []
    for column in range(lines_number):
        line_str = ""
                
        for line in range (columns_number):
            test_snake = False
            test_apple = False
            test_wall = False
            for snake_coor_list in snake_list:
                if snake_coor_list[0] == line and snake_coor_list[1] == column:
                    test_snake = True
            for apple_coor_list in apples_list:
                if apple_coor_list[0] == line and apple_coor_list[1] == column:
                    test_apple = True
            for wall_coor_list in walls_list:
                if wall_coor_list[0] == line and wall_coor_list[1] == column:
                    test_wall = True
            if test_snake:
                line_str += snake_char
            elif test_wall:
                line_str += wall_char
            elif test_apple:
                line_str += apple_char
            else: 
                line_str += blank_char
            
        lines_list += [line_str]

    os.system("cls")
    print('=== score : ' + str(score) + ' === level : ' + str(level) + ' ===')

    for i in lines_list:
        print(i)

def level_calculator(entry_score):
    return entry_score//10

def score_calculator(score, snake_list, apples_list):
    if snake_list[0] in apples_list:
        score += 1
        apples_list.remove(snake_list[0])
    return score

def directions(direction_init, refresh_time):
    element_direction=direction_init
    count = 0
    while count < refresh_time:
        if keyboard.is_pressed("escape"):
            break
        
        if keyboard.is_pressed("down"):
            element_direction = "down"
        
        if keyboard.is_pressed("left"):
            if direction_init != "right":
                element_direction = "left"
        
        if keyboard.is_pressed("right"):
            if direction_init != "left":
                element_direction = "right"
        
        time.sleep(0.1)
        count += 0.1
    
    return element_direction



start_game()

init = initialisation()
columns_number = 40
lines_number = 25
snake_len = 14 
head_snake_x = lines_number//2
head_snake_y = snake_len
refresh_time = init['refresh_time_init']
direction = "down"
snake_list = [[head_snake_x, head_snake_y-i] for i in range(snake_len)]
snake_char = chr(0x2592)
wall_char = chr(0x2588)
apple_char = 'o'
blank_char = ' '
apples_list = init['apples_list']
walls_list = init['walls_list']
score = init['score']
level = init['level']
apple_probability_init = init['apple_probability_init']
wall_probability_init = init['wall_probability_init']

while True:

    # calcul of probability to have an apple and a wall
    apple_probability = probability(init['apple_probability_init'], level, 0.1)
    wall_probability = probability(init['wall_probability_init'], level, 0.8)
    
    # calcul coordonates of elments
    if direction == "down":        
        next_step = down_direction(snake_list, apples_list, apple_probability, walls_list, wall_probability, columns_number)
        snake_list = next_step[0]
        apples_list = next_step[1]
        walls_list = next_step[2]

    if direction == "left":
        snake_list = left_direction(snake_list)
        
    if direction == "right":
        snake_list = right_direction(snake_list)
    
    # calcul of score and level
    score = score_calculator(score, snake_list, apples_list)
    level = level_calculator(score)
    
    # print on screen all elements
    print_screen(lines_number, columns_number, snake_list, apples_list, walls_list, score, level)

    if refresh_time>0.1:
        refresh_time = init['refresh_time_init']-(level*0.1)

    direction = directions(direction, refresh_time)

    if keyboard.is_pressed("escape"):
        break

    # manage the end of the game
    restart = end_game(snake_list, walls_list)
    if restart:
        init = initialisation()
        columns_number = 40
        lines_number = 25
        snake_len = 14 
        head_snake_x = lines_number//2
        head_snake_y = snake_len
        refresh_time = init['refresh_time_init']
        direction = "down"
        snake_list = [[head_snake_x, head_snake_y-i] for i in range(snake_len)]
        snake_char = chr(0x2592)
        wall_char = chr(0x2588)
        apple_char = 'o'
        blank_char = ' '
        apples_list = init['apples_list']
        walls_list = init['walls_list']
        score = init['score']
        level = init['level']
        apple_probability_init = init['apple_probability_init']
        wall_probability_init = init['wall_probability_init']
    
