from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np


BASE_FEATURES = ["bias", "total_energy_ev", "height_angstrom", "max_force_ev_per_ang"]
NUMERIC_FEATURES = {"total_energy_ev", "adsorption_energy_ev", "height_angstrom", "max_force_ev_per_ang"}
CATEGORICAL_FIELDS = ["system_name", "adsorbate", "site", "orientation"]


@dataclass(frozen=True)
class DeltaModel:
    feature_names: list[str]
    coefficients: np.ndarray
    ridge_alpha: float
    target_name: str = "delta_energy_ev"
    candidate_energy_key: str = "total_energy_ev"
    corrected_energy_key: str = "corrected_total_energy_ev"
    delta_key: str = "delta_energy_pred_ev"

    def predict(self, records: list[dict[str, Any]]) -> np.ndarray:
        x = featurize_records(records, self.feature_names)
        return x @ self.coefficients

    def to_dict(self) -> dict[str, Any]:
        return {
            "model_type": "ridge_linear_delta_energy",
            "target_name": self.target_name,
            "candidate_energy_key": self.candidate_energy_key,
            "corrected_energy_key": self.corrected_energy_key,
            "delta_key": self.delta_key,
            "ridge_alpha": self.ridge_alpha,
            "feature_names": self.feature_names,
            "coefficients": self.coefficients.tolist(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DeltaModel":
        return cls(
            feature_names=list(data["feature_names"]),
            coefficients=np.asarray(data["coefficients"], dtype=float),
            ridge_alpha=float(data["ridge_alpha"]),
            target_name=str(data.get("target_name", "delta_energy_ev")),
            candidate_energy_key=str(data.get("candidate_energy_key", "total_energy_ev")),
            corrected_energy_key=str(data.get("corrected_energy_key", "corrected_total_energy_ev")),
            delta_key=str(data.get("delta_key", "delta_energy_pred_ev")),
        )

    def save(self, path: str | Path) -> None:
        output = Path(path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(self.to_dict(), indent=2, sort_keys=True), encoding="utf-8")


def load_delta_model(path: str | Path) -> DeltaModel:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return DeltaModel.from_dict(data)


def build_training_data(
    records: list[dict[str, Any]],
    truth_energy_key: str = "ks_total_energy_ev",
    candidate_energy_key: str = "total_energy_ev",
) -> tuple[list[dict[str, Any]], np.ndarray]:
    usable = [
        record
        for record in records
        if record.get("ks_status") == "parsed_converged"
        and record.get("converged") is not False
        and record.get("candidate_converged") is not False
        and record.get(truth_energy_key) is not None
        and record.get(candidate_energy_key) is not None
    ]
    y = np.asarray(
        [float(record[truth_energy_key]) - float(record[candidate_energy_key]) for record in usable],
        dtype=float,
    )
    return usable, y


def train_delta_model(
    records: list[dict[str, Any]],
    ridge_alpha: float = 1.0,
    truth_energy_key: str = "ks_total_energy_ev",
    candidate_energy_key: str = "total_energy_ev",
    corrected_energy_key: str = "corrected_total_energy_ev",
    delta_key: str = "delta_energy_pred_ev",
) -> tuple[DeltaModel, dict[str, Any]]:
    usable, y = build_training_data(records, truth_energy_key=truth_energy_key, candidate_energy_key=candidate_energy_key)
    if not usable:
        raise ValueError("No parsed_converged records with both KS and fast energies were found")
    feature_names = infer_feature_names(usable, candidate_energy_key=candidate_energy_key)
    x = featurize_records(usable, feature_names)
    coefficients = _ridge_solve(x, y, ridge_alpha=ridge_alpha)
    model = DeltaModel(
        feature_names=feature_names,
        coefficients=coefficients,
        ridge_alpha=ridge_alpha,
        target_name=f"delta_{candidate_energy_key}",
        candidate_energy_key=candidate_energy_key,
        corrected_energy_key=corrected_energy_key,
        delta_key=delta_key,
    )
    pred = x @ coefficients
    residual = pred - y
    metrics = {
        "n_records_total": len(records),
        "n_records_trainable": len(usable),
        "n_features": len(feature_names),
        "ridge_alpha": ridge_alpha,
        "target_mean_ev": float(np.mean(y)),
        "truth_energy_key": truth_energy_key,
        "candidate_energy_key": candidate_energy_key,
        "corrected_energy_key": corrected_energy_key,
        "train_mae_ev": float(np.mean(np.abs(residual))),
        "train_rmse_ev": float(np.sqrt(np.mean(residual**2))),
        "warning": None,
    }
    if len(usable) < 5:
        metrics["warning"] = "Very small training set; model is only a pipeline sanity check."
    return model, metrics


def infer_feature_names(records: list[dict[str, Any]], candidate_energy_key: str = "total_energy_ev") -> list[str]:
    feature_names = list(BASE_FEATURES)
    if candidate_energy_key != "total_energy_ev":
        feature_names = ["bias", candidate_energy_key, "height_angstrom", "max_force_ev_per_ang"]
    for field in CATEGORICAL_FIELDS:
        values = sorted({str(record.get(field, "unknown")) for record in records})
        feature_names.extend(f"{field}={value}" for value in values)
    return feature_names


def featurize_records(records: list[dict[str, Any]], feature_names: list[str]) -> np.ndarray:
    rows = []
    for record in records:
        row = []
        for name in feature_names:
            if name == "bias":
                row.append(1.0)
            elif name in NUMERIC_FEATURES:
                row.append(_float_or_zero(record.get(name)))
            elif "=" in name:
                field, value = name.split("=", 1)
                row.append(1.0 if str(record.get(field, "unknown")) == value else 0.0)
            else:
                raise ValueError(f"Unknown feature name: {name}")
        rows.append(row)
    return np.asarray(rows, dtype=float)


def _ridge_solve(x: np.ndarray, y: np.ndarray, ridge_alpha: float) -> np.ndarray:
    regularizer = ridge_alpha * np.eye(x.shape[1], dtype=float)
    # Do not regularize the intercept.
    regularizer[0, 0] = 0.0
    return np.linalg.pinv(x.T @ x + regularizer) @ x.T @ y


def _float_or_zero(value: Any) -> float:
    if value is None:
        return 0.0
    return float(value)
