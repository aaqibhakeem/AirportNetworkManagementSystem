import sys, os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, 
                               QStackedWidget, QLabel, QLineEdit, QFormLayout, 
                               QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout,
                               QComboBox, QSpinBox, QGraphicsView, QTextEdit, QStyle, QGraphicsDropShadowEffect)
from PySide6.QtGui import QIcon, QColor, QPixmap, QPainter, QPen, QBrush
from PySide6.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QSize, QTimer, QPoint,QParallelAnimationGroup
from src.utils.crud import CRUDOperations
from src.utils.graph import load_airport_coordinates, create_graph_from_airports, draw_graph, ShortestPathAlgorithms, ask_add_route_to_db
import mysql.connector
import plotly