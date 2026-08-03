#!/bin/bash
#SBATCH --job-name=nnUNet503_f0
#SBATCH --output=/hdd4/sines/gpl/ahad.sines/peds_brain_project/logs/nnunet503_f0_%j.out
#SBATCH --error=/hdd4/sines/gpl/ahad.sines/peds_brain_project/logs/nnunet503_f0_%j.err
#SBATCH --partition=gpu
#SBATCH --gres=gpu:v100:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=72:00:00

set -e

echo "Job started"
hostname
date

cd /hdd4/sines/gpl/ahad.sines/peds_brain_project

source ~/.bashrc
conda activate brats
source scripts/00_env.sh

echo "Environment:"
which python
python --version

echo "nnU-Net paths:"
echo "nnUNet_raw=$nnUNet_raw"
echo "nnUNet_preprocessed=$nnUNet_preprocessed"
echo "nnUNet_results=$nnUNet_results"

echo "CUDA check:"
python - <<'PY'
import torch
print("CUDA available:", torch.cuda.is_available())
print("GPU count:", torch.cuda.device_count())
if torch.cuda.is_available():
    print("GPU name:", torch.cuda.get_device_name(0))
    print("CUDA version:", torch.version.cuda)
PY

echo "Starting nnU-Net 3d_fullres fold 0 training..."
nnUNetv2_train 503 3d_fullres 0

echo "Training completed"
date
