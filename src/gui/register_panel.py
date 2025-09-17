"""
Register Display Panel
Shows the current state of all LEGv8 registers
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QComboBox, QLabel, QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from core.registers import RegisterFile


class RegisterPanel(QWidget):
    """Panel displaying LEGv8 registers"""
    
    def __init__(self, register_file: RegisterFile):
        super().__init__()
        self.register_file = register_file
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the register panel UI"""
        layout = QVBoxLayout(self)
        
        # Title and controls
        header_layout = QHBoxLayout()
        title = QLabel("Registers")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Number base selection
        base_label = QLabel("Display:")
        header_layout.addWidget(base_label)
        
        self.base_combo = QComboBox()
        self.base_combo.addItems(["Decimal", "Hexadecimal", "Binary"])
        self.base_combo.currentTextChanged.connect(self.update_display)
        header_layout.addWidget(self.base_combo)
        
        layout.addLayout(header_layout)
        
        # Register table
        self.register_table = QTableWidget()
        self.register_table.setColumnCount(3)
        self.register_table.setHorizontalHeaderLabels(["Register", "Value", "Description"])
        
        # Setup table appearance
        self.register_table.setAlternatingRowColors(True)
        self.register_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.register_table.setFont(QFont("Consolas", 10))
        
        # Set column widths
        header = self.register_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        
        self.register_table.setColumnWidth(0, 80)  # Register name
        self.register_table.setColumnWidth(2, 100) # Description
        
        layout.addWidget(self.register_table)
        
        # Initialize register display
        self.setup_register_table()
        self.update_display()
        
    def setup_register_table(self):
        """Setup the register table with all registers"""
        register_names = self.register_file.get_register_names()
        self.register_table.setRowCount(len(register_names))
        
        descriptions = [
            "General Purpose",  # X0
            "General Purpose",  # X1
            "General Purpose",  # X2
            "General Purpose",  # X3
            "General Purpose",  # X4
            "General Purpose",  # X5
            "General Purpose",  # X6
            "General Purpose",  # X7
            "General Purpose",  # X8
            "General Purpose",  # X9
            "General Purpose",  # X10
            "General Purpose",  # X11
            "General Purpose",  # X12
            "General Purpose",  # X13
            "General Purpose",  # X14
            "General Purpose",  # X15
            "General Purpose",  # X16
            "General Purpose",  # X17
            "General Purpose",  # X18
            "General Purpose",  # X19
            "General Purpose",  # X20
            "General Purpose",  # X21
            "General Purpose",  # X22
            "General Purpose",  # X23
            "General Purpose",  # X24
            "General Purpose",  # X25
            "General Purpose",  # X26
            "General Purpose",  # X27
            "Stack Pointer",    # X28 (SP)
            "Frame Pointer",    # X29 (FP)
            "Link Register",    # X30 (LR)
            "Zero Register"     # X31 (XZR)
        ]
        
        for i, (name, desc) in enumerate(zip(register_names, descriptions)):
            # Register name
            name_item = QTableWidgetItem(name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.register_table.setItem(i, 0, name_item)
            
            # Value (will be updated in update_display)
            value_item = QTableWidgetItem("0")
            value_item.setFlags(value_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            value_item.setFont(QFont("Consolas", 10))
            self.register_table.setItem(i, 1, value_item)
            
            # Description
            desc_item = QTableWidgetItem(desc)
            desc_item.setFlags(desc_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.register_table.setItem(i, 2, desc_item)
            
    def update_display(self):
        """Update register display with current values"""
        register_values = self.register_file.get_all()
        base = self.base_combo.currentText()
        
        for i, value in enumerate(register_values):
            # Format value based on selected base
            if base == "Hexadecimal":
                formatted_value = f"0x{value & 0xFFFFFFFFFFFFFFFF:016X}"
            elif base == "Binary":
                formatted_value = f"0b{value & 0xFFFFFFFFFFFFFFFF:064b}"
            else:  # Decimal
                formatted_value = str(value)
                
            # Update table item
            item = self.register_table.item(i, 1)
            if item:
                item.setText(formatted_value)
                
    def get_register_info(self, register_num: int) -> dict:
        """Get detailed information about a specific register"""
        if not (0 <= register_num <= 31):
            return {}
            
        value = self.register_file.read(register_num)
        name = self.register_file.get_register_names()[register_num]
        
        return {
            "name": name,
            "number": register_num,
            "value": value,
            "hex": f"0x{value & 0xFFFFFFFFFFFFFFFF:016X}",
            "binary": f"0b{value & 0xFFFFFFFFFFFFFFFF:064b}",
            "recently_modified": False  # Flash functionality removed
        }
