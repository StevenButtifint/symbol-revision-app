import tkinter as tk
import random
import glob
import os

from tkinter import mainloop, Tk, Frame, Grid, N, E, S, W, Button, StringVar, OptionMenu, Label
from PIL import Image, ImageTk
from os import listdir


from constants import *


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


    @staticmethod
    def _makeOptionMenu(frame, choice, packs, bg, font, rx, ry, rw, rh, anchor):
        w = tk.OptionMenu(frame, choice, *packs)
        w.config(bg=bg, relief="solid", highlightthickness=0, font=font)
        w["menu"].config(bg=bg, fg=FONT_COLOUR, relief="solid")
        w.place(relx=rx, rely=ry, relw=rw, relh=rh, anchor=anchor)


    def startSession(self, pack_choice):
        self.setupSession(pack_choice)
        self.introducePage()
        

    def setupSession(self, pack_choice):
        self.current_pack = pack_choice
        self.lives = 3
        self.introduced_items.clear()
        self.pack_items.clear()
        self.pack_items = self.getItems(f'res/packs/{self.current_pack}', "png")
        

    def introducePage(self):
        introduction_frame = self.makeFrame(self.window, 0, 0, 1, 1, "nw", self.bg_colour)

        #pick random item, add to introduced list
        new_item = random.choice(self.pack_items)
        self.introduced_items.append(new_item)
        self.pack_items.remove(new_item)

        if (len(self.introduced_items) == 16) or (self.pack_items == []):
            self.full_grid = True

        new_item_name = os.path.basename(new_item)[:-4]

        question_label = Label(introduction_frame, font=("Avalon", 20), text="This is the image for \n" + new_item_name, bg=self.bg_colour)
        question_label.place(relx=0.5, rely=0.25, anchor="center")

        new_item_image = self.getTileImage(new_item, 300, 300)
        new_item_label = Label(introduction_frame, image = new_item_image)
        new_item_label.place(relx=0.5, rely=0.5, anchor="center")
        
        ok_button = Button(introduction_frame, font=("Avalon", 16), text="OK",
                           bg=self.fg_colour, command=lambda: self.makeRoundPage())
        ok_button.place(relx=0.5, rely=0.8, relw=0.2, relh=0.08, anchor="center")
        mainloop()


    def makeRoundPage(self):

        round_frame = self.makeFrame(self.window, 0, 0, 1, 1, "nw", "black")
        
        header_frame = self.makeFrame(round_frame, 0, 0, 1, 0.3, "nw", self.bg_colour)
        tiles_frame = self.makeFrame(round_frame, 0, 0.3, 1, 0.7, "nw", self.bg_colour)

        #load all png items from pack location
        all_items = self.getItems(f'res/packs/{self.current_pack}', "png")

        #pick name from pack and add to end of question
        self.correct_item = os.path.basename(random.choice(self.introduced_items))[:-4]
        
        question_label = Label(header_frame, font=("Avalon", 20), text="What is the image for\n " +
                               self.correct_item, bg=self.bg_colour)
        question_label.place(relx=0.5, rely=0.5, anchor="center")

        random.shuffle(self.introduced_items)

        tile_images = []
        tile_names = []
        
        for item in self.introduced_items:
            tile_images.append(self.getTileImage(item, 160, 160))
            tile_names.append(os.path.basename(item)[:-4])

        for x in range(len(self.introduced_items)):
            tile = Button(tiles_frame, image=tile_images[x])
            tile["command"] = lambda name=tile_names[x], tile=tile: self.checkTileClick(name, tile, question_label)
            tile["bg"] = self.fg_colour
            tile.place(relx=((x%4)*0.25), rely=((x//4)*0.25), relw=0.25, relh=0.25, anchor="nw")

        mainloop()#makes images show on buttons keeps page live?


    def checkTileClick(self, tile_name, tile, question_label):
        if tile_name == self.correct_item:
            print("correct")
            
            if not self.full_grid:
                self.introducePage()
                
            elif self.introduced_items != []:
                self.removeItem(self.correct_item, self.introduced_items)
                tile.destroy()

                if self.introduced_items != []:
                    self.correct_item = os.path.basename(random.choice(self.introduced_items))[:-4]
                    question_label["text"] = "What is the image for \n" + self.correct_item
                else:
                    self.full_grid = False
                    if self.pack_items == []:
                        self.makeHomePage()
                    else:
                        self.introducePage()                

        elif tile["bg"] != "red":
            tile["bg"] = "red"
            print("wrong")




    def getTileImage(self, img_name, w, h):
        image = self.getImage(img_name)
        image = self.resizeImage(image, w, h)
        return ImageTk.PhotoImage(image)


if __name__ == "__main__":
    root = Tk()
    symbolRevisionWindow(root)

