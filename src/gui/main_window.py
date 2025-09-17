"""
Main Window for PyLEGv8 Simulator
Contains the primary interface with code editor, register display, and controls
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                             QSplitter, QPushButton, QMenuBar, QToolBar, 
                             QStatusBar, QMessageBox, QTextEdit)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction, QFont

from gui.code_editor import CodeEditor
from gui.register_panel import RegisterPanel
from gui.memory_panel import MemoryPanel
from gui.help_dialog import HelpDialog
from core.cpu import LEGv8CPU
from parser.assembly_parser import AssemblyParser


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.cpu = LEGv8CPU()
        self.parser = AssemblyParser()
        self.compiled_instructions = []
        self.current_instruction_index = 0
        
        self.init_ui()
        self.setup_timer()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("PyLEGv8 - LEGv8 Assembly Simulator")
        self.setMinimumSize(1200, 800)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left panel: Code editor and controls
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # Right panel: Register and memory display
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # Set initial splitter sizes (60% left, 40% right)
        splitter.setSizes([720, 480])
        
        # Create menu bar and toolbar
        self.create_menus()
        self.create_toolbar()
        self.create_status_bar()
        
    def create_left_panel(self) -> QWidget:
        """Create the left panel with code editor and controls"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Code editor
        self.code_editor = CodeEditor()
        layout.addWidget(self.code_editor)
        
        # Control buttons
        controls_layout = QHBoxLayout()
        
        self.compile_btn = QPushButton("Compile")
        self.compile_btn.clicked.connect(self.compile_code)
        controls_layout.addWidget(self.compile_btn)
        
        self.step_btn = QPushButton("Step")
        self.step_btn.clicked.connect(self.step_execution)
        self.step_btn.setEnabled(False)
        controls_layout.addWidget(self.step_btn)
        
        self.run_btn = QPushButton("Run All")
        self.run_btn.clicked.connect(self.run_all)
        self.run_btn.setEnabled(False)
        controls_layout.addWidget(self.run_btn)
        
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self.reset_simulation)
        controls_layout.addWidget(self.reset_btn)
        
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
        # Console output
        self.console = QTextEdit()
        self.console.setMaximumHeight(150)
        self.console.setReadOnly(True)
        self.console.setFont(QFont("Consolas", 10))
        layout.addWidget(self.console)
        
        return panel
        
    def create_right_panel(self) -> QWidget:
        """Create the right panel with register and memory displays"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Create splitter for register and memory panels
        right_splitter = QSplitter(Qt.Orientation.Vertical)
        layout.addWidget(right_splitter)
        
        # Register panel
        self.register_panel = RegisterPanel(self.cpu.registers)
        right_splitter.addWidget(self.register_panel)
        
        # Memory panel
        self.memory_panel = MemoryPanel(self.cpu.memory)
        right_splitter.addWidget(self.memory_panel)
        
        # Set initial sizes (60% registers, 40% memory)
        right_splitter.setSizes([300, 200])
        
        return panel
        
    def create_menus(self):
        """Create menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        new_action = QAction("New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        open_action = QAction("Open...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Simulation menu
        sim_menu = menubar.addMenu("Simulation")
        
        compile_action = QAction("Compile", self)
        compile_action.setShortcut("F5")
        compile_action.triggered.connect(self.compile_code)
        sim_menu.addAction(compile_action)
        
        step_action = QAction("Step", self)
        step_action.setShortcut("F10")
        step_action.triggered.connect(self.step_execution)
        sim_menu.addAction(step_action)
        
        run_action = QAction("Run All", self)
        run_action.setShortcut("F9")
        run_action.triggered.connect(self.run_all)
        sim_menu.addAction(run_action)
        
        reset_action = QAction("Reset", self)
        reset_action.setShortcut("F6")
        reset_action.triggered.connect(self.reset_simulation)
        sim_menu.addAction(reset_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        help_action = QAction("LEGv8 Reference", self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def create_toolbar(self):
        """Create toolbar"""
        toolbar = self.addToolBar("Main")
        
        toolbar.addAction("Compile", self.compile_code)
        toolbar.addAction("Step", self.step_execution)
        toolbar.addAction("Run", self.run_all)
        toolbar.addAction("Reset", self.reset_simulation)
        toolbar.addSeparator()
        toolbar.addAction("Help", self.show_help)
        
    def create_status_bar(self):
        """Create status bar"""
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")
        
    def setup_timer(self):
        """Setup timer for register flash effects"""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_displays)
        self.update_timer.start(100)  # Update every 100ms
        
    def compile_code(self):
        """Compile the assembly code"""
        try:
            code = self.code_editor.toPlainText()
            self.compiled_instructions = self.parser.parse(code)
            
            if self.compiled_instructions:
                # Reset CPU state for fresh execution
                self.cpu.reset()
                self.update_displays()  # Update UI to show reset state
                
                self.console.append(f"✓ Compiled successfully: {len(self.compiled_instructions)} instructions")
                self.console.append("✓ CPU state reset - ready for execution")
                self.step_btn.setEnabled(True)
                self.run_btn.setEnabled(True)
                self.current_instruction_index = 0
                
                # Highlight first instruction
                if self.compiled_instructions:
                    first_line = self.compiled_instructions[0].line_number
                    self.code_editor.highlight_current_line(first_line)
            else:
                self.console.append("⚠ No instructions found")
                
        except Exception as e:
            error_message = str(e)
            if '\n' in error_message:
                # Multiple errors - show them nicely formatted
                self.console.append("✗ Compilation errors found:")
                for line in error_message.split('\n'):
                    self.console.append(f"  {line}")
            else:
                # Single error
                self.console.append(f"✗ Compilation error: {error_message}")
            self.step_btn.setEnabled(False)
            self.run_btn.setEnabled(False)
            
    def step_execution(self):
        """Execute one instruction step"""
        if (self.current_instruction_index >= len(self.compiled_instructions) or 
            self.cpu.is_halted):
            self.console.append("Execution complete")
            return False  # Return False to indicate execution should stop
            
        try:
            instruction = self.compiled_instructions[self.current_instruction_index]
            result = self.cpu.step(instruction)
            
            if "error" in result:
                self.console.append(f"✗ Runtime error: {result['error']}")
                return False  # Return False to indicate execution should stop
                
            # Log execution
            self.console.append(f"PC={result['pc']:04X}: {instruction}")
            
            # Update displays
            self.update_displays()
            
            # Determine next instruction based on PC value
            new_pc = result['pc']
            next_instruction_index = new_pc // 4  # Each instruction is 4 bytes
            
            # Check if we're still within the program bounds
            if 0 <= next_instruction_index < len(self.compiled_instructions):
                self.current_instruction_index = next_instruction_index
                next_instruction = self.compiled_instructions[next_instruction_index]
                line_num = next_instruction.line_number
                self.code_editor.highlight_current_line(line_num)
                return True  # Continue execution
            else:
                # Program counter is beyond our instructions - program completed
                self.code_editor.clear_highlight()
                self.console.append("✓ Program completed")
                self.cpu.is_halted = True  # Halt the CPU
                return False  # Return False to indicate execution should stop
                
        except Exception as e:
            self.console.append(f"✗ Execution error: {str(e)}")
            return False  # Return False to indicate execution should stop
            
    def run_all(self):
        """Run all remaining instructions"""
        max_instructions = 10000  # Prevent infinite loops
        count = 0
        
        # Continue execution until program completes or hits limits
        while count < max_instructions:
            # Call step_execution and check if we should continue
            try:
                should_continue = self.step_execution()
                if not should_continue:
                    # Program completed normally or encountered an error
                    break
                count += 1
            except Exception as e:
                self.console.append(f"✗ Execution error during run all: {str(e)}")
                break
            
        if count >= max_instructions:
            self.console.append("⚠ Execution stopped: maximum instruction limit reached")
            
    def reset_simulation(self):
        """Reset the simulation to initial state"""
        self.cpu.reset()
        self.current_instruction_index = 0
        self.step_btn.setEnabled(bool(self.compiled_instructions))
        self.run_btn.setEnabled(bool(self.compiled_instructions))
        
        # Highlight first instruction if we have compiled instructions
        if self.compiled_instructions:
            first_line = self.compiled_instructions[0].line_number
            self.code_editor.highlight_current_line(first_line)
        else:
            self.code_editor.clear_highlight()
            
        self.console.append("✓ Simulation reset - all registers and memory cleared")
        self.update_displays()
        
    def update_displays(self):
        """Update register and memory displays"""
        self.register_panel.update_display()
        self.memory_panel.update_display()
        
    def new_file(self):
        """Create new file"""
        self.code_editor.clear()
        self.reset_simulation()
        
    def open_file(self):
        """Open assembly file"""
        # TODO: Implement file dialog
        pass
        
    def save_file(self):
        """Save assembly file"""
        # TODO: Implement file dialog
        pass
        
    def show_help(self):
        """Show help dialog"""
        dialog = HelpDialog(self)
        dialog.exec()
        
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About PyLEGv8", 
                         "PyLEGv8 - LEGv8 Assembly Simulator\\n"
                         "Version 0.1.0\\n\\n"
                         "A Python-based simulator for the LEGv8 instruction set.")
