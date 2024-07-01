# This file contains all the functions that are used in the main file

#necessary imports
import random
import time
from collections import Counter

# global variables
players_actual = []
players_actual_tiles_of_interest = []
wars = []
num_players = 0
pixel_size = 0
screen = None
running = True
not_end = True
reset_game = False
game_speed = 0

# Function to receive important data from the main file
def send_important_data(players, num_players0, pixel_size0, screen0, game_speed0):
    global players_actual
    players_actual = players
    global num_players
    num_players = num_players0
    global pixel_size
    pixel_size = pixel_size0
    global screen
    screen = screen0
    global game_speed
    game_speed = game_speed0

# Function to check if a player has some border tiles with another player and returning them
def border_tiles_func(player1, player2):
    potential_tiles1 = []
    potential_tiles2 = []
    border_tiles = []
    # Works in all directions now
    for j in range(len(players_actual[player1]["coordinates"])):
        potential_tiles1.append((players_actual[player1]["coordinates"][j][0]+1, players_actual[player1]["coordinates"][j][1]))
        potential_tiles1.append((players_actual[player1]["coordinates"][j][0]-1, players_actual[player1]["coordinates"][j][1]))
        potential_tiles1.append((players_actual[player1]["coordinates"][j][0], players_actual[player1]["coordinates"][j][1]+1))
        potential_tiles1.append((players_actual[player1]["coordinates"][j][0], players_actual[player1]["coordinates"][j][1]-1))

    for k in range(len(players_actual[player2]["coordinates"])):
        potential_tiles2.append((players_actual[player2]["coordinates"][k][0]+1, players_actual[player2]["coordinates"][k][1]))
        potential_tiles2.append((players_actual[player2]["coordinates"][k][0]-1, players_actual[player2]["coordinates"][k][1]))
        potential_tiles2.append((players_actual[player2]["coordinates"][k][0], players_actual[player2]["coordinates"][k][1]+1))
        potential_tiles2.append((players_actual[player2]["coordinates"][k][0], players_actual[player2]["coordinates"][k][1]-1))

    for i in potential_tiles1:
        for j in range(len(players_actual[player2]["coordinates"])):
            if i == players_actual[player2]["coordinates"][j]:
                if is_encircled(i, player1):
                    for g in range(2):
                        border_tiles.append(i)
                else:
                    border_tiles.append(i)
    for i in potential_tiles2:
        for j in range(len(players_actual[player1]["coordinates"])):
            if i == players_actual[player1]["coordinates"][j]:
                if is_encircled(i, player2):
                    for h in range(10):
                        border_tiles.append(i)
                else:
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
    


# Function to change the owner of the tile after the battle
def change_of_owner(winner_of_battle, tile_attacked, player1, player2):
    global players_actual
    ply = players_actual.copy()
    if winner_of_battle == player1:
        # Remove tile from player2's coordinates
        for i in range(ply[player2]["num_of_tiles"]):
            if ply[player2]["coordinates"][i] == tile_attacked:
                ply[player2]["coordinates"] = tuple(
                    coord for coord in ply[player2]["coordinates"] if coord != tile_attacked
                )

            # Add tile to player1's coordinates
                ply[player1]["coordinates"] = tuple(
                    list(ply[player1]["coordinates"]) + [tile_attacked]
                )

            # Update the number of tiles
                ply[player1]["num_of_tiles"] += 1
                ply[player2]["num_of_tiles"] -= 1
            else:
                pass
    else:
        # Remove tile from player1's coordinates
        if tile_attacked in ply[player1]["coordinates"]:
            ply[player1]["coordinates"] = tuple(
                coord for coord in ply[player1]["coordinates"] if coord != tile_attacked
            )

            # Add tile to player2's coordinates
            ply[player2]["coordinates"] = tuple(
                list(ply[player2]["coordinates"]) + [tile_attacked]
            )

            # Update the number of tiles
            ply[player2]["num_of_tiles"] += 1
            ply[player1]["num_of_tiles"] -= 1
        else:
            pass

    return ply

# Map logic function, manages the diplomacy and battle logic
def map_logic(game_speed, num_players):
    global wars
    while not_end:
        while reset_game == False:
            while  running:
                diplomacy_logic(num_players)
                battle_logic()
                time.sleep(game_speed)
            time.sleep(0.1)
        time.sleep(0.1)


# diplomacy logic function, decides what will happen between players
def diplomacy_logic(num_players):
    global wars
    chance_of_nothing = 5
    diplomacy_options = []
    chance_of_peace = 1
    chance_of_war = 3
    for i in range(chance_of_nothing):
        diplomacy_options.append("nothing")

    for j in range(chance_of_peace):
        diplomacy_options.append("peace")
    
    for k in range(chance_of_war):
        diplomacy_options.append("war")
    
    for i in range(num_players):
        choice = random.choice(diplomacy_options)
        if choice == "peace":
            peace_logic(i)
        elif choice == "war":
            war_logic(i, num_players)
        else:
            pass

# war logic function, decides how will war be implemented between 2 players
def war_logic(player, num_players):
    global wars
    enemy = random.randint(0, num_players-1)
    if enemy == player or (player, enemy) in wars or (enemy, player) in wars:
        pass
    else:
        wars.append((player, enemy))

# peace logic function, removes players from wars list, currently peaces out with all other players 
# eventualy only one war will be peaced out, working on it
def peace_logic(player):
    global wars
    possible_peace = []
    for i in range(len(wars)):
        if wars[i][0] == player or wars[i][1] == player:
            possible_peace.append(i)
    m = 0
    for i in possible_peace:
        wars.pop(i-m)
        m += 1

def battle_logic():
    global players_actual, wars
    if len(wars) == 0:
        pass
    else:
        try:
            for i in range(len(wars)):
                player1 = wars[i][0]
                player2 = wars[i][1]
                power1 = players_actual[player1]["num_of_tiles"]
                power2 = players_actual[player2]["num_of_tiles"]
                tile_attacked = []
                border_tiles = []
                winner_of_battle = 0
                border_tiles.append(border_tiles_func(player1, player2))
                try:
                    tile_attacked.append(random.choice(border_tiles[0]))
                    winner_of_battle= battle_logic_core(power1, power2, player1, player2)
                    players_actual = change_of_owner(winner_of_battle, tile_attacked[0], player1, player2)
                    border_tiles.clear()
                    tile_attacked.clear()
                except IndexError:
                    pass
        except IndexError:
            pass
# removing occupied tiles from free tiles
def remove_occupied_tiles(players, num_players, map_free_tiles, map_occupied_tiles, index_version_of_free_tiles):
    map_free_tiles -= num_players
    for i in range(num_players):
        try:
            map_occupied_tiles.append(players[i]["coordinates"][0])
            index_version_of_free_tiles.remove(players[i]["coordinates"][0])
        except ValueError:
            pass
    return map_free_tiles

# expansion logic function, finds free tiles around all the player controled ones
def expandsion_initial(num_players,map_free_tiles, index_version_of_free_tiles):
    global players_actual, reset_game
    potential_tiles = []
    free_potential_tiles = []
    for i in range(num_players):
        for j in range(len(players_actual[i]["coordinates"])):
            # 4 directions expansion (left, right, up, down)
            potential_tiles.append((players_actual[i]["coordinates"][j][0]+1, players_actual[i]["coordinates"][j][1]))
            potential_tiles.append((players_actual[i]["coordinates"][j][0]-1, players_actual[i]["coordinates"][j][1]))
            potential_tiles.append((players_actual[i]["coordinates"][j][0], players_actual[i]["coordinates"][j][1]+1))
            potential_tiles.append((players_actual[i]["coordinates"][j][0], players_actual[i]["coordinates"][j][1]-1))
            # diagonal expansion (up-right, up-left, down-right, down-left)
            potential_tiles.append((players_actual[i]["coordinates"][j][0]+1, players_actual[i]["coordinates"][j][1]+1))
            potential_tiles.append((players_actual[i]["coordinates"][j][0]-1, players_actual[i]["coordinates"][j][1]+1))
            potential_tiles.append((players_actual[i]["coordinates"][j][0]+1, players_actual[i]["coordinates"][j][1]-1))
            potential_tiles.append((players_actual[i]["coordinates"][j][0]-1, players_actual[i]["coordinates"][j][1]-1))
            
        list1 = potential_tiles
        list2 = index_version_of_free_tiles
        free_potential_tiles = [value for value in list1 if value in list2]
        try:
            random_tile = random.choice(free_potential_tiles)
            list2.remove(random_tile)
            if random_tile != None:
                map_free_tiles -= 1
                players_actual[i]["coordinates"].append(random_tile)
                players_actual[i]["num_of_tiles"] += 1
                #free_potential_tiles.clear()
                #potential_tiles.clear()
                if map_free_tiles == 0:
                    return map_free_tiles
        except IndexError:
            pass
        free_potential_tiles.clear()
        potential_tiles.clear()
    return map_free_tiles

# is encircled function, checks if a tile is encircled on all sides, if yes, than it has a higher chance of being attacked, this makes the map more pretty
def is_encircled(tile, player_controling):
    bordering_tiles = []
    # 4 directions encirclement check (left, right, up, down)
    bordering_tiles.append((tile[0]+1, tile[1]))
    bordering_tiles.append((tile[0]-1, tile[1]))
    bordering_tiles.append((tile[0], tile[1]+1))
    bordering_tiles.append((tile[0], tile[1]-1))
    # diagonal encirclement check (up-right, up-left, down-right, down-left)
    bordering_tiles.append((tile[0]+1, tile[1]+1))
    bordering_tiles.append((tile[0]-1, tile[1]+1))
    bordering_tiles.append((tile[0]+1, tile[1]-1))
    bordering_tiles.append((tile[0]-1, tile[1]-1))
    answer = 0
    for i in bordering_tiles:
        for j in range(len(players_actual[player_controling]["coordinates"])):
            if players_actual[player_controling]["coordinates"][j] == i:
                answer += 1
            else:
                pass
                
    if answer == 0:
        return False
    else:
        return True
    
# this function decides which tiles are of interest to other functions, and hopefully will make the game run not necceserily faster but it could make the speed of the game more stable, provided that it will work like I think it will
# its now not fully operational and implementing is under way
# curently it does something weird in this place, but I think it could have something to do with the fact that theres multiple threads trying to access the same list, I will try to fix it
def optimalization():
    global players_actual, players_actual_tiles_of_interest, running, not_end, game_speed, num_players
    play = players_actual.copy()
    print(play)
    temp = []
    numberofruns = 0

    while not_end:
        print("outer loop running")
        while running:
            print("inner loop running")
            # this list will be cleared every run, otherwise it will keep adding the same tiles to the list causing the list to grow and eventually bug out
            players_actual_tiles_of_interest.clear()

            # filing the list with the coordinates of all the players, if coordinates are already in the list they will be ignored
            for i in range(num_players):
                players_actual_tiles_of_interest.append(play[i]["coordinates"])
            
            # if the tiles in players_actual_tiles_of_interest have a neighbour that is in other players tiles than they can stay, the tiles that do not will be removed, here was the bug, what it basicaly did is it didnt find a neighbour and therefore assumed that it it self is a neighbour, this is fixed now
            for i in range(num_players):
                for j in range(len(players_actual_tiles_of_interest)):
                    for k in range(len(players_actual_tiles_of_interest[j])):
                        if (players_actual_tiles_of_interest[j][k][0]+1, players_actual_tiles_of_interest[j][k][1]) in play[i]["coordinates"] or (players_actual_tiles_of_interest[j][k][0], players_actual_tiles_of_interest[j][k][1]+1) in play[i]["coordinates"] or (players_actual_tiles_of_interest[j][k][0]-1, players_actual_tiles_of_interest[j][k][1]) in play[i]["coordinates"] or (players_actual_tiles_of_interest[j][k][0], players_actual_tiles_of_interest[j][k][1]-1) in play[i]["coordinates"] or (players_actual_tiles_of_interest[j][k][0]+1, players_actual_tiles_of_interest[j][k][1]+1) in play[i]["coordinates"] or (players_actual_tiles_of_interest[j][k][0]-1, players_actual_tiles_of_interest[j][k][1]+1) in play[i]["coordinates"] or (players_actual_tiles_of_interest[j][k][0]+1, players_actual_tiles_of_interest[j][k][1]-1) in play[i]["coordinates"] or (players_actual_tiles_of_interest[j][k][0]-1, players_actual_tiles_of_interest[j][k][1]-1) in play[i]["coordinates"]:
                            pass
                        elif i == j:
                            pass
                        else:
                            temp.append(players_actual_tiles_of_interest[j][k])


            # removing the tiles that do not have a neighbour from players_actual_tiles_of_interest, uses count() to check if the tile is in the temp list enough times to justify removing it
            for i in range(len(temp)):
                for j in range(len(players_actual_tiles_of_interest)):
                    for k in range(len(players_actual_tiles_of_interest[j])):
                        for h in range(len(temp)):
                            try:
                                if temp[h] == players_actual_tiles_of_interest[j][k]:
                                    count = Counter(temp)
                                    if count[temp[i]] == num_players-1 or count[temp[i]] > num_players-1:
                                        try:
                                            print("removing tile")
                                            list1 = players_actual_tiles_of_interest[j]
                                            print("list conversion done")
                                            print(list1)
                                            print(temp[i])
                                            list1.remove(temp[i])
                                            print("removal done")
                                            
                                            #players_actual_tiles_of_interest[j].remove(temp[i])
                                        except ValueError:
                                            print("value error")
                                    else:
                                        pass
                            except IndexError:
                                pass
                            else:
                                pass

            #print(players_actual_tiles_of_interest)
            
            temp.clear()
            count.clear()

            
            print("thread 3 running")
            numberofruns += 1
            if numberofruns == 5:
                stop_thread()
                #running = False
                #not_end = False

            time.sleep(game_speed)


    


# stopping all functions in case of exiting the game
def stop_all_functions():
    global running
    players_actual.clear()
    running = False

# Function that basically starts all functions again after the game is reseted to initial state
def start_all_functions():
    global running
    running = True

# function to control the game reseting
def game_full_reset():
    global reset_game
    reset_game = True

# function to reset the reset_game variable
def reset_reset_game():
    global reset_game
    reset_game = False

# Function to stop the thread
def stop_thread():
    global not_end
    not_end = False
