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


