import pyaudio
import wave
import subprocess


form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
sample_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
record_secs = 6 # seconds to record
dev_index = 1 # device index found by list_audio_devices.py
wav_output_filename = 'recordings/rec.wav' # name of .wav file


def trigger_analyzer():
    subprocess.call(['docker', 'start', 'music-analyzer'])


def record():

    audio = pyaudio.PyAudio()

    stream = audio.open(format = form_1,rate = sample_rate,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=chunk)

    frames = []

    # loop through stream and append audio chunks to frame array
    for ii in range(0,int((sample_rate/chunk)*record_secs)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wavefile = wave.open(wav_output_filename,'wb')
    wavefile.setnchannels(chans)
    wavefile.setsampwidth(audio.get_sample_size(form_1))
    wavefile.setframerate(sample_rate)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()

    print('rec.wav file saved.')
    trigger_analyzer()



if __name__ == '__main__':

    try:
        while True:
            record()
    except KeyboardInterrupt:
        pass