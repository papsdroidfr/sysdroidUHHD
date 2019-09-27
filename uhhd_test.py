#!/usr/bin/env python3
########################################################################
# Filename    : UHHD_test.py
# Description : tests pixels Unicorn HAT HD
# auther      : papsdroid
# modification: 2019/09/25
########################################################################
import time, unicornhathd

#classe application principale
#------------------------------------------------------------------------------
class Application():
    def __init__(self) :
        self.delay = 2 #délais d'attente entre chaque changement d'affichage
        print('démarrage test, CTRL-C pour sortir')
        
        
    #boucle principale
    #------------------
    def loop(self):
        while True:
            self.draw_fullbox(0,0,15,15,[255,0,0])
            unicornhathd.show()
            time.sleep(self.delay)
            self.draw_fullbox(0,0,15,15,[0,255,0])
            unicornhathd.show()
            time.sleep(self.delay)
            self.draw_fullbox(0,0,15,15,[0,0,255])
            unicornhathd.show()
            time.sleep(self.delay)

    # fonction exécutée sur appui CTRL-C
    #-------------------------------------
    def destroy(self):          
        print('fin du test')
        unicornhathd.off() 

    #dessine un rectangle plein en pos (x0,y0),(x1,y1) de couleur c=[r,v,b]
    #----------------------------------------------------------------------
    def draw_fullbox(self, x0, y0, x1, y1, c):
        for x in range(x0, x1+1):
            for y in range(y0, y1+1):
                unicornhathd.set_pixel(x, y, c[0],c[1],c[2])


if __name__ == '__main__':     # Program start from here
    appl=Application()  
    try:
        appl.loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        appl.destroy()    
