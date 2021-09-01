import math
import wave
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def cepstrum_analyzer1(file):
    wf = wave.open(file, 'rb')

    n = 1024
    fs = wf.getframerate()
    ceps_dim = 20 # cepstrum dimension

    p = pyaudio.PyAudio()
    stream = p.open(
        format = p.get_format_from_width(wf.getsampwidth()),
        channels = wf.getnchannels(),
        rate = fs,
        input_device_index = 0,
        output = True,
    )

    hamming_window = np.hamming(n)
    quef = np.array(list(range(n)))
    freq = np.fft.fftfreq(n, 1 / fs)

    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)
    lines1, = ax1.plot([], [])
    lines2, = ax2.plot([], [])
    lines3, = ax2.plot([], [], color = 'red')

    def update(i):
        data = wf.readframes(n)
        stream.write(data)

        ampl = np.frombuffer(data, dtype = "int16") * hamming_window
        spec_log = 20 * np.log10(abs(np.fft.fft(ampl)) / n * 2)
        ceps = np.real(np.fft.ifft(spec_log))

        ax1.set_xlim(0, n//2)
        ax1.set_ylim(-10, 10)
        lines1.set_data(quef[0:n//2], ceps[0:n//2])

        ceps_env = np.array(ceps)
        ceps_env[ceps_dim:n-ceps_dim+1] = 0
        spec_env = np.real(np.fft.fft(ceps_env))

        ax2.set_xlim(0, 5000)
        ax2.set_ylim(-30, 60)
        lines2.set_data(freq[0:n//2], spec_log[0:n//2])
        lines3.set_data(freq[0:n//2], spec_env[0:n//2])

        return lines1, lines2, lines3

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

def cepstrum_analyzer2():
    n = 1024
    fs = 48000 # sampling frequency [Hz]
    ceps_dim = 20 # cepstrum dimension

    p = pyaudio.PyAudio()
    stream = p.open(
        format = pyaudio.paInt16, # 16bit
        channels = 1, # monaural
        rate = fs,
        input = True,
        input_device_index = 0,
        frames_per_buffer = n
    )

    hamming_window = np.hamming(n)
    quef = np.array(list(range(n)))
    freq = np.fft.fftfreq(n, 1 / fs)

    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)
    lines1, = ax1.plot([], [])
    lines2, = ax2.plot([], [])
    lines3, = ax2.plot([], [], color = 'red')

    def update(i):
        ampl = np.frombuffer(stream.read(n), dtype = "int16") * hamming_window
        spec_log = 20 * np.log10(abs(np.fft.fft(ampl)) / n * 2)
        ceps = np.real(np.fft.ifft(spec_log))

        ax1.set_xlim(0, n//2)
        ax1.set_ylim(-10, 10)
        lines1.set_data(quef[0:n//2], ceps[0:n//2])

        ceps_env = np.array(ceps)
        ceps_env[ceps_dim:n-ceps_dim+1] = 0
        spec_env = np.real(np.fft.fft(ceps_env))

        ax2.set_xlim(0, 5000)
        ax2.set_ylim(-30, 60)
        lines2.set_data(freq[0:n//2], spec_log[0:n//2])
        lines3.set_data(freq[0:n//2], spec_env[0:n//2])

        return lines1, lines2, lines3

    ani = animation.FuncAnimation(
        fig,
        update,
        interval = 0,
        blit = True
    )
    plt.show()
    plt.close()

    stream.close()
    p.terminate()

cepstrum_analyzer1(".\sample.wav")
cepstrum_analyzer2()