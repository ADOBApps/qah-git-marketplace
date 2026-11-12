# Post Process Plotter

Plot and analyse post-processing output for **Quantum ESPRESSO**, **CP2K** and
**VASP**: DOS, PDOS, band structures, potentials and volumetric fields.

Version 1.1.1 adds a pure-Python VASP field layer (streaming reader; correct
VASP augmentation-occupancy parsing). No Perl, no VTST scripts and
no external executables are needed.

## Tabs

| Tab | Input | What it gives |
|---|---|---|
| Band Structure | QE / CP2K band files | band plot |
| DOS | QE / CP2K DOS | total DOS |
| PDOS | QE / CP2K PDOS | projected DOS |
| Work Function | QE / CP2K potential | 1D profile and work function |
| **VASP Charge** | CHGCAR, LOCPOT, PARCHG, ELFCAR | planar averages, vacuum levels, work function, cube export |

## VASP Charge tab

1. **Browse…** a CHGCAR, LOCPOT, PARCHG or ELFCAR and press **Load**.
2. The header panel shows kind, atom counts, grid, cell volume and data blocks
   (for a spin-polarised CHGCAR: Total and Magnetization).
3. Choose the axis (a/b/c) and an optional macroscopic averaging window.
4. **Plot** shows the planar average; **Work function** adds the vacuum
   plateaus, φ = E_vac − E_F and the ionisation potential (E_vac − VBM).
5. **Export CSV…**, **Save plot…** and **Export cube…** write the results.

E_F is read from the `OUTCAR` next to the field when present; the VBM comes from
`EIGENVAL`. Both can be overridden.

Notes:

- CHGCAR stores ρ(r)·V_cell. The module reports electrons as Σvalues/N_grid and
  converts to e/Å³ by dividing by |det A|.
- Gaussian cube files are written in **bohr** with density in e/bohr³ and
  potential in Hartree (standard convention), so VESTA/ChimeraX read them
  directly.
- A work function needs `LVHAR = .TRUE.` (and, for an asymmetric slab,
  `LDIPOL`/`IDIPOL`) to be publication-grade. The tab warns when the two vacuum
  plateaus differ by more than 0.2 eV.

## Command line

`vasp_charge.py` also runs standalone:

```bash
python vasp_charge.py info LOCPOT
python vasp_charge.py avg LOCPOT --axis c --csv profile.csv
python vasp_charge.py workfunction LOCPOT            # uses OUTCAR/EIGENVAL
python vasp_charge.py workfunction LOCPOT --fermi -1.30
python vasp_charge.py cube CHGCAR density.cube       # bohr / e/bohr^3
python vasp_charge.py sum A B CHGCAR_sum
python vasp_charge.py diff reference CHGCAR CHGCAR_diff
```

`sum` and `diff` keep the VASP header and augmentation-occupancy sections, so
the output is a readable CHGCAR, not just a plotting array.

## Tests

```bash
TIO2_SN_VASP=~/TiO2-Sn/vasp python test_vasp_charge.py
```

Builds synthetic spin-polarised CHGCARs (round trip, arithmetic, cube, periodic
interpolation) and checks four real LOCPOT files against the work functions in
`TiO2-Sn/vasp/analysis/work_function.py`.

## Documentation

- `docs/documentation.pdf` — user manual (5 pages): GUI, CLI, VASP format,
  units, validation, limitations, credits.
- `docs/documentation.tex` + `docs/references.bib` — LaTeX sources; rebuild with
  `cd docs && pdflatex documentation && bibtex documentation && pdflatex documentation && pdflatex documentation`.
- `_state/` — **git-ignored** working state for the next agent (`STATE.json`,
  `NOTES.md`): validation numbers, format gotchas, decisions and next steps.

## Credits

The operations implemented here were designed after studying the VTST scripts
of the **Henkelman group** (University of Texas at Austin), in particular
`chgsum.pl`, `chgdiff.pl`, `chg2cube.pl`, `chgsplit.pl` and `chgvalue.pl`.
Those scripts were used **only as a behavioural reference and numerical
oracle**: no Perl code is executed, bundled or translated. See
`docs/documentation.pdf` §8 for the full citation and references
(Henkelman 2006; Sanville 2007; Tang 2009; Yu & Trinkle 2011) and
`docs/references.bib`.

## Implementation

`vasp_charge.py` is an independent implementation of the documented VASP
formats. The Henkelman-group VTST Perl scripts (`chgsum.pl`, `chgdiff.pl`,
`chg2cube.pl`, …) are not used or copied; they served only as a numerical
oracle. See the module docstring for units and conventions.

## License

GPL-3.0-or-later, as the rest of QAH.
