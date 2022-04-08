# # Author: Joaquin CORNEJO
# # Scape game 
# 08/04/2022
# ==========================
from FUNCTIONS import *

# Initialiser l'écran
wn = turtle.Screen()
wn.tracer(0) 

# Tracer le plan
turtle.hideturtle()
matrice = lire_matrice(fichier_plan)
tracer_zone_chateau()
tracer_zone_annonces()
tracer_zone_inventaire()
afficher_plan(matrice)

# Mise à jourd de l'écran   
wn.update() 
wn.mainloop() 


