# TGRS_GSFF
The codes and datasets for Airborne Multispectral Point Cloud Classification


Mangrove HSI5 Three-Seed Encrypted Model Complete Data Package 2.3.0

Linux x86_64 / Python 3.9

The ZIP archive contains the Linux program package (including complete 0.Data required for ZJK_10 testing), checksum files, and this document.
assets/models.enc stores the encrypted HSI5 weights for seeds 121, 122, and 123; no plaintext model.pth is included.

1. After extracting the ZIP, enter the extracted directory in Ubuntu:

sha256sum -c mangrove_classifier_with_data_linux_py39.tar.gz.sha256
tar -xzf mangrove_classifier_with_data_linux_py39.tar.gz
cd mangrove_classifier_with_data_linux_py39



2.1 Activate the environment on the local machine:

source /home/hit/anaconda3/etc/profile.d/conda.sh
conda activate py39-torch
python -m pip install -r requirements-runtime.txt

2.2 Data sets
Data set files are too large to commit to a repository. Access to data sets can be done using this URL;
https://pan.baidu.com/s/1v5biQbnEg930rnTHbxTDcQ, w4st

Each data set has its licensing; you should include them in your paper/work.


On a new machine, first read the environment instructions in environment_zh.md.

3. Run the bundled data directly:

python check_environment.py
python main.py --dataset ZJK_10 --test --grid --seed 121


Change --seed 122 or --seed 123 to load the corresponding weights. The default seed is 123.

4. Use your own prepared data:

python main.py --dataset ZJK_10 --test --grid --seed 121 --data-root /actual/path/0.Data --data-name MyScene --check-data
python main.py --dataset ZJK_10 --test --grid --seed 121 --data-root /actual/path/0.Data --data-name MyScene


When no ground-truth labels are available, append --predict-only to the test command; this performs prediction only and does not generate a confusion matrix.

Your data must satisfy the requirements in 0.Data/Data_Description_zh.md: binary PLY, XYZ, ten specified spectral fields, a matching KDTree, a downsampled PLY, and sampling center indices.
Arbitrary RGB / XYZ / LAS data cannot be tested directly; the test process does not build indices or convert data.

Default output: output/ZJK_10_GRID/<seed>/HSI5/conf_matrix.csv.
Custom data: output/<scene_name>_GRID/<seed>/HSI5/.
Prediction-only results are saved to the predict_only subdirectory under the corresponding scene directory.

Local encryption only prevents direct access to standalone model files and does not guarantee protection against reverse engineering or memory extraction. Do not distribute alongside older unencrypted packages.

Citation
If you use this in your research, please cite the papers:

@article{li2026enhanced,
  title={An Enhanced Geometric-Spectral Feature Learning Framework for Airborne Multispectral Point Cloud Classification},
  author={Li, Xian and Gu, Yanfeng and Xu, Linghua and Pi{\v{z}}urica, Aleksandra},
  journal={IEEE Transactions on Geoscience and Remote Sensing},
  year={2026},
  publisher={IEEE}
}

@article{liu2025enhanced,
  title={An enhanced classification method based on adaptive multi-scale fusion for long-tailed multispectral point clouds},
  author={Liu, Tianzhu and Hu, Bangyan and Gu, Yanfeng and Li, Xian and Pi{\v{z}}urica, Aleksandra},
  journal={Science China Information Sciences},
  volume={68},
  number={8},
  pages={182302},
  year={2025},
  publisher={Springer}
}
