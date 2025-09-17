# PyLEGv8 - LEGv8 Assembly Simulator

A Python-based LEGv8 Assembly Simulator with GUI, inspired by the [ARM University Graphical Micro-Architecture Simulator](https://github.com/arm-university/Graphical-Micro-Architecture-Simulator).

## Features

✅ **Code Editor with Syntax Highlighting**
- LEGv8 assembly syntax highlighting
- Line numbers with current execution highlighting
- Built-in example programs

✅ **Register Display Panel**
- All 32 LEGv8 registers (X0-X31)
- Multiple display formats (decimal, hexadecimal, binary)
- Special register annotations (SP, FP, LR, XZR)

✅ **Memory Panel**
- Memory visualization in multiple formats (bytes, words, doublewords)
- Navigate to specific addresses
- Memory usage statistics

✅ **Step-by-Step Execution**
- Compile and validate LEGv8 assembly code
- Execute one instruction at a time
- Run all instructions at once
- Reset simulation state

✅ **Comprehensive Help System**
- Complete LEGv8 instruction reference
- Example programs with explanations
- Quick reference guide

✅ **Error Detection & Validation**
- Syntax error detection during compilation
- Runtime error handling
- Helpful error messages

## Supported Instructions

### Arithmetic Instructions
- `ADD Rd, Rn, Rm` - Add registers
- `ADDS Rd, Rn, Rm` - Add registers (sets flags)
- `SUB Rd, Rn, Rm` - Subtract registers  
- `SUBS Rd, Rn, Rm` - Subtract registers (sets flags)
- `ADDI Rd, Rn, #imm` - Add immediate
- `ADDIS Rd, Rn, #imm` - Add immediate (sets flags)
- `SUBI Rd, Rn, #imm` - Subtract immediate
- `SUBIS Rd, Rn, #imm` - Subtract immediate (sets flags)
- `MOVZ Rd, #imm` - Move immediate (zero other bits)
- `MOVK Rd, #imm` - Move immediate (keep other bits)

### Logical Instructions
- `AND Rd, Rn, Rm` - Bitwise AND
- `ORR Rd, Rn, Rm` - Bitwise OR
- `EOR Rd, Rn, Rm` - Bitwise XOR
- `LSL Rd, Rn, Rm` - Logical shift left
- `LSR Rd, Rn, Rm` - Logical shift right

### Data Transfer Instructions
- `LDUR Rt, [Rn, #offset]` - Load doubleword (64-bit)
- `STUR Rt, [Rn, #offset]` - Store doubleword (64-bit)
- `LDURW Rt, [Rn, #offset]` - Load word (32-bit)
- `STURW Rt, [Rn, #offset]` - Store word (32-bit)
- `LDURB Rt, [Rn, #offset]` - Load byte (8-bit)
- `STURB Rt, [Rn, #offset]` - Store byte (8-bit)

### Branch Instructions
- `B label` - Unconditional branch
- `CBZ Rt, label` - Branch if register is zero
- `CBNZ Rt, label` - Branch if register is not zero
- `B.EQ label` - Branch if equal (Z flag set)
- `B.NE label` - Branch if not equal (Z flag clear)
- `B.LT label` - Branch if less than (signed)
- `B.GE label` - Branch if greater/equal (signed)
- `B.GT label` - Branch if greater than (signed)
- `B.LE label` - Branch if less/equal (signed)

## Installation

### Prerequisites
- Python 3.12+
- UV package manager

### Setup
```bash
# Clone or download the project
cd pyLegV8

# Install dependencies using UV
uv sync

# Run the application
uv run python src/main.py
```

## Usage

1. **Write Assembly Code**: Use the code editor to write LEGv8 assembly programs
2. **Compile**: Click "Compile" (F5) to parse and validate your code
3. **Execute**: Use "Step" (F10) for single instruction execution or "Run All" (F9) to execute all instructions
4. **Monitor State**: Watch registers and memory update in real-time
5. **Get Help**: Use the Help menu for instruction reference and examples

### Example Program
```assembly
// Simple arithmetic example
ADDI X1, XZR, #10    // Load 10 into X1
ADDI X2, XZR, #20    // Load 20 into X2
ADD  X3, X1, X2      // X3 = X1 + X2 = 30
STUR X3, [X28, #0]   // Store result to memory
```

## Project Structure

```
src/
├── main.py              # Application entry point
├── core/                # LEGv8 simulator core
│   ├── cpu.py          # CPU simulation logic
│   ├── registers.py    # Register file implementation
│   ├── memory.py       # Memory simulation
│   └── instruction.py  # Instruction definitions
├── gui/                 # GUI components
│   ├── main_window.py  # Main application window
│   ├── code_editor.py  # Code editor with syntax highlighting
│   ├── register_panel.py # Register display panel
│   ├── memory_panel.py # Memory display panel
│   └── help_dialog.py  # Help system
└── parser/             # Assembly parser
    └── assembly_parser.py # LEGv8 assembly parser
```

## Development

The project uses UV for dependency management and follows Python best practices:

- **Core Architecture**: Modular design with separate CPU, memory, and register components
- **GUI Framework**: PyQt6 for cross-platform desktop GUI
- **Parser**: Custom LEGv8 assembly parser with error detection
- **Testing**: Built-in validation and error handling

## Educational Purpose

This simulator is designed as a learning tool for:
- Understanding LEGv8 instruction set architecture
- Visualizing program execution step-by-step
- Learning assembly programming concepts
- Exploring computer architecture fundamentals

## Future Enhancements

- [ ] Branch and conditional instructions (B, BR, CBZ, CBNZ)
- [ ] Visual datapath display
- [ ] File I/O for assembly programs
- [ ] Debugging breakpoints
- [ ] Performance metrics and cycle counting
- [ ] Export execution traces

## License

This project is open source. See LICENSE file for details.

## Acknowledgments

Inspired by the ARM University LEGv8 Simulator. Built with modern Python and PyQt6 for enhanced educational experience.