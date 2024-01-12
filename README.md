### Attributions:
 - Realtime audio FFT analysis implementation: https://github.com/aiXander/Realtime_PyAudio_FFT/tree/master
 - High speed WS2812B driver over arduino: https://github.com/adafruit/Adafruit_NeoPXL8

### Required Hardware (or at least what I am using):
 - Raspberry Pi 4 Model B, 8GB of ram just to be safe (though I used a 2GB version during development)
 - RP2040 dev board of some sort, I used BL2040 Mini because that's what I had at the time
 - WS2812B based display matrix
 - USB microphone
 - USB wifi adapter

### Steps:
 - Use Raspberry Pi Imager to image the latest Raspberry Pi OS (64-bit) (2023-12-05 release as of right now) on a micro sd card
    - In the settings for OS customisation, set hostname whatever you'd like, and set username and password to something memorable but fairly secure. Don't configure wireless LAN at all, as this needs to be set up as a hotspot, but do set locale settings as it is convenient
    - Make sure SSH is enabled using password authentication under services
 - Boot up Raspberry pi with a monitor and keyboard/mouse connected to configure it (can't be bothered to figure out how to automate this at the moment)
 - Disable bluetooth comms on the taskbar
 - Under the wifi menu, there should be an option to create a hotspot.
    - Make sure to pick the onboard integrated wifi interface
    - pick wpa2 because wpa3 just doesn't seem to work at the moment
    - Give it a name and password, this is what you will connect to for controlling the Pi
    - Set it to autoconnect, with priority 1
 - Connect to the internet using the USB wifi adapter, set to autoconnect with priority 0
 - `sudo apt install python3-poetry libportaudio-dev`
 - `poetry config virtualenvs.in-project true`
 - `git clone this repo`
 - `cd cybercat`
 - `poetry install`
 - `poetry run python -m cybercat`
 - Using another device, connect to the wifi hotspot that the Pi is running, and then use the browser to navigate to `<hostname>.local:8080` (replace "hostname" with the Pi's hostname). This should show the web interface
