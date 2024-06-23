# futere updates will adress and will potentialy include multicoring as current one thread is starting to be not enough
# Also peace function will have to be advanced, currently its only temporary solution
# Final core function will be added and thats the battle function, it will use chances to determine who would win


import threading
import pygame
import random
import time
from strategy_functions import border_tiles_func, battle_logic_core, change_of_owner

pygame.init()

# map logic and free tiles logic
map_size = 2
pixel_size = 50
map = []
map_free_tiles = map_size*map_size
map_occupied_tiles = []
index_version_of_free_tiles = []
for i in range(map_size):
    for j in range(map_size):
        map.append((0, 0))
for i in range(map_size):
    for j in range(map_size):
        index_version_of_free_tiles.append((i, j))

# diplomacy variables
wars = []

# Screen setings
screen = pygame.display.set_mode((map_size*pixel_size+map_size*pixel_size/10, map_size*pixel_size))
pygame.display.set_caption("Pixel Strategy")
pygame.display.set_icon(pygame.image.load("Pixel_strategy/strategy.png"))
controlwindowsize = map_size*pixel_size/10

# creating players and setting their initial position
players = []
num_players = 2
for i in range(num_players):
    playercoords1 = (random.randint(0, map_size-1), random.randint(0, map_size-1))
    map_occupied_tiles.append((playercoords1 ))   
    players.append(
        {
            "color": (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
            "coordinates": [(playercoords1[0], playercoords1[1])],
            "num_of_tiles": 1
        }
    )

    
def reset_game():
    pass

# expansion logic function, finds free tiles around all the player controled ones, currently only in 4 directions, will be expanded to 8 once the game is more advanced
def expandsion_initial():
    global map_free_tiles, map_occupied_tiles, index_version_of_free_tiles
    potential_tiles = []
    free_potential_tiles = []
    for i in range(num_players):
        for j in range(len(players[i]["coordinates"])):
            potential_tiles.append((players[i]["coordinates"][j][0]+1, players[i]["coordinates"][j][1]))
            potential_tiles.append((players[i]["coordinates"][j][0]-1, players[i]["coordinates"][j][1]))
            potential_tiles.append((players[i]["coordinates"][j][0], players[i]["coordinates"][j][1]+1))
            potential_tiles.append((players[i]["coordinates"][j][0], players[i]["coordinates"][j][1]-1))
        list1 = potential_tiles
        list2 = index_version_of_free_tiles
        free_potential_tiles = [value for value in list1 if value in list2]
        try:
            random_tile = random.choice(free_potential_tiles)
            map_free_tiles -= 1
            index_version_of_free_tiles.remove(random_tile)
            players[i]["coordinates"].append(random_tile)
            players[i]["num_of_tiles"] += 1
            free_potential_tiles.clear()
            potential_tiles.clear()
        except IndexError:
            pass


        
# removing occupied tiles from free tiles
def remove_occupied_tiles():
    global map_free_tiles, map_occupied_tiles, index_version_of_free_tiles
    map_free_tiles -= num_players
    for i in range(num_players):
        map_occupied_tiles.append(players[i]["coordinates"][0])
        try:
            index_version_of_free_tiles.remove(players[i]["coordinates"][0])
        except ValueError:
            pass

# battle logic function, decides how the war will go, it uses the power of players to determine the chances of wining in each battle for each tile
# specific functions are in strategy_functions.py
def battle_logic():
    if len(wars) == 0:
        pass
    else:
        for i in range(len(wars)):
            global players
            player1 = wars[i][0]
            player2 = wars[i][1]
            power1 = players[player1]["num_of_tiles"]
            power2 = players[player2]["num_of_tiles"]
            tile_attacked = []
            border_tiles = []
            winner_of_battle = []
            border_tiles.append(border_tiles_func(players, player1, player2))
            tile_attacked.append(random.choice(border_tiles[0]))
            winner_of_battle.append(battle_logic_core(power1, power2, player1, player2))
            print("--------------------")
            players = change_of_owner(winner_of_battle, tile_attacked, players, player1, player2)
            print(players)
            border_tiles.clear()

# peace logic function, removes players from wars list, currently peaces out with all other players 
# eventualy only one war will be peaced out, working on it
def peace_logic(player):
    possible_peace = []
    for i in range(len(wars)):
        if wars[i][0] == player or wars[i][1] == player:
            possible_peace.append(i)
    m = 0
    for i in possible_peace:
        wars.pop(i-m)
        m += 1
    

# war logic function, decides how will war be implemented between 2 players
def war_logic(player):
    enemy = random.randint(0, num_players-1)
    if enemy == player or (player, enemy) in wars or (enemy, player) in wars:
        pass
    else:
        wars.append((player, enemy))

# diplomacy logic function, decides what will happen between players
def diplomacy_logic():
    chance_of_nothing = 10
    diplomacy_options = []
    chance_of_peace = 3
    chance_of_war = 5
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
            war_logic(i)
        else:
            pass

 # Drawing players and player controlled tiles, now fully working!!!    
def drawing_players():
    while running:
        for i in range(num_players):
            for j in range(len(players[i]["coordinates"])): 
                pygame.draw.rect(screen, players[i]["color"], (players[i]["coordinates"][j][0]*pixel_size, players[i]["coordinates"][j][1]*pixel_size, pixel_size, pixel_size))
    
# Map logic function, manages the diplomacy and battle logic
def map_logic():
    while running:
        diplomacy_logic()
        battle_logic()
        time.sleep(0.4)
        


running = True
initial_check = True
Threads_started = False

# trying to implement multithreading, maybe it will help with the performance
thread1 = threading.Thread(target=drawing_players)
thread2 = threading.Thread(target=map_logic)

# Main loop
while running:

    # Background color
    screen.fill((255, 255, 255))

    #control screen color and size
    pygame.draw.rect(screen, (50, 50, 50), (map_size*pixel_size, 0, controlwindowsize, map_size*pixel_size))

    #event checking
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.type == pygame.r:
                reset_game()
    
    # checking if players are not on top of each other
    while initial_check:
        needs_recheck = False
        for i in range(num_players):
            for j in range(num_players):
                if i == j:
                    pass
                elif players[i]["coordinates"][0] == players[j]["coordinates"][0]:
                    list_of_similar = []
                    list_of_similar.append(i)
                    list_of_similar.append(j)
                    players[random.choice(list_of_similar)]["coordinates"][0] = (random.randint(0, map_size-1), random.randint(0, map_size-1))
                    list_of_similar.clear()
                    needs_recheck = True
                elif players[i]["color"] == players[j]["color"]:
                    list_of_similar.append(i)
                    list_of_similar.append(j)
                    players[random.choice(list_of_similar)]["color"] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    list_of_similar.clear()

    # removing occupied tiles from free tiles
        remove_occupied_tiles()
         
    #check is done
        if needs_recheck:
            initial_check = True
        else:
            initial_check = False

    # initial drawing of players, threading had some issues with this part, therefore it is implemented like this
    if Threads_started == False:
        for i in range(num_players):
            for j in range(len(players[i]["coordinates"])): 
                pygame.draw.rect(screen, players[i]["color"], (players[i]["coordinates"][j][0]*pixel_size, players[i]["coordinates"][j][1]*pixel_size, pixel_size, pixel_size))

    # peacefull expansion logic
    if map_free_tiles > 0:  
        expandsion_initial()
    # starting the threads
    elif Threads_started == False and map_free_tiles == 0:
        thread1.start()
        thread2.start()
        Threads_started = True
    else:
        pass

    time.sleep(0.4)

    pygame.display.update()




pygame.quit()
