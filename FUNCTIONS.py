# Python libraries
import numpy as np
import turtle

# My configurations
from CONFIGS import *

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

def tracer_carre(dimension):  
    for _  in range(4):
        turtle.forward(dimension) 
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

def afficher_plan(matrice): 
    # Trouver les dimensions de la matrice
    (nb_lignes, nb_cols) = np.asarray(matrice).shape

    # Trouver le pas
    pas = calculer_pas(matrice)

    # Tracer le plan 
    for i in range(nb_lignes): 
        for j in range(nb_cols): 
            case = [i, j]
            print(matrice[i][j])
            couleur = COULEURS[matrice[i][j]]
            tracer_case(case, couleur, pas)

    return

# =================================
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