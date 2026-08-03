#!/bin/bash
#SBATCH --job-name=brats_download
#SBATCH --partition=gpu
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=3-00:00:00
#SBATCH --output=/hdd4/sines/gpl/ahad.sines/peds_brain_project/logs/%x_%j.out
#SBATCH --error=/hdd4/sines/gpl/ahad.sines/peds_brain_project/logs/%x_%j.err

set -euo pipefail

cd /hdd4/sines/gpl/ahad.sines/peds_brain_project

source scripts/00_env.sh

echo "Started Synapse download at: $(date)"
echo "Running on node: $(hostname)"
echo "Using Python: /hdd4/sines/gpl/ahad.sines/.conda/envs/brats/bin/python"

/hdd4/sines/gpl/ahad.sines/.conda/envs/brats/bin/python scripts/01_download_synapse.py

echo "Finished Synapse download at: $(date)"
