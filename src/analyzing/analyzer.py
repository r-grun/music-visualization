import soundcard as sc
import numpy as np
from scipy.special import softmax
from essentia import Pool, run, reset
from essentia.streaming import (
    VectorInput,
    FrameCutter,
    RhythmExtractor2013
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
    patch_size = 64
    length_factor = 15

    buffer_size = patch_size * hop_size * length_factor


    # Configure algorithms
    buffer = np.zeros(buffer_size, dtype='float32')
    vimp = VectorInput(buffer)
    # fc = FrameCutter(frameSize=frame_size, hopSize=hop_size)
    extractor = RhythmExtractor2013()
    pool = Pool()


    # Configure network
    # vimp.data   >>  fc.signal
    # fc.frame    >>  extractor.signal
    vimp.data   >>  extractor.signal
    extractor.bpm     >>  (pool, 'bpm')
    extractor.ticks     >>  (pool, 'ticks')
    extractor.confidence     >>  (pool, 'confidence')
    extractor.estimates     >>  (pool, 'estimates')
    extractor.bpmIntervals     >>  (pool, 'bpmIntervals')



    pool.clear()

    # Capture and process the speakers loopback.
    with sc.all_microphones(include_loopback=True)[0].recorder(samplerate=sample_rate) as mic:
        while True:
            callback_console(mic.record(numframes=buffer_size).mean(axis=1), buffer, pool, vimp)




if (__name__ == "__main__"):
    main()