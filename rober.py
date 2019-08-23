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
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


__version__ = "1.0.0"

class MainWindow(Wid.QMainWindow):
    
    def __init__(self, parent = None):
        super().__init__()
        self.initUi()
        
    def initUi(self):
        #self.sizelabel.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
        self.form_widget = FormWidget(self)
        self.setCentralWidget(self.form_widget)
        self.setGeometry(10, 10, 640, 480)
        
        
        # Creamos una menubar y una toolbar.
        fileToolbar = self.addToolBar('Toolbar')
        menubar1 = self.menuBar()
        fileMenu = menubar1.addMenu('&File')
        editMenu = menubar1.addMenu("Edit")
        helpmenu = menubar1.addMenu('&Help')
        newSample = self.createAction("New Sample", "newsample", None, 
                                      "Create a new Sample file.")
        
        newSample.triggered.connect(self.saveFile)
        fileMenu.addAction(newSample)
        fileToolbar.addAction(newSample)
        
        ##
        
    def createAction(self, text, icon=None, shortcut=None, tip=None, 
                     checkable=False):
        
        action = Wid.QAction(text, self)
        if icon is not None:
            name = icon + ".png"
            action.setIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__), 
                                              name)))
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if checkable:
            action.setCheckable(True)
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
        self.graph = PlotCanvas(self, width=4, height=6, dpi=100)
        
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
        openbutton.clicked.connect(self.getFile)
        # HAY UN ERROR DE NONETYPE ACÁ
        self.button1.clicked.connect(self.replot1(updateType='momentOffset'))
        self.button3.clicked.connect(self.replot1(updateType='saturationMag'))

        
        vsmlayout.addWidget(openbutton)
        vsmlayout.addWidget(self.xframe)
        vsmWidget.setLayout(vsmlayout)
        
        # RHEED Widget.
        rheedWidget = Wid.QWidget()
        #rheedlayout = Wid.QVBoxLayout(self)
        xrayWidget = Wid.QWidget()
        #xraylayout = Wid.QVBoxLayout(self)
        tab = Wid.QTabWidget()
        tab.setParent(self)
        tab.addTab(infoWidget, "Sample &Info")
        tab.addTab(xrayWidget, "&XRR Measurements")
        tab.addTab(rheedWidget, "&RHEED Measurements")
        tab.addTab(vsmWidget, "VS&M Measurements")
        self.layout.addWidget(tab)
        self.setLayout(self.layout)

    def getFile(self):
        name = Wid.QFileDialog.getOpenFileName(self, 'Open XRR File...')
        self.vsminfo.loadFile(name[0])
        self.graph.updatePlot(self.vsminfo.moment, self.vsminfo.field)
        self.xframe.show()
        self.vsminfo.testfunc()

    def replot1(self, updateType=None):
        if len(self.vsminfo.moment) != 0:
            if updateType == 'momentOffset':
                self.vsminfo.momentOffset()
                self.graph.updatePlot(self.vsminfo.field, self.vsminfo.moment)
            elif updateType == 'saturationMag':
                self.vsminfo.saturationMag()
            self.updateLabel(updateType)
        else:
            pass

    def updateLabel(self, updateType=None):
        if updateType == 'momentOffset':
            self.label1.setText('Moment Offset = %e' % self.vsminfo.offset)
            # OFFSET IS STUCK AT 0!!!1!
            self.label1.setStyleSheet('color= green')
        elif updateType == 'saturationMag':
            self.label3.setText('Saturation Magnetization = %f' %
                                self.vsminfo.saturationmag)
        else:
            pass
    
############################################################################# 
        
class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, Wid.QSizePolicy.Expanding,
                                   Wid.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.line1, = self.axes.plot([], [], 'ro')
        self.draw()
        self.axes.set_title('Magnetization vs Field')
        self.axes.grid()
        self.axes.set_ylabel('Moment')
        self.axes.set_xlabel('Field')

    def updatePlot(self, datax, datay):
        self.line1.set_xdata(datax)
        self.line1.set_ydata(datay)
        self.axes.set_ylim(-max(datay), max(datay))
        self.axes.set_xlim(-max(datax), max(datax))
        self.draw()
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
