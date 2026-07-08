import pytest

from ofks.workflows.sweep_dftpy_convergence import filter_sweep_variants, render_sweep_markdown


def test_render_sweep_markdown_includes_convergence_counts():
    records = [
        {
            "variant": "wt",
            "structure_id": "abc",
            "site": "top",
            "height_angstrom": 2.0,
            "status": "ok",
            "converged": False,
            "total_energy_ev": -1.0,
            "max_force_ev_per_ang": 2.0,
            "runtime_seconds": 3.0,
            "metadata": {"density_iterations": 100},
        }
    ]

    markdown = render_sweep_markdown(records)

    assert "Converged records: 0" in markdown
    assert "| wt | abc | top | 2" in markdown


def test_filter_sweep_variants_selects_requested_order():
    variants = filter_sweep_variants("mgp_atomic_sp08_m30,wt_atomic_sp08_m100")

    assert [variant["name"] for variant in variants] == ["mgp_atomic_sp08_m30", "wt_atomic_sp08_m100"]


def test_filter_sweep_variants_rejects_unknown_name():
    with pytest.raises(Exception, match="Unknown sweep variant"):
        filter_sweep_variants("missing")
