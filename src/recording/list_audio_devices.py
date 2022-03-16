import pyaudio
p = pyaudio.PyAudio()

for index in range(p.get_device_count()):
        print(p.get_device_info_by_index(index).get('name') + '\t' + str(index))