import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, 
                               QStackedWidget, QLabel, QLineEdit, QFormLayout, 
                               QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout,
                               QComboBox, QSpinBox, QGraphicsView, QTextEdit)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QSize, QTimer, QPoint
from src.crud import CRUDOperations
from src.graph import load_airport_coordinates, create_graph_from_airports, draw_graph, ShortestPathAlgorithms, ask_add_route_to_db
import mysql.connector
import plotly