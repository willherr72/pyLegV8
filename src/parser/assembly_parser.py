"""
LEGv8 Assembly Parser
Parses LEGv8 assembly code into instruction objects
"""

import re
from typing import List, Dict, Optional, Tuple
from core.instruction import (Instruction, RTypeInstruction, ITypeInstruction, 
                              DTypeInstruction, BTypeInstruction, CBTypeInstruction,
                              CondBTypeInstruction, InstructionType)


class ParseError(Exception):
    """Assembly parsing error"""
    def __init__(self, message: str, line_number: int = 0, line_text: str = ""):
        self.line_number = line_number
        self.line_text = line_text
        super().__init__(f"Line {line_number}: {message}")


class AssemblyParser:
    """LEGv8 assembly code parser"""
    
    def __init__(self):
        # Define instruction patterns and types
        self.r_type_instructions = {
            'ADD', 'SUB', 'ADDS', 'SUBS', 'AND', 'ORR', 'EOR', 'LSL', 'LSR'
        }
        
        self.i_type_instructions = {
            'ADDI', 'SUBI', 'ADDIS', 'SUBIS', 'ANDI', 'ORRI', 'EORI'
        }
        
        self.move_instructions = {
            'MOVZ', 'MOVK'
        }
        
        self.d_type_instructions = {
            'LDUR', 'STUR', 'LDURW', 'STURW', 'LDURB', 'STURB'
        }
        
        self.b_type_instructions = {
            'B'
        }
        
        self.cb_type_instructions = {
            'CBZ', 'CBNZ'
        }
        
        self.conditional_branches = {
            'EQ', 'NE', 'LT', 'LE', 'GT', 'GE', 'LO', 'LS', 'HI', 'HS'
        }
        
        # Regex patterns
        self.register_pattern = re.compile(r'^X(\d+)$', re.IGNORECASE)
        self.special_register_pattern = re.compile(r'^(XZR|SP|LR|FP)$', re.IGNORECASE)
        self.immediate_pattern = re.compile(r'^#?(-?\d+)$')
        self.memory_pattern = re.compile(r'^\[(X\d+|XZR|SP|LR|FP),?\s*#?(-?\d+)?\]$', re.IGNORECASE)
        self.comment_pattern = re.compile(r'//.*$')
        self.label_pattern = re.compile(r'^([A-Za-z_][A-Za-z0-9_]*):$')  # Label definition
        self.label_ref_pattern = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')  # Label reference
        
    def parse(self, assembly_code: str) -> List[Instruction]:
        """Parse assembly code and return list of instructions (two-pass parsing)"""
        lines = assembly_code.strip().split('\n')
        
        # First pass: collect labels and instructions
        labels = {}  # label_name -> instruction_index
        instructions = []
        errors = []
        
        instruction_index = 0
        for line_num, line in enumerate(lines, 1):
            try:
                parsed = self.parse_line_with_labels(line, line_num)
                if parsed:
                    if parsed['type'] == 'label':
                        labels[parsed['name']] = instruction_index
                    elif parsed['type'] == 'instruction':
                        instructions.append(parsed['instruction'])
                        instruction_index += 1
            except ParseError as e:
                errors.append(f"Line {line_num}: {str(e)}")
        
        # If there are parsing errors, raise them now
        if errors:
            raise ParseError("\n".join(errors))
            
        # Second pass: resolve branch targets
        for instruction in instructions:
            if hasattr(instruction, 'target_label') and instruction.target_label:
                if instruction.target_label in labels:
                    # Convert instruction index to PC address (each instruction is 4 bytes)
                    instruction.target_address = labels[instruction.target_label] * 4
                else:
                    errors.append(f"Undefined label: {instruction.target_label}")
                    
        if errors:
            raise ParseError("\n".join(errors))
                
        return instructions
        
    def parse_line_with_labels(self, line: str, line_number: int) -> Optional[Dict]:
        """Parse a line that may contain a label or instruction"""
        # Remove comments
        line = self.comment_pattern.sub('', line).strip()
        
        # Skip empty lines
        if not line:
            return None
            
        # Check for label definition
        label_match = self.label_pattern.match(line)
        if label_match:
            return {
                'type': 'label',
                'name': label_match.group(1)
            }
            
        # Otherwise, parse as instruction
        instruction = self.parse_line(line, line_number)
        if instruction:
            return {
                'type': 'instruction',
                'instruction': instruction
            }
            
        return None
        
    def parse_line(self, line: str, line_number: int) -> Optional[Instruction]:
        """Parse a single line of assembly code"""
        # Remove comments
        line = self.comment_pattern.sub('', line).strip()
        
        # Skip empty lines
        if not line:
            return None
            
        # Split instruction and operands more carefully
        # First split on whitespace to get instruction
        parts = line.split(None, 1)  # Split on first whitespace only
        if not parts:
            return None
            
        mnemonic = parts[0].upper()
        
        # Parse operands if they exist
        if len(parts) > 1:
            operands = self.parse_operands(parts[1])
        else:
            operands = []
        
        # Check for conditional branch (B.EQ, B.NE, etc.)
        if '.' in mnemonic:
            base_mnemonic, condition = mnemonic.split('.', 1)
            if base_mnemonic == 'B' and condition.upper() in self.conditional_branches:
                return self.parse_cond_branch(condition, operands, line_number)
        
        # Parse based on instruction type
        if mnemonic in self.r_type_instructions:
            return self.parse_r_type(mnemonic, operands, line_number)
        elif mnemonic in self.i_type_instructions:
            return self.parse_i_type(mnemonic, operands, line_number)
        elif mnemonic in self.move_instructions:
            return self.parse_move_type(mnemonic, operands, line_number)
        elif mnemonic in self.d_type_instructions:
            return self.parse_d_type(mnemonic, operands, line_number)
        elif mnemonic in self.b_type_instructions:
            return self.parse_b_type(mnemonic, operands, line_number)
        elif mnemonic in self.cb_type_instructions:
            return self.parse_cb_type(mnemonic, operands, line_number)
        else:
            raise ParseError(f"Unknown instruction: {mnemonic}", line_number)
            
    def parse_r_type(self, mnemonic: str, operands: List[str], line_number: int) -> RTypeInstruction:
        """Parse R-type instruction"""
        if len(operands) != 3:
            raise ParseError(f"R-type instruction {mnemonic} requires 3 operands", line_number)
            
        rd = self.parse_register(operands[0], line_number)
        rn = self.parse_register(operands[1], line_number)
        rm = self.parse_register(operands[2], line_number)
        
        return RTypeInstruction(mnemonic, rd, rn, rm, line_number)
        
    def parse_i_type(self, mnemonic: str, operands: List[str], line_number: int) -> ITypeInstruction:
        """Parse I-type instruction"""
        if len(operands) != 3:
            raise ParseError(f"I-type instruction {mnemonic} requires 3 operands", line_number)
            
        rd = self.parse_register(operands[0], line_number)
        rn = self.parse_register(operands[1], line_number)
        immediate = self.parse_immediate(operands[2], line_number)
        
        return ITypeInstruction(mnemonic, rd, rn, immediate, line_number)
        
    def parse_move_type(self, mnemonic: str, operands: List[str], line_number: int) -> ITypeInstruction:
        """Parse move-type instruction (2 operands: Rd, #immediate)"""
        if len(operands) != 2:
            raise ParseError(f"Move instruction {mnemonic} requires 2 operands", line_number)
            
        rd = self.parse_register(operands[0], line_number)
        immediate = self.parse_immediate(operands[1], line_number)
        
        # For move instructions, we use XZR (register 31) as the "source" register
        return ITypeInstruction(mnemonic, rd, 31, immediate, line_number)
        
    def parse_d_type(self, mnemonic: str, operands: List[str], line_number: int) -> DTypeInstruction:
        """Parse D-type instruction"""
        if len(operands) != 2:
            raise ParseError(f"D-type instruction {mnemonic} requires 2 operands", line_number)
            
        rt = self.parse_register(operands[0], line_number)
        
        # Parse memory operand [Xn, #offset] or [Xn]
        memory_match = self.memory_pattern.match(operands[1])
        if not memory_match:
            raise ParseError(f"Invalid memory operand: {operands[1]}", line_number)
            
        reg_str = memory_match.group(1)
        offset = int(memory_match.group(2)) if memory_match.group(2) else 0
        
        # Parse the register part (could be X# or special name)
        rn = self.parse_register(reg_str, line_number)
            
        return DTypeInstruction(mnemonic, rt, rn, offset, line_number)
        
    def parse_operands(self, operand_string: str) -> List[str]:
        """Parse operand string, handling memory operands carefully"""
        operands = []
        current_operand = ""
        bracket_depth = 0
        
        for char in operand_string:
            if char == '[':
                bracket_depth += 1
                current_operand += char
            elif char == ']':
                bracket_depth -= 1
                current_operand += char
            elif char == ',' and bracket_depth == 0:
                # Only split on commas outside of brackets
                if current_operand.strip():
                    operands.append(current_operand.strip())
                current_operand = ""
            else:
                current_operand += char
        
        # Add the last operand
        if current_operand.strip():
            operands.append(current_operand.strip())
            
        return operands
        
    def parse_b_type(self, mnemonic: str, operands: List[str], line_number: int) -> BTypeInstruction:
        """Parse B-type instruction (unconditional branch)"""
        if len(operands) != 1:
            raise ParseError(f"B-type instruction {mnemonic} requires 1 operand", line_number)
            
        target_label = operands[0]
        if not self.label_ref_pattern.match(target_label):
            raise ParseError(f"Invalid label reference: {target_label}", line_number)
            
        return BTypeInstruction(mnemonic, target_label, line_number)
        
    def parse_cb_type(self, mnemonic: str, operands: List[str], line_number: int) -> CBTypeInstruction:
        """Parse CB-type instruction (conditional branch on zero/not zero)"""
        if len(operands) != 2:
            raise ParseError(f"CB-type instruction {mnemonic} requires 2 operands", line_number)
            
        register = self.parse_register(operands[0], line_number)
        target_label = operands[1]
        if not self.label_ref_pattern.match(target_label):
            raise ParseError(f"Invalid label reference: {target_label}", line_number)
            
        return CBTypeInstruction(mnemonic, register, target_label, line_number)
        
    def parse_cond_branch(self, condition: str, operands: List[str], line_number: int) -> CondBTypeInstruction:
        """Parse conditional branch instruction (B.EQ, B.NE, etc.)"""
        if len(operands) != 1:
            raise ParseError(f"Conditional branch B.{condition} requires 1 operand", line_number)
            
        target_label = operands[0]
        if not self.label_ref_pattern.match(target_label):
            raise ParseError(f"Invalid label reference: {target_label}", line_number)
            
        return CondBTypeInstruction("B", condition, target_label, line_number)
        
    def parse_register(self, operand: str, line_number: int) -> int:
        """Parse register operand (X0-X31, XZR, SP, LR, FP)"""
        operand = operand.strip()
        
        # Check for special register names first
        special_match = self.special_register_pattern.match(operand)
        if special_match:
            reg_name = special_match.group(1).upper()
            if reg_name == 'XZR':
                return 31  # Zero register
            elif reg_name == 'SP':
                return 28  # Stack pointer
            elif reg_name == 'LR':
                return 30  # Link register
            elif reg_name == 'FP':
                return 29  # Frame pointer
        
        # Check for standard X# format
        match = self.register_pattern.match(operand)
        if not match:
            raise ParseError(f"Invalid register: {operand}", line_number)
            
        reg_num = int(match.group(1))
        if not (0 <= reg_num <= 31):
            raise ParseError(f"Invalid register number: {reg_num}", line_number)
            
        return reg_num
        
    def parse_immediate(self, operand: str, line_number: int) -> int:
        """Parse immediate value"""
        match = self.immediate_pattern.match(operand.strip())
        if not match:
            raise ParseError(f"Invalid immediate value: {operand}", line_number)
            
        value = int(match.group(1))
        
        # Check immediate value range (LEGv8 typically uses 12-bit immediates)
        if not (-2048 <= value <= 2047):
            raise ParseError(f"Immediate value out of range (-2048 to 2047): {value}", line_number)
            
        return value
        
    def validate_syntax(self, assembly_code: str) -> List[Tuple[int, str]]:
        """Validate syntax and return list of (line_number, error_message) tuples"""
        errors = []
        lines = assembly_code.strip().split('\n')
        
        for line_num, line in enumerate(lines, 1):
            try:
                self.parse_line(line, line_num)
            except ParseError as e:
                errors.append((line_num, str(e)))
                
        return errors
