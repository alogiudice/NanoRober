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
import PyPlotCanvas as canvas



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
        xrrinfo = Wid.QLabel()
        xrrinfo.setText('-Details from loaded XRR data:')
        thetacritlab = Wid.QLabel()
        thetacrit2lab = Wid.QLabel()
        thetacritlab.setText('2\u03B8<sub>c</sub> (I/2) = ?')
        thetacrit2lab.setText('2\u03B8<sub>c</sub> (intercept) = ?')
        xrlayout.addWidget(self.graphxr, 0, 0)
        xrlayout.addWidget(xrrinfo, 1, 0)
        xrlayout.addWidget(thetacritlab, 2, 0)
        xrlayout.addWidget(thetacrit2lab, 3, 0)
        self.xrframe.hide()
        self.xrframe.setLayout(xrlayout)
        
        openbuttonxr = Wid.QPushButton('Open XRR file...', self)
        openbuttonxr.setToolTip('Open a XRR data file to analyze.')
        openbuttonxr.clicked.connect(self.getFilexrr)
 


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
            self.graph.getData()
        elif self.updateType == 'saturationMag':
            self.vsminfo.saturationMag()
        elif self.updateType == 'coerField':
            self.fieldpoly, self.newfield, self.hc = self.vsminfo.coerField()
            self.graph.updatePlot([self.vsminfo.field, self.vsminfo.moment],
                                  [self.fieldpoly, self.newfield], 
                                  [(-self.hc, self.hc), (0,0)])
        self.updateLabel()
        
        
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
            pixmap = QtGui.QPixmap(ico).scaledToHeight(64, 
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
