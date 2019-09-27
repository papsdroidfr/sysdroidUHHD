#!/usr/bin/env python3
########################################################################
# Filename    : sysDroid_main.py
# Description : information système raspberry pi (température, CPU, mémoire) sur un Unicorn HAT HD
# auther      : papsdroid
# modification: 2019/09/18
########################################################################
import time, os, unicornhathd
import threading
import psutil
from sysdroid_UHHD import SysDroid_uhhd


#classe affichage infos système (via thread)
#-----------------------------------------------------------------------------------------
class SysDroid(threading.Thread):
    def __init__(self, verbose, delay, rotation):     
        threading.Thread.__init__(self)  # appel au constructeur de la classe mère Thread
        self.etat=False             # état du thread False(non démarré), True (démarré)
        self.verbose = verbose      # True: active les print
        self.delay = delay          # délais en secondes de rafraichissement des infos systèmes
        self.rotation = rotation    # angle d'affichage sur la matrice UHHD (mutliple de 90°)
        print ('Sysdroid démarre ... ')
        self.uhhd = SysDroid_uhhd(rotation)       # matrice de leds UHHD
        self.readsys = ReadSys(verbose, delay)    # thread de lecture des informations système 
        self.readsys.start()              # démarrage du thread de lecture des info systèmes
       
    #exécution du thread
    #-------------------
    def run(self):
        self.etat=True
        while (self.etat):
            if not(self.readsys.infoLues):
                self.uhhd.draw_title_P(self.uhhd.hue_level(self.readsys.cpu_util))
                self.uhhd.draw_level(self.readsys.cpus_util[0],1,6) #niveau CPU[0]
                self.uhhd.draw_level(self.readsys.cpus_util[1],2,6) #niveau CPU[1]
                self.uhhd.draw_level(self.readsys.cpus_util[2],3,6) #niveau CPU[2]
                self.uhhd.draw_level(self.readsys.cpus_util[3],4,6) #niveau CPU[3]
                self.uhhd.draw_title_R(self.uhhd.hue_level(self.readsys.mem_used))
                self.uhhd.draw_level(self.readsys.mem_used,7,6)     #niveau RAM
                self.uhhd.draw_title_D(self.uhhd.hue_level(self.readsys.disk_used))
                self.uhhd.draw_square_level(self.readsys.disk_used,10,6) #niveau disk
                self.uhhd.draw_level(self.readsys.cpu_t_level,1,0)       #niveau cpu T° (0%: <=30, 100%:>=80°C)
                self.uhhd.draw_T(self.readsys.cpu_t,self.uhhd.hue_level(self.readsys.cpu_t_level)) #affichage T° CPU
                self.uhhd.show()
                self.readsys.set_infoLues()
            else:
                time.sleep(0.5) # mise en pause (sinon proc saturé par boucle infinie)
        
    #arrêt du thread
    #---------------
    def stop(self):
        self.etat=False
        self.readsys.stop()     # arret du thread readsys
        self.uhhd.stop()        # extinction de la matrice UHHD
        print('Sysdroid arrêté')      


#classe de lecture des informations systèmes à lire
#-----------------------------------------------------------------------------------------
class ReadSys(threading.Thread):
    def __init__(self, verbose, delay):
        threading.Thread.__init__(self)  # appel au constructeur de la classe mère Thread
        self.verbose = verbose           # True active les print
        self.delay = delay               # délais en secondes entre chaque nouvelle lecture (30s par défaut)
        self.etat=False                  # état du thread False(non démarré), True (démarré)
        self.t_min = 40                  # température minimale (0% si en dessous)
        self.t_max = 80                  # température maximale (100% si au dessus)
        self.cpu_t=0                     # température du CPU
        self.cpu_t_level = 0             # % T°CPu 0%: <=t_min, 100%: >= t_max
        self.cpu_util   = 0              # CPU global utilisation (%)
        self.cpus_util  = [0,0,0,0]      # CPUs utilisation (%)
        self.mem_used   = 0              # mémoire physique utilisée (%)
        self.disk_used  = 0              # usage du disk à la racine ('/') en %
        self.infoLues   = True           # True si les infos sont prises en compte, False sinon.

    #mise à jour de la variable infoLues à True
    #-------------------------------------------
    def set_infoLues(self):
        self.infoLues=True

    #lecture de la température CPU
    #-----------------------------
    def get_cpu_temp(self):     
        tmp = open('/sys/class/thermal/thermal_zone0/temp')
        cpu = tmp.read()
        tmp.close()
        return(round(float(cpu)/1000,1))

    #converti la t° CPU en % entre t_min et t_max
    #-------------------------------------------------------------------
    def convert_cpu_pct(self):
        return (float)(self.cpu_t-self.t_min)/(self.t_max-self.t_min)*100
    
   
    #démarrage du thread
    #-------------------
    def run(self):
        self.etat=True
        if self.verbose:
            print('Thread lecture info système démarré')
        while (self.etat):
            #lecture et stockage des informations système
            self.cpu_t = self.get_cpu_temp()
            self.cpu_t_level = self.convert_cpu_pct()
            self.cpu_util = psutil.cpu_percent()
            self.cpus_util = psutil.cpu_percent(percpu=True)
            self.mem_used = psutil.virtual_memory()[2]
            self.disk_used = psutil.disk_usage('/')[3]
            self.infoLues = False
            if self.verbose:
                print ('CPU:', self.cpu_util,'CPUs:', self.cpus_util,'% MEM used:',self.mem_used,'% CPU T°:', self.cpu_t,'°C', ' DISK:',self.disk_used,'%')
            time.sleep(self.delay)

    #arrêt du thread
    #----------------
    def stop(self):
        self.etat=False
        if self.verbose:
            print('Thread lecture info système stoppé')

#classe application principale
#------------------------------------------------------------------------------
class Application():
    def __init__(self, verbose=False, delay=30, rotation=0):
        self.sysdroid = SysDroid(verbose, delay, rotation) 
        self.sysdroid.start()   # démarrage du thread de surveillance système
     	
    def loop(self):
        while True:
            time.sleep(1)
            continue

    def destroy(self):          # fonction exécutée sur appui CTRL-C
        self.sysdroid.stop()    # arrêt du thread de surveillance système       


if __name__ == '__main__':     # Program start from here
    appl=Application(verbose=False, delay=1, rotation=90)  
    try:
        appl.loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        appl.destroy()    

