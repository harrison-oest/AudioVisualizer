import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import struct
import os
from scipy.fftpack import fft
from tkinter import TclError
import time
from apa102_pi.driver import apa102
from colour import Color

strip = apa102.APA102(num_led=240, order='rgb')
strip.clear_strip()

CHUNK = 1024                                                        #size of each audio packet
FORMAT = pyaudio.paInt16                                            #bit size of audio packet input
CHANNELS = 1                                                        #mono channel microphone
RATE = 44100                                                        #44.1 kHz recording freq
INDEX = 2


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

#THE 'DO STUFF' PART OF THE CODE
while True:
                                                                    #Gather data and unpack into integers
    data = stream.read(CHUNK, exception_on_overflow = False)
    Idata=struct.unpack_from(str(CHUNK) + 'BH', data, offset=1)
        
                                                                #place into array and offset accordingly for smooth sound wave
    Ndata = np.array(Idata, dtype='b')[::2] + 128                                   #set y data for audio waveform
        
    #do the FFT magic
    FFTy = fft(Ndata)
    savedata = np.abs(FFTy[0:CHUNK] * 4 / (256 * CHUNK))
    
    #Binned Data
    newdata = savedata[1:]           #Create new data set, remove 1st value since 0-11Hz frequency gets unneccesarily
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
        newdata[455:500],                       #14: 5k - 10k
        newdata[501:2000]                       #15: 10k - 20k
    ]
    
    #get max 3 values and sum
    y_data = []                                                             #Binned Data Array

    #Get largest values from the bins, looping is just easier here since we are doing so much to the data
    for i in range(len(bins)):
        curBin = bins[i]
        binData = curBin[np.argsort(curBin)[-3:]]                           #Get highest 3 values
        binData = binData**(1/2) * 54                                           #Log scaling 
        y_data.append(np.sum(binData))                                      #Add 3 largest values to the 
        
    multiplier = 0.6
    mid_multiplier = 0.8
    brightness = 10
    for i in range(0,240):
        strip.set_pixel_rgb(i, 0x000000)
    strip.show()
    
    colors = [0xFF0000, 0x00FF00, 0x0000FF]
        
    for val in range(1,len(y_data)+1):
        if val == 1:
            led_size = int(y_data[val-1] * multiplier)
            for led in range(0,led_size):
                if led >= 0 and led < 5:
                    strip.set_pixel_rgb(led, colors[2], brightness)
                elif led >= 5 and led < 10:
                    strip.set_pixel_rgb(led, colors[1], brightness)
                elif led >= 10:
                    strip.set_pixel_rgb(led, colors[0], brightness)   
        elif val == 2:
            led_size = int(y_data[val-1] * multiplier)
            for led in range(15,led_size+15):
                if led >= 15 and led < 20:
                    strip.set_pixel_rgb(led, colors[2], brightness)
                elif led >= 20 and led < 25:
                    strip.set_pixel_rgb(led, colors[1], brightness)
                elif led >= 25:
                    strip.set_pixel_rgb(led, colors[0], brightness)
        elif val == 3:
            led_size = int(y_data[val-1] * multiplier)
            for led in range(30,led_size+30):
                if led >= 30 and led < 35:
                    strip.set_pixel_rgb(led, colors[2], brightness)
                elif led >= 35 and led < 40:
                    strip.set_pixel_rgb(led, colors[1], brightness)
                elif led >= 40:
                    strip.set_pixel_rgb(led, colors[0], brightness)            
        elif val == 4:
            led_size = int(y_data[val-1] * multiplier)
            for led in range(45,led_size+45):
                if led >= 45 and led < 50:
                    strip.set_pixel_rgb(led, colors[2], brightness)
                elif led >= 50 and led < 55:
                    strip.set_pixel_rgb(led, colors[1], brightness)
                elif led >= 55:
                    strip.set_pixel_rgb(led, colors[0], brightness)
        elif val == 5:
            led_size = int(y_data[val-1] * multiplier)
            for led in range(60,led_size+60):
                if led >= 60 and led < 65:
                    strip.set_pixel_rgb(led, colors[2], brightness)
                elif led >= 65 and led < 70:
                    strip.set_pixel_rgb(led, colors[1], brightness)
                elif led >= 70:
                    strip.set_pixel_rgb(led, colors[0], brightness)
        elif val == 6:
            led_size = int(y_data[val-1] * mid_multiplier)
            for led in range(75,led_size+75):
                if led >= 75 and led < 80:
                    strip.set_pixel_rgb(led, colors[2], brightness)
                elif led >= 80 and led < 85:
                    strip.set_pixel_rgb(led, colors[1], brightness)
                elif led >= 85:
                    strip.set_pixel_rgb(led, colors[0], brightness)
        elif val == 7:
            led_size = int(y_data[val-1] * mid_multiplier)
            for led in range(90,led_size+90):
                if led >= 90 and led < 95:
                    strip.set_pixel_rgb(led, colors[2], brightness)
                elif led >= 95 and led < 100:
                    strip.set_pixel_rgb(led, colors[1], brightness)
                elif led >= 100:
                    strip.set_pixel_rgb(led, colors[0], brightness)
        elif val == 8:
            led_size = int(y_data[val-1] * mid_multiplier)
            for led in range(105,led_size+105):
                if led >= 105 and led < 110:
                    strip.set_pixel_rgb(led, colors[2], brightness)
                elif led >= 110 and led < 115:
                    strip.set_pixel_rgb(led, colors[1], brightness)
                elif led >= 115:
                    strip.set_pixel_rgb(led, colors[0], brightness)
        elif val == 9:
            led_size = int(y_data[val-1] * mid_multiplier)
            for led in range(120,led_size+120):
                if led >= 120 and led < 125:
                    strip.set_pixel_rgb(led, colors[2], brightness)
                elif led >= 125 and led < 130:
                    strip.set_pixel_rgb(led, colors[1], brightness)
                elif led >= 130:
                    strip.set_pixel_rgb(led, colors[0], brightness)           
        elif val == 10:
            led_size = int(y_data[val-1] * mid_multiplier)
            for led in range(135,led_size+135):
                if led >= 135 and led < 140:
                    strip.set_pixel_rgb(led, colors[2], brightness)
                elif led >= 140 and led < 145:
                    strip.set_pixel_rgb(led, colors[1], brightness)
                elif led >= 145:
                    strip.set_pixel_rgb(led, colors[0], brightness)
        elif val == 11:
            led_size = int(y_data[val-1] * mid_multiplier)
            for led in range(150,led_size+150):
                if led >= 150 and led < 155:
                    strip.set_pixel_rgb(led, colors[2], brightness)
                elif led >= 155 and led < 160:
                    strip.set_pixel_rgb(led, colors[1], brightness)
                elif led >= 160:
                    strip.set_pixel_rgb(led, colors[0], brightness)
        elif val == 12:
            led_size = int(y_data[val-1] * mid_multiplier)
            for led in range(165,led_size+165):
                if led >= 165 and led < 170:
                    strip.set_pixel_rgb(led, colors[2], brightness)
                elif led >= 170 and led < 175:
                    strip.set_pixel_rgb(led, colors[1], brightness)
                elif led >= 175:
                    strip.set_pixel_rgb(led, colors[0], brightness)
        elif val == 13:
            led_size = int(y_data[val-1] * mid_multiplier)
            for led in range(180,led_size+180):
                if led >= 180 and led < 185:
                    strip.set_pixel_rgb(led, colors[2], brightness)
                elif led >= 185 and led < 190:
                    strip.set_pixel_rgb(led, colors[1], brightness)
                elif led >= 190:
                    strip.set_pixel_rgb(led, colors[0], brightness)
        elif val == 14:
            led_size = int(y_data[val-1] * mid_multiplier)
            for led in range(195,led_size+195):
                if led >= 195 and led < 200:
                    strip.set_pixel_rgb(led, colors[2], brightness)
                elif led >= 200 and led < 205:
                    strip.set_pixel_rgb(led, colors[1], brightness)
                elif led >= 205:
                    strip.set_pixel_rgb(led, colors[0], brightness)
        elif val == 15:
            led_size = int(y_data[val-1] * multiplier)
            for led in range(210,led_size+210):
                if led >= 210 and led < 215:
                    strip.set_pixel_rgb(led, colors[2], brightness)
                elif led >= 215 and led < 220:
                    strip.set_pixel_rgb(led, colors[1], brightness)
                elif led >= 220:
                    strip.set_pixel_rgb(led, colors[0], brightness)
        elif val == 16:
            led_size = int(y_data[val-1] * multiplier)
            for led in range(225,led_size+225):
                if led >= 225 and led < 230:
                    strip.set_pixel_rgb(led, colors[2], brightness)
                elif led >= 230 and led < 235:
                    strip.set_pixel_rgb(led, colors[1], brightness)
                elif led >= 235:
                    strip.set_pixel_rgb(led, colors[0], brightness)         
        
    strip.show()
    count += 1





