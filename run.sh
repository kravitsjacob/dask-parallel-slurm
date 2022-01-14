#! /bin/bash

#SBATCH --job-name=dask-parallel
#SBATCH --output=result.out
#SBATCH --error=result.err
#SBATCH --time=0-00:05
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=amilan-ucb

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
  --worker_queue=amilan-ucb \
  --worker_cores=1 \
  --worker_memory='1 GB' \
  --worker_processes=1 \
  --worker_walltime=00:10:00 \
