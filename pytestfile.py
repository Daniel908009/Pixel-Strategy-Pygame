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
            # filing the list with the coordinates of all the players, if coordinates are already in the list they will be ignored
            for i in range(num_players):
                for j in range(len(players_actual[i]["coordinates"])):
                    if players_actual[i]["coordinates"][j] in players_actual_tiles_of_interest:
                        pass
                    else:
                        players_actual_tiles_of_interest.append(players_actual[i]["coordinates"][j])
            
            
            
            
            #for i in range(num_players):
             #   for j in range(len(players_actual[i]["coordinates"])):
              #      players_actual_tiles_of_interest.append(players_actual[i]["coordinates"][j])
            
            # if the tiles in players_actual_tiles_of_interest have a neighbour that is in other players tiles than they can stay, the tiles that do not will be removed
            for i in range(num_players):
                for j in range(len(players_actual_tiles_of_interest)):
                    if (players_actual_tiles_of_interest[j][0]+1, players_actual_tiles_of_interest[j][1]) in players_actual[i]["coordinates"] or (players_actual_tiles_of_interest[j][0], players_actual_tiles_of_interest[j][1]+1) in players_actual[i]["coordinates"] or (players_actual_tiles_of_interest[j][0]-1, players_actual_tiles_of_interest[j][1]) in players_actual[i]["coordinates"] or (players_actual_tiles_of_interest[j][0], players_actual_tiles_of_interest[j][1]-1) in players_actual[i]["coordinates"] or (players_actual_tiles_of_interest[j][0]+1, players_actual_tiles_of_interest[j][1]+1) in players_actual[i]["coordinates"] or (players_actual_tiles_of_interest[j][0]-1, players_actual_tiles_of_interest[j][1]+1) in players_actual[i]["coordinates"] or (players_actual_tiles_of_interest[j][0]+1, players_actual_tiles_of_interest[j][1]-1) in players_actual[i]["coordinates"] or (players_actual_tiles_of_interest[j][0]-1, players_actual_tiles_of_interest[j][1]-1) in players_actual[i]["coordinates"]:
                        pass
                    else:
                        print("temp is being appended")
                        temp.append(players_actual_tiles_of_interest[j])
                        print(temp)

            # removing the tiles that do not have a neighbour from players_actual_tiles_of_interest
            for i in range(len(temp)):
                players_actual_tiles_of_interest.remove(temp[i])
                print("removed")

            print(players_actual_tiles_of_interest)
            
            temp.clear()
            
            print("running")
            numberofruns += 1
            if numberofruns == 5:
                running = False
                not_end = False
            #running = False
            #not_end = False
            time.sleep(game_speed)

# simulation parameters of optimalization
running = True
not_end = True
game_speed = 0.09
num_players = 2
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
                                (0, 1),(1,1),(2,1),
                                (0,2),(1,2),(2,2)], "num_of_tiles": 9})
   
players.append({"coordinates": [(0, 3),(1,3),(2,3),(3, 3),(3,1),(3,0)], "num_of_tiles": 7})


print(players[0]["coordinates"])
print(players[1]["coordinates"])
players_actual = players
print(players_actual[0]["coordinates"])
print(players_actual[1]["coordinates"])
optimalization()
