import pygame
import random


pygame.init()

# map logic and free tiles logic
map_size = 5
pixel_size = 50
controlwindowsize = pixel_size
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
        

# Screen setings
screen = pygame.display.set_mode((map_size*pixel_size+controlwindowsize, map_size*pixel_size))
pygame.display.set_caption("Pixel Strategy")
pygame.display.set_icon(pygame.image.load("Pixel_strategy/strategy.png"))


# creating players and setting their initial position
players = []
which_player_occupies_what = []
num_players = 2
for i in range(num_players):
    playercoords1 = (random.randint(0, map_size-1), random.randint(0, map_size-1))
    map_occupied_tiles.append((playercoords1 ))   
    players.append(
        {
            "color": (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
            "coordinates": (playercoords1[0], playercoords1[1]),
            "num_of_tiles": 1
        }
    )

    
def reset_game():
    pass


# expansion logic function, finds free tiles around all the player controled ones
def expandsion_initial():
    pass
    
        
# removing occupied tiles from free tiles
def remove_occupied_tiles():
    global map_free_tiles, map_occupied_tiles, index_version_of_free_tiles
    map_free_tiles -= num_players
    for i in range(num_players):
        map_occupied_tiles.append(players[i]["coordinates"])
        index_version_of_free_tiles.remove(players[i]["coordinates"])
    

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

    #which player has which tile
        for i in range(num_players):
            which_player_occupies_what.append(players[i]["coordinates"])

    # removing occupied tiles from free tiles
        remove_occupied_tiles()
         
    #check is done
        initial_check = False

    # Drawing players and player controlled tiles
    for i in range(num_players):
        pygame.draw.rect(screen, players[i]["color"], (players[i]["coordinates"][0]*pixel_size, players[i]["coordinates"][1]*pixel_size, pixel_size, pixel_size))
        for j in range(players[i]["num_of_tiles"]):
            pygame.draw.rect(screen, players[i]["color"], (players[i]["coordinates"][0]*pixel_size, players[i]["coordinates"][1]*pixel_size, pixel_size, pixel_size))

    # peacefull expansion logic   
    expandsion_initial()



    pygame.display.update()




pygame.quit()
