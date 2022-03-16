# Instructions on how to use recording functionality

The script will record the audio loopback (of the speakers and microphone-input)  as `.wav` file and store it in files of 6s length to `./recordings`

<br>

## Prequisites

1. Make sure ALSA is installed on the system
2. Run `$ sudo apt install -y portaudio19-dev python3-pyaudio`
3. Run `$ alsamixer` to open the alsamixer
4. Press F4 to switch to [Capture]-Mode
5. Increase volume to 100% using the Up-Arrow-Key
6. End `alsamixer` by pressing ESC


<br>

## Start recording and running the script 

Run `python3 recording.py` <br>
Note that the mic input at index 1 is used.
Find the index by using the `list_audio_devices.py`. The number behind the device is the used index


<br>
<br> 

---


### Further sources

- https://makersportal.com/blog/2018/8/23/recording-audio-on-the-raspberry-pi-with-python-and-a-usb-microphone
- https://stackoverflow.com/questions/48690984/portaudio-h-no-such-file-or-directory

