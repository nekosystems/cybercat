from multiprocessing.managers import BaseManager
import threading
import time
from typing import Type

import board
import neopixel

from cybercat.scene_interface import SceneInterface

from cybercat.scenes.rainbow_scene import RainbowScene
from cybercat.scenes.fft_scene import FFTScene

scene_list = [
    RainbowScene,
    FFTScene,
]




class SceneManager:
    def __init__(self, width, height, target_fps = 60):
        self._width = width
        self._height = height
        self._target_fps = target_fps

        self._pixels = neopixel.NeoPixel(board.D10, self._width * self._height, brightness=0.2, pixel_order=neopixel.GRB, auto_write=False)
        self._current_scene_type: Type[SceneInterface] = RainbowScene

        self._loop_thread_event = threading.Event()
        self._pixel_lock = threading.Lock()
        self._scene_lock = threading.Lock()
        self._loop_thread = threading.Thread(target=self._loop_thread_f, args=(self._pixels,), daemon=True)
        
        self._loop_thread.start()

    def set_brightness(self, brightness):
        with self._pixel_lock:
            self._pixels.brightness = brightness

    def set_scene(self, scene: Type[SceneInterface]):
        with self._scene_lock:
            self._current_scene_type = scene


    def _loop_thread_f(self, pixels: neopixel.NeoPixel):
        current_scene_instance = self._current_scene_type(self._width, self._height)
        last_frame = time.time()
        frame_period = 1.0 / self._target_fps
        while not self._loop_thread_event.is_set():
            time.sleep(frame_period * 0.1)
            now = time.time()

            with self._scene_lock:
                if self._current_scene_type != type(current_scene_instance):
                    print("Switching to " + self._current_scene_type.__name__)
                    current_scene_instance.deinit()
                    current_scene_instance = self._current_scene_type(self._width, self._height)

            if (now > last_frame + frame_period):
                last_frame = now

                frame = current_scene_instance.get_frame()

                with self._pixel_lock:
                    for i in range(pixels.n):
                        pixels[i] = frame[i]
                    pixels.show()

            # last_update = time.time()
            # last_sec = time.time()
            # num_frames = 0
            # while True:
            #     now = time.time()
            #     if (now - last_update) > (1./fps):
            #         last_update = time.time()
            #         raw_fftx, raw_fft, binned_fftx, binned_fft = ear.get_audio_features()
            #         num_frames += 1
            #     elif args.sleep_between_frames:
            #         time.sleep(((1./fps)-(time.time()-last_update)) * 0.99)
                
            #     if now > last_sec + 1:
            #         print(num_frames)
            #         num_frames = 0
            #         last_sec = now












class CustomManager(BaseManager):
    pass
CustomManager.register("SceneManager", SceneManager)