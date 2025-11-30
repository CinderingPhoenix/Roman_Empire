# testproj - Python front-end for C++ backend

This workspace contains a small C++ program that prints player stats and a Python GUI that can run the exe, parse its output, and display the results.

Files added by the GUI scaffold:
- `ui_run_testproj.py` - PySide6 GUI that runs `testproj.exe`, attempts `--json` then falls back to text parsing, shows the raw output, a parsed table, and a small bar chart for rate stats.
- `requirements.txt` - Python dependencies (PySide6, matplotlib)

Quick start (PowerShell):

1. Install Python dependencies:

```powershell
python -m pip install -r requirements.txt
```

2. Run the GUI (make sure `testproj.exe` is present in the same folder or update the path in the script):

```powershell
python ui_run_testproj.py
```

Notes & next steps
- For robust machine-to-machine integration, modify `tstprjfl.cpp` to support a `--json` flag and print JSON. The GUI will automatically use JSON if present.
- For tighter integration (no exe parse), consider compiling your logic into a DLL and calling from Python via `ctypes` or write pybind11 bindings for a Python-native module.
- If you want, I can prepare the JSON-printing patch and/or a pybind11 wrapper next.
