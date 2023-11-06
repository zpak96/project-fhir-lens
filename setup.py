#!/usr/bin/env python

from setuptools import setup


setup(
    name='rito',
    version='1.0dev',
    url='https://github.com/ZanePaksi/rito',
    author='Zane Paksi',
    author_email='zane.paksi@outlook.com',
    packages=['rito'],
    include_package_data=True,
    package_dir={'rito': 'rito'},
    package_data={'rito': ['schemas/*.json']},
    long_description=open('README.md').read()
)
