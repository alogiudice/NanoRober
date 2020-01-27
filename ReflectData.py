import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
from scipy import stats
import statsmodels.api as sm
from math import pow
from scipy.interpolate import UnivariateSpline
import re

auto_optim = True

class Reflect():
    
    def __init__(self, lambdax = 1.5406):
        # Defino los patrones a buscar en el archivo p/ encontrar los theta 
        # y counts.
        self.counts = []
        self.x = []
        self.lambdax = lambdax
        self.maxcounts = 0
        self.maxcounts_i = 0
        self.thetacritic1 = 0
        self.thetacritic2 = 0
        self.thetastart_i = None
        self.thetaend_i = None
        self.thetarangestart = None
        self.thetarangeend = None
        self.x_cutoff = None
        self.peaks_index_zero = None
        
    def testReflect(self):
        print('XRR Module loaded!')
        
    def loadFile(self, file):
        pattern1 = re.compile("[Cc]ounts\"\>")
        pattern2 = re.compile("axis\=\"2Theta\" unit\=\"deg\"")
        pattern3 = re.compile("[Ss]tartPosition\>")
        pattern4 = re.compile("[Ee]ndPosition\>")
        pattern5 = re.compile("\<\/intensities")
        pattern6 = re.compile("[dD]ata[Pp]oints")
        
        try:
            f = open(file).read()
        except IOError:
            print("Cannot open file %s" % file)
            raise
        
        # Start of search
        start_match = pattern6.search(f)
        
        f = f[start_match.end():]
        
        try:
            pattern2.search(f) is not None
        except NameError:
            print("ERROR! Cannot find theta coordinates for file.")
            raise
        
        match_start1 = pattern3.search(f)
        # Theta values always use 4 digits.
        thetastart = float(f[match_start1.end():match_start1.end()+6])
        aux_index = match_start1.end() + 6
        match_start2 = pattern4.search(f[aux_index:])
        
        thetaend = float(f[aux_index + match_start2.end():aux_index + 
                           match_start2.end() + 6])
        
        # Getting the counts list.
        match = pattern1.search(f)
        # index1 = start point of counts measurements.
        index1 = int(match.end() + 1)
        match_end = pattern5.search(f[index1:])
        index2 = int(match_end.start())
        counts = f[index1:index1+index2].split()
        # Generate counts list.
        self.counts = list(map(float, counts)) 
        # Generate 2theta list
        self.x = np.linspace(thetastart, thetaend, len(counts))
        self.thetastart_i = 0
        self.thetaend_i = len(self.x)
        
    def thetacrit(self, maxindex_crop = 1.6):
        # Esta función devuelve el valor del ángulo crítico del sistema, tenien
        # -do en cuenta a éste calculado como el ángulo en el que I = Imax / 2.
        
        max_value = max(self.counts)
        max_index = self.counts.index(max_value)
        thetacrit_value = max_value / 2        
        # Buscamos el valor más cercano al del I/2 y le asignamos el valor de 
        # theta crítico.
        
        maxindex_scan = int(max_index * maxindex_crop)
        # Croppeamos el array hasta este valor.
        
        scan = self.counts[max_index + 1:maxindex_scan]
        scan = [abs(value - thetacrit_value) for value in scan]
        mini = np.argmin(scan)
        thetacritic = self.x[max_index + 1 + mini]
        
        return thetacritic
    
    def thetacritSpline(self, maxindex_crop=1.6):
        #Esta función saca el theta crítico ajustando la curva con una spline, 
        # y sacando su cero. Es más precisa que la antigua thetacrit.
        self.maxcounts = max(self.counts)
        self.maxcounts_i = self.counts.index(self.maxcounts)

        thetacrit_value = self.maxcounts / 2        
        
        maxindex_scan = int(self.maxcounts_i * maxindex_crop)
        
        fieldpoly = self.x[self.maxcounts_i + 1:maxindex_scan]
        scan = self.counts[self.maxcounts_i + 1:maxindex_scan]
        scan = [(value - thetacrit_value) for value in scan]   
        spline = UnivariateSpline(fieldpoly, scan)
        thetacritic = spline.roots()
        self.thetacritic1 = thetacritic[0]
              
    
    def smoothcounts(self, fig, fraclowess, x_cutoffindex):
        # Esta función grafica los datos sin smoothear, los ya smootheados por 
        # lowess, y a los picos encontrados. Devuelve el array peaks_index, en 
        # que están especificadas las posiciones de los picos en el rango 
        # [max_index:x_cutoff]
        
        # La idea es ver ahora cómo obtener los máx y mín de la curva. Es un p_
        # roceso que parece complicado, porque vamos a tener que smoothear la 
        # función. Probé con savgol y no dio muy bien para el tipo de señal que
        #tenemos. También habría que poner hasta qué pico queremos smoothear.
        max_value = max(self.counts)
        max_index = self.counts.index(max_value)
        self.x_cutoff = self.x.index(x_cutoffindex)
    
        # Croppeamos los arrays para realizar los ajustes en este rango.
        if self.x_cutoff is None:
            xx = self.x[max_index:self.thetaend_i]
            yy = self.counts[max_index:self.thetaend_i]
        else:
            xx = self.x[max_index:self.x_cutoff]
            yy = self.counts[max_index:self.x_cutoff]
            
        
        lowess = sm.nonparametric.lowess(yy, xx, frac=fraclowess)
        
        peaks_index = argrelextrema(lowess[:,1], np.greater)
        peaks_index_zero = [max_index + y for y in peaks_index[0]]
        print("Found %d local maxima." % len(peaks_index[0]) )
        
        peak_list = []
        xpeaks = []
        
        for peak in peaks_index[0]:
            peak_list.append(lowess[peak, 1])
            xpeaks.append(xx[peak])

        # Ahora, se debería modificar el gráfico a partir de esa
        # función, pero el plot no es un atributo de esta clase,
        # así que devolveremos los valores y que FormWidget se
        # encargue de graficar.
            
        #fig.clear()
        #ax = fig.add_subplot(111)
        #ax.set_ylabel('counts')
        #ax.set_xlabel('2theta[deg]')
        #ax.grid()
        
        #ax.plot(xx, yy, color='orange', label='data')
        
       # ax.plot(xx, lowess[:,1], color='blue', linestyle='--', label='smooth')
        #ax.plot(xpeaks, peak_list, 'ro', label='found maxima')
       # ax.set_yscale('log')
       # plt.legend(loc='upper right')
            
        #fig.canvas.draw()
        #fig_smooth.canvas.flush_events()
        
        return peaks_index_zero, lowess, xpeaks, peak_list

    def smoothcounts_wg(self, indexinit, indexend, cutoff, fraclowess):
        # En esta función tenemos en cuenta que ya se especificó anteriormente
        # el intervalo a tener en cuenta mediante un thetastary y un thetaend.
        # Por las dudas, se pide un cutoff por si se quiere cortar la curva
        # anteriormente, pero no es necesario.
        idx = np.searchsorted(self.x, cutoff, side="left")
        xx = self.x[indexinit:idx]
        yy = self.counts[indexinit:idx]
        self.x_cutoff = idx
        
        lowess = sm.nonparametric.lowess(yy, xx, frac=fraclowess)
        
        peaks_index = argrelextrema(lowess[:,1], np.greater)
        self.peaks_index_zero = [indexinit + y for y in peaks_index[0]]
        print("Found %d local maxima." % len(peaks_index[0]) )
        
        peak_list = []
        xpeaks = []
        
        for peak in peaks_index[0]:
            peak_list.append(lowess[peak, 1])
            xpeaks.append(xx[peak])

        return lowess, xpeaks, peak_list


    def get_slope(self, n_limit = 12):
        
        # Esta función obtiene los parámetros del ajuste lineal del sin**2 de los 
        # picos con los valores de n. Toma un array c con las posiciones en 2theta
        # (en deg) de los picos y el valor n inicial para generar la sucesión de 
        # de etiquetas. AJusta automáticamente segun se adquiera el mejor valor
        # de difs entre theta crítico de I y el del ajuste.
        n = 1
        angpeaks = [0] * len(self.peaks_index_zero)
        angpeaks = [np.sin(pow(self.x[peak] * (np.pi / 360), 2)) for peak in 
                    self.peaks_index_zero]
        
        # Para cada n distinto
        npeaks = np.arange(n, n + len(self.peaks_index_zero), 1)
        npeaks = [pow(nn * self.lambdax / 2, 2) for nn in npeaks]
        
        
        slope1, intercept1, r_value1, p_value1, std_err1 = stats.linregress(
                npeaks, angpeaks)
        
        thetacrit_int = self.thetacrit()
        thetacrit_exp1 = pow(intercept1, 1/2) * (360 / np.pi)
        thetacrit_diff1 = ( (thetacrit_exp1 - thetacrit_int) / thetacrit_int ) * 100
        
        while n < n_limit:
            n += 1/2
            npeaks = np.arange(n, n + len(self.peaks_index_zero), 1)
            npeaks = [pow(nn * self.lambdax / 2, 2) for nn in npeaks]
            slope, intercept, r_value, p_value, std_err = stats.linregress(npeaks, 
                                                                       angpeaks)
            
            thetacrit_exp = pow(intercept, 1/2) * (360 / np.pi)
            thetacrit_diff = ((thetacrit_exp - thetacrit_int) / thetacrit_int ) * 100
            #print(thetacrit_exp)
            #print(r_value)

            if r_value > r_value1 and abs(thetacrit_diff1) > abs(thetacrit_diff):
                slope1 = slope
                intercept1 = intercept
                r_value1 = r_value
                thetacrit_diff1 = thetacrit_diff
            else:
                break
        
        #fittedline = [m * slope + intercept for m in npeaks]
        #line3, = ax2.plot(npeaks, angpeaks, 'o')
        #line4, = ax2.plot(npeaks, fittedline, color='green')
    
        print('Final n: %i' % n)
        print('Fitting results for data:')
        print("slope: %e,\nIntercept: %e,\nR-squared: %f" % (slope1, intercept1, 
                                                             r_value1))
        
        print('2theta_crit value obtained is %f . Value obtained from counts'
              ' was %f' % (thetacrit_exp1, thetacrit_int) )
        
        print("Percentage difference between both critical angles is %f. " 
              % thetacrit_diff1)
        
        return n, slope1, intercept1, r_value1, thetacrit_exp1, thetacrit_diff1
    
    def save_reflect(self, filename):
        with open(filename, 'w') as file:
            for index, item in enumerate(self.counts):
                file.write("%f %f\n" % (x[index], item))
            

