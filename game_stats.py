player_A = {2: 1, 3: 1, 4: 0, 5: 0, 6: 0, 7: 7, 8: 0, 9: 0, 10: 1, 11: 1, 12: 0}
player_B = {2:0, 3:0, 4:0, 5:3, 6:2, 7:9, 8:11, 9:8, 10:0, 11:0, 12:0}
hypo_A = player_A.copy()
hypo_B = player_B.copy()
board_end = {k: 2*(7-abs(7-k))-1 for k in range(2, 13)}
completed = set()
player_A_score = 0
player_B_score = 0

for key in player_A:
    if player_A[key] >= board_end[key]:
        completed.add(key)
        player_A_score += 1
    elif player_B[key] >= board_end[key]:
        completed.add(key)
        player_B_score += 1

hypo_completed = completed.copy()
PLAYER_MOVE = 1 # Starts with A