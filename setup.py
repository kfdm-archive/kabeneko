#!/usr/bin/env python

from setuptools import setup

setup(
    name='Teamcity Cat',
    description='Teamcity Status Wallboard',
    author='Paul Traylor',
    url='https://github.com/kfdm/kabeneko',
    version='0.1',
    packages=['TeamcityCat'],
    install_requires=['Flask', 'argparse', 'requests'],
    entry_points={
        'console_scripts': [
            'tc-cat = TeamcityCat.web:main',
        ]
    }
)
