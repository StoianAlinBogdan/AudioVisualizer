import pyaudio
import numpy as np
import struct
import matplotlib.pyplot as plt
from scipy.fftpack import fft


def determine_config():
    devices = [p.get_device_info_by_index(i) for i in range(p.get_device_count())]
    
    for i in range(len(devices)):
        print("{}: {}, input: {}, output: {}, sample: {}".format(
            devices[i]['index'], devices[i]['name'],
            devices[i]['maxInputChannels'], devices[i]['maxOutputChannels'],
            devices[i]['defaultSampleRate'])
        )

    id = int(input("Insert loopback interface for output device index: "))
    return {
        "format": pyaudio.paInt16,
        "channels": devices[id]['maxInputChannels'],
        "rate": int(devices[id]['defaultSampleRate']),
        "input": True,
        "output": False,
        "frames_per_buffer": int(devices[id]['defaultSampleRate']/20),
        "input_device_index": id
    }
    

def window_closed(event):
    try:
        raise Exception
    except Exception:
        print("Exiting gracefully!")
        exit()


if __name__ == "__main__":
    p = pyaudio.PyAudio()
    
    config = determine_config()
    stream = p.open(
        format=config['format'],
        channels=config['channels'],
        rate=config['rate'],
        input=config['input'],
        output=config['output'],
        frames_per_buffer=config['frames_per_buffer'],
        input_device_index=config['input_device_index']
    )
    
    fig, (ax, ax2) = plt.subplots(2)
    # plot some random thing that looks like the signal to setup the plot:
    x = np.arange(0, config['frames_per_buffer'] * config['channels'], 2)
    xf = np.linspace(0, config['rate'], config['frames_per_buffer'])
    line, = ax.plot(x, np.random.rand(config['frames_per_buffer']), '-', lw=2)
    line_fft, = ax2.plot(x, np.random.rand(config['frames_per_buffer']), '-', lw=2)
    
    ax.set_ylim(-1, 1)
    ax.set_xlim(0, config['frames_per_buffer'])
    ax2.set_xlim(0, config['frames_per_buffer']/2)
    plt.ion()
    fig.canvas.mpl_connect('close_event', window_closed)

    while True:
        try:
            raw_data = stream.read(config['frames_per_buffer'])
            signal_array = np.array(struct.unpack(str(config['frames_per_buffer'] * config['channels']) + 'h', raw_data))
            signal_array = signal_array[0::2] # left channel only
            signal_array_norm = signal_array / abs(np.max(signal_array))
            #signal_array_norm = signal_array_norm[0::2] # left channel only
            line.set_ydata(signal_array_norm)
            
            fft_data = fft(signal_array_norm)
            fft_data_norm = np.abs(fft_data / np.max(fft_data)) # this is logarithmic - see https://stackoverflow.com/questions/25735153/plotting-a-fast-fourier-transform-in-python
            line_fft.set_ydata(fft_data_norm)
            
            
            plt.show(block=False)
            plt.pause(0.001)
            

        except KeyboardInterrupt:
            print("Exiting gracefully!")
            break     
     