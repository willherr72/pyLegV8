"""
LEGv8 CPU Core Implementation
Handles the main CPU state, registers, and execution logic
"""

from typing import Dict, Any, Optional
from core.registers import RegisterFile
from core.memory import Memory
from core.instruction import Instruction


class LEGv8CPU:
    """LEGv8 CPU simulator core"""
    
    def __init__(self):
        self.registers = RegisterFile()
        self.memory = Memory()
        self.pc = 0  # Program Counter
        self.instruction_count = 0
        self.cycle_count = 0
        self.is_halted = False
        self.last_executed_instruction: Optional[Instruction] = None
        
        # Condition flags for conditional branches
        self.flags = {
            'N': False,  # Negative
            'Z': False,  # Zero
            'V': False,  # Overflow
            'C': False   # Carry
        }
        
    def reset(self):
        """Reset CPU to initial state"""
        self.registers.reset()
        self.memory.clear()
        self.pc = 0
        self.instruction_count = 0
        self.cycle_count = 0
        self.is_halted = False
        self.last_executed_instruction = None
        
        # Reset condition flags
        self.flags = {
            'N': False,  # Negative
            'Z': False,  # Zero
            'V': False,  # Overflow
            'C': False   # Carry
        }
        
    def step(self, instruction: Instruction) -> Dict[str, Any]:
        """Execute one instruction and return execution results"""
        if self.is_halted:
            return {"error": "CPU is halted"}
            
        try:
            # Store the instruction for reference
            self.last_executed_instruction = instruction
            
            # Execute the instruction
            result = instruction.execute(self)
            
            # Update counters
            self.instruction_count += 1
            self.cycle_count += 1
            
            # Increment PC (unless instruction modifies it)
            if not result.get("pc_modified", False):
                self.pc += 4
                
            return {
                "success": True,
                "pc": self.pc,
                "instruction_count": self.instruction_count,
                "cycle_count": self.cycle_count,
                "register_changes": result.get("register_changes", []),
                "memory_changes": result.get("memory_changes", [])
            }
            
        except Exception as e:
            return {"error": str(e)}
            
    def set_flags(self, result: int):
        """Set condition flags based on arithmetic result"""
        # Convert to signed 64-bit for flag calculations
        if result > 2**63 - 1:
            result = result - 2**64
        elif result < -2**63:
            result = result + 2**64
            
        self.flags['N'] = result < 0      # Negative flag
        self.flags['Z'] = result == 0     # Zero flag
        # V and C flags would require more complex overflow/carry detection
        # For now, we'll implement basic functionality
        self.flags['V'] = False  # Overflow (simplified)
        self.flags['C'] = False  # Carry (simplified)
            
    def get_state(self) -> Dict[str, Any]:
        """Get current CPU state for display"""
        return {
            "pc": self.pc,
            "registers": self.registers.get_all(),
            "instruction_count": self.instruction_count,
            "cycle_count": self.cycle_count,
            "is_halted": self.is_halted,
            "flags": self.flags.copy()
        }
