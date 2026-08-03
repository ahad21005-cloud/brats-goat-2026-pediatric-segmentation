#!/usr/bin/env bash
#SBATCH --job-name=predict_503_f0
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=08:00:00
#SBATCH --output=/hdd4/sines/gpl/ahad.sines/peds_brain_project/logs/predict_503_f0_%j.out
#SBATCH --error=/hdd4/sines/gpl/ahad.sines/peds_brain_project/logs/predict_503_f0_%j.err

set -euo pipefail

echo "Fold 0 inference on official validation set started"
date
hostname

# --- environment ---
source ~/.conda/etc/profile.d/conda.sh 2>/dev/null || true
conda activate brats
export PATH="/hdd4/sines/gpl/ahad.sines/.conda/envs/brats/bin:$PATH"

export PROJECT_DIR="/hdd4/sines/gpl/ahad.sines/peds_brain_project"
export nnUNet_raw="${PROJECT_DIR}/data/nnUNet_raw"
export nnUNet_preprocessed="${PROJECT_DIR}/data/nnUNet_preprocessed"
export nnUNet_results="${PROJECT_DIR}/data/nnUNet_results"
export nnUNet_compile=0
export TORCHDYNAMO_DISABLE=1

mkdir -p ${PROJECT_DIR}/outputs/predictions_fold0_official_val

echo "Running inference on official validation cases..."

nnUNetv2_predict \
  -i ${PROJECT_DIR}/data/nnUNet_raw/Dataset503_BraTSGoAT/imagesTs \
  -o ${PROJECT_DIR}/outputs/predictions_fold0_official_val \
  -d 503 \
  -c 3d_fullres \
  -f 0

echo "Prediction count:"
find ${PROJECT_DIR}/outputs/predictions_fold0_official_val -name "*.nii.gz" | wc -l

echo "Fold 0 inference finished"
date
