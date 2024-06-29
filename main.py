# Description: Main file of the game, here the game logic is implemented

import threading
import pygame
import random
import time
from strategy_functions import map_logic, remove_occupied_tiles, expandsion_initial, send_important_data, stop_all_functions, start_all_functions, stop_thread, game_full_reset, reset_reset_game

pygame.init()

# map logic and free tiles logic
map_size = 28
pixel_size = 20
ratio = (1, 2)
map = []
map_occupied_tiles = []
index_version_of_free_tiles = []


# diplomacy variables
wars = []

# game speed
game_speed = 0.09

# Screen setings
screen = pygame.display.set_mode(((map_size*pixel_size+map_size*pixel_size/3)*ratio[1], (map_size*pixel_size)*ratio[0]))
pygame.display.set_caption("Pixel Strategy")
pygame.display.set_icon(pygame.image.load("Pixel_strategy/strategy.png"))
controlwindowsize = (map_size*pixel_size/3)*ratio[1]

# creating map and free tiles
map_free_tiles = (map_size*ratio[0])*(map_size*ratio[1])
for i in range(map_size*ratio[1]):
    for j in range(map_size*ratio[0]):
        map.append((0, 0))
for i in range(map_size*ratio[1]):
    for j in range(map_size*ratio[0]):
        index_version_of_free_tiles.append((i, j))

# creating players and setting their initial position
players = []
players_actual = []
num_players = 20
for i in range(num_players):
    playercoords1 = (random.randint(0, (map_size-1)*ratio[1]), random.randint(0, (map_size-1)*ratio[0]))
    map_occupied_tiles.append((playercoords1 ))   
    players.append(
        {
            "color": (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
            "coordinates": [(playercoords1[0], playercoords1[1])],
            "num_of_tiles": 1
        }
    )
    
# drawing players and player controlled tiles, this cant be done in the functions file as pygame doesnt support this kind of thing
def drawing_players():
    global running, num_players, players, screen, pixel_size
    players_actual = players
    while not_end:
        while running:
            try:
                for i in range(num_players):
                    for j in range(len(players_actual[i]["coordinates"])):
                        try:
                            pygame.draw.rect(screen, players_actual[i]["color"], (players_actual[i]["coordinates"][j][0]*pixel_size, players_actual[i]["coordinates"][j][1]*pixel_size, pixel_size, pixel_size))
                        except IndexError:
                            pass
            except IndexError:
                    pass
  
# function for reseting the game and setting the initial values again, currently working only partially, threading has some issues with this part
def reset_game():
    global map_free_tiles, index_version_of_free_tiles, initial_check, just_once, Threads_started, sended, running, map_occupied_tiles, initial_expansion_done
    map_occupied_tiles.clear()
    players.clear()
    for i in range(num_players):
        playercoords1 = (random.randint(0, (map_size-1)*ratio[1]), random.randint(0, (map_size-1)*ratio[0]))
        map_occupied_tiles.append((playercoords1 ))
        players.append(
        {
            "color": (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
            "coordinates": [(playercoords1[0], playercoords1[1])],
            "num_of_tiles": 1
        }
        )
    map_free_tiles = (map_size*ratio[0])*(map_size*ratio[1])
    index_version_of_free_tiles.clear()
    for i in range(map_size*ratio[1]):
        for j in range(map_size*ratio[0]):
            index_version_of_free_tiles.append((i, j))
    initial_check = True
    just_once = True
    sended = False
    running = False
    stop_all_functions()
    time.sleep(0.1)
    running = True
    start_all_functions()
    game_full_reset()
    initial_expansion_done = False



running = True
initial_check = True
Threads_started = False
sended = False
just_once = True
not_end = True
initial_expansion_done = False

# trying to implement multithreading, maybe it will help with the performance
thread1 = threading.Thread(target=drawing_players)
thread2 = threading.Thread(target=map_logic, args=(game_speed, num_players))

# Main loop
while running:

    # Background color
    screen.fill((255, 255, 255))

    #control screen color and size
    pygame.draw.rect(screen, (50, 50, 50), ((map_size*pixel_size)*ratio[1], 0, controlwindowsize, (map_size*pixel_size)*ratio[0] ))
    #buttons inside control screen
    pygame.draw.rect(screen, (0, 0, 0), ((map_size*pixel_size)*ratio[1]+controlwindowsize/50, (map_size*pixel_size)*ratio[0]/20, controlwindowsize-controlwindowsize/20, (map_size*pixel_size)*ratio[0]/5))
    pygame.draw.rect(screen, (0, 0, 0), ((map_size*pixel_size)*ratio[1]+controlwindowsize/50, (map_size*pixel_size)*ratio[0]/2, controlwindowsize-controlwindowsize/20, (map_size*pixel_size)*ratio[0]/12))

    #text inside buttons
    font = pygame.font.Font(None, int((map_size*pixel_size)*ratio[0]/12))
    text = font.render("Reset", True, (255, 255, 255))
    screen.blit(text, ((map_size*pixel_size)*ratio[1]+controlwindowsize/2.5, (map_size*pixel_size)*ratio[0]/2))

    #event checking
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop_all_functions()
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                stop_all_functions()
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if(map_size*pixel_size)*ratio[1]+controlwindowsize/50 <= mouse[0] <= (map_size*pixel_size)*ratio[1]+controlwindowsize-controlwindowsize/20 and (map_size*pixel_size)*ratio[0]/2 <= mouse[1] <= (map_size*pixel_size)*ratio[0]/2+(map_size*pixel_size)*ratio[0]/12:
                reset_game()
            elif (map_size*pixel_size)*ratio[1]+controlwindowsize/50 <= mouse[0] <= (map_size*pixel_size)*ratio[1]+controlwindowsize-controlwindowsize/20 and (map_size*pixel_size)*ratio[0]/20 <= mouse[1] <= (map_size*pixel_size)*ratio[0]/20+(map_size*pixel_size)*ratio[0]/5:
                pass
    
    # checking if players are not on top of each other
    while initial_check:
        needs_recheck = False
        for i in range(num_players):
            for j in range(num_players):
                try:
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
                        needs_recheck = True
                except IndexError:
                    needs_recheck = True

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
        try:
            if sended == False:
                send_important_data(players, num_players, pixel_size, screen)
                sended = True
            map_free_tiles = expandsion_initial(num_players,map_free_tiles, index_version_of_free_tiles)
            initial_expansion_done = True
        except IndexError:
            pass

    # starting the threads
    elif Threads_started == False and map_free_tiles == 0:
        thread1.start()
        thread2.start()
        Threads_started = True
    else:
        if initial_expansion_done:
            reset_reset_game()
        else:
            pass        

    time.sleep(game_speed)
    pygame.display.update()




pygame.quit()
stop_all_functions()
not_end = False
stop_thread()

try:
    thread1.join()
    thread2.join()
except:
    pass
