from pathlib import Path

import numpy as np

from ofks.parsers.qe import RY_PER_BOHR_TO_EV_PER_ANG, RY_TO_EV, parse_qe_output


def test_parse_qe_output_reads_last_energy_and_force_block():
    result = parse_qe_output(Path("tests/fixtures/qe/pw.out"))

    assert result.converged
    assert result.job_done
    assert result.raw_total_energy_ry == -16.0
    assert result.total_energy_ev == -16.0 * RY_TO_EV
    assert result.forces_ev_per_ang is not None
    assert result.forces_ev_per_ang.shape == (2, 3)
    assert np.isclose(result.forces_ev_per_ang[1, 2], 0.0003 * RY_PER_BOHR_TO_EV_PER_ANG)
