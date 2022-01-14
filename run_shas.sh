#! /bin/bash

#SBATCH --job-name=dask-parallel
#SBATCH --output=result.out
#SBATCH --error=result.err
#SBATCH --time=00:05:00
#SBATCH --nodes=1
#SBATCH --partition=shas

module purge

# Load conda commands
source /curc/sw/anaconda3/latest

# Create conda environment
conda env create -f environment.yml

# Activate conda environment
conda activate dask-parallel

# Run
python main.py \
  --npartitions=2 \
  --n_workers=2 \
  --worker_cores=1 \
  --worker_memory='0.5 GB' \
  --worker_processes=1 \
