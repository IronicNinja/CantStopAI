import numpy as np
import sys
import math
import random
import game_stats

#pylint: skip-file

def random_roll(chips_list, hypo_completed):
    """
    Simulates a random roll. Takes into consideration what the current chips list is and what the "hypothesized" completed
    chips are. Thus, this function will only return rolls that are actually pickable.

    Returns: rolls, boolean that determines whether to split the numbers (e.g. pick 6 OR 8)
    """
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
            if rolls[0] in chips_list or rolls[1] in chips_list or rolls[0] == rolls[1]:
                return rolls, False
            else:
                return rolls, True
        elif n == 3:
            if rolls[0] in chips_list and rolls[1] in chips_list:
                return rolls, False
            else:
                return [], False

def player_move(chips_list, hypo_A, hypo_B, hypo_completed, board_end, PLAYER_MOVE, RANDOM=True):
    """
    Simulates a player's move, where they are presented with the three rolls. If RANDOM is set to true, then this code randomly
    chooses a number to pick from the possible choices.

    Returns: Updated chips list, updated completed list, "True" which means the roll FAILED/didn't go through and the player's progress is gone
    """

    rolls_list = []
    for i in range(3):
        rolls, is_split = random_roll(chips_list, hypo_completed)

        if is_split:
            for roll in rolls:
                rolls_list.append([roll])
        elif rolls:
            rolls_list.append(rolls)

    if not rolls_list:
        return chips_list, hypo_completed, True

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
    """
    Randomly determines if the player's turn continues
    """

    if RANDOM:
        is_cont = random.random()
        if is_cont <= RIG:
            return True
        else:
            return False

def run(chips_list, player_A, player_B, hypo_A, hypo_B, player_A_score, player_B_score, A_score_org, B_score_org, completed, hypo_completed, board_end, PLAYER_MOVE):
    """
    Driver Monte Carlo Simulation

    Returns: Result, total fails, total ends
    """
    total_fails = 0
    total_ends = 0

    while True:
        chips_list, hypo_completed, failed = player_move(chips_list, hypo_A, hypo_B, hypo_completed, board_end, PLAYER_MOVE)
        if failed:
            total_fails += 1
            # Reset all parameters
            if PLAYER_MOVE:
                hypo_A = player_A.copy()
                if total_fails == 1 and total_ends == 0:
                    player_A_score = A_score_org
            else:
                hypo_B = player_B.copy()
                if total_fails == 1 and total_ends == 0:
                    player_B_score = B_score_org
            hypo_completed = completed.copy()
            chips_list = set()
            PLAYER_MOVE = (1-PLAYER_MOVE)
            continue
        
        if len(chips_list) < 3:
            # You should never end before using all three chips
            continue

        is_cont = continue_turn(RIG=0.5) # Potentially have RIG higher since you don't really want to end too early typically
        if not is_cont:
            total_ends += 1
            # Copy all parameters over
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
                return 1, total_fails, total_ends
            elif player_B_score >= 3:
                return 0, total_fails, total_ends

def play(ITERATIONS, PRINT_STATS=False):
    # Original parameters - is changed every play + continuation
    player_A_org = game_stats.player_A.copy()
    player_B_org = game_stats.player_B.copy()
    hypo_A_org = game_stats.hypo_A.copy()
    hypo_B_org = game_stats.hypo_B.copy()
    player_A_score_org = game_stats.player_A_score
    player_B_score_org = game_stats.player_B_score
    hypo_A_score_org = game_stats.player_A_score
    hypo_B_score_org = game_stats.player_B_score
    completed_org = game_stats.completed.copy()
    hypo_completed_org = game_stats.hypo_completed.copy()
    PLAYER_MOVE_org = game_stats.PLAYER_MOVE
    chips_list_org = set()
    board_end = {k: 2*(7-abs(7-k))-1 for k in range(2, 13)}

    while True:
        # Input -1 for impossible moves
        a1, a2 = [int(x) for x in input("Top Dice: ").split()]
        b1, b2 = [int(x) for x in input("Middle Dice: ").split()]
        c1, c2 = [int(x) for x in input("Last Dice: ").split()]
        possible_moves = [[a1, a2], [b1, b2], [c1, c2]]
        # Pre split
        possible_moves_tmp = []
        go = True
        for i in range(len(possible_moves)):
            rolls = []
            for move in possible_moves[i]:
                if move not in hypo_completed_org and move != -1:
                    rolls.append(move)

            n = len(chips_list_org)
            if not rolls:
                continue
            elif len(rolls) == 1:
                if n == 3:
                    if rolls[0] in chips_list_org:
                        possible_moves_tmp.append(rolls)  
                    else:
                        continue
                else:
                    possible_moves_tmp.append(rolls)
            else:
                if n <= 1:
                    possible_moves_tmp.append(rolls)
                elif n == 2:
                    if rolls[0] in chips_list_org or rolls[1] in chips_list_org or rolls[0] == rolls[1]:
                        possible_moves_tmp.append(rolls)
                    else:
                        for roll in rolls:
                            possible_moves_tmp.append([roll])
                elif n == 3:
                    if rolls[0] in chips_list_org and rolls[1] in chips_list_org:
                        possible_moves_tmp.append(rolls)
                    else:
                        continue
            go = False
                
        if go:
            print("No moves are possible.")
            return

        possible_moves = possible_moves_tmp
        
        win_percentage = []
        for i in range(len(possible_moves)):
            # Current move copy of original version - Iterated over 3 times
            player_A_now = player_A_org.copy()
            player_B_now = player_B_org.copy()
            hypo_A_now = hypo_A_org.copy()
            hypo_B_now = hypo_B_org.copy()
            player_A_score_now = player_A_score_org
            player_B_score_now = player_B_score_org
            hypo_A_score_now = hypo_A_score_org
            hypo_B_score_now = hypo_B_score_org
            completed_now = completed_org.copy()
            hypo_completed_now = hypo_completed_org.copy()
            PLAYER_MOVE_now = PLAYER_MOVE_org
            chips_list_now = chips_list_org.copy()

            for move in possible_moves[i]:
                chips_list_now.add(move)
                if PLAYER_MOVE_now:
                    player_A_now[move] += 1
                    if player_A_now[move] >= board_end[move]:
                        hypo_completed_now.add(move)
                        hypo_A_score_now += 1
                else:
                    player_B_now[move] += 1
                    if player_B_now[move] >= board_end[move]:
                        hypo_completed_now.add(move)
                        hypo_B_score_now += 1
            
            result_list = [0, 0]
            other_info = [0, 0]
            for j in range(ITERATIONS):
                # Copy of each turn's version
                player_A = player_A_now.copy()
                player_B = player_B_now.copy()
                hypo_A = hypo_A_now.copy()
                hypo_B = hypo_B_now.copy()
                A_score_org = player_A_score_now
                B_score_org = player_B_score_now
                player_A_score = hypo_A_score_now # local storage
                player_B_score = hypo_B_score_now
                completed = completed_now.copy()
                hypo_completed = hypo_completed_now.copy()
                PLAYER_MOVE = PLAYER_MOVE_now
                chips_list = chips_list_now.copy()
                
                result, total_fails, total_ends = run(chips_list, 
                            player_A, player_B, hypo_A, hypo_B, player_A_score, player_B_score, A_score_org, B_score_org, completed, hypo_completed, board_end, PLAYER_MOVE)
                
                result_list[result] += 1
                other_info[0] += total_fails
                other_info[1] += total_ends

            if PLAYER_MOVE_now:
                win_percentage.append([result_list[1], i])
            else:
                win_percentage.append([result_list[0], i])
            
            if len(possible_moves[i]) == 1:
                print(f"For roll {possible_moves[i][0]}, Player A won {result_list[1]} times, Player B won {result_list[0]} times. There was an average of {other_info[0]/ITERATIONS} fails and {other_info[1]/ITERATIONS} ends.")
            else:
                print(f"For roll {possible_moves[i][0]} and {possible_moves[i][1]}, Player A won {result_list[1]} times, Player B won {result_list[0]} times. There was an average of {other_info[0]/ITERATIONS} fails and {other_info[1]/ITERATIONS} ends.")

        win_percentage.sort(reverse=True)
        print(f"The player should pick Dice number {win_percentage[0][1]+1}, which has the roll(s) {possible_moves[win_percentage[0][1]]}")
        # Make the move that leads to the highest win percentage
        for move in possible_moves[win_percentage[0][1]]:
            chips_list_org.add(move)
            if PLAYER_MOVE_org:
                hypo_A_org[move] += 1
                if hypo_A_org[move] >= board_end[move]:
                    hypo_completed_org.add(move)
                    hypo_A_score_org += 1
                    if hypo_A_score_org >= 3:
                        print("Player A wins.")
                        return
            else:
                hypo_B_org[move] += 1
                if hypo_B_org[move] >= board_end[move]:
                    hypo_completed_org.add(move)
                    hypo_B_score_org += 1
                    if hypo_B_score_org >= 3:
                        print("Player B wins.")
                        return

        # Determine if we should end
        result_list = [0, 0]
        win_percentage_cont = []
        for j in range(ITERATIONS):
            # end
            player_A = hypo_A_org.copy()
            player_B = hypo_B_org.copy()
            hypo_A = hypo_A_org.copy()
            hypo_B = hypo_B_org.copy()
            A_score_org = hypo_A_score_org
            B_score_org = hypo_B_score_org
            player_A_score = hypo_A_score_org
            player_B_score = hypo_B_score_org
            completed = hypo_completed_org.copy()
            hypo_completed = hypo_completed_org.copy()
            PLAYER_MOVE = (1-PLAYER_MOVE_org)
            chips_list = set()

            result, total_fails, total_ends = run(chips_list, 
                            player_A, player_B, hypo_A, hypo_B, player_A_score, player_B_score, A_score_org, B_score_org, completed, hypo_completed, board_end, PLAYER_MOVE)
            
            result_list[result] += 1

        if PLAYER_MOVE_org:
            win_percentage_cont.append(result_list[1])
        else:
            win_percentage_cont.append(result_list[0])
        
        print(f"If the turn ends, then Player A won {result_list[1]} times, Player B won {result_list[0]} times.")

        result_list = [0, 0]

        for j in range(ITERATIONS):
            # continue
            player_A = player_A_org.copy()
            player_B = player_B_org.copy()
            hypo_A = hypo_A_org.copy()
            hypo_B = hypo_B_org.copy()
            A_score_org = player_A_score_org
            B_score_org = player_B_score_org
            player_A_score = hypo_A_score_org
            player_B_score = hypo_B_score_org
            completed = completed_org.copy()
            hypo_completed = hypo_completed_org.copy()
            PLAYER_MOVE = PLAYER_MOVE_org
            chips_list = chips_list_org.copy()

            result, total_fails, total_ends = run(chips_list, 
                        player_A, player_B, hypo_A, hypo_B, player_A_score, player_B_score, A_score_org, B_score_org, completed, hypo_completed, board_end, PLAYER_MOVE)
            
            result_list[result] += 1

        if PLAYER_MOVE_org:
            win_percentage_cont.append(result_list[1])
        else:
            win_percentage_cont.append(result_list[0])
        
        print(f"If the turn continues, then Player A won {result_list[1]} times, Player B won {result_list[0]} times.")

        with open('game.txt', 'w') as f:
            if PLAYER_MOVE_org:
                f.write(f"player_A = {hypo_A_org}\nplayer_A_score = {hypo_A_score_org}\n")
            else:
                f.write(f"player_B = {hypo_B_org}\nplayer_B_score = {hypo_B_score_org}\n")
                    
            f.write(f"completed = {hypo_completed_org}\nchips_list = {chips_list_org}")

        if win_percentage_cont[1] >= win_percentage_cont[0] or len(chips_list_org) < 3:
            print("The player should continue the game... waiting for input now...")
        else:
            print("The computer suggests you should end your turn. Will you continue? Type yes/no.")
            while True:
                is_cont = str(input("Continue: "))
                if is_cont.lower() == "yes":
                    break
                elif is_cont.lower() == "no":
                    return
                else:
                    print("Try to input again...")
            
play(1600, PRINT_STATS=True)