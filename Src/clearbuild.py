import shutil
import sys
import os

print("RMTree build directories script")

print("Running script")

print("Geting current working directory")
cwd = os.getcwd()

print("Running shutil.rmtree")
try:
    print("RMTree build")
    shutil.rmtree(os.path.join(cwd,"build"))
except FileNotFoundError as e:
    print("FileNotFoundError: " + str(e))

try:
    print("RMTree build")
    shutil.rmtree(os.path.join(cwd, "dist"))
except FileNotFoundError as e:
    print("FileNotFoundError: " + str(e))

print("All done, exiting")

sys.exit(0)