import pygame as py
import math
import vectors
import config
import random
import requests
import io

# Global dictionary to store surfaces
IMAGE_CACHE = {}

def get_cloud_image(index):
    """
    Returns a Surface for cloud #index from S3, downloaded once.
    """
    cache_key = f"cloud{index}"
    if cache_key in IMAGE_CACHE:
        return IMAGE_CACHE[cache_key]

    url = f"https://sky-warrior.s3.us-east-2.amazonaws.com/images/clouds/cloud{index}.png"
    response = requests.get(url)
    if response.status_code != 200:
        raise FileNotFoundError(f"Could not download {url}")

    image_bytes = io.BytesIO(response.content)
    img = py.image.load(image_bytes).convert_alpha()

    # scale to self.scale if needed (optional, or do it later in code)
    # but if you do the scaling here, store the scaled version in the cache

    IMAGE_CACHE[cache_key] = img
    return img

class Clouds:
    def __init__(self):
        self.cloud_imgs = []
        self.scale = 700
        for i in range(1,14):

            img = get_cloud_image(i)
            img = py.transform.scale(img,(self.scale,self.scale))
            self.cloud_imgs.append(img)


    def draw(self,win,pos,camoff):

        if pos[0] < 0:
            qx = int(pos[0]/self.scale -1)
        else:
            qx = int(pos[0] / self.scale )
        if pos[1] < 0:
            qy = int(pos[1]/self.scale - 1)
        else:
            qy = int(pos[1] / self.scale )

        i = math.fabs(qx+qy)%13
        xys = [[qx*self.scale, qy*self.scale, i]]


        lqx = qx-1
        lqy = qy
        l = math.fabs(lqx + lqy) % 13
        xys.append([lqx*self.scale,lqy*self.scale,l])

        lqx = qx - 1
        lqy = qy-1
        l = math.fabs(lqx + lqy) % 13
        xys.append([lqx * self.scale, lqy * self.scale, l])

        lqx = qx + 1
        lqy = qy - 1
        l = math.fabs(lqx + lqy) % 13
        xys.append([lqx * self.scale, lqy * self.scale, l])

        rqx = qx+1
        rqy = qy
        r = math.fabs(rqx + rqy) % 13
        xys.append([rqx*self.scale, rqy*self.scale, r])

        rqx = qx + 1
        rqy = qy+1
        r = math.fabs(rqx + rqy) % 13
        xys.append([rqx * self.scale, rqy * self.scale, r])

        rqx = qx - 1
        rqy = qy + 1
        r = math.fabs(rqx + rqy) % 13
        xys.append([rqx * self.scale, rqy * self.scale, r])

        uqx = qx
        uqy = qy-1
        u = math.fabs(uqx + uqy) % 13
        xys.append([uqx*self.scale, uqy*self.scale, u])

        dqx = qx
        dqy = qy+1
        d = math.fabs(dqx + dqy) % 13
        xys.append([dqx*self.scale, dqy*self.scale, d])

        for xy in xys:
            ind = int(xy[2])
            random.seed(xy[0]*xy[1]+xy[1])
            c = random.randint(0,1)
            if c==1:
                g = vectors.sub_vec([xy[0],xy[1]],pos)
                g = vectors.add_vec(g,[config.screen_width/2+camoff[0],config.screen_height/2+camoff[1]])
                g = vectors.ret_int(g)
                win.blit(self.cloud_imgs[ind],g)