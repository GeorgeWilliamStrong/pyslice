# PySlice

![Build Status](https://github.com/GeorgeWilliamStrong/pyslice/actions/workflows/examples.yml/badge.svg)

A lightweight Python library for 3D volume visualization.

## Quickstart

```sh
git clone https://github.com/GeorgeWilliamStrong/pyslice
cd pyslice
pip install -e .
```

## Usage

PySlice has been designed to be lightweight and prioritise ease-of-use. Simply import `slicer` and call it whilst passing in either a 3D numpy array, or a list of 3D numpy arrays that you wish to visualize. Please also see the demo notebook and script [here](https://github.com/GeorgeWilliamStrong/pyslice/tree/main/examples) for further details!

```python
from pyslice import slicer
slicer(...)
```

![](https://imgur.com/abDT7Qk.gif)
