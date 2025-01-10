import object
import config
import vectors
import random
import math
import pygame as py
class Particle(object.Object):
    def __init__(self, pos, color=(255, 255, 255), size=5, lifespan=50):
        object.Object.__init__(self)
        self.pos = list(pos)
        self.size = size
        self.color = color  # RGB color
        self.lifespan = lifespan  # Frames until the particle disappears
        self.alpha = 255  # Full opacity

    def update(self, slowvalue):
        # Update position based on velocity
        self.pos[0] += self.v[0] * config.dt * slowvalue
        self.pos[1] += self.v[1] * config.dt * slowvalue

        # Decrease lifespan and alpha
        self.lifespan -= 1 * slowvalue
        if self.lifespan > 0:
            self.alpha = max(0, int((self.lifespan / 50) * 255))
        else:
            self.alpha = 0

    def draw(self, surface, ref):
        if self.alpha > 0:
            # Create a surface for the particle with per-pixel alpha
            particle_surface = py.Surface((self.size * 2, self.size * 2), py.SRCALPHA)
            py.draw.circle(particle_surface, (*self.color, self.alpha), (self.size, self.size), self.size)
            # Calculate the particle's screen position with screen center offset
            screen_x = self.pos[0] - ref[0] + config.screen_width / 2 - self.size
            screen_y = self.pos[1] - ref[1] + config.screen_height / 2 - self.size
            # Blit the particle onto the main surface
            surface.blit(particle_surface, (screen_x, screen_y))


class Colored_Particle(object.Object):
    def __init__(self,pos):
        object.Object.__init__(self)
        self.pos = list(pos)
        self.size = 1

class SparkSystem:
    def __init__(self):
        self.particles = []

    def add_particles(self,pos, vel,n):
        for i in range(n):
            d = random.randint(5,10)
            angle = random.randint(0,359)
            color  = None
            if(random.randint(0,1)):
                color = [0xff,0xdf,0x00]
            else:
                color = [0xdd,0x00,0x00]
            smp = object.Object()
            angle = smp.calculate_angle(vel)

            a1 = int(angle - 175)%360
            a2 = int(angle + 175)%360
            #print(min(a1%360,a2%360),max(a1%360,a2%360))
            a = math.radians(random.randint(min(a1, a2), max(a1, a2)))
            np_angle = math.radians(random.randint(min(a1, a2), max(a1, a2)))
            newpoint = [math.cos(np_angle) * d, math.sin(np_angle) * d]
            #print(a1,a2)
            newpoint = smp.add_vec(pos,newpoint)
            speed = random.randint(100,500)
            v = [math.cos(a),math.sin(a)]
            self.particles.append([newpoint,v, color,100,speed])

    def update(self,slowvalue):
        removethis = []
        for p in self.particles:
            pos = p[0]
            v = p[1]
            pos[0] += v[0]*config.dt*slowvalue*p[-1]
            pos[1] += v[1]*config.dt*slowvalue*p[-1]
            p[3]-=1
            if(p[3]<0):
                removethis.append(p)
        for p in removethis:
            self.particles.remove(p)


class ParticleSystem:
    def __init__(self, color=(255, 255, 255), size=5, lifespan=30):
        self.particles = []
        self.color = color
        self.size = size
        self.lifespan = lifespan

    def add_particle(self, pos, velocity):
        particle = Particle(pos, self.color, self.size, self.lifespan)
        particle.v = velocity
        self.particles.append(particle)

    def update(self, slowvalue):
        for particle in self.particles[:]:
            particle.update(slowvalue)
            if particle.lifespan <= 0:
                self.particles.remove(particle)

    def draw(self, surface, ref):
        for particle in self.particles:
            particle.draw(surface, ref)

    def renderPosition(self, ref,):
        for p in self.particles:
            p.renderPosition(ref)


class VelocityParticleSystem:
    def __init__(self):
        self.particles = []
        self.particle_release_time = 3
        self.particle_limits = 50

    def add_particle(self,pos,vel):


        parti = Particle(pos)
        parti.v = vel
        self.particles.append(parti)
        self.particle_release_time = 0

        if len(self.particles) > self.particle_limits:
            self.particles.pop(0)

    def update(self,slowvalue):
        for p in self.particles:
            p.pos = vectors.add_vec(p.pos,vectors.multiply(config.dt*slowvalue,p.v))


    def renderPosition(self, ref,slowvalue):
        self.update(slowvalue)
        for p in self.particles:
            p.renderPosition(ref)

if __name__ == '__main__':
    j = object.Object()
    # print(j.calculate_angle([23,34]))