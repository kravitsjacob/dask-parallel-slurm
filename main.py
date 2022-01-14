from dask_jobqueue import SLURMCluster
from dask.distributed import Client, LocalCluster, progress
import dask.dataframe as dd
import numpy as np
import pandas as pd

NUMNODES = 4
NUMPROCESSES = 1


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

    # Run parallel simulation
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
