#!/usr/bin/env bash
#SBATCH --job-name=nnUNet503_f2_resume
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=3-00:00:00
#SBATCH --output=/hdd4/sines/gpl/ahad.sines/peds_brain_project/logs/nnUNet503_f2_resume_%j.out
#SBATCH --error=/hdd4/sines/gpl/ahad.sines/peds_brain_project/logs/nnUNet503_f2_resume_%j.err
set -euo pipefail
echo "Fold 2 RESUME from checkpoint - started at $(date)"
hostname
export PATH="/hdd4/sines/gpl/ahad.sines/.conda/envs/brats/bin:$PATH"
export PROJECT_DIR="/hdd4/sines/gpl/ahad.sines/peds_brain_project"
export nnUNet_raw="${PROJECT_DIR}/data/nnUNet_raw"
export nnUNet_preprocessed="${PROJECT_DIR}/data/nnUNet_preprocessed"
export nnUNet_results="${PROJECT_DIR}/data/nnUNet_results"
export OMP_NUM_THREADS=2
export MKL_NUM_THREADS=2
export nnUNet_n_proc_DA=2
export nnUNet_compile=0
export TORCHDYNAMO_DISABLE=1
echo "Environment:"
which python
python --version
echo "nnUNet_n_proc_DA=$nnUNet_n_proc_DA"
echo "nnUNet_compile=$nnUNet_compile"
echo "GPU status:"
nvidia-smi || true
echo "Starting Fold 2 RESUME from checkpoint..."
nnUNetv2_train 503 3d_fullres 2 --c
echo "Fold 2 RESUME completed at $(date)"
