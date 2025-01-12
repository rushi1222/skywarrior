import pygame as py
import time
import requests
import io

class Sound:
    def __init__(self):
        # List of remote sound URLs
        self.songs = [
            "https://sky-warrior.s3.us-east-2.amazonaws.com/sounds/explosion01.flac",
            "https://sky-warrior.s3.us-east-2.amazonaws.com/sounds/shootbullet.wav",
            "https://sky-warrior.s3.us-east-2.amazonaws.com/sounds/tick1.wav",
            "https://sky-warrior.s3.us-east-2.amazonaws.com/sounds/gametrack.ogg",
            "https://sky-warrior.s3.us-east-2.amazonaws.com/sounds/bullethit.flac",
            "https://sky-warrior.s3.us-east-2.amazonaws.com/sounds/explosion.wav"
        ]

        py.mixer.init()

        # Download and load each sound
        self.boom = self.load_sound_from_url(self.songs[0])
        self.shoot = self.load_sound_from_url(self.songs[1])
        self.tick = self.load_sound_from_url(self.songs[2])
        self.serious = self.load_sound_from_url(self.songs[3])
        self.hit = self.load_sound_from_url(self.songs[4])
        self.missile_explosion = self.load_sound_from_url(self.songs[5])

        self.sound = 0.1
        self.boomtimer = time.time()
        self.shoottimer = time.time()
        self.lasttick = time.time()

    def load_sound_from_url(self, url):
        """
        Downloads a sound file from the given URL and returns a pygame Sound object.
        """
        response = requests.get(url)
        if response.status_code != 200:
            raise FileNotFoundError(f"Unable to download sound from {url}")
        
        file_like = io.BytesIO(response.content)
        return py.mixer.Sound(file_like)

    def playTheme(self):
        self.serious.set_volume(0.5)
        self.serious.play(-1)

    def mBooms(self):
        now  = time.time()
        if now - self.boomtimer > 2:
            self.boom.set_volume(0.5)
            self.boom.play(0)
            self.boomtimer = time.time()

    def mShoots(self):
        self.shoot.set_volume(self.sound)
        self.shoot.play(0)

    def mHit(self):
        self.hit.set_volume(self.sound)
        self.hit.play(0)

    def missileExplosion(self, dis):
        v = 1
        if dis < 100:
            v = 0.5
        elif dis < 300:
            v = 0.4
        elif dis < 700:
            v = 0.25
        elif dis < 1000:
            v = 0.17
        elif dis < 2000:
            v = 0.1
        self.missile_explosion.set_volume(v)
        self.missile_explosion.play(0)

    def mTicks(self, tickdur):
        now = time.time()
        if now - self.lasttick > tickdur:
            self.tick.set_volume(0.3)
            self.tick.play(0)
            self.lasttick = now
            return now
        return -1
