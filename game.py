import numpy as np
import sys
import math
import random
import game_stats

#pylint: skip-file

def random_roll(chips_list, hypo_completed):
    tmp_rolls = [random.randint(1, 6) + random.randint(1, 6), random.randint(1, 6) + random.randint(1, 6)]
    rolls = []
    for i in range(2):
        if tmp_rolls[i] not in hypo_completed:
            rolls.append(tmp_rolls[i])

    n = len(chips_list)
    if not rolls:
        return [], False
    elif len(rolls) == 1:
        if n == 3:
            if rolls[0] in chips_list:
                return rolls, False
            else:
                return [], False
        else:
            return rolls, False
    else:
        if n <= 1:
            return rolls, False
        elif n == 2:
            if rolls[0] in chips_list or rolls[1] in chips_list:
                return rolls, False
            else:
                return rolls, True
        elif n == 3:
            if rolls[0] in chips_list and rolls[1] in chips_list:
                return rolls, False
            else:
                return [], False

def player_move(chips_list, player_A, player_B, hypo_A, hypo_B, completed, hypo_completed, board_end, PLAYER_MOVE, RANDOM=True):
    rolls_list = []
    for i in range(3):
        rolls, is_split = random_roll(chips_list, hypo_completed)
        if is_split:
            for roll in rolls:
                rolls_list.append([roll])
        elif rolls:
            rolls_list.append(rolls)
    #print(rolls_list)

    if not rolls_list:
        if PLAYER_MOVE:
            hypo_A = player_A.copy()
        else:
            hypo_B = player_B.copy()
        hypo_completed = completed.copy()
        return set(), hypo_completed, True

    if RANDOM:
        index = random.randint(0, len(rolls_list)-1)
        for roll in rolls_list[index]:
            if PLAYER_MOVE:
                hypo_A[roll] += 1
                if hypo_A[roll] >= board_end[roll]:
                    hypo_completed.add(roll)
            else:
                hypo_B[roll] += 1
                if hypo_B[roll] >= board_end[roll]:
                    hypo_completed.add(roll)
            chips_list.add(roll)

        return chips_list, hypo_completed, False
            
def continue_turn(RANDOM=True, RIG=0.5):
    if RANDOM:
        is_cont = random.random()
        if is_cont <= RIG:
            return True
        else:
            return False

def run(chips_list, player_A, player_B, hypo_A, hypo_B, player_A_score, player_B_score, completed, hypo_completed, board_end, PLAYER_MOVE):
    # monte carlo simulation

    while True:
        chips_list, hypo_completed, is_cont = player_move(chips_list, player_A, player_B, hypo_A, hypo_B, completed, hypo_completed, board_end, PLAYER_MOVE)
        if is_cont:
            PLAYER_MOVE = (1-PLAYER_MOVE)
            continue

        if len(chips_list) < 3:
            continue

        is_cont = continue_turn(RIG=0.8)
        if not is_cont:
            if PLAYER_MOVE:
                player_A = hypo_A.copy()
            else:
                player_B = hypo_B.copy()

            for num in hypo_completed:
                if num not in completed:
                    if PLAYER_MOVE:
                        player_A_score += 1
                    else:
                        player_B_score += 1

            completed = hypo_completed.copy()
            PLAYER_MOVE = (1-PLAYER_MOVE)

            if player_A_score >= 3:
                return 1, player_A, player_B, hypo_A, hypo_B, player_A_score, player_B_score, completed, hypo_completed, board_end, PLAYER_MOVE
            elif player_B_score >= 3:
                return 0, player_A, player_B, hypo_A, hypo_B, player_A_score, player_B_score, completed, hypo_completed, board_end, PLAYER_MOVE

def play(ITERATIONS):
    # Input -1 for impossible moves
    a1, a2 = [int(x) for x in input("Top Dice: ").split()]
    b1, b2 = [int(x) for x in input("Middle Dice: ").split()]
    c1, c2 = [int(x) for x in input("Last Dice: ").split()]
    possible_moves = [[a1, a2], [b1, b2], [c1, c2]]

    # Original parameters - is changed every play + continuation
    player_A_org = game_stats.player_A.copy()
    player_B_org = game_stats.player_B.copy()
    hypo_A_org = game_stats.hypo_A.copy()
    hypo_B_org = game_stats.hypo_B.copy()
    player_A_score_org = game_stats.player_A_score
    player_B_score_org = game_stats.player_B_score
    completed_org = game_stats.completed.copy()
    hypo_completed_org = game_stats.hypo_completed.copy()
    PLAYER_MOVE_org = game_stats.PLAYER_MOVE
    board_end = {k: 2*(7-abs(7-k))-1 for k in range(2, 13)}
    chips_list_org = set()

    while True:
        win_percentage = []
        for i in range(len(possible_moves)):
            # Current move copy of original version - Iterated over 3 times
            player_A_now = player_A_org.copy()
            player_B_now = player_B_org.copy()
            hypo_A_now = hypo_A_org.copy()
            hypo_B_now = hypo_B_org.copy()
            player_A_score_now = player_A_score_org
            player_B_score_now = player_B_score_org
            completed_now = completed_org.copy()
            hypo_completed_now = hypo_completed_org.copy()
            PLAYER_MOVE_now = PLAYER_MOVE_org
            chips_list_now = chips_list_org.copy()
            for move in possible_moves[i]:
                if move == -1:
                    continue
                    
                chips_list_now.add(move)
                if PLAYER_MOVE_now:
                    player_A_now[move] += 1
                    if player_A_now[move] >= board_end[move]:
                        hypo_completed_now.add(move)
                        player_A_score_now += 1
                else:
                    player_B_now[move] += 1
                    if player_B_now[move] >= board_end[move]:
                        hypo_completed_now.add(move)
                        player_B_score_now += 1
            
            result_list = [0, 0]
            for j in range(ITERATIONS):
                # Copy of each turn's version
                player_A = player_A_now.copy()
                player_B = player_B_now.copy()
                hypo_A = hypo_A_now.copy()
                hypo_B = hypo_B_now.copy()
                player_A_score = player_A_score_now
                player_B_score = player_B_score_now
                completed = completed_now.copy()
                hypo_completed = hypo_completed_now.copy()
                PLAYER_MOVE = PLAYER_MOVE_now
                chips_list = chips_list_now.copy()
                result, player_A, player_B, hypo_A, hypo_B, player_A_score, player_B_score, completed, hypo_completed, board_end, PLAYER_MOVE = run(chips_list, 
                            player_A, player_B, hypo_A, hypo_B, player_A_score, player_B_score, completed, hypo_completed, board_end, PLAYER_MOVE)
                result_list[result] += 1

            if PLAYER_MOVE_now:
                win_percentage.append([result_list[1], i])
            else:
                win_percentage.append([result_list[0], i])
            
            print(f"Player A won {result_list[1]} times, Player B won {result_list[0]} times")
        
        win_percentage.sort(reverse=True)
        
        # Make the move that leads to the highest win percentage
        for move in possible_moves[win_percentage[0][1]]:
            chips_list_org.add(move)
            if PLAYER_MOVE_org:
                player_A_org[move] += 1
                if player_A_org[move] >= board_end[move]:
                    hypo_completed_org.add(move)
                    player_A_score_org += 1
            else:
                player_B_org[move] += 1
                if player_B_org[move] >= board_end[move]:
                    hypo_completed_org.add(move)
                    player_B_score_org += 1

        result_list = [0, 0]
        # Simulate whether to continue
        for j in range(ITERATIONS):
            # continue
            result, player_A, player_B, hypo_A, hypo_B, player_A_score, player_B_score, completed, hypo_completed, board_end, PLAYER_MOVE = run(chips_list, 
                    player_A, player_B, hypo_A, hypo_B, player_A_score, player_B_score, completed, hypo_completed, board_end, PLAYER_MOVE)

        for j in range(ITERATIONS):
            # end
            PLAYER_MOVE = (1-PLAYER_MOVE_org)
            result, player_A, player_B, hypo_A, hypo_B, player_A_score, player_B_score, completed, hypo_completed, board_end, PLAYER_MOVE = run(chips_list, 
                    player_A, player_B, hypo_A, hypo_B, player_A_score, player_B_score, completed, hypo_completed, board_end, PLAYER_MOVE)
            
play(10000)