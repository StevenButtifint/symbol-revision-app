from PIL import Image, ImageTk
from os import listdir
import tkinter as tk
import random
import glob
import os
from constants import *


class symbolRevisionWindow:
    def __init__(self, parent):
        self.window = parent
        self.window.geometry("536x750")
        self.window.title("Symbol Reviser")
        self.window.iconbitmap("res/icons/icon.ico")
        self.packs = listdir("res/packs")
        self.current_pack = self.packs[0]
        self.pack_items = []
        self.introduced_items = []
        self.lives = 3
        self.full_grid = False
        self.correct_item = ""
        self.makeHomePage()


    def makeHomePage(self):
        homeFrame = self.makeFrame(self.window, 0.5, 0.5, 1, 1, "center", COLOUR_LIGHT)
        self._makeLabel(homeFrame, (FONT_TYPE, 15), "Pick the image pack to learn:", FONT_COLOUR, COLOUR_LIGHT, 0.5, 0.42,"center")
        pack_choice = tk.StringVar(homeFrame)
        pack_choice.set(self.current_pack) # default choice
        self._makeOptionMenu(homeFrame, pack_choice, self.packs, COLOUR_DARK, (FONT_TYPE, 16), 0.57, 0.5, 0.5, 0.08, "e")
        self._makeButton(homeFrame, (FONT_TYPE, 16), "START", COLOUR_DARK, 0.6, 0.5, 0.3, 0.08, "w", lambda: self.startSession(pack_choice.get()))
        self._makeButton(homeFrame, (FONT_TYPE, 13), "EXIT", COLOUR_DARK, 0.5, 0.95, 0.12, 0.04, "center", lambda: quit())


    @staticmethod
    def _makeButton(frame, font, text, bg, rx, ry, rw, rh, anchor, command):
        button = tk.Button(frame, font=font, text=text, bg=bg, command = lambda: command())
        button.place(relx=rx, rely=ry, relw=rw, relh=rh, anchor=anchor)
        return button


    @staticmethod
    def _makeLabel(frame, font, text, fg, bg, rx, ry, anchor):
        label = tk.Label(frame, font=font, text=text, fg=fg, bg=bg)
        label.place(relx=rx, rely=ry, anchor=anchor)
        return label


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
        introduction_frame = self.makeFrame(self.window, 0, 0, 1, 1, "nw", COLOUR_LIGHT)
        #pick random item, add to introduced list
        new_item = random.choice(self.pack_items)
        self.introduced_items.append(new_item)
        self.pack_items.remove(new_item)

        if (len(self.introduced_items) == 16) or (self.pack_items == []):
            self.full_grid = True

        new_item_name = os.path.basename(new_item)[:-4]
        self._makeLabel(introduction_frame, (FONT_TYPE, 20), "This is the image for \n" + new_item_name, FONT_COLOUR, COLOUR_LIGHT, 0.5, 0.25,"center")
        new_item_image = self.getTileImage(new_item, 300, 300)
        new_item_label = tk.Label(introduction_frame, image = new_item_image)
        new_item_label.place(relx=0.5, rely=0.5, anchor="center")
        self._makeButton(introduction_frame, (FONT_TYPE, 16), "OK", COLOUR_DARK, 0.5, 0.8, 0.2, 0.08, "center", lambda: self.makeRoundPage())
        root.mainloop()


    def makeRoundPage(self):

        round_frame = self.makeFrame(self.window, 0, 0, 1, 1, "nw", COLOUR_LIGHT)
        header_frame = self.makeFrame(round_frame, 0, 0, 1, 0.3, "nw", COLOUR_LIGHT)
        tiles_frame = self.makeFrame(round_frame, 0, 0.3, 1, 0.7, "nw", COLOUR_LIGHT)

        #load all png items from pack location
        all_items = self.getItems(f'res/packs/{self.current_pack}', "png")
        #pick name from pack and add to end of question
        self.correct_item = os.path.basename(random.choice(self.introduced_items))[:-4]
        question_label = self._makeLabel(header_frame, (FONT_TYPE, 20), "What is the image for\n " + self.correct_item, FONT_COLOUR, COLOUR_LIGHT, 0.5, 0.5,"center")
        random.shuffle(self.introduced_items)

        tile_images = []
        tile_names = []
        
        for item in self.introduced_items:
            tile_images.append(self.getTileImage(item, 160, 160))
            tile_names.append(os.path.basename(item)[:-4])

        for x in range(len(self.introduced_items)):
            tile = self._makeButton(tiles_frame, (FONT_TYPE, 16), "", COLOUR_DARK, ((x%4)*0.25), ((x//4)*0.25), 0.25, 0.25, "nw", lambda: quit())
            tile["image"] = tile_images[x]            
            tile["command"] = lambda name=tile_names[x], tile=tile: self.checkTileClick(name, tile, question_label)

        root.mainloop()


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

        elif tile["bg"] != COLOUR_INCORRECT:
            tile["bg"] = COLOUR_INCORRECT
            print("wrong")


    @staticmethod
    def removeItem(item, items):
        for content in items:
            if content[:-4].endswith(item):
                items.remove(content)

                
    @staticmethod
    def getItems(location, extension):
        return glob.glob(f'{location}/*.{extension}')


    @staticmethod
    def makeFrame(parent, relx, rely, relw, relh, anchor, bg):
        frame = tk.Frame(parent, bg=bg)
        frame.place(relx=relx, rely=rely, relw=relw, relh=relh, anchor=anchor)
        return frame


    def getTileImage(self, img_name, w, h):
        image = Image.open(img_name)
        image = image.resize((w, h))
        return ImageTk.PhotoImage(image)


if __name__ == "__main__":
    root = tk.Tk()
    symbolRevisionWindow(root)

