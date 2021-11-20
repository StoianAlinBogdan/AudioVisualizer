import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft

CHUNK = 2400
#CHUNK = 800
FORMAT = pyaudio.paInt16
CHANNELS = 2 # tine minte asta
RATE = 48000

p = pyaudio.PyAudio()

stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=False,
    frames_per_buffer=CHUNK,
    input_device_index=12
)

fig, (ax, ax2) = plt.subplots(2)
x = np.arange(0, 2 * CHUNK * CHANNELS, 2)
xf = np.linspace(0, RATE, CHUNK * CHANNELS)
line, = ax.plot(x, np.random.rand(CHUNK * CHANNELS), '-', lw=2)
line_fft, = ax2.semilogx(xf, np.random.rand(CHUNK * CHANNELS), '.', lw=2)
ax.set_ylim(-256, 256)
ax.set_xlim(0, CHUNK * 2 * CHANNELS)

ax2.set_xlim(20, RATE/4)

while True:
    plt.ion()
    plt.show()
    data = stream.read(CHUNK)
    data_int = np.array(struct.unpack(str(CHUNK * CHANNELS) + 'h', data))/ 128 # / 128 based on system volumme......
    line.set_ydata(data_int)
    
    yf = fft(data_int*2)
    yf = yf / max(yf)
    #line_fft.set_ydata(np.abs(yf[0:CHUNK*CHANNELS]) / (128 * CHUNK * CHANNELS))
    line_fft.set_ydata(np.abs(yf))
    
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.001)