import COMMUN.commun as C
import COMMUN.variables as V

import JEU_Pytris.pytris as PT


import asyncio
import websockets
import json
import time

class webSocket():  
    async def tache1_socket(actions_websocket):   
        
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
                            await actions_websocket.put(donnees)
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


        
async def tache2(actions_websocket):
    print("     + Initialisation Tache JEU :")
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, tache2_jeu, actions_websocket)        
                    
def tache2_jeu(actions_websocket):
    print("+ Démarrage du moteur PyTris")
    
    commun = C.CCommun("Pytris", actions_websocket) 
    commun.Salon.boucle()
    
    if V.boucle:
        pytris = PT.CPyTris(commun, actions_websocket)
        pytris.boucle()



async def main():
    print("Initialisation des taches :")
    actions_websocket = asyncio.Queue()
    
    await asyncio.gather(
        webSocket.tache1_socket(actions_websocket),
        tache2(actions_websocket)
    )    
       
asyncio.run(main())

