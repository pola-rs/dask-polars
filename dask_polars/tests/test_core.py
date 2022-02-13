import polars as pl

import dask_polars as dp

df = pl.DataFrame({"a": [1, 2, 3, 4], "b": [1.0, 2.0, 3.0, 4.0]})
ddf = dp.from_dataframe(df)


def test_basic():
    assert str(ddf.compute()) == str(df)


def test_meta():
    assert list(ddf._meta.schema.keys()) == df.columns
    assert list(ddf._meta.schema.values()) == df.dtypes


def test_sum():
    assert str(ddf.sum().compute()) == str(df.sum())


def test_add():
    assert str((ddf + 2).compute()) == str(df + 2)
