from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='pyslice-3d',
    version='1.0',
    description='A lightweight Python library for 3D volume visualization.',
    long_description='A lightweight Python library for 3D volume visualization.',
    author='George Strong',
    author_email='geowstrong@gmail.com',
    license='AGPL-3.0',
    python_requires=">=3.9",
    packages=find_packages(),
    install_requires=required)
