import pygame as py
import config
import font
import database
import requests
import io

# Cache for images loaded in menu
IMAGE_CACHE = {}

def get_background():
    """
    Loads main menu background from S3 and returns a pygame Surface.
    """
    if "menu_bg" in IMAGE_CACHE:
        return IMAGE_CACHE["menu_bg"]
    
    url = "https://sky-warrior.s3.us-east-2.amazonaws.com/images/background.png"
    response = requests.get(url)
    if response.status_code != 200:
        raise FileNotFoundError(f"Could not download {url}")

    image_bytes = io.BytesIO(response.content)
    bg = py.image.load(image_bytes).convert_alpha()
    IMAGE_CACHE["menu_bg"] = bg
    return bg

def get_lock_image():
    """ Used in 'levelmenu' for the lock icon. """
    if "lock_image" in IMAGE_CACHE:
        return IMAGE_CACHE["lock_image"]
    
    url = "https://sky-warrior.s3.us-east-2.amazonaws.com/images/lock.jpg"
    response = requests.get(url)
    if response.status_code != 200:
        raise FileNotFoundError(f"Could not download lock_image from {url}")

    image_bytes = io.BytesIO(response.content)
    img = py.image.load(image_bytes).convert_alpha()
    IMAGE_CACHE["lock_image"] = img
    return img

class Menu:
    def __init__(self):
        self.background = py.Surface((config.screen_width, config.screen_height))
        self.background.fill((0x8c, 0xbe, 0xd6))
         # Main background image
        bg_surf = get_background()
        bg_surf = py.transform.scale(bg_surf, (config.screen_width, config.screen_height))
        self.backgroundImage = bg_surf

        self.pause = False
        self.quit = False
        self.play = False
        self.showmenu = False
        
        self.finalstates = ["start", "levelmenu", "quitgame", "unpause", "quitlevel", "loadlevel", "pause"]
        self.states = ["mainmenu", "gamemenu", "levelmenu"]
        self.options = {
            "mainmenu": {
                "Play": "loadlast",
                "select level": "levelmenu",
                "quit": "quitgame",
                "**keys**": "W,A,D",
                "movement-W,A,D": "W,A,D",
                "speed-shift": "shift",
                "slowmotion-ctrl": "ctrl",
                "shoot-spacebar": "space",
                "*******": "W,A,D",
            },
            "gamemenu": {
                "resume": "unpause",
                "quit level": "quitlevel"
            },
            "difficultymenu": {
                "easy": "none",
                "normal": "none"
            },
            "levelmenu": {
                "Levels": "loadlevel"
            },
        }
        self.fontsystem = font.BigFontSystem()
        self.smfontsystem = font.SmallFontSystem()
        self.option_selected = "mainmenu"
        self.state = "mainmenu"

        self.level_selected = -1
        self.current_option_texts = []
        self.menu_surface = py.Surface((250, 300))
        self.optionon = -1
        self.database = database.Database()

    def draw(self, win):

        if self.option_selected == "mainmenu":
            win.blit(self.backgroundImage, (0, 0))
            i = 50 + 20

            self.menu_surface = py.Surface((450, 500))
            self.menu_surface = py.Surface.convert_alpha(self.menu_surface)
            self.menu_surface.fill((0, 0, 0, 180))
            self.current_option_texts = []
            ind = -1
            t, tr = self.fontsystem.draw("Sky Warrior", (200, 50, 50))

            tr.x = 20
            tr.y = 20
            self.menu_surface.blit(t, tr)

            # Display High Score
            high_score_text, high_score_rect = self.smfontsystem.draw(f"High Score: {self.database.get_high_score()}")
            high_score_rect.x = 20
            high_score_rect.y = i + 5  # Adjust position as needed
            self.menu_surface.blit(high_score_text, high_score_rect)
            i += 40  # Adjust spacing after high score

            for option in self.options["mainmenu"]:
                ind += 1
                if self.optionon == ind:
                    t, tr = self.fontsystem.draw(option, (200, 235, 100))
                else:
                    t, tr = self.fontsystem.draw(option, (250, 250, 250))
                tr.x = 20
                tr.y = i
                i += 45
                self.current_option_texts.append([option, t, tr])
                self.menu_surface.blit(t, tr)

            win.blit(self.menu_surface, (100, 200))

        elif self.option_selected == "gamemenu":
            i = 50 + 20
            self.menu_surface = py.Surface((250, 300))
            self.menu_surface = py.Surface.convert_alpha(self.menu_surface)
            self.menu_surface.fill((20, 20, 10, 100))
            self.current_option_texts = []
            ind = -1
            t, tr = self.fontsystem.draw("SkyWars", (200, 50, 50))
            tr.x = 20
            tr.y = 20
            self.menu_surface.blit(t, tr)
            for option in self.options["gamemenu"]:
                ind += 1
                if self.optionon == ind:
                    t, tr = self.fontsystem.draw(option, (240, 235, 100))
                else:
                    t, tr = self.fontsystem.draw(option)
                tr.x = 20
                tr.y = i
                i += 45
                self.current_option_texts.append([option, t, tr])
                self.menu_surface.blit(t, tr)

            win.blit(self.menu_surface, (100, 200))

        elif self.option_selected == "levelmenu":
            win.blit(self.backgroundImage, (0, 0))
            i = 50 + 20
            self.menu_surface = py.Surface((780, 250))
            self.menu_surface = self.menu_surface.convert_alpha()
            self.menu_surface.fill((20, 20, 10, 100))
            self.current_option_texts = []

            lock_image = get_lock_image()
            lock_image = py.transform.scale(lock_image, (16, 16))
            posx = 30
            for level_num in range(1, 6):
                small_surface = py.Surface.convert_alpha(py.Surface((120, 120)))
                if self.optionon == level_num - 1:
                    small_surface.fill((255, 255, 0, 100))
                else:
                    small_surface.fill((255, 255, 224, 100))
                text = f"Level {level_num}"
                t, tr = self.fontsystem.draw(text)
                tr.centerx = 60
                tr.centery = 60
                small_surface.blit(t, tr)
                small_surface_rect = small_surface.get_rect()
                small_surface_rect.x = posx
                small_surface_rect.y = 65
                if level_num > self.database.levelunlocked:
                    small_surface.blit(lock_image, (60, 100))

                self.current_option_texts.append([text, small_surface, small_surface_rect])
                self.menu_surface.blit(small_surface, small_surface_rect)
                posx += 150

            self.optionon = -1

            # Back Button
            back_surface = py.Surface.convert_alpha(py.Surface((50, 30)))
            back_surface.fill((20, 20, 10, 100))
            if self.optionon == 7:
                b, btr = self.smfontsystem.draw("back", (240, 235, 100))
            else:
                b, btr = self.smfontsystem.draw("back")
            btr.centerx = 25
            btr.centery = 15
            back_surface.blit(b, btr)
            bsr = back_surface.get_rect()
            bsr.centerx = 780 / 2
            bsr.y = 210
            self.current_option_texts.append(["back", back_surface, bsr])
            self.menu_surface.blit(back_surface, bsr)
            win.blit(self.menu_surface, (250, 200))

    def navigate(self, i):
        o = self.current_option_texts[i][0]

        if self.option_selected == "mainmenu":
            if o == "Play":
                self.state = "start"
                self.level_selected = self.database.levelunlocked
            if o == "select level":
                self.option_selected = "levelmenu"
            if o == "quit":
                self.state = "quitgame"

        if self.option_selected == "gamemenu":
            if o == "resume":
                self.state = "start"

            if o == "quit level":
                self.option_selected = "mainmenu"
                self.state = "mainmenu"

        if self.option_selected == "levelmenu":
            if o == "Level 1":
                self.state = "start"
                self.level_selected = 1

            elif o == "Level 2":
                if self.database.levelunlocked>=2:
                    self.state = "start"
                    self.level_selected = 2

            elif o == "Level 3":
                if self.database.levelunlocked>=3:
                    self.state = "start"
                    self.level_selected = 3
                pass
            elif o == "Level 4":
                if self.database.levelunlocked>=4:
                    self.state = "start"
                    self.level_selected = 4
                pass
            elif o == "Level 5":
                if self.database.levelunlocked>=5:
                    self.state = "start"
                    self.level_selected = 5
                pass

            if o == "back":
                self.option_selected = "mainmenu"

    def update(self, mousepos, clicked, escape):
        if escape:
            if self.state == "start":
                self.option_selected = "gamemenu"
                self.state = "mainmenu"
        i = -1
        m = list(mousepos)
        if self.option_selected in ["mainmenu", "gamemenu"]:
            m[0] -= 100
            m[1] -= 200

        elif self.option_selected == "levelmenu":
            m[0] -= 250
            m[1] -= 200

        self.optionon = -1  # Reset option highlight

        for op in self.current_option_texts:
            i += 1
            recta = op[2]

            if recta.collidepoint(m):
                self.optionon = i
                if clicked:
                    self.navigate(self.optionon)
                break

if __name__ == "__main__":
    pass
