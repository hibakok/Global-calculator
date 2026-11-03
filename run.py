# Точка запуска Global Calculator: python run.py

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from branch_9_console import main

main()