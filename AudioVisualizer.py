#!/usr/bin/env python
# coding: utf-8

# In[2]:


#import libs
import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import struct
import os
from scipy.fftpack import fft
from tkinter import TclError
import time
from apa102_pi.driver import apa102

strip = apa102.APA102(num_led=240, order='rgb')
strip.clear_strip()


# get_ipython().run_line_magic('matplotlib', 'tk')
                                                                    #opens up new window for live graphing

CHUNK = 8192                                                        #size of each audio packet
FORMAT = pyaudio.paInt16                                            #bit size of audio packet input
CHANNELS = 2                                                        #mono channel microphone
RATE = 44100                                                        #44.1 kHz recording freq
INDEX = 2


# In[3]:


#INITIALIZE PYAUDIO STREAM
PAud = pyaudio.PyAudio()
stream = PAud.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input_device_index = INDEX,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
    )

#SET UP PLOTS
fig, (ax, ay, az) = plt.subplots(3, figsize=(12,8))
                                                                #ax = Waveform
                                                                #ay = Fourier Composite
                                                                #az = Binned Values from ay

#X-Axes
Audx = np.arange(0, 2*CHUNK, 2)
FFTx = np.linspace(0, RATE, CHUNK)
Barx = np.arange(16)

#Line objs
Audline, = ax.plot(Audx, np.random.rand(CHUNK), '-')
FFTline, = ay.semilogx(FFTx, np.random.rand(CHUNK), '-')
Barline, = az.plot(Barx, [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], '-')
                                                                #All Y-data in above lines gets changed, just a placeholder

#make the plot look nice
fig.tight_layout(pad=3)                                         #Space out graphs
ax.set_title('Recorded Audio')
ax.set_ylabel('Magnitude')
ay.set_title('Frequency Transform')
az.set_title('Frequency Bin Amplitude')
ax.set_ylim(0,255)
ax.set_xlim(0,2*CHUNK)
plt.setp(ax, xticks=[0, CHUNK, 2*CHUNK], yticks=[0,128,255])
ay.set_xlim(20, RATE/2)
az.set_ylim(0,1)
az.set_xlim(0,15)


#THE 'DO STUFF' PART OF THE CODE
while True:
                                                                #Gather data and unpack into integers
    data = stream.read(CHUNK, exception_on_overflow = False)
    Idata=struct.unpack_from(str(CHUNK) + 'BH', data, offset=1)
        
                                                                #place into array and offset accordingly for smooth sound wave
    Ndata = np.array(Idata, dtype='b')[::2] + 128
    Audline.set_ydata(Ndata)                                    #set y data for audio waveform
        
    #do the FFT magic
    FFTy = fft(Ndata)
    savedata = np.abs(FFTy[0:CHUNK] * 4 / (256 * CHUNK))
    FFTline.set_ydata(savedata)                                 #set y data for FFT composite
    
    #Binned Data
    newdata = FFTline.get_ydata()[1:]           #Create new data set, remove 1st value since 0-11Hz frequency gets unneccesarily
                                                #amplified from white noise and uneven signals
    #create bins
    bins = [
        newdata[0:4],                           #0: 0-44
        newdata[5:11],                          #1: 44-121
        newdata[12:18],                         #2: 121-198
        newdata[19:26],                         #3: 198-286
        newdata[27:34],                         #4: 286-374
        newdata[35:44],                         #5: 374-484
        newdata[45:58],                         #6: 484-638
        newdata[59:70],                         #7: 638-770
        newdata[71:95],                         #8: 770-1.05k
        newdata[96:115],                        #9: 1.05k-1.27k
        newdata[116:180],                       #10: 1.27k-2k
        newdata[181:240],                       #11: 2k-2.6k
        newdata[241:340],                       #12: 2.6k-3.8k
        newdata[341:454],                       #13: 3.8k-5k
        newdata[455:910],                       #14: 5k - 10k
        newdata[911:2000]                       #15: 10k - 20k
    ]
    
    #get max 3 values and sum
    y_data = []                                                             #Binned Data Array

    #Get largest values from the bins, looping is just easier here since we are doing so much to the data
    for i in range(len(bins)):
        curBin = bins[i]
        binData = curBin[np.argsort(curBin)[-3:]]                           #Get highest 3 values
        binData = binData**(1/2) * 54                                           #Log scaling 
        y_data.append(np.sum(binData))                                      #Add 3 largest values to the 
        
    Barline.set_ydata(y_data)                                               #set y data for bins
    
    multiplier = 0.6
    strip.clear_strip()
    
    for val in range(1,len(y_data)+1):
        if val == 1:
            led_size = int(y_data[val-1] * multiplier)
            for led in range(0,led_size):
                strip.set_pixel_rgb(led, 0xFF0000)
        elif val == 2:
            led_size = int(y_data[val-1] * multiplier)
            for led in range(15,led_size+15):
                strip.set_pixel_rgb(led, 0xFF0000)
        elif val == 3:
            led_size = int(y_data[val-1] * multiplier)
            for led in range(30,led_size+30):
                strip.set_pixel_rgb(led, 0xFF0000)            
        elif val == 4:
            led_size = int(y_data[val-1] * multiplier)
            for led in range(45,led_size+45):
                strip.set_pixel_rgb(led, 0xFF0000)
        elif val == 5:
            led_size = int(y_data[val-1] * multiplier)
            for led in range(60,led_size+60):
                strip.set_pixel_rgb(led, 0x00FF00)
        elif val == 6:
            led_size = int(y_data[val-1] * multiplier)
            for led in range(75,led_size+75):
                strip.set_pixel_rgb(led, 0x00FF00)
        elif val == 7:
            led_size = int(y_data[val-1] * multiplier)
            for led in range(90,led_size+90):
                strip.set_pixel_rgb(led, 0x00FF00)
        elif val == 8:
            led_size = int(y_data[val-1] * multiplier)
            for led in range(105,led_size+105):
                strip.set_pixel_rgb(led, 0x00FF00)
        elif val == 9:
            led_size = int(y_data[val-1] * multiplier)
            for led in range(120,led_size+120):
                strip.set_pixel_rgb(led, 0x0000FF)            
        elif val == 10:
            led_size = int(y_data[val-1] * multiplier)
            for led in range(135,led_size+135):
                strip.set_pixel_rgb(led, 0x0000FF)
        elif val == 11:
            led_size = int(y_data[val-1] * multiplier)
            for led in range(150,led_size+150):
                strip.set_pixel_rgb(led, 0x0000FF)
        elif val == 12:
            led_size = int(y_data[val-1] * multiplier)
            for led in range(165,led_size+165):
                strip.set_pixel_rgb(led, 0x0000FF)
        elif val == 13:
            led_size = int(y_data[val-1] * multiplier)
            for led in range(180,led_size+180):
                strip.set_pixel_rgb(led, 0xFFFFFF)
        elif val == 14:
            led_size = int(y_data[val-1] * multiplier)
            for led in range(195,led_size+195):
                strip.set_pixel_rgb(led, 0xFFFFFF)            
        elif val == 15:
            led_size = int(y_data[val-1] * multiplier)
            for led in range(210,led_size+210):
                strip.set_pixel_rgb(led, 0xFFFFFF)
        elif val == 16:
            led_size = int(y_data[val-1] * multiplier)
            for led in range(225,led_size+225):
                strip.set_pixel_rgb(led, 0xFFFFFF)           
        
    strip.show()





