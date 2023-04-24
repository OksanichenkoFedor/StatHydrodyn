from tkinter import Tk, W, E, BOTH, ttk, messagebox
import tkinter as tk
from tkinter.ttk import Frame, Button, Entry, Style, Label, Radiobutton

import plot, backend, circle_funcs, counting, eclipse_funcs
import custom_contur_funcs
from additional_panels import CirclePanel, EclipsePanel, RectanglePanel, CustomPanel

import config


class PE2_Frame(Frame):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.master.title("Нелинейные колебания")
        # Style().configure("TFrame", background="#333")
        self.pack(fill=BOTH, expand=True)

        Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 10')

        self.columnconfigure(2, pad=5)
        self.rowconfigure(4, pad=5)

        self.plotF = plot.PlotFrame(self)
        # self.bA = blockA(self)
        # self.bB = blockB(self)
        # self.bC = blockC(self)
        # self.bD = blockD(self)
        self.common = common_frame(self)

        self.plotF.grid(row=0, column=0, rowspan=4)
        self.common.grid(row=0, column=1, columnspan=2)
        # self.bA.grid(row=1, column=1)
        # self.bB.grid(row=1, column=2)
        # self.bC.grid(row=2, column=1)
        # self.bD.grid(row=2, column=2)
        # self.bE.grid(row=3, column=1)

        # self.pack()


class common_frame(Frame):
    def __init__(self, parent):
        self.master = parent
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.n_cells = tk.StringVar()
        self.poss_err = tk.StringVar()
        self.nc_status_text = tk.StringVar()
        self.pe_status_text = tk.StringVar()

        self.draw_row = 8

        self.columnconfigure(3, pad=3)
        self.rowconfigure(4, pad=3)

        # подписи

        self.tot_lbl = Label(self, text="Parameters of the simulation")
        self.tot_lbl.grid(row=1, column=0, columnspan=2)
        # поля для параметров
        self.nc_lbl = Label(self, text="Number of cells:")
        self.nc_lbl.grid(row=2, column=0)
        self.nc_ent = Entry(self, textvariable=self.n_cells)
        self.n_cells.set(config.N)
        self.nc_ent.grid(row=2, column=1)
        self.nc_status_lbl = tk.Label(self, textvariable=self.nc_status_text, fg="green")
        self.nc_status_text.set("Correct value")
        self.nc_status_lbl.grid(row=3, column=0, columnspan=2)
        self.n_cells.trace("w", lambda name, index, mode, status=self.nc_status_text, colr=self.nc_status_lbl,
                                       value=self.n_cells: self.n_cells_callback(name, index, mode, status, colr,
                                                                                 value))

        self.pe_lbl = tk.Label(self, text="Possible error (log10):")
        self.pe_lbl.grid(row=4, column=0)
        self.pe_ent = tk.Entry(self, textvariable=self.poss_err)
        self.poss_err.set(config.poss_err)
        self.pe_ent.grid(row=4, column=1)
        self.pe_status_lbl = tk.Label(self, textvariable=self.pe_status_text, fg="green")
        self.pe_status_text.set("Correct value")
        self.pe_status_lbl.grid(row=5, column=0, columnspan=2)
        self.poss_err.trace("w", lambda name, index, mode, status=self.pe_status_text, colr=self.pe_status_lbl,
                                        value=self.poss_err: self.poss_err_callback(name, index, mode, status, colr,
                                                                                    value))

        self.curr_counting = tk.StringVar()

        self.rb_circle = Radiobutton(self, text="Circle",
                                     variable=self.curr_counting, value="circle")
        self.rb_eclipse = Radiobutton(self, text="Eclipse",
                                      variable=self.curr_counting, value="eclipse")
        self.rb_rectangle = Radiobutton(self, text="Rectangle",
                                        variable=self.curr_counting, value="rectangle")
        self.rb_custom = Radiobutton(self, text="Custom contur",
                                     variable=self.curr_counting, value="custom")

        self.curr_counting.set("circle")
        self.rb_circle.grid(row=6, column=0)
        self.rb_eclipse.grid(row=6, column=1)
        self.rb_rectangle.grid(row=7, column=0)
        self.rb_custom.grid(row=7, column=1)
        self.curr_counting.trace("w",
                                 lambda name, index, mode, status=self.curr_counting,: self.curr_counting_callback(name,
                                                                                                                   index,
                                                                                                                   mode,
                                                                                                                   status))

        self.circle_panel = CirclePanel(self)
        self.circle_panel.grid(row=self.draw_row, column=0, columnspan=2)

        self.eclipse_panel = EclipsePanel(self)
        self.eclipse_panel.grid(row=self.draw_row, column=0, columnspan=2)

        self.rectangle_panel = RectanglePanel(self)
        self.rectangle_panel.grid(row=self.draw_row, column=0, columnspan=2)

        self.custom_panel = CustomPanel(self)
        self.custom_panel.grid(row=self.draw_row, column=0, columnspan=2)

        # self.bcircle = tk.Button(self, text="Circle", width=14,
        #                       command=self.circle)
        # self.bcircle.grid(row=7, column=0, columnspan=4)

        # self.bcompile = tk.Button(self, text="Compile", state=tk.DISABLED, width=14,
        #                         command=self.compile)
        # self.bcompile.grid(row=6, column=0, columnspan=4)
        self.forget_not_drawing()

    def n_cells_callback(self, name, index, mode, status, colr, value):
        good_value = False
        try:
            n_cells = int(value.get())
            good_value = True
        except:
            pass
        if good_value:
            if n_cells > 0:
                config.N = n_cells
                status.set("Correct value")
                colr.configure(fg="green")
            else:
                status.set("Put positive value")
                colr.configure(fg="red")
        else:
            status.set("Put positive integer value")
            colr.configure(fg="red")

    def poss_err_callback(self, name, index, mode, status, colr, value):
        good_value = False
        try:
            poss_err = float(value.get())
            good_value = True
        except:
            pass
        if good_value:
            config.poss_err = poss_err
            status.set("Correct value")
            colr.configure(fg="green")
        else:
            status.set("Put float value")
            colr.configure(fg="red")

    def forget_not_drawing(self):
        if config.curr_counting == "circle":
            self.circle_panel = CirclePanel(self)
            self.circle_panel.grid(row=self.draw_row, column=0, columnspan=2)
            self.eclipse_panel.grid_forget()
            self.rectangle_panel.grid_forget()
            self.custom_panel.grid_forget()
        elif config.curr_counting == "eclipse":
            self.eclipse_panel = EclipsePanel(self)
            self.eclipse_panel.grid(row=self.draw_row, column=0, columnspan=2)
            self.circle_panel.grid_forget()
            self.rectangle_panel.grid_forget()
            self.custom_panel.grid_forget()
        elif config.curr_counting == "rectangle":
            self.rectangle_panel = RectanglePanel(self)
            self.rectangle_panel.grid(row=self.draw_row, column=0, columnspan=2)
            self.circle_panel.grid_forget()
            self.eclipse_panel.grid_forget()
            self.custom_panel.grid_forget()
        elif config.curr_counting == "custom":
            self.circle_panel.grid_forget()
            self.custom_panel = CustomPanel(self)
            self.custom_panel.grid(row=self.draw_row, column=0, columnspan=2)
            self.circle_panel.grid_forget()
            self.eclipse_panel.grid_forget()
            self.rectangle_panel.grid_forget()

    def curr_counting_callback(self, name, index, mode, status):
        config.curr_contur = None
        config.curr_drawing = "empty"
        self.master.plotF.replot()
        config.curr_counting = status.get()
        self.forget_not_drawing()
