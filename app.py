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
        self.window.geometry("536x750")
        self.window.title("Symbol Reviser")
        self.window.iconbitmap("res/icons/icon.ico")
        self.packs = self.getPacks("res/packs")
        self.current_pack = self.packs[0]
        self.pack_items = []
        self.introduced_items = []
        self.lives = 3
        self.full_grid = False
        self.correct_item = ""
        self.bg_colour = "PaleGreen3"
        self.fg_colour = "PaleGreen4"
        self.makeHomePage()


    def makeHomePage(self):
        homeFrame = self.makeFrame(self.window, 0.5, 0.5, 1, 1, "center", self.bg_colour)

        question_label = Label(homeFrame, font=("Avalon", 15), text="Pick the image pack to learn:", fg="black", bg=self.bg_colour)
        question_label.place(relx=0.5, rely=0.42, anchor="center")
        
        pack_choice = StringVar(homeFrame)
        pack_choice.set(self.current_pack) # default choice
        w = OptionMenu(homeFrame, pack_choice, *self.packs)
        w.config(bg=self.fg_colour, relief="solid", highlightthickness=0, font=("Avalon", 16))
        w["menu"].config(bg=self.fg_colour, fg="black", relief="solid")
        w.place(relx=0.57, rely=0.5, relw=0.5, relh=0.08, anchor="e")
        
        start_btn = Button(homeFrame, font=("Avalon", 16), text="START", bg=self.fg_colour, command=lambda: self.startSession(pack_choice.get()))
        start_btn.place(relx=0.6, rely=0.5, relw=0.3, relh=0.08, anchor="w")
        
        exit_btn = Button(homeFrame, font=("Avalon", 13), text="EXIT", bg=self.fg_colour, command=lambda: quit())
        exit_btn.place(relx=0.5, rely=0.95, relw=0.12, relh=0.04, anchor="center")


        
        start_btn = Button(homeFrame, font=("Avalon", 15), text="Start", command=lambda: self.startSession(pack_choice.get()))
        start_btn.place(relx=0.5, rely=0.7, relw=0.2, relh=0.05, anchor="center")

if __name__ == "__main__":
    root = Tk()
    symbolRevisionWindow(root)

