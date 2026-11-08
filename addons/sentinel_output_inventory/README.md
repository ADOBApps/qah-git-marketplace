# Sentinel Output Inventory

Read-only inventory for calculation and data folders.

Reports:

- total files and total size;
- output/data file count;
- top extensions;
- empty outputs;
- tiny/truncated outputs;
- files larger than 1 GiB;
- the largest output files.

Recognized formats include common quantum-chemistry and materials-science
extensions (`out`, `log`, `cif`, `xyz`, `cube`, `chgcar`, `vasprun.xml`,
`poscar`, `pwi`, `pwo`, `wout`, `fchk`, `molden`, `h5`, `csv`, `json`, ...).

## Use

**Plugin Sentinel -> Addons -> Sentinel Output Inventory**, pin it, add a
calculation folder or output file, and run.

## Capabilities

```text
read-files
findings
report
```

Read-only. No network, no subprocesses, no native code.
