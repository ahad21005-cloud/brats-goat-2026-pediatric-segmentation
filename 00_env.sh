#!/usr/bin/env bash

export PROJECT_DIR="/hdd4/sines/gpl/ahad.sines/peds_brain_project"

export nnUNet_raw="${PROJECT_DIR}/data/nnUNet_raw"
export nnUNet_preprocessed="${PROJECT_DIR}/data/nnUNet_preprocessed"
export nnUNet_results="${PROJECT_DIR}/data/nnUNet_results"

export OMP_NUM_THREADS=4
export MKL_NUM_THREADS=4
export nnUNet_n_proc_DA=4

echo "PROJECT_DIR=${PROJECT_DIR}"
echo "nnUNet_raw=${nnUNet_raw}"
echo "nnUNet_preprocessed=${nnUNet_preprocessed}"
echo "nnUNet_results=${nnUNet_results}"
