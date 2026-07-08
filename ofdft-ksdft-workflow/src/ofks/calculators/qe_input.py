from __future__ import annotations

from typing import Any

from ase import Atoms
from ase.constraints import FixAtoms
from ase.data import atomic_masses, atomic_numbers


def render_qe_input(atoms: Atoms, config: dict[str, Any], prefix: str) -> str:
    """Render a minimal Quantum ESPRESSO pw.x input."""
    if str(config.get("backend", "")).lower() != "qe":
        raise ValueError("QE input writer requires a calculator config with backend: qe")

    symbols = _unique_symbols(atoms)
    pseudo_map = config.get("pseudopotentials", {})
    missing = [symbol for symbol in symbols if symbol not in pseudo_map]
    if missing:
        raise ValueError(f"Missing pseudopotentials for: {', '.join(missing)}")

    lines: list[str] = []
    calculation = str(config.get("calculation", "relax"))
    lines.extend(_control_block(prefix, str(config.get("pseudo_dir", "./pseudo")), config, calculation))
    lines.extend(_system_block(atoms, symbols, config))
    lines.extend(_electrons_block(config))
    if _uses_ions_block(calculation):
        lines.extend(_ions_block(config))
    lines.append("ATOMIC_SPECIES")
    for symbol in symbols:
        mass = atomic_masses[atomic_numbers[symbol]]
        lines.append(f"  {symbol} {mass:.6f} {pseudo_map[symbol]}")
    lines.append("")
    lines.append("CELL_PARAMETERS angstrom")
    for vector in atoms.cell.array:
        lines.append(f"  {vector[0]: .12f} {vector[1]: .12f} {vector[2]: .12f}")
    lines.append("")
    lines.append("ATOMIC_POSITIONS angstrom")
    fixed_indices = _fixed_indices(atoms)
    for atom in atoms:
        flags = "0 0 0" if atom.index in fixed_indices else "1 1 1"
        x, y, z = atom.position
        lines.append(f"  {atom.symbol} {x: .12f} {y: .12f} {z: .12f} {flags}")
    lines.append("")
    lines.extend(_kpoints_block(config))
    return "\n".join(lines) + "\n"


def _control_block(prefix: str, pseudo_dir: str, config: dict[str, Any], calculation: str) -> list[str]:
    lines = [
        "&CONTROL",
        f"  calculation = '{calculation}'",
        f"  prefix = '{prefix}'",
        "  outdir = './out'",
        f"  pseudo_dir = '{pseudo_dir}'",
        "  tprnfor = .true.",
        "  tstress = .true.",
    ]
    nstep = _control_nstep(config, calculation)
    if nstep is not None:
        lines.append(f"  nstep = {nstep}")
    lines.append("/")
    return lines


def _system_block(atoms: Atoms, symbols: list[str], config: dict[str, Any]) -> list[str]:
    lines = [
        "&SYSTEM",
        "  ibrav = 0",
        f"  nat = {len(atoms)}",
        f"  ntyp = {len(symbols)}",
        f"  ecutwfc = {float(config.get('ecutwfc_ry', 50.0)):.8g}",
        f"  ecutrho = {float(config.get('ecutrho_ry', 400.0)):.8g}",
        f"  input_dft = '{config.get('xc', 'PBE')}'",
    ]
    smearing = config.get("smearing") or {}
    if smearing:
        lines.extend(
            [
                "  occupations = 'smearing'",
                f"  smearing = '{smearing.get('type', 'cold')}'",
                f"  degauss = {float(smearing.get('degauss_ry', 0.02)):.8g}",
            ]
        )
    dispersion = config.get("dispersion")
    if dispersion:
        lines.append(f"  vdw_corr = '{dispersion}'")
    if config.get("dipole_correction"):
        lines.extend(
            [
                "  assume_isolated = '2D'",
            ]
        )
    lines.extend(["/"])
    return lines


def _electrons_block(config: dict[str, Any]) -> list[str]:
    electrons = config.get("electrons") or {}
    return [
        "&ELECTRONS",
        f"  conv_thr = {str(electrons.get('conv_thr', '1.0d-6'))}",
        f"  mixing_beta = {float(electrons.get('mixing_beta', 0.3)):.8g}",
        "/",
    ]


def _ions_block(config: dict[str, Any]) -> list[str]:
    relax = config.get("relax") or {}
    return [
        "&IONS",
        f"  ion_dynamics = '{relax.get('ion_dynamics', 'bfgs')}'",
        "/",
    ]


def _control_nstep(config: dict[str, Any], calculation: str) -> int | None:
    control = config.get("control") or {}
    if "nstep" in control:
        return int(control["nstep"])
    if _uses_ions_block(calculation):
        relax = config.get("relax") or {}
        if "max_steps" in relax:
            return int(relax["max_steps"])
    return None


def _uses_ions_block(calculation: str) -> bool:
    return calculation.lower() in {"relax", "vc-relax", "md", "vc-md"}


def _kpoints_block(config: dict[str, Any]) -> list[str]:
    kpoints = config.get("kpoints", [1, 1, 1])
    if len(kpoints) != 3:
        raise ValueError("QE kpoints must contain exactly three integers")
    return [
        "K_POINTS automatic",
        f"  {int(kpoints[0])} {int(kpoints[1])} {int(kpoints[2])} 0 0 0",
    ]


def _unique_symbols(atoms: Atoms) -> list[str]:
    symbols: list[str] = []
    for symbol in atoms.get_chemical_symbols():
        if symbol not in symbols:
            symbols.append(symbol)
    return symbols


def _fixed_indices(atoms: Atoms) -> set[int]:
    fixed: set[int] = set()
    for constraint in atoms.constraints:
        if isinstance(constraint, FixAtoms):
            fixed.update(int(index) for index in constraint.index)
    return fixed
