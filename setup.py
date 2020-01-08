#!/usr/bin/env python

from setuptools import setup
import pkg_resources


# DATA_PATH = pkg_resources.resource_filename('fhir.r4.schema.json', Path('schemas/'))

setup(
    name='fhirlens',
    version='2.3dev',
    url='https://github.com/zpak96/project-fhir-lens',
    author='Zane Paksi',
    author_email='zane.paksi@outlook.com',
    packages=['fhirlens'],
    include_package_data=True,
    package_dir={'fhirlens': 'fhirlens'},
    package_data={'fhirlens': ['schemas/*.json']},
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read()
)
