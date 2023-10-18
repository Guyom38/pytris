import COMMUN.commun as C
import COMMUN.variables as V

import JEU_Pytris.pytris as PT

import pygame
from pygame.locals import *


import asyncio
import websockets
import json
import time

class webSocket():  
    async def tache1_socket():   
        
        while V.boucle:
            print("     + Initialisation Tache Socket :")  
            try:
                async with websockets.connect(V.urlWss) as websocket: # ...
                    print("         + boucle thread websocket")
                    V.web_socket = True
                    
                    data_to_send = {"game": "pytris",
                                    "id_game": str(V.web_socket_id_partie),  
                                    "type_client": "game" }
                    
                    await websocket.send(json.dumps(data_to_send))
                    while V.boucle:
                        try:
                            message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                            donnees = json.loads(message)
                           
                            injecte_event(donnees)
                            print(str(donnees))
                            
                        except asyncio.TimeoutError:
                            print("Timeout: Aucun message reçu pendant 1 seconde. "+str(time.time()))
                            continue
                        
            except (websockets.ConnectionClosed, OSError):
                print("Erreur de connexion. Tentative de reconnexion dans 5 secondes...")
                await asyncio.sleep(5)
            except asyncio.CancelledError:
                print("Tâche annulée. Nettoyage et fermeture.")
                return

def injecte_event(data_events):
    if 'playerId' in data_events:                                            
        idJoueurWS = int(data_events['playerId'])                        
        if idJoueurWS not in V.JOUEURS_WEBSOCKET:
            V.JOUEURS_WEBSOCKET[idJoueurWS] = len(V.JOUEURS_WEBSOCKET) 
            print("Nouveau Joueur #"+str(idJoueurWS)+" => id:" + str(V.JOUEURS_WEBSOCKET[idJoueurWS]))       
        idJoueur = V.JOUEURS_WEBSOCKET[idJoueurWS]                        
                        
    if 'joystick' in data_events['data']:
        if data_events['data']['joystick']['x'] > 0:  pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 0,  'value': 1 }))
        elif data_events['data']['joystick']['x'] < 0:  pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 0,  'value': -1 }))
        else: pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 0,  'value': 0 }))
        
        if data_events['data']['joystick']['y'] > 14:  pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 1,  'value': 1 }))
        elif data_events['data']['joystick']['y'] < -14:  pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 1,  'value': -1 }))
        else: pygame.event.post(pygame.event.Event(pygame.JOYAXISMOTION, {'joy': idJoueur,  'axis': 1,  'value': 0 }))
  
    elif 'button' in data_events['data']: 
        etat = pygame.JOYBUTTONUP if data_events['data']['state'] == 'pressed' else pygame.JOYBUTTONDOWN
        if data_events['data']['button'] == 'A':  pygame.event.post(pygame.event.Event(etat, {'joy': idJoueur,  'button': 0 }))
        elif data_events['data']['button'] == 'B':  pygame.event.post(pygame.event.Event(etat, {'joy': idJoueur,  'button': 1 }))
        elif data_events['data']['button'] == 'X':  pygame.event.post(pygame.event.Event(etat, {'joy': idJoueur,  'button': 2 }))
        elif data_events['data']['button'] == 'Y':  pygame.event.post(pygame.event.Event(etat, {'joy': idJoueur,  'button': 3 }))
        elif data_events['data']['button'] == 'START':  pygame.event.post(pygame.event.Event(etat, {'joy': idJoueur,  'button': 9 }))
        elif data_events['data']['button'] == 'SELECT':  pygame.event.post(pygame.event.Event(etat, {'joy': idJoueur,  'button': 8 }))
        
                            

        
async def tache2():
    print("     + Initialisation Tache JEU :")
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, tache2_jeu)        
                    
def tache2_jeu():
    print("+ Démarrage du moteur PyTris")
    
    commun = C.CCommun("Pytris") 
    commun.Salon.boucle()
    
    if V.boucle:
        pytris = PT.CPyTris(commun)
        pytris.boucle()


async def main():
    print("Initialisation des taches :")
    await asyncio.gather(
        webSocket.tache1_socket(),
        tache2()
    )    
       
asyncio.run(main())

