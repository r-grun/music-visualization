import json

from essentia.streaming import (
    VectorInput,
    FrameCutter,
    TensorflowInputMusiCNN,
    VectorRealToTensor,
    TensorToPool,
    TensorflowPredict,
    PoolToTensor,
    TensorToVectorReal
)
from essentia import Pool, run, reset
import numpy as np
from scipy.special import softmax
import soundcard as sc



with open('msd-musicnn-1.json', 'r') as json_file:
    metadata = json.load(json_file)

model_file = 'msd-musicnn-1.pb'
input_layer = metadata['schema']['inputs'][0]['name']
output_layer = metadata['schema']['outputs'][0]['name']
classes = metadata['classes']
n_classes = len(classes)

# Analysis parameters.
sample_rate = 16000
frame_size = 512 
hop_size = 256
n_bands = 96
patch_size = 64
display_size = 10

buffer_size = patch_size * hop_size



buffer = np.zeros(buffer_size, dtype='float32')
vimp = VectorInput(buffer)
fc = FrameCutter(frameSize=frame_size, hopSize=hop_size)
tim = TensorflowInputMusiCNN()
vtt = VectorRealToTensor(shape=[1, 1, patch_size, n_bands],
                         lastPatchMode='discard')
ttp = TensorToPool(namespace=input_layer)
tfp = TensorflowPredict(graphFilename=model_file,
                        inputs=[input_layer],
                        outputs=[output_layer])
ptt = PoolToTensor(namespace=output_layer)
ttv = TensorToVectorReal()
pool = Pool()



vimp.data   >> fc.signal
fc.frame    >> tim.frame
tim.bands   >> vtt.frame
tim.bands   >> (pool, 'melbands')
vtt.tensor  >> ttp.tensor
ttp.pool    >> tfp.poolIn
tfp.poolOut >> ptt.pool
ptt.tensor  >> ttv.tensor
ttv.frame   >> (pool, output_layer)


def callback_console(data):
    buffer[:] = data.flatten()

    # Generate predictions.
    reset(vimp)
    run(vimp)
    
    index_max = np.argmax(softmax(20 * pool[output_layer][-1, :].T))
    print(classes[index_max])




pool.clear()

# Capture and process the speakers loopback.
with sc.all_microphones(include_loopback=True)[0].recorder(samplerate=sample_rate) as mic:
    while True:
        callback_console(mic.record(numframes=buffer_size).mean(axis=1))