import sys
import cx_Freeze as cxF

base = None

if sys.platform == "win32":
    base = "Win32GUI"

executables = [cxF.Executable("TkEdit.py", base=base, target_name="TkEdit.exe", icon="asset/TkEditI.ico")]

includefile = ["asset/", "LICENSE", "clearlooks/", "Pmw/", "list.txt", "awthemes/", "ttkthemes/"]

include = ["atexit"]

exclude = []

pkgmodule = ["PIL", "requests", "tkinterdnd2", "witkets", "ttkwidgets", "tksvg"]

options = {"build_exe": {"includes":include, "packages": pkgmodule, 'include_files':includefile, 'excludes': exclude}}

f = open("LICENSE", "r")
License = f.read()
f.close()
f = None

cxF.setup(
    name="TkEdit",
    version="0.1",
    url="https://mxp2095onetechguy.github.io/TkEdit/",
    license=License,
    author="MXPSQL",
    author_email="2000onetechguy@gmail.com",
    description="Tkinter (Tk) based editor. Better than Microsoft notepad",
    platforms=["Windows", "Linux", "MacOS"],
    keywords=["Tkinter", "Editor"],


    options=options,
    executables=executables,
)