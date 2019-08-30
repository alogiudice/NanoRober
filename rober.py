#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 16:55:48 2019

@author: agostina
"""

import os
import sys
from datetime import date
from PyQt5.QtCore import QSize, Qt
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as Wid
import VsmData as vsm
import ReflectData as reflect
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.lines as lines


__version__ = "1.0.0"

class MainWindow(Wid.QMainWindow):
    
    def __init__(self, parent = None):
        super().__init__()
        self.initUi()
        
    def initUi(self):
        #self.sizelabel.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
        self.form_widget = FormWidget(self)
        self.setCentralWidget(self.form_widget)
        self.setGeometry(10, 10, 640, 640)
        
        
        # Creamos una menubar y una toolbar.
        fileToolbar = self.addToolBar('Toolbar')
        menubar1 = self.menuBar()
        fileMenu = menubar1.addMenu('&File')
        editMenu = menubar1.addMenu("Edit")
        helpmenu = menubar1.addMenu('&Help')
        newSample = self.createAction("New Sample", "newsample", None, 
                                      "Create a new Sample file.")
        
        helpme = self.createAction("About", 'Rober', None, None)
        
        newSample.triggered.connect(self.saveFile)
        helpme.triggered.connect(self.helpAbout)
        helpmenu.addAction(helpme)
        fileMenu.addAction(newSample)
        fileToolbar.addAction(newSample)
        
        ##
    def helpAbout(self):
        msg = Wid.QMessageBox.about(self, "About NanoRober",
                            """<b>NanoRober - Sample Analysis Simplifier</b> 
                            <p>Version %s (2019) by Agostina Lo Giudice.
                            (logiudic@tandar.cnea.gov.ar)
                            <p>This program is distributed under the GNU 
                            Public License v3.
                            """ % __version__)
        
    def createAction(self, text, icon=None, shortcut=None, tip=None):
        action = Wid.QAction(text, self)
        if icon is not None:
            name = icon + ".png"
            action.setIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__), 
                                              name)))
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        return action
    
    def saveFile(self):
        name = Wid.QFileDialog.getSaveFileName(self, 'Save file as')
        file = open(name[0], 'w')
        today = date.today()
        file.write('Holis! File created on %s\n File created with RoberNano.\n'
                   'Chauchis.' % today)
         
 #############################################################################       
        
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
        
        #VSM Widget.
        vsmWidget = Wid.QWidget()
        vsmlayout = Wid.QVBoxLayout(self)
        
        self.xframe = Wid.QFrame()
        xlayout = Wid.QGridLayout()
        
        #Iniciamos el objeto para plottear los datos.
        #self.graph = PlotCanvas(self, 3, width=4, height=6, dpi=100)
        self.graph = PlotCanvas(3, width=4, height=6, dpi=100)
        
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
        self.button3.clicked.connect(lambda: self.replot1('saturationMag'))
        self.button4.clicked.connect(lambda: self.replot1('coerField'))

        
        vsmlayout.addWidget(openbutton)
        vsmlayout.addWidget(self.xframe)
        vsmWidget.setLayout(vsmlayout)
        
        # RHEED Widget.
        rheedWidget = Wid.QWidget()
        #rheedlayout = Wid.QVBoxLayout(self)
        
        ###################################################### XRR Widget
        xrayWidget = Wid.QWidget()
        xraylayout = Wid.QVBoxLayout(self)
        
        self.xrframe = Wid.QFrame()
        xrlayout = Wid.QGridLayout()
        
        #Iniciamos el objeto para plottear los datos.
        #self.graph = PlotCanvas(self, 3, width=4, height=6, dpi=100)
        self.graphxr = PlotCanvas(3, width=4, height=6, dpi=100)

        self.xrframe.hide()
        self.xrframe.setLayout(xrlayout)
        
        openbuttonxr = Wid.QPushButton('Open XRR file...', self)
        openbuttonxr.setToolTip('Open a XRR data file to analyze.')
        openbuttonxr.clicked.connect(self.getFilexrr)
 
#        self.button1.clicked.connect(lambda: self.replot1('momentOffset'))
#        self.button3.clicked.connect(lambda: self.replot1('saturationMag'))
#        self.button4.clicked.connect(lambda: self.replot1('coerField'))

        xraylayout.addWidget(openbuttonxr)
        xraylayout.addWidget(self.xrframe)
        xrayWidget.setLayout(xraylayout)
        
        
        
        
        
        
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
        self.vsminfo.loadFile(name[0])
        self.graph.updatePlot([self.vsminfo.moment, self.vsminfo.field])
        self.xframe.show()
        self.vsminfo.testfunc()
            
    def getFilexrr(self):
        name = Wid.QFileDialog.getOpenFileName(self, 'Open XRR File...')
        self.refldat.loadFile(name[0])
        self.graphxr.updatePlot([self.refldat.x, self.refldat.counts])
        self.xrframe.show()
        self.refldat.testReflect()

    def replot1(self, stri):
        self.updateType = stri
        if len(self.vsminfo.moment) != 0:
            if self.updateType == 'momentOffset':
                self.vsminfo.momentOffset()
                self.graph.updatePlot([self.vsminfo.field, self.vsminfo.moment])
            elif self.updateType == 'saturationMag':
                self.vsminfo.saturationMag()
            elif self.updateType == 'coerField':
                self.fieldpoly, self.newfield, self.hc = self.vsminfo.coerField()
                self.graph.updatePlot([self.vsminfo.field, self.vsminfo.moment],
                                      [self.fieldpoly, self.newfield], 
                                      [(-self.hc, self.hc), (0,0)])
            self.updateLabel()
        else:
            pass

    def updateLabel(self):
        if self.updateType == 'momentOffset':
            self.label1.setText('Moment Offset = %e' % self.vsminfo.offset)
            self.label1.setStyleSheet('color= green')
        elif self.updateType == 'saturationMag':
            self.label3.setText('Saturation Magnetization = %f' %
                                self.vsminfo.saturationmag)
        elif self.updateType == 'coerField':
            self.label4.setText('Coercitive field = %e Oe' % self.hc)
        else:
            pass
    
############################################################################# 
        
        
class PlotCanvas(FigureCanvas):

    def __init__(self, linenumber, parent=None, width=5, height=4, dpi=100):
        
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, Wid.QSizePolicy.Expanding,
                                   Wid.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
        self.ldict = {}
        lcolors = ('magenta', 'red', 'orange', 'purple', 'green')
        lmarkers = ('o', 'o', 's', 'o', 'o')
        
        for i in range(0, linenumber):
            key = 'line' + str(i)
            self.ldict[key] = lines.Line2D([], [], marker=lmarkers[i], 
                                          color=lcolors[i]) 

        self.draw()
        self.axes.set_title('Magnetization vs Field')
        self.axes.grid()
        self.axes.set_ylabel('Moment')
        self.axes.set_xlabel('Field')

    def updatePlot(self, *args):
        for data, key in zip(args, self.ldict):
            self.ldict[key].set_data(data)
            #print(self.ldict[key])
            self.axes.add_line(self.ldict[key])
            if key == 'line0':
                self.axes.set_ylim(-max(data[1]), max(data[1]))
                self.axes.set_xlim(-max(data[0]), max(data[0]))
        self.fig.canvas.draw() 
        self.flush_events()        
        


#############################################################################            
            
if __name__ == '__main__':
    app = Wid.QApplication(sys.argv)
    app.setOrganizationName("Rober Ltd")
    app.setOrganizationDomain("www.github.com/alogiudice/nanorober-py")
    app.setApplicationName("NanoRober - version %s" % __version__)
    app.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__),
                                               "rober.png")))
    form = MainWindow()
    form.show()
    app.exec_()
