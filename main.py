import pygame
import random
import time


pygame.init()

# map logic and free tiles logic
map_size = 40
pixel_size = 20
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
num_players = 40
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
        index_version_of_free_tiles.remove(players[i]["coordinates"][0])
    
# battle logic function, decides how the war will go
def battle_logic():
    pass

# peace logic function, decides how will peace be implemented
def peace_logic(player):
    if player in wars:
        i = wars.index(player)
        wars.pop(i)

# war logic function, decides how will war be implemented between 2 players
def war_logic(player):
    enemy = random.choice(players)
    if enemy == player:
        war_logic(player)
    else:
        wars.append((player, enemy))

# diplomacy logic function, decides what will happen between players
def diplomacy_logic():
    chance_of_action = 10000
    diplomacy_options = ["peace","war"]
    for i in range(chance_of_action):
        diplomacy_options.append("nothing")
    for i in range(num_players):
        choice = random.choice(diplomacy_options)
        if choice == "peace":
            peace_logic(i)
        elif choice == "war":
            war_logic(i)
        else:
            pass
    

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

    # Drawing players and player controlled tiles
    for i in range(num_players):
        for j in range(len(players[i]["coordinates"])): 
            pygame.draw.rect(screen, players[i]["color"], (players[i]["coordinates"][j][0]*pixel_size, players[i]["coordinates"][j][1]*pixel_size, pixel_size, pixel_size))
            

    # peacefull expansion logic
    if map_free_tiles > 0:  
        expandsion_initial()
    else:
        diplomacy_logic()
        battle_logic()

    time.sleep(0.4)
    
    print(wars)    

    pygame.display.update()




pygame.quit()
