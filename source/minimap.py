import pygame as py
import fighter
import missile
import vectors
import math
import requests
import io

IMAGE_CACHE = {}

def get_map_outline():
    if "mapoutline" in IMAGE_CACHE:
        return IMAGE_CACHE["mapoutline"]

    url = "https://sky-warrior.s3.us-east-2.amazonaws.com/images/mapoutline.png"
    response = requests.get(url)
    if response.status_code != 200:
        raise FileNotFoundError(f"Could not download mapoutline from {url}")

    img_bytes = io.BytesIO(response.content)
    outline_surf = py.image.load(img_bytes).convert_alpha()
    IMAGE_CACHE["mapoutline"] = outline_surf
    return outline_surf

class Minimap:

    def __init__(self):
        self.permimage = get_map_outline()
        self.permimage = py.transform.scale(self.permimage, (128,128))
        self.image = self.permimage.copy()
        self.positions = []
        pass

    def update(self,sprites,player):
        self.positions = []
        for sprite in sprites:
            k = vectors.sub_vec(sprite.pos,player.pos)
            k = [k[0]/30,k[1]/30]
            d = vectors.norm(k)

            if(d<50):

                k = [k[0]+63,k[1]+63]
                self.positions.append(k)
        self.draw()

    def draw(self):
        self.image = self.permimage.copy()
        for pos in self.positions:
            py.draw.circle(self.image,(255,0,0),pos,2,2)