# brats-goat-2026-pediatric-segmentation
Engineering-optimized nnU-Net v2 baseline for BraTS-GoAT 2026 Task 3 (Pediatric Brain Tumor Segmentation)
# BraTS-GoAT 2026 (Task 3): Pediatric Brain Tumor Segmentation

This repository contains the methodology, SLURM HPC scripts, and codebase for our submission to the **BraTS-GoAT 2026 Challenge (Task 3: Generalizability)**.

**Authors:** Ahad Ali Nazir, Absaar ul Jabbar  
**Institution:** School of Interdisciplinary Engineering and Sciences (SINES), National University of Sciences and Technology (NUST), Islamabad, Pakistan

## Project Overview
This project establishes an engineering-optimized **nnU-Net v2 (3D full-resolution)** baseline for segmenting pediatric brain tumors into three sub-regions:
1. Necrotic Core (NCR)
2. Peritumoral Edema (ED)
3. Enhancing Tumor (ET)

The model was trained on the **Dataset 503 (BraTS Pediatric Tumors)** cohort using a rigorous 5-fold cross-validation strategy.

##  Infrastructure & Engineering Optimizations
Training was conducted on the NUST SINES High-Performance Computing (HPC) cluster using NVIDIA A10G (24GB VRAM) GPUs. To guarantee stable, multi-day 1000-epoch training runs under strict 72-hour SLURM wall-time limits, we implemented the following critical cluster optimizations:

* **Worker Down-regulation:** Reduced parallel data-augmentation workers (`nnUNet_n_proc_DA=2`) to resolve `ArrayMemoryError` multi-threading crashes during 3D spatial augmentation.
* **Compilation Bypass:** Disabled PyTorch dynamic compilation (`TORCHDYNAMO_DISABLE=1` and `nnUNet_compile=0`) to prevent graph-compilation instability over multi-day workloads.

##  Repository Contents
* `/slurm_scripts/`: Custom bash scripts used for cluster deployment, including the bulletproof environment path activation and automatic resume logic.
* `/src/`: (Coming Soon) Inference pipeline and ensembling logic.
* **Docker Submission:** The finalized 5-fold ensemble model will be containerized and pushed to the official Synapse registry for the July 23, 2026 hidden test-set evaluation.

## Preliminary Validation Results
Our current baseline demonstrates strong performance, particularly in delineating enhancing tumor and edema regions. 

| Fold | Overall Mean Dice | NCR Dice | ED Dice | ET Dice |
| :--- | :---------------: | :------: | :-----: | :-----: |
| Fold 0 | 0.827 | 0.770 | 0.850 | 0.862 |
| Fold 1 | 0.830 | 0.780 | 0.850 | 0.861 |
| Fold 2 | 0.831 | 0.780 | 0.849 | 0.864 |
| Fold 3 | 0.824 | 0.758 | 0.853 | 0.862 |
| Fold 4 (Best) | **0.845** | **0.795** | **0.860** | **0.878** |
| **Mean (5-fold)** | **0.831** | **0.776** | **0.853** | **0.866** |
