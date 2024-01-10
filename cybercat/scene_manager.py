from multiprocessing.managers import BaseManager
import threading
import time
from typing import Type

import board
import neopixel
import serial

from cybercat.scene_interface import SceneInterface

from cybercat.scenes.rainbow_scene import RainbowScene
from cybercat.scenes.fft_scene import FFTScene

scene_list = [
    RainbowScene,
    FFTScene,
]




from rpi_ws281x import ws, Color, Adafruit_NeoPixel

# LED strip configuration:
# LED_1_COUNT = 1024        # Number of LED pixels.
# LED_1_PIN = 12          # GPIO pin connected to the pixels (must support PWM! GPIO 13 and 18 on RPi 3).
# LED_1_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
# LED_1_DMA = 10          # DMA channel to use for generating signal (Between 1 and 14)
# LED_1_BRIGHTNESS = 10  # Set to 0 for darkest and 255 for brightest
# LED_1_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
# LED_1_CHANNEL = 0       # 0 or 1
# LED_1_STRIP = ws.WS2812_STRIP

# LED_2_COUNT = 1024        # Number of LED pixels.
# LED_2_PIN = 13          # GPIO pin connected to the pixels (must support PWM! GPIO 13 or 18 on RPi 3).
# LED_2_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
# LED_2_DMA = 10          # DMA channel to use for generating signal (Between 1 and 14)
# LED_2_BRIGHTNESS = 10  # Set to 0 for darkest and 255 for brightest
# LED_2_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
# LED_2_CHANNEL = 1       # 0 or 1
# LED_2_STRIP = ws.WS2812_STRIP




class SceneManager:
    def __init__(self, width, height, target_fps = 60):
        self._width = width
        self._height = height
        self._target_fps = target_fps

        # self._pixels = neopixel.NeoPixel(board.D10, self._width * self._height, brightness=0.2, pixel_order=neopixel.GRB, auto_write=False)
        # self._pixels2 = neopixel.NeoPixel(board.D6, self._width * self._height, brightness=0.2, pixel_order=neopixel.GRB, auto_write=False)

        # self._pixels = Adafruit_NeoPixel(LED_1_COUNT, LED_1_PIN, LED_1_FREQ_HZ,
        #                                 LED_1_DMA, LED_1_INVERT, LED_1_BRIGHTNESS,
        #                                 LED_1_CHANNEL, LED_1_STRIP)

        # self._pixels2 = Adafruit_NeoPixel(LED_2_COUNT, LED_2_PIN, LED_2_FREQ_HZ,
        #                                 LED_2_DMA, LED_2_INVERT, LED_2_BRIGHTNESS,
        #                                 LED_2_CHANNEL, LED_2_STRIP)
        
        # self._pixels.begin()
        # self._pixels2.begin()

        self._serial = serial.Serial("/dev/ttyACM0", "115200")
        

        self._current_scene_type: Type[SceneInterface] = RainbowScene

        self._loop_thread_event = threading.Event()
        self._pixel_lock = threading.Lock()
        self._scene_lock = threading.Lock()
        # self._loop_thread = threading.Thread(target=self._loop_thread_f, args=(self._pixels, self._pixels2), daemon=True)
        self._loop_thread = threading.Thread(target=self._loop_thread_f, args=(self._serial,), daemon=True)
        
        self._loop_thread.start()

    def set_brightness(self, brightness):
        with self._pixel_lock:
            self._pixels.brightness = brightness

    def set_scene(self, scene: Type[SceneInterface]):
        with self._scene_lock:
            self._current_scene_type = scene
            print("Setting: " + str(self._current_scene_type))


    # def _loop_thread_f(self, pixels: Adafruit_NeoPixel,  pixels2: Adafruit_NeoPixel):
    def _loop_thread_f(self, serial: serial.Serial):
        current_scene_instance = self._current_scene_type(self._width, self._height)
        last_frame = time.time()
        frame_period = 1.0 / self._target_fps
        frame_counter = 0
        last_sec = time.time()
        while not self._loop_thread_event.is_set():
            time.sleep(frame_period * 0.1)
            now = time.time()

            
            if now > last_sec + 1:
                last_sec = now
                print(frame_counter)
                frame_counter = 0

            with self._scene_lock:
                if self._current_scene_type != type(current_scene_instance):
                    print("Switching to " + self._current_scene_type.__name__)
                    current_scene_instance.deinit()
                    current_scene_instance = self._current_scene_type(self._width, self._height)

            if (now > last_frame + frame_period):
                last_frame = now
                frame_counter += 1
                # frame = current_scene_instance.get_frame()
                
                # frame = [(10, 10, 10)] * (self._width * self._height)
                # frame = [Color(20, 20, 20)] * (self._width * self._height)
                # buf = bytearray([10] * (self._width * self._height * 3))
                # frame = [Color(*x) for x in current_scene_instance.get_frame()]
                # with self._pixel_lock:
                #     for i in range(pixels2.numPixels()):
                #         # pixels[i] = frame[i]
                #         pixels.setPixelColor(i, frame[i])
                #         pixels2.setPixelColor(i, frame[i])

                #     # pixels._post_brightness_buffer = buf
                #     # pixels2._post_brightness_buffer = buf
                #     pixels.show()
                #     pixels2.show()

                frame = [42, 0, 0]
                for x in current_scene_instance.get_frame():
                    frame.extend(x)
                # print(len(frame))
                # frame = [42, 0, 0] + ([10] * (32 * 64 * 3))
                serial.write(bytes(frame))

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