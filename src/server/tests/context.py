import os
import sys

def set_ctx(path):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), path)))

