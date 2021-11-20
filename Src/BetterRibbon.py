import witkets as wtk
import tkinter as tk
import tkinter.ttk as ttk



class BetterRibbon(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.Ribbon = wtk.Ribbon(self)
        self.Ribbon.pack(side=tk.RIGHT, expand=True, fill=tk.X)

        self.showbutton = ttk.Menubutton(self, text="V")
        self.showbutton.pack()

        self.menu = self.menu = tk.Menu(self.showbutton, tearoff=0)
        self.showbutton["menu"] = self.menu
    
    def getRibbon(self):
        return self.Ribbon

    def getMenu(self):
        return self.menu

    def getShowButton(self):
        return self.showbutton

    def showMenu(self, e):

        self.menu.post(e.x_root, e.y_root)
