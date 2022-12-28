import os
import keyboard
import time
import random

columns_number = 40
lines_number = 25
snake_len = 14 
head_snake_x = lines_number//2
head_snake_y = snake_len
refresh_time_init = 0.5
refresh_time = refresh_time_init
direction = "down"
snake_list = [[head_snake_x, head_snake_y-i] for i in range(snake_len)]
apple_probability_init = 0.08
wall_probability_init = 0.01
apples_list = []
walls_list = []
score = 0
level = 0

os.system("cls")

with open('starting_page.txt', 'r') as f:
    # lit le contenu du fichier et l'affiche à l'aide de print()
    print(f.read())
 
while True:
    if keyboard.is_pressed("space"):
        break


while True:

    if level > 0:
        apple_probability = apple_probability_init/(level*1.1)
        wall_probability = wall_probability_init+(level*0.01)
    else:
        apple_probability = apple_probability_init
        wall_probability = wall_probability_init
    
    if direction == "down":        
        snake_list[0] = [snake_list[0][0], head_snake_y]
        for i in range (snake_len-1, 0, -1):
            snake_list[i] = [snake_list[i-1][0], snake_list[i-1][1]-1]
        
        apples_list_next_step = []
        for apple_coor in apples_list:
            if apple_coor[1]-1 >= 0:
                apples_list_next_step.append([apple_coor[0], apple_coor[1]-1])
        apples_list = apples_list_next_step

        for i in range(columns_number):
            if random.random() < apple_probability:
                apples_list += [[i, lines_number-1]]

        walls_list_next_step = []
        for wall_coor in walls_list:
            if wall_coor[1]-1 >= 0:
                walls_list_next_step.append([wall_coor[0], wall_coor[1]-1])
        walls_list = walls_list_next_step

        for i in range(columns_number):
            if random.random() < wall_probability:
                walls_list += [[i, lines_number-1]]


    if direction == "left":
        for i in range (snake_len-1, 0, -1):
            snake_list[i] = snake_list[i-1]
        snake_list[0] = [snake_list[0][0]-1, head_snake_y]
        
    if direction == "right":
        for i in range (snake_len-1, 0, -1):
            snake_list[i] = snake_list[i-1]
        snake_list[0] = [snake_list[0][0]+1, head_snake_y]
    
    if snake_list[0][0] > columns_number-1:
        snake_list[0][0] = 0
    
    if snake_list[0][0] < 0:
        snake_list[0][0] = columns_number-1




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
                line_str += chr(0x2592)
            elif test_wall:
                line_str += chr(0x2588)
            elif test_apple:
                line_str += 'o'
            else: 
                line_str += ' '
            
        lines_list += [line_str]

    if snake_list[0] in apples_list:
        score += 1
        apples_list.remove(snake_list[0])

    level = score//10

    os.system("cls")
    print('=== score : ' + str(score) + ' === level : ' + str(level) + ' ===')

    for i in lines_list:
        print(i)

    if snake_list[0] in walls_list:
        print("you lose !!!")
        exit()

    
    if refresh_time>0.1:
        refresh_time = refresh_time_init-(level*0.1)

    count = 0
    while count < refresh_time:
        if keyboard.is_pressed("escape"):
            break
        
        if keyboard.is_pressed("down"):
            direction = "down"
        
        if keyboard.is_pressed("left"):
            if direction != "right":
                direction = "left"
        
        if keyboard.is_pressed("right"):
            if direction != "left":
                direction = "right"
        
        time.sleep(0.1)
        count += 0.1

    if keyboard.is_pressed("escape"):
        break
