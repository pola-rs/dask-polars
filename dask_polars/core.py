import numbers
import operator

import dask
import polars
from dask.utils import apply, funcname


class DataFrame(dask.base.DaskMethodsMixin):
    def __init__(self, name, graph, meta, npartitions):
        self._name = name
        self._graph = graph
        self._meta = meta
        self.npartitions = npartitions

    def __dask_graph__(self):
        return self._graph

    def __dask_keys__(self):
        return [(self._name, i) for i in range(self.npartitions)]

    @staticmethod
    def __dask_optimize__(graph, keys):
        return graph

    __dask_scheduler__ = staticmethod(dask.threaded.get)

    def __dask_postcompute__(self):
        return polars.concat, ()

    def __dask_tokenize__(self):
        return self._name

    def map_partitions(self, func, *args, **kwargs):
        name = funcname(func) + "-" + dask.base.tokenize(self, func, **kwargs)
        graph = {
            (name, i): (apply, func, [key] + list(args), kwargs)
            for i, key in enumerate(self.__dask_keys__())
        }
        meta = func(self._meta, *args, **kwargs)
        return DataFrame(name, {**self._graph, **graph}, meta, self.npartitions)

    def __add__(self, other):
        if not isinstance(other, numbers.Number):
            return NotImplemented
        return self.map_partitions(operator.add, other)

    def head(self, length=5):
        name = "head-" + dask.base.tokenize(self, length)
        graph = {
            (name, 0): (polars.DataFrame.head, self._graph[(self._name, 0)], length)
        }
        return DataFrame(name, {**self._graph, **graph}, self._meta, 1)

    def sum(self):
        tmp = self.map_partitions(polars.DataFrame.sum)
        name = "sum-" + dask.base.tokenize(tmp)
        graph = {
            (name, 0): (polars.DataFrame.sum, (polars.concat, tmp.__dask_keys__()))
        }
        return DataFrame(name, {**tmp._graph, **graph}, self._meta.sum(), 1)

    def __repr__(self):
        return self.head().compute().__repr__()


def from_dataframe(df: polars.DataFrame, npartitions=1) -> DataFrame:
    assert npartitions == 1
    name = "from-dataframe-" + dask.base.tokenize(df)
    graph = {(name, 0): df}

    return DataFrame(name, graph, df.head(0), npartitions)
