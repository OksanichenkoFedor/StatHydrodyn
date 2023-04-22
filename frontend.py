from tkinter import Tk, W, E, BOTH, ttk, messagebox
import tkinter as tk
from tkinter.ttk import Frame, Button, Entry, Style, Label, Radiobutton


import plot, backend, circle_funcs, counting
import custom_contur_funcs


import config


class PE2_Frame(Frame):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.master.title("Нелинейные колебания")
        #Style().configure("TFrame", background="#333")
        self.pack(fill=BOTH, expand=True)

        Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 10')

        self.columnconfigure(2, pad=5)
        self.rowconfigure(4, pad=5)

        self.plotF = plot.PlotFrame(self)
        #self.bA = blockA(self)
        #self.bB = blockB(self)
        #self.bC = blockC(self)
        #self.bD = blockD(self)
        self.common = common_frame(self)

        self.plotF.grid(row=0, column=0, rowspan=4)
        self.common.grid(row=0, column=1, columnspan=2)
        #self.bA.grid(row=1, column=1)
        #self.bB.grid(row=1, column=2)
        #self.bC.grid(row=2, column=1)
        #self.bD.grid(row=2, column=2)
        #self.bE.grid(row=3, column=1)

        #self.pack()


class common_frame(Frame):
    def __init__(self, parent):
        self.master = parent
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.n_cells = tk.StringVar()
        self.poss_err = tk.StringVar()

        self.columnconfigure(3, pad=3)
        self.rowconfigure(4, pad=3)

        # подписи
        self.tot_lbl = Label(self, text="Общие параметры")
        self.tot_lbl.grid(row=0, column=0, columnspan=4)
        self.tot_lbl = Label(self, text="Параметры симуляции")
        self.tot_lbl.grid(row=1, column=0, columnspan=2)
        # поля для параметров
        self.dt_lbl = Label(self, text="Number of cells:")
        self.dt_lbl.grid(row=2, column=0)
        self.dt_ent = Entry(self, textvariable=self.n_cells)
        self.n_cells.set(config.N)
        self.dt_ent.grid(row=2, column=1)

        self.T_lbl = Label(self, text="Possible error (log10):")
        self.T_lbl.grid(row=3, column=0)
        self.T_ent = Entry(self, textvariable=self.poss_err)
        self.poss_err.set(config.poss_err)
        self.T_ent.grid(row=3, column=1)


        self.bcircle = tk.Button(self, text="Circle", width=14,
                               command=self.circle)
        self.bcircle.grid(row=5, column=0, columnspan=2)

        self.bcompile = tk.Button(self, text="Compile", state=tk.DISABLED, width=14,
                                 command=self.compile)
        self.bcompile.grid(row=5, column=2, columnspan=2)



    def unsafe_compile(self):
        config.poss_err = float(self.poss_err.get())
        config.N = int(self.n_cells.get())


    def circle(self):
        self.unsafe_compile()

        if config.is_count_custom:
            # потом уберём
            circle_funcs.generate_circle()
            backend.contur_ordering()
            custom_contur_funcs.generate_is_in_array()
        else:
            if config.curr_counting:
                circle_funcs.generate_circle()

        config.curr_drawing = "contur"
        self.master.plotF.replot()
        self.bcompile.config(state=tk.NORMAL)


    def compile(self):
        counting.count()
        config.curr_drawing = "3d"
        self.master.plotF.replot()
        self.bcompile.config(state=tk.DISABLED)