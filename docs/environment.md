# Environment notes

Tested in October 2026 on one NVIDIA L40 (48 GB), Python 3.12, with a CUDA 13 driver.

## Pinned stack

- earth2studio **0.20.0** (the version published on PyPI; uv resolves it through the PyPI and NVIDIA package indexes)
- torch **2.13.0** (CUDA 13.2 wheels from the `pytorch-cu132` index)
- All other versions are resolved in `uv.lock`; use `uv sync` (not `pip install`) so you get exactly the tested set.

## Install

```bash
uv sync
uv run python -m ipykernel install --user --name hurricane-forecasts --display-name "hurricane-forecasts"
```

## Known issues and fixes

- **GPU memory between models.** Models from earlier cells stay on the GPU and can cause out-of-memory errors in later sections. Each notebook defines `free_gpu(...)` and calls it in a `finally:` block after every model, so it is released even when a cell fails. If a cell is interrupted by hand, restart the kernel.
- **`import cupy` needs pytest.** cupy imports `cupy.testing` internally, which requires `pytest`; it is listed in `dependencies` for that reason.
- **Headless runs.** `uv run jupyter nbconvert --to notebook --execute --allow-errors --inplace <notebook>` keeps the outputs of the cells that succeeded when a later cell fails.
- **Prebuilt torch-harmonics wheel.** torch-harmonics 0.8.1 is published on PyPI only as a source distribution and compiles CUDA extensions when it is installed, which needs torch inside the build environment, `nvcc` and a long CUDA compile. PyPI offers no prebuilt wheel of it for torch 2.13.0+cu132, so this repo expects one prebuilt cp312 wheel, `torch_harmonics-0.8.1-cp312-cp312-linux_x86_64.whl`, in a git-ignored `wheels/` folder at the repo root. `[tool.uv.sources]` points at it, and `uv sync` fails without it. Build it once against torch 2.13.0+cu132 following the upstream torch-harmonics build instructions, keep that exact file name, then run `uv lock`, because `uv.lock` pins the sha256 of the author's wheel. On the author's machine `wheels` is a symlink to a folder of prebuilt wheels. `pyproject.toml` also still lists a flash-attn source and override left over from an earlier setup; `uv.lock` no longer contains flash-attn, so that wheel is not needed.
- **Git-only dependencies.** `earth2studio[sfno]` needs `makani` and `earth2studio[graphcast]` needs `weathernext`, and neither is published on PyPI. Both are listed in `dependencies` and pinned in `[tool.uv.sources]` to the same GitHub commits that earth2studio 0.20.0 pins, so `uv lock` and `uv sync` need `git` and network access to github.com.
- **GraphCast runs on JAX.** GraphCast is the one model here that is not a torch model, and it shares the GPU with the torch models in one notebook kernel. The notebook sets `XLA_PYTHON_CLIENT_PREALLOCATE=false` and `XLA_PYTHON_CLIENT_ALLOCATOR=platform` before importing anything so JAX allocates on demand and can hand memory back to the driver once GraphCast is freed; without them JAX keeps the memory it grew to until the kernel restarts, and Aurora or SFNO may then run out of GPU memory. `weathernext`, which the `graphcast` extra installs, requires `xarray<=2026.2.0`, so `uv.lock` holds xarray 2026.2.0.
- **CUDA 13 cupy and cucim.** The CUDA 13 builds (`cupy-cuda13x`, `cucim-cu13`) match torch 2.13.0+cu132. Importing earth2studio's models prints one harmless warning, `CuPy distance computation test failed with error: cuVS >= 24.12 or pylibraft < 24.12 should be installed to use this feature`; it only means the optional cuVS accelerator is not installed.
