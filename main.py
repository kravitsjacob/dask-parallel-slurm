# from dask_jobqueue import SLURMCluster
# from dask.distributed import Client, LocalCluster, progress
# import dask.dataframe as dd
import numpy as np
import pandas as pd

NUMNODES = 4
NUMPROCESSES = 1


def job(inputs, constant):
    """General 'job' to be parallelized which has `inputs` that
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


if __name__ == '__main__':
    # cluster = SLURMCluster(cores=2, memory='1 GB', processes=NUMPROCESSES, walltime='00:10:00', queue='amilan-ucb')
    # cluster.scale(NUMNODES*NUMPROCESSES)
    # client = Client(cluster)
    print("start script...")
    x = np.random.normal(0, 1, (100, 5))
    df = pd.DataFrame(
        columns=['Input 1', 'Input 2', 'Input 3', 'Input 4', 'Input 5'],
        data=x
    )
    a = df.apply(
        lambda row: job(inputs=row, constant=1008),
        axis=1
    )
    print(a)


    # ddf = dd.from_pandas(df, npartitions=10)
    # run = ddf.apply(
    #     job,
    #     axis=1,
    #     meta=pd.DataFrame(columns=['Max', 'Min', 'Mean'], dtype='float64')
    # ).persist()
    # progress(run)
    # res = run.compute(scheduler=client)
    # print(res)
    # print("finished!")
