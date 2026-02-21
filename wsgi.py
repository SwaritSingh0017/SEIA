import sys
import os

path = '/home/sayam/SEIA'
if path not in sys.path:
    sys.path.insert(0, path)
    
from dotenv import load_dotenv
load_dotenv(os.path.join(path, 'key.env'))

from app import app as application

