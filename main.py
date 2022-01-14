import argparse
from dask_jobqueue import SLURMCluster
from dask.distributed import Client, progress
import dask
import dask.dataframe as dd
import numpy as np
import pandas as pd


def input_parse():
    # Create argument parser
    argparse_inputs = argparse.ArgumentParser()

    # Command line arguments
    argparse_inputs.add_argument(
        '--npartitions',
        type=int,
        action='store',
        help='The number of partitions of the index to create.',
        required=False
    )
    argparse_inputs.add_argument(
        '--n_workers',
        type=int,
        action='store',
        help='Target number of workers.',
        required=False
    )
    argparse_inputs.add_argument(
        '--worker_queue',
        type=int,
        action='store',
        help='Destination queue for each worker job.',
        required=False
    )
    argparse_inputs.add_argument(
        '--worker_project',
        type=int,
        action='store',
        help='Accounting string associated with each worker job.',
        required=False
    )
    argparse_inputs.add_argument(
        '--worker_cores',
        type=int,
        action='store',
        help='Total number of cores per job.',
        required=False
    )
    argparse_inputs.add_argument(
        '--worker_memory',
        type=int,
        action='store',
        help='Total amount of memory per job.',
        required=False
    )
    argparse_inputs.add_argument(
        '--worker_processes',
        type=int,
        action='store',
        help='Cut the job up into this many processes.',
        required=False
    )
    argparse_inputs.add_argument(
        '--worker_walltime',
        type=int,
        action='store',
        help='Walltime for each worker job.',
        required=False
    )
    # Parse arguments
    argparse_inputs = argparse_inputs.parse_args()

    return argparse_inputs


def simulation(inputs, constant):
    """General 'simulation' to be parallelized which has `inputs` that
    change on every evaluation and a `constant` object that does
    not chaange on every evalation.

    Parameters
    ----------
    inputs : pandas.core.series.Series
        Series of inputs
    constant : int
        Constant used for demonstration

    Returns
    -------
    results : pandas.core.series.Series
        Series of outputs. Each index will become a column after apply.
    """
    results = pd.Series(
        {
            'Max': inputs.max(),
            'Min': inputs.min(),
            'Mean': inputs.mean(),
            'constant': constant
        }
    )
    return results


def main():
    # Parse arguments
    clargs = input_parse()

    # Generate random inputs
    df = pd.DataFrame(
        columns=['Input 1', 'Input 2', 'Input 3', 'Input 4', 'Input 5'],
        data=np.random.normal(0, 1, (100, 5))
    )
    print('success: Generating random inputs')

    # Run serially on first 5 to test
    res_test = df.iloc[0:5].apply(
        lambda row: simulation(inputs=row, constant=1008),
        axis=1
    )
    print('Results of serial test')
    print(res_test)

    # Run parallel simulations
    cluster = SLURMCluster(cores=2, memory='1 GB', processes=NUMPROCESSES, walltime='00:10:00', queue='amilan-ucb')
    cluster.scale(n=1)
    client = Client(cluster)
    ddf = dd.from_pandas(df, npartitions=10)
    run = ddf.apply(
        simulation,
        axis=1,
        meta=pd.DataFrame(columns=['Max', 'Min', 'Mean'], dtype='float64')
    ).persist()
    progress(run)
    res = run.compute(scheduler=client)
    print(res)


if __name__ == '__main__':
    main()
