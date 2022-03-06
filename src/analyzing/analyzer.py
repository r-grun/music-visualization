import soundcard as sc
import numpy as np
from scipy.special import softmax
from essentia import Pool, run, reset
from essentia.streaming import (
    VectorInput,
    FrameCutter,
    PercivalBpmEstimator
)

def save_to_db(bpm, vol, key):
    pass


def callback_console(data, buffer, pool, vimp):
    buffer[:] = data.flatten()

    # Generate predictions.
    reset(vimp)
    run(vimp)
    
    print(pool['bpm'])


def main():

    sample_rate = 44100
    frame_size = 512 
    hop_size = 256
    n_bands = 96
    patch_size = 64
    display_size = 10

    buffer_size = patch_size * hop_size


    # Configure algorithms
    buffer = np.zeros(buffer_size, dtype='float32')
    vimp = VectorInput(buffer)
    fc = FrameCutter(frameSize=frame_size, hopSize=hop_size)
    bpm = PercivalBpmEstimator(frameSize = frame_size, hopSize = hop_size, sampleRate = sample_rate)
    pool = Pool()


    # Configure network
    vimp.data   >>  fc.signal
    fc.frame    >>  bpm.signal
    bpm.bpm     >>  (pool, 'bpm')



    pool.clear()

    # Capture and process the speakers loopback.
    with sc.all_microphones(include_loopback=True)[0].recorder(samplerate=sample_rate) as mic:
        while True:
            callback_console(mic.record(numframes=buffer_size).mean(axis=1), buffer, pool, vimp)




if (__name__ == "__main__"):
    main()