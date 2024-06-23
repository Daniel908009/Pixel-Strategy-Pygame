            
def border_tiles_func(players, player1, player2):
    potential_tiles1 = []
    potential_tiles2 = []
    border_tiles = []
    # Needs to be completed, currently its only a basic idea
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
                for m in range(len(border_tiles)):
                    if i == border_tiles[m]:
                        pass
                    else:
                        border_tiles.append(i)
    for i in potential_tiles2:
        for j in range(len(players[player1]["coordinates"])):
            if i == players[player1]["coordinates"][j]:
                for m in range(len(border_tiles)):
                    if i == border_tiles[m]:
                        pass
                    else:
                        border_tiles.append(i)
    #potential_tiles1.clear()
    #potential_tiles2.clear()
    return border_tiles
        