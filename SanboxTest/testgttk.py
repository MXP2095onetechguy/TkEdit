import tkinter as tk
from tkinter import ttk
from gttk import GTTK

window = tk.Tk()
gttk = GTTK(window)
style = ttk.Style()
style.theme_use("gttk")
print(gttk.get_current_theme()) # Prints the active GTK theme
gttk.set_gtk_theme("Yaru") # Sets GTK theme, provided by developer
ttk.Button(window, text="Destroy", command=window.destroy).pack()

window.mainloop()