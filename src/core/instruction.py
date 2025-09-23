"""
LEGv8 Instruction Implementation
Handles parsing and execution of LEGv8 instructions
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from enum import Enum


class InstructionType(Enum):
    """LEGv8 instruction types"""
    R_TYPE = "R"  # Register type (ADD, SUB, AND, OR, etc.)
    I_TYPE = "I"  # Immediate type (ADDI, SUBI, etc.)
    D_TYPE = "D"  # Data transfer type (LDUR, STUR)
    B_TYPE = "B"  # Branch type (B)
    BL_TYPE = "BL"  # Branch and link type (BL)
    BR_TYPE = "BR"  # Branch register type (BR)
    CB_TYPE = "CB"  # Conditional branch type (CBZ, CBNZ)
    COND_B_TYPE = "COND_B"  # Conditional branch with flags (B.EQ, B.NE, etc.)


class Instruction(ABC):
    """Abstract base class for LEGv8 instructions"""
    
    def __init__(self, mnemonic: str, operands: List[str], line_number: int = 0):
        self.mnemonic = mnemonic.upper()
        self.operands = operands
        self.line_number = line_number
        self.instruction_type: Optional[InstructionType] = None
        
    @abstractmethod
    def execute(self, cpu) -> Dict[str, Any]:
        """Execute the instruction on the given CPU"""
        pass
        
    def __str__(self) -> str:
        return f"{self.mnemonic} {', '.join(self.operands)}"


class RTypeInstruction(Instruction):
    """R-type instructions (register-register operations)"""
    
    def __init__(self, mnemonic: str, rd: int, rn: int, rm: int, line_number: int = 0):
        super().__init__(mnemonic, [f"X{rd}", f"X{rn}", f"X{rm}"], line_number)
        self.rd = rd  # destination register
        self.rn = rn  # first source register  
        self.rm = rm  # second source register
        self.instruction_type = InstructionType.R_TYPE
        
    def execute(self, cpu) -> Dict[str, Any]:
        val_rn = cpu.registers.read(self.rn)
        val_rm = cpu.registers.read(self.rm)
        result_changes = []
        
        if self.mnemonic == "ADD" or self.mnemonic == "ADDS":
            result = val_rn + val_rm
        elif self.mnemonic == "SUB" or self.mnemonic == "SUBS":
            result = val_rn - val_rm
        elif self.mnemonic == "AND":
            result = val_rn & val_rm
        elif self.mnemonic == "ORR":
            result = val_rn | val_rm
        elif self.mnemonic == "EOR":
            result = val_rn ^ val_rm
        elif self.mnemonic == "MUL":
            result = val_rn * val_rm
        elif self.mnemonic == "LSL":  # Logical shift left
            result = val_rn << (val_rm & 0x3F)  # Only use bottom 6 bits for shift amount
        elif self.mnemonic == "LSR":  # Logical shift right
            result = (val_rn & 0xFFFFFFFFFFFFFFFF) >> (val_rm & 0x3F)
        else:
            raise ValueError(f"Unsupported R-type instruction: {self.mnemonic}")
            
        # Set flags for flag-setting instructions
        if self.mnemonic in ["ADDS", "SUBS"]:
            cpu.set_flags(result)
            
        if cpu.registers.write(self.rd, result):
            result_changes.append(self.rd)
            
        return {"register_changes": result_changes}


class ITypeInstruction(Instruction):
    """I-type instructions (immediate operations)"""
    
    def __init__(self, mnemonic: str, rd: int, rn: int, immediate: int, line_number: int = 0):
        super().__init__(mnemonic, [f"X{rd}", f"X{rn}", f"#{immediate}"], line_number)
        self.rd = rd
        self.rn = rn
        self.immediate = immediate
        self.instruction_type = InstructionType.I_TYPE
        
    def execute(self, cpu) -> Dict[str, Any]:
        val_rn = cpu.registers.read(self.rn)
        result_changes = []
        
        if self.mnemonic == "ADDI" or self.mnemonic == "ADDIS":
            result = val_rn + self.immediate
        elif self.mnemonic == "SUBI" or self.mnemonic == "SUBIS":
            result = val_rn - self.immediate
        elif self.mnemonic == "MOVZ":
            result = self.immediate  # Move immediate, zero other bits
        elif self.mnemonic == "MOVK":
            result = (val_rn & 0xFFFFFFFFFFFF0000) | (self.immediate & 0xFFFF)  # Keep other bits, move immediate to lower 16
        elif self.mnemonic == "ANDI":
            result = val_rn & self.immediate
        elif self.mnemonic == "ORRI":
            result = val_rn | self.immediate
        elif self.mnemonic == "EORI":
            result = val_rn ^ self.immediate
        else:
            raise ValueError(f"Unsupported I-type instruction: {self.mnemonic}")
            
        # Set flags for flag-setting instructions
        if self.mnemonic in ["ADDIS", "SUBIS"]:
            cpu.set_flags(result)
            
        if cpu.registers.write(self.rd, result):
            result_changes.append(self.rd)
            
        return {"register_changes": result_changes}


class DTypeInstruction(Instruction):
    """D-type instructions (data transfer)"""
    
    def __init__(self, mnemonic: str, rt: int, rn: int, offset: int, line_number: int = 0):
        super().__init__(mnemonic, [f"X{rt}", f"[X{rn}, #{offset}]"], line_number)
        self.rt = rt  # target register
        self.rn = rn  # base register
        self.offset = offset  # memory offset
        self.instruction_type = InstructionType.D_TYPE
        
    def execute(self, cpu) -> Dict[str, Any]:
        base_addr = cpu.registers.read(self.rn)
        address = base_addr + self.offset
        result_changes = []
        memory_changes = []
        
        if self.mnemonic == "LDUR":  # Load doubleword
            value = cpu.memory.read_doubleword(address)
            if cpu.registers.write(self.rt, value):
                result_changes.append(self.rt)
            memory_changes.append((address, "read", value))
            
        elif self.mnemonic == "STUR":  # Store doubleword
            value = cpu.registers.read(self.rt)
            cpu.memory.write_doubleword(address, value)
            memory_changes.append((address, "write", value))
            
        elif self.mnemonic == "LDURW":  # Load word
            value = cpu.memory.read_word(address)
            if cpu.registers.write(self.rt, value):
                result_changes.append(self.rt)
            memory_changes.append((address, "read", value))
            
        elif self.mnemonic == "STURW":  # Store word
            value = cpu.registers.read(self.rt) & 0xFFFFFFFF  # Mask to 32 bits
            cpu.memory.write_word(address, value)
            memory_changes.append((address, "write", value))
            
        elif self.mnemonic == "LDURB":  # Load byte
            value = cpu.memory.read_byte(address)
            if cpu.registers.write(self.rt, value):
                result_changes.append(self.rt)
            memory_changes.append((address, "read", value))
            
        elif self.mnemonic == "STURB":  # Store byte
            value = cpu.registers.read(self.rt) & 0xFF  # Mask to 8 bits
            cpu.memory.write_byte(address, value)
            memory_changes.append((address, "write", value))
            
        else:
            raise ValueError(f"Unsupported D-type instruction: {self.mnemonic}")
            
        return {
            "register_changes": result_changes,
            "memory_changes": memory_changes
        }


class BTypeInstruction(Instruction):
    """B-type instructions (unconditional branch)"""
    
    def __init__(self, mnemonic: str, target_label: str, line_number: int = 0):
        super().__init__(mnemonic, [target_label], line_number)
        self.target_label = target_label
        self.target_address = None  # Will be resolved during parsing
        self.instruction_type = InstructionType.B_TYPE
        
    def execute(self, cpu) -> Dict[str, Any]:
        if self.target_address is None:
            raise ValueError(f"Branch target '{self.target_label}' not resolved")
            
        # Set PC to target address
        cpu.pc = self.target_address
        
        return {
            "pc_modified": True,
            "register_changes": [],
            "memory_changes": []
        }


class BLTypeInstruction(Instruction):
    """BL-type instructions (branch and link)"""
    
    def __init__(self, mnemonic: str, target_label: str, line_number: int = 0):
        super().__init__(mnemonic, [target_label], line_number)
        self.target_label = target_label
        self.target_address = None  # Will be resolved during parsing
        self.instruction_type = InstructionType.BL_TYPE
        
    def execute(self, cpu) -> Dict[str, Any]:
        if self.target_address is None:
            raise ValueError(f"Branch target '{self.target_label}' not resolved")
            
        result_changes = []
        
        # Save return address (PC + 4) to Link Register (LR = X30)
        return_address = cpu.pc + 4
        if cpu.registers.write(30, return_address):  # LR is X30
            result_changes.append(30)
        
        # Set PC to target address
        cpu.pc = self.target_address
        
        return {
            "pc_modified": True,
            "register_changes": result_changes,
            "memory_changes": []
        }


class BRTypeInstruction(Instruction):
    """BR-type instructions (branch to register)"""
    
    def __init__(self, mnemonic: str, register: int, line_number: int = 0):
        super().__init__(mnemonic, [f"X{register}"], line_number)
        self.register = register
        self.instruction_type = InstructionType.BR_TYPE
        
    def execute(self, cpu) -> Dict[str, Any]:
        # Get target address from register
        target_address = cpu.registers.read(self.register)
        
        # Set PC to target address
        cpu.pc = target_address
        
        return {
            "pc_modified": True,
            "register_changes": [],
            "memory_changes": []
        }


class CBTypeInstruction(Instruction):
    """CB-type instructions (conditional branch on zero/not zero)"""
    
    def __init__(self, mnemonic: str, register: int, target_label: str, line_number: int = 0):
        super().__init__(mnemonic, [f"X{register}", target_label], line_number)
        self.register = register
        self.target_label = target_label
        self.target_address = None  # Will be resolved during parsing
        self.instruction_type = InstructionType.CB_TYPE
        
    def execute(self, cpu) -> Dict[str, Any]:
        if self.target_address is None:
            raise ValueError(f"Branch target '{self.target_label}' not resolved")
            
        reg_value = cpu.registers.read(self.register)
        should_branch = False
        
        if self.mnemonic == "CBZ":
            should_branch = (reg_value == 0)
        elif self.mnemonic == "CBNZ":
            should_branch = (reg_value != 0)
        else:
            raise ValueError(f"Unsupported CB-type instruction: {self.mnemonic}")
            
        if should_branch:
            cpu.pc = self.target_address
            return {"pc_modified": True, "register_changes": [], "memory_changes": []}
        else:
            return {"pc_modified": False, "register_changes": [], "memory_changes": []}


class CondBTypeInstruction(Instruction):
    """Conditional branch instructions using flags (B.EQ, B.NE, etc.)"""
    
    def __init__(self, mnemonic: str, condition: str, target_label: str, line_number: int = 0):
        super().__init__(f"{mnemonic}.{condition}", [target_label], line_number)
        self.condition = condition.upper()
        self.target_label = target_label
        self.target_address = None  # Will be resolved during parsing
        self.instruction_type = InstructionType.COND_B_TYPE
        
    def execute(self, cpu) -> Dict[str, Any]:
        if self.target_address is None:
            raise ValueError(f"Branch target '{self.target_label}' not resolved")
            
        should_branch = self._check_condition(cpu.flags)
        
        if should_branch:
            cpu.pc = self.target_address
            return {"pc_modified": True, "register_changes": [], "memory_changes": []}
        else:
            return {"pc_modified": False, "register_changes": [], "memory_changes": []}
            
    def _check_condition(self, flags: Dict[str, bool]) -> bool:
        """Check if condition is met based on flags"""
        N, Z, V, C = flags['N'], flags['Z'], flags['V'], flags['C']
        
        if self.condition == "EQ":
            return Z  # Equal (zero)
        elif self.condition == "NE":
            return not Z  # Not equal (not zero)
        elif self.condition == "LT":
            return N != V  # Less than (signed)
        elif self.condition == "LE":
            return (N != V) or Z  # Less than or equal (signed)
        elif self.condition == "GT":
            return (not Z) and (N == V)  # Greater than (signed)
        elif self.condition == "GE":
            return N == V  # Greater than or equal (signed)
        elif self.condition == "LO":
            return not C  # Less than (unsigned)
        elif self.condition == "LS":
            return (not C) or Z  # Less than or equal (unsigned)
        elif self.condition == "HI":
            return C and (not Z)  # Greater than (unsigned)
        elif self.condition == "HS":
            return C  # Greater than or equal (unsigned)
        else:
            raise ValueError(f"Unsupported condition: {self.condition}")
