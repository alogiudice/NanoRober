#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 16:26:35 2019

@author: agostina
"""

import matplotlib.pyplot as plt
import matplotlib.collections as mcol
from matplotlib.legend_handler import HandlerLineCollection, HandlerTuple
from matplotlib.lines import Line2D
import numpy as np

t1 = np.arange(0.0, 2.0, 0.1)
t2 = np.arange(0.0, 2.0, 0.01)

fig, ax = plt.subplots()

# note that plot returns a list of lines.  The "l1, = plot" usage
# extracts the first element of the list into l1 using tuple
# unpacking.  So l1 is a Line2D instance, not a sequence of lines
l1 = ax.plot(t2, np.exp(-t2))
l1[0]
#l2, l3 = ax.plot(t2, np.sin(2 * np.pi * t2), '--o', t1, np.log(1 + t1), '.')
#l4, = ax.plot(t2, np.exp(-t2) * np.sin(2 * np.pi * t2), 's-.')
#
#ax.legend((l2, l4), ('oscillatory', 'damped'), loc='upper right', shadow=True)
#ax.set_xlabel('time')
#ax.set_ylabel('volts')
#ax.set_title('Damped oscillation')
#plt.show()