import pygame
import random


pygame.init()

# map logic and free tiles logic
map_size = 5
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
screen = pygame.display.set_mode((map_size*100, map_size*100))
pygame.display.set_caption("Pixel Strategy")
#pygame.display.set_icon(pygame.image.load("assets/icon.png"))


# creating players and setting their initial position
players = []
num_players = 2
for i in range(num_players):
    playercoords1 = (random.randint(0, map_size-1), random.randint(0, map_size-1))
    playercoords2 = (random.randint(0, map_size-1), random.randint(0, map_size-1))
    map_occupied_tiles.append((playercoords1, playercoords2))   
    players.append(
        {
            "color": (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
            "coordinates": (playercoords1, playercoords2),
            "num_of_tiles": 1
        }
    )


# logic for finding free tile around player
def logic_for_finding_nearest_free_tile(player):
        for m in range(players.num_of_tiles):
            coords = players[player].coordinates[m-1]
            coords_to_check = []
            for i in range(3):
                for j in range(3):
                    coords_to_check.append((coords[0]-1+i, coords[1]-1+j))
                    print(coords_to_check)
    




# expansion logic function
def expandsion_initial():
    global map_free_tiles, players
    for i in range(num_players):
        players[i-1].coordinates.append(logic_for_finding_nearest_free_tile(i))
        pass
    


running = True
initial_check = True

# Main loop
while running:

    # Background color
    screen.fill((0, 0, 0))
    #event checking
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Drawing map
    for i in range(map_size):
        for j in range(map_size):
            pygame.draw.rect(screen, (255, 255, 255), (i*100, j*100, 100, 100))
    
    # checking if players are not on top of each other
    while initial_check:
        for i in range(num_players):
            for j in range(num_players):
                if i == j:
                    continue
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
    map_free_tiles -= num_players
    print(len(map_free_tiles))
    for i in range(len(map_occupied_tiles)):
        index_version_of_free_tiles.remove(map_occupied_tiles[i][i+1])
        i+=2
        print(index_version_of_free_tiles)

    initial_check = False

    # Drawing players
    current_round = 1
    for player in players:
        for i in range(current_round):
            for j in range(current_round):
                pygame.draw.rect(screen, player["color"], (player["coordinates"][i-1][0]*100, player["coordinates"][i-1][1]*100, 100, 100))
    current_round += 1

    # peacefull expansion logic   
    #expandsion_initial()



    pygame.display.update()




pygame.quit()





pygame.quit()
