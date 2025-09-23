"""
Help Dialog with LEGv8 Instruction Reference and Examples
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
                             QTextEdit, QTreeWidget, QTreeWidgetItem, QSplitter,
                             QPushButton, QLabel)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class HelpDialog(QDialog):
    """Help dialog with instruction reference and examples"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("LEGv8 Reference - PyLEGv8 Help")
        self.setMinimumSize(900, 700)
        
        self.init_ui()
        self.populate_content()
        
    def init_ui(self):
        """Initialize the help dialog UI"""
        layout = QVBoxLayout(self)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Instruction reference tab
        self.create_instruction_tab()
        
        # Examples tab
        self.create_examples_tab()
        
        # Quick reference tab
        self.create_quick_ref_tab()
        
        # Close button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
    def create_instruction_tab(self):
        """Create instruction reference tab"""
        tab = QSplitter(Qt.Orientation.Horizontal)
        
        # Instruction tree
        self.instruction_tree = QTreeWidget()
        self.instruction_tree.setHeaderLabel("Instructions")
        self.instruction_tree.itemClicked.connect(self.on_instruction_selected)
        tab.addWidget(self.instruction_tree)
        
        # Instruction details
        self.instruction_details = QTextEdit()
        self.instruction_details.setReadOnly(True)
        self.instruction_details.setFont(QFont("Consolas", 10))
        tab.addWidget(self.instruction_details)
        
        # Set initial splitter sizes
        tab.setSizes([250, 650])
        
        self.tab_widget.addTab(tab, "Instructions")
        
    def create_examples_tab(self):
        """Create examples tab"""
        tab = QSplitter(Qt.Orientation.Horizontal)
        
        # Example tree
        self.example_tree = QTreeWidget()
        self.example_tree.setHeaderLabel("Examples")
        self.example_tree.itemClicked.connect(self.on_example_selected)
        tab.addWidget(self.example_tree)
        
        # Example code
        self.example_code = QTextEdit()
        self.example_code.setReadOnly(True)
        self.example_code.setFont(QFont("Consolas", 10))
        tab.addWidget(self.example_code)
        
        # Set initial splitter sizes
        tab.setSizes([250, 650])
        
        self.tab_widget.addTab(tab, "Examples")
        
    def create_quick_ref_tab(self):
        """Create quick reference tab"""
        tab = QTextEdit()
        tab.setReadOnly(True)
        tab.setFont(QFont("Consolas", 10))
        
        self.tab_widget.addTab(tab, "Quick Reference")
        self.quick_ref_text = tab
        
    def populate_content(self):
        """Populate help content"""
        self.populate_instructions()
        self.populate_examples()
        self.populate_quick_reference()
        
    def populate_instructions(self):
        """Populate instruction reference"""
        instructions_data = {
            "Arithmetic Instructions": {
                "ADD": {
                    "syntax": "ADD Rd, Rn, Rm",
                    "description": "Add two registers",
                    "example": "ADD X1, X2, X3  // X1 = X2 + X3",
                    "operation": "Rd = Rn + Rm"
                },
                "ADDS": {
                    "syntax": "ADDS Rd, Rn, Rm",
                    "description": "Add two registers (sets flags)",
                    "example": "ADDS X1, X2, X3  // X1 = X2 + X3, set flags",
                    "operation": "Rd = Rn + Rm (with flags)"
                },
                "SUB": {
                    "syntax": "SUB Rd, Rn, Rm",
                    "description": "Subtract two registers",
                    "example": "SUB X1, X2, X3  // X1 = X2 - X3",
                    "operation": "Rd = Rn - Rm"
                },
                "SUBS": {
                    "syntax": "SUBS Rd, Rn, Rm",
                    "description": "Subtract two registers (sets flags)",
                    "example": "SUBS X1, X2, X3  // X1 = X2 - X3, set flags",
                    "operation": "Rd = Rn - Rm (with flags)"
                },
                "MUL": {
                    "syntax": "MUL Rd, Rn, Rm",
                    "description": "Multiply two registers (lower 64 bits of 128-bit product)",
                    "example": "MUL X1, X2, X3  // X1 = lower 64 bits of X2 * X3",
                    "operation": "Rd = (Rn * Rm) & 0xFFFFFFFFFFFFFFFF"
                },
                "SMULH": {
                    "syntax": "SMULH Rd, Rn, Rm",
                    "description": "Signed multiply high (upper 64 bits of 128-bit signed product)",
                    "example": "SMULH X1, X2, X3  // X1 = upper 64 bits of signed X2 * X3",
                    "operation": "Rd = (signed Rn * signed Rm) >> 64"
                },
                "UMULH": {
                    "syntax": "UMULH Rd, Rn, Rm",
                    "description": "Unsigned multiply high (upper 64 bits of 128-bit unsigned product)",
                    "example": "UMULH X1, X2, X3  // X1 = upper 64 bits of unsigned X2 * X3",
                    "operation": "Rd = (unsigned Rn * unsigned Rm) >> 64"
                },
                "SDIV": {
                    "syntax": "SDIV Rd, Rn, Rm",
                    "description": "Signed divide (treating operands as signed integers)",
                    "example": "SDIV X1, X2, X3  // X1 = X2 / X3 (signed division)",
                    "operation": "Rd = signed Rn / signed Rm (throws error if Rm = 0)"
                },
                "UDIV": {
                    "syntax": "UDIV Rd, Rn, Rm",
                    "description": "Unsigned divide (treating operands as unsigned integers)",
                    "example": "UDIV X1, X2, X3  // X1 = X2 / X3 (unsigned division)",
                    "operation": "Rd = unsigned Rn / unsigned Rm (throws error if Rm = 0)"
                },
                "CMP": {
                    "syntax": "CMP Rn, Rm",
                    "description": "Compare two registers (sets flags, no result stored)",
                    "example": "CMP X1, X2  // Compare X1 and X2, set flags for conditional branches",
                    "operation": "Sets flags based on Rn - Rm (like SUBS but no destination)"
                },
                "CMPI": {
                    "syntax": "CMPI Rn, #imm",
                    "description": "Compare register with immediate (sets flags, no result stored)",
                    "example": "CMPI X1, #10  // Compare X1 with 10, set flags for conditional branches",
                    "operation": "Sets flags based on Rn - immediate (like SUBIS but no destination)"
                },
                "ADDI": {
                    "syntax": "ADDI Rd, Rn, #imm",
                    "description": "Add immediate to register",
                    "example": "ADDI X1, X2, #100  // X1 = X2 + 100",
                    "operation": "Rd = Rn + immediate"
                },
                "SUBI": {
                    "syntax": "SUBI Rd, Rn, #imm",
                    "description": "Subtract immediate from register",
                    "example": "SUBI X1, X2, #50  // X1 = X2 - 50",
                    "operation": "Rd = Rn - immediate"
                },
                "MOVZ": {
                    "syntax": "MOVZ Rd, #imm",
                    "description": "Move immediate, zero other bits",
                    "example": "MOVZ X1, #100  // X1 = 100",
                    "operation": "Rd = immediate"
                },
                "MOVK": {
                    "syntax": "MOVK Rd, #imm",
                    "description": "Move immediate, keep other bits",
                    "example": "MOVK X1, #255  // X1 = (X1 & 0xFFFF0000) | 255",
                    "operation": "Rd = (Rd & ~0xFFFF) | immediate"
                },
                "ADDIS": {
                    "syntax": "ADDIS Rd, Rn, #imm",
                    "description": "Add immediate and set flags",
                    "example": "ADDIS X1, X2, #100  // X1 = X2 + 100, set flags",
                    "operation": "Rd = Rn + immediate (with flags)"
                },
                "SUBIS": {
                    "syntax": "SUBIS Rd, Rn, #imm",
                    "description": "Subtract immediate and set flags",
                    "example": "SUBIS X1, X2, #50  // X1 = X2 - 50, set flags",
                    "operation": "Rd = Rn - immediate (with flags)"
                }
            },
            "Logical Instructions": {
                "AND": {
                    "syntax": "AND Rd, Rn, Rm",
                    "description": "Bitwise AND of two registers",
                    "example": "AND X1, X2, X3  // X1 = X2 & X3",
                    "operation": "Rd = Rn AND Rm"
                },
                "ORR": {
                    "syntax": "ORR Rd, Rn, Rm",
                    "description": "Bitwise OR of two registers",
                    "example": "ORR X1, X2, X3  // X1 = X2 | X3",
                    "operation": "Rd = Rn OR Rm"
                },
                "EOR": {
                    "syntax": "EOR Rd, Rn, Rm",
                    "description": "Bitwise XOR of two registers",
                    "example": "EOR X1, X2, X3  // X1 = X2 ^ X3",
                    "operation": "Rd = Rn XOR Rm"
                },
                "ANDI": {
                    "syntax": "ANDI Rd, Rn, #imm",
                    "description": "Bitwise AND with immediate",
                    "example": "ANDI X1, X2, #255  // X1 = X2 & 255",
                    "operation": "Rd = Rn AND immediate"
                },
                "ORRI": {
                    "syntax": "ORRI Rd, Rn, #imm",
                    "description": "Bitwise OR with immediate",
                    "example": "ORRI X1, X2, #15  // X1 = X2 | 15",
                    "operation": "Rd = Rn OR immediate"
                },
                "EORI": {
                    "syntax": "EORI Rd, Rn, #imm",
                    "description": "Bitwise XOR with immediate",
                    "example": "EORI X1, X2, #255  // X1 = X2 ^ 255",
                    "operation": "Rd = Rn XOR immediate"
                }
            },
            "Shift Instructions": {
                "LSL": {
                    "syntax": "LSL Rd, Rn, Rm",
                    "description": "Logical shift left",
                    "example": "LSL X1, X2, X3  // X1 = X2 << X3",
                    "operation": "Rd = Rn << Rm"
                },
                "LSR": {
                    "syntax": "LSR Rd, Rn, Rm",
                    "description": "Logical shift right",
                    "example": "LSR X1, X2, X3  // X1 = X2 >> X3",
                    "operation": "Rd = Rn >> Rm"
                }
            },
            "Data Transfer Instructions": {
                "LDUR": {
                    "syntax": "LDUR Rt, [Rn, #offset]",
                    "description": "Load doubleword (64-bit) from memory",
                    "example": "LDUR X1, [X2, #8]  // X1 = memory[X2 + 8]",
                    "operation": "Rt = Memory[Rn + offset]"
                },
                "STUR": {
                    "syntax": "STUR Rt, [Rn, #offset]",
                    "description": "Store doubleword (64-bit) to memory",
                    "example": "STUR X1, [X2, #8]  // memory[X2 + 8] = X1",
                    "operation": "Memory[Rn + offset] = Rt"
                },
                "LDURW": {
                    "syntax": "LDURW Rt, [Rn, #offset]",
                    "description": "Load word (32-bit) from memory",
                    "example": "LDURW X1, [X2, #4]  // X1 = memory[X2 + 4] (32-bit)",
                    "operation": "Rt = Memory[Rn + offset] (32-bit)"
                },
                "STURW": {
                    "syntax": "STURW Rt, [Rn, #offset]",
                    "description": "Store word (32-bit) to memory",
                    "example": "STURW X1, [X2, #4]  // memory[X2 + 4] = X1 (32-bit)",
                    "operation": "Memory[Rn + offset] = Rt (32-bit)"
                },
                "LDURB": {
                    "syntax": "LDURB Rt, [Rn, #offset]",
                    "description": "Load byte (8-bit) from memory",
                    "example": "LDURB X1, [X2, #1]  // X1 = memory[X2 + 1] (8-bit)",
                    "operation": "Rt = Memory[Rn + offset] (8-bit)"
                },
                "STURB": {
                    "syntax": "STURB Rt, [Rn, #offset]",
                    "description": "Store byte (8-bit) to memory",
                    "example": "STURB X1, [X2, #1]  // memory[X2 + 1] = X1 (8-bit)",
                    "operation": "Memory[Rn + offset] = Rt (8-bit)"
                }
            },
            "Branch Instructions": {
                "B": {
                    "syntax": "B label",
                    "description": "Unconditional branch to label",
                    "example": "B loop  // Jump to 'loop' label",
                    "operation": "PC = label address"
                },
                "BL": {
                    "syntax": "BL label",
                    "description": "Branch and link - call a function",
                    "example": "BL my_function  // Call function, save return address in LR (X30)",
                    "operation": "LR = PC + 4, PC = label address"
                },
                "BR": {
                    "syntax": "BR Xn",
                    "description": "Branch to register - return from function",
                    "example": "BR X30  // Return from function using Link Register",
                    "operation": "PC = Xn"
                },
                "CBZ": {
                    "syntax": "CBZ Rt, label",
                    "description": "Branch if register is zero",
                    "example": "CBZ X1, end  // Jump to 'end' if X1 == 0",
                    "operation": "if (Rt == 0) PC = label"
                },
                "CBNZ": {
                    "syntax": "CBNZ Rt, label",
                    "description": "Branch if register is not zero",
                    "example": "CBNZ X1, loop  // Jump to 'loop' if X1 != 0",
                    "operation": "if (Rt != 0) PC = label"
                },
                "B.EQ": {
                    "syntax": "B.EQ label",
                    "description": "Branch if equal (zero flag set)",
                    "example": "B.EQ equal  // Jump if last comparison was equal",
                    "operation": "if (Z == 1) PC = label"
                },
                "B.NE": {
                    "syntax": "B.NE label",
                    "description": "Branch if not equal (zero flag clear)",
                    "example": "B.NE loop  // Jump if last comparison was not equal",
                    "operation": "if (Z == 0) PC = label"
                },
                "B.LT": {
                    "syntax": "B.LT label",
                    "description": "Branch if less than (signed)",
                    "example": "B.LT negative  // Jump if last comparison was less than",
                    "operation": "if (N != V) PC = label"
                },
                "B.GE": {
                    "syntax": "B.GE label",
                    "description": "Branch if greater than or equal (signed)",
                    "example": "B.GE positive  // Jump if last comparison was >= 0",
                    "operation": "if (N == V) PC = label"
                },
                "B.GT": {
                    "syntax": "B.GT label",
                    "description": "Branch if greater than (signed)",
                    "example": "B.GT positive  // Jump if last comparison was > 0",
                    "operation": "if (!Z && N == V) PC = label"
                },
                "B.LE": {
                    "syntax": "B.LE label",
                    "description": "Branch if less than or equal (signed)",
                    "example": "B.LE nonpositive  // Jump if last comparison was <= 0",
                    "operation": "if (Z || N != V) PC = label"
                }
            },
            "Condition Flags": {
                "N Flag": {
                    "syntax": "N (Negative Flag)",
                    "description": "Set when result is negative (bit 63 = 1)",
                    "example": "SUBS X1, X2, X3  // Sets N if X2 - X3 < 0",
                    "operation": "N = 1 if result < 0, else 0"
                },
                "Z Flag": {
                    "syntax": "Z (Zero Flag)",
                    "description": "Set when result equals zero",
                    "example": "SUBS X1, X2, X2  // Sets Z since X2 - X2 = 0",
                    "operation": "Z = 1 if result == 0, else 0"
                },
                "V Flag": {
                    "syntax": "V (Overflow Flag)",
                    "description": "Set when signed arithmetic overflow occurs",
                    "example": "ADDS X1, X2, X3  // Sets V on signed overflow",
                    "operation": "V = 1 if signed overflow, else 0 (simplified)"
                },
                "C Flag": {
                    "syntax": "C (Carry Flag)",
                    "description": "Set when unsigned arithmetic produces carry",
                    "example": "ADDS X1, X2, X3  // Sets C on unsigned overflow",
                    "operation": "C = 1 if unsigned carry, else 0 (simplified)"
                },
                "Flag Usage": {
                    "syntax": "Using Flags with Branches",
                    "description": "Conditional branches test flag combinations",
                    "example": "SUBS X1, X2, X3; B.EQ equal  // Branch if X2 == X3",
                    "operation": "Flag-setting instructions: ADDS, SUBS, ADDIS, SUBIS"
                }
            }
        }
        
        for category, instructions in instructions_data.items():
            category_item = QTreeWidgetItem([category])
            self.instruction_tree.addTopLevelItem(category_item)
            
            for name, data in instructions.items():
                instruction_item = QTreeWidgetItem([name])
                instruction_item.setData(0, Qt.ItemDataRole.UserRole, data)
                category_item.addChild(instruction_item)
                
        self.instruction_tree.expandAll()
        
    def populate_examples(self):
        """Populate example programs"""
        examples = {
            "Basic Examples": {
                "Hello Assembly": {
                    "description": "Simple arithmetic operations",
                    "code": """// Basic arithmetic example
// Load some values and perform operations

ADDI X1, XZR, #10    // Load 10 into X1
ADDI X2, XZR, #20    // Load 20 into X2
ADD  X3, X1, X2      // X3 = X1 + X2 = 30
SUB  X4, X3, X1      // X4 = X3 - X1 = 20
STUR X3, [X28, #0]   // Store result to memory
STUR X4, [X28, #8]   // Store second result"""
                },
                "Memory Operations": {
                    "description": "Loading and storing data in memory",
                    "code": """// Memory operations example
// Demonstrate load/store instructions

ADDI X1, XZR, #100   // Load value 100
ADDI X2, XZR, #200   // Load value 200

// Store values to memory
STUR X1, [X28, #0]   // Store X1 at [SP + 0]
STUR X2, [X28, #8]   // Store X2 at [SP + 8]

// Load values back from memory
LDUR X3, [X28, #0]   // Load from [SP + 0] into X3
LDUR X4, [X28, #8]   // Load from [SP + 8] into X4

// Add the loaded values
ADD  X5, X3, X4      // X5 = X3 + X4 = 300"""
                },
                "Logical Operations": {
                    "description": "Bitwise logical operations",
                    "code": """// Logical operations example
// Demonstrate AND, OR, XOR operations

ADDI X1, XZR, #15    // X1 = 15  (0x0F)
ADDI X2, XZR, #51    // X2 = 51  (0x33)

AND  X3, X1, X2      // X3 = X1 & X2 = 3   (0x03)
ORR  X4, X1, X2      // X4 = X1 | X2 = 63  (0x3F)
EOR  X5, X1, X2      // X5 = X1 ^ X2 = 60  (0x3C)

// Store results
STUR X3, [X28, #0]   // Store AND result
STUR X4, [X28, #8]   // Store OR result
STUR X5, [X28, #16]  // Store XOR result"""
                },
                "Multiplication": {
                    "description": "Multiplication operations with MUL instruction",
                    "code": """// Multiplication example
// Calculate area and factorial-like operations

ADDI X1, XZR, #6     // Width = 6
ADDI X2, XZR, #8     // Height = 8
MUL  X3, X1, X2      // Area = Width * Height = 48

// Calculate 5 * 3 * 2  
ADDI X4, XZR, #5     // Load 5
ADDI X5, XZR, #3     // Load 3  
ADDI X6, XZR, #2     // Load 2
MUL  X7, X4, X5      // X7 = 5 * 3 = 15
MUL  X8, X7, X6      // X8 = 15 * 2 = 30

// Store results
STUR X3, [X28, #0]   // Store area (48)
STUR X8, [X28, #8]   // Store calculation result (30)"""
                }
            },
            "Advanced Examples": {
                "Array Sum": {
                    "description": "Calculate sum of array elements",
                    "code": """// Array sum example
// Calculate sum of first 5 numbers: 1+2+3+4+5

ADDI X1, XZR, #0     // Sum accumulator
ADDI X2, XZR, #1     // Current number
ADDI X3, XZR, #5     // Counter (how many to add)
ADDI X4, XZR, #0     // Base address for storage

// Store array values first
STUR X2, [X28, #0]   // Store 1
ADDI X2, X2, #1      // Increment to 2
STUR X2, [X28, #8]   // Store 2
ADDI X2, X2, #1      // Increment to 3
STUR X2, [X28, #16]  // Store 3
ADDI X2, X2, #1      // Increment to 4
STUR X2, [X28, #24]  // Store 4
ADDI X2, X2, #1      // Increment to 5
STUR X2, [X28, #32]  // Store 5

// Now sum them up
LDUR X5, [X28, #0]   // Load first element
ADD  X1, X1, X5      // Add to sum
LDUR X5, [X28, #8]   // Load second element
ADD  X1, X1, X5      // Add to sum
LDUR X5, [X28, #16]  // Load third element
ADD  X1, X1, X5      // Add to sum
LDUR X5, [X28, #24]  // Load fourth element
ADD  X1, X1, X5      // Add to sum
LDUR X5, [X28, #32]  // Load fifth element
ADD  X1, X1, X5      // Add to sum (result = 15)

STUR X1, [X28, #40]  // Store final sum"""
                },
                "Counting Loop": {
                    "description": "Count from 1 to 10 using branches",
                    "code": """// Counting loop with branches
// Count from 1 to 10 and store each number

ADDI X1, XZR, #1     // Counter starts at 1
ADDI X2, XZR, #10    // Maximum count
ADDI X3, XZR, #0     // Memory offset

loop:
    STUR X1, [X28, X3]   // Store current count
    ADDI X3, X3, #8      // Increment memory offset  
    ADDI X1, X1, #1      // Increment counter
    
    SUBS X4, X1, X2      // Compare counter with max
    B.LE loop            // Branch if counter <= max
    
// End of program - X1 will be 11, stored 1-10 in memory"""
                },
                "Find Maximum": {
                    "description": "Find maximum of two numbers using conditional branches",
                    "code": """// Find maximum of two numbers
// Compare X1 and X2, store larger value in X3

ADDI X1, XZR, #25    // First number
ADDI X2, XZR, #30    // Second number

SUBS X4, X1, X2      // Compare X1 - X2
B.GE first_larger    // Branch if X1 >= X2

// X2 is larger
ADD X3, X2, XZR      // X3 = X2
B end                // Skip to end

first_larger:
    ADD X3, X1, XZR  // X3 = X1

end:
    STUR X3, [X28, #0] // Store maximum value"""
                },
                "Advanced Multiplication": {
                    "description": "128-bit multiplication using MUL, SMULH, and UMULH",
                    "code": """// Advanced multiplication example
// Shows 128-bit multiplication with high/low parts

// Test 1: Large unsigned multiplication
ADDI X1, XZR, #1000  // Load 1000
MUL  X2, X1, X1      // X2 = lower 64 bits of 1000 * 1000 = 1000000
UMULH X3, X1, X1     // X3 = upper 64 bits of 1000 * 1000 = 0 (small result)

// Test 2: Very large numbers (using valid immediate ranges)
MOVZ X4, #1000       // Load 1000 (within immediate range)
ADDI X15, XZR, #32   // Load shift amount in register
LSL  X4, X4, X15     // Shift left 32: X4 = 1000 << 32 (very large)
MOVZ X5, #2000       // Load 2000 
LSL  X5, X5, X15     // Shift left 32: X5 = 2000 << 32 (very large)

MUL   X6, X4, X5     // X6 = lower 64 bits of large * large
UMULH X7, X4, X5     // X7 = upper 64 bits (will be non-zero)
SMULH X8, X4, X5     // X8 = signed upper 64 bits (same for positive numbers)

// Test 3: Signed vs unsigned behavior with "negative" numbers
// Create a large number that appears negative in signed interpretation
MOVZ  X9, #1000      // Load 1000 (valid immediate)
ADDI  X16, XZR, #48  // Load shift amount 48 in register
LSL   X9, X9, X16    // Shift left 48: MSB=1, appears negative if signed
ADDI  X10, XZR, #1000 // Multiply by 1000

MUL   X11, X9, X10   // Lower 64 bits (same for signed/unsigned)
SMULH X12, X9, X10   // Signed high part (negative interpretation)  
UMULH X13, X9, X10   // Unsigned high part (positive interpretation)

// Store results to compare
STUR X2, [X28, #0]   // Store lower bits of 1000*1000
STUR X3, [X28, #8]   // Store upper bits of 1000*1000 (should be 0)
STUR X6, [X28, #16]  // Store lower bits of large multiplication
STUR X7, [X28, #24]  // Store unsigned upper bits
STUR X8, [X28, #32]  // Store signed upper bits (same as unsigned for positive)
STUR X11, [X28, #40] // Store lower bits
STUR X12, [X28, #48] // Store signed upper (negative interpretation)
STUR X13, [X28, #56] // Store unsigned upper (positive interpretation)"""
                },
                "Advanced Division": {
                    "description": "Signed vs unsigned division with SDIV and UDIV",
                    "code": """// Advanced division example
// Demonstrates SDIV vs UDIV and remainder calculations

// Simple signed division
ADDI X1, XZR, #20    // Dividend = 20
ADDI X2, XZR, #4     // Divisor = 4
SDIV X3, X1, X2      // X3 = 20 / 4 = 5 (signed division)

// Division with remainder (integer division)
ADDI X4, XZR, #23    // Dividend = 23
ADDI X5, XZR, #7     // Divisor = 7
SDIV X6, X4, X5      // X6 = 23 / 7 = 3 (remainder discarded)

// Calculate actual remainder using modulo formula: a % b = a - (a/b)*b
MUL  X7, X6, X5      // X7 = (23/7) * 7 = 3 * 7 = 21
SUB  X8, X4, X7      // X8 = 23 - 21 = 2 (remainder)

// Compare signed vs unsigned division with large numbers  
// Load a large number that has different signed/unsigned interpretation
MOVZ X9, #1000       // Load 1000 (valid immediate)
ADDI X14, XZR, #32   // Load shift amount in register
LSL  X9, X9, X14     // Shift left 32: make it large
ADDI X10, XZR, #1000 // Divisor = 1000

SDIV X11, X9, X10    // X11 = signed division
UDIV X12, X9, X10    // X12 = unsigned division (should be the same for positive)

// Store results
STUR X3, [X28, #0]   // Store 5 (20/4)
STUR X6, [X28, #8]   // Store 3 (23/7 quotient)
STUR X8, [X28, #16]  // Store 2 (23/7 remainder)
STUR X11, [X28, #24] // Store signed division result
STUR X12, [X28, #32] // Store unsigned division result

// Note: Division by zero will cause a runtime error
// Example: SDIV X13, X1, XZR  // This would throw "Division by zero error" """
                },
                "Function Call": {
                    "description": "Function calls using BL (Branch and Link) and BR (Branch Register)",
                    "code": """// Function call demonstration with BL and BR
// Shows how to call functions and return properly

// Main program
ADDI X0, XZR, #10        // Load 10 into X0
ADDI X1, XZR, #5         // Load 5 into X1
BL   add_function        // Call function - saves return address in LR (X30)
MOVZ X2, #999            // This executes AFTER function returns

// Program end
end_program:
    STUR X0, [X28, #0]   // Store result at memory location
    STUR X2, [X28, #8]   // Store X2 to verify it was set
    B end_program        // Infinite loop to end

// Function that adds two numbers
add_function:
    ADD  X0, X0, X1      // X0 = X0 + X1 (10 + 5 = 15)
    MOVZ X3, #42         // Mark that function executed  
    BR   X30             // Return to saved address in LR

// Expected results:
// X0 = 15 (sum of 10 + 5)
// X2 = 999 (proves function returned correctly)
// X3 = 42 (proves function executed)"""
                }
            },
            "Branch Examples": {
                "Function Call Basic": {
                    "description": "Simple BL and BR function call example",
                    "code": """// Basic BL and BR example
// Demonstrates the simplest function call

ADDI X0, XZR, #100   // Load initial value
BL   my_function     // Call function 
ADDI X0, X0, #1      // This runs after function returns
STUR X0, [X28, #0]   // Store final result
B    end             // Jump to end to prevent looping

my_function:
    ADDI X0, X0, #50 // Add 50 to X0 (X0 becomes 150)
    BR X30           // Return using Link Register

end:
    B end            // Infinite loop to halt program"""
                },
                "Simple Branch": {
                    "description": "Basic unconditional and conditional branches",
                    "code": """// Simple branching example
// Test different branch types

ADDI X1, XZR, #5     // Load test value
ADDI X2, XZR, #0     // Initialize result

// Test CBZ (branch if zero)
CBNZ X1, not_zero    // Branch if X1 != 0
ADDI X2, X2, #100    // This won't execute
B end

not_zero:
    ADDI X2, X2, #1  // X2 = 1 (X1 was not zero)

// Test conditional branch with flags
SUBS X3, X1, X1      // X1 - X1 = 0, sets Z flag
B.EQ zero_result     // Branch if equal (Z flag set)
ADDI X2, X2, #200    // This won't execute
B end

zero_result:
    ADDI X2, X2, #10 // X2 = 11 (subtraction was zero)

end:
    STUR X2, [X28, #0] // Store final result (should be 11)"""
                },
                "Factorial": {
                    "description": "Calculate factorial using a loop with branches",
                    "code": """// Factorial calculation using branches
// Calculate 5! = 5 * 4 * 3 * 2 * 1 = 120

ADDI X1, XZR, #5     // Number to calculate factorial of
ADDI X2, XZR, #1     // Result accumulator
ADDI X3, XZR, #1     // Constant 1 for comparison

factorial_loop:
    CBZ X1, done         // If X1 == 0, we're done
    MUL X2, X2, X1       // result *= X1 (using MUL instruction)
    SUBI X1, X1, #1      // X1--
    B factorial_loop     // Continue loop

done:
    STUR X2, [X28, #0]   // Store factorial result"""
                },
                "Flag Usage Example": {
                    "description": "Demonstrates condition flags with SUBS and conditional branches",
                    "code": """// Flag usage with conditional branches
// Shows how flags are set and used for decision making

ADDI X1, XZR, #10    // Load 10 
ADDI X2, XZR, #20    // Load 20
ADDI X3, XZR, #10    // Load 10 (same as X1)

// Compare X1 and X2 (10 vs 20)
SUBS X4, X1, X2      // X4 = X1 - X2 = -10, sets N flag (negative)
B.LT  x1_less        // Branch if X1 < X2 (N≠V, true here)
B.GE  x1_greater     // This won't execute

x1_less:
    MOVZ X5, #1      // X5 = 1 (X1 was less than X2)
    B continue

x1_greater:
    MOVZ X5, #2      // X5 = 2 (X1 was greater/equal to X2)

continue:
// Compare X1 and X3 (10 vs 10)  
SUBS X6, X1, X3      // X6 = X1 - X3 = 0, sets Z flag (zero)
B.EQ  equal          // Branch if equal (Z=1, true here)
B.NE  not_equal      // This won't execute

equal:
    MOVZ X7, #42     // X7 = 42 (X1 equals X3)
    B end

not_equal:
    MOVZ X7, #99     // X7 = 99 (X1 not equal to X3)

end:
    STUR X5, [X28, #0]  // Store first comparison result (1)
    STUR X7, [X28, #8]  // Store second comparison result (42)"""
                },
                "CMP and CMPI Examples": {
                    "description": "Using CMP and CMPI for clean comparisons and conditional branches",
                    "code": """// CMP and CMPI comparison examples
// Shows clean comparison without storing intermediate results

ADDI X1, XZR, #15    // Load 15
ADDI X2, XZR, #20    // Load 20

// Test 1: CMP instruction (compare two registers)
CMP  X1, X2          // Compare X1 and X2 (15 vs 20), sets flags
B.LT first_smaller   // Branch if X1 < X2 (should branch)
MOVZ X3, #999        // This won't execute

first_smaller:
    MOVZ X3, #1      // X3 = 1 (X1 was less than X2)

// Test 2: CMPI instruction (compare register with immediate)  
CMPI X1, #15         // Compare X1 with 15 (15 vs 15), sets flags
B.EQ values_equal    // Branch if equal (should branch)
MOVZ X4, #888        // This won't execute

values_equal:
    MOVZ X4, #2      // X4 = 2 (X1 equals 15)

// Test 3: CMPI with different value
CMPI X2, #25         // Compare X2 with 25 (20 vs 25), sets flags  
B.LT less_than_25    // Branch if X2 < 25 (should branch)
MOVZ X5, #777        // This won't execute

less_than_25:
    MOVZ X5, #3      // X5 = 3 (X2 was less than 25)

// Test 4: CMP for greater than test
CMP  X2, X1          // Compare X2 and X1 (20 vs 15), sets flags
B.GT second_greater  // Branch if X2 > X1 (should branch)
MOVZ X6, #666        // This won't execute

second_greater:
    MOVZ X6, #4      // X6 = 4 (X2 was greater than X1)

// Store all results
STUR X3, [X28, #0]   // Store 1 (CMP result)
STUR X4, [X28, #8]   // Store 2 (CMPI equal result)  
STUR X5, [X28, #16]  // Store 3 (CMPI less than result)
STUR X6, [X28, #24]  // Store 4 (CMP greater than result)

// Advantages of CMP/CMPI:
// - Cleaner code (no intermediate results stored)
// - Purpose is clear (comparison only)
// - No register wasted on unused subtraction result"""
                }
            }
        }
        
        for category, examples_dict in examples.items():
            category_item = QTreeWidgetItem([category])
            self.example_tree.addTopLevelItem(category_item)
            
            for name, data in examples_dict.items():
                example_item = QTreeWidgetItem([name])
                example_item.setData(0, Qt.ItemDataRole.UserRole, data)
                category_item.addChild(example_item)
                
        self.example_tree.expandAll()
        
    def populate_quick_reference(self):
        """Populate quick reference"""
        quick_ref = """LEGv8 QUICK REFERENCE

REGISTERS:
  X0-X30    : General purpose registers (64-bit)
  X31 (XZR) : Zero register (always contains 0)
  X28 (SP)  : Stack pointer
  X29 (FP)  : Frame pointer
  X30 (LR)  : Link register

INSTRUCTION FORMATS:
  R-type: instruction Rd, Rn, Rm
  I-type: instruction Rd, Rn, #immediate
  D-type: instruction Rt, [Rn, #offset]

COMMON INSTRUCTIONS:

Arithmetic:
  ADD   Rd, Rn, Rm     # Rd = Rn + Rm
  ADDS  Rd, Rn, Rm     # Rd = Rn + Rm (with flags)
  SUB   Rd, Rn, Rm     # Rd = Rn - Rm
  SUBS  Rd, Rn, Rm     # Rd = Rn - Rm (with flags)
  MUL   Rd, Rn, Rm     # Rd = lower 64-bits of Rn * Rm
  SMULH Rd, Rn, Rm     # Rd = upper 64-bits of signed Rn * Rm  
  UMULH Rd, Rn, Rm     # Rd = upper 64-bits of unsigned Rn * Rm
  SDIV  Rd, Rn, Rm     # Rd = signed Rn / signed Rm
  UDIV  Rd, Rn, Rm     # Rd = unsigned Rn / unsigned Rm
  CMP   Rn, Rm         # Compare registers (sets flags only)
  CMPI  Rn, #imm       # Compare register with immediate (sets flags only)
  ADDI  Rd, Rn, #imm   # Rd = Rn + immediate
  ADDIS Rd, Rn, #imm   # Rd = Rn + immediate (with flags)
  SUBI  Rd, Rn, #imm   # Rd = Rn - immediate
  SUBIS Rd, Rn, #imm   # Rd = Rn - immediate (with flags)
  MOVZ  Rd, #imm       # Rd = immediate
  MOVK  Rd, #imm       # Move immediate, keep other bits

Logical:
  AND  Rd, Rn, Rm     # Rd = Rn & Rm
  ORR  Rd, Rn, Rm     # Rd = Rn | Rm
  EOR  Rd, Rn, Rm     # Rd = Rn ^ Rm
  ANDI Rd, Rn, #imm   # Rd = Rn & immediate
  ORRI Rd, Rn, #imm   # Rd = Rn | immediate
  EORI Rd, Rn, #imm   # Rd = Rn ^ immediate

Shift:
  LSL  Rd, Rn, Rm     # Rd = Rn << Rm
  LSR  Rd, Rn, Rm     # Rd = Rn >> Rm

Memory:
  LDUR  Rt, [Rn, #offset]   # Load doubleword (64-bit)
  STUR  Rt, [Rn, #offset]   # Store doubleword (64-bit)
  LDURW Rt, [Rn, #offset]   # Load word (32-bit)
  STURW Rt, [Rn, #offset]   # Store word (32-bit)
  LDURB Rt, [Rn, #offset]   # Load byte (8-bit)
  STURB Rt, [Rn, #offset]   # Store byte (8-bit)

Branches:
  B      label          # Unconditional branch
  BL     label          # Branch and link (function call)
  BR     Xn             # Branch to register (function return)
  CBZ    Rt, label      # Branch if register == 0
  CBNZ   Rt, label      # Branch if register != 0
  B.EQ   label          # Branch if equal (after SUBS/SUBIS)
  B.NE   label          # Branch if not equal
  B.LT   label          # Branch if less than (signed)
  B.LE   label          # Branch if less/equal (signed)
  B.GT   label          # Branch if greater than (signed)
  B.GE   label          # Branch if greater/equal (signed)

CONDITION FLAGS:
  N (Negative)    : Set if result < 0
  Z (Zero)        : Set if result == 0  
  V (Overflow)    : Set if signed arithmetic overflow (simplified)
  C (Carry)       : Set if unsigned carry (simplified)
  
Flag-setting instructions:
  ADDS, SUBS, ADDIS, SUBIS  # Set flags based on result

Conditional branches use flags:
  B.EQ  # Branch if Z=1 (equal/zero)
  B.NE  # Branch if Z=0 (not equal/not zero) 
  B.LT  # Branch if N≠V (less than, signed)
  B.GE  # Branch if N=V (greater/equal, signed)
  B.GT  # Branch if Z=0 and N=V (greater than, signed)
  B.LE  # Branch if Z=1 or N≠V (less/equal, signed)

ADDRESSING MODES:
  [Rn]         # Base register only
  [Rn, #offset] # Base register + offset

IMMEDIATE VALUES:
  #123         # Decimal immediate
  #-50         # Negative immediate
  Range: -2048 to +2047

COMMENTS:
  // This is a comment

LABELS:
  loop:                 # Label definition
  B loop                # Branch to label

TIPS:
- All instructions are case-insensitive
- Register names can be X0-X31 or XZR, SP, LR, FP
- Memory addresses are byte-addressed
- Word operations require 4-byte alignment
- Doubleword operations require 8-byte alignment
- Use SUBS/SUBIS to set flags for conditional branches
- Labels must start with letter/underscore, followed by letters/numbers/underscores
- Function calls: Use BL to call, BR X30 to return
- BL automatically saves return address in Link Register (X30)
"""
        
        self.quick_ref_text.setPlainText(quick_ref)
        
    def on_instruction_selected(self, item, column):
        """Handle instruction selection"""
        data = item.data(0, Qt.ItemDataRole.UserRole)
        if data:
            details = f"""INSTRUCTION: {item.text(0)}

Syntax: {data['syntax']}

Description: {data['description']}

Operation: {data['operation']}

Example:
{data['example']}
"""
            self.instruction_details.setPlainText(details)
            
    def on_example_selected(self, item, column):
        """Handle example selection"""
        data = item.data(0, Qt.ItemDataRole.UserRole)
        if data:
            code = f"""// {item.text(0)}
// {data['description']}

{data['code']}
"""
            self.example_code.setPlainText(code)
