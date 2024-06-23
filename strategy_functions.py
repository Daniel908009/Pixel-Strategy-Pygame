# This file contains all the functions that are used in the main file

#necessary imports
import random


# Function to check if a player has some border tiles with another player and returning them
def border_tiles_func(players, player1, player2):
    potential_tiles1 = []
    potential_tiles2 = []
    border_tiles = []
    # Needs to be enhanced, currently only checks in 4 directions
    for j in range(len(players[player1]["coordinates"])):
        potential_tiles1.append((players[player1]["coordinates"][j][0]+1, players[player1]["coordinates"][j][1]))
        potential_tiles1.append((players[player1]["coordinates"][j][0]-1, players[player1]["coordinates"][j][1]))
        potential_tiles1.append((players[player1]["coordinates"][j][0], players[player1]["coordinates"][j][1]+1))
        potential_tiles1.append((players[player1]["coordinates"][j][0], players[player1]["coordinates"][j][1]-1))

    for k in range(len(players[player2]["coordinates"])):
        potential_tiles2.append((players[player2]["coordinates"][k][0]+1, players[player2]["coordinates"][k][1]))
        potential_tiles2.append((players[player2]["coordinates"][k][0]-1, players[player2]["coordinates"][k][1]))
        potential_tiles2.append((players[player2]["coordinates"][k][0], players[player2]["coordinates"][k][1]+1))
        potential_tiles2.append((players[player2]["coordinates"][k][0], players[player2]["coordinates"][k][1]-1))

    for i in potential_tiles1:
        for j in range(len(players[player2]["coordinates"])):
            if i == players[player2]["coordinates"][j]:
                border_tiles.append(i)
    for i in potential_tiles2:
        for j in range(len(players[player1]["coordinates"])):
            if i == players[player1]["coordinates"][j]:
                border_tiles.append(i)
    
    potential_tiles1.clear()
    potential_tiles2.clear()
    return border_tiles
        
# Function to decide who wins the battle, works on chances of winning based on the power of players
def battle_logic_core(power1, power2, player1, player2):
    all_outcomes = power1 + power2
    who_wins = random.randint(1, all_outcomes)
    if who_wins > power1:
        return player2
    else:
        return player1
    
# Function to change the owner of the tile after the battle ends
def change_of_owner(winner_of_battle, tile_attacked, players, player1, player2):
    if winner_of_battle[0] == player1:
        players[player2]["coordinates"].remove(tile_attacked)
        players[player1]["coordinates"].append(tile_attacked)
        players[player1]["num_of_tiles"] += 1
        players[player2]["num_of_tiles"] -= 1
    else:
        players[player1]["coordinates"].remove(tile_attacked)
        players[player2]["coordinates"].append(tile_attacked)
        players[player2]["num_of_tiles"] += 1
        players[player1]["num_of_tiles"] -= 1    
