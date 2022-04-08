# # Author: Joaquin CORNEJO
# # Scape game 
# 08/04/2022
# ==========================
from FUNCTIONS import *

global matrice, position, pas, dictionnaire, list_objets, questions

# Define mouvements
def deplacer_gauche():
    global matrice, position, pas, dictionnaire, list_objets, questions
    turtle.onkeypress(None, "Left") 
    position_new, matrice_new, list_objets_new = \
        deplacer(questions, dictionnaire, list_objets, matrice, position, pas, [0, -1]) 
    position = position_new
    matrice = matrice_new
    list_objets = list_objets_new
    turtle.onkeypress(deplacer_gauche, "Left")   
    return

def deplacer_droite():
    global matrice, position, pas, dictionnaire, list_objets, questions
    turtle.onkeypress(None, "Right")  
    position_new, matrice_new, list_objets_new =\
        deplacer(questions, dictionnaire, list_objets, matrice, position, pas, [0, 1]) 
    position = position_new
    matrice = matrice_new
    list_objets = list_objets_new
    turtle.onkeypress(deplacer_droite, "Right")  
    return

def deplacer_haut():
    global matrice, position, pas, dictionnaire, list_objets, questions
    turtle.onkeypress(None, "Up")   
    position_new, matrice_new, list_objets_new =\
        deplacer(questions, dictionnaire, list_objets, matrice, position, pas, [-1, 0]) 
    position = position_new
    matrice = matrice_new
    list_objets = list_objets_new
    turtle.onkeypress(deplacer_haut, "Up")   
    return

def deplacer_bas():
    global matrice, position, pas, dictionnaire, list_objets, questions
    turtle.onkeypress(None, "Down") 
    position_new, matrice_new, list_objets_new =\
        deplacer(questions, dictionnaire, list_objets, matrice, position, pas, [1, 0]) 
    position = position_new
    matrice = matrice_new
    list_objets = list_objets_new
    turtle.onkeypress(deplacer_bas, "Down")   
    return

# Definir variables
matrice = lire_matrice(fichier_plan)
dictionnaire = creer_dictionnaire_des_objets(fichier_objets)
questions = creer_dictionnaire_des_objets(fichier_questions)
pas = calculer_pas(matrice)
position = list(POSITION_DEPART)
list_objets = []

# Initialiser l'écran
wn = turtle.Screen()
wn.tracer(0) 
turtle.hideturtle()

# Tracer le plan
tracer_zone_chateau()
tracer_zone_annonces()
tracer_zone_inventaire()
afficher_plan(matrice, pas)
tracer_personnage(position, pas)
wn.update()

# Déplacements
turtle.listen()   
turtle.onkeypress(deplacer_gauche, "Left")   
turtle.onkeypress(deplacer_droite, "Right")
turtle.onkeypress(deplacer_haut, "Up")
turtle.onkeypress(deplacer_bas, "Down")

# Loop
turtle.mainloop()



