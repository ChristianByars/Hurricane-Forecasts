# Environment notes

Tested on 31 October – 1 November 2026 on one NVIDIA L40 (48 GB), Python 3.12, with a CUDA 13 driver.

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

- **GPU memory between models.** Models from earlier cells stay on the GPU and can cause out-of-memory errors in later sections. The notebook defines `free_gpu(...)`, which deletes the named variables, collects garbage and releases PyTorch's cached memory, and calls it in a `finally:` block after every model. This is best effort: if a forecast fails part-way, the traceback can keep the model on the GPU. After any failed or interrupted cell, restart the kernel.
- **`import cupy` needs pytest.** cupy imports `cupy.testing` internally, which requires `pytest`; it is listed in `dependencies` for that reason.
- **Headless runs.** `uv run jupyter nbconvert --to notebook --execute --allow-errors --inplace <notebook>` keeps the outputs of the cells that succeeded when a later cell fails.
- **Prebuilt torch-harmonics wheel.** torch-harmonics 0.8.1 is published on PyPI only as a source distribution and compiles CUDA extensions when it is installed, which needs torch inside the build environment, `nvcc` and a long CUDA compile. PyPI offers no prebuilt wheel of it for torch 2.13.0+cu132, so this repo expects one prebuilt cp312 wheel, `torch_harmonics-0.8.1-cp312-cp312-linux_x86_64.whl`, in a git-ignored `wheels/` folder at the repo root. `[tool.uv.sources]` points at it, and `uv sync` fails without it. Build it once against torch 2.13.0+cu132 following the upstream torch-harmonics build instructions, keep that exact file name, then run `uv lock`, because `uv.lock` pins the sha256 of the author's wheel. On the author's machine `wheels` is a symlink to a folder of prebuilt wheels. `pyproject.toml` also still lists a flash-attn source and override left over from an earlier setup; no package in `uv.lock` depends on flash-attn any more, so that wheel is not needed.
- **Git-only dependency.** `earth2studio[sfno]` needs `makani`, which is not published on PyPI. It is listed in `dependencies` and pinned in `[tool.uv.sources]` to the same GitHub commit that earth2studio 0.20.0 pins, so `uv lock` and `uv sync` need `git` and network access to github.com.
- **CUDA 13 cupy and cucim.** The CUDA 13 builds (`cupy-cuda13x`, `cucim-cu13`) match torch 2.13.0+cu132. Importing earth2studio's models prints two harmless messages: `Error Loading numa symbols, please install libnuma to avoid any performance issues`, and `CuPy distance computation test failed with error: cuVS >= 24.12 or pylibraft < 24.12 should be installed to use this feature`. The first means `libnuma` is not installed; the second means the optional cuVS accelerator is not installed.
