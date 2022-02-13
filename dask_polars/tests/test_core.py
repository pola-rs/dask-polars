import polars

import dask_polars as dp

df = polars.from_dict({"a": [1, 2, 3, 4], "b": [1.0, 2.0, 3.0, 4.0]})
ddf = dp.from_dataframe(df)


def test_basic():
    assert str(ddf.compute()) == str(df)


def test_sum():
    assert str(ddf.sum().compute()) == str(df.sum())


def test_add():
    assert str((ddf + 2).compute()) == str(df + 2)
