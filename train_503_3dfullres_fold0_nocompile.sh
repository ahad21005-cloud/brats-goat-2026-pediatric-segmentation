#!/usr/bin/env bash
#SBATCH --job-name=nnUNet503_f0_fix
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=3-00:00:00
#SBATCH --output=/hdd4/sines/gpl/ahad.sines/peds_brain_project/logs/nnUNet503_f0_fix_%j.out
#SBATCH --error=/hdd4/sines/gpl/ahad.sines/peds_brain_project/logs/nnUNet503_f0_fix_%j.err

set -euo pipefail

echo "Fixed main Dataset503 fold 0 job started"
date
hostname

export PATH="/hdd4/sines/gpl/ahad.sines/.conda/envs/brats/bin:$PATH"

export PROJECT_DIR="/hdd4/sines/gpl/ahad.sines/peds_brain_project"
export nnUNet_raw="${PROJECT_DIR}/data/nnUNet_raw"
export nnUNet_preprocessed="${PROJECT_DIR}/data/nnUNet_preprocessed"
export nnUNet_results="${PROJECT_DIR}/data/nnUNet_results"

export OMP_NUM_THREADS=8
export MKL_NUM_THREADS=8
export nnUNet_n_proc_DA=4

# Critical fix proven by smoke job 7819
export nnUNet_compile=0
export TORCHDYNAMO_DISABLE=1

echo "Environment:"
which python
python --version
which nnUNetv2_train
echo "PROJECT_DIR=$PROJECT_DIR"
echo "nnUNet_raw=$nnUNet_raw"
echo "nnUNet_preprocessed=$nnUNet_preprocessed"
echo "nnUNet_results=$nnUNet_results"
echo "nnUNet_compile=$nnUNet_compile"
echo "TORCHDYNAMO_DISABLE=$TORCHDYNAMO_DISABLE"

echo "GPU:"
nvidia-smi || true

echo "Starting Dataset503 fold 0 full training..."
nnUNetv2_train 503 3d_fullres 0

echo "Dataset503 fold 0 full training finished"
date
