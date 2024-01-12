from cybercat.scene_interface import SceneInterface



class BlankScene(SceneInterface):

    def __init__(self, width, height):
        num_pixels = width * height
        self.frame = []
        for i in range(num_pixels):
            self.frame.append((0, 0, 0))

        super().__init__(width, height)
    
    def get_frame(self):
        return self.frame