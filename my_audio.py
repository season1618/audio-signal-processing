import wave
import pyaudio

class MyAudio:
    def __init__(self, file = ".\sample.wav", n = 1024, fs = 48000):
        self.file = file
        self.n = n
        self.fs = fs # sampling frequency [Hz]
    

    def record(self, record_time = 5):
        p = pyaudio.PyAudio()

        stream = p.open(
            format = pyaudio.paInt16, # 16bit
            channels = 1,
            rate = self.fs,
            input = True,
            input_device_index = 0,
            frames_per_buffer = self.n
        )

        print("start")

        frames = []
        for i in range(0, int(self.fs * record_time / self.n)):
            frames.append(stream.read(self.n))

        print("end")

        stream.close()
        p.terminate()

        wf = wave.open(self.file, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(frames))
        wf.close()

    def play(self):
        wf = wave.open(self.file, 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(
            format = p.get_format_from_width(wf.getsampwidth()),
            channels = wf.getnchannels(),
            rate = wf.getframerate(),
            input_device_index = 0,
            output = True,
        )
        while True:
            data = wf.readframes(self.n)
            if data == b'':
                break
            stream.write(data)
        stream.close()
        p.terminate()

myaudio = MyAudio()
while True:
    args = input().split()
    length = len(args)
    if length == 0:
        break
    
    if args[0] == 'r':
        if length == 1:
            myaudio.record()
        else:
            myaudio.record(int(args[1]))
    elif args[0] == 'p':
        myaudio.play()
    else:
        break