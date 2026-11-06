Environment Setup
System:​ Linux x86_64 (native Linux, or WSL2 Ubuntu on Windows). The core extension is a .so built for cpython-39, so CPython 3.9 is mandatory.
The verified local environment is /home/hit/anaconda3/envs/py39-torch:

```text
Python 3.9.21
PyTorch 2.5.0 / CUDA 11.8
torch-scatter 2.1.2+pt25cu118
numpy 1.24.3
scipy 1.10.1
scikit-learn 1.6.1
pandas 1.3.5
matplotlib 3.4.3
seaborn 0.11.2
tqdm 4.67.1
cryptography 44.0.3
```

## On the Preconfigured Local Machine

```bash
source /home/hit/anaconda3/etc/profile.d/conda.sh
conda activate py39-torch
python -m pip install -r requirements-runtime.txt
python check_environment.py
python main.py --dataset ZJK_10 --test --grid --seed 121
```

## On a New Machine

First install Miniconda or Anaconda inside Linux, then enter the program directory and run the following commands. On Windows machines, install WSL2 Ubuntu first — this package cannot run directly under Windows Python. NVIDIA GPU testing requires a working driver to be set up beforehand. 32 GB of RAM is recommended for the full scenario.

```bash
conda create -n py39-torch python=3.9 pip --override-channels -c conda-forge -y
conda activate py39-torch
python -m pip install -r requirements-runtime.txt
```

# With a compatible NVIDIA GPU:

```bash
python -m pip install torch==2.5.0 --index-url https://download.pytorch.org/whl/cu118
python -m pip install 'torch-scatter==2.1.2+pt25cu118' --only-binary=:all: -f https://data.pyg.org/whl/torch-2.5.0+cu118.html
```

#For CPU-only, install these instead:

```bash
python -m pip install torch==2.5.0 --index-url https://download.pytorch.org/whl/cpu
python -m pip install 'torch-scatter==2.1.2+pt25cpu' --only-binary=:all: -f https://data.pyg.org/whl/torch-2.5.0+cpu.html
```

#This complete package already includes the ZJK_10 test data, so there is no need to copy any data separately after setting up the environment:

```bash
python check_environment.py
python main.py --dataset ZJK_10 --test --grid --seed 121
```

#To switch models, simply set --seed to 121, 122, or 123.
#Version 2.3.0 adds cryptography==44.0.3 for in-memory loading of encrypted models; when upgrading an older environment, you also need to run pip install -r requirements-runtime.txt.
#For your own scenario, first prepare the data as described in 0.Data/DataDescription.md, then add --data-root and --data-name.
