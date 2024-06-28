# Description: Main file of the game, here the game logic is implemented

import threading
import pygame
import random
import time
from strategy_functions import map_logic, remove_occupied_tiles, expandsion_initial, send_important_data, stop_all_functions

pygame.init()

# map logic and free tiles logic
map_size = 10
pixel_size = 20
ratio = (1, 2)
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

# game speed
game_speed = 0.09

# Screen setings
screen = pygame.display.set_mode((map_size*pixel_size+map_size*pixel_size/10, map_size*pixel_size))
pygame.display.set_caption("Pixel Strategy")
pygame.display.set_icon(pygame.image.load("Pixel_strategy/strategy.png"))
controlwindowsize = map_size*pixel_size/10

# creating players and setting their initial position
players = []
players_actual = []
num_players = 10
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
    
# drawing players and player controlled tiles, this cant be done in the functions file as pygame doesnt support this
def drawing_players():
    global running, num_players, players, screen, pixel_size
    players_actual = players
    while running:
        for i in range(num_players):
            for j in range(len(players_actual[i]["coordinates"])):
                try:
                    pygame.draw.rect(screen, players_actual[i]["color"], (players_actual[i]["coordinates"][j][0]*pixel_size, players_actual[i]["coordinates"][j][1]*pixel_size, pixel_size, pixel_size))
                except IndexError:
                    pass

def reset_game():
    pass


running = True
initial_check = True
Threads_started = False
sended = False
just_once = True

# trying to implement multithreading, maybe it will help with the performance
thread1 = threading.Thread(target=drawing_players)
thread2 = threading.Thread(target=map_logic, args=(game_speed, num_players))

# Main loop
while running:

    # Background color
    screen.fill((255, 255, 255))

    #control screen color and size
    pygame.draw.rect(screen, (50, 50, 50), (map_size*pixel_size, 0, controlwindowsize, map_size*pixel_size))

    #event checking
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop_all_functions()
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
        if just_once:
            map_free_tiles = remove_occupied_tiles(players, num_players, map_free_tiles, map_occupied_tiles, index_version_of_free_tiles)
            just_once = False
    
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
        if sended == False:
            send_important_data(players, num_players, pixel_size, screen)
            sended = True
        map_free_tiles = expandsion_initial(num_players,map_free_tiles, index_version_of_free_tiles)
        
    # starting the threads
    elif Threads_started == False and map_free_tiles == 0:
        thread1.start()
        thread2.start()
        Threads_started = True
    else:
        pass

    time.sleep(game_speed)

    pygame.display.update()




pygame.quit()
try:
    thread1.join()
    thread2.join()
except:
    pass
