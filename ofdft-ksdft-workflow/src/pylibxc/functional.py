from __future__ import annotations

import ctypes
import ctypes.util
import os
from pathlib import Path
from typing import Any

import numpy as np


XC_UNPOLARIZED = 1
XC_POLARIZED = 2


class LibXCFunctional:
    """Minimal pylibxc-compatible wrapper backed by libxc's C API.

    This intentionally implements only the API surface used by DFTpy for
    LDA/GGA semilocal functionals. Meta-GGA, spin-polarized calculations, and
    higher derivatives should use a full pylibxc binding.
    """

    def __init__(self, name: str, polarization: str = "unpolarized"):
        self.name = name.lower()
        self.polarization = polarization.lower()
        if self.polarization not in {"unpolarized", "polarized"}:
            raise ValueError(f"Unsupported LibXC polarization: {polarization}")
        self._needs_laplacian = False
        self._lib = _load_libxc()
        self._functional_id = self._functional_number(self.name)
        self._handle = self._lib.xc_func_alloc()
        if not self._handle:
            raise RuntimeError("libxc failed to allocate xc_func_type")
        nspin = XC_UNPOLARIZED if self.polarization == "unpolarized" else XC_POLARIZED
        status = self._lib.xc_func_init(self._handle, self._functional_id, nspin)
        if status != 0:
            self._lib.xc_func_free(self._handle)
            raise ValueError(f"libxc failed to initialize functional {name!r}")

    def __del__(self) -> None:
        handle = getattr(self, "_handle", None)
        lib = getattr(self, "_lib", None)
        if handle and lib:
            try:
                lib.xc_func_end(handle)
                lib.xc_func_free(handle)
            except Exception:
                pass
            self._handle = None

    def compute(self, inp: dict[str, Any], **kwargs: Any) -> dict[str, np.ndarray]:
        rho = _as_double_array(inp["rho"])
        if self.polarization == "polarized":
            raise NotImplementedError("This lightweight pylibxc shim only supports unpolarized calculations.")
        if self.name.startswith("gga"):
            return self._compute_gga(rho, _as_double_array(inp["sigma"]), **kwargs)
        if self.name.startswith("lda"):
            return self._compute_lda(rho, **kwargs)
        raise NotImplementedError(f"Unsupported LibXC functional family for {self.name!r}")

    def _compute_lda(self, rho: np.ndarray, **kwargs: Any) -> dict[str, np.ndarray]:
        zk = np.empty_like(rho)
        vrho = np.empty_like(rho)
        self._lib.xc_lda_exc_vxc(
            self._handle,
            rho.size,
            _ptr(rho),
            _ptr(zk),
            _ptr(vrho),
        )
        out: dict[str, np.ndarray] = {}
        if kwargs.get("do_exc", False):
            out["zk"] = zk
        if kwargs.get("do_vxc", False):
            out["vrho"] = vrho
        return out

    def _compute_gga(self, rho: np.ndarray, sigma: np.ndarray, **kwargs: Any) -> dict[str, np.ndarray]:
        zk = np.empty_like(rho)
        vrho = np.empty_like(rho)
        vsigma = np.empty_like(sigma)
        self._lib.xc_gga_exc_vxc(
            self._handle,
            rho.size,
            _ptr(rho),
            _ptr(sigma),
            _ptr(zk),
            _ptr(vrho),
            _ptr(vsigma),
        )
        out: dict[str, np.ndarray] = {}
        if kwargs.get("do_exc", False):
            out["zk"] = zk
        if kwargs.get("do_vxc", False):
            out["vrho"] = vrho
            out["vsigma"] = vsigma
        return out

    def _functional_number(self, name: str) -> int:
        number = self._lib.xc_functional_get_number(name.encode("ascii"))
        if number <= 0:
            raise ValueError(f"Unknown libxc functional: {name!r}")
        return int(number)


def _load_libxc() -> ctypes.CDLL:
    for candidate in _libxc_candidates():
        try:
            lib = ctypes.CDLL(candidate)
            _configure_api(lib)
            return lib
        except OSError:
            continue
    raise ModuleNotFoundError("Could not load libxc shared library for pylibxc compatibility layer.")


def _libxc_candidates() -> list[str]:
    candidates: list[str] = []
    candidates.extend(_libxc_env_candidates("LIBXC_LIBRARY_PATH"))
    candidates.extend(_libxc_env_candidates("LD_LIBRARY_PATH"))
    candidates.extend(
        candidate
        for candidate in [
            ctypes.util.find_library("xc"),
            "libxc.so",
            "libxc.so.15",
            "/opt/homebrew/lib/libxc.dylib",
            "/usr/local/lib/libxc.dylib",
        ]
        if candidate
    )
    return list(dict.fromkeys(candidates))


def _libxc_env_candidates(env_name: str) -> list[str]:
    paths: list[str] = []
    for raw_path in os.environ.get(env_name, "").split(os.pathsep):
        if not raw_path:
            continue
        path = Path(raw_path)
        if path.is_file():
            paths.append(str(path))
        elif path.is_dir():
            paths.append(str(path / "libxc.so"))
            paths.extend(str(candidate) for candidate in sorted(path.glob("libxc.so*")))
    return paths


def _configure_api(lib: ctypes.CDLL) -> None:
    if getattr(lib, "_ofks_configured", False):
        return
    double_ptr = ctypes.POINTER(ctypes.c_double)
    lib.xc_functional_get_number.argtypes = [ctypes.c_char_p]
    lib.xc_functional_get_number.restype = ctypes.c_int
    lib.xc_func_alloc.argtypes = []
    lib.xc_func_alloc.restype = ctypes.c_void_p
    lib.xc_func_init.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
    lib.xc_func_init.restype = ctypes.c_int
    lib.xc_func_end.argtypes = [ctypes.c_void_p]
    lib.xc_func_end.restype = None
    lib.xc_func_free.argtypes = [ctypes.c_void_p]
    lib.xc_func_free.restype = None
    lib.xc_lda_exc_vxc.argtypes = [ctypes.c_void_p, ctypes.c_size_t, double_ptr, double_ptr, double_ptr]
    lib.xc_lda_exc_vxc.restype = None
    lib.xc_gga_exc_vxc.argtypes = [
        ctypes.c_void_p,
        ctypes.c_size_t,
        double_ptr,
        double_ptr,
        double_ptr,
        double_ptr,
        double_ptr,
    ]
    lib.xc_gga_exc_vxc.restype = None
    lib._ofks_configured = True


def _as_double_array(value: Any) -> np.ndarray:
    return np.ascontiguousarray(np.asarray(value, dtype=np.float64).reshape(-1))


def _ptr(array: np.ndarray) -> ctypes.POINTER(ctypes.c_double):
    return array.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
