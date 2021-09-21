import tkinter as tk
import random
import glob
import os

from tkinter import mainloop, Tk, Frame, Grid, N, E, S, W, Button, StringVar, OptionMenu, Label
from PIL import Image, ImageTk
from os import listdir




class symbolRevisionWindow:
    def __init__(self, parent):
        self.window = parent
        self.window.geometry("700x980")
        self.window.title("Symbol Reviser")

        self.packs = self.getPacks("res/packs")
        self.current_pack = self.packs[0]

        self.pack_items = []
        self.introduced_items = []
        self.lives = 3
        self.full_grid = False
        self.correct_item = ""


    def makeHomePage(self):
        homeFrame = self.makeFrame(self.window, 0.5, 0.5, 1, 1, "center", "green")

        question_label = Label(homeFrame, font=("Avalon", 15), text="Pick the symbol pack to learn:", bg="green")
        question_label.place(relx=0.5, rely=0.4, anchor="center")
        
        pack_choice = StringVar(homeFrame)
        pack_choice.set(self.current_pack) # default choice
        w = OptionMenu(homeFrame, pack_choice, *self.packs)
        w.place(relx=0.5, rely=0.5, relw=0.2, relh=0.04, anchor="center")
        
        start_btn = Button(homeFrame, font=("Avalon", 15), text="Start", command=lambda: self.startSession(pack_choice.get()))
        start_btn.place(relx=0.5, rely=0.7, relw=0.2, relh=0.05, anchor="center")


