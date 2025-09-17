#!/usr/bin/env python3
"""
PyLEGv8 - Python-based LEGv8 Assembly Simulator
Main application entry point
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("PyLEGv8 Simulator")
    app.setApplicationVersion("0.1.0")
    app.setOrganizationName("PyLEGv8")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
