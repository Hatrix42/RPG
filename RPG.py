﻿# RPG
import pygame
from pygame.locals import *
from classes import *
import re
import os
from pprint import pprint
import sqlite3
import ast


import GameFonctions
import FightFonctions

# Initialisation Pygame
# La Listes.fenetre fait 800*800 et le jeu 600*600
# Les cases font 30*30
pygame.init()
titre = 'Un super RPG'
pygame.key.set_repeat(1, 200)
Listes.fenetre = pygame.display.set_mode((600,600))
pygame.display.set_caption(titre)

creer_images_perso()


# Listes.fenetre.blit(pygame.image.load(os.path.join("images", "fond.png")), (0,0))
Listes.fenetre.fill((240, 240, 240))

# On crée une liste contenant chaque carte
Listes.liste_cartes = list()

# Chargement de tous les fichiers nécessaires
GameFonctions.ClansInfo.Ini_Clans()
##GameFonctions.ClansInfo.OpenClansStats()

Listes.liste_persos = []

for val in os.listdir("MyCharacters"):
    Listes.liste_persos = creer_liste_perso()

# Selection du personnage
selection_personnage(Listes.fenetre)
GameFonctions.MyCharacters.StatsCalc.CalcTotalStats(GameFonctions.MyCharacters.Character1)

# On lit le dossier "map" et on crée associe l'objet Carte à chaque indice qui correspond à son nom (Ainsi la carte 6 se trouvera à Listes.liste_cartes[6])
for i in range(len(os.listdir("map"))):
    Listes.liste_cartes.append(Carte(i))

    # Après avoir crée l'objet, on la charge (collisions, etc)
    Listes.liste_cartes[i].charger_carte()

    
    
    
Listes.liste_items = creer_liste_objets()
for i in Listes.liste_items.keys():
    Listes.liste_items[i].charger_item()
    
    
    
    
Listes.liste_quetes = creer_liste_quetes()
for i in Listes.liste_quetes.keys():
    Listes.liste_quetes[i].charger_quete()

Listes.liste_pnjs = creer_liste_pnj()
for i in Listes.liste_pnjs.keys():
    Listes.liste_pnjs[i].charger_pnj()

Listes.liste_obstacles = creer_liste_obstacles()
for i in Listes.liste_obstacles.keys():
    Listes.liste_obstacles[i].charger_obs()

# Listes.liste_items = dict()
# for i in os.listdir("items"): # i vaut le nom du pnj, "bidule.txt"
    # if re.match("[0-9a-zA-Z_\-\.\ ]+.txt", i):
        # Listes.liste_items[i.replace(".txt", "")] = Item(i.replace(".txt", ""))
        # Listes.liste_items[i.replace(".txt", "")].charger_item()
      
Joueur.inventaire = dict()
for val in Listes.liste_items.values():
    Joueur.inventaire[val.nom] = val.nombre
    
# print(Listes.liste_items)
# print(Joueur.inventaire)

# selection_personnage(Listes.fenetre)

Quete.charger_quete_en_cours()

Listes.liste_mobs = creer_liste_mobs()


# On définit quels événements permettent de se déplacer
cle_deplacement = [K_UP, K_DOWN, K_LEFT, K_RIGHT]

# On affiche la carte sur laquelle est le personnage puis le personnage lui même
Listes.liste_cartes[Joueur.carte].afficher_carte(Listes.fenetre)
Listes.fenetre.blit(Joueur.orientation, (Joueur.position_x,Joueur.position_y))

# On affiche ensuite les pnjs présents au démarrage
for val in Listes.liste_pnjs.values():
    if val.carte == Joueur.carte:
        Listes.fenetre.blit(val.image, (val.pos_x, val.pos_y))

for val in Listes.liste_items.values():
    for val2 in val.position:
        if int(val2[1]) == Joueur.carte:
            Listes.fenetre.blit(val.image, (int(val2[0][0]), int(val2[0][1])))

for i in Listes.liste_obstacles.keys():
    if Listes.liste_obstacles[i].carte == Joueur.carte:
        Listes.liste_obstacles[i].afficher_obstacle(Listes.fenetre)

pygame.display.flip() # Un petit peu d'eau, faut rafraichir

GameFonctions.MyCharacters.ReadSave(GameFonctions.MyCharacters.Character1.Nickname, GameFonctions.MyCharacters.Character1)
GameFonctions.MyCharacters.UpdateSave(GameFonctions.MyCharacters.Character1)
# print(type(Joueur.inventaire))
# print(ast.literal_eval(Joueur.inventaire))
# print(type(ast.literal_eval(Joueur.inventaire)))


continuer = 1
while continuer == 1:
    pygame.time.Clock().tick(300) # Faut un peu ralentir la boucle

    # Si on clique sur la chtite croix pour quitter
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = 0

        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            # if event.pos[0] > 10 and event.pos[0] < 610 and event.pos[1] > 10 and event.pos[1] < 610:
            Joueur.position_x = event.pos[0]//30*30
            Joueur.position_y = event.pos[1]//30*30
            print(Joueur.position_x, Joueur.position_y)
            afficher_monde(Listes.fenetre)

        # Si on a pressé une touche
        if event.type == KEYDOWN:
            # Soit elle se trouve dans les clés de déplacement et on bouge le perso
            if event.key in cle_deplacement:
                Joueur.bouger_perso(event.key, Listes.fenetre, Joueur.inventaire);

            # Soit c'est "Entrée" et on fait parler le personnage
            if event.key == K_RETURN:
                Joueur.parler_pnj(Listes.fenetre, Joueur.inventaire)
                Joueur.prendre_item(Joueur.inventaire, Listes.fenetre)

            if event.key == K_ESCAPE:
                options(Listes.fenetre, Joueur.inventaire)

            if event.key == K_i:
                # pprint(Joueur.inventaire)
                afficher_Joueur.inventaire(Listes.fenetre, Joueur.inventaire)
            
            if event.key == K_g:
                nb = 0
                for val in Listes.mob_prob.values():
                    nb += val
                
                for val in Listes.mob_prob.keys():
                    print(val, Listes.mob_prob[val]/nb*100)
            
            if event.key == K_h:
                print("Quêtes en cours : {0}".format(Quete.en_cours))
                print("Quêtes finies : {0}".format(Quete.quetes_finies))
                print("\n")

            if event.key == K_u:
                pygame.image.save(Listes.fenetre, os.path.join("cartes_images", "{0}.png".format(Joueur.carte)))

            if event.key == K_m:
                try:
                    Joueur.carte = int(input("carte : "))
                except:
                    pass

            if event.key == K_d:
                print(GameFonctions.MyCharacters.Character1.Sort)
                    
            if event.key == K_f:
                FightFonctions.Fight.StartFightMob(GameFonctions.MyCharacters.Character1)
                GameFonctions.MyCharacters.UpdateSave(GameFonctions.MyCharacters.Character1)
 
                afficher_monde(Listes.fenetre)


        # if event.type == MOUSEMOTION: # Décommenter pour avoir la position de la souris.
            # print("position {},{}".format(event.pos[0],event.pos[1]))