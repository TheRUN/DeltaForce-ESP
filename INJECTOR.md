# DLL Injector - Educational Documentation

## ⚠️ CRITICAL DISCLAIMER

**THIS IS AN EDUCATIONAL PROJECT FOR LEARNING PURPOSES ONLY**

DLL injection is a powerful technique that can be used for both legitimate and malicious purposes. This implementation is designed to teach:
- Windows API programming
- Process memory management
- Security implications of code injection
- Debugging and analysis techniques

**DO NOT:**
- Use this in online multiplayer games
- Violate any software's terms of service
- Use for malicious purposes
- Distribute for unauthorized modification of software

**Legal Notice:** Unauthorized code injection may be illegal in your jurisdiction and can result in account bans, legal action, or criminal charges. Use responsibly in controlled, authorized environments only.

---

## What is DLL Injection?

DLL (Dynamic Link Library) injection is a technique where you insert code from a DLL into the address space of another running process. The injected DLL then executes within the context of that process.

### Legitimate Uses

1. **Debugging Tools**: Debuggers like Visual Studio inject DLLs to monitor and control applications
2. **Profiling**: Performance profilers inject code to measure execution time
3. **Anti-Cheat Systems**: Game protection systems inject monitoring code
4. **Security Research**: Analyzing malware behavior in sandboxed environments
5. **Accessibility Tools**: Screen readers and automation tools

### How It Works

```
┌─────────────────────────────────────────────┐
│         DLL Injection Process               │
└─────────────────────────────────────────────┘

1. Injector Process (This Tool)
   └─> Opens target process
       └─> Allocates memory in target
           └─> Writes DLL path to memory
               └─> Creates remote thread
                   └─> Thread calls LoadLibrary
                       └─> DLL loaded into target

┌────────────────┐        ┌────────────────┐
│  Your Injector │───────>│ Target Process │
│    (This App)  │ Inject │   (Game/App)   │
└────────────────┘        └────────────────┘
                               │
                               ├─> Your DLL Code Runs Here
                               └─> Can access game memory
```

## Features

### Injection Methods

#### 1. LoadLibrary Injection (Implemented)

**How it works:**
1. Open target process with `OpenProcess`
2. Allocate memory with `VirtualAllocEx`
3. Write DLL path with `WriteProcessMemory`
4. Get address of `LoadLibraryA` in kernel32.dll
5. Create remote thread with `CreateRemoteThread` calling LoadLibrary
6. LoadLibrary loads your DLL into the target process

**Advantages:**
- Simple and reliable
- Windows handles most of the work
- Easy to implement

**Disadvantages:**
- Easy to detect by anti-cheat
- Creates suspicious remote thread
- Limited stealth

#### 2. Manual Mapping (Placeholder)

Manual mapping is an advanced technique where you manually map the PE file into memory:
- Parse PE headers
- Map sections manually
- Resolve imports
- Fix relocations
- Call entry point

This is much more complex but harder to detect.

## Usage

### GUI Application

Run the GUI for an easy-to-use interface:

```bash
python injector_gui.py
```

**Steps:**
1. Select target process from the list
2. Browse and select your DLL file
3. Choose injection method
4. Click "Inject DLL"

### Programmatic Usage

```python
from injector import DLLInjector, InjectionMethod

# Create injector
injector = DLLInjector()

# Inject DLL
success, message = injector.inject_dll(
    process_id=1234,
    dll_path="C:/path/to/your.dll",
    method=InjectionMethod.LOAD_LIBRARY
)

if success:
    print(f"Injection successful: {message}")
else:
    print(f"Injection failed: {message}")
```

## Requirements

### System Requirements
- Windows OS (Vista or later)
- Python 3.8+
- Administrator privileges (for some injections)

### Python Dependencies
```bash
pip install psutil  # For process enumeration
```

## Creating a DLL to Inject

Here's a simple example DLL in C++:

```cpp
// example.cpp
#include <windows.h>
#include <iostream>

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
    switch (ul_reason_for_call) {
    case DLL_PROCESS_ATTACH:
        // DLL loaded - your code here
        MessageBoxA(NULL, "DLL Injected!", "Success", MB_OK);
        
        // Create a thread for your code
        CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)MainThread, NULL, 0, NULL);
        break;
        
    case DLL_PROCESS_DETACH:
        // DLL unloaded
        break;
    }
    return TRUE;
}

DWORD WINAPI MainThread(LPVOID param) {
    // Your main code here
    // Can access game memory, hook functions, etc.
    
    while (true) {
        // Do something
        Sleep(100);
    }
    
    return 0;
}
```

Compile with:
```bash
cl /LD example.cpp /link /OUT:example.dll
```

## Technical Details

### Windows API Functions Used

**Process Manipulation:**
- `OpenProcess` - Opens a handle to a process
- `OpenProcessToken` - Opens access token of a process
- `VirtualAllocEx` - Allocates memory in another process
- `VirtualFreeEx` - Frees allocated memory
- `WriteProcessMemory` - Writes data to another process
- `ReadProcessMemory` - Reads data from another process

**Thread Management:**
- `CreateRemoteThread` - Creates a thread in another process
- `WaitForSingleObject` - Waits for thread to finish
- `GetExitCodeThread` - Gets thread exit code

**Privilege Management:**
- `LookupPrivilegeValueW` - Gets privilege LUID
- `AdjustTokenPrivileges` - Enables/disables privileges

**Module Management:**
- `GetModuleHandleW` - Gets handle to loaded module
- `GetProcAddress` - Gets address of exported function

### SeDebugPrivilege

The injector requests SeDebugPrivilege, which allows:
- Opening any process regardless of security descriptor
- Reading/writing memory of protected processes
- Required for injecting into some processes

This privilege is only granted to administrators.

### Memory Layout

```
Target Process Memory Space:
┌─────────────────────────────────────┐
│  0x00000000 - 0x7FFFFFFF            │ User Space
│  ├── Executable (.exe)              │
│  ├── Loaded DLLs                    │
│  │   ├── kernel32.dll               │
│  │   ├── ntdll.dll                  │
│  │   └── user32.dll                 │
│  ├── [Your Injected DLL] ← HERE    │
│  └── Heap/Stack                     │
│                                      │
│  0x80000000 - 0xFFFFFFFF            │ Kernel Space
│  └── Operating System               │
└─────────────────────────────────────┘
```

## Troubleshooting

### "Failed to open process"
**Solution:** Run the injector as Administrator. Right-click and select "Run as administrator"

### "Failed to enable debug privilege"
**Solution:** You need administrator rights. Also ensure you're running on Windows.

### "LoadLibrary failed in target process"
**Possible causes:**
1. DLL architecture mismatch (32-bit vs 64-bit)
2. DLL has missing dependencies
3. DLL exports are invalid
4. Target process doesn't allow injection

**Solution:** 
- Ensure DLL is same architecture as target (both 32-bit or both 64-bit)
- Check DLL with Dependency Walker
- Test DLL in a simple test application first

### "Access Denied"
**Solution:** Some processes are protected:
- System processes (csrss.exe, lsass.exe)
- Protected processes (anti-cheat protected games)
- Run injector as Administrator

### DLL injected but nothing happens
**Possible causes:**
1. DLL doesn't have DllMain
2. DLL crashes immediately
3. DLL has bugs

**Solution:**
- Add logging to your DLL (write to file)
- Use a debugger to attach to target process
- Test your DLL in isolation first

## Security Implications

### Detection Methods

Anti-cheat systems can detect injection via:
1. **CreateRemoteThread detection** - Monitors thread creation
2. **Module enumeration** - Checks loaded DLLs
3. **Memory scanning** - Scans for suspicious code patterns
4. **Behavioral analysis** - Monitors API calls

### Protection Against Injection

Applications can protect against injection:
1. **Code signing** - Only load signed DLLs
2. **Protected processes** - Use Protected Process Light (PPL)
3. **Hook detection** - Monitor for API hooks
4. **Memory protection** - Use guard pages and memory encryption

## Educational Exercises

### Exercise 1: Process Explorer
Create a DLL that enumerates all modules loaded in a process:
```cpp
HMODULE modules[1024];
DWORD cbNeeded;
EnumProcessModules(GetCurrentProcess(), modules, sizeof(modules), &cbNeeded);
```

### Exercise 2: Function Hooking
Hook a Windows API function to intercept calls:
```cpp
// Learn about Microsoft Detours or similar hooking libraries
```

### Exercise 3: Memory Scanner
Read and search memory of target process for specific patterns.

## Related Concepts

- **API Hooking**: Intercepting API calls
- **Code Caves**: Finding unused memory to inject code
- **Shellcode Injection**: Injecting raw assembly code
- **Process Hollowing**: Replacing a legitimate process
- **Reflective DLL Injection**: DLL loads itself

## References

### Documentation
- [Microsoft Process and Thread Functions](https://docs.microsoft.com/en-us/windows/win32/procthread/)
- [Windows Memory Management](https://docs.microsoft.com/en-us/windows/win32/memory/)
- [PE Format Specification](https://docs.microsoft.com/en-us/windows/win32/debug/pe-format)

### Learning Resources
- **Books:**
  - "Windows Internals" by Mark Russinovich
  - "Reversing: Secrets of Reverse Engineering" by Eldad Eilam
  
- **Articles:**
  - DLL Injection Techniques (Guided Hacking)
  - Windows API Programming (MSDN)

### Tools for Learning
- **Process Monitor** - Monitor process activity
- **Process Explorer** - View loaded DLLs
- **Dependency Walker** - Analyze DLL dependencies
- **API Monitor** - Monitor API calls
- **x64dbg** - Debugger for examining processes

## Best Practices

1. **Always test in a VM or sandbox first**
2. **Use meaningful error messages**
3. **Clean up resources (handles, memory)**
4. **Validate all inputs**
5. **Handle errors gracefully**
6. **Log operations for debugging**
7. **Only inject into processes you own or have permission**

## Legal and Ethical Considerations

### Legal Uses
✅ Testing your own applications
✅ Educational experiments in controlled environments
✅ Authorized security research
✅ With explicit permission from software owner

### Illegal Uses
❌ Cheating in online games
❌ Cracking software protections
❌ Stealing data from other processes
❌ Modifying software without authorization
❌ Violating terms of service

**Remember:** With great power comes great responsibility. Use this knowledge ethically and legally.

## Support

For educational questions:
- Review the code comments
- Check Windows API documentation
- Study security research papers
- Join programming communities (legally focused)

---

**Final Reminder:** This tool is for educational purposes only. Always use responsibly and legally.
