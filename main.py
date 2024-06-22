# futere updates will adress the sometimes present error and will potentialy include multicoring as current one thread is starting to be not enough
# Also peace function will have to be advanced, currently its only temporary solution
# Final core function will be added and thats the battle function, it will use chances to determine who would win



import pygame
import random
import time


pygame.init()

# map logic and free tiles logic
map_size = 100
pixel_size = 5
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
num_players = 5
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


# expansion logic function, finds free tiles around all the player controled ones
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
        #possible errors may be happening here, working on it
        try:
            index_version_of_free_tiles.remove(players[i]["coordinates"][0])
        except ValueError:
            pass
# battle logic function, decides how the war will go
def battle_logic():
    pass

# peace logic function, removes players from wars list, currently peaces out with all other players 
# eventualy only one war will be peaced out, working on it

def peace_logic(player):
    print(player)
    possible_peace = []
    for i in range(len(wars)):
        if wars[i][0] == player or wars[i][1] == player:
            possible_peace.append(i)
    print(possible_peace)
    m = 0
    for i in possible_peace:
        wars.pop(i-m)
        m += 1
    print(wars)

# war logic function, decides how will war be implemented between 2 players
def war_logic(player):
    enemy = random.randint(0, num_players-1)
    if enemy == player or (player, enemy) in wars or (enemy, player) in wars:
        print("war not declared, invalid enemy or war already declared")
    else:
        wars.append((player, enemy))
    print(wars)

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
            print("peace declared")
            peace_logic(i)
        elif choice == "war":
            print("war declared")
            war_logic(i)
        else:
            pass
    
# war rearenge function, rearenges the indexes of the wars list, so that the first index is always larger than the second
def wars_rearenge():
    for i in range(len(wars)):
        if wars[i][0] < wars[i][1]:
            pass
        else:
            wars[i] = (wars[i][1], wars[i][0])



running = True
initial_check = True



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
        for i in range(num_players):
            for j in range(num_players):
                if i == j:
                    pass
                elif players[i]["coordinates"] == players[j]["coordinates"]:
                    list_of_similar = []
                    list_of_similar.append(i)
                    list_of_similar.append(j)
                    players[random.choice(list_of_similar)]["coordinates"] = (random.randint(0, map_size-1), random.randint(0, map_size-1))
                    
                    list_of_similar.clear()
                elif players[i]["color"] == players[j]["color"]:
                    list_of_similar.append(i)
                    list_of_similar.append(j)
                    players[random.choice(list_of_similar)]["color"] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    list_of_similar.clear()

    # removing occupied tiles from free tiles
        remove_occupied_tiles()
         
    #check is done
        initial_check = False

    # Drawing players and player controlled tiles, can somehow generate errors, not sure why, posibly when they have some kind of wrong coordinates?
    # working on it
    for i in range(num_players):
        for j in range(len(players[i]["coordinates"])): 
            pygame.draw.rect(screen, players[i]["color"], (players[i]["coordinates"][j][0]*pixel_size, players[i]["coordinates"][j][1]*pixel_size, pixel_size, pixel_size))
            

    # peacefull expansion logic
    if map_free_tiles > 0:  
        expandsion_initial()
    else:
        wars_rearenge()
        diplomacy_logic()
        battle_logic()

    time.sleep(0.1)
    
    pygame.display.update()




pygame.quit()
