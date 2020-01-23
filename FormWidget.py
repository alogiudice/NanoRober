#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 15:49:40 2019

@author: agostina
"""

import os
from PyQt5.QtCore import QSize, Qt, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap, QIcon, QDoubleValidator
import PyQt5.QtWidgets as Wid
import numpy as np
import VsmData as vsm
import ReflectData as reflect
import PyPlotCanvas as canvas

class Communicate(QObject):
    x = pyqtSignal()

class FormWidget(Wid.QWidget):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.vsminfo = vsm.VsmData()
        self.xrronvalue = Communicate()
        self.refldat = reflect.Reflect()
        
        self.layout = Wid.QVBoxLayout(self)
        
        infoWidget = Wid.QWidget()
        infolayout = Wid.QGridLayout()
        samplename = Wid.QLineEdit()
        samplelabel = Wid.QLabel('Sample Name:')
        samplelabel.setBuddy(samplename)
        samplecompos = Wid.QLineEdit()
        samplecomposlabel = Wid.QLabel('Sample Composition:')
        samplecomposlabel.setBuddy(samplecompos)
        depoprocess = Wid.QComboBox()
        depoprocess.addItems(["Unknown", "Sputtering", "Pulsed Laser Deposition", 
                              "CVD", "MBE"])
    
        depolabel = Wid.QLabel('Deposition Process:')
        depolabel.setText('Deposition Process')
        depolabel.setBuddy(depoprocess)
        datefabric = Wid.QCalendarWidget()
        datelabel = Wid.QLabel('Date of fabrication:')
        datelabel.setBuddy(datefabric)
        infolayout.addWidget(samplelabel, 0, 0)
        infolayout.addWidget(samplename, 0, 1)
        infolayout.addWidget(samplecomposlabel, 1, 0)
        infolayout.addWidget(samplecompos, 1, 1)
        infolayout.addWidget(depoprocess, 2, 1)
        infolayout.addWidget(depolabel, 2, 0)
        infolayout.addWidget(datelabel, 3, 0)
        infolayout.addWidget(datefabric, 3, 1)
        infoWidget.setLayout(infolayout)
        
        #######################################################VSM Widget.
        #################################################
        ##########################################
        
        vsmWidget = Wid.QWidget()
        vsmlayout = Wid.QVBoxLayout(self)
        
        self.xframe = Wid.QFrame()
        xlayout = Wid.QGridLayout()
        
        #Iniciamos el objeto para plottear los datos.
        self.graph = canvas.PlotCanvas(3, width=4, height=6, dpi=100)
        
        self.label1 = Wid.QLabel('Moment Offset = ?')
        self.label2 = Wid.QLabel('Sample Dimensions = ?')
        self.label3 = Wid.QLabel('Saturation Magnetization = ?')
        self.label4 = Wid.QLabel('Coercitive Field = ?')
        self.button1 = Wid.QPushButton('Calc...')
        self.button2 = Wid.QPushButton('Edit...')
        self.button3 = Wid.QPushButton('Calc...')
        self.button4 = Wid.QPushButton('Calc...')

        
        xlayout.addWidget(self.graph, 0, 0)
        xlayout.addWidget(self.label1, 1, 0)
        xlayout.addWidget(self.label2, 2, 0)
        xlayout.addWidget(self.label3, 3, 0)
        xlayout.addWidget(self.label4, 4, 0)
        xlayout.addWidget(self.button1, 1, 1)
        xlayout.addWidget(self.button2, 2, 1)
        xlayout.addWidget(self.button3, 3, 1)
        xlayout.addWidget(self.button4, 4, 1)

        self.xframe.hide()
        self.xframe.setLayout(xlayout)
        
        openbutton = Wid.QPushButton('Open VSM file...', self)
        openbutton.setToolTip('Open a VSM data file to analyze.')
        openbutton.clicked.connect(self.getFilevsm)
 
        self.button1.clicked.connect(lambda: self.replot1('momentOffset'))
        self.button2.clicked.connect(self.openDialog)
        self.button3.clicked.connect(lambda: self.replot1('saturationMag'))
        self.button4.clicked.connect(lambda: self.replot1('coerField'))

        
        vsmlayout.addWidget(openbutton)
        vsmlayout.addWidget(self.xframe)
        vsmWidget.setLayout(vsmlayout)
        
        #######################################################
        ################################################################
        #######################################################################
        
        # RHEED Widget.
        rheedWidget = Wid.QWidget()
        #rheedlayout = Wid.QVBoxLayout(self)
        
        ###################################################### XRR Widget
        #################################################
        ######################################
        
        xrayWidget = Wid.QWidget()
        xraylayout = Wid.QVBoxLayout(self)
        
        self.xrframe = Wid.QFrame()
        xrlayout = Wid.QGridLayout()
        
        #Iniciamos el objeto para plottear los datos.

        sizesofxr = (3.0, 1, 10)
        self.graphxr = canvas.PlotCanvas(3, ownsizes=sizesofxr, width=4, height=6, dpi=100)

        layout1 = Wid.QGridLayout()
        xrrinfo = Wid.QLabel()
        xrrinfo.setText('-Details from loaded XRR data:')
        
        # Primer theta crit
        self.thetacritlab = Wid.QLabel()
        thetacritbutton = Wid.QPushButton()
        thetacritbutton.setText("Calc...")
        thetacritbutton.clicked.connect(lambda: self.replot1('thetacrit1'))
        thetacritbutton.setFixedSize(70, 25)
        self.thetacritlab.setText('2\u03B8<sub>c</sub> (I/2) = ?')
        
        # Etiqueta para el segundo theta.
        self.thetacrit2lab = Wid.QLabel()
        thetacrit2button = Wid.QPushButton()
        thetacrit2button.setText("Calculate from regression")
        thetacrit2button.clicked.connect(self.smoothXRRDialogRange)
        thetacrit2button.setFixedSize(200, 25)
        self.thetacrit2lab.setText('2\u03B8<sub>c</sub> (intercept) = ?')
        
        # Etiquetas para el ajuste
        #self.line = Wid.QFrame() 
        self.layout2 = Wid.QGridLayout()
        self.infolabel1 = Wid.QLabel()
        self.infolabel1.setText('-Peak fitting info:')
        self.infolabel2 = Wid.QLabel()
        self.infolabel2.setText('Number of peaks: ?')
        self.infolabel3 = Wid.QLabel()
        self.infolabel3.setText('Lowess: ?')
        self.infolabel4 = Wid.QLabel()
        self.infolabel4.setText('Slope:')
        self.infolabel5 = Wid.QLabel()
        self.infolabel5.setText('Intercept: ?')
        self.infolabel6 = Wid.QLabel()
        self.infolabel6.setText('R-squared: ?')
        self.infolabel7 = Wid.QLabel()
        self.infolabel7.setText('n-oddity: ?')
        #self.line.setFrameShadow(Wid.QFrame.Raised)
        
        self.layout2.addWidget(self.infolabel1, 0, 0)
        self.layout2.addWidget(self.infolabel2, 1, 0)      
        self.layout2.addWidget(self.infolabel3, 1, 1)
        self.layout2.addWidget(self.infolabel4, 2, 0)
        self.layout2.addWidget(self.infolabel5, 2, 1)
        self.layout2.addWidget(self.infolabel6, 3, 0)
        self.layout2.addWidget(self.infolabel7, 3, 1)
        
        # Agregamos al layout
        xrlayout.addWidget(self.graphxr, 0, 0)
        xrlayout.addWidget(xrrinfo, 1, 0)
        xrlayout.addLayout(layout1, 2, 0)
        layout1.addWidget(self.thetacritlab, 0, 0)
        layout1.addWidget(thetacritbutton, 0, 1)
        layout1.addWidget(self.thetacrit2lab, 1, 0)
        layout1.addWidget(thetacrit2button, 1, 1)
        layout1.addLayout(self.layout2, 2, 0)
        #xrlayout.addWidget(thetacrit2lab, 3, 0)
        self.xrframe.hide()
        self.xrframe.setLayout(xrlayout)
        
        #Initial open button for xrr files
        openbuttonxr = Wid.QPushButton('Open XRR file...', self)
        openbuttonxr.setToolTip('Open a XRR data file to analyze.')
        openbuttonxr.clicked.connect(self.getFilexrr)
 
        #XRR tab layout
        xraylayout.addWidget(openbuttonxr)
        xraylayout.addWidget(self.xrframe)
        xrayWidget.setLayout(xraylayout)
        
        
        # Tab info
        tab = Wid.QTabWidget()
        tab.setParent(self)
        tab.addTab(infoWidget, "Sample &Info")
        tab.addTab(xrayWidget, "&XRR data")
        tab.addTab(rheedWidget, "&RHEED data")
        tab.addTab(vsmWidget, "VS&M data")
        self.layout.addWidget(tab)
        self.setLayout(self.layout)

    def savegraph(self, data):
         name = Wid.QFileDialog.getSaveFileName(self, 'Save png image to location')
         if name is None:
             pass
         if data is "xrr":
             self.graphxr.savePlot(name[0])
         elif data is "vsm":
             self.graph.savePlot(name[0])

    def getFilevsm(self):
        name = Wid.QFileDialog.getOpenFileName(self, 'Open VSM File...')
        if name is None:
            pass
        self.vsminfo.loadFile(name[0])
        self.graph.limitPlot([-max(self.vsminfo.field), max(self.vsminfo.field)],
                             [-max(self.vsminfo.moment), max(self.vsminfo.moment)])

        self.graph.updatexyLabels('Field', 'Moment')
        self.graph.updatePlot([self.vsminfo.field, self.vsminfo.moment])
        self.xframe.show()
        self.vsminfo.testfunc()
        
    def getFilexrr(self):
        name = Wid.QFileDialog.getOpenFileName(self, 'Open XRR File...')
        if name is None:
            pass

        self.refldat.loadFile(name[0])
        self.thetarangestart = 0
        self.thetarangeend = len(self.refldat.x)
        self.graphxr.scalePlot('log')
        self.graphxr.updatexyLabels('2theta', 'Counts')
        self.graphxr.limitPlot([0, max(self.refldat.x)],
                                [min(self.refldat.counts), 
                                 max(self.refldat.counts)])
        self.graphxr.updatePlot([self.refldat.x, self.refldat.counts])
        self.xrframe.show()
        self.refldat.testReflect()
        self.xrronvalue.x.emit()


    def replot1(self, stri):
        self.updateType = stri
        if len(self.vsminfo.moment) == 0:
            pass
        if self.updateType == 'momentOffset':
            self.vsminfo.momentOffset()
            self.graph.limitPlot([-max(self.vsminfo.field), max(self.vsminfo.field)],
                                 [-max(self.vsminfo.moment), max(self.vsminfo.moment)])
            self.graph.updatePlot([self.vsminfo.field, self.vsminfo.moment])
            #self.graph.getData()
        elif self.updateType == 'saturationMag':
            self.vsminfo.saturationMag()
        elif self.updateType == 'coerField':
            self.fieldpoly, self.newfield, self.hc = self.vsminfo.coerField()
            self.graph.updatePlot([self.vsminfo.field, self.vsminfo.moment],
                                  [self.fieldpoly, self.newfield], 
                                  [(-self.hc, self.hc), (0,0)])
        elif self.updateType == 'thetacrit1':
            self.refldat.thetacritSpline()
            
            
        self.updateLabel()

    def replotXRRrange(self, tstart, tend):
        try:
            numstart = float(tstart.text())
            numend = float(tend.text())
            assert numstart < numend
        except:
            warn = Wid.QMessageBox()
            warn.setWindowTitle('Invalid data')
            ico = os.path.join(os.path.dirname(__file__), "laika.png")
            pixmap = QPixmap(ico).scaledToHeight(64, 
                                  Qt.SmoothTransformation)
            warn.setIconPixmap(pixmap)
            warn.setText('Invalid theta values or range! \nMake sure that '
                         'both values are \ncorrectly formatted &'
                         ' try again.')

            warn.setStandardButtons(Wid.QMessageBox.Ok)
            warn.buttonClicked.connect(warn.close)
            warn.exec_()
        else:
            idx = np.searchsorted(self.refldat.x, numstart, side="left")
            idy = np.searchsorted(self.refldat.x[idx:], numend, side="left")
            # I'll only change the graph scale, but we must know the
            # numbers for calculation.

            self.refldat.thetastart_i = idx
            self.refldat.thetaend_i = idy
 
            self.refldat.thetarangestart = self.refldat.x[idx]
            self.refldat.thetarangeend = self.refldat.x[idx+idy]
            # We set the new y limits as well.
            miny = np.amin(self.refldat.counts[idx:idx+idy])
            maxy = np.amax(self.refldat.counts[idx:idx+idy])
                    
            self.graphxr.limitPlot([self.refldat.thetarangestart,self.refldat.thetarangeend],
                                   [miny, maxy])
        
        
    def updateLabel(self):
        if self.updateType == 'momentOffset':
            self.label1.setText('Moment Offset = %e' % self.vsminfo.offset)
            self.label1.setStyleSheet('color=green')
        elif self.updateType == 'saturationMag':
            self.label3.setText('Saturation Magnetization = %f' %
                                self.vsminfo.saturationmag)
        elif self.updateType == 'coerField':
            self.label4.setText('Coercitive field = %e Oe' % self.hc)
        elif self.updateType == 'thetacrit1':
            self.thetacritlab.setText('2\u03B8<sub>c</sub> (I/2) = %f' % 
                                      self.refldat.thetacritic1)
        else:
            pass
        
    def openDialog(self):
       self.dialogM = Wid.QDialog()
       self.dialogM.setWindowTitle("Set sample size")      
       frame = Wid.QVBoxLayout()
       inputs = Wid.QFormLayout()
       text = Wid.QLabel()
       text.setText('Specify your sample\'s width \n'
                    '& height measured in cms.\n '
                    '(e.g: 1.2)')
       textx = Wid.QLabel()
       textx.setText('Width: ')
       width = Wid.QLineEdit()
       texty = Wid.QLabel()
       texty.setText('Height: ')
       height = Wid.QLineEdit()
       b1 = Wid.QPushButton("Submit", self.dialogM)
       b2 = Wid.QPushButton("Cancel", self.dialogM)
       b1.clicked.connect(lambda: self.returnSize(width, height))
       b2.clicked.connect(self.dialogM.close)
       b = Wid.QHBoxLayout()
       b.addWidget(b1)
       b.addWidget(b2)
       inputs.addRow(textx, width)
       inputs.addRow(texty, height)
       frame.addWidget(text)
       frame.addLayout(inputs)
       frame.addLayout(b)
       self.dialogM.setLayout(frame)
       self.dialogM.setFixedSize(230,170)
       self.dialogM.setWindowModality(Qt.ApplicationModal)
       self.dialogM.exec_()
       
    def returnSize(self, width, height):
        try:
            self.vsminfo.width = float(width.text())
            self.vsminfo.height = float(height.text())
        except:
            warn = Wid.QMessageBox()
            warn.setWindowTitle('Invalid data')
            ico = os.path.join(os.path.dirname(__file__), "laika.png")
            pixmap = QPixmap(ico).scaledToHeight(64, 
                                  Qt.SmoothTransformation)
            warn.setIconPixmap(pixmap)
            warn.setText('Invalid width or height!\nMake sure that '
                         'both measurements are \ncorrectly formatted &'
                         ' try again.')

            warn.setStandardButtons(Wid.QMessageBox.Ok)
            warn.buttonClicked.connect(warn.close)
            warn.exec_()
        # Replot graph
        else:
            self.vsminfo.sampleMeasure(self.vsminfo.width, self.vsminfo.height)
            self.graph.limitPlot([-max(self.vsminfo.field), max(self.vsminfo.field)],
                                 [-max(self.vsminfo.moment), max(self.vsminfo.moment)])
            self.graph.updatePlot([self.vsminfo.field, self.vsminfo.moment])
            self.graph.updatexyLabels('Field (Oe)', 'Units?')
            self.dialogM.close()
            
    def openXRRDialogRange(self):
        self.dialogM = Wid.QDialog()
        self.dialogM.setWindowTitle("Obtain 2\u03B8 by linear "
                                    "regression")
        frame = Wid.QVBoxLayout()
        inputs = Wid.QFormLayout()
        text = Wid.QLabel()
        text.setText('Specify the 2\u03B8 range you would like\n'
                     'to display.')
        starttext = Wid.QLabel()
        starttext.setText('2\u03B8 start: ')
        start = Wid.QLineEdit()
        endtext = Wid.QLabel()
        endtext.setText('2\u03B8 end: ')
        end = Wid.QLineEdit()
        b1 = Wid.QPushButton("Update", self.dialogM)
        b2 = Wid.QPushButton("Close", self.dialogM)
        b1.clicked.connect(lambda: self.replotXRRrange(start, end))
        b2.clicked.connect(self.dialogM.close)
        b = Wid.QHBoxLayout()
        b.addWidget(b1)
        b.addWidget(b2)
        inputs.addRow(starttext, start)
        inputs.addRow(endtext, end)
        frame.addWidget(text)
        frame.addLayout(inputs)
        frame.addLayout(b)
        self.dialogM.setLayout(frame)
        self.dialogM.setFixedSize(380,170)
        self.dialogM.setWindowModality(Qt.ApplicationModal)
        self.dialogM.exec_()

    def smoothXRRDialogRange(self):
           self.dialogM = Wid.QDialog()
           self.dialogM.setWindowTitle("Curve smoothing and peak "
                                       "finding")
           frame = Wid.QVBoxLayout()
           inputs1 = Wid.QHBoxLayout()
           inputs2 = Wid.QHBoxLayout()
           text = Wid.QLabel()
           text.setText('Specify the theta cutoff and \n'
                        'lowess fraction to use.')
           starttext = Wid.QLabel()
           starttext.setText('2\u03B8 cutoff: ')
           
           start = Wid.QLineEdit()
           start.setValidator(QDoubleValidator())
           endtext = Wid.QLabel()
           endtext.setText('Lowess fraction: ')
           self.end = Wid.QDoubleSpinBox()
           self.end.setRange(0.00,1.00)
           self.end.setSingleStep(0.01)
           b1 = Wid.QPushButton("Update", self.dialogM)
           b2 = Wid.QPushButton("Close", self.dialogM)
           b1.clicked.connect(lambda: self.smoothxrr(start.text(),
                                                     self.end.value()) )
           b2.clicked.connect(self.dialogM.close)

           b = Wid.QHBoxLayout()
           b.addWidget(b1)
           b.addWidget(b2)
           inputs1.addWidget(starttext)
           inputs1.addWidget(start)
           inputs2.addWidget(endtext)
           inputs2.addWidget(self.end)
           frame.addWidget(text)
           frame.addLayout(inputs1)
           frame.addLayout(inputs2)
           frame.addLayout(b)
           self.dialogM.setLayout(frame)
           self.dialogM.setFixedSize(380,170)
           self.dialogM.setWindowModality(Qt.ApplicationModal)
           self.dialogM.exec_()


    def smoothxrr(self, cutoff, fraclowess):
        # cutoff es lo que sale de la LineEdit box, sin modificar.
        # fraclowess viene de un DoubleSpinBox. Siempre es un float.
        
        if cutoff is "":
            print('No cutoff was specified. Using last theta value instead')
            cutoff = self.refldat.x[self.refldat.thetaend_i]
        else:
            cutoff = float(cutoff)
            
        lowess, xpeaks, peak_list = self.refldat.smoothcounts_wg(self.refldat.thetastart_i,
                                                                 self.refldat.thetaend_i,
                                                                 cutoff, fraclowess)

        start = self.refldat.thetastart_i
        end = self.refldat.x_cutoff
        
        if end is None:
            end = self.refldat.thetaend_i
            print('cutoff is None')


        self.graphxr.updatePlot([self.refldat.x[start:end], self.refldat.counts[start:end]],
                                [self.refldat.x[start:end], lowess[:,1]],
                                [xpeaks, peak_list])


    def calcPeaks(self):
        # Toma los valores calculados anteriormente al hacer el smooth de la función y encontrar
        # los picos, y luego elige el n a usar tal que minimice la diferencia entre el theta
        # crítico inicial y el encontrado aquí.

        n, slope1, intercept1, r_value1, thetacrit_exp1, thetacrit_diff1 = self.refldat.get_slope()
        thetacritcounts = self.refldat.thetacrit()
        thick = pow(slope1, -0.5)
        thicknm = thick * 0.1

        if abs(thetacrit_diff1) < 10:
            pic = "c-ok.png"
        elif 10 < abs(thetacrit_diff1) < 30:
            pic = "c-med.png"
        else:
            pic = "c-bad.png"
            
        message = Wid.QMessageBox()
        ico = os.path.join(os.path.dirname(__file__), pic)
        pixmap = QPixmap(ico).scaledToHeight(84, 
                                             Qt.SmoothTransformation)
        message.setIconPixmap(pixmap)
        text1 = ("Finished! A film thickness of %.3f nm was calculated."
                 "( = %.3f Angstroms)") % (thicknm, thick)
        message.setText(text1)
        message.setWindowTitle("Peak fitting finished")
        data = ("Details: \nFinal n: %d \nFitting results from data:\nSlope = %.4E\n"
                "Intercept = %.4E \nR-Squared = %f \n2\u03B8c value obtained was "
                "%.4f. Value obtained from counts was %.4f.\nPercentage difference"
                " between both critical angles is %.3f") % (n, slope1, intercept1,
                                                            r_value1, thetacrit_exp1,
                                                            thetacritcounts,
                                                            thetacrit_diff1)
        message.setDetailedText(data)
        message.setStandardButtons(Wid.QMessageBox.Ok)
        message.exec_()
        
