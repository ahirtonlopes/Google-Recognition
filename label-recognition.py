#!/usr/bin/python3.6

"""

"""
__author__ = "Ahirton Lopes"
__credits__ = ["Ahirton Lopes"]
__license__ = "None"
__version__ = "1.0"
__maintainer__ = "Ahirton Lopes"
__email__ = "ahirtonlopes@gmail.com"
__status__ = "Beta"

"""

Utilizando a API "Google Vision" junto a uma Raspberry Pi e a Pi Camera.  
Tirar uma foto de um objeto, fazemos o upload da foto tirada no Google Cloud. 
Podemos analisar a imagem e retornar "rótulos" (o que se tem na foto), logotipos 
(logotipos de empresas na foto) e detecção de emoção em faces.

Utilizando a rotulação automatizada em imagens via Google Vision API.

"""

import base64
import picamera
import json
import os

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/pi/vision.json"

def takephoto():
    camera = picamera.PiCamera()
    camera.capture('image.jpg')

def main():
    takephoto()
    """Executando a rotulação automatizada em uma foto"""

    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials)

    with open('image.jpg', 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'LABEL_DETECTION',
                    'maxResults': 10
                }]
            }]
        })
        response = service_request.execute()
        print (json.dumps(response, indent=4, sort_keys=True))	#Print it out and make it somewhat pretty.

if __name__ == '__main__':

    main()
