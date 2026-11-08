# Sentinel Dangerous API Audit

Static report-only scan for high-risk Python APIs:

- `eval`, `exec`, `compile`, `__import__`;
- `pickle.load(s)`, `marshal.load(s)`, unsafe `yaml.load`;
- `os.system`, `os.popen`, `subprocess` and `shell=True`;
- `ctypes` native loading, `winreg`;
- dynamic `importlib` loading and `pty.spawn`.

Nothing is imported or executed.
