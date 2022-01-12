# dask-parallel-slurm
An example repository for a perfectly parallelizable job using Dask on a cluster computer with the Slurm workload manager. 

# How does it work
All inputs (parameters that change with each parallelized execution) are stored in a Pandas dataframe and Dask is used to automate the distribution of the tasks. The inputs in this example are numerical data and the outputs are some summary statistics (max, min, mean, median, and standard deviation).
