import numpy as np
import essentia.standard as es
import redis

file_name = 'recordings/rec.wav'

redis = redis.Redis(host='172.28.1.4', port=6379, db=0)


def save_to_db(bpm, vol, key) -> None:
    """
        Saves the omitted values to the redis db
    """

    redis.set('bpm', bpm)
    print('bpm (' + str(bpm) + ') written to redis.')

    redis.set('vol', vol)
    print('vol (' + str(vol) + ') written to redis.')

    redis.set('key', key)
    print('key (' + str(key) + ') written to redis.')


def main():

    print('Analyzer started.')

    sample_rate = 44100
    frame_size = 512 
    hop_size = 256
    patch_size = 64
    length_factor = 15

    buffer_size = patch_size * hop_size * length_factor


    # Loading an audio file.
    audio = es.EasyLoader(filename=file_name, sampleRate = sample_rate)() # try MonoLoader, EqloudLoader
    print(file_name + ' loaded.')

    # Compute beat positions and BPM.
    rhythm_extractor = es.RhythmExtractor2013(method="multifeature")
    bpm, _, _, _, _ = rhythm_extractor(audio)
    print('Rhythm extracted.')

    loudness_extractor = es.Loudness()
    vol = loudness_extractor(audio)
    print('Loudness extracted.')

    key_extractor = es.KeyExtractor(sampleRate = sample_rate)
    key, scale, _ = key_extractor(audio)
    print('Key extracted.')
    

    save_to_db(bpm, vol, str(key + ' ' + scale))


    # For testing only
    # writer = es.MonoWriter(filename='rec_cleaned.wav', format='wav', sampleRate=sample_rate)
    # writer(audio)

    # print('File saved.')



if (__name__ == "__main__"):
    main()