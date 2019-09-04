#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 16:35:34 2019

@author: agostina
"""

import re
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
import numpy as np

class VsmData():  
    # Clase abarcativa de medidas y tareas abdicadas a datos del VSM.
    def __init__(self):
        self.datapoints = 0
        self.field = []
        self.moment = []
        self.offset = 0
        self.saturationmag = 0
        self.width = 0
        self.height = 0

    def testfunc(self):
        print('VSM module OK!')

    def loadFile(self, fileinp):
        
        pattern1 = re.compile("DataPoints")
        pattern2 = re.compile("[Mm]omentX [Dd]ata")
        pattern3 = re.compile("[Ff]ield [Dd]ata")
        str5 = 'DataPoints '
        index_p2 = 0
        index_p3 = 0
        try:
            f = open(fileinp).read().splitlines()
        except IOError:
            print("ERROR! Cannot find %s in current directory." % (fileinp))
            raise
        
        # Setteamos índices a partir de los cuales vamos a guardar los datos.
        for index, item in enumerate(f):
            if pattern1.search(item) != None:
               self.datapoints = int(item.replace(str5,''))
            if pattern2.search(item) != None:
               index_p2 = index + 1
            if pattern3.search(item) != None:
               index_p3 = index + 1
        # Appendeamos los puntos.
        for x in range(0, self.datapoints):
            self.moment.append(float(f[x + index_p2]))
            self.field.append(float(f[x + index_p3]))
    
    def momentOffset(self):
        # Corregimos un offset en momentos que puede haberse producido durante
        # mediciones.
        self.offset = (max(self.moment) + min(self.moment)) / 2
        print('Offset is: %f' % self.offset)
        for i in range(0, self.datapoints):
            self.moment[i] = self.moment[i] - self.offset
    
    # No estoy muy segura de esto todavía. No lo usaría. Es para tener el resultado
    # en superficie.

    
    def sampleMeasure(self, xlength, ylength):
       #xlength = float(input('Sample width(in cms)? '))
       #ylength = float(input('Sample length(in cms)? '))
       area = xlength * ylength
       for i in range(0, self.datapoints):
           self.moment[i] = self.moment[i] / area
    

    def saturationMag(self):
        self.saturationmag = max(self.moment)
        
    
    def save_vsm(self, outfile):
        # Escribimos el archivo.
        outfile += '.dat'
        fout = open(outfile, "w+")
        for x in range(0, self.datapoints):
            fout.write("%f %f\n" % (self.field[x], self.moment[x]))                                
        fout.close()  
        print('Done! :) File output: %s' % outfile)
    
    def coerField(self, points=3):

        a = np.argmin(np.absolute(self.moment))
        #polygrd = input("")
        mompoly = np.zeros(2*points)
        fieldpoly = np.zeros(2*points)
        
        for i in range(0, 2*points):
            if self.field[a] < 0:   
               mompoly[i] = self.moment[a-i+3]
               fieldpoly[i] = self.field[a-i+3]
            else:
                mompoly[i] = self.moment[a+i-3]
                fieldpoly[i] = self.field[a+i-3]
        
        spline = UnivariateSpline(fieldpoly, mompoly)
        hc = abs(spline.roots())
        print("Hc calculado en: %f G." % (hc) )
        newfield = spline(fieldpoly)
        return fieldpoly, newfield, hc
