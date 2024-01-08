class SceneInterface:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def get_frame(self):
        return [(0, 0, 255)] * (self.width * self.height)
    
    def deinit(self):
        pass