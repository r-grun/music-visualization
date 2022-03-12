import soundcard as sc
import numpy as np
from scipy.special import softmax
from essentia import run, reset
from essentia.streaming import (
    VectorInput,
    MonoWriter
)

def main():

    sample_rate = 44100
    hop_size = 256
    patch_size = 64
    length_factor = 15

    buffer_size = patch_size * hop_size * length_factor


    # Configure algorithms
    buffer = np.zeros(buffer_size, dtype='float32')
    vimp = VectorInput(buffer)
    writer = MonoWriter(filename='recording.wav')


    # Configure network
    vimp.data   >>  writer.audio



    # Capture and process the speakers loopback.
    with sc.all_microphones(include_loopback=True)[0].recorder(samplerate=sample_rate) as mic:
        while True:
            audio_input = mic.record(numframes=buffer_size).mean(axis=1)

            buffer[:] = audio_input.flatten()

            reset(vimp)
            run(vimp)




if (__name__ == "__main__"):
    main()