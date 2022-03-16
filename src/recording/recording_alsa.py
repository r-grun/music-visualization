import sys
import time
import getopt
import wave
import os
import alsaaudio

path = './recordings/'
rec_file = 'rec.raw'
conv_file = 'rec.wav'


def usage():
    print('usage: recordtest.py [-d <device>]', file=sys.stderr)
    sys.exit(2)


if __name__ == '__main__':

    device = 'default'

    opts, args = getopt.getopt(sys.argv[1:], 'd:')
    for o, a in opts:
        if o == '-d':
            device = a

    if not args:
        usage()
        
    os.makedirs(os.path.dirname(path + rec_file), exist_ok=True)
        
    f = open(path + rec_file, 'wb')

	# Open the device in nonblocking capture mode in mono, with a sampling rate of 44100 Hz
	# and 16 bit little endian samples
	# The period size controls the internal number of frames per period.
	# The significance of this parameter is documented in the ALSA api.
	# For our purposes, it is suficcient to know that reads from the device
	# will return this many frames. Each frame being 2 bytes long.
	# This means that the reads below will return either 320 bytes of data
	# or 0 bytes of data. The latter is possible because we are in nonblocking
	# mode.
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, channels=1,
        rate=44100, format=alsaaudio.PCM_FORMAT_S16_LE, periodsize=160, device=device)

    while True:
        loops = 6000
        while loops > 0:
            loops -= 1
            # Read data from device
            l, data = inp.read()

            if l:
                f.write(data)
                time.sleep(.001)
                print(loops)

        with open(path + rec_file, "rb") as inp_f:
            data_conv = inp_f.read()
            with wave.open(conv_file, "wb") as out_f:
                out_f.setnchannels(1)
                out_f.setsampwidth(2) # number of bytes
                out_f.setframerate(44100)
                out_f.writeframesraw(data_conv)