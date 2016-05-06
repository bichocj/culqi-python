# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from pyculqi import __version__

setup(
    name='pyculqi',
    version=__version__,
    url='https://github.com/culqi/culqi-python',
    author='culqi',
    author_email='luis.vercelli@culqi.com',
    description='Implementación del api de culqi',
    license='MIT',
    packages=find_packages(),
    zip_safe=False,
    install_requires=['pycrypto', 'requests']
)