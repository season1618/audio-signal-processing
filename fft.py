import math
import wave
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def FFT(N, T, ampl1):
    time = np.array(list(range(N))) * T
    #plt.plot(time, ampl1)
    #plt.xlabel('time[s]')
    #plt.ylabel('amplitude')
    #plt.show()

    ampl2 = abs(np.fft.fft(ampl1)) / N * 2
    freq = np.fft.fftfreq(N, T)
    #plt.plot(freq, ampl2)
    #plt.xlabel('freqency[Hz]')
    #plt.ylabel('amplitude')
    #plt.show()

    return (freq, ampl2)