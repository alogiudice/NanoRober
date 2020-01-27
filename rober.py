#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 16:55:48 2019

@author: agostina
"""

import os
import sys
from datetime import date
from PyQt5.QtCore import QSize, Qt, pyqtSlot
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as Wid
import FormWidget as formw



__version__ = "1.0.0"

class MainWindow(Wid.QMainWindow):
    
    def __init__(self, parent = None):
        super().__init__()
        self.initUi()
        
    def initUi(self):
        #self.sizelabel.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
        self.form_widget = formw.FormWidget(self)
        self.setCentralWidget(self.form_widget)
        self.setGeometry(10, 10, 640, 640)
        
        # Creamos una menubar y una toolbar.
        fileToolbar = self.addToolBar('Toolbar')
        menubar1 = self.menuBar()
        fileMenu = menubar1.addMenu('&File')
        editMenu = menubar1.addMenu("Edit")
        dataMenu = menubar1.addMenu('Data')
        helpmenu = menubar1.addMenu('&Help')
        newSample = self.createAction("New Sample", "newsample", None, 
                                      "Create a new Sample file.")

        # Data menu options
        self.xrrsubmenu = dataMenu.addMenu("XRR data")
        # self.xrrsubmenu.setDisabled(True)
        self.vsmsubmenu = dataMenu.addMenu("VSM data")
        #vsmsubmenu.setDisabled(True)

        #VSM menu
        vsmgeometry = self.createAction("Measurement's geometry...", None, None, None)
        self.vsmsubmenu.addAction(vsmgeometry)

        vsmsample = self.createAction("Set sample size", None, None, None)
        self.vsmsubmenu.addAction(vsmsample)
        vsmsample.triggered.connect(self.form_widget.openDialog)
         
        vsmoffset = self.createAction("Correct offset", None, None, None)
        self.vsmsubmenu.addAction(vsmoffset)
        vsmoffset.triggered.connect(lambda: self.form_widget.replot1("momentOffset"))

        vsmsaturation = self.createAction("Calculate Msat", None, None, None)
        self.vsmsubmenu.addAction(vsmsaturation)
        vsmsaturation.triggered.connect(lambda: self.form_widget.replot1("saturationMag"))

        savevsmimage = self.createAction("Save VSM image as PNG", None, None, None)
        self.vsmsubmenu.addAction(savevsmimage)
        savevsmimage.triggered.connect(lambda: self.form_widget.savegraph("vsm"))
        

        # XRR menu
        changerangestr = "Adjust theta range for smoothing and\n peak finding"
        xrrchangerange = self.createAction("Change theta working range", None, None,
                                           changerangestr)
        self.xrrsubmenu.addAction(xrrchangerange)
        xrrchangerange.triggered.connect(self.form_widget.openXRRDialogRange)
        saveplotv = self.createAction("Save VSM plot as...")
        smoothcurve = self.createAction("Curve smoothing and peak finding...")
        smoothcurve.triggered.connect(self.form_widget.smoothXRRDialogRange)
        self.xrrsubmenu.addAction(smoothcurve)
        peakmanip = self.createAction("Edit peak points")
        peakmanip.triggered.connect(self.form_widget.editPeaks)
        self.xrrsubmenu.addAction(peakmanip)
        peakfinding = self.createAction("Fit peaks")
        peakfinding.triggered.connect(self.form_widget.calcPeaks)
        self.xrrsubmenu.addAction(peakfinding)
        savexrrimage = self.createAction("Save XRR image as PNG", None, None, None)
        savexrrimage.triggered.connect(lambda: self.form_widget.savegraph("xrr"))
        self.xrrsubmenu.addAction(savexrrimage)
        

        # Help menu
        
        helpme = self.createAction("About", 'Rober', None, None)
        
        newSample.triggered.connect(self.saveFile)
        helpme.triggered.connect(self.helpAbout)
        helpmenu.addAction(helpme)
        fileMenu.addAction(newSample)
        fileToolbar.addAction(newSample)

    # DOESN'T WORK YET :( SIGNAL FROM FORMWIDGET IS NOT BEING EMMITED
    @pyqtSlot()
    def receive_trigger_xrr(self):
        self.form_widget.xrronvalue.x.connect(self.onchangexrrvalue)
        print('REceived Trigger! Yayyyy')
            
    def onchangexrrvalue(self):
        self.xrrmenu.setDisabled(False)

        
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
    
#    def savePlot(self, graph):
#        name = Wid.QFileDialog.getSaveFileName(self, 'Save plot as')
#        self.graph.print_png(name[0])
#        print('Done printing file to %s.' % name[0])
    
    def saveFile(self):
        name = Wid.QFileDialog.getSaveFileName(self, 'Save file as')
        file = open(name[0], 'w')
        today = date.today()
        file.write('Holis! File created on %s\n File created with RoberNano.\n'
                   'Chauchis.' % today)
 #############################################################################       
            
            
if __name__ == '__main__':
    app = Wid.QApplication(sys.argv)
    app.setOrganizationName("Rober Ltd")
    app.setOrganizationDomain("www.github.com/alogiudice/nanorober-py")
    app.setApplicationName("NanoRober - version %s" % __version__)
    app.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__),
                                               "icons/rober.png")))
    form = MainWindow()
    form.show()
    app.exec_()
