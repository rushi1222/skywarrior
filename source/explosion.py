import pygame as py
import requests
import io

IMAGE_CACHE = {}

def get_explosion_frame(i, size=0.75):
    """
    Returns the i-th explosion frame from S3, scaled by `size`.
    """
    cache_key = f"explosion_{i}"
    if cache_key in IMAGE_CACHE:
        return IMAGE_CACHE[cache_key]

    url = f"https://sky-warrior.s3.us-east-2.amazonaws.com/images/exp{i}.png"
    response = requests.get(url)
    if response.status_code != 200:
        raise FileNotFoundError(f"Could not download {url}")

    image_bytes = io.BytesIO(response.content)
    img = py.image.load(image_bytes).convert_alpha()

    # scale the image
    w, h = int(128 * size), int(128 * size)
    img = py.transform.scale(img, (w, h))

    IMAGE_CACHE[cache_key] = img
    return img

class Explosion:
    def __init__(self):
        self.size = 0.75
        self.shocksize = 1

        self.images = []
        for i in range(1,12):

            img = get_explosion_frame(i, self.size)
            self.images.append(img)

    def get_image(self,i):
        return self.images[i]