from cybercat.scene_interface import SceneInterface

import imageio.v3 as iio
from PIL import Image, ImageSequence, ImageOps

import time



class MediaScene(SceneInterface):

    def __init__(self, width, height, media: str):
        self.width = width
        self.height = height
        num_pixels = width * height
        self.frame = [(0, 0, 0)] * num_pixels

        self._media_handle = Image.open(media)
        if (getattr(self._media_handle, "is_animated", False)):
            self._media_frames = ImageSequence.Iterator(self._media_handle)
        else:
            self._media_frames = [self._media_handle]
        # def resized(frames):
        #     for f in frames:
        #         result = f.convert("RGB")
        #         result.thumbnail((width, height), Image.ANTIALIAS)
        #         yield ImageOps.pad(result, (width, height), color=(0, 0, 0))
            
        def resized(frames):
            ret = []
            for f in frames:
                result = f.convert("RGB")
                result.thumbnail((width, height), Image.LANCZOS)
                ret.append(ImageOps.pad(result, (width, height), color=(0, 0, 0)))
            return ret

        self._media_frames = resized(self._media_frames)

        self._index = 0
        self._frame_shown_at = time.monotonic()
        self._fill_frame(self._index)

        super().__init__(width, height)

    def _fill_frame(self, i):
        frame_data = list(self._media_frames[i].getdata())
        for w in range(self.width):
            for h in range(self.height):
                self.frame[w * self.height + h] = frame_data[w + self.width * h]

    def _get_frame_d(self, i):
        return self._media_frames[i].info.get("duration", 1000/15) / 1000
    
    def get_frame(self):
        now = time.monotonic()
        last_index = self._index
        duration_s = self._get_frame_d(self._index)
        delta = now - self._frame_shown_at
        while delta > duration_s:
            delta -= duration_s
            self._frame_shown_at += duration_s
            self._index = (self._index + 1) % len(self._media_frames)
            duration_s = self._get_frame_d(self._index)

        if self._index != last_index:
            self._fill_frame(self._index)

        return self.frame
    
    def deinit(self):
        return super().deinit()