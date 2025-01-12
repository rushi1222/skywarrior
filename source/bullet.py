import config
import math
import pygame as py
import requests
import io

# Global dictionary to store surfaces
IMAGE_CACHE = {}

def get_bullet_image():
    """
    Returns a Surface of bullet image from S3, downloaded once.
    """
    # If it's already in IMAGE_CACHE, return it right away.
    if "bullet" in IMAGE_CACHE:
        return IMAGE_CACHE["bullet"]

    # Otherwise, download from S3, store in cache.
    url = "https://sky-warrior.s3.us-east-2.amazonaws.com/images/bullet.png"
    response = requests.get(url)
    if response.status_code != 200:
        raise FileNotFoundError(f"Failed to load bullet.png from {url}")

    image_bytes = io.BytesIO(response.content)
    surface = py.image.load(image_bytes).convert_alpha()
    IMAGE_CACHE["bullet"] = surface
    return surface
class Bullet(py.sprite.Sprite):
    def __init__(self,angle):
        py.sprite.Sprite.__init__(self)
        self.pos = [0,0]
        self.dir = [1,0]
        self.time = 5

        self.image = get_bullet_image()

        self.rect = self.image.get_rect()
        self.speed  = 1500

        self.angle = angle
        self.rot_center()

    def rot_center(self):
        orig_rect = self.image.get_rect()
        # rad = np.arccos(np.dot(self.unit(self.v),np.array([1,0])))
        # self.angle = np.rad2deg(rad)
        rot_image = py.transform.rotate(self.image, -self.angle - 90)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        self.image = rot_image
        self.rect = self.image.get_rect()
        self.rect.centerx = config.screen_width / 2
        self.rect.centery = config.screen_height / 2

class BulletsSystem:
    def __init__(self):
        self.bullets = py.sprite.Group()
        self.nexttime = 1
        self.slowvalue = 1

    def add_bullet(self,pos,direction,angle):

        if self.nexttime <0:
            if type(direction) == type([]):
                b = Bullet(angle)
                b.pos = list(pos)
                b.dir = dir
                self.bullets.add(b)

            elif type(direction) == type(2) or type(direction) == type(2.3):
                b =Bullet(angle)
                b.pos = list(pos)
                r = math.radians(direction)
                dire = [math.cos(r),math.sin(r)]
                b.dir = dire
                self.bullets.add(b)

            self.nexttime = 1
        else:
            self.nexttime -= 1*self.slowvalue
    def update(self,slowvalue):
        self.slowvalue = slowvalue

        for b in self.bullets.sprites():
            if b.time>0:
                b.pos[0] += b.dir[0]*b.speed*config.dt*slowvalue
                b.pos[1] += b.dir[1]*b.speed*config.dt*slowvalue
                b.time -= 0.5*slowvalue

            else:
                b.kill()