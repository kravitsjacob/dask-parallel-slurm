# dask-parallel-slurm
An minimal example of a perfectly parallelizable simulation using Python (with Dask) on a cluster computer with the Slurm workload manager. 

# What does this do?
A [perfectly parallelizable](https://en.wikipedia.org/wiki/Embarrassingly_parallel) problem is one where there is no dependency or need for communication between parallel tasks within the problem. Many computational research problems fit into this classification of problems. For example, perhaps you have some simulation (model, functions, etc.) that you need to run many times with different inputs. However, the results of each simulation do not impact one another. Such problems are perfectly parallelizable!

This repository provides a minimal working example of implementing a perfectly parallelizable task in Python. The `inputs` (parameters that change with each simulation) in this example are 10000 sets of numerical data and the outputs are some summary statistics (max, min, and mean) of each set of `inputs`. All `inputs` are initially stored in a [Pandas dataframe](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html). [Dask](https://dask.org/) is used to automate the distribution of the simulations among workers on a Slurm cluster. We have also included a `constant` input to the simulation, as often there may be some nonchanging inputs to a given simulation. The result is a Pandas dataframe of all the summary statistics corresponding to each input.

# Usage
This repository has been specifically made for usage on [RMACC Summit Supercomputer](https://www.colorado.edu/rc/resources/summit). However, it should be able easily portable to any computing evnironment using the Slurm workload manager.
1. [Login](https://curc.readthedocs.io/en/latest/access/logging-in.html) to your computing environment
2. Clone the repository using `$git clone https://github.com/kravitsjacob/dask-parallel-slurm.git`
3. Change into cloned directory `$cd dask-parallel-slurm`
4. Submit the job to Slurm using `$sbatch run.sh --partition shas`
    * If you are running on alpine use `$sbatch run.sh --partition amilan-ucb`

# Contents
```
dask-parallel-slurm
    .gitignore
    environment.yml: Conda environment specifications
    LICENSE
    main.py: Python analysis
    README.md
    run.sh: Slurm bash script
 ```
