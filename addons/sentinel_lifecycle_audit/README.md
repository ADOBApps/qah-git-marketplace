# Sentinel Lifecycle Audit

Static load/lifecycle audit:

- QTimer intervals below 1 s;
- `while True` loops;
- blocking `time.sleep`;
- threads without wait/stop/quit/cleanup evidence;
- `atexit.register`;
- heavy imports.

Static only. Runtime thread and timer state is not observed.
