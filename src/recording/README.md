# Instructions on how to use recording functionality

The script will record the audio loopback (of the speakers and microphone-input) and store it in files of 6s length to `./recordings`

<br>

## Prequisites

1. Make sure ALSA is installed on the system
2. Activate `snd-aloop` kernel moduke for setting up loopback devices <br>
    `$ sudo modprobe snd-aloop` <br>
    To activate the module on startup, insert it in `/etc/modules`
3. Install `pyalsaaudio` python module <br>
    `$ pip install pyalsaaudio`

<br>

## Running the script 


1. Start `recording.py` script <br>
    `$ python3 ./recording.py`



<br>
<br> 

---


### Further sources
- https://www.alsa-project.org/wiki/Main_Page 
- https://sysplay.in/blog/linux/2019/06/playing-with-alsa-loopback-devices/
- https://pypi.org/project/pyalsaaudio/