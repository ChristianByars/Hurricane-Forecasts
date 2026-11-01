"""Track and intensity skill tables for tropical-cyclone forecasts (used by the Helene notebook)."""
from __future__ import annotations

import numpy as np
import pandas as pd

from metrics import haversine_km, intensity_error


def _position_error_km(df: pd.DataFrame, ref_df: pd.DataFrame) -> np.ndarray:
    return haversine_km(
        df["center_lat"].values, df["center_lon"].values,
        ref_df["center_lat"].values, ref_df["center_lon"].values,
    )


def track_skill_table(ref_df: pd.DataFrame, model_dfs: dict) -> pd.DataFrame:
    """Per model: position error (km) and MSLP error (hPa) against the reference track.

    All DataFrames need the columns center_lat, center_lon, min_mslp_hpa and the same valid_time grid
    (rows are compared positionally). Steps where either track has no storm (NaN) are ignored.
    """
    rows = []
    for name, df in model_dfs.items():
        pos = _position_error_km(df, ref_df)
        inten = intensity_error(df["min_mslp_hpa"].values, ref_df["min_mslp_hpa"].values)
        rows.append({
            "Model": name,
            "Position error, mean (km)": round(float(np.nanmean(pos)), 1),
            "Position error, max (km)": round(float(np.nanmax(pos)), 1),
            "MSLP bias (hPa)": round(inten["bias"], 2),
            "MSLP RMSE (hPa)": round(inten["rmse"], 2),
        })
    return pd.DataFrame(rows)


def lead_error_table(ref_df: pd.DataFrame, model_dfs: dict, init_time) -> pd.DataFrame:
    """Position error (km) and MSLP error (hPa) at each forecast lead hour, one column pair per model."""
    lead_h = ((ref_df["valid_time"] - pd.Timestamp(init_time)) / pd.Timedelta(hours=1)).astype(int)
    out = pd.DataFrame({"Lead (h)": lead_h.values})
    for name, df in model_dfs.items():
        out[f"{name} position error (km)"] = np.round(_position_error_km(df, ref_df), 1)
        out[f"{name} MSLP error (hPa)"] = np.round(df["min_mslp_hpa"].values - ref_df["min_mslp_hpa"].values, 1)
    return out
