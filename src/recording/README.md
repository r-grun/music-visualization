# Instructions on how to use recording functionality

The script will record the audio loopback (of the speakers and microphone-input)  as `.wav` file and store it in files of 6s length to `./recordings`

<br>

## Prequisites

1. Make sure ALSA is installed on the system
2. Activate `snd-aloop` kernel moduke for setting up loopback devices <br>
    `$ sudo modprobe snd-aloop` <br>
    `$ arecord -l` will provide a list of the installed soundcards.<br>
    To activate the module on startup, insert it in `/etc/modules`.<br>
    The loopback card will then be card 0.
3. Install `pyalsaaudio` python module <br>
    `$ pip install pyalsaaudio`

<br>

## Start recording and running the script 


2. Start `recording.py` script <br>
    `$ python3 ./recording.py [-d <device>]`<br>
    A specific device can be omitted by passing it via the parameter `-d`



<br>
<br> 

---


### Further sources
- https://www.alsa-project.org/wiki/Main_Page 
- https://sysplay.in/blog/linux/2019/06/playing-with-alsa-loopback-devices/
- https://pypi.org/project/pyalsaaudio/