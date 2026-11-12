# Post Process Plotter

Post-processing workbench for **VASP**, **Quantum ESPRESSO** and **CP2K**:
band structures, DOS, PDOS, potentials and work functions, plus volumetric VASP
fields (CHGCAR/LOCPOT/PARCHG/ELFCAR).

Pure Python (NumPy + matplotlib). No Perl, no VTST scripts and no external
executables at runtime.

## Tabs

| Tab | Input | What it gives |
|---|---|---|
| Band Structure | QE / CP2K band files | band plot |
| DOS | QE / CP2K DOS | total DOS |
| PDOS | QE / CP2K PDOS | projected DOS |
| Work Function | QE / CP2K potential | 1D profile and work function |
| **VASP Charge** | CHGCAR, LOCPOT, PARCHG, ELFCAR | planar averages, vacuum levels, work function, cube export |

Every tab is wrapped in a scroll area and stays usable at 700 × 500.

## Terminal CLI

`post_process_cli.py` works without Qt or QAH:

```bash
python post_process_cli.py doctor
python post_process_cli.py detect LOCPOT

# band structure / DOS / PDOS / potential (QE or CP2K)
python post_process_cli.py bands bands.gnu --csv bands.csv --plot bands.png
python post_process_cli.py dos dos.dat --csv dos.csv
python post_process_cli.py pdos pdos.dat --plot pdos.pdf
python post_process_cli.py potential pot.dat --plot pot.png

# VASP volumetric fields
python post_process_cli.py vasp info CHGCAR
python post_process_cli.py vasp avg LOCPOT --axis c --csv profile.csv
python post_process_cli.py vasp workfunction LOCPOT
python post_process_cli.py vasp cube CHGCAR density.cube
python post_process_cli.py vasp sum A B CHGCAR_sum
python post_process_cli.py vasp diff reference CHGCAR CHGCAR_diff
```

Every data command supports `--json`, `--csv FILE`, `--plot FILE` and `--dpi`.

## VASP Charge tab

1. **Browse…** a CHGCAR, LOCPOT, PARCHG or ELFCAR and press **Load**. Large
   files are read in a worker thread; a **progress bar** and a **Cancel** button
   appear while the grid is parsed (a 934 MB, 53.8 M-point CHGCAR takes ~40 s).
2. The header panel shows kind, atom counts, grid, cell volume and data blocks
   (for a spin-polarised CHGCAR: Total and Magnetization).
3. Choose the axis (a/b/c) and an optional macroscopic averaging window.
4. **Plot** shows the planar average; **Work function** adds the vacuum
   plateaus, φ = E_vac − E_F and the ionisation potential (E_vac − VBM).
5. **Export CSV…**, **Save plot…** and **Export cube…** write the results.

E_F is read from the `OUTCAR` next to the field; the VBM comes from `EIGENVAL`.
Both can be overridden.

Notes:

- CHGCAR stores ρ(r)·V_cell. Electrons are Σvalues/N_grid; e/Å³ = value/volume.
- Cube files are written in **bohr** (density e/bohr³, potential Hartree), so
  VESTA/ChimeraX read them directly.
- A work function needs `LVHAR = .TRUE.` and, for an asymmetric slab,
  `LDIPOL`/`IDIPOL`. The tab warns when the vacuum plateaus differ by more than
  0.2 eV.

## Tests

```bash
python3 test_vasp_charge.py          # reader/writer/analysis (synthetic + real)
TIO2_SN_VASP=~/TiO2-Sn/vasp python3 test_vasp_charge.py
python3 test_cli.py                  # CLI + analyzer (synthetic, optional real)
TIO2_SN_VASP=~/TiO2-Sn/vasp python3 test_cli.py
```

## Documentation

- `docs/documentation.pdf` — user manual: GUI, CLI, VASP format, units,
  validation, limitations, credits.
- `docs/documentation.tex` + `docs/references.bib` — LaTeX sources. Rebuild:
  `cd docs && pdflatex documentation && bibtex documentation && pdflatex documentation && pdflatex documentation`.
- `.state/` — **git-ignored and hidden** working state for the next agent
  (`STATE.json`, `NOTES.md`): validation numbers, format traps, decisions,
  next steps. Hidden paths are skipped by the marketplace packager.

## Credits

The VASP operations were designed after studying the VTST scripts of the
**Henkelman group** (University of Texas at Austin), in particular
`chgsum.pl`, `chgdiff.pl`, `chg2cube.pl`, `chgsplit.pl` and `chgvalue.pl`.
Those scripts were used **only as a behavioural reference and numerical
oracle**: no Perl code is executed, bundled or translated. See
`docs/documentation.pdf` §8 for the citation and references
(Henkelman 2006; Sanville 2007; Tang 2009; Yu & Trinkle 2011) and
`docs/references.bib`.

## Implementation

`vasp_charge.py` is an independent implementation of the documented VASP
formats. The reader streams the grid (a 934 MB CHGCAR with 53.8 M points and
432 augmentation sections reads in ~40 s at 457 MB peak), preserves the
augmentation sections when writing, handles non-orthogonal cells and
spin-polarised blocks, and converts to Gaussian cube.

## License

GPL-3.0-or-later, as the rest of QAH.
