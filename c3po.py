from random import *

# Init your variables here 

# Put your bot name here
name = "C3PO"

# C3PO strategy : return random available celle 

def play(board, available_cells, player):
    return available_cells[randint(0,len(available_cells)-1)]