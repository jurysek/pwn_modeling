#!/usr/bin/env python
# Licensed under a 3-clause BSD style license - see LICENSE

from setuptools import setup, find_packages

setup(
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'gammapy~=1.2',
        'jupyterlab~=3.5.2',
    ],
    tests_require=[
        'pytest',
    ],
)
