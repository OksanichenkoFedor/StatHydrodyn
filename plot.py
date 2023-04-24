import matplotlib
import matplotlib.pyplot as plt
import tkinter as tk
import config
import backend
from scipy.fft import fft, fftfreq
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk



from matplotlib.figure import Figure

class PlotFrame(tk.Frame):
    def __init__(self, parent):
        self.master = parent
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.f = Figure(figsize=(10, 10))#, dpi=100, tight_layout=True)
        self.a = self.f.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.f, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, columnspan=2)

        self.toolbarFrame = tk.Frame(master=self)
        self.toolbarFrame.grid(row=1, columnspan=2, sticky="w")
        self.toolbar1 = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)
        self.plot()

    def plot(self):
        self.replot()


    def replot(self):
        self.f.clf()

        if config.curr_drawing in ["3d", "contur", "empty", "drawing"]:
            if config.curr_drawing == "3d":
                self.a = self.f.add_subplot(111, projection='3d')
                curr_x = config.curr_x
                if (config.curr_x).all() != None:
                    X = np.arange(0, config.curr_x.shape[0], 1)
                    Y = np.arange(0, config.curr_x.shape[1], 1)
                    K, B = np.meshgrid(X, Y)
                    Fs = config.curr_x
                    surf = self.a.plot_surface(K, B, Fs)
                    self.a.set_xlabel('x')
                    self.a.set_ylabel('y')
                    self.a.set_zlabel('V')
            elif config.curr_drawing == "contur":

                if config.curr_contur != None:
                    self.a = self.f.add_subplot(111)
                    self.a.set_xlim([0, config.N])
                    self.a.set_ylim([0, config.N])
                    self.a.plot(config.curr_contur[0], config.curr_contur[1])
                    self.a.grid()
            elif config.curr_drawing == "empty":
                pass

            self.canvas.draw()


        else:
            print("Incorrect current drawing")
        self.canvas.draw()
