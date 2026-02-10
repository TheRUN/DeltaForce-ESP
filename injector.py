"""
DLL Injector Module for Educational Purposes
Demonstrates process injection techniques using Windows API

EDUCATIONAL DISCLAIMER:
This code is for educational purposes only. It demonstrates various
DLL injection techniques used in software development, debugging, and
security research. Do NOT use this for malicious purposes or to violate
any terms of service.

Educational Focus:
- Windows API process manipulation
- DLL injection techniques (LoadLibrary, Manual Mapping)
- Process memory management
- Security implications of code injection
"""

import ctypes
import logging
from ctypes import wintypes
from typing import Optional, Tuple
import os
from enum import Enum


class InjectionMethod(Enum):
    """Enumeration of DLL injection methods"""
    LOAD_LIBRARY = "LoadLibrary"      # Classic LoadLibrary injection
    MANUAL_MAP = "ManualMap"          # Advanced manual mapping


# Windows API constants
PROCESS_ALL_ACCESS = 0x1F0FFF
PROCESS_CREATE_THREAD = 0x0002
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_OPERATION = 0x0008
PROCESS_VM_WRITE = 0x0020
PROCESS_VM_READ = 0x0010

MEM_COMMIT = 0x1000
MEM_RESERVE = 0x2000
MEM_RELEASE = 0x8000

PAGE_READWRITE = 0x04
PAGE_EXECUTE_READWRITE = 0x40

INVALID_HANDLE_VALUE = -1

# Token privileges for elevation
TOKEN_ADJUST_PRIVILEGES = 0x0020
TOKEN_QUERY = 0x0008
SE_DEBUG_NAME = "SeDebugPrivilege"
SE_PRIVILEGE_ENABLED = 0x00000002


class LUID(ctypes.Structure):
    """Locally Unique Identifier structure"""
    _fields_ = [
        ("LowPart", wintypes.DWORD),
        ("HighPart", wintypes.LONG),
    ]


class LUID_AND_ATTRIBUTES(ctypes.Structure):
    """LUID and its attributes"""
    _fields_ = [
        ("Luid", LUID),
        ("Attributes", wintypes.DWORD),
    ]


class TOKEN_PRIVILEGES(ctypes.Structure):
    """Token privileges structure"""
    _fields_ = [
        ("PrivilegeCount", wintypes.DWORD),
        ("Privileges", LUID_AND_ATTRIBUTES * 1),
    ]


class DLLInjector:
    """
    DLL Injector class for educational demonstration of process injection.
    
    Educational Note:
    Process injection is a technique where code is inserted into the address
    space of another process. This is used legitimately for:
    - Debugging and analysis tools
    - Anti-cheat systems
    - Performance profilers
    - Security research
    
    However, it can also be misused. This implementation is for learning only.
    """
    
    def __init__(self):
        """Initialize the DLL injector"""
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        
        try:
            # Load Windows API libraries
            self.kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            self.advapi32 = ctypes.WinDLL('advapi32', use_last_error=True)
            self.ntdll = ctypes.WinDLL('ntdll', use_last_error=True)
        except Exception as e:
            self.logger.error(f"Failed to load Windows DLLs: {e}")
            raise RuntimeError("This injector requires Windows OS")
    
    def enable_debug_privilege(self) -> bool:
        """
        Enable SeDebugPrivilege for the current process.
        
        Educational Note:
        SeDebugPrivilege allows a process to debug and adjust memory of any
        process, regardless of security descriptor. This is required for
        injecting into protected processes.
        
        Returns:
            bool: True if privilege enabled successfully
        """
        try:
            # Get current process token
            h_token = wintypes.HANDLE()
            h_process = self.kernel32.GetCurrentProcess()
            
            if not self.advapi32.OpenProcessToken(
                h_process,
                TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY,
                ctypes.byref(h_token)
            ):
                self.logger.error("Failed to open process token")
                return False
            
            # Lookup privilege value
            luid = LUID()
            if not self.advapi32.LookupPrivilegeValueW(
                None,
                SE_DEBUG_NAME,
                ctypes.byref(luid)
            ):
                self.logger.error("Failed to lookup privilege value")
                self.kernel32.CloseHandle(h_token)
                return False
            
            # Set up privilege structure
            tp = TOKEN_PRIVILEGES()
            tp.PrivilegeCount = 1
            tp.Privileges[0].Luid = luid
            tp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED
            
            # Adjust token privileges
            if not self.advapi32.AdjustTokenPrivileges(
                h_token,
                False,
                ctypes.byref(tp),
                ctypes.sizeof(TOKEN_PRIVILEGES),
                None,
                None
            ):
                self.logger.error("Failed to adjust token privileges")
                self.kernel32.CloseHandle(h_token)
                return False
            
            self.kernel32.CloseHandle(h_token)
            self.logger.info("SeDebugPrivilege enabled successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error enabling debug privilege: {e}")
            return False
    
    def inject_dll_loadlibrary(
        self,
        process_id: int,
        dll_path: str
    ) -> Tuple[bool, str]:
        """
        Inject DLL using LoadLibrary method.
        
        Educational Note:
        This is the classic DLL injection technique:
        1. Open target process
        2. Allocate memory in target process
        3. Write DLL path to allocated memory
        4. Create remote thread that calls LoadLibrary with our DLL path
        
        Advantages:
        - Simple and reliable
        - LoadLibrary handles DLL loading automatically
        
        Disadvantages:
        - Easy to detect by anti-cheat systems
        - Limited stealth
        
        Args:
            process_id: Target process ID
            dll_path: Full path to DLL file
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        h_process = None
        remote_memory = None
        
        try:
            # Validate DLL path
            if not os.path.exists(dll_path):
                return False, f"DLL file not found: {dll_path}"
            
            dll_path = os.path.abspath(dll_path)
            dll_path_bytes = dll_path.encode('utf-8') + b'\x00'
            
            self.logger.info(f"Injecting {dll_path} into PID {process_id}")
            
            # Step 1: Open target process
            h_process = self.kernel32.OpenProcess(
                PROCESS_CREATE_THREAD | PROCESS_VM_OPERATION | 
                PROCESS_VM_WRITE | PROCESS_VM_READ,
                False,
                process_id
            )
            
            if not h_process or h_process == INVALID_HANDLE_VALUE:
                return False, f"Failed to open process {process_id}. Try running as administrator."
            
            self.logger.info("Process opened successfully")
            
            # Step 2: Allocate memory in target process
            remote_memory = self.kernel32.VirtualAllocEx(
                h_process,
                None,
                len(dll_path_bytes),
                MEM_COMMIT | MEM_RESERVE,
                PAGE_READWRITE
            )
            
            if not remote_memory:
                return False, "Failed to allocate memory in target process"
            
            self.logger.info(f"Memory allocated at 0x{remote_memory:X}")
            
            # Step 3: Write DLL path to allocated memory
            bytes_written = ctypes.c_size_t(0)
            if not self.kernel32.WriteProcessMemory(
                h_process,
                remote_memory,
                dll_path_bytes,
                len(dll_path_bytes),
                ctypes.byref(bytes_written)
            ):
                return False, "Failed to write DLL path to target process"
            
            self.logger.info(f"DLL path written ({bytes_written.value} bytes)")
            
            # Step 4: Get address of LoadLibraryA
            h_kernel32 = self.kernel32.GetModuleHandleW("kernel32.dll")
            load_library_addr = self.kernel32.GetProcAddress(
                h_kernel32,
                b"LoadLibraryA"
            )
            
            if not load_library_addr:
                return False, "Failed to get LoadLibraryA address"
            
            self.logger.info(f"LoadLibraryA address: 0x{load_library_addr:X}")
            
            # Step 5: Create remote thread to call LoadLibrary
            thread_id = wintypes.DWORD(0)
            h_thread = self.kernel32.CreateRemoteThread(
                h_process,
                None,
                0,
                load_library_addr,
                remote_memory,
                0,
                ctypes.byref(thread_id)
            )
            
            if not h_thread:
                return False, "Failed to create remote thread"
            
            self.logger.info(f"Remote thread created (TID: {thread_id.value})")
            
            # Wait for thread to complete
            self.kernel32.WaitForSingleObject(h_thread, 5000)  # 5 second timeout
            
            # Get thread exit code (DLL base address)
            exit_code = wintypes.DWORD(0)
            self.kernel32.GetExitCodeThread(h_thread, ctypes.byref(exit_code))
            
            self.kernel32.CloseHandle(h_thread)
            
            if exit_code.value == 0:
                return False, "LoadLibrary failed in target process"
            
            self.logger.info(f"DLL loaded at address: 0x{exit_code.value:X}")
            
            return True, f"DLL successfully injected at 0x{exit_code.value:X}"
            
        except Exception as e:
            self.logger.error(f"Injection error: {e}")
            return False, f"Injection failed: {str(e)}"
            
        finally:
            # Cleanup
            if remote_memory and h_process:
                self.kernel32.VirtualFreeEx(h_process, remote_memory, 0, MEM_RELEASE)
            if h_process:
                self.kernel32.CloseHandle(h_process)
    
    def inject_dll(
        self,
        process_id: int,
        dll_path: str,
        method: InjectionMethod = InjectionMethod.LOAD_LIBRARY
    ) -> Tuple[bool, str]:
        """
        Inject a DLL into a target process.
        
        Args:
            process_id: Target process ID
            dll_path: Full path to DLL file
            method: Injection method to use
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        # Enable debug privilege first
        if not self.enable_debug_privilege():
            self.logger.warning("Failed to enable debug privilege. Some injections may fail.")
        
        if method == InjectionMethod.LOAD_LIBRARY:
            return self.inject_dll_loadlibrary(process_id, dll_path)
        elif method == InjectionMethod.MANUAL_MAP:
            # Manual mapping is more advanced and complex
            # For educational purposes, we'll provide a placeholder
            return False, "Manual mapping not yet implemented (advanced technique)"
        else:
            return False, f"Unknown injection method: {method}"
    
    def validate_dll(self, dll_path: str) -> Tuple[bool, str]:
        """
        Validate a DLL file before injection.
        
        Educational Note:
        Important checks before injection:
        - File exists and is readable
        - File is a valid PE (Portable Executable)
        - Architecture matches (x86 vs x64)
        
        Args:
            dll_path: Path to DLL file
            
        Returns:
            Tuple of (valid: bool, message: str)
        """
        if not os.path.exists(dll_path):
            return False, "DLL file does not exist"
        
        if not dll_path.lower().endswith('.dll'):
            return False, "File must have .dll extension"
        
        try:
            # Check if file is readable
            with open(dll_path, 'rb') as f:
                # Read PE header
                header = f.read(2)
                if header != b'MZ':
                    return False, "Not a valid PE file (missing MZ signature)"
            
            return True, "DLL file is valid"
            
        except Exception as e:
            return False, f"Error validating DLL: {str(e)}"


def main():
    """Example usage of the DLL injector"""
    print("=" * 70)
    print("DLL Injector - Educational Demonstration")
    print("=" * 70)
    print()
    print("WARNING: This is for educational purposes only!")
    print("Do not use this tool for malicious purposes or to violate terms of service.")
    print()
    
    # This is just a demonstration - actual injection should be done
    # through the GUI or with proper error handling
    injector = DLLInjector()
    
    print("DLL Injector initialized.")
    print("Use the GUI (injector_gui.py) or import this module for actual injection.")
    print()
    print("Example usage:")
    print("  from injector import DLLInjector, InjectionMethod")
    print("  injector = DLLInjector()")
    print("  success, msg = injector.inject_dll(1234, 'path/to/your.dll')")
    print()


if __name__ == "__main__":
    main()
