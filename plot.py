import matplotlib
import matplotlib.pyplot as plt
import tkinter as tk
import config
import backend
from scipy.fft import fft, fftfreq
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Polygon

matplotlib.use('TkAgg')

from matplotlib.ticker import MultipleLocator, FormatStrFormatter

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from matplotlib.figure import Figure


class PlotFrame(tk.Frame):
    def __init__(self, parent):
        self.master = parent
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.f = Figure(figsize=(10, 10))  # , dpi=100, tight_layout=True)
        self.a = self.f.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.f, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, columnspan=2)
        self.canvas.mpl_connect("motion_notify_event", self.move_mouse_event)
        self.canvas.mpl_connect("button_press_event", self.click_mouse_event)
        self.canvas.mpl_connect("button_release_event", self.unclick_mouse_event)

        self.toolbarFrame = tk.Frame(master=self)
        self.toolbarFrame.grid(row=1, columnspan=2, sticky="w")
        self.toolbar1 = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)
        self.plot()

    def plot(self):
        self.replot()

    def replot(self):
        if config.curr_drawing != "empty plot":
            self.f.clf()

        if config.curr_drawing in ["3d", "contur", "empty", "drawing", "empty plot"]:
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
                    for i in range(len(config.curr_contur[0])):
                        self.fill_point(config.curr_contur[0][i], config.curr_contur[1][i])
                    # self.a.plot(config.curr_contur[0], config.curr_contur[1])
                    self.make_grid()

            elif config.curr_drawing == "empty":
                pass
            elif config.curr_drawing == "empty plot":
                self.a = self.f.add_subplot(111)
                self.a.set_xlim([0, config.N])
                self.a.set_ylim([0, config.N])
                self.make_grid()
            elif config.curr_drawing == "drawing":
                self.a = self.f.add_subplot(111)
                self.a.set_xlim([0, config.N])
                self.a.set_ylim([0, config.N])
                self.make_grid()

            self.canvas.draw()


        else:
            print("Incorrect current drawing")
        config.last_drawed = config.curr_drawing
        self.canvas.draw()

    def make_grid(self):
        self.a.xaxis.set_major_locator(MultipleLocator(config.major_delta))
        self.a.yaxis.set_major_locator(MultipleLocator(config.major_delta))
        self.a.xaxis.set_minor_locator(MultipleLocator(config.minor_delta))
        self.a.yaxis.set_minor_locator(MultipleLocator(config.minor_delta))
        self.a.xaxis.grid(True, 'minor', alpha=config.minor_alpha)
        self.a.yaxis.grid(True, 'minor', alpha=config.minor_alpha)
        self.a.xaxis.grid(True, 'major')
        self.a.yaxis.grid(True, 'major')

    def fill_point(self, x, y):
        polygon = Polygon([(x + 0, y + 0), (x + 1, y + 0), (x + 1, y + 1), (x + 0, y + 1)], fill=True, closed=True)
        self.a.add_patch(polygon)

    def move_mouse_event(self, event):
        if config.curr_counting != "custom":
            return 0
        if config.curr_drawing != "drawing":
            return 0
        if not config.mouse_clicked:
            return 0
        if event.ydata == None or event.xdata == None:
            return 0
        x = int(event.xdata)
        y = int(event.ydata)
        config.curr_contur[0].append(x)
        config.curr_contur[1].append(y)
        self.fill_point(x, y)
        self.canvas.draw()
        #print("Move:", event.xdata, event.ydata)

    def click_mouse_event(self, event):
        if event.ydata == None or event.xdata == None:
            return 0
        if config.curr_counting != "custom":
            return 0
        if config.curr_drawing != "drawing":
            return 0
        config.mouse_clicked = True
        config.curr_contur = [[], []]
        #print("Click:", event.xdata, event.ydata)

    def unclick_mouse_event(self, event):
        if config.curr_counting != "custom":
            return 0
        if config.curr_drawing != "drawing":
            return 0
        config.mouse_clicked = False
        self.master.common.custom_panel.custom_contur()
        #print("Unclick", event.xdata, event.ydata)
