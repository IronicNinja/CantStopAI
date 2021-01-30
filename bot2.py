import numpy as np
import pygame
import sys
import math
import random

#pylint: skip-file

pygame.init()
res = (720, 720) 
screen = pygame.display.set_mode(res) 
SCREEN_COLOR = (60, 25, 60)
screen.fill(SCREEN_COLOR)
color = (255,255,255) 
color_light = (170,170,170) 
color_dark = (100,100,100) 
 
width = screen.get_width() 
height = screen.get_height() 
myfont = pygame.font.SysFont('Corbel', 30) 

### INIT BOARD LOGIC
player_A = {k: 0 for k in range(2, 13)}
player_B = {k: 0 for k in range(2, 13)}
board_end = [3, 5, 7, 9, 11, 13, 11, 9, 7, 5, 1]

r = 0
player_pos_list = {'A': [], 'B': []}
for num in player_A:
    A_text = myfont.render(f"{player_A[num]}", True, color)
    B_text = myfont.render(f"{player_B[num]}", True, color)
    pos_A = [width/18*r+width/6, height/2-height/3, width/18, height/12]
    pos_B = [width/18*r+width/6, height/2-height/4, width/18, height/12]
    screen.blit(A_text, pos_A)
    screen.blit(B_text, pos_B)
    player_pos_list['A'].append(pos_A)
    player_pos_list['B'].append(pos_B)
    r += 1

def random_roll():
    return [random.randint(1, 6) + random.randint(1, 6), random.randint(1, 6) + random.randint(1, 6)]

def player_move(chips_list):
    rolls_list = [random_roll(), random_roll(), random_roll()]

    for i in range(len(rolls_list)):
        pos_list.append([width/3*i+width/12, height/2-height/15, 120, height/18])

    while True:
        for ev in pygame.event.get(): 
            if ev.type == pygame.QUIT: 
                pygame.quit()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(pos_list)):
                    pos = pos_list[i]
                    if pos[0] <= mouse[0] <= pos[0] + pos[2] and pos[1] <= mouse[1] <= pos[1] + pos[3]:
                        return rolls_list[i], pos_list

        mouse = pygame.mouse.get_pos()
        for i in range(len(rolls_list)):
            roll = rolls_list[i]
            roll_text = myfont.render(f'Roll: {roll[0]} {roll[1]}', True, color)
            pos = pos_list[i]

            if pos[0] <= mouse[0] <= pos[0] + pos[2] and pos[1] <= mouse[1] <= pos[1] + pos[3]:
                pygame.draw.rect(screen, color_light, pos)
            else:
                pygame.draw.rect(screen, color_dark, pos)

            screen.blit(roll_text, pos)

        pygame.display.update()

def continue_turn(pos_list):
    my_pos = [pos_list[0], pos_list[2]]
    while True:
        for ev in pygame.event.get(): 
            if ev.type == pygame.QUIT: 
                pygame.quit()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                if my_pos[0][0] <= mouse[0] <= my_pos[0][0] + my_pos[0][2] and my_pos[0][1] <= mouse[1] <= my_pos[0][1] + my_pos[0][3]:
                    return True
                elif my_pos[1][0] <= mouse[0] <= my_pos[1][0] + my_pos[1][2] and my_pos[1][1] <= mouse[1] <= my_pos[1][1] + my_pos[1][3]:
                    return False

        mouse = pygame.mouse.get_pos()
        text_list = ["Continue", "Stop"]
        r = 0

        pygame.draw.rect(screen, SCREEN_COLOR, pos_list[1])

        for pos in my_pos:
            if pos[0] <= mouse[0] <= pos[0] + pos[2] and pos[1] <= mouse[1] <= pos[1] + pos[3]:
                pygame.draw.rect(screen, color_light, pos)
            else:
                pygame.draw.rect(screen, color_dark, pos)

            curr_text = myfont.render(text_list[r], True, color)
            screen.blit(curr_text, pos)
            r += 1

        pygame.display.update()

WHOSE_MOVE = 0
pieces_list = []
while True: 
    for ev in pygame.event.get(): 
        if ev.type == pygame.QUIT: 
            pygame.quit() 

        if ev.type == pygame.MOUSEBUTTONDOWN: 
            if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40: 
                pygame.quit() 
             
    moves, pos_list = player_move()
    for move in moves:
        if WHOSE_MOVE == 0:
            player_A[move] += 1
            pos = player_pos_list['A'][move-2]
            pygame.draw.rect(screen, SCREEN_COLOR, pos)
            A_text = myfont.render(f"{player_A[move]}", True, color)
            screen.blit(A_text, pos)
        else:
            player_B[move] += 1
            pos = player_pos_list['B'][move-2]
            pygame.draw.rect(screen, SCREEN_COLOR, pos)
            B_text = myfont.render(f"{player_B[move]}", True, color)
            screen.blit(B_text, pos)

    pygame.display.update() 
    is_continue = continue_turn(pos_list)
    if not is_continue:
        WHOSE_MOVE = (1-WHOSE_MOVE)