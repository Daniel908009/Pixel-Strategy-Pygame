# This file contains all the functions that are used in the main file

#necessary imports
import random
import time
import pygame

# global variables
players_actual = []
wars = []

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
    


# Function to change the owner of the tile after the battle
def change_of_owner(winner_of_battle, tile_attacked, players, player1, player2):
    ply = players.copy()
    print("change is about to happen")
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
def map_logic(running, game_speed, num_players):
    global wars
    while running:
        diplomacy_logic(num_players)
        battle_logic()
        time.sleep(game_speed)


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
        for i in range(len(wars)):
            player1 = wars[i][0]
            player2 = wars[i][1]
            print("battle is about to happen")
            print(player1, player2)
            print(players_actual[player1]["num_of_tiles"], players_actual[player2]["num_of_tiles"])

            power1 = players_actual[player1]["num_of_tiles"]
            power2 = players_actual[player2]["num_of_tiles"]
            tile_attacked = []
            border_tiles = []
            winner_of_battle = 0
            border_tiles.append(border_tiles_func(players_actual, player1, player2))
            try:
                tile_attacked.append(random.choice(border_tiles[0]))
                winner_of_battle= battle_logic_core(power1, power2, player1, player2)
                players_actual = change_of_owner(winner_of_battle, tile_attacked[0], players_actual, player1, player2)
                border_tiles.clear()
                tile_attacked.clear()
            except IndexError:
                pass
           
# removing occupied tiles from free tiles
def remove_occupied_tiles(players, num_players, map_free_tiles, map_occupied_tiles, index_version_of_free_tiles):
    map_free_tiles -= num_players
    for i in range(num_players):
        map_occupied_tiles.append(players[i]["coordinates"][0])
        try:
            index_version_of_free_tiles.remove(players[i]["coordinates"][0])
        except ValueError:
            pass
    return map_free_tiles

# expansion logic function, finds free tiles around all the player controled ones, currently only in 4 directions, will be expanded to 8 once the game is more advanced
def expandsion_initial(num_players,map_free_tiles, map_occupied_tiles, index_version_of_free_tiles):
    potential_tiles = []
    free_potential_tiles = []
    for i in range(num_players):
        for j in range(len(players_actual[i]["coordinates"])):
            potential_tiles.append((players_actual[i]["coordinates"][j][0]+1, players_actual[i]["coordinates"][j][1]))
            potential_tiles.append((players_actual[i]["coordinates"][j][0]-1, players_actual[i]["coordinates"][j][1]))
            potential_tiles.append((players_actual[i]["coordinates"][j][0], players_actual[i]["coordinates"][j][1]+1))
            potential_tiles.append((players_actual[i]["coordinates"][j][0], players_actual[i]["coordinates"][j][1]-1))
        list1 = potential_tiles
        list2 = index_version_of_free_tiles
        free_potential_tiles = [value for value in list1 if value in list2]
        try:
            random_tile = random.choice(free_potential_tiles)
            index_version_of_free_tiles.remove(random_tile)
            map_free_tiles -= 1
            players_actual[i]["coordinates"].append(random_tile)
            players_actual[i]["num_of_tiles"] += 1
            free_potential_tiles.clear()
            potential_tiles.clear()
        except IndexError:
            pass
    return map_free_tiles
