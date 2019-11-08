from random import *

# Init your variables here 

# Put your bot name here
name = "Bender"

# Bender strategy : return the first element in the available cells.
# That always generates horizontal line in the top of the board 

def play(board, available_cells, player):
    return available_cells[0]