import telebot
import json
from datetime import datetime
import time
import os

TOKEN = '6040239312:AAH-fFssTQKU3t-aFMB1j87KrlhlTrkT8Z8'
DOWNLOAD_DIR = 'C:\\Users\\mosvo\\Documents\\programming\\tg_bot_waitlist\\models\\'

EXTNESIONS = ['.stl', '.stp', '.step', '.3mf', '.a3d', '.m3d', '.gcode']

DEFAULT_STATUS = 'НЕ НАЧАТО'
