#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import random

class UtilArgumentError(Exception):
	pass

def flip_coin(prob=0.5):
	return True if random.random() < prob else False

def binary_to_real(min, max, value, num_bits):
	if isinstance(value, 'str'):
		if value.startswith('0b'):
			value = eval(value)
		else:
			value = int(value, 2)

	return float(value) * float(max-min)/(2**num_bits-1) + min
