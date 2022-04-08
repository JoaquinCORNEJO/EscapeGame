# Python libraries
import operator
import numpy as np
import turtle

# My configurations
from CONFIGS import *

# =================================
# NIVEAU 1: AFFICHAGE DU PLAN
# =================================

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
    posy = -(case[0]+1) * pas
    posx = case[1] * pas

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

# ---------------------------------
def tracer_rectangle(init= tuple([0, 0]), fin= tuple([1, 1]), color= COULEUR_EXTERIEUR): 

    # Set initial position (We consider bottom-left corner)
    x0 = min(init[0], fin[0])
    y0 = min(init[1], fin[1])

    # Set final position
    x1 = max(init[0], fin[0])
    y1 = max(init[1], fin[1])

    # Dimensions
    longx = abs(x1-x0)
    longy = abs(y1-y0) 
    if longx*longy == 0: raise Warning('Dimensions are zero') 

    # Move pen to initial position
    turtle.penup()
    turtle.goto(x0, y0)
    turtle.pendown()

    # Set the fillcolor
    turtle.fillcolor(color)
    
    # start the filling color
    turtle.begin_fill()
    
    for _ in range(4):
        
        # Drawing length
        if _ % 2 == 0:
            turtle.forward(longx) 
            turtle.left(90) 
        
        # Drawing width
        else:
            turtle.forward(longy) 
            turtle.left(90)

    # ending the filling of the color
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

# =================================
# NIVEAU 2: GESTION DE DEPLACEMENT
# =================================
def tracer_personnage(case, pas): 

    # Trouver les coordonnées initiales
    coord = coordonnees(case , pas)
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

def deplacer(questions, dictionnaire, list_objets, 
            matrice, case, pas, mouvement): 

    # Définir les positions
    old_case = np.asarray(case)
    new_case = np.asarray(case) + np.asarray(mouvement)

    # Vérifier si la nouvelle position est valide (est dans la matrice)
    (nb_lignes, nb_cols) = np.asarray(matrice).shape
    is_newposition_valid = True

    if (new_case[0]> -1 and new_case[0]<nb_lignes) and\
        (new_case[1]> -1 and new_case[1]<nb_cols): pass
    else: is_newposition_valid = False

    # Vérifier si le mouvment est valide (n'est pas un mur)
    if matrice[new_case[0]][new_case[1]] != 1: pass
    else: is_newposition_valid = False

    # Copy some objects
    matrice_new = matrice.copy()
    list_objets_new = list_objets.copy()
    case_current = old_case

    if is_newposition_valid :
        tracer_zone_annonces()

        # Verifier si dans la casse il y a un objet
        if matrice[new_case[0]][new_case[1]] == 4:
            # Definir les nouveaux valeurs
            case_current = new_case
            matrice_new, list_objets_new = \
            ramasser_objet(dictionnaire, list_objets, matrice, old_case, new_case, pas)

        elif matrice[new_case[0]][new_case[1]] == 3:
            matrice_new, case_current = poser_question(matrice, old_case, new_case, pas, questions)

        else:
            # Definir les nouveaux valeurs
            case_current = new_case
            color = COULEURS[matrice[old_case[0]][old_case[1]]]
            tracer_case(old_case, color, pas)
            tracer_personnage(new_case, pas)
        
    return case_current, matrice_new, list_objets_new

# =================================
# NIVEAU 3: COLLECTE D'OBJETS
# =================================
def ecrire_zone_affichage(text):
    # Definir le point au milieu pour l'affichage
    text_pos = tuple(map(operator.add, 
                POINT_AFFICHAGE_ANNONCES, POINT_AFFICHAGE_ANNONCES_FIN))

    # Ecrire texte
    tracer_zone_annonces()
    turtle.penup()
    turtle.goto(text_pos[0]/2-60, text_pos[1]/2)
    turtle.pendown()
    turtle.write(text)
    turtle.penup()

    return

def creer_dictionnaire_des_objets(fichier_des_objets):
    with open(fichier_des_objets, 'r') as file:
        lignes = file.readlines()

        dictionnaire = {}
        for i in range(len(lignes)):
            a, b = eval(lignes[i])
            dictionnaire[a] = b

    return dictionnaire

def ramasser_objet(dictionnaire: dict, list_objets: list, 
                    matrice, old_case, new_case, pas):

    # Definir le point au milieu pour l'affichage
    text_pos = tuple(map(operator.add, 
                POINT_AFFICHAGE_ANNONCES, POINT_AFFICHAGE_ANNONCES_FIN))

    # Ecrire texte
    ecrire_zone_affichage("Vous avez trouvé: une clef à molette")

    # Retracer l'ancienne case
    tracer_case(old_case, COULEUR_CASES, pas)

    # Retracer le nouveau case
    matrice_new = matrice.copy()
    matrice_new[new_case[0]][new_case[1]] = 0
    tracer_case(new_case, COULEUR_CASES, pas)

    # Tracer le personage
    tracer_personnage(new_case, pas)

    # Ajouter le nouvel objet
    list_objets_new = list_objets.copy()
    list_objets_new.append(dictionnaire[tuple(new_case)])

    # Ecrire la nouvelle list d'objets
    text_pos = tuple(map(operator.add, 
                POINT_AFFICHAGE_INVENTAIRE, POINT_AFFICHAGE_INVENTAIRE_FIN))

    # Ecrire texte
    tracer_zone_inventaire()
    for _ in range(len(list_objets_new)):
        turtle.penup()
        turtle.goto(text_pos[0]/2-40, text_pos[1]/2 - _*20)
        turtle.pendown()
        turtle.write(list_objets_new[_])
        turtle.penup()
    
    return matrice, list_objets_new

# =================================
# NIVEAU 4: QUESTIONS-REPONSES
# =================================

def poser_question(matrice, old_case, new_case, pas, questions):

    # Ecrire texte
    ecrire_zone_affichage("Cette porte est fermée")

    # Poser la question
    question_text = questions[tuple(new_case)][0]
    reponse = turtle.textinput("Question", question_text)
    turtle.listen()

    # Definir les variables de sortie
    matrice_new = matrice.copy()
    case_current = old_case

    # Verifier si la réponse est bonne
    if reponse == questions[tuple(new_case)][1]:
        ecrire_zone_affichage("Cette porte est ouverte")

        # Retracer l'ancienne case
        tracer_case(old_case, COULEUR_CASES, pas)

        # Retracer le nouveau case
        matrice_new[new_case[0]][new_case[1]] = 0
        tracer_case(new_case, COULEUR_CASES, pas)

        # Tracer le personage
        tracer_personnage(new_case, pas)
        case_current = new_case

    else: 
        ecrire_zone_affichage("Mauvaise réponse")

    return matrice_new, case_current
