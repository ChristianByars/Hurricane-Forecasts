# Hurricane Forecast Comparison

Comparing AI weather model tropical cyclone track forecasts against ERA5 reanalysis for three major hurricanes using [NVIDIA earth2studio](https://github.com/NVIDIA/earth2studio).

## Models

- **AIFS** (ECMWF Artificial Intelligence Forecasting System) -- global ML weather model
- **GraphCast** (Google DeepMind) -- graph neural network weather model
- **ERA5** -- ECMWF reanalysis used as ground truth

Each storm is evaluated at three lead times: 72h, 168h, and 240h. Tracks are extracted using the Wu-Duan tropical cyclone tracker.
