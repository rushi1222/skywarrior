import pygame as py
from pygame.locals import *
import requests
import io

FONT_CACHE = {}

def get_karma_font(size):
    """
    Downloads (or retrieves from cache) the 'karma future' TTF and returns a pygame.Font object of `size`.
    """
    cache_key = f"karma_future_{size}"
    if cache_key in FONT_CACHE:
        return FONT_CACHE[cache_key]

    url = "https://sky-warrior.s3.us-east-2.amazonaws.com/font/karma+future.ttf"
    response = requests.get(url)
    if response.status_code != 200:
        raise FileNotFoundError(f"Failed to download karma future font from {url}")

    font_bytes = io.BytesIO(response.content)
    loaded_font = py.font.Font(font_bytes, size)
    FONT_CACHE[cache_key] = loaded_font
    return loaded_font

class BigFontSystem:
    def __init__(self):
        # self.basicfont = py.font.SysFont(None,20)
        self.basicfont = get_karma_font(30)
    def draw(self,text,color = (255,255,255)):
        text = self.basicfont.render(text, True, color)
        textrect = text.get_rect()
        return [text,textrect]

class SmallFontSystem:
    def __init__(self):

        self.basicfont = get_karma_font(20)

    def draw(self,text,color = (255,255,255)):
        text = self.basicfont.render(text, True, color)
        textrect = text.get_rect()
        return [text,textrect]
