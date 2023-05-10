# On importe les librairies nécessaires  
from sense_hat import SenseHat
import time
import urllib.request
import os
import params 
#Parametrage du temps d'attente entre les différentes mesures
sleep_between_two_measures = params.sleep
# On renseigne sa clé API permettant d'écrire sur le channel
API = params.key


# On démarre le module Sense HAT
sense = SenseHat()

#Définition des couleurs
red = (255, 0, 0)
orange = (255, 165, 0)
green = (100, 255, 157)
purple = (160, 32, 240)
blue = (0, 0, 255)



i=0
#On tourne en boucle
while True:
	#On detecte si le boutton est appuyé, si c'est le cas, on etteint le raspberry après avoir mis le senshat en violet
    for event in sense.stick.get_events():
        if event.action == "pressed":
            if event.direction == "middle":
                sense.clear(purple)
                time.sleep(5)
                sense.clear()
                os.system("sudo shutdown -h now")
                
# On lit les valeurs différents capteurs 
    pression_sense = sense.get_pressure()
    Pression = pression_sense
    Humidité= sense.get_humidity()
    Temperature = sense.get_temperature()
    pitch, roll, yaw = sense.get_orientation().values()
    x, y, z = sense.get_accelerometer_raw().values()
    
 # On envoie les valeurs sur Thingspeak
    url_debut = 'https://api.thingspeak.com/update?api_key='
    url = url_debut + API + '&field1=' + str(Temperature) + '&field2=' + str(Humidité) + '&field3=' + str(Pression) + '&field4=' + str(x) + '&field5=' + str(y) + '&field6=' + str(z)
    try:
        if not i%10: #tous les 10 pas de temps on envoie la requette (1 pas de temps = 1/10 * sleep time between two measures)
            ret = urllib.request.urlopen(url)
            print(ret)

            i=0
        ipv4 = os.popen('ip addr show wlan0 | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip()
        sense.show_message(ipv4[-3:],0.2)
        print(ipv4)
        sense.clear(green)
        i+=1
        
    except Exception as e:
        sense.show_message("Une erreur est survenue. Tentative de reconnection n",0.07)
        print(e)
        sense.clear(red)
        for event in sense.stick.get_events():
            if event.action == "pressed":
                if event.direction == "middle":
                    sense.clear(purple)
                    time.sleep(5)
                    sense.clear()
                    os.system("sudo shutdown -h now")
    time.sleep(sleep_between_two_measures/10)
    
    


