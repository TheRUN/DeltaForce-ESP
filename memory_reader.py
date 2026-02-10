"""
Memory Reader Module for Delta Force 2025 ESP
Educational purpose: Demonstrates process memory reading and pointer arithmetic
"""

import ctypes
import struct
import logging
from typing import Optional, List, Tuple
from ctypes import wintypes

# Windows API constants
PROCESS_ALL_ACCESS = 0x1F0FFF
TH32CS_SNAPPROCESS = 0x00000002

# Windows API structures
class PROCESSENTRY32(ctypes.Structure):
    """Windows process entry structure for enumerating processes"""
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("cntUsage", wintypes.DWORD),
        ("th32ProcessID", wintypes.DWORD),
        ("th32DefaultHeapID", ctypes.POINTER(ctypes.c_ulong)),
        ("th32ModuleID", wintypes.DWORD),
        ("cntThreads", wintypes.DWORD),
        ("th32ParentProcessID", wintypes.DWORD),
        ("pcPriClassBase", ctypes.c_long),
        ("dwFlags", wintypes.DWORD),
        ("szExeFile", ctypes.c_char * 260)
    ]


class Player:
    """Represents a player entity in game memory"""
    def __init__(self):
        self.position: Tuple[float, float, float] = (0.0, 0.0, 0.0)
        self.health: int = 100
        self.team_id: int = 0
        self.is_local: bool = False
        self.is_valid: bool = False
        self.name: str = "Unknown"


class MemoryReader:
    """
    Memory reading class for interfacing with game process.
    
    Educational Focus:
    - Process enumeration and handle management
    - Memory reading with proper error handling
    - Pointer arithmetic and dereferencing
    - Data structure parsing from raw memory
    """
    
    def __init__(self, process_name: str):
        """
        Initialize the memory reader.
        
        Args:
            process_name: Name of the target process (e.g., "DeltaForce.exe")
        """
        self.process_name = process_name
        self.process_id: Optional[int] = None
        self.process_handle = None
        self.base_address: Optional[int] = None
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Load Windows API functions
        try:
            self.kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
        except Exception as e:
            self.logger.warning(f"Running on non-Windows platform: {e}")
            self.kernel32 = None
    
    def find_process(self) -> bool:
        """
        Find the target process by name.
        
        Educational Note:
        This demonstrates process enumeration using Windows API's CreateToolhelp32Snapshot.
        We iterate through all running processes to find our target.
        
        Returns:
            bool: True if process found, False otherwise
        """
        if not self.kernel32:
            self.logger.error("Kernel32 not available - Windows required")
            return False
        
        try:
            # Create snapshot of all processes
            snapshot = self.kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
            if snapshot == -1:
                self.logger.error("Failed to create process snapshot")
                return False
            
            # Initialize process entry structure
            process_entry = PROCESSENTRY32()
            process_entry.dwSize = ctypes.sizeof(PROCESSENTRY32)
            
            # Get first process
            if not self.kernel32.Process32First(snapshot, ctypes.byref(process_entry)):
                self.kernel32.CloseHandle(snapshot)
                return False
            
            # Iterate through processes
            while True:
                if process_entry.szExeFile.decode('utf-8', errors='ignore') == self.process_name:
                    self.process_id = process_entry.th32ProcessID
                    self.logger.info(f"Found process {self.process_name} with PID {self.process_id}")
                    self.kernel32.CloseHandle(snapshot)
                    return True
                
                if not self.kernel32.Process32Next(snapshot, ctypes.byref(process_entry)):
                    break
            
            self.kernel32.CloseHandle(snapshot)
            self.logger.warning(f"Process {self.process_name} not found")
            return False
            
        except Exception as e:
            self.logger.error(f"Error finding process: {e}")
            return False
    
    def attach(self) -> bool:
        """
        Attach to the target process.
        
        Educational Note:
        Opens a handle to the process with PROCESS_ALL_ACCESS permissions.
        This handle allows us to read/write the process memory.
        
        Returns:
            bool: True if successfully attached, False otherwise
        """
        if not self.process_id:
            if not self.find_process():
                return False
        
        if not self.kernel32:
            self.logger.error("Cannot attach - Windows API not available")
            return False
        
        try:
            # Open process with all access rights
            self.process_handle = self.kernel32.OpenProcess(
                PROCESS_ALL_ACCESS,
                False,
                self.process_id
            )
            
            if not self.process_handle or self.process_handle == -1:
                self.logger.error(f"Failed to open process {self.process_id}")
                return False
            
            self.logger.info(f"Successfully attached to process {self.process_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error attaching to process: {e}")
            return False
    
    def read_memory(self, address: int, size: int) -> Optional[bytes]:
        """
        Read raw bytes from process memory.
        
        Educational Note:
        Uses ReadProcessMemory API to read data from another process's address space.
        Includes error handling for invalid addresses and access violations.
        
        Args:
            address: Memory address to read from
            size: Number of bytes to read
            
        Returns:
            bytes: Read data, or None on failure
        """
        if not self.process_handle or not self.kernel32:
            return None
        
        try:
            buffer = ctypes.create_string_buffer(size)
            bytes_read = ctypes.c_size_t(0)
            
            result = self.kernel32.ReadProcessMemory(
                self.process_handle,
                ctypes.c_void_p(address),
                buffer,
                size,
                ctypes.byref(bytes_read)
            )
            
            if not result or bytes_read.value != size:
                return None
            
            return buffer.raw
            
        except Exception as e:
            self.logger.debug(f"Error reading memory at 0x{address:X}: {e}")
            return None
    
    def read_int(self, address: int) -> Optional[int]:
        """Read a 32-bit integer from memory."""
        data = self.read_memory(address, 4)
        if data:
            return struct.unpack('<i', data)[0]
        return None
    
    def read_float(self, address: int) -> Optional[float]:
        """Read a 32-bit float from memory."""
        data = self.read_memory(address, 4)
        if data:
            return struct.unpack('<f', data)[0]
        return None
    
    def read_vec3(self, address: int) -> Optional[Tuple[float, float, float]]:
        """
        Read a 3D vector (x, y, z) from memory.
        
        Educational Note:
        3D positions are typically stored as three consecutive floats (12 bytes).
        This is common in game engines for representing coordinates.
        
        Args:
            address: Memory address of the vector
            
        Returns:
            Tuple of (x, y, z) coordinates, or None on failure
        """
        data = self.read_memory(address, 12)
        if data:
            return struct.unpack('<fff', data)
        return None
    
    def read_pointer(self, base_address: int, offsets: List[int]) -> Optional[int]:
        """
        Read a pointer chain (multi-level pointer).
        
        Educational Note:
        Games often use pointer chains: Base -> Offset1 -> Offset2 -> Final Value
        Each step requires dereferencing a pointer and adding an offset.
        
        Args:
            base_address: Starting address
            offsets: List of offsets to follow
            
        Returns:
            Final address, or None on failure
        """
        if not self.kernel32:
            return None
            
        address = base_address
        
        for offset in offsets[:-1]:
            address = self.read_int(address + offset)
            if address is None or address == 0:
                return None
        
        return address + offsets[-1]
    
    def get_local_player(self) -> Optional[Player]:
        """
        Read local player data from memory.
        
        Educational Note:
        This is a placeholder that demonstrates the structure.
        Real implementation would use actual game offsets.
        
        Returns:
            Player object with local player data, or None
        """
        # This is a mock implementation for educational purposes
        # Real implementation would read from actual game memory offsets
        player = Player()
        player.is_local = True
        player.is_valid = True
        player.position = (0.0, 0.0, 0.0)
        player.health = 100
        player.team_id = 1
        player.name = "Local Player"
        
        return player
    
    def get_player_list(self) -> List[Player]:
        """
        Read all player entities from memory.
        
        Educational Note:
        Games typically store players in arrays or linked lists.
        We iterate through the structure and parse each player entity.
        
        Returns:
            List of Player objects
        """
        # Mock implementation for educational purposes
        # Real implementation would iterate through actual game's player list
        players = []
        
        # Example: create mock players for demonstration
        for i in range(3):
            player = Player()
            player.is_valid = True
            player.position = (float(i * 100), float(i * 50), 0.0)
            player.health = 100 - (i * 20)
            player.team_id = i % 2
            player.name = f"Player {i+1}"
            players.append(player)
        
        return players
    
    def get_view_matrix(self) -> Optional[List[float]]:
        """
        Read the view matrix from game memory.
        
        Educational Note:
        The view matrix (4x4) is used to transform 3D world coordinates
        to 2D screen coordinates. It's essential for ESP rendering.
        
        Returns:
            16-element list representing 4x4 matrix, or None
        """
        # Mock implementation - returns identity-like matrix
        # Real implementation would read from actual game memory
        return [
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0
        ]
    
    def detach(self):
        """Close the process handle and clean up."""
        if self.process_handle and self.kernel32:
            self.kernel32.CloseHandle(self.process_handle)
            self.process_handle = None
            self.logger.info("Detached from process")
    
    def __del__(self):
        """Destructor to ensure proper cleanup."""
        self.detach()
