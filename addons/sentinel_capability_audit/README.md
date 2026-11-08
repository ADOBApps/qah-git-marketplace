# Sentinel Capability Audit

Compares declared `capabilities` with static source evidence:

- network, subprocess, native/ctypes, registry;
- filesystem writes, credentials, persistence;
- dynamic code, GUI and database.

Reports undeclared capability evidence and declared capabilities without static
evidence. Static only; dynamic code may be missed.
