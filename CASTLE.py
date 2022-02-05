# Python libraries
import numpy as np
import turtle

# My configurations
from CONFIGS import *

def draw_rectangle(init= tuple([0, 0]), fin= tuple([1, 1]), color= COULEUR_EXTERIEUR): 

    # Set initial position (We consider bottom-left corner)
    x0 = min(init[0], fin[0])
    y0 = min(init[1], fin[1])

    # Set final position
    x1 = max(init[0], fin[0])
    y1 = max(init[1], fin[1])

    # Dimensions
    longx = abs(x1-x0)
    longy = abs(y1-y0) 
    
    if longx*longy != 0:
        pass 
    else: 
        raise Warning('Dimensions are zero')

    # Move pen to initial position
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

def draw_square(init= tuple([0, 0]), long= 1, color= COULEUR_EXTERIEUR): 

    # Move pen to initial position
    turtle.goto(init[0], init[1])
    turtle.pendown()

    # Set the fillcolor
    turtle.fillcolor(color)
    
    # start the filling color
    turtle.begin_fill()
    
    for _  in range(4):
        turtle.forward(long) 
        turtle.left(90) 

    # ending the filling of the color
    turtle.end_fill()

    turtle.penup()

    return


class Castle(): 
    def __init__(self, filename: None): 

        if filename is not None: 
            pass 
        else: 
            raise Warning('I need a .txt file')

        matrix = np.loadtxt(filename, dtype='i', delimiter=' ')

        # Draw map
        turtle.penup()
        turtle.hideturtle()
        self.draw_ad_display_area()
        self.draw_inventory_area()
        self.draw_castle_area()
        self.draw_castle_map(matrix)

        return

    def draw_castle_area(self): 

        # Set values to castle map
        init = ZONE_PLAN_MINI
        fin = ZONE_PLAN_MAXI

        
        # Set values to draw the map area 
        draw_rectangle(init= init, fin= fin)

        return

    def draw_ad_display_area(self): 

        # Set values to draw ad display area
        init = POINT_AFFICHAGE_ANNONCES
        fin = POINT_AFFICHAGE_ANNONCES_FIN

        draw_rectangle(init= init, fin= fin)

        return

    def draw_inventory_area(self): 

        # Set values to draw inventory area
        init = POINT_AFFICHAGE_INVENTAIRE
        fin = POINT_AFFICHAGE_INVENTAIRE_FIN

        draw_rectangle(init= init, fin= fin)

        return 

    def draw_castle_map(self, matrix): 

        def find_size_square(matrix): 
            # Set values to castle map
            large = abs(ZONE_PLAN_MAXI[0] - ZONE_PLAN_MINI[0])
            long = abs(ZONE_PLAN_MAXI[1] - ZONE_PLAN_MINI[1])

            # Find shape of the matrix
            nb_rows, nb_cols = np.shape(matrix) 

            # Find distance
            Lsquare = min(long/nb_rows, large/nb_cols)

            return Lsquare

        def find_coordinates(indi, indj, Lsquare, nb_rows):

            # Set offsets
            offsetx =  ZONE_PLAN_MINI[0]
            offsety = ZONE_PLAN_MINI[1] + Lsquare * nb_rows - Lsquare

            # Find position without offsets
            posx =  indj * Lsquare
            posy = -  indi * Lsquare

            # Position with offset
            posx += offsetx
            posy += offsety

            return [posx, posy]

        # Define size of square
        Lsquare = find_size_square(matrix)

        # Find shape of the matrix
        nb_rows, nb_cols = np.shape(matrix)

        for i in range(nb_rows):
            for j in range(nb_cols): 
                color = COULEURS[matrix[i,j]]
                coordinates = find_coordinates(i, j, Lsquare, nb_rows)
                draw_square(coordinates, Lsquare, color)

        return



