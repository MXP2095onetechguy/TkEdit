import sys
import cx_Freeze as cxF

base = None

if sys.platform == "win32":
    base = "Win32GUI"

executables = [cxF.Executable("TkEdit.py", base=base, target_name="TkEdit.exe", icon="asset/TkEditI.ico")]

includefile = ["asset/", "LICENSE"]

include = ["atexit"]

exclude = []

pkgmodule = ["PIL", "requests"]

options = {"build_exe": {"includes":include, "packages": pkgmodule, 'include_files':includefile, 'excludes': exclude}}

cxF.setup(
    name="TkEdit",
    version="0.1",
    description="Tkinter (Tk) based editor. Better than Microsoft notepad",
    options=options,
    executables=executables,
)