# Author: Joaquin CORNEJO
# Scape game 

# Python libraries
import numpy as np
import turtle

# My libraries
from CONFIGS import * 
from CASTLE import Castle

# Set name of the file containing the castle map
filename = fichier_plan

# Initialize screen
wn = turtle.Screen()

# This turns off screen updates 
wn.tracer(0) 

# Create game
Castle(filename)

# Update the screen to see the changes   
wn.update() 

# Keep the window open
wn.mainloop() 