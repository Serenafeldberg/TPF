

import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
from note import Note
import functions
from typing import List

class Instrument ():
    def __init__ (self, file, frecuency):
        self.file = file
        self.note = Note('debussy-clair-de-lune.txt')
        self.frecuency = frecuency
        self.duration = self.note.get_duration()
        self.instrument = self.read_file()

    def get_instrument (self):
        pass

    def read_file (self):
        all = []
        with open (self.file, 'r') as fn:
            lines = fn.readlines()
            for line in lines:
                line = line.strip("\n")
                new_lines = line.split()
                new = []
                for elem in new_lines:
                    try:
                        elem = float(elem)
                        if elem == int(elem):
                            elem = int(elem)
                    except:
                        ValueError
                    new.append(elem)
                if len(new) != 0:
                    all.append(new)
        return all

    def all_fn (self, function, t, t0=1, t1=1, a1=1, a=1, f=1):
        '''
        It is a dictionary with all the posible functions, and their corresponding formula
        '''
        fn = {'CONSTANT': functions.constant(t), 'LINEAR':  functions.linear(t, t0), 'INVLINEAR': functions.invlinear(t, t0), 'SIN': functions.sin(t, a, f)
        , 'EXP': functions.exp(t, t0), 'INVEXP': functions.invexp(t, t0), "QUARTCOS": functions.quartcos(t, t0)
        , "QUARTSIN": functions.quartsin(t, t0), 'HALFCOS': functions.halfcos(t, t0), 'HALFSIN': functions.halfsin(t, t0)
        , 'LOG': functions.log(t, t0), 'INVLOG': functions.invlog(t, t0), 'TRI': functions.tri(t, t0, t1, a1), 'PULSES': functions.pulses(t, t0, t1, a1)}
        return fn[function]

    def get_params (self, a_list: List, t):
        '''
        Depending on the amount of elements in the list, and on the parameters, it will return a float valued in a function
        
        '''
        len_list = len(a_list)
        if len_list == 4:
            fn = a_list[0]
            first_param = a_list[1]
            second_param = a_list[2]
            third_param = a_list[3]
            function = self.all_fn(fn, t0 = first_param, t1 = second_param, a1 = third_param, t = t)
        if len_list == 3:
            fn = a_list[0]
            first_param = a_list[1]
            second_param = a_list[2]
            function = self.all_fn(fn, a = first_param, f = second_param, t = t)
        if len_list == 2:
            fn = a_list[0]
            first_param = a_list[1]
            function = self.all_fn(fn, t0 = first_param, t = t)
        if len_list == 1:
            fn = a_list[0]
            function = self.all_fn(fn, t = t)

        return function

    def attack (self, t):
        list_attack = self.instrument[-3]
        attack = self.get_params(list_attack, t)
        seconds = list_attack[1]

        return attack, seconds

    def decay (self, t):
        list_decay = self.instrument[-1]
        decay = self.get_params(list_decay, t)
        seconds = list_decay[1]

        return decay, seconds

    def sustained (self, t):
        list_sustained = self.instrument[-2]
        sustained = self.get_params(list_sustained, t)

        return sustained


    def gen_mod (self, t, y, duration_n):
        '''
        Modulariza la nota con ataque, sostenido, decaimiento

        PARAMS
        -> t: array del tiempo
        -> y: array de la nota
        -> duration_n: duracion de la nota
        
        '''
        
        #attack
        data_a, duration_a = self.attack(t)
        y [t < duration_a] *= data_a [t < duration_a]

        #decay
        data_d, duration_d = self.decay(t)
        seconds_d = duration_n - duration_d
        y [t >= seconds_d] *= data_d [t >= seconds_d]

        #sustained
        data_s = self.sustained(t)
        y [(t >= duration_a) & (t < seconds_d)] *= data_s [(t >= duration_a) & (t < seconds_d)]

        return y 

    def gen_tone(self, frec, end , tstart = 0):
        '''
        devuelva una señal que sea la suma de armónicos para una dada
        frecuencia fundamental

        PARAMS:
        -> freq: frecuency of the note
        -> end: time of end
        -> tstart: time of start
        '''
        ins = self.read_file()
        t = np.arange(tstart, end, 1/self.frecuency) 
        yy = 0
        harmonics = ins[0][0]
        if harmonics > 0:
            for i in range (1, harmonics+1):
                multiplies = ins[i][0]
                a = ins[i][1]
                y = a * np.sin(2 * np.pi * multiplies * frec * t)
                yy += y
        
        array_mod = self.gen_mod(t, yy, (end - tstart))
        plt.plot(t, array_mod)
        plt.show()
        return array_mod

    def partes (self):
        '''
        Genera un array vacio y dependiendo de la duracion de la nota, y el tiempo en el que
        debe sonar, se lo agrega al array

        PARAMS
        -> frecuency: frecuencia de muestreo
        -> duration: Total duration of the partiture

        returns an array with the sinthetisized notes.
        
        '''
        zero = np.arange(self.frecuency * self.duration, dtype= float)
        notes = self.note.read_file()
        for val in notes.keys():
            start = notes[val][0]
            duration_note = notes[val][2]
            end = start + duration_note
            frec = notes[val][1]
            y = self.gen_tone(frec, end, start)
            
            if zero[int(start*self.frecuency):int(end*self.frecuency)].shape == y.shape:
                zero[int(start*self.frecuency):int(end*self.frecuency)] += y
            zero [zero > 1] = 1
            zero [zero < -1] = -1
    
        return zero 

    #codigo de ernesto
    def tone (self, frec, d):
        t = np.arange(0.5 * frec)
        waveform = 1 * np.sin(2 * np.pi * 440 * t / frec)
        waveform1 = 0.8 * np.sin(2 * np.pi * 880 * t / frec)
        waveform2 = 0.1 * np.sin(2 * np.pi * 1320 * t / frec)
       
        a = np.zeros(int(frec * d))
        a[0:int(frec*0.5)] += waveform
        a[int(frec*0.5): int(frec*1)] += waveform1

        a[int(frec*1) : int(frec*1.5)] += waveform
        a[int(frec*1) : int(frec*1.5)] += waveform1
        a[int(frec*1) : int(frec*1.5)] += waveform2
        a[int(frec*1) : int(frec*1.5)] /= 3

        return a
        size = a.size
        x = np.arange(0, d, (d/size))
        plt.plot(x, a)
        plt.show()

ins = Instrument('piano.txt', 44100)
ins.gen_tone(440, 0.18)
#y = ins.partes()

#write ('audio.wav', 44100, y)
