
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
#import matplotlib.pyplot as plt
import matplotlib.lines as lines
import PyQt5.QtWidgets as Wid

class PlotCanvas(FigureCanvas):

    def __init__(self, linenumber, parent=None, width=5, height=4, dpi=100):
        
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, Wid.QSizePolicy.Expanding,
                                   Wid.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
        self.ldict = {}
        lcolors = ('blue', 'red', 'purple', 'orange', 'green')
        lmarkers = ('o', 'o', 's', 'o', 'o')
        
        for i in range(0, linenumber):
            key = 'line' + str(i)
            self.ldict[key] = lines.Line2D([], [], marker=lmarkers[i], 
                                          color=lcolors[i], linestyle='') 

        self.draw()
        self.axes.grid()
        self.axes.set_ylabel('y')
        self.axes.set_xlabel('x')

    def scalePlot(self, scale='linear'):
        self.axes.set_yscale(scale)


    def limitPlot(self, xvalues, yvalues):
        # Replot with new scales.
        self.axes.set_xlim(xvalues)        
        self.axes.set_ylim(yvalues)
        self.fig.canvas.draw() 
        self.flush_events()   
        
    def getData(self):
        for key in self.ldict:
            print(self.ldict[key].get_data())


    def updatePlot(self, *args):
        for data, key in zip(args, self.ldict):
            self.ldict[key].set_data(data)
            self.axes.add_line(self.ldict[key])
        self.fig.canvas.draw() 
        self.flush_events()        
        
    def updatexyLabels(self, xlabel, ylabel):
        self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel(ylabel)
