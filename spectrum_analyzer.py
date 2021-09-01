import math
import wave
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def spectrum_analyzer1(file):
    wf = wave.open(file, 'rb')
    n = 1024
    fs = wf.getframerate()

    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)
    lines1, = ax1.plot([], [])
    lines2, = ax2.plot([], [])

    hamming_window = np.hamming(n)
    time = np.array(list(range(n)))
    freq = np.fft.fftfreq(n, 1 / fs)

    p = pyaudio.PyAudio()
    stream = p.open(
        format = p.get_format_from_width(wf.getsampwidth()),
        channels = wf.getnchannels(),
        rate = fs,
        input_device_index = 0,
        output = True,
    )

    def update(i):
        data = wf.readframes(n)
        stream.write(data)
        ampl1 = np.frombuffer(data, dtype = "int16") * hamming_window
        ampl2 = abs(np.fft.fft(ampl1)) / n * 2

        ax1.set_xlim(0, 1024)
        ax1.set_ylim(-10000, 10000)
        lines1.set_data(time, ampl1)

        ax2.set_xlim(0, 20000)
        ax2.set_ylim(0, 1000)
        lines2.set_data(freq[0:n//2+1], ampl2[0:n//2+1])
        
        return lines1, lines2

    ani = animation.FuncAnimation(
        fig,
        update,
        frames = math.ceil(wf.getnframes() / n),
        interval = 0,
        blit = True
    )
    plt.show()
    plt.close()

    stream.close()
    p.terminate()

def spectrum_analyzer2():
    n = 1024
    fs = 48000 # sampling frequency [Hz]

    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)
    lines1, = ax1.plot([], [])
    lines2, = ax2.plot([], [])

    hamming_window = np.hamming(n)
    time = np.array(list(range(n)))
    freq = np.fft.fftfreq(n, 1 / fs)

    p = pyaudio.PyAudio()
    stream = p.open(
        format = pyaudio.paInt16, # 16bit
        channels = 1, # monaural
        rate = fs,
        input = True,
        input_device_index = 0,
        frames_per_buffer = n
    )

    def update(i):
        ampl1 = np.frombuffer(stream.read(n), dtype = "int16") * hamming_window
        ampl2 = abs(np.fft.fft(ampl1)) / n * 2

        ax1.set_xlim(0, 1024)
        ax1.set_ylim(-10000, 10000)
        lines1.set_data(time, ampl1)

        ax2.set_xlim(0, 20000)
        ax2.set_ylim(0, 1000)
        lines2.set_data(freq[0:n//2+1], ampl2[0:n//2+1])

        return lines1, lines2

    ani = animation.FuncAnimation(
        fig,
        update,
        interval = 0,
        blit = True
    )
    plt.show()
    #ani.save('.\sample.gif', writer = 'pillow')
    plt.close()

    stream.close()
    p.terminate()

#spectrum_analyzer1(".\sample.wav")
spectrum_analyzer2()