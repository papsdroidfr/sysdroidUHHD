#!/usr/bin/env python3
########################################################################
# Filename    : sysdroid_uhhd.py
# Description : classe pour gérer la matrice UHHD
# auther      : papsdroid
# modification: 2019/09/18
########################################################################
import time, unicornhathd

#classe pour afficher des msg à partir de codes binaires représantant chaque lettre en 5*3
#-----------------------------------------------------------------------------------------
class Msg():
    def __init__(self):
        #dictionnaire des codes binaires représentant chaque charactère au format 5x3
        self.font5x3 = {    
            "0" : [0b11111, 0b10001, 0b11111], # "0"
            "1" : [0b01001, 0b11111, 0b00001], # "1"
            "2" : [0b10011, 0b10101, 0b01001], # "2"
            "3" : [0b10101, 0b10101, 0b11111], # "3"
            "4" : [0b00110, 0b01010, 0b11111], # "4"
            "5" : [0b11101, 0b10101, 0b10111], # "5"
            "6" : [0b11111, 0b10101, 0b10111], # "6"
            "7" : [0b10001, 0b10110, 0b11000], # "7"
            "8" : [0b11111, 0b10101, 0b11111], # "8"
            "9" : [0b11101, 0b10101, 0b11111], # "9"
     
            "A" : [0b01111, 0b10100, 0b01111], # "A"
            "B" : [0b11111, 0b10101, 0b01010], # "B"
            "C" : [0b01110, 0b10001, 0b10001], # "C"
            "D" : [0b11111, 0b10001, 0b01110], # "D"
            "E" : [0b11111, 0b10101, 0b10101], # "E"
            "F" : [0b01111, 0b10100, 0b10100], # "F"
            "G" : [0b01110, 0b10001, 0b11101], # "G"
            "H" : [0b11111, 0b00100, 0b11111], # "H"
            "I" : [0b00000, 0b10111, 0b00000], # "I"
            "J" : [0b00011, 0b00001, 0b11110], # "J"
            "K" : [0b11111, 0b00100, 0b11011], # "K"
            "L" : [0b11110, 0b00001, 0b00001], # "L"
            "M" : [0b11111, 0b01000, 0b11111], # "M"
            "N" : [0b11111, 0b10000, 0b01111], # "N"
            "O" : [0b01110, 0b10001, 0b01110], # "O"
            "P" : [0b11111, 0b10100, 0b01100], # "P"
            "Q" : [0b01110, 0b10010, 0b01101], # "Q"
            "R" : [0b11111, 0b10110, 0b01101], # "R"
            "S" : [0b01001, 0b10101, 0b10011], # "S"
            "T" : [0b10000, 0b11111, 0b10000], # "T"
            "U" : [0b11110, 0b00001, 0b11110], # "U"
            "V" : [0b11100, 0b00011, 0b11100], # "V"
            "W" : [0b11111, 0b00100, 0b11111], # "W"
            "X" : [0b11011, 0b00100, 0b11011], # "X"
            "Y" : [0b11000, 0b00111, 0b11000], # "Y"
            "Z" : [0b10011, 0b10101, 0b11001], # "Z"
 
            "." : [0b00001],                    # "."
            "," : [0b00001, 0b00010],           # ","
            ":" : [0b01010],                    # ":"
            "-" : [0b00100, 0b00100],           # "-"
            "°" : [0b01000, 0b10100, 0b01000],  # "°"
            "*" : [0b01010, 0b00100, 0b01010],  # "*"
            " " : [ 0, 0, 0]                    # " "
        }

          
    # génère la liste des codes binaires correspondant à un texte
    # chaque code binaire sur 5b représente 5 pixels verticaux à allumer (1) ou étteindre(0)
    # plusieurs codes binaires mis côte à côte forment une lettre
    # chaque lettre est séparée de la suivante par une barre verticale étteinte: code 0b00000
    #-----------------------------------------------------------------------------------------------------------
    def create_msg(self, text):
        matrix= []
        for i in range(len(text)):
            if text[i].upper() in self.font5x3: # recherche dans le dictionnaire l'existance du charactère
                matrix = matrix + self.font5x3[text[i].upper()]     # ajout des codes binaires correpondant à la lettre
                matrix = matrix + [0]                              # ajout d'une colonne vide pour séparrer chaque lettre.
        return matrix

#classe affichage d'infos sur la Unicorn HAT HD
#-----------------------------------------------------------------------------------------
class SysDroid_uhhd():
    def __init__(self, rotation):
        unicornhathd.brightness(0.6)
        unicornhathd.clear()
        unicornhathd.rotation(rotation)  #(x|colonne, y|lignes)  (0,0): en bas à gauche
        self.c_gris_fonce = [20,20,10]
        self.c_rouge = [255,0,0]
        self.c_orange = [240,150,28]
        self.c_vert = [0,255,0]
        self.c_bleu = [23,7,238]
        self.c_jaune = [100,100,0]
        self.hue_min = 0.33                 # color HSV: vert pour un niveau 0%
        self.hue_max = 1.0                  # color HSV: rouge pour un niveau 100%
        self.hue_delta = self.hue_max - self.hue_min     # calculé une fois pour toutes
        self.msg = Msg()
        
        #initialisation de l'affichage
        self.animation_start()
        self.draw_titles(self.c_orange) #dessine les titres persistants 4 premières lignes
        self.draw_level(0,1,6)        #fond niveau CPU0
        self.draw_level(0,2,6)        #fond niveau CPU1
        self.draw_level(0,3,6)        #fond niveau CPU2
        self.draw_level(0,4,6)        #fond niveau CPU3
        self.draw_level(0,7,6)        #fond niveau RAM
        self.draw_fullbox(10, 6, 14, 10 ,self.c_gris_fonce) #fond niveau DISK
        self.draw_level(0,1,0)        #fond niveau T°
        unicornhathd.show()

    #affiche le buffer sur la matrice
    #--------------------------------
    def show(self):
        unicornhathd.show()
        
    #extinction de la matrice UHHD
    #--------------------------------
    def stop(self):
        self.animation_quit()
        unicornhathd.off()      

    #dessine un rectangle plein en pos (x0,y0),(x1,y1) de couleur c=[r,v,b]
    #----------------------------------------------------------------------
    def draw_fullbox(self, x0, y0, x1, y1, c):
        for x in range(x0, x1+1):
            for y in range(y0, y1+1):
                unicornhathd.set_pixel(x, y, c[0],c[1],c[2])

    #dessine un rectangle creux en pos (x0,y0),(x1,y1) de couleur c=[r,v,b]
    #----------------------------------------------------------------------
    def draw_box(self, x0, y0, x1, y1, c):
        for x in range(x0, x1+1):
            unicornhathd.set_pixel(x, y0, c[0],c[1],c[2])
            unicornhathd.set_pixel(x, y1, c[0],c[1],c[2])
        for y in range(y0, y1+1):
            unicornhathd.set_pixel(x0, y, c[0],c[1],c[2])
            unicornhathd.set_pixel(x1, y, c[0],c[1],c[2])

    #animation de démarrage: rectangle grossissant
    #---------------------------------------------
    def animation_start(self):
        for n in range(0,8):
            unicornhathd.clear()
            self.draw_box(7-n,7-n, 8+n,8+n, self.c_bleu)
            unicornhathd.show() 
            time.sleep(0.05)

    #animation quitter: rectangle rétraississant
    #-------------------------------------------
    def animation_quit(self):
        for n in range(0,8):
            unicornhathd.clear()
            self.draw_box(n,n, 15-n,15-n, self.c_bleu)
            unicornhathd.show()    
            time.sleep(0.05)

    #dessine 3 pixels (code binaire 3bits) horizontale pos (x,y), couleur h=HUE
    #---------------------------------------------------------------------------------------------
    def draw_horiz_3b(self, n3b, x, y, h):
        xb=0b100
        for c in range(3):
            if (xb & n3b) == xb :
                unicornhathd.set_pixel_hsv(x+c,y,h, 1.0, 0.7)
            else:
                unicornhathd.set_pixel(x+c,y,0,0,0) #led noire éteinte
            xb>>=1  #décalage 1b vers la droite

        
    #dessine les titres persistants en haut de la matrice (4 premières lignes)
    #-------------------------------------------------------------------------
    def draw_titles(self, c):
        unicornhathd.clear()
        self.draw_title_P(self.hue_min)
        self.draw_title_R(self.hue_min)
        self.draw_title_D(self.hue_min)
        unicornhathd.show()

    def draw_title_P(self,h):
        self.draw_horiz_3b(0b110,1,15,h)
        self.draw_horiz_3b(0b101,1,14,h)
        self.draw_horiz_3b(0b110,1,13,h)
        self.draw_horiz_3b(0b100,1,12,h)

    def draw_title_R(self,h):
        self.draw_horiz_3b(0b110,6,15,h)
        self.draw_horiz_3b(0b101,6,14,h)
        self.draw_horiz_3b(0b110,6,13,h)
        self.draw_horiz_3b(0b101,6,12,h)

    def draw_title_D(self,h):
        self.draw_horiz_3b(0b110,11,15,h)
        self.draw_horiz_3b(0b101,11,14,h)
        self.draw_horiz_3b(0b101,11,13,h)
        self.draw_horiz_3b(0b110,11,12,h)       
    

    #caclule la couleur HUE: varie de 0.33(vert) à 1.00 (rouge) proportionnellement à level
    #------------------------------------------------------------------
    def hue_level(self, level): #level varie de 0 à 100
        return (self.hue_min + level/100*self.hue_delta)

    # dessine une ligne verticale de niveau sur 5 pixels
    # level: entier de 0 à 100 (%)
    # couleur du fond: tous les pixels en gris
    # couleur du niveau: variation de couleur du vert(0) au rouge (100)
    #----------------------------------------------------------------------------------------------
    def draw_level(self, level, x, y):
        nb_p = int(level/20)        #nb de palliers de 20% atteints: 0 à 5
        h = self.hue_level(level)   #HUE en fonction du level (0:vert à 100 rouge)
        for i in range(5):
            unicornhathd.set_pixel(x,y+i,self.c_gris_fonce[0],self.c_gris_fonce[1],self.c_gris_fonce[2])    # fond gris
            if (level/20>i):
                unicornhathd.set_pixel_hsv(x,y+i, self.hue_level(level), 1.0, (i+1)/(1+nb_p)) #dégradé bas(-) vers haut(+)
                #unicornhathd.set_pixel_hsv(x,y+i, self.hue_level(level), 1.0, 1-i/(nb_p+1))    #dégradé bas(+) vers haut(-)
        
        

    # représente un niveau de 0 à 100 sous forme de carré de taille 5*5
    # chaque colonne du carré représente une portion de 20% du niveau
    # chaque point d'une colonne représente une portion de 4%
    #------------------------------------------------------------------------
    def draw_square_level(self, level, x,y):
        nb_c = int(level/20)        #nb de tranches de 20% atteintes, varie de 0 à 5
        nb_l = int((level%20)/4)    #reste représantant 4% chacun: varie de 0 à 5
        self.draw_fullbox(10, 6, 14, 10 ,self.c_gris_fonce) #fond niveau DISK
        h = self.hue_level(level)
        #tranches pleines de 20%
        for c in range(nb_c):
            for l in range(5):
                unicornhathd.set_pixel_hsv(c+x,l+y, h, 1.0, (c+1)/nb_c) #dégradé gauche(-) vers droite (+)
                #unicornhathd.set_pixel_hsv(c+x,l+y, h, 1.0, 1-c/(nb_c+1))    #dégradé gauche(+) vers droite (-)
                
        #tranches de 4% supplémentaires
        for l in range(nb_l):
            unicornhathd.set_pixel_hsv(nb_c+x,l+y,h)  #dégradé gauche(-) vers droite (+)
            #unicornhathd.set_pixel_hsv(nb_c+x,l+y,h, 1.0,1-nb_c/(nb_c+1)  )   #dégradé gauche(+) vers droite (-)
            

    # affiche T° CPU t 
    #-----------------------------------------------------
    def draw_T(self, t, h):
        matrix_bin = self.msg.create_msg(str(t)) #conversion du message en codes binaires
        for i in range(13): #T° exprimées sous forme de 13 codes binaires
            xb=0b10000
            n5b=matrix_bin[i] #1 code binaire sur 5b rerpésente une barre verticale de 5 pixels
            for l in range(5):
                if (xb & n5b) == xb :
                    unicornhathd.set_pixel_hsv(3+i,4-l, h, 1.0, 1.0)
                else:
                    unicornhathd.set_pixel(3+i,4-l,0,0,0) #led noire éteinte
                xb>>=1 #décalage 1b vers la droite
                
    
