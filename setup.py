#!/usr/bin/env python

from os.path import exists
from setuptools import setup
import dask_polars

setup(name='dask_polars',
      version=dask_polars.__version__,
      license='BSD',
      packages=['dask_polars'],
      long_description=(open('README.rst').read() if exists('README.rst')
                        else ''),
      zip_safe=False,
      python_requires=">=3.7",
      )
