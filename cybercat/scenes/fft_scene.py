from cybercat.scene_interface import SceneInterface
from cybercat.fft.stream_analyzer import Stream_Analyzer

import numpy as np

import colorsys
import time


class FFTScene(SceneInterface):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.frame = [(0, 0, 0)] * (width * height)
        self.ear = Stream_Analyzer(
                    device = None,        # Pyaudio (portaudio) device index, defaults to first mic input
                    rate   = None,               # Audio samplerate, None uses the default source settings
                    FFT_window_size_ms  = 30,    # Window size used for the FFT transform
                    updates_per_second  = 500,  # How often to read the audio stream for new data
                    smoothing_length_ms = 100,    # Apply some temporal smoothing to reduce noisy features
                    n_frequency_bins = 100, # The FFT features are grouped in bins
                    visualize = False,               # Visualize the FFT features with PyGame
                    verbose   = False,    # Print running statistics (latency, fps, ...)
                    height    = height,     # Height, in pixels, of the visualizer window,
                    window_ratio = 1.0  # Float ratio of the visualizer window. e.g. 24/9
                )

        super().__init__(width, height)
    
    def get_frame(self):
        
        raw_fftx, raw_fft, binned_fftx, binned_fft = self.ear.get_audio_features()
        if np.min(self.ear.bin_mean_values) > 0:
            frequency_bin_energies = 0.2 * self.ear.frequency_bin_energies / self.ear.bin_mean_values
            
            feature_values = frequency_bin_energies[::-1]
            # print(feature_values)
            feature_values = feature_values * self.height
            for w in range(self.width):
                for h in range(self.height):
                    if feature_values[w] > h:
                        self.frame[w * self.width + h] = (255, 255, 255)
                    else:
                        self.frame[w * self.width + h] = (0, 0, 0)
        return self.frame