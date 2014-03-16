#! /usr/bin/env python
# -*- Mode: Python; py-indent-offset: 4 -*-
# 
# Copyright (C) 2014 Charles Twardy
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

"""
plot_lognorm.py
--------------
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import lognorm
from itertools import cycle

#data = pd.read_csv("lognorm_params.csv")
# Columns are: category, meanlog, stdlog
data = []
with open('lognorm_params.csv') as f:
    for row in f:
        data.append(row.strip()[:-3].split(','))

def get_axis(s, axarr):
    '''Return subplot and title based on category string s'''

    if s.startswith('hiker'):
        return axarr[0,0], 'Hiker'
    elif s.startswith('dementia'):
        return axarr[0,1], 'Dementia'
    elif s.startswith('child 1-3'):
        return axarr[1,0], 'Child 1-3'
    elif s.startswith('child 4-6'):
        return axarr[1,1], 'Child 4-6'
    elif s.startswith('child 7-9'):
        return axarr[2,0], 'Child 7-9'
    elif s.startswith('child 10-12'):
        return axarr[2,1], 'Child 10-12'
    elif s.startswith('child 13-15'):
        return axarr[2,2], 'Child 13-15'
    else:
        return axarr[2,2]
    
X = np.linspace(0,5,200)  # km
linestyles = ['-','--','-.',':']
cyclers = {}
fig, axarray = plt.subplots(3, 3, sharex='col', sharey='row')
fig.set_size_inches(8,6)
fig.suptitle("Lognormal Probability Density by Category (km)", fontsize=14)
for line in data[1:]:
    categ, mu, sigma = line
    if 'else' in categ:
        continue
    scale, shape = np.exp(float(mu)), float(sigma)
    Y = lognorm.pdf(X, [shape], scale=scale)
    axis,title = get_axis(categ, axarray)
    try:
        linecycler = cyclers[axis]
    except KeyError:
        cyclers[axis] = cycle(linestyles)
        linecycler = cyclers[axis]
    axis.plot(X,Y,next(linecycler),label=categ[len(title):])
    axis.set_title(title)
    axis.legend()
    
# Fine-tune figure; hide x ticks for top plots and y ticks for right plots
plt.setp([a.get_xticklabels() for a in axarr[0, :]], visible=False)
plt.setp([a.get_yticklabels() for a in axarr[:, 1]], visible=False)
[ax.set_xlabel('DistIPP (km)') for ax in axarray[2,:]]
[ax.set_ylabel('Probability Density') for ax in axarray[:,0]]
plt.setp(axarray[0,2], visible=False)
plt.setp(axarray[2,2], visible=False)


plt.ylim((0,1.2))
plt.legend()
#plt.tight_layout()
#plt.savefig('lognormals.pdf')
plt.show()
