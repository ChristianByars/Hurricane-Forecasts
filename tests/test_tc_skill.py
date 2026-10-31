import numpy as np
import pandas as pd
import pytest

import tc_skill


def _track(lat0, mslp0, n=3):
    return pd.DataFrame({
        "valid_time": pd.date_range("2024-09-24", periods=n, freq="6h"),
        "center_lat": [lat0] * n,
        "center_lon": [-85.0] * n,
        "min_mslp_hpa": [mslp0 - 2.0 * i for i in range(n)],
    })


def test_track_skill_table_perfect_and_offset_models():
    ref = _track(25.0, 1000.0)
    table = tc_skill.track_skill_table(ref, {"A": ref.copy(), "B": _track(26.0, 1004.0)}).set_index("Model")
    assert table.loc["A", "Position error, mean (km)"] == 0.0
    assert table.loc["A", "MSLP RMSE (hPa)"] == 0.0
    assert table.loc["B", "Position error, mean (km)"] == pytest.approx(111.2, abs=0.2)
    assert table.loc["B", "MSLP bias (hPa)"] == 4.0


def test_missing_steps_are_ignored():
    ref = _track(25.0, 1000.0)
    model = _track(26.0, 1000.0)
    model.loc[1, ["center_lat", "center_lon", "min_mslp_hpa"]] = np.nan
    row = tc_skill.track_skill_table(ref, {"A": model}).iloc[0]
    assert row["Position error, mean (km)"] == pytest.approx(111.2, abs=0.2)


def test_lead_error_table_uses_hours_since_init():
    ref = _track(25.0, 1000.0)
    table = tc_skill.lead_error_table(ref, {"A": _track(26.0, 1000.0)}, "2024-09-24")
    assert table["Lead (h)"].tolist() == [0, 6, 12]
    assert table["A position error (km)"].iloc[0] == pytest.approx(111.2, abs=0.2)
    assert table["A MSLP error (hPa)"].tolist() == [0.0, 0.0, 0.0]
