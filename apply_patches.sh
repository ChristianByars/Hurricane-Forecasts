#!/usr/bin/env bash
set -euo pipefail

VENV=".venv/lib/python3.12/site-packages"

# 1. Patch cupy CCCL extended_data_types.h — disable fp8/fp6/fp4 under NVRTC
#    CUDA 13 fp8 headers use types from vector_types.h that NVRTC doesn't provide.
EDT="$VENV/cupy/_core/include/cupy/_cccl/libcudacxx/cuda/std/__cccl/extended_data_types.h"
if [ -f "$EDT" ]; then
  if grep -q '!defined(__CUDACC_RTC__)' "$EDT"; then
    echo "[skip] extended_data_types.h already patched"
  else
    sed -i 's/&& !defined(CCCL_DISABLE_NVFP8_SUPPORT)/\&\& !defined(CCCL_DISABLE_NVFP8_SUPPORT) \\\n    \&\& !defined(__CUDACC_RTC__)/' "$EDT"
    echo "[done] extended_data_types.h patched"
  fi
else
  echo "[warn] $EDT not found — is cupy-cuda13x installed?"
fi

# 2. Patch earth2studio graphcast_operational.py — xarray Dataset compatibility
GC="$VENV/earth2studio/models/px/graphcast_operational.py"
if [ -f "$GC" ]; then
  if grep -q 'inputs.copy() if isinstance' "$GC"; then
    echo "[skip] graphcast_operational.py already patched"
  else
    sed -i 's/inputs = xr\.Dataset(inputs)/inputs = inputs.copy() if isinstance(inputs, xr.Dataset) else xr.Dataset(inputs)/' "$GC"
    sed -i 's/targets_template = xr\.Dataset(targets_template)/targets_template = targets_template.copy() if isinstance(targets_template, xr.Dataset) else xr.Dataset(targets_template)/' "$GC"
    sed -i 's/forcings = xr\.Dataset(forcings)/forcings = forcings.copy() if isinstance(forcings, xr.Dataset) else xr.Dataset(forcings)/' "$GC"
    echo "[done] graphcast_operational.py patched"
  fi
else
  echo "[warn] $GC not found — is earth2studio installed?"
fi

# 3. Clear cupy kernel cache
rm -rf ~/.cupy/kernel_cache/*
echo "[done] cupy kernel cache cleared"

echo ""
echo "All patches applied. Notebooks are ready to run."
