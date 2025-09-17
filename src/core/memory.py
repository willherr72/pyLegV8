"""
LEGv8 Memory Implementation
Simulates system memory for the LEGv8 processor
"""

from typing import Dict, List, Tuple, Optional


class Memory:
    """Simulated memory for LEGv8"""
    
    def __init__(self, size: int = 1024 * 1024):  # 1MB default
        self.size = size
        self._memory: Dict[int, int] = {}  # Sparse memory representation
        self._last_accessed: List[Tuple[int, str]] = []  # (address, operation) pairs
        
    def clear(self):
        """Clear all memory"""
        self._memory.clear()
        self._last_accessed.clear()
        
    def read_byte(self, address: int) -> int:
        """Read a byte from memory"""
        self._check_address(address)
        value = self._memory.get(address, 0)
        self._last_accessed.append((address, "read"))
        return value
        
    def write_byte(self, address: int, value: int):
        """Write a byte to memory"""
        self._check_address(address)
        if not (0 <= value <= 255):
            raise ValueError(f"Byte value must be 0-255, got {value}")
        self._memory[address] = value
        self._last_accessed.append((address, "write"))
        
    def read_word(self, address: int) -> int:
        """Read a 32-bit word from memory (little-endian)"""
        if address % 4 != 0:
            raise ValueError(f"Word access must be aligned to 4 bytes, address: {address}")
            
        bytes_data = []
        for i in range(4):
            bytes_data.append(self.read_byte(address + i))
            
        # Combine bytes in little-endian order
        value = (bytes_data[3] << 24) | (bytes_data[2] << 16) | (bytes_data[1] << 8) | bytes_data[0]
        return self._to_signed_32(value)
        
    def write_word(self, address: int, value: int):
        """Write a 32-bit word to memory (little-endian)"""
        if address % 4 != 0:
            raise ValueError(f"Word access must be aligned to 4 bytes, address: {address}")
            
        # Normalize to 32-bit
        value = self._to_unsigned_32(value)
        
        # Split into bytes (little-endian)
        bytes_data = [
            value & 0xFF,
            (value >> 8) & 0xFF,
            (value >> 16) & 0xFF,
            (value >> 24) & 0xFF
        ]
        
        for i, byte_val in enumerate(bytes_data):
            self.write_byte(address + i, byte_val)
            
    def read_doubleword(self, address: int) -> int:
        """Read a 64-bit doubleword from memory (little-endian)"""
        if address % 8 != 0:
            raise ValueError(f"Doubleword access must be aligned to 8 bytes, address: {address}")
            
        bytes_data = []
        for i in range(8):
            bytes_data.append(self.read_byte(address + i))
            
        # Combine bytes in little-endian order
        value = 0
        for i in range(8):
            value |= (bytes_data[i] << (i * 8))
            
        return self._to_signed_64(value)
        
    def write_doubleword(self, address: int, value: int):
        """Write a 64-bit doubleword to memory (little-endian)"""
        if address % 8 != 0:
            raise ValueError(f"Doubleword access must be aligned to 8 bytes, address: {address}")
            
        # Normalize to 64-bit
        value = self._to_unsigned_64(value)
        
        # Split into bytes (little-endian)
        for i in range(8):
            byte_val = (value >> (i * 8)) & 0xFF
            self.write_byte(address + i, byte_val)
            
    def get_used_addresses(self) -> List[int]:
        """Get list of all addresses that have been written to"""
        return sorted(self._memory.keys())
        
    def get_memory_dump(self, start_addr: int = 0, size: int = 256) -> Dict[int, int]:
        """Get memory dump for display"""
        dump = {}
        for addr in range(start_addr, start_addr + size, 4):
            if any(addr + i in self._memory for i in range(4)):
                try:
                    dump[addr] = self.read_word(addr)
                except:
                    # If we can't read a full word, show individual bytes
                    dump[addr] = self._memory.get(addr, 0)
        return dump
        
    def get_recent_accesses(self, count: int = 10) -> List[Tuple[int, str]]:
        """Get recent memory accesses"""
        return self._last_accessed[-count:]
        
    def _check_address(self, address: int):
        """Validate memory address"""
        if not (0 <= address < self.size):
            raise ValueError(f"Memory address out of bounds: {address}")
            
    def _to_signed_32(self, value: int) -> int:
        """Convert unsigned 32-bit to signed"""
        if value >= 2**31:
            return value - 2**32
        return value
        
    def _to_unsigned_32(self, value: int) -> int:
        """Convert signed 32-bit to unsigned"""
        return value & 0xFFFFFFFF
        
    def _to_signed_64(self, value: int) -> int:
        """Convert unsigned 64-bit to signed"""
        if value >= 2**63:
            return value - 2**64
        return value
        
    def _to_unsigned_64(self, value: int) -> int:
        """Convert signed 64-bit to unsigned"""
        return value & 0xFFFFFFFFFFFFFFFF
