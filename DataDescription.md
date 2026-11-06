# 0.DataDescription

# This document applies to both the bundled ZJK_10 dataset and your own custom scenarios. The model is always the pretrained ZJK_10 HSI5, with selectable seeds 121, 122, or 123.

# 1. Which Data Can Be Run Directly

# Only ten-band point clouds that have undergone preparation consistent with the original project can be used directly:
# Each point must have both 3D coordinates and ten specified band values.
## A sklearn KDTree corresponding point-by-point to the original point cloud must already exist.
## A sampled-centers PLY and the indices of these centers within the original point cloud must already exist.
## When label evaluation is used, every original point must have a ground-truth label, encoded as integers 0–7 matching the model.
## Point clouds containing only RGB, XYZ, LAS/LAZ, CSV, ASCII PLY, different bands, or different class encodings cannot​ be fed directly into this program.
## This package does not​ automatically convert files, substitute bands, rebuild KDTrees, or generate sampling centers. Do not​ rename file extensions or copy unrelated .pkl files as a substitute for proper data preparation.

# 2. Folder Structure
#Bundled example:

```text
0.Data/
├── DataDescription.md
├── 0.utils/meta/class_ZJK_10.txt
└── ZJK_10/
    ├── ply_ori/ZJK_10_ori.ply
    ├── ply_sub/ZJK_10_sub.ply
    └── input_ori/
        ├── ZJK_10_KDTree.pkl
        └── ZJK_10_sub_proj.pkl
```

For your own scenario, using MyScene as an example:

```text
/actual/0.Data/
└── MyScene/
    ├── ply_ori/MyScene_ori.ply
    ├── ply_sub/MyScene_sub.ply
    └── input_ori/
        ├── MyScene_KDTree.pkl
        └── MyScene_sub_proj.pkl
```

# The scene directory name and the prefix of all four filenames must match exactly. The scene name may contain only English letters, digits, underscores, or hyphens.
# Your custom directory does not​ need to provide 0.utils; the program will use the fixed model class table shipped with the delivery package.

## 3. Original PLY: <scene_name>_ori.ply
#  Must be a binary​ point cloud PLY, preferably binary_little_endian; ASCII PLY is not​ supported.
#  Minimum 4096 points, using vertex scalar properties; field names are case-sensitive.

Field	Requirement
X, Y, Z	Numeric coordinates, uppercase. Units and scale must match the training data; do not mix angular (e.g. lat/lon) and planar coordinates.
re740	1st input spectral channel
re705	2nd input spectral channel
r650	3rd input spectral channel
g531	4th input spectral channel
b444	5th input spectral channel
re717	6th input spectral channel
nir842	7th input spectral channel
r668	8th input spectral channel
g560	9th input spectral channel
b475	10th input spectral channel
label	Required for labeled evaluation; integer 0–7. May be omitted in prediction-only mode.

# Floating-point fields may use float or double; label is recommended as uchar or int. The physical field order in the file may vary; the program reads by name and feeds channels to the network in the order listed above.
# Coordinates and band values must not contain NaN/Inf; the global maximum of all spectral values must be greater than 0.
#  Spectral data must be consistent with the actual bands and radiance/reflectance processing used during training. Do not​ rename RGB or arbitrary 10-column data to impersonate these bands.
#  The program retains the original project preprocessing: all ten channels across the entire scene are divided by a single global maximum; per-channel normalization is not​ applied.
#  Local point coordinates are subtracted by the current sampling center coordinates. Having a correctly formatted new dataset does not​ guarantee accuracy across different regions or sensors comparable to the training area.

## 4. Model Class Encoding
# Defined by the line order in 0.utils/meta/class_ZJK_10.txt (bundled):

```text
0 Reject
1 Tidal flat
2 Building
3 Brug gymno
4 Aegi corn
5 Wood
6 Avic mari
7 Kand obov
```

# The program does not​ reorder or remap classes based on display names from Excel or elsewhere.
# If your own annotations use 1–8, a different class set, or a different order, you must first map them to the model protocol; a directly comparable confusion matrix cannot be computed otherwise.
# For data without ground-truth labels, use --predict-only; do not​ fill in fake labels to compute accuracy.


## 5. Sampling Centers PLY: <scene_name>_sub.ply
#Also a binary PLY, representing M pre-prepared sampling centers / downsampled points.
#It is recommended to retain the X, Y, Z, ten-band, and label fields in the original project format. The test entry reads point count and labels from this file (labels may be omitted in prediction-only mode).
#M must be greater than 0 and equal to the length of the first item in sub_proj.pkl. Center order must correspond item-by-item with the indices.
#Sampling centers should cover the area requiring prediction; this program does not​ supplement sampling additionally. Points not visited by any neighborhood query receive label 0 per the original test rules.

## 6. Spatial Index: <scene_name>_KDTree.pkl
#Must contain a sklearn.neighbors.KDTree object — not​ a scipy KDTree/cKDTree, dictionary, coordinate array, or file path string.
#Saving with scikit-learn 1.6.1 (the delivered environment version) is recommended.
#The KDTree should use default Euclidean distance and be built from the complete X, Y, Z of the original PLY in original point order: N×3.
#The KDTree point count, coordinate values, and point order must match ori.ply exactly. Do not​ use a KDTree from another scene, nor shuffle or modify the PLY after tree construction.
#If coordinate precision changed due to re-saving after tree construction, you must re-align both in the preparation stage.
#The test only reads the existing index and validates its coordinates and order in chunks; it does not​ rebuild the index.

## 7. Center Indices: <scene_name>_sub_proj.pkl
# The pickle payload must be a non-empty list or tuple. The first item proj[0] is a 1D integer array of length M.
#  Each value is the row index (zero-based, range 0 to N-1) of a sampling center in the original point cloud.
#  It is not​ an N-length full-point-cloud nearest-neighbor back-projection table. This program follows the original dataset_grid interpretation of proj[0].
#  If a multi-item list/tuple exported from the original project is used, items beyond the first are not​ used during testing.
#  Only load .pkl files generated by yourself or from trusted sources.

## 8. Running and Output

```bash
# First validate your data (reads full PLY and indices)
python main.py --dataset ZJK_10 --test --grid --seed 121 --data-root /actual/path/0.Data --data-name MyScene --check-data

# With labels: predict and generate raw confusion matrix
python main.py --dataset ZJK_10 --test --grid --seed 121 --data-root /actual/path/0.Data --data-name MyScene

# Without labels: prediction only
python main.py --dataset ZJK_10 --test --grid --seed 121 --data-root /actual/path/0.Data --data-name MyScene --predict-only
```

#For labeled evaluation, conf_matrix.csv is a raw 8×8 count matrix with rows = predicted, columns = ground truth, ordered 0–7, with no header or row index.
#Prediction-only mode saves only predictions and run logs; it does not​ generate fake confusion matrices, OA, or mIoU.
#Pred.ply contains only the pred label field; its point row order is consistent with ori.ply and can be merged with original coordinates.
#32 GB RAM is recommended for full-scene processing. When a GPU is available, CUDA is used automatically; you may also specify --device cpu explicitly.