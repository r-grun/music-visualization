import json

from essentia.streaming import (
    VectorInput,
    FrameCutter,
    TempoCNN,
    MonoLoader
)
from essentia import Pool, run, reset, log, EAll
import numpy as np
from scipy.special import softmax
import soundcard as sc
from datetime import datetime


log.infoActive = True                   # activate the info level
log.debugLevels += EAll        # activate all debug modules

with open('deeptemp-k16-3.json', 'r') as json_file:
    metadata = json.load(json_file)

model_file = 'deeptemp-k16-3.pb'
input_layer = metadata['schema']['inputs'][0]['name']
output_layer = metadata['schema']['outputs'][0]['name']

# Analysis parameters.
sample_rate = 11025
frame_size = 1024 
hop_size = 256
n_bands = 40
patch_size = 64
display_size = 10

buffer_size = patch_size * hop_size
buffer_size = buffer_size * 15





buffer = np.zeros(buffer_size, dtype='float32')
vimp = VectorInput(buffer)
fc = FrameCutter(frameSize=frame_size, hopSize=hop_size)
tempo = TempoCNN(graphFilename=model_file,
                        input=input_layer,
                        output=output_layer)
pool = Pool()
loader = MonoLoader(filename='fireworks.mp3', sampleRate = sample_rate)



loader.audio   >> fc.signal
fc.frame    >> tempo.audio
tempo.globalTempo   >>  (pool, 'global')
tempo.localTempo   >>  (pool, 'local')
tempo.localTempoProbabilities   >>  (pool, 'prob')





bpms = [x for x in range(1, 256)]

def callback_console(data):
    buffer[:] = data.flatten()

    # Generate predictions.
    reset(vimp)
    run(vimp)
    
    # Kernel Error: 
    print(pool.containsKey(output_layer))
    
    if pool.containsKey(output_layer):
        print(datetime.now())
        print(pool['global'][-1, :].T)
        index_max = np.argmax(softmax(20 * pool['local'][-1, :].T))
        print(bpms[index_max])


pool.clear()


# # Capture and process the speakers loopback.
# with sc.all_microphones(include_loopback=True)[0].recorder(samplerate=sample_rate) as mic:
#     while True:
#         callback_console(mic.record(numframes=buffer_size).mean(axis=1))


reset(loader)
run(loader)

print('global BPM: {}'.format(pool['global']))