#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 15:49:40 2019

@author: agostina
"""

import os
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap, QIcon
import PyQt5.QtWidgets as Wid
import VsmData as vsm
import ReflectData as reflect
import PyPlotCanvas as canvas

class FormWidget(Wid.QWidget):
    
    def __init__(self, parent):
        
        self.vsminfo = vsm.VsmData()
        self.refldat = reflect.Reflect()
        super().__init__(parent)
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
        
        self.graphxr = canvas.PlotCanvas(3, width=4, height=6, dpi=100)
        self.graphlow = canvas.PlotCanvas(4, width=3, height=3, dpi=100)

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
        thetacrit2button.clicked.connect(self.openDialogXRR)
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
        tab.addTab(xrayWidget, "&XRR Measurements")
        tab.addTab(rheedWidget, "&RHEED Measurements")
        tab.addTab(vsmWidget, "VS&M Measurements")
        self.layout.addWidget(tab)
        self.setLayout(self.layout)

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
        self.graphxr.scalePlot('log')
        self.graphxr.updatexyLabels('2theta', 'Counts')
        self.graphxr.limitPlot([0, max(self.refldat.x)],
                                [min(self.refldat.counts), 
                                 max(self.refldat.counts)])
        self.graphxr.updatePlot([self.refldat.x, self.refldat.counts])
        self.xrframe.show()
        self.refldat.testReflect()


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
            
        elif self.updateType == 'lowess':
            self.graphlow.updatePlot()
            
        self.updateLabel()
        
#    def replotNormal(self, graph, *kwargs):
#        x1 = self.refldat.maxcounts_i
#        x2 = 
#        self.graphlow.updatePlot([self.refldat.x,[])
        
        
        
        
    def updateLabel(self):
        if self.updateType == 'momentOffset':
            self.label1.setText('Moment Offset = %e' % self.vsminfo.offset)
            self.label1.setStyleSheet('color= green')
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
            
    def openDialogXRR(self):
        self.dialogM = Wid.QDialog()
        self.dialogM.setWindowTitle("Obtain 2\u03B8 by linear "
                                    "regression")      
        
        checkico = os.path.join(os.path.dirname(__file__), "check.png")
        pixmap = QPixmap(checkico)
        self.graphlow.replot1
        self.layout = Wid.QHBoxLayout()
        self.layout.addWidget(self.graphlow)
        
        self.layout2 = Wid.QGridLayout()
        #Theta cutoff
        theta_cutoff = Wid.QLabel()
        theta_cutoff.setText('\u03B8 cutoff:')
        theta_cutoff_line = Wid.QLineEdit()
        theta_cutoff_accept = Wid.QPushButton()
        theta_cutoff_accept.setIcon(QIcon(pixmap))
        #Lowess
        lowess = Wid.QLabel()
        lowess.setText('Lowess frac: ')
        lowess_line = Wid.QLineEdit()
        lowess_accept = Wid.QPushButton()
        lowess_accept.setIcon(QIcon(pixmap))
        
        self.layout2.addWidget(theta_cutoff, 0, 0)
        self.layout2.addWidget(theta_cutoff_line, 0, 1)
        self.layout2.addWidget(theta_cutoff_accept, 0, 2)
        self.layout2.addWidget(lowess, 1, 0)
        self.layout2.addWidget(lowess_line, 1, 1)
        self.layout2.addWidget(lowess_accept, 1, 2)
        self.layout.addLayout(self.layout2)
        
        frame1 = Wid.QFrame()
        frame1.setFrameShape(Wid.QFrame.HLine)
        frame1.setLineWidth(1)
        self.layout3 = Wid.QVBoxLayout()
        self.layout3.addWidget(frame1)
        self.layout2.addLayout(self.layout3, 2,0)
        
        self.dialogM.setLayout(self.layout)
        #self.dialogM.setFixedSize(230,170)
        self.dialogM.setWindowModality(Qt.ApplicationModal)
        self.dialogM.exec_()