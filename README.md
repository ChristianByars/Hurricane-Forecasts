# Hurricane Forecast Comparison

Comparing AI weather model tropical cyclone track forecasts against ERA5 reanalysis using [NVIDIA earth2studio](https://github.com/NVIDIA/earth2studio). One representative hurricane event is used (Helene) rather than several, per project convention of one event per forecast type.

## Models

- **AIFS2** (ECMWF Artificial Intelligence Forecasting System v2) -- global ML weather model, initialized from IFS
- **SFNO / Aurora** -- global ML weather models, initialized from ERA5
- **ERA5** -- ECMWF reanalysis used as ground truth

Evaluated at a 72h lead time. Storm center is located as the maximum smoothed 850 hPa relative vorticity, and intensity as the minimum MSLP within the domain. A companion notebook (`helene_forecast_comparison_wuduan.ipynb`) instead extracts tracks with the Wu-Duan tropical cyclone tracker.

## Storms

### Hurricane Helene (2024)

Category 4 hurricane that made landfall in the Florida Big Bend region on September 27, 2024.

![Helene 72h Track Comparison](images/helene_track_72h.png)

## Setup

Requires Python 3.12+ and a GPU with 46GB of VRAM.

```bash
uv sync
```
