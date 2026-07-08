import numpy as np

from pylibxc.functional import LibXCFunctional


def test_pylibxc_compat_gga_pbe_returns_dftpy_keys():
    func = LibXCFunctional("gga_x_pbe", "unpolarized")

    out = func.compute(
        {"rho": np.array([0.1, 0.2]), "sigma": np.array([0.01, 0.02])},
        do_exc=True,
        do_vxc=True,
    )

    assert set(out) == {"zk", "vrho", "vsigma"}
    assert out["zk"].shape == (2,)
    assert np.isfinite(out["zk"]).all()
