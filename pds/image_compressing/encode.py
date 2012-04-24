#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
#
# This file is part of Coruja-scripts
#
# Coruja-scripts is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# Coruja-scripts is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Coruja-scripts.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2011 Grupo Falabrasil - http://www.laps.ufpa.br/falabrasil
#
# Author 2011: Pedro Batista - pedosb@gmail.com

import sys
import numpy as np
from scipy.ndimage import imread as imread
from matplotlib import pyplot as plt

BLOCK_LEN = 8

def encode(file_name):
	image = imread(file_name)

	dct_coeff = np.zeros(image.shape)

	for i_shift in xrange(image.shape[0] / BLOCK_LEN):
		print i_shift
		for j_shift in xrange(image.shape[1] / BLOCK_LEN):
			i = i_shift * BLOCK_LEN
			j = j_shift * BLOCK_LEN
			block = image[i:i+BLOCK_LEN, j:j+BLOCK_LEN]
			for k1 in xrange(BLOCK_LEN):
				for k2 in xrange(BLOCK_LEN):
					for n1 in xrange(BLOCK_LEN):
						for n2 in xrange(BLOCK_LEN):
							dct_coeff[i+k1:i+BLOCK_LEN+k1, j+k2:j+k2+BLOCK_LEN] += \
									np.cos(np.pi/BLOCK_LEN * (n1 + 0.5) * k1) *\
									np.cos(np.pi/BLOCK_LEN * (n2 + 0.5) * k2) *\
									block[n1, n2]

	plt.imshow(dct_coeff)

encode(sys.argv[1])
