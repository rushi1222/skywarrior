import object
import particle
import pygame as py
import config
import math
import random
import time

class Missile(py.sprite.Sprite, object.Object):
    def __init__(self):
        object.Object.__init__(self)
        py.sprite.Sprite.__init__(self)
        self.speed = config.missile_speed
        self.turn_speed = config.missile_turn_speed
        self.particle_system = particle.ParticleSystem(color=(150, 150, 150), size=3, lifespan=30)  # Grey smoke
        self.permimage = py.image.load("../images/missile.png")
        self.image = py.image.load("../images/missile.png")
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(1000, 2000)
        self.rect.y = random.randint(1000, 2000)
        self.fuel = random.randint(config.missile_fuel - 50, config.missile_fuel)
        self.killit = False
        self.created_time = time.time()
        self.activated = False
        self.slowvalue = 1
        self.last_dir_change_time = time.time()

    def scalar_multiply(self, scalar, vector):
        return [scalar * component for component in vector]

    def renderPosition(self, ref):
        super().renderPosition(ref)
        self.particle_system.draw(self.image, ref)  # Draw particles

    def rot_center(self):
        orig_rect = self.permimage.get_rect()
        rad = math.acos(self.dot(self.unit(self.v), [1, 0]))
        rad2 = math.acos(self.dot(self.unit(self.v), [0, 1]))
        self.angle = math.degrees(rad)
        self.angle2 = math.degrees(rad2)

        if self.angle2 >= 90:
            rot_image = py.transform.rotate(self.permimage, -270 - (180 - self.angle))
        else:
            rot_image = py.transform.rotate(self.permimage, -self.angle - 90)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        self.image = rot_image
        self.rect = self.image.get_rect()
        self.rect.centerx = self.renderpos[0]
        self.rect.centery = self.renderpos[1]

    def update(self, playerpos, speed, slowvalue):
        self.slowvalue = slowvalue

        time_since_dir_change = time.time() - self.last_dir_change_time
        # Missile changes trajectory every few seconds
        if time_since_dir_change >= 3.0:
            rot_dir = self.sub_vec(playerpos, self.pos)
            v_turn = self.unit(self.sub_vec(rot_dir, self.v))
            v_turn = self.scalar_multiply(self.slowvalue, v_turn)
            self.v = self.add_vec(self.multiply(self.speed, self.v), self.scalar_multiply(self.turn_speed, v_turn))
            self.last_dir_change_time = time.time()

        # Update trajectory and fuel
        if not self.killit:
            rot_dir = self.sub_vec(playerpos, self.pos)
            v_turn = self.unit(self.sub_vec(rot_dir, self.v))
            self.v = self.add_vec(self.multiply(self.speed, self.v), self.scalar_multiply(self.turn_speed, v_turn))
            self.fuel -= 0.5 * slowvalue
        else:
            self.kill()
            self.particle_system.particles.clear()

        self.v = self.unit(self.v)
        self.pos = self.add_vec(self.pos, self.multiply(self.speed * config.dt * slowvalue, self.v))

        # Emit particles for trails
        if not self.killit:
            trail_offset = self.multiply(-self.rect.width * 0.5, self.v)
            trail_pos = self.add_vec(self.pos, trail_offset)
            trail_velocity = self.scalar_multiply(0, self.v)
            self.particle_system.add_particle(trail_pos, trail_velocity)

        self.particle_system.update(slowvalue)
        self.rot_center()
        self.renderPosition(playerpos)

        if time.time() - self.created_time > 0.5:
            self.activated = True