"""
Memory Display Panel
Shows memory contents
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QComboBox, QLabel, QSpinBox,
                             QPushButton, QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from core.memory import Memory


class MemoryPanel(QWidget):
    """Panel displaying memory contents"""
    
    def __init__(self, memory: Memory):
        super().__init__()
        self.memory = memory
        self.start_address = 0
        self.display_size = 64  # Show 64 bytes by default
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the memory panel UI"""
        layout = QVBoxLayout(self)
        
        # Title and controls
        header_layout = QHBoxLayout()
        title = QLabel("Memory")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Address controls
        addr_label = QLabel("Start Address:")
        header_layout.addWidget(addr_label)
        
        self.addr_spinbox = QSpinBox()
        self.addr_spinbox.setRange(0, 1024 * 1024 - 1)
        self.addr_spinbox.setValue(0)
        self.addr_spinbox.setSingleStep(4)
        self.addr_spinbox.valueChanged.connect(self.update_start_address)
        header_layout.addWidget(self.addr_spinbox)
        
        # Display format
        format_label = QLabel("Format:")
        header_layout.addWidget(format_label)
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(["Words (32-bit)", "Bytes", "Doublewords (64-bit)"])
        self.format_combo.currentTextChanged.connect(self.update_display)
        header_layout.addWidget(self.format_combo)
        
        layout.addLayout(header_layout)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.update_display)
        button_layout.addWidget(self.refresh_btn)
        
        self.goto_btn = QPushButton("Go to Address")
        self.goto_btn.clicked.connect(self.goto_address)
        button_layout.addWidget(self.goto_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Memory table
        self.memory_table = QTableWidget()
        self.memory_table.setColumnCount(3)
        self.memory_table.setHorizontalHeaderLabels(["Address", "Value (Hex)", "Value (Dec)"])
        
        # Setup table appearance
        self.memory_table.setAlternatingRowColors(True)
        self.memory_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.memory_table.setFont(QFont("Consolas", 10))
        
        # Set column widths
        header = self.memory_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        
        self.memory_table.setColumnWidth(0, 100)  # Address
        
        layout.addWidget(self.memory_table)
        
        # Memory statistics
        self.stats_label = QLabel("Memory Stats: 0 bytes used")
        self.stats_label.setFont(QFont("Arial", 9))
        layout.addWidget(self.stats_label)
        
        # Initialize display
        self.update_display()
        
    def update_start_address(self, address: int):
        """Update the starting address for memory display"""
        self.start_address = address
        self.update_display()
        
    def update_display(self):
        """Update memory display"""
        format_type = self.format_combo.currentText()
        
        if "Words" in format_type:
            self.display_words()
        elif "Doublewords" in format_type:
            self.display_doublewords()
        else:  # Bytes
            self.display_bytes()
            
        self.update_statistics()
        
    def display_words(self):
        """Display memory as 32-bit words"""
        self.memory_table.setHorizontalHeaderLabels(["Address", "Value (Hex)", "Value (Dec)"])
        
        # Calculate number of words to display (aligned to 4-byte boundaries)
        aligned_start = (self.start_address // 4) * 4
        num_words = self.display_size // 4
        
        self.memory_table.setRowCount(num_words)
        
        for i in range(num_words):
            address = aligned_start + (i * 4)
            
            try:
                value = self.memory.read_word(address)
                hex_value = f"0x{value & 0xFFFFFFFF:08X}"
                dec_value = str(value)
            except:
                hex_value = "----"
                dec_value = "----"
                
            # Address
            addr_item = QTableWidgetItem(f"0x{address:08X}")
            addr_item.setFlags(addr_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.memory_table.setItem(i, 0, addr_item)
            
            # Hex value
            hex_item = QTableWidgetItem(hex_value)
            hex_item.setFlags(hex_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            hex_item.setFont(QFont("Consolas", 10))
            self.memory_table.setItem(i, 1, hex_item)
            
            # Decimal value
            dec_item = QTableWidgetItem(dec_value)
            dec_item.setFlags(dec_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.memory_table.setItem(i, 2, dec_item)
            
                
    def display_doublewords(self):
        """Display memory as 64-bit doublewords"""
        self.memory_table.setHorizontalHeaderLabels(["Address", "Value (Hex)", "Value (Dec)"])
        
        # Calculate number of doublewords to display (aligned to 8-byte boundaries)
        aligned_start = (self.start_address // 8) * 8
        num_doublewords = self.display_size // 8
        
        self.memory_table.setRowCount(num_doublewords)
        
        for i in range(num_doublewords):
            address = aligned_start + (i * 8)
            
            try:
                value = self.memory.read_doubleword(address)
                hex_value = f"0x{value & 0xFFFFFFFFFFFFFFFF:016X}"
                dec_value = str(value)
            except:
                hex_value = "----"
                dec_value = "----"
                
            # Address
            addr_item = QTableWidgetItem(f"0x{address:08X}")
            addr_item.setFlags(addr_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.memory_table.setItem(i, 0, addr_item)
            
            # Hex value
            hex_item = QTableWidgetItem(hex_value)
            hex_item.setFlags(hex_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            hex_item.setFont(QFont("Consolas", 10))
            self.memory_table.setItem(i, 1, hex_item)
            
            # Decimal value
            dec_item = QTableWidgetItem(dec_value)
            dec_item.setFlags(dec_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.memory_table.setItem(i, 2, dec_item)
            
                
    def display_bytes(self):
        """Display memory as individual bytes"""
        self.memory_table.setHorizontalHeaderLabels(["Address", "Value (Hex)", "Value (Dec)"])
        
        self.memory_table.setRowCount(self.display_size)
        
        for i in range(self.display_size):
            address = self.start_address + i
            
            try:
                value = self.memory.read_byte(address)
                hex_value = f"0x{value:02X}"
                dec_value = str(value)
            except:
                hex_value = "--"
                dec_value = "--"
                
            # Address
            addr_item = QTableWidgetItem(f"0x{address:08X}")
            addr_item.setFlags(addr_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.memory_table.setItem(i, 0, addr_item)
            
            # Hex value
            hex_item = QTableWidgetItem(hex_value)
            hex_item.setFlags(hex_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            hex_item.setFont(QFont("Consolas", 10))
            self.memory_table.setItem(i, 1, hex_item)
            
            # Decimal value
            dec_item = QTableWidgetItem(dec_value)
            dec_item.setFlags(dec_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.memory_table.setItem(i, 2, dec_item)
            
            
    def update_statistics(self):
        """Update memory usage statistics"""
        used_addresses = self.memory.get_used_addresses()
        bytes_used = len(used_addresses)
        
        if bytes_used > 0:
            min_addr = min(used_addresses)
            max_addr = max(used_addresses)
            span = max_addr - min_addr + 1
            self.stats_label.setText(
                f"Memory Stats: {bytes_used} bytes used, "
                f"Range: 0x{min_addr:X} - 0x{max_addr:X} (span: {span} bytes)"
            )
        else:
            self.stats_label.setText("Memory Stats: 0 bytes used")
            
    def goto_address(self):
        """Go to a specific memory address"""
        # For now, just go to the current spinbox value
        self.start_address = self.addr_spinbox.value()
        self.update_display()
        
    def goto_used_memory(self):
        """Go to first used memory location"""
        used_addresses = self.memory.get_used_addresses()
        if used_addresses:
            first_used = min(used_addresses)
            self.addr_spinbox.setValue(first_used)
            self.start_address = first_used
            self.update_display()
