# This file should trigger S004 in the linter tool

import subprocess

subprocess.run("dir", shell=True)
