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
    MUL X2, X2, X1       // result *= X1 (Note: MUL not implemented yet, use multiple adds)
    SUBI X1, X1, #1      // X1--
    B factorial_loop     // Continue loop

done:
    STUR X2, [X28, #0]   // Store factorial result

// Simplified version without MUL:
// This example shows the structure but would need
// multiple ADD operations to simulate multiplication"""
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
