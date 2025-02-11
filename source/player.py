from object import Object
import particle
import config
import pygame as py
import spritesheet
import math
import random
import time
import requests
import io

IMAGE_CACHE = {}

def get_player_top_image(i):
    cache_key = f"top_{i}"
    if cache_key in IMAGE_CACHE:
        return IMAGE_CACHE[cache_key]

    url = f"https://sky-warrior.s3.us-east-2.amazonaws.com/images/top{i}.png"
    response = requests.get(url)
    if response.status_code != 200:
        raise FileNotFoundError(f"Could not download {url}")

    surf = py.image.load(io.BytesIO(response.content)).convert_alpha()
    IMAGE_CACHE[cache_key] = surf
    return surf

def get_sonic_image(i):
    ck = f"sonic_{i}"
    if ck in IMAGE_CACHE:
        return IMAGE_CACHE[ck]

    url = f"https://sky-warrior.s3.us-east-2.amazonaws.com/images/sonic/sonic{i}.png"
    response = requests.get(url)
    if response.status_code != 200:
        raise FileNotFoundError(f"Could not download {url}")

    surf = py.image.load(io.BytesIO(response.content)).convert_alpha()
    IMAGE_CACHE[ck] = surf
    return surf

def get_boom_image(i):
    ck = f"boom_{i}"
    if ck in IMAGE_CACHE:
        return IMAGE_CACHE[ck]

    url = f"https://sky-warrior.s3.us-east-2.amazonaws.com/images/sonic/boom/boom{i}.png"
    response = requests.get(url)
    if response.status_code != 200:
        raise FileNotFoundError(f"Could not download {url}")

    surf = py.image.load(io.BytesIO(response.content)).convert_alpha()
    IMAGE_CACHE[ck] = surf
    return surf

def get_damage_image():
    if "damage" in IMAGE_CACHE:
        return IMAGE_CACHE["damage"]

    url = "https://sky-warrior.s3.us-east-2.amazonaws.com/images/damage.png"
    resp = requests.get(url)
    if resp.status_code != 200:
        raise FileNotFoundError(f"Could not download damage.png from {url}")

    surf = py.image.load(io.BytesIO(resp.content)).convert_alpha()
    IMAGE_CACHE["damage"] = surf
    return surf

def get_ship_image():
    if "ship" in IMAGE_CACHE:
        return IMAGE_CACHE["ship"]
    url = "https://sky-warrior.s3.us-east-2.amazonaws.com/images/ship.png"
    resp = requests.get(url)
    if resp.status_code != 200:
        raise FileNotFoundError(f"Could not download ship.png from {url}")

    surf = py.image.load(io.BytesIO(resp.content)).convert_alpha()
    IMAGE_CACHE["ship"] = surf
    return surf

class Player(py.sprite.Sprite,Object):
    def __init__(self):
        Object.__init__(self)
        py.sprite.Sprite.__init__(self)
        self.speed= config.normal_speed
        self.turn_speed = 3.3
        self.particle_system = particle.ParticleSystem()
        self.vParticle_system = particle.VelocityParticleSystem()
        self.imgs = []
        self.sonic_imgs = []
        self.boom_imgs = []
        self.health = config.player_health
        self.live = True
        self.turbo = 100
        self.emp_affected = False
        self.releasing_turbo = False
        self.slowvalue = 1
        self.emp_duration = 0
        self.fuel = 500

        for i in range(1, 7):
            self.imgs.append(get_player_top_image(i))
        for i in range(1, 7):
             self.sonic_imgs.append(get_sonic_image(i))
        for i in range(1, 9):
            self.boom_imgs.append(get_boom_image(i))
            

        self.damaging = False
        self.damageshowindex = 0

        self.frame = 0
        self.sonic_frame = 0
        self.width = 80
        self.height = 80

        self.damage_image = get_damage_image()
        self.permimage = self.imgs[self.frame]
        self.permimage = py.transform.scale(self.permimage,(self.width,self.height))

        self.image = get_ship_image()
        self.rect = self.permimage.get_rect()
        self.angle = 0
        self.shoottimer = time.time()

    def rot_center(self):
        if self.speed > 300 and self.speed < 400:
            ind = int((self.speed - 300) / 13)
            self.permimage = self.boom_imgs[ind]
            self.permimage = py.transform.scale(self.permimage,(self.width*1.8,self.height*1.8))
            self.turn_speed = 5
        else:
            self.turn_speed = 3.3
            if not self.releasing_turbo:
                if self.damaging:
                    self.permimage = self.damage_image.copy()
                    self.damageshowindex+=1
                    if self.damageshowindex > 4:
                        self.damaging = False
                        self.damageshowindex = 0
                else:
                    self.permimage = self.imgs[int(self.frame/3)]
            else:

                self.permimage = self.sonic_imgs[int(self.frame/3)]

            self.permimage = py.transform.scale(self.permimage, (self.width*1.8,self.height*1.8))
        orig_rect = self.permimage.get_rect()
        # rad = np.arccos(np.dot(self.unit(self.v),np.array([1,0])))
        # self.angle = np.rad2deg(rad)
        rot_image = py.transform.rotate(self.permimage, -self.angle - 90)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        self.image = rot_image
        self.rect = self.image.get_rect()
        self.rect.centerx = config.screen_width/2
        self.rect.centery = config.screen_height/2

    def release_turbo(self):

        if self.turbo>0.5 and self.emp_duration==0:
            self.releasing_turbo = True
            self.turbo-=0.5*self.slowvalue
            if self.speed < config.normal_speed+200:
                self.speed += 20*self.slowvalue

        if self.turbo == 0.0:
            self.releasing_turbo = False

    def stop_turb(self):
        self.releasing_turbo = False

    def turn_left(self):
        self.angle -= self.turn_speed*self.slowvalue

    def turn_right(self):
        self.angle += self.turn_speed*self.slowvalue

    def throttleUp(self):
        # print(self.turbo)
        if self.turbo < 100 and not self.releasing_turbo:
            self.turbo += 1*self.slowvalue

        if self.speed < config.normal_speed and not self.releasing_turbo:
            self.speed+=3*self.slowvalue

        # elif self.speed > config.normal_speed:
        #     if self.speed > 300:
        #         self.speed -= 15*self.slowvalue
        #     else:
        #         self.speed -= 3*self.slowvalue

    def throttleDown(self):
        #print(self.speed,config.normal_speed)
        if self.speed > config.normal_speed and self.releasing_turbo == False:
            self.speed-= 3*self.slowvalue


    def update(self,slowvalue):
        if self.emp_affected == True:
            self.emp_duration = 1000
            self.emp_affected = False

        self.slowvalue = slowvalue
        r = math.radians(self.angle)
        dir = [math.cos(r),math.sin(r)]
        if self.emp_duration>0:
            self.emp_duration -= 3*slowvalue
            #print(self.emp_duration)
        else:
            self.emp_duration = 0

        if self.emp_duration >0:
            if self.speed > 160:
                self.speed-= 1
            else:
                self.speed = 160

        self.v = self.add_vec(self.multiply(self.speed, self.v), self.multiply(self.turn_speed * 120, dir))
        self.v = self.unit(self.v)
        self.pos = self.add_vec(self.pos,self.multiply(self.speed*config.dt*slowvalue,self.v))

        r = math.radians(-self.angle-180+90)
        r1 = math.radians(-self.angle - 180 - 90)
        r2 = math.radians(self.angle+random.randint(-90,90))
        p1 = self.multiply(5, [math.cos(r), math.sin(r)])
        p2 = self.multiply(random.randint(10, 45), [math.cos(r), math.sin(r)])
        if self.live:
           # Emit trail particles with some randomness
             # Particle emission behind the player
            trail_offset = self.multiply(-self.width * 0.4, self.v)
            trail_pos = self.add_vec(self.pos, trail_offset)
            
            trail_velocity = self.multiply(-0.3, self.v)
            self.particle_system.add_particle(trail_pos, trail_velocity)

        self.rot_center()
        self.frame = (self.frame + 1) % 18

        
        #sounds

    def renderPosition(self):
        self.particle_system.renderPosition(self.pos)
        self.vParticle_system.renderPosition(self.pos,self.slowvalue)
