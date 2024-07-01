# Description: This file is for testing different parts of the code in isolation. It is not meant to be run as a standalone program.

import random
import time
import threading
import pygame
from collections import Counter

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

# this function decides which tiles are of interest to other functions, somewhere in here is a mistake that causes the function to give weird results 
# somehow specific tiles are being removed even though they should not be, because they have are neighbours with other players tiles, weird...
def optimalization():
    global players_actual, players_actual_tiles_of_interest, running, not_end, game_speed, num_players
    temp = []
    numberofruns = 0

    while not_end:
        while running:
            players_actual_tiles_of_interest.clear()
            # filing the list with the coordinates of all the players, if coordinates are already in the list they will be ignored
            for i in range(num_players):
                players_actual_tiles_of_interest.append(players_actual[i]["coordinates"])
            print(players_actual_tiles_of_interest)
            
            # if the tiles in players_actual_tiles_of_interest have a neighbour that is in other players tiles than they can stay, the tiles that do not will be removed
            for i in range(num_players):
                for j in range(len(players_actual_tiles_of_interest)):
                    for k in range(len(players_actual_tiles_of_interest[j])):
                        if (players_actual_tiles_of_interest[j][k][0]+1, players_actual_tiles_of_interest[j][k][1]) in players_actual[i]["coordinates"] or (players_actual_tiles_of_interest[j][k][0], players_actual_tiles_of_interest[j][k][1]+1) in players_actual[i]["coordinates"] or (players_actual_tiles_of_interest[j][k][0]-1, players_actual_tiles_of_interest[j][k][1]) in players_actual[i]["coordinates"] or (players_actual_tiles_of_interest[j][k][0], players_actual_tiles_of_interest[j][k][1]-1) in players_actual[i]["coordinates"] or (players_actual_tiles_of_interest[j][k][0]+1, players_actual_tiles_of_interest[j][k][1]+1) in players_actual[i]["coordinates"] or (players_actual_tiles_of_interest[j][k][0]-1, players_actual_tiles_of_interest[j][k][1]+1) in players_actual[i]["coordinates"] or (players_actual_tiles_of_interest[j][k][0]+1, players_actual_tiles_of_interest[j][k][1]-1) in players_actual[i]["coordinates"] or (players_actual_tiles_of_interest[j][k][0]-1, players_actual_tiles_of_interest[j][k][1]-1) in players_actual[i]["coordinates"]:
                            pass
                        else:
                            temp.append(players_actual_tiles_of_interest[j][k])
                            print(str(players_actual_tiles_of_interest[j][k]) + "this is being appended to temp")
            print(str(temp) + "temp")


            # removing the tiles that do not have a neighbour from players_actual_tiles_of_interest, uses count() to check if the tile is in the temp list enough times to justify removing it
            for i in range(len(temp)):
                for j in range(len(players_actual_tiles_of_interest)):
                    for k in range(len(players_actual_tiles_of_interest[j])):
                        for h in range(len(temp)):
                            try:
                                if temp[h] == players_actual_tiles_of_interest[j][k]:
                                    count = Counter(temp)
                                    print(count)
                                    print(count)
                                    if count[temp[i]] == num_players-1 or count[temp[i]] > num_players-1:
                                        try:
                                            players_actual_tiles_of_interest[j].remove(temp[i])
                                        except ValueError:
                                            pass
                                    else:
                                        pass
                            except IndexError:
                                pass
                            else:
                                pass

            print(players_actual_tiles_of_interest)
            
            temp.clear()
            count.clear()

            
            print("running")
            numberofruns += 1
            #if numberofruns == 5:
            #    running = False
            #    not_end = False
            running = False
            not_end = False
            time.sleep(game_speed)
            #time.sleep(1)

# simulation parameters of optimalization
running = True
not_end = True
game_speed = 0.09
num_players = 4
players = []
players_actual = []
players_actual_tiles_of_interest = []
map_occupied_tiles = []
pixel = 4
ratio = (1, 1)
map_size = pixel*pixel
#for i in range(num_players):
#    playercoords1 = (random.randint(0, (map_size-1)*ratio[1]), random.randint(0, (map_size-1)*ratio[0]))
#    map_occupied_tiles.append((playercoords1 ))   
#    players.append(
#        {
#            "color": (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
#            "coordinates": [(playercoords1[0], playercoords1[1])],
#            "num_of_tiles": 1
#        }
#    )
players.append({"coordinates": [(0, 0),(1,0),(2,0),
                                (0, 1),(2,1),
                                (0,2),(1,2),(2,2)], "num_of_tiles": 8})
   
players.append({"coordinates": [(0, 3),(1,3),(2,3)], "num_of_tiles": 3})

players.append({"coordinates": [(3, 3),(3,1)], "num_of_tiles": 2})

players.append({"coordinates": [(3,0), (3,2), (1,1)], "num_of_tiles": 3})



players_actual = players

optimalization()
