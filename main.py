import dask
from dask_jobqueue import SLURMCluster
from dask.distributed import Client, LocalCluster, progress
import dask.dataframe as dd
import random
import numpy as np
import pandas as pd

NUMNODES = 4
NUMPROCESSES = 1

def slowsum(ser):
    results = pd.Series(
        {
            'Max': ser.max(),
            'Min': ser.min(),
            'Mean': ser.mean()
        }
    )
    return results


if __name__ == '__main__':
    cluster = SLURMCluster(cores=2, memory='1 GB', processes=NUMPROCESSES, walltime='00:10:00', queue='amilan-ucb')
    cluster.scale(NUMNODES*NUMPROCESSES)
    client = Client(cluster)
    print("start script...")
    x = np.random.normal(0, 1, (500, 5))
    df = pd.DataFrame(columns=['a', 'b', 'c', 'd', 'e'], data=x)
    ddf = dd.from_pandas(df, npartitions=10)
    run = ddf.apply(
        slowsum,
        axis=1,
        meta=pd.DataFrame(columns=['Max', 'Min', 'Mean'], dtype='float64')
    ).persist()
    progress(run)
    res = run.compute(scheduler=client)
    print(res)
    print("finished!")