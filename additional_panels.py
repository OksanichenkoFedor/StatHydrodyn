import tkinter as tk
from tkinter.ttk import Progressbar
from tkinter import Entry, Label
import config
from circle_funcs import generate_circle
from eclipse_funcs import generate_eclipse
from rectangle_funcs import generate_rectangle
from backend import contur_ordering
from custom_contur_funcs import generate_is_in_array
from counting import count

class Circle_panel(tk.Frame):
    def __init__(self, master):
        self.master = master
        super().__init__(master)

        self.progress_var = tk.IntVar()
        self.progress_txt = tk.StringVar()

        self.bcircle = tk.Button(self, text="Count contur", width=14,
                                 command=self.circle)
        self.bcircle.grid(row=0, column=0, columnspan=2)
        self.bcompile = tk.Button(self, text="Compile", state=tk.DISABLED, width=14,
                                  command=self.compile)
        self.bcompile.grid(row=1, column=0, columnspan=2)
        self.progress_bar = Progressbar(self, orient="horizontal",  maximum=10,  mode="determinate",  var=self.progress_var)
        self.progress_lbl = tk.Label(self, textvariable=self.progress_txt)
        self.progress_txt.set("Delta: 0")
        self.progress_bar.grid(row=2, column=0)
        self.progress_lbl.grid(row=2, column=1)


    def circle(self):

        generate_circle()
        contur_ordering()
        generate_is_in_array()

        config.curr_drawing = "contur"
        self.master.master.plotF.replot()
        self.bcompile.config(state=tk.NORMAL)


    def compile(self):
        config.curr_drawing = "empty"
        self.master.master.plotF.replot()
        count(self.progress_bar, self.progress_txt, self.progress_var)
        config.curr_drawing = "3d"
        self.master.master.plotF.replot()
        self.bcompile.config(state=tk.DISABLED)



class Eclipse_panel(tk.Frame):
    def __init__(self, master):
        self.master = master
        super().__init__(master)

        self.progress_var = tk.IntVar()
        self.progress_txt = tk.StringVar()
        self.a_status_text = tk.StringVar()
        self.b_status_text = tk.StringVar()

        self.a = tk.StringVar()
        self.a_lbl = Label(self, text="a: ")
        self.a_lbl.grid(row=0, column=0)
        self.a_ent = Entry(self, textvariable=self.a)
        self.a.set(config.a)
        self.a_ent.grid(row=0, column=1)
        self.a_status_lbl = tk.Label(self, textvariable=self.a_status_text, fg="green")
        self.a_status_text.set("Correct value")
        self.a_status_lbl.grid(row=1, column=0, columnspan=2)
        self.a.trace("w", lambda name, index, mode, status=self.a_status_text, colr=self.a_status_lbl,
                                       value=self.a: self.a_callback(name, index, mode, status, colr,
                                                                                 value))

        self.b = tk.StringVar()
        self.b_lbl = Label(self, text="b: ")
        self.b_lbl.grid(row=2, column=0)
        self.b_ent = Entry(self, textvariable=self.b)
        self.b.set(config.b)
        self.b_ent.grid(row=2, column=1)
        self.b_status_lbl = tk.Label(self, textvariable=self.b_status_text, fg="green")
        self.b_status_text.set("Correct value")
        self.b_status_lbl.grid(row=3, column=0, columnspan=2)
        self.b.trace("w", lambda name, index, mode, status=self.b_status_text, colr=self.b_status_lbl,
                                 value=self.b: self.b_callback(name, index, mode, status, colr,
                                                              value))

        self.beclipse = tk.Button(self, text="Count contur", width=14,
                                 command=self.eclipse)
        self.beclipse.grid(row=4, column=0, columnspan=2)
        self.bcompile = tk.Button(self, text="Compile", state=tk.DISABLED, width=14,
                                  command=self.compile)
        self.bcompile.grid(row=5, column=0, columnspan=2)

        self.progress_bar = Progressbar(self, orient="horizontal", maximum=10, mode="determinate",
                                        var=self.progress_var)
        self.progress_lbl = tk.Label(self, textvariable=self.progress_txt)
        self.progress_txt.set("Delta: 0")
        self.progress_bar.grid(row=6, column=0)
        self.progress_lbl.grid(row=6, column=1)



    def eclipse(self):
        generate_eclipse()
        contur_ordering()
        generate_is_in_array()

        config.curr_drawing = "contur"
        self.master.master.plotF.replot()
        self.bcompile.config(state=tk.NORMAL)

    def compile(self):
        config.curr_drawing = "empty"
        self.master.master.plotF.replot()
        count(self.progress_bar, self.progress_txt, self.progress_var)
        config.curr_drawing = "3d"
        self.master.master.plotF.replot()
        self.bcompile.config(state=tk.DISABLED)

    def a_callback(self, name, index, mode, status, colr, value):
        good_value = False
        try:
            a = float(value.get())
            good_value = True
        except:
            pass
        if good_value:
            if a >= 1.0:
                config.a = a
                status.set("Correct value")
                colr.configure(fg="green")
            else:
                status.set("The semi-axis of the ellipse can't be smaller than 1")
                colr.configure(fg="red")
        else:
            status.set("Enter the number")
            colr.configure(fg="red")

    def b_callback(self, name, index, mode, status, colr, value):
        good_value = False
        try:
            b = float(value.get())
            good_value = True
        except:
            pass
        if good_value:
            if b >= 1.0:
                config.b = b
                status.set("Correct value")
                colr.configure(fg="green")
            else:
                status.set("The semi-axis of the ellipse can't be smaller than 1")
                colr.configure(fg="red")
        else:
            status.set("Enter the number")
            colr.configure(fg="red")


class Rectangle_panel(tk.Frame):
    def __init__(self, master):
        self.master = master
        super().__init__(master)

        self.progress_var = tk.IntVar()
        self.progress_txt = tk.StringVar()
        self.m_status_text = tk.StringVar()
        self.n_status_text = tk.StringVar()

        self.m = tk.StringVar()
        self.m_lbl = Label(self, text="m: ")
        self.m_lbl.grid(row=0, column=0)
        self.m_ent = Entry(self, textvariable=self.m)
        self.m.set(config.m)
        self.m_ent.grid(row=0, column=1)
        self.m_status_lbl = tk.Label(self, textvariable=self.m_status_text, fg="green")
        self.m_status_text.set("Correct value")
        self.m_status_lbl.grid(row=1, column=0, columnspan=2)
        self.m.trace("w", lambda name, index, mode, status=self.m_status_text, colr=self.m_status_lbl,
                                       value=self.m: self.m_callback(name, index, mode, status, colr,
                                                                                 value))

        self.n = tk.StringVar()
        self.n_lbl = Label(self, text="n: ")
        self.n_lbl.grid(row=2, column=0)
        self.n_ent = Entry(self, textvariable=self.n)
        self.n.set(config.n)
        self.n_ent.grid(row=2, column=1)
        self.n_status_lbl = tk.Label(self, textvariable=self.n_status_text, fg="green")
        self.n_status_text.set("Correct value")
        self.n_status_lbl.grid(row=3, column=0, columnspan=2)
        self.n.trace("w", lambda name, index, mode, status=self.n_status_text, colr=self.n_status_lbl,
                                 value=self.n: self.n_callback(name, index, mode, status, colr,
                                                              value))

        self.beclipse = tk.Button(self, text="Count contur", width=14,
                                 command=self.rectangle)
        self.beclipse.grid(row=4, column=0, columnspan=2)
        self.bcompile = tk.Button(self, text="Compile", state=tk.DISABLED, width=14,
                                  command=self.compile)
        self.bcompile.grid(row=5, column=0, columnspan=2)

        self.progress_bar = Progressbar(self, orient="horizontal", maximum=10, mode="determinate",
                                        var=self.progress_var)
        self.progress_lbl = tk.Label(self, textvariable=self.progress_txt)
        self.progress_txt.set("Delta: 0")
        self.progress_bar.grid(row=6, column=0)
        self.progress_lbl.grid(row=6, column=1)



    def rectangle(self):
        generate_rectangle()
        contur_ordering()
        generate_is_in_array()

        config.curr_drawing = "contur"
        self.master.master.plotF.replot()
        self.bcompile.config(state=tk.NORMAL)

    def compile(self):
        config.curr_drawing = "empty"
        self.master.master.plotF.replot()
        count(self.progress_bar, self.progress_txt, self.progress_var)
        config.curr_drawing = "3d"
        self.master.master.plotF.replot()
        self.bcompile.config(state=tk.DISABLED)

    def m_callback(self, name, index, mode, status, colr, value):
        good_value = False
        try:
            m = float(value.get())
            good_value = True
        except:
            pass
        if good_value:
            if (m <= 1.0) and (m > 0):
                config.m = m
                status.set("Correct value")
                colr.configure(fg="green")
            else:
                status.set("m must be in (0,1] diapason")
                colr.configure(fg="red")
        else:
            status.set("Enter the number")
            colr.configure(fg="red")

    def n_callback(self, name, index, mode, status, colr, value):
        good_value = False
        try:
            n = float(value.get())
            good_value = True
        except:
            pass
        if good_value:
            if (n <= 1.0) and (n > 0):
                config.n = n
                status.set("Correct value")
                colr.configure(fg="green")
            else:
                status.set("n must be in (0,1] diapason")
                colr.configure(fg="red")
        else:
            status.set("Enter the number")
            colr.configure(fg="red")