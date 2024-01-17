# PySlice3D

A lightweight Python library for 3D volume visualization.

## Quickstart

```sh
git clone https://github.com/GeorgeWilliamStrong/PySlice3D
pip install -e .
```

## Usage

PySlice3D has been designed to be lightweight and prioritises ease-of-use. Simply import `slicer` and call it whilst passing in either a 3D numpy array, or a list of 3D numpy arrays that you wish to visualize. Please also see the demo [notebook](https://github.com/GeorgeWilliamStrong/PySlice3D/blob/main/examples/notebook_demo.ipynb) and [script](https://github.com/GeorgeWilliamStrong/PySlice3D/blob/main/examples/script_demo.py).

```python
from pyslice import slicer
slicer(...)
```

![](https://imgur.com/abDT7Qk.gif)
