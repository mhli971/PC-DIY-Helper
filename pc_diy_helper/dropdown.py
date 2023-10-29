import tkinter as tk
from tkinter import ttk


class Dropdown:
    # Do not change anything here, all default
    def __init__(self, master, label_text, options, update_func, row, column):
        self.label = ttk.Label(master, text=label_text)
        self.label.grid(row=row, column=column, pady=5, padx=5)
        self.var = tk.StringVar(master)
        if options != []:
            self.var.set(options[0])  # set the default option
        else:
            self.var.set("")
        self.menu = ttk.Combobox(master, textvariable=self.var, values=options)
        self.menu.grid(row=row, column=column + 1, pady=5, padx=5)
        self.menu.bind("<<ComboboxSelected>>", update_func)
