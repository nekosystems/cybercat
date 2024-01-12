from cybercat.scene_manager import CustomManager, SceneManager, scene_list
import os

from nicegui import ui



width = 64
height = 32
max_brightness = 0.2
default_brightness = 0.05
media_dir = os.path.join("cybercat", "media")

# def parse_args():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--device', type=int, default=None, dest='device',
#                         help='pyaudio (portaudio) device index')
#     parser.add_argument('--height', type=int, default=450, dest='height',
#                         help='height, in pixels, of the visualizer window')
#     parser.add_argument('--n_frequency_bins', type=int, default=100, dest='frequency_bins',
#                         help='The FFT features are grouped in bins')
#     parser.add_argument('--verbose', action='store_true')
#     parser.add_argument('--window_ratio', default='24/9', dest='window_ratio',
#                         help='float ratio of the visualizer window. e.g. 24/9')
#     parser.add_argument('--sleep_between_frames', dest='sleep_between_frames', action='store_true',
#                         help='when true process sleeps between frames to reduce CPU usage (recommended for low update rates)')
#     return parser.parse_args()

# def convert_window_ratio(window_ratio):
#     if '/' in window_ratio:
#         dividend, divisor = window_ratio.split('/')
#         try:
#             float_ratio = float(dividend) / float(divisor)
#         except:
#             raise ValueError('window_ratio should be in the format: float/float')
#         return float_ratio
#     raise ValueError('window_ratio should be in the format: float/float')

# def run_FFT_analyzer():
#     args = parse_args()
#     window_ratio = convert_window_ratio(args.window_ratio)

#     ear = Stream_Analyzer(
#                     device = args.device,        # Pyaudio (portaudio) device index, defaults to first mic input
#                     rate   = None,               # Audio samplerate, None uses the default source settings
#                     FFT_window_size_ms  = 30,    # Window size used for the FFT transform
#                     updates_per_second  = 500,  # How often to read the audio stream for new data
#                     smoothing_length_ms = 100,    # Apply some temporal smoothing to reduce noisy features
#                     n_frequency_bins = args.frequency_bins, # The FFT features are grouped in bins
#                     visualize = 0,               # Visualize the FFT features with PyGame
#                     verbose   = args.verbose,    # Print running statistics (latency, fps, ...)
#                     height    = args.height,     # Height, in pixels, of the visualizer window,
#                     window_ratio = window_ratio  # Float ratio of the visualizer window. e.g. 24/9
#                     )

#     fps = 60  #How often to update the FFT features + display
#     last_update = time.time()
#     last_sec = time.time()
#     num_frames = 0
#     while True:
#         now = time.time()
#         if (now - last_update) > (1./fps):
#             last_update = time.time()
#             raw_fftx, raw_fft, binned_fftx, binned_fft = ear.get_audio_features()
#             num_frames += 1
#         elif args.sleep_between_frames:
#             time.sleep(((1./fps)-(time.time()-last_update)) * 0.99)
        
#         if now > last_sec + 1:
#             print(num_frames)
#             num_frames = 0
#             last_sec = now










if __name__ in {"__main__", "__mp_main__"}:
    # run_FFT_analyzer()

    # import serial
    # import time

    # ser = serial.Serial("/dev/ttyACM0", "115200")
    # print(ser.name)

    # f = [42, 0, 0] + ([10] * (32 * 64 * 3))
    # # print(bytes(f))
    # # print("1")
    # ser.write(b'@')
    # ser.write(bytes(f))
    # # ser.write(b'*   ')
    # # ser.write(b'?')
    # # print("2")
    # # time.sleep(1)
    # # print(ser.read_all())
    # ser.close()
    # # print("3")
    # exit()


    with CustomManager() as m:
        scene_manager:SceneManager = m.SceneManager(width, height, target_fps=30, default_brightness=default_brightness)

        ui.label('CYBERCAT')
        ui.separator()
        brightness_slider = ui.slider(min=0, max=max_brightness, step=0.01, value=default_brightness, on_change=lambda: scene_manager.set_brightness(brightness_slider.value))
        for scene in scene_list:
            ui.button(scene.__name__, on_click=lambda scene=scene: scene_manager.set_scene(scene))
        
        files = [f for f in os.listdir(media_dir) if os.path.isfile(os.path.join(media_dir, f))]
        selections = {os.path.join(media_dir, f): f.split(".")[0] for f in files}
        media_selector = ui.select(selections, on_change=lambda: scene_manager.set_media(media_selector.value))

        ui.run(reload=False, show = False)