from cybercat.scene_interface import SceneInterface

import colorsys
import time


class RainbowScene(SceneInterface):

    def __init__(self, width, height):
        self.last_frame = time.time()

        num_pixels = width * height
        self.frame = []
        for i in range(num_pixels):
            color = colorsys.hsv_to_rgb(i/num_pixels, 1.0, 1.0)
            self.frame.append((int(color[0]*255), int(color[1]*255), int(color[2]*255)))

        super().__init__(width, height)
    
    def get_frame(self):
        self.frame.append(self.frame.pop(0))
        return self.frame