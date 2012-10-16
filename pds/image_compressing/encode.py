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
NUM_COEF = 8

def encode(file_name):
	image = imread(file_name)
#	image = np.array([[3, 4], [8, 2]])
	image = image[:32,:32]

	dct_coeff = np.zeros(image.shape)
	new_image = np.zeros(image.shape)

	for i_shift in xrange(image.shape[0] / BLOCK_LEN):
		print i_shift
		for j_shift in xrange(image.shape[1] / BLOCK_LEN):
			i = i_shift * BLOCK_LEN
			j = j_shift * BLOCK_LEN
#			block = image[i:i+BLOCK_LEN, j:j+BLOCK_LEN]
			alfa = lambda x: np.sqrt(1./BLOCK_LEN) if x == 0 else np.sqrt(2./BLOCK_LEN)
			for k1 in xrange(NUM_COEF):
				for k2 in xrange(NUM_COEF):
					for n1 in xrange(BLOCK_LEN):
						for n2 in xrange(BLOCK_LEN):
							dct_coeff[i+k1, j+k2] += \
									np.cos(np.pi/BLOCK_LEN * (n1 + .5) * k1) *\
									np.cos(np.pi/BLOCK_LEN * (n2 + .5) * k2) *\
									image[i+n1, j+n2]
					dct_coeff[i+k1, j+k2] *= alfa(k1) * alfa(k2)
			for n1 in xrange(BLOCK_LEN):
				for n2 in xrange(BLOCK_LEN):
					new_idx = i+n1, j+n2
					for k1 in xrange(BLOCK_LEN):
						for k2 in xrange(BLOCK_LEN):
							new_image[new_idx] += \
									np.cos(np.pi/BLOCK_LEN * (n1 + .5) * k1) *\
									np.cos(np.pi/BLOCK_LEN * (n2 + .5) * k2) *\
									dct_coeff[i+k1, j+k2] *\
									alfa(k1) * alfa(k2)
	new_image = new_image.astype(int)
#	print "block\n", image
#	print "dct\n", dct_coeff
#	print "new_image\n", new_image
	print image - new_image
#	break
	plt.imshow(new_image)
	plt.figure()
	plt.imshow(image)
	plt.show()

encode(sys.argv[1])
