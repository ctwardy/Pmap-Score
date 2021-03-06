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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

"""
map_lognorm.py
--------------

Copied from plot_lognorm.py to try generating 2D probability maps.

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
from PIL import Image
from PIL import PngImagePlugin
from scipy.stats import lognorm
from scipy import misc

def tag_image(filename, mu, sigma, Ptot):
    '''Add model metadata to the image.
    TODO: use "with" statement?  Close image?

    '''
    im = Image.open(filename)
    meta = PngImagePlugin.PngInfo()
    meta.add_text("mean",str(mu))
    meta.add_text("stdev",str(sigma))
    meta.add_text("pden sum",str(pden_sum))
    im.save(filename, "png", pnginfo = meta)

data = []
with open('lognorm_params.csv') as f:
    for row in f:
        data.append(row.strip()[:-3].split(','))

x=y=np.linspace(-12.5,12.5,500)#represents 50 meter cells, only need to do this once
xx,yy=np.meshgrid(x,y)
dist = np.sqrt(xx**2 + yy**2)

for line in data[1:]:
    categ, mu, sigma = line
    scale, shape = np.exp(float(mu)), float(sigma)
    lnorm = lognorm([shape],scale=scale)
    qtiles = [lnorm.ppf(q) for q in [.25,.50,.75]]

    z = lnorm.pdf(dist)
    #z = np.exp(z) #retransform into regular space  # Not sure that makes sense. -crt.
    Z = np.divide(z, np.sum(z))   # Divide by sum(pdens) not by #pixels.
    # But actually what we need is to look up or calculate the *probability*
    # outside the bbox.  Two simple approximations:
    # a) Get the prob out past 12.5km from integrating the lnorm pdf. (lnorm.survival?)
    # b) Generate to say 25km, take sum(to 12.5km) / sum(all); clip
    
    pden_sum = np.sum(z)
    print"size=%d, sum_z=%f, sum_Z=%f" % (np.size(z), pden_sum, np.sum(Z))
   
    plt.title(categ)
    plt.imshow(z,cmap='gist_gray')
    plt.colorbar()
    name = 'lognormal_pngs_test2/%s.png' % categ
    plt.imsave(name, z, cmap='gist_gray')
    tag_image(name, mu, sigma, pden_sum)
