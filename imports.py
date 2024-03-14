#BACKENDS
import os
import math
import subprocess
import platform
import psutil
import sys

#numba optimizer
# from numba import njit





#OPTIMIZER

import numpy as np
from collections import Counter
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, COIN_CMD, value

#PYQT

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTabWidget,
    QTableWidget,
    QHeaderView,
    QTableWidgetItem,
    QCheckBox,
    QGroupBox,
    QLineEdit,
    QGridLayout,
    QFormLayout,
    QScrollArea,
    QItemDelegate,
    QDoubleSpinBox,
    QMessageBox
)
from PyQt6.QtGui import QFont, QDoubleValidator, QGuiApplication
from PyQt6.QtCore import Qt, pyqtSignal
#files
from setup import *
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "feed_gui.settings")
import django
django.setup()
from feed.models import Feed, Fomular
from django.shortcuts import get_object_or_404

from backend import *
from gui import *



