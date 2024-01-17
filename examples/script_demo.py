from pyslice import *

icbm = ICBM2009NonLinSym()

batch = list(map(icbm.dict.get, ['t1', 't2', 'wm', 'gm']))
slicer(batch, axis=2)
