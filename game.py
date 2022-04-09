# # Author: Joaquin CORNEJO
# # Scape game 
# 08/04/2022
# ==========================
# Python libraries
import operator
import numpy as np
import turtle

# My configurations
from CONFIGS import *

# ---------------------------------
# NIVEAU 1: AFFICHAGE DU PLAN
# ---------------------------------
def lire_matrice(fichier): 
    
    # Ovrir fichier texte
    matrix = np.loadtxt(fichier, dtype='i', delimiter=' ')

    return matrix.tolist()

def calculer_pas(matrice):
    # Trouver les dimensions de la matrice
    (nb_lignes, nb_cols) = np.asarray(matrice).shape

    # Définir dimensions
    largeur = abs(ZONE_PLAN_MAXI[0] - ZONE_PLAN_MINI[0])
    hauteur = abs(ZONE_PLAN_MAXI[1] - ZONE_PLAN_MINI[1])

    # Trouver la dimension de la case (le pas)
    pas = min(hauteur/nb_lignes, largeur/nb_cols)

    return pas

def coordonnees(case, pas): 
    # Définir les coordonnées du coin inférieur 
    offsetx = ZONE_PLAN_MINI[0]
    offsety = ZONE_PLAN_MAXI[1] 

    # Trouver la position du coin inférieur à gauche de la case
    posy = -(case[0] + 1)*pas
    posx = case[1]*pas

    # Nouvelle position avec les off-sets
    posx += offsetx
    posy += offsety

    return [posx, posy]

def tracer_carre(pas):  
    for _  in range(4):
        turtle.forward(pas) 
        turtle.left(90) 
    return

def tracer_case(case, couleur, pas): 

    # Trouver les coordonnées initiales
    coord = coordonnees(case, pas)

    # Positionner le crayon aux coordonnées initiales
    turtle.penup()
    turtle.goto(coord[0], coord[1])
    turtle.pendown()

    # Tracer un carré avec un remplissage de couleur définie
    turtle.fillcolor(couleur)
    turtle.begin_fill()
    tracer_carre(pas)
    turtle.end_fill()
    turtle.penup()

    return

def afficher_plan(matrice, pas): 
    # Trouver les dimensions de la matrice
    (nb_lignes, nb_cols) = np.asarray(matrice).shape

    # Tracer le plan 
    for i in range(nb_lignes): 
        for j in range(nb_cols): 
            case = [i, j]
            couleur = COULEURS[matrice[i][j]]
            tracer_case(case, couleur, pas)

    return

def tracer_rectangle(init= (0, 0), fin= (1, 1), color= COULEUR_EXTERIEUR): 

    # Définir position initial (coin inférieur gauche)
    x0 = min(init[0], fin[0])
    y0 = min(init[1], fin[1])

    # Définir position final (coin supérieur droit)
    x1 = max(init[0], fin[0])
    y1 = max(init[1], fin[1])

    # Dimensions
    longx = abs(x1-x0)
    longy = abs(y1-y0) 
    if longx*longy == 0: raise Warning('Dimensions are zero') 

    # Aller à la position initial
    turtle.penup()
    turtle.goto(x0, y0)
    turtle.pendown()

    # Définir la couleur
    turtle.fillcolor(color)
    turtle.begin_fill()
    
    for _ in range(4):
        if _ % 2 == 0: # Largeur
            turtle.forward(longx) 
            turtle.left(90) 
        else: # Hauteur
            turtle.forward(longy) 
            turtle.left(90)

    turtle.end_fill()
    turtle.penup()

    return

def tracer_zone_chateau(): 

    tracer_rectangle(init= ZONE_PLAN_MINI, 
                        fin= ZONE_PLAN_MAXI)
    return

def tracer_zone_annonces(): 

    tracer_rectangle(init= POINT_AFFICHAGE_ANNONCES, 
                    fin= POINT_AFFICHAGE_ANNONCES_FIN)
    return

def tracer_zone_inventaire():

    tracer_rectangle(init= POINT_AFFICHAGE_INVENTAIRE, 
                    fin= POINT_AFFICHAGE_INVENTAIRE_FIN)
    return 

# ---------------------------------
# NIVEAU 2: GESTION DE DEPLACEMENT
# ---------------------------------
def tracer_personnage(case, pas): 

    # Trouver les coordonnées initiales
    coord = coordonnees(case, pas)
    coord[0] += pas/2
    coord[1] += pas/2

    # Positionner le crayon aux coordonnées initiales
    turtle.penup()
    turtle.goto(coord[0], coord[1])
    turtle.pendown()

    # Tracer le personnage
    turtle.dot(RATIO_PERSONNAGE*pas, COULEUR_PERSONNAGE)
    turtle.penup()

    return

def deplacer(dico_questions: dict, dico_objets: dict, list_objets, 
            matrice, case, pas, mouvement): 

    # Définir les positions
    case_depart = np.asarray(case)
    case_arrivee = np.asarray(case) + np.asarray(mouvement)

    # Vérifier si la nouvelle position est valide (est dans la matrice)
    (nb_lignes, nb_cols) = np.asarray(matrice).shape
    is_mouvement_valide = True

    if (case_arrivee[0]<-1 or case_arrivee[0]<nb_lignes) and\
        (case_arrivee[1]>-1 and case_arrivee[1]<nb_cols): pass
    else: is_mouvement_valide = False

    # Vérifier si le mouvment est valide (n'est pas un mur)
    if matrice[case_arrivee[0]][case_arrivee[1]] != 1: pass
    else: is_mouvement_valide = False

    # Copier quelques variables
    matrice_actuelle = matrice.copy()
    liste_objets_actuelle = list_objets.copy()
    case_actuelle = case_depart

    if is_mouvement_valide :
        tracer_zone_annonces()
        if matrice[case_arrivee[0]][case_arrivee[1]] == 4: # Si dans la case il y a un objet
            case_actuelle = case_arrivee
            matrice_actuelle, liste_objets_actuelle = \
                ramasser_objet(dico_objets, list_objets, matrice, case_depart, case_arrivee, pas)

        elif matrice[case_arrivee[0]][case_arrivee[1]] == 3: # Si dans la case il y a une porte
            matrice_actuelle, case_actuelle =\
                poser_question(dico_questions, matrice, case_depart, case_arrivee, pas)

        else:
            case_actuelle = case_arrivee
            tracer_case(case_depart, COULEUR_CASES, pas)
            tracer_personnage(case_arrivee, pas)
        
    return case_actuelle, matrice_actuelle, liste_objets_actuelle

# ---------------------------------
# NIVEAU 3: COLLECTE D'OBJETS
# ---------------------------------
def ecrire_zone_annonces(text, offset_x= 120, offset_y= 10):

    # Definir le point au milieu pour l'affichage
    text_pos = tuple(map(operator.add, 
                POINT_AFFICHAGE_ANNONCES, POINT_AFFICHAGE_ANNONCES_FIN))

    # Ecrire texte
    tracer_zone_annonces()
    turtle.penup()
    turtle.goto(text_pos[0]/2-offset_x, text_pos[1]/2-offset_y)
    turtle.pendown()
    turtle.write(text, font=("Verdana", 14, "normal"))
    turtle.penup()

    return

def ecrire_zone_inventaire(text, offset_x= 70, offset_y= 0):

    # Definir le point au milieu pour l'affichage
    text_pos = tuple(map(operator.add, 
                POINT_AFFICHAGE_INVENTAIRE, POINT_AFFICHAGE_INVENTAIRE_FIN))

    # Ecrire texte
    turtle.penup()
    turtle.goto(text_pos[0]/2-offset_x, text_pos[1]/2+80-offset_y)
    turtle.pendown()
    turtle.write(text, font=("Verdana", 10, "normal"))
    turtle.penup()

    return

def creer_dictionnaire(fichier_des_objets):
    with open(fichier_des_objets, 'r') as file:
        lignes = file.readlines()
        dictionnaire = {}
        for line in lignes:
            a, b = eval(line)
            dictionnaire[a] = b

    return dictionnaire

def ramasser_objet(dico_objets: dict, list_objets, 
                    matrice, case_depart, case_arrivee, pas):

    # Affichage
    ecrire_zone_annonces("Vous avez trouvé: une clef à molette", offset_x=160)

    # Dessiner
    tracer_case(case_depart, COULEUR_CASES, pas)
    tracer_case(case_arrivee, COULEUR_CASES, pas)
    tracer_personnage(case_arrivee, pas)

    # Copier quelques variables
    matrice_new = matrice.copy()
    list_objets_new = list_objets.copy()

    # Modifier les variables 
    matrice_new[case_arrivee[0]][case_arrivee[1]] = 0  
    try: list_objets_new.append(dico_objets[tuple(case_arrivee)])
    except: pass

    # Ecrire texte
    tracer_zone_inventaire()
    for i, objet in enumerate(list_objets_new):
        ecrire_zone_inventaire(objet, offset_y= i*20)
    
    return matrice, list_objets_new

# ---------------------------------
# NIVEAU 4: QUESTIONS-REPONSES
# ---------------------------------
def poser_question(dico_questions: dict, matrice, case_depart, case_arrivee, pas):

    # Affichage zone d'annonces
    ecrire_zone_annonces("Cette porte est fermée")

    # Poser la question
    question_text = dico_questions[tuple(case_arrivee)][0]
    reponse = turtle.textinput("Question", question_text)
    turtle.listen()

    # Copier quelques variables
    matrice_actuelle = matrice.copy()
    case_actuelle = case_depart

    # Verifier si la réponse est correcte
    if reponse == dico_questions[tuple(case_arrivee)][1]:
        ecrire_zone_annonces("Cette porte est ouverte")

        # Dessiner
        tracer_case(case_depart, COULEUR_CASES, pas)
        tracer_case(case_arrivee, COULEUR_CASES, pas)
        tracer_personnage(case_arrivee, pas)

        # Modifier variables
        matrice_actuelle[case_arrivee[0]][case_arrivee[1]] = 0
        case_actuelle = case_arrivee

    else: 
        ecrire_zone_annonces("Mauvaise réponse", offset_x= 90)

    return matrice_actuelle, case_actuelle

def deplacer_gauche():
    global matrice, dico_objets, dico_questions, pas, position, list_objets
    turtle.onkeypress(None, "Left") 
    outputs = deplacer(dico_questions, dico_objets, list_objets, matrice, position, pas, [0, -1]) 
    position = outputs[0]
    matrice = outputs[1]
    list_objets = outputs[2]
    turtle.onkeypress(deplacer_gauche, "Left")   
    return

def deplacer_droite():
    global matrice, dico_objets, dico_questions, pas, position, list_objets
    turtle.onkeypress(None, "Right")  
    outputs = deplacer(dico_questions, dico_objets, list_objets, matrice, position, pas, [0, 1]) 
    position = outputs[0]
    matrice = outputs[1]
    list_objets = outputs[2]
    turtle.onkeypress(deplacer_droite, "Right")  
    return

def deplacer_haut():
    global matrice, dico_objets, dico_questions, pas, position, list_objets
    turtle.onkeypress(None, "Up")   
    outputs = deplacer(dico_questions, dico_objets, list_objets, matrice, position, pas, [-1, 0]) 
    position = outputs[0]
    matrice = outputs[1]
    list_objets = outputs[2]
    turtle.onkeypress(deplacer_haut, "Up")   
    return

def deplacer_bas():
    global matrice, dico_objets, dico_questions, pas, position, list_objets
    turtle.onkeypress(None, "Down") 
    outputs = deplacer(dico_questions, dico_objets, list_objets, matrice, position, pas, [1, 0]) 
    position = outputs[0]
    matrice = outputs[1]
    list_objets = outputs[2]
    turtle.onkeypress(deplacer_bas, "Down")   
    return

# ================================
# CODE PRINCIPAL
# ================================
# Definir variables globales
matrice = lire_matrice(fichier_plan)
dico_objets = creer_dictionnaire(fichier_objets)
dico_questions = creer_dictionnaire(fichier_questions)
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