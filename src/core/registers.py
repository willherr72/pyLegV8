"""
LEGv8 Register File Implementation
Manages the 32 general-purpose registers and special registers
"""

from typing import Dict, List, Optional


class RegisterFile:
    """LEGv8 register file with 31 general purpose registers + zero register"""
    
    def __init__(self):
        # 32 64-bit registers (X0-X31)
        # X31 is the zero register (always 0)
        # X30 is the link register (LR)
        # X29 is the frame pointer (FP) 
        # X28 is the stack pointer (SP) - though SP is usually separate
        self._registers = [0] * 32
        self._last_modified: List[Optional[int]] = [None] * 32
        self._modification_counter = 0
        
    def reset(self):
        """Reset all registers to zero"""
        self._registers = [0] * 32
        self._last_modified = [None] * 32
        self._modification_counter = 0
        
    def read(self, reg_num: int) -> int:
        """Read value from register"""
        if not (0 <= reg_num <= 31):
            raise ValueError(f"Invalid register number: {reg_num}")
        return self._registers[reg_num]
        
    def write(self, reg_num: int, value: int) -> bool:
        """Write value to register. Returns True if register was actually modified."""
        if not (0 <= reg_num <= 31):
            raise ValueError(f"Invalid register number: {reg_num}")
            
        # X31 is always zero
        if reg_num == 31:
            return False
            
        # Ensure value fits in 64-bit signed integer
        value = self._normalize_64bit(value)
        
        if self._registers[reg_num] != value:
            self._registers[reg_num] = value
            self._modification_counter += 1
            self._last_modified[reg_num] = self._modification_counter
            return True
        return False
        
    def _normalize_64bit(self, value: int) -> int:
        """Normalize value to 64-bit signed integer"""
        # Handle overflow/underflow
        if value > 2**63 - 1:
            value = value - 2**64
        elif value < -2**63:
            value = value + 2**64
        return value
        
    def get_all(self) -> List[int]:
        """Get all register values"""
        return self._registers.copy()
        
    def get_register_names(self) -> List[str]:
        """Get standard register names"""
        names = []
        for i in range(32):
            if i == 28:
                names.append(f"X{i} (SP)")
            elif i == 29:
                names.append(f"X{i} (FP)")
            elif i == 30:
                names.append(f"X{i} (LR)")
            elif i == 31:
                names.append(f"X{i} (XZR)")
            else:
                names.append(f"X{i}")
        return names
        
    def get_recently_modified(self, count: int = 5) -> List[int]:
        """Get list of recently modified register numbers"""
        # Sort by modification time (most recent first)
        modified_regs = []
        for i, mod_time in enumerate(self._last_modified):
            if mod_time is not None:
                modified_regs.append((i, mod_time))
        
        modified_regs.sort(key=lambda x: x[1], reverse=True)
        return [reg_num for reg_num, _ in modified_regs[:count]]
        
    def was_recently_modified(self, reg_num: int, within_steps: int = 1) -> bool:
        """Check if register was modified within the last N steps"""
        if self._last_modified[reg_num] is None:
            return False
        return (self._modification_counter - self._last_modified[reg_num]) < within_steps
