# Description: This file is for testing different parts of the code in isolation. It is not meant to be run as a standalone program.

import random
import time
import threading
import pygame

#def expandsion_initial(num_players, map_free_tiles, index_version_of_free_tiles):
#    global players_actual
#
#    for i in range(num_players):
#        potential_tiles = []
#        
#        for coord in players_actual[i]["coordinates"]:
#            x, y = coord
#            # 4 directions expansion (left, right, up, down)
#            potential_tiles.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])
#            # diagonal expansion (up-right, up-left, down-right, down-left)
#            potential_tiles.extend([(x+1, y+1), (x-1, y+1), (x+1, y-1), (x-1, y-1)])
#        
#        # Find potential free tiles from potential tiles
#        free_potential_tiles = [tile for tile in potential_tiles if tile in index_version_of_free_tiles]
#
#        if not free_potential_tiles:
#            continue  # If no free potential tiles, skip to the next player
#        
#        try:
#            random_tile = random.choice(free_potential_tiles)
#            index_version_of_free_tiles.remove(random_tile)
#            map_free_tiles -= 1
#
#            players_actual[i]["coordinates"].append(random_tile)
#            players_actual[i]["num_of_tiles"] += 1
#
#            print(f"Player {i}: Added tile {random_tile}. Total tiles: {players_actual[i]['num_of_tiles']}")
#            
#            if map_free_tiles == 0:
#                return map_free_tiles
#        except IndexError:
#            print(f"Player {i}: No more free potential tiles.")
#            continue
#    
#    return map_free_tiles
#
## Example usage and testing:
#players_actual = [
#    {"coordinates": [(0, 0)], "num_of_tiles": 1},
#    {"coordinates": [(10, 10)], "num_of_tiles": 1},
#    # Add more players as needed
#]
#
#num_players = len(players_actual)
#map_free_tiles = 100  # Example number of free tiles
#index_version_of_free_tiles = [(x, y) for x in range(20) for y in range(20)]  # Example grid of free tiles
#while map_free_tiles > 0:
#    map_free_tiles = expandsion_initial(num_players, map_free_tiles, index_version_of_free_tiles)
#
#print("Final players state:")
#for player in players_actual:
#    print(player)
#print(f"Remaining free tiles: {map_free_tiles}")
#

def optimalization():
    global players_actual, players_actual_tiles_of_interest, running, not_end, game_speed, num_players
    temp = []
    numberofruns = 0

    while not_end:
        while running:
            # filing the list with the coordinates of all the players
            for i in range(num_players):
                players_actual_tiles_of_interest.append(players_actual[i]["coordinates"])
            # if the tile borders anything else than the player that controls it, it is of interest
            for l in range(num_players):
                for m in range(len(players_actual[l]["coordinates"])):
                    tile = players_actual[l]["coordinates"][m]
                    for k in range(players_actual[l]["num_of_tiles"]):
                        if (tile[0]+1, tile[1]) not in players_actual[l]["coordinates"][k] or (tile[0]-1, tile[1]) not in players_actual[l]["coordinates"][k] or (tile[0], tile[1]+1) not in players_actual[l]["coordinates"][k] or (tile[0],tile[1]-1) not in players_actual[l]["coordinates"][k] or (tile[0]+1, tile[1]+1) not in players_actual[l]["coordinates"][k] or (tile[0]-1, tile[1]+1) not in players_actual[l]["coordinates"][k] or (tile[0]+1, tile[1]-1) not in players_actual[l]["coordinates"][k] or (tile[0]-1, tile[1]-1) not in players_actual[l]["coordinates"][k]:
                            numberofruns += 1
                    if numberofruns == len(players_actual[l]["coordinates"]):
                        temp.append(tile)
            for i in range(len(temp)):
                for j in range(len(players_actual_tiles_of_interest)):
                    if temp[i] in players_actual_tiles_of_interest[j]:
                        players_actual_tiles_of_interest.remove(players_actual_tiles_of_interest[j])

            time.sleep|(game_speed)

# simulation parameters of optimalization
running = True
not_end = True
game_speed = 0.09
num_players = 2




optimalization()