#!/usr/bin/env python3

# TkEdit
# TkEdit
# TkEdit

# fork of <https://github.com/dh7qc/Python-Text-Editor>

# Licenses
# GPL
# Copyright (C) 2021 MXPSQL
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# MIT License
# 
# Copyright (c) 2021 MXPSQL
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 
# 
# Zlib license
# 
# Copyright (c) 2021 MXPSQL
# 
# This software is provided 'as-is', without any express or implied
# warranty. In no event will the authors be held liable for any damages
# arising from the use of this software.
# 
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
# 
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.
#
# One last request for you and users of TkEdit:
# Please don't sue or bring me to the court to steal this from me.

import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as tkfd
from tkinter import messagebox as tkmb
from tkinter import simpledialog as tksd
import tkinter.font as tkf
import tkinter.scrolledtext as tkst
from PIL import Image, ImageTk, ImageGrab
import os
from hashlib import md5
import sys
import requests
import argparse
import tkinterdnd2 as tkdnd
import tooltip
import Pmw
import webbrowser
import witkets as wtk

class LessViewer(tk.Toplevel):
    def __init__(self, parent, text, font, **kwargs):
        super().__init__(parent, **kwargs)

        self.font = font

        self.fm = tk.Frame(self)
        self.fm.pack()

        self.text = tkst.ScrolledText(self.fm, font=self.font)
        self.text.pack(side=tk.TOP, fill=tk.BOTH)
        self.text.insert(tk.END, text)
        self.text["state"] = tk.DISABLED

        self.exit = tk.Button(self.fm, text="Exit", command=self.destroy)
        self.exit.pack()

class Document:
    def __init__(self, Frame, TextWidget, FileDir=''):
        self.file_dir = FileDir
        self.file_name = 'Untitled' if not FileDir else os.path.basename(FileDir)
        self.textbox = TextWidget

    def Mk5(self):
        self.status = md5(self.textbox.get(1.0, 'end').encode('utf-8'))
        
class Editor:
    def __init__(self, master, assetDir, font, firstfile, srcurl, wtkstyle, **kwargs):
        self.master = master
        # print(firstfile)

        self.font = font

        self.wtkstyle = wtkstyle
        wtk.Style.set_default_fonts()
        self.wtkstyle.apply_default()

        self.srcurl = srcurl

        self.assetPath = os.path.join(os.getcwd(), assetDir)

        # create main frame
        self.fm = tk.Frame(self.master, **kwargs)
        self.fm.pack(fill=tk.BOTH)

        # create timers
        self.fm.timer = tk.Frame(self.fm)
        self.fm.timer.t1 = tk.Frame(self.fm.timer)

        # self.fm.timer.t1.after(20, self.UpdateStatus)

        # create toolbar
        # self.ImageExit = Image.open(os.path.join(self.assetPath, "Exit.png"))
        # self.ImageTkExit = ImageTk.PhotoImage(self.ImageExit)

        self.RibbonToolbarfm = tk.Frame(self.fm)
        self.RibbonToolbarfm.pack(fill=tk.X, side=tk.TOP)

        self.RibbonToolbar = wtk.Ribbon(self.RibbonToolbarfm)
        self.RibbonToolbar_pack()

        self.RibbonToolbar.maintab = self.RibbonToolbar.add_tab('Main Document')
        self.RibbonToolbar.maintab.Editor = self.RibbonToolbar.maintab.create_h_group("Editor")



        self.RibbonToolbar_right_click_menu = tk.Menu(self.master, tearoff=0)
        self.RibbonToolbar_right_click_menu.add_command(label="Open from WebRequest", command=self.webrequest)
        self.RibbonToolbar_right_click_menu.add_command(label="Quit", command=self.exit)
        self.RibbonToolbar_right_click_menu.add_separator()
        self.RibbonToolbar_right_click_menu.add_command(label="Hide toolbar", command=self.RibbonToolbar_unpack)
        self.RibbonToolbar.bind('<Button-3>', self.right_click_toolbar)

        self.RibbonToolbar.maintab.Editor.exit = self.RibbonToolbar.maintab.Editor.create_toolbar_item(os.path.join(self.assetPath, "Exit.png"), text="Exit")
        self.RibbonToolbar.maintab.Editor.exit["command"] = self.exit
        # self.RibbonToolbar.exit.pack(side=tk.LEFT, padx=2, pady=2)
        self.RibbonToolbar.maintab.Editor.exit.tooltip = tooltip.CreateToolTip(self.RibbonToolbar.maintab.Editor.exit, text="Exit the editor")

        # self.ImageClose = Image.open(os.path.join(self.assetPath, "Close.png"))
        # self.ImageTkClose = ImageTk.PhotoImage(self.ImageClose)

        # self.RibbonToolbar.close = tk.Button(self.RibbonToolbar, relief=tk.FLAT, command=self.close_tab, image=self.ImageTkClose)
        # self.RibbonToolbar.close.pack(side=tk.LEFT, padx=2, pady=2)
        # self.RibbonToolbar.close.tooltip = tooltip.CreateToolTip(self.RibbonToolbar.close, text="Close the open tab", waittime=250)
        self.RibbonToolbar.maintab.Editor.close = self.RibbonToolbar.maintab.Editor.create_toolbar_item(os.path.join(self.assetPath, "Close.png"), text="Close")
        self.RibbonToolbar.maintab.Editor.close["command"] = self.close_tab
        self.RibbonToolbar.maintab.Editor.close.tooltip = tooltip.CreateToolTip(self.RibbonToolbar.maintab.Editor.close, text="Close the open tab", waittime=250)

        # self.RibbonToolbar.separator = tk.Label(self.RibbonToolbar, text="|")
        # self.RibbonToolbar.separator.pack(side=tk.LEFT, padx=2, pady=2)

        # self.ImageNew = Image.open(os.path.join(self.assetPath, "New.png"))
        # self.ImageTkNew = ImageTk.PhotoImage(self.ImageNew)

        self.RibbonToolbar.maintab.OpenNew = self.RibbonToolbar.maintab.create_h_group("Open and New")

        # self.RibbonToolbar.new = tk.Button(self.RibbonToolbar, relief=tk.FLAT, image=self.ImageTkNew, command=self.new_file)
        # self.RibbonToolbar.new.pack(side=tk.LEFT, padx=2, pady=2)
        # self.RibbonToolbar.new.tooltip = tooltip.CreateToolTip(self.RibbonToolbar.new, text="New tab for new file")

        self.RibbonToolbar.maintab.OpenNew.new = self.RibbonToolbar.maintab.OpenNew.create_toolbar_item(os.path.join(self.assetPath, "New.png"), text="New")
        self.RibbonToolbar.maintab.OpenNew.new["command"] = self.new_file
        self.RibbonToolbar.maintab.OpenNew.new.tooltip = tooltip.CreateToolTip(self.RibbonToolbar.maintab.OpenNew.new, text="New tab for new file")


        # self.ImageOpenL = Image.open(os.path.join(self.assetPath, "Open.png"))
        # self.ImageTkOpenL = ImageTk.PhotoImage(self.ImageOpenL)

        # self.RibbonToolbar.openlocal = tk.Button(self.RibbonToolbar, relief=tk.FLAT, command=self.open_file, image=self.ImageTkOpenL)
        # self.RibbonToolbar.openlocal.pack(side=tk.LEFT, padx=2, pady=2)
        # self.RibbonToolbar.openlocal.tooltip = tooltip.CreateToolTip(self.RibbonToolbar.openlocal, text="Open from local filesystem")

        self.RibbonToolbar.maintab.OpenNew.openlocal = self.RibbonToolbar.maintab.OpenNew.create_toolbar_item(os.path.join(self.assetPath, "Open.png"), text="Open")
        self.RibbonToolbar.maintab.OpenNew.openlocal["command"] = self.open_file
        self.RibbonToolbar.maintab.OpenNew.openlocal = tooltip.CreateToolTip(self.RibbonToolbar.maintab.OpenNew.openlocal, text="Open from local filesystem")

        # self.ImageWebRq = Image.open(os.path.join(self.assetPath, "WebRq.png"))
        # self.ImageTkWebRq = ImageTk.PhotoImage(self.ImageWebRq)

        # self.RibbonToolbar.WebRq = tk.Button(self.RibbonToolbar, relief=tk.FLAT, command=self.webrequest, image=self.ImageTkWebRq)
        # self.RibbonToolbar.WebRq.pack(side=tk.LEFT, padx=2, pady=2)
        # self.RibbonToolbar.WebRq.tooltip = tooltip.CreateToolTip(self.RibbonToolbar.WebRq, text="Open by fecthing from web")

        self.RibbonToolbar.maintab.OpenNew.WebRq = self.RibbonToolbar.maintab.OpenNew.create_toolbar_item(os.path.join(self.assetPath, "WebRq.png"), text="WebRequest")
        self.RibbonToolbar.maintab.OpenNew.WebRq["command"] = self.webrequest
        self.RibbonToolbar.maintab.OpenNew.WebRq = tooltip.CreateToolTip(self.RibbonToolbar.maintab.OpenNew.WebRq, text="Open by fecthing from web")

        # self.RibbonToolbar.separator2 = tk.Label(self.RibbonToolbar, text="|")
        # self.RibbonToolbar.separator2.pack(side=tk.LEFT, padx=2, pady=2)

        self.RibbonToolbar.maintab.FileWritter = self.RibbonToolbar.maintab.create_h_group("File Writter")

        # self.ImageSave = Image.open(os.path.join(self.assetPath, "save.png"))
        # self.ImageTkSave = ImageTk.PhotoImage(self.ImageSave)

        # self.RibbonToolbar.Save = tk.Button(self.RibbonToolbar, relief=tk.FLAT, command=self.save_file, image=self.ImageTkSave)
        # self.RibbonToolbar.Save.pack(side=tk.LEFT, padx=2, pady=2)
        # self.RibbonToolbar.Save.tooltip = tooltip.CreateToolTip(self.RibbonToolbar.Save, text="Save file")

        self.RibbonToolbar.maintab.FileWritter.Save = self.RibbonToolbar.maintab.FileWritter.create_toolbar_item(os.path.join(self.assetPath, "save.png"), text="Save")
        self.RibbonToolbar.maintab.FileWritter.Save["command"] = self.save_file
        self.RibbonToolbar.maintab.FileWritter.Save = tooltip.CreateToolTip(self.RibbonToolbar.maintab.FileWritter.Save, text="Save file")

        # self.ImageSaveAs = Image.open(os.path.join(self.assetPath, "saveas.png"))
        # self.ImageTkSaveAs = ImageTk.PhotoImage(self.ImageSaveAs)

        # self.RibbonToolbar.SaveAs = tk.Button(self.RibbonToolbar, relief=tk.FLAT, command=self.save_as, image=self.ImageTkSaveAs)
        # self.RibbonToolbar.SaveAs.pack(side=tk.LEFT, padx=2, pady=2)
        # self.RibbonToolbar.SaveAs.tooltip = tooltip.CreateToolTip(self.RibbonToolbar.SaveAs, text="Save file as")

        self.RibbonToolbar.maintab.FileWritter.SaveAs = self.RibbonToolbar.maintab.FileWritter.create_toolbar_item(os.path.join(self.assetPath, "saveas.png"), text="Save As")
        self.RibbonToolbar.maintab.FileWritter.SaveAs["command"] = self.save_as
        self.RibbonToolbar.maintab.FileWritter.SaveAs = tooltip.CreateToolTip(self.RibbonToolbar.maintab.FileWritter.SaveAs, text="Save file as")

        self.RibbonToolbar.edittab = self.RibbonToolbar.add_tab('Edit')

        self.RibbonToolbar.edittab.Clipboard = self.RibbonToolbar.edittab.create_h_group("Clipboard")

        self.RibbonToolbar.edittab.Clipboard.cut = self.RibbonToolbar.edittab.Clipboard.create_toolbar_item(os.path.join(self.assetPath, "Cut.png"), text="Cut")
        self.RibbonToolbar.edittab.Clipboard.cut["command"] = self.cut
        self.RibbonToolbar.edittab.Clipboard.cut.tooltip = tooltip.CreateToolTip(self.RibbonToolbar.edittab.Clipboard.cut, text="Delete the selected text, but copy it to the clipboard before it gets deleted")

        self.RibbonToolbar.edittab.Clipboard.copy = self.RibbonToolbar.edittab.Clipboard.create_toolbar_item(os.path.join(self.assetPath, "copy.png"), text="copy")
        self.RibbonToolbar.edittab.Clipboard.copy["command"] = self.copy
        self.RibbonToolbar.edittab.Clipboard.copy.tooltip = tooltip.CreateToolTip(self.RibbonToolbar.edittab.Clipboard.copy, text="Copy the text to the clipboard")

        self.RibbonToolbar.edittab.Clipboard.paste = self.RibbonToolbar.edittab.Clipboard.create_toolbar_item(os.path.join(self.assetPath, "paste.png"), text="paste")
        self.RibbonToolbar.edittab.Clipboard.paste["command"] = self.paste
        self.RibbonToolbar.edittab.Clipboard.paste.tooltip = tooltip.CreateToolTip(self.RibbonToolbar.edittab.Clipboard.paste, text="Paste from the clipboard")
        
        # self.RibbonToolbar.edittab.Clipboard.cut = self.RibbonToolbar.edittab.Clipboard.create_toolbar_item(os.path.join(self.assetPath, "Cut.png"), text="Cut")
        # self.RibbonToolbar.edittab.Clipboard.cut["command"] = self.cut
        # self.RibbonToolbar.edittab.Clipboard.cut.tooltip = tooltip.CreateToolTip(self.RibbonToolbar.edittab.Clipboard.cut, text="Delete the selected text, but copy it to the clipboard before it gets deleted")

        self.RibbonToolbar.edittab.TextSelect = self.RibbonToolbar.edittab.create_h_group("Text and Pen select")

        self.RibbonToolbar.edittab.TextSelect.SelectAll = self.RibbonToolbar.edittab.TextSelect.create_toolbar_item(os.path.join(self.assetPath, "SelectAll.png"), text="Select")
        self.RibbonToolbar.edittab.TextSelect.SelectAll["command"] = self.select_all
        self.RibbonToolbar.edittab.TextSelect.SelectAll = tooltip.CreateToolTip(self.RibbonToolbar.edittab.TextSelect.SelectAll, text="Select all text")

        self.RibbonToolbar.edittab.TextSelect.delete = self.RibbonToolbar.edittab.TextSelect.create_toolbar_item(os.path.join(self.assetPath, "Delete.png"), text="Delete")
        self.RibbonToolbar.edittab.TextSelect.delete["command"] = self.delete
        self.RibbonToolbar.edittab.TextSelect.delete = tooltip.CreateToolTip(self.RibbonToolbar.edittab.TextSelect.delete, text="Delete selected text")

        self.RibbonToolbar.edittab.TextSelect.UndoRedo = self.RibbonToolbar.edittab.TextSelect.create_v_group([(os.path.join(self.assetPath, "undo.png"), 'Undo'), (os.path.join(self.assetPath, "redo.png"), 'Redo')])
        self.RibbonToolbar.edittab.TextSelect.UndoRedo[0]["command"] = self.undo
        self.RibbonToolbar.edittab.TextSelect.UndoRedo[0].tooltip = tooltip.CreateToolTip(self.RibbonToolbar.edittab.TextSelect.UndoRedo[0], text="Undo text")
        self.RibbonToolbar.edittab.TextSelect.UndoRedo[1]["command"] = self.redo
        self.RibbonToolbar.edittab.TextSelect.UndoRedo[1].tooltip = tooltip.CreateToolTip(self.RibbonToolbar.edittab.TextSelect.UndoRedo[1], text="Redo text")

        
        self.filetypes = (("Normal text file", "*.txt"), ("all files", "*.*"))
        self.init_dir = os.path.join(os.path.expanduser('~'), 'Desktop')
        
        self.tabs = {} # { index, text widget }

        # create editor Frame
        self.editfm = tk.Frame(self.fm)
        self.editfm.pack(expand=1, fill=tk.BOTH)
        
        # Create Notebook ( for tabs ).
        self.nb = ttk.Notebook(self.editfm)
        self.nb.bind("<Button-2>", self.close_tab)
        self.nb.bind("<B1-Motion>", self.move_tab)
        self.nb.pack(expand=1, fill=tk.BOTH, side=tk.TOP)
        self.nb.enable_traversal()
        #self.nb.bind('<<NotebookTabChanged>>', self.tab_change)

        # Override the X button.
        self.master.protocol('WM_DELETE_WINDOW', self.exit)
        
        # Create Menu Bar
        menubar = tk.Menu(self.master)
        
        # Create File Menu
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.new_file)
        filemenu.add_command(label="Open From Local", command=self.open_file)
        filemenu.add_command(label="Open From Web", command=self.webrequest)
        filemenu.add_command(label="Open as Less", command=self.LessView)
        filemenu.add_command(label="Save", command=self.save_file)
        filemenu.add_command(label="Save As...", command=self.save_as)
        filemenu.add_command(label="Close", command=self.close_tab)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exit)
        
        # Create Edit Menu
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo", command=self.undo)
        editmenu.add_separator()
        editmenu.add_command(label="Cut", command=self.cut)
        editmenu.add_command(label="Copy", command=self.copy)
        editmenu.add_command(label="Paste", command=self.paste)
        editmenu.add_command(label="Delete", command=self.delete)
        editmenu.add_command(label="Select All", command=self.select_all)
        editmenu.add_separator()
        editmenu.add_command(label="Show Toolbar", command=self.RibbonToolbar_pack)
        
        # Create Format Menu, with a check button for word wrap.
        formatmenu = tk.Menu(menubar, tearoff=0)
        self.word_wrap = tk.BooleanVar()
        formatmenu.add_checkbutton(label="Word Wrap", onvalue=True, offvalue=False, variable=self.word_wrap, command=self.wrap)

        # Create help menu
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Show Repository", command=lambda: webbrowser.open(self.srcurl, new=2))
        helpmenu.add_command(label="About", command=self.showAboutDialog)
        helpmenu.add_command(label="License", command=self.showLicense)
        
        # Attach to Menu Bar
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Edit", menu=editmenu)
        menubar.add_cascade(label="Format", menu=formatmenu)
        menubar.add_cascade(label="Help", menu=helpmenu)
        self.master.config(menu=menubar)
        
        # Create right-click menu.
        self.right_click_menu = tk.Menu(self.master, tearoff=0)
        self.right_click_menu.add_command(label="Undo", command=self.undo)
        self.right_click_menu.add_separator()
        self.right_click_menu.add_command(label="Cut", command=self.cut)
        self.right_click_menu.add_command(label="Copy", command=self.copy)
        self.right_click_menu.add_command(label="Paste", command=self.paste)
        self.right_click_menu.add_command(label="Delete", command=self.delete)
        self.right_click_menu.add_separator()
        self.right_click_menu.add_command(label="Select All", command=self.select_all)
        
        # Create tab right-click menu
        self.tab_right_click_menu = tk.Menu(self.master, tearoff=0)
        self.tab_right_click_menu.add_command(label="New Tab", command=self.new_file)
        self.tab_right_click_menu.add_command(label="Close Open Tab", command=self.close_tab)
        self.nb.bind('<Button-3>', self.right_click_tab)

        # create status bar
        self.statusbar = tk.Frame(self.editfm)
        self.statusbar.pack(fill=tk.X, side=tk.BOTTOM)

        self.statusbar.fmfm = tk.Frame(self.statusbar)
        self.statusbar.fmfm.pack(fill=tk.X, side=tk.TOP)

        self.statusbar.fmfm.fm1 = tk.Frame(self.statusbar.fmfm, relief=tk.SUNKEN, bd=1)
        self.statusbar.fmfm.fm1.pack(side=tk.LEFT, expand=1, fill=tk.X)
        # self.statusbar.fmfm.fm1.grid(row=0, column=0)

        self.statusbar.fmfm.fm1.label = tk.Label(self.statusbar.fmfm.fm1, text="A")
        self.statusbar.fmfm.fm1.label.pack(side=tk.LEFT, expand=1)

        self.statusbar.fmfm.fm2 = tk.Frame(self.statusbar.fmfm, relief=tk.SUNKEN, bd=1)
        self.statusbar.fmfm.fm2.pack(side=tk.LEFT, expand=1, fill=tk.X)
        # self.statusbar.fmfm.fm2.grid(row=0, column=1)

        self.statusbar.fmfm.fm2.label = tk.Label(self.statusbar.fmfm.fm2, text="A")
        self.statusbar.fmfm.fm2.label.pack(side=tk.LEFT, expand=1)

        self.statusbar.scrollbar = tk.Scrollbar(self.statusbar, orient=tk.HORIZONTAL)
        # self.statusbar.scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        # self.statusbar.scrollbar["command"] = self.statusbar.fmfm.xview

        # Create Initial Tab
        if firstfile:
            if not self.openfs(firstfile):
                first_tab = ttk.Frame(self.nb)
                doc = Document( first_tab, None )
                doc.textbox =self.create_text_widget(first_tab, doc)
                doc.Mk5()
                self.tabs[ first_tab ] = doc
                self.nb.add(first_tab, text='Untitled')
                self.UpdateStatusFile("New file buffer generated")
        else:
            first_tab = ttk.Frame(self.nb)
            doc = Document( first_tab, None )
            doc.textbox =self.create_text_widget(first_tab, doc)
            doc.Mk5()
            self.tabs[ first_tab ] = doc
            self.nb.add(first_tab, text='Untitled')
            self.UpdateStatusFile("New file buffer generated") 

        # dnd binding
        # self.nb.drop_target_register(tkdnd.DND_FILES)
        # self.nb.dnd_bind('<<Drop>>', lambda e: self.openfs( e.data.strip("{").strip("}") ))
	
        # self.nb.dnd_bind('<<Drop>>', lambda e: self.openfs(e.data))
        # self.nb.dnd_bind('<<Drop>>', lambda e: print(e))

    def create_text_widget(self, frame, document):
        # Horizontal Scroll Bar 
        xscrollbar = tk.Scrollbar(frame, orient='horizontal')
        xscrollbar.pack(side='bottom', fill='x')
        
        # Vertical Scroll Bar
        yscrollbar = tk.Scrollbar(frame)
        yscrollbar.pack(side='right', fill='y')

        # Create Text Editor Box
        textbox = tk.Text(frame, relief='sunken', borderwidth=0, wrap='none', font=self.font)
        textbox.config(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set, undo=True, autoseparators=True)

        # Keyboard / Click Bindings
        textbox.bind('<Control-s>', self.save_file)
        textbox.bind('<Control-o>', self.open_file)
        textbox.bind('<Control-n>', self.new_file)
        textbox.bind('<Control-a>', self.select_all)
        textbox.bind('<Control-w>', self.close_tab)
        textbox.bind('<Button-3>', self.right_click)
        textbox.bind('<KeyRelease>', lambda e: self.UpdateStatusMouse(textbox.index('current'), document))
        textbox.bind('<KeyPress>', lambda e: self.UpdateStatusMouse(textbox.index('current'), document))

        # drag and drop bind
        # textbox.drop_target_register(tkdnd.DND_FILES)
        # textbox.dnd_bind('<<Drop>>', lambda e: self.openfs( e.data.strip("{").strip("}") ))

        self.UpdateStatusMouse(textbox.index('current'), document)


        # Pack the textbox
        textbox.pack(fill='both', expand=True)   

        # say the new status
        # self.UpdateStatusFile("New file buffer generated")     
        
        # Configure Scrollbars
        xscrollbar.config(command=textbox.xview)
        yscrollbar.config(command=textbox.yview)
        
        return textbox

    def UpdateStatusMouse(self, mousepos, document):
        # print(mousepos)
        self.statusbar.fmfm.fm1.label["text"] = 'Line/Row: ' + mousepos.split('.')[0] + '. Charater/Column: ' + mousepos.split('.')[1] + ". Document " + str(document.file_name) + "."

    def UpdateStatusFile(self, status):
        self.statusbar.fmfm.fm2.label["text"] = "File status: " + status

    def open_file(self, *args):        
        # Open a window to browse to the file you would like to open, returns the directory.
        file_dir = (tkinter
         .filedialog
         .askopenfilename(initialdir=self.init_dir, title="Select file", filetypes=self.filetypes))

        return self.openfs(file_dir)

    def openfs(self, file_dir):
        # If directory is not the empty string, try to open the file. 
        if file_dir:
            try:
                # Open the file.
                file = open(file_dir)
                
                # Create a new tab.
                new_tab = ttk.Frame(self.nb)
                doc = Document(new_tab, None, file_dir)
                doc.textbox = self.create_text_widget(new_tab, doc)
                doc.Mk5()
                self.tabs[ new_tab ] = doc
                self.nb.add(new_tab, text=os.path.basename(file_dir))
                self.nb.select( new_tab )
                            
                # Puts the contents of the file into the text widget.
                self.tabs[ new_tab ].textbox.insert('end', file.read())
                
                # Update hash
                self.tabs[ new_tab ].status = md5(self.tabs[ new_tab ].textbox.get(1.0, 'end').encode('utf-8'))

                self.UpdateStatusFile("Opened from local filesystem")
                return True
            except Exception as e:
                self.UpdateStatusFile("Failed to open from local filesystem")
                tkmb.showerror("File open error", str(e))
                return False
        else:
            self.UpdateStatusFile("Cancled to open file from local filesystem")
            return False

    def save_as(self):
        curr_tab = self.get_tab()
    
        # Gets file directory and name of file to save.
        file_dir = (tkinter
         .filedialog
         .asksaveasfilename(initialdir=self.init_dir, title="Select file", filetypes=self.filetypes, defaultextension='.txt'))
        
        # Return if directory is still empty (user closes window without specifying file name).
        if not file_dir:
            self.UpdateStatusFile("Cancled to save file as new file")
            return
         
        # Adds .txt suffix if not already included.
        if file_dir[-4:] != '.txt':
            file_dir += '.txt'
            
        self.tabs[ curr_tab ].file_dir = file_dir
        self.tabs[ curr_tab ].file_name = os.path.basename(file_dir)
        self.nb.tab( curr_tab, text=self.tabs[ curr_tab ].file_name) 
            
        # Writes text widget's contents to file.
        file = open(file_dir, 'w')
        file.write(self.tabs[ curr_tab ].textbox.get(1.0, 'end'))
        file.close()
        
        # Update hash
        self.tabs[ curr_tab ].status = md5(self.tabs[ curr_tab ].textbox.get(1.0, 'end').encode('utf-8'))

        self.UpdateStatusFile("File saved as new file")
        
    def save_file(self, *args):
        curr_tab = self.get_tab()
        
        # If file directory is empty or Untitled, use save_as to get save information from user. 
        if not self.tabs[ curr_tab ].file_dir:
            self.save_as()

        # Otherwise save file to directory, overwriting existing file or creating a new one.
        else:
            with open(self.tabs[ curr_tab ].file_dir, 'w') as file:
                file.write(self.tabs[ curr_tab ].textbox.get(1.0, 'end'))
                
            # Update hash
            self.tabs[ curr_tab ].status = md5(self.tabs[ curr_tab ].textbox.get(1.0, 'end').encode('utf-8'))

        self.UpdateStatusFile("File saved")
                
    def new_file(self, *args):                
        # Create new tab
        new_tab = ttk.Frame(self.nb)
        doc = Document(new_tab, None)
        doc.textbox = self.create_text_widget(new_tab, doc)
        doc.Mk5()
        self.tabs[ new_tab ] = doc
        self.tabs[ new_tab ].textbox.config(wrap= 'word' if self.word_wrap.get() else 'none')
        self.nb.add(new_tab, text='Untitled')
        self.nb.select( new_tab )

        self.UpdateStatusFile("New file buffer generated")
        
    def copy(self):
        # Clears the clipboard, copies selected contents.
        try: 
            sel = self.tabs[ self.get_tab() ].textbox.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.master.clipboard_clear()
            self.master.clipboard_append(sel)
        # If no text is selected.
        except tk.TclError:
            pass
            
    def delete(self):
        # Delete the selected text.
        try:
            self.tabs[ self.get_tab() ].textbox.delete(tk.SEL_FIRST, tk.SEL_LAST)
        # If no text is selected.
        except tk.TclError:
            pass
            
    def cut(self):
        # Copies selection to the clipboard, then deletes selection.
        try: 
            sel = self.tabs[ self.get_tab() ].textbox.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.master.clipboard_clear()
            self.master.clipboard_append(sel)
            self.tabs[ self.get_tab() ].textbox.delete(tk.SEL_FIRST, tk.SEL_LAST)
        # If no text is selected.
        except tk.TclError:
            pass
            
    def wrap(self):
        if self.word_wrap.get() == True:
            for index in self.tabs:
                self.tabs[ index ].textbox.config(wrap="word")
        else:
            for index in self.tabs:
                self.tabs[ index ].textbox.config(wrap="none")
            
    def paste(self):
        try: 
            self.tabs[ self.get_tab() ].textbox.insert(tk.INSERT, self.master.clipboard_get())
        except tk.TclError:
            pass
            
    def select_all(self, *args):
        curr_tab = self.get_tab()
        
        # Selects / highlights all the text.
        self.tabs[ curr_tab ].textbox.tag_add(tk.SEL, "1.0", tk.END)
        
        # Set mark position to the end and scroll to the end of selection.
        self.tabs[ curr_tab ].textbox.mark_set(tk.INSERT, tk.END)
        self.tabs[ curr_tab ].textbox.see(tk.INSERT)

    def undo(self):
        try:
            self.tabs[ self.get_tab() ].textbox.edit_undo()
        except tk.TclError:
            tkmb.showerror("Undo Error", "There is nothing to undo!")

    def redo(self):
        try:
            self.tabs[ self.get_tab() ].textbox.edit_redo()
        except tk.TclError:
            tkmb.showerror("Redo Error", "There is nothing to redo!")

    def right_click(self, event):
        self.right_click_menu.post(event.x_root, event.y_root)
        
    def right_click_tab(self, event):
        self.tab_right_click_menu.post(event.x_root, event.y_root)
    
    def right_click_toolbar(self, event):
        self.RibbonToolbar_right_click_menu.post(event.x_root, event.y_root)
        
    def close_tab(self, event=None):
        # Close the current tab if close is selected from file menu, or keyboard shortcut.
        if event is None or event.type == str( 2 ):
            selected_tab = self.get_tab()
        # Otherwise close the tab based on coordinates of center-click.
        else:
            try:
                index = event.widget.index('@%d,%d' % (event.x, event.y))
                selected_tab = self.nb._nametowidget( self.nb.tabs()[index] )
            except tk.TclError:
                return

        # Prompt to save changes before closing tab
        if self.save_changes():
            try:
                self.nb.forget( selected_tab )
                self.tabs.pop( selected_tab )
            except KeyError:
                pass

        # Exit if last tab is closed
        if self.nb.index("end") == 0:
            self.master.destroy()
        
    def exit(self):
        status = None

        try:
            status = self.save_changes()
        except KeyError:
            status = True
        # Check if any changes have been made.
        if status:
            self.master.destroy()
        else:
            return

    def webrequest(self):
        file_dir = tksd.askstring(title="Raw url location", prompt="Where do you want to fecth the raw data?:")
        if not file_dir:
            self.UpdateStatusFile("Cancled to download file from web")
            return

        try:
            # Open the file.
            file = requests.get(file_dir).text
            
            # Create a new tab.
            new_tab = ttk.Frame(self.nb)
            doc = Document(new_tab, None, file_dir)
            doc.textbox = self.create_text_widget(new_tab, doc)
            doc.Mk5()
            self.tabs[ new_tab ] = doc
            self.nb.add(new_tab, text=os.path.basename(file_dir))
            self.nb.select( new_tab )
                        
            # Puts the contents of the file into the text widget.
            self.tabs[ new_tab ].textbox.insert('end', file)
            
            # Update hash
            self.tabs[ new_tab ].status = md5(self.tabs[ new_tab ].textbox.get(1.0, 'end').encode('utf-8'))

            self.UpdateStatusFile("File downloaded from web sucessfully")
        except Exception as e:
            self.UpdateStatusFile("File failed to download from web")
            tkmb.showerror("Webrequest error", str(e))
            return

    def LessView(self):
        file_dir = (tkfd.askopenfilename(initialdir=self.init_dir, title="Select file", filetypes=self.filetypes))
        
        # If directory is not the empty string, try to open the file. 
        if file_dir:
            # try:
                # Open the file.
                file = open(file_dir)
                text = file.read()
                file.close()
                less = LessViewer(self.master, text, self.font)
                less.resizable(False, False)
                less.mainloop()
            # except Exception as e:
            #     tkmb.showerror("Less Viewing error", str(e))
            #     pass

    def RibbonToolbar_pack(self):
        try:
            self.RibbonToolbar.pack(fill=tk.X, side=tk.TOP)
        except:
            pass

    def RibbonToolbar_unpack(self):
        try:
            self.RibbonToolbar.pack_forget()
        except:
            pass

               
    def save_changes(self):
        curr_tab = self.get_tab()
        file_dir = self.tabs[ curr_tab ].file_dir
        
        # Check if any changes have been made, returns False if user chooses to cancel rather than select to save or not.
        if md5(self.tabs[ curr_tab ].textbox.get(1.0, 'end').encode('utf-8')).digest() != self.tabs[ curr_tab ].status.digest():
            # If changes were made since last save, ask if user wants to save.
            m = tkmb.askyesnocancel('Editor', 'Do you want to save changes to ' + ('Untitled' if not file_dir else file_dir) + '?' )
            
            # If None, cancel.
            if m is None:
                return False
            # else if True, save.
            elif m is True:
                self.save_file()
            # else don't save.
            else:
                pass
                
        return True
    
    # Get the object of the current tab.
    def get_tab(self):
        return self.nb._nametowidget( self.nb.select() )
        
    def move_tab(self, event):
        '''
        Check if there is more than one tab.
        
        Use the y-coordinate of the current tab so that if the user moves the mouse up / down 
        out of the range of the tabs, the left / right movement still moves the tab.
        '''
        if self.nb.index("end") > 1:
            y = self.get_tab().winfo_y() - 5
            
            try:
                self.nb.insert( event.widget.index('@%d,%d' % (event.x, y)), self.nb.select() )
            except tk.TclError:
                return

    # About dialog with Pmw
    def showAboutDialog(self):
        Pmw.aboutversion('1.0')
        Pmw.aboutcopyright('Copyright MXPSQL 2021\nAll rights reserved')
        Pmw.aboutcontact("Visit " + str(self.srcurl) + " for more info")

        about = Pmw.AboutDialog(self.master, applicationname = "TkEdit")
        about.withdraw()
        about.show()

    # Show license
    def showLicense(self):
        text = ""

        try:
            f = open("LICENSE", "r")
            text = f.read()
            f.close()
        except FileNotFoundError:
            text = "LICENSE does not exist!"
        
        less = LessViewer(self.master, text, self.font)
        less.mainloop()


# open tkinterdnd.tk and initialize it for Pmw
win = tkdnd.TkinterDnD.Tk()
# win = tk.Tk()
Pmw.initialise(win)
# add dnd to window
win.drop_target_register(tkdnd.DND_FILES)
# make argument parser
win.argparse = argparse.ArgumentParser()
win.argparse.add_argument('-f', '--file', action='store', help="File input", dest="file", type=str, default="", metavar="\"File here\"")
win.argparse.add_argument('dfile', action='store', help="File input for drag and drop", type=str, default=None, metavar="\"Drag and drop file here\"", nargs="?")
# parse args
win.argv = sys.argv
sys.argv.pop(0)
win.args, win.unknownargs = win.argparse.parse_known_args(sys.argv)
sys.argv = win.argv
# configuration
win.asset = "asset"
win.helv36 = tkf.Font(family="Microsoft Sans Serif",size=8)
win.assetPath = os.path.join(os.getcwd(), win.asset)
win.title("TkEdit")
win.srcurl = "https://github.com/MXP2095onetechguy/TkEdit"
win.wtkstyle = wtk.Style()
win.iconphoto(True,tk.PhotoImage(file=os.path.join(win.assetPath, "TkEdit.png")))
# print(win.args)
# make editor
win.app = Editor(win, assetDir=win.asset, font=win.helv36, firstfile=win.args.file or win.args.dfile or None, srcurl=win.srcurl, wtkstyle=win.wtkstyle)
# register dnd to window
win.dnd_bind('<<Drop>>', lambda e: win.app.openfs( e.data.strip("{").strip("}") ))
# mainloop
win.mainloop()
# Exit
sys.exit(0)


