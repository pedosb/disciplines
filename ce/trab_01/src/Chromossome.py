#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import random

from scipy import sin, sqrt

from util import flip_coin
from Allele import BinaryListAllele, BinaryAllele
from Gene import RealGene, Gene

class ChromossomeArgumentError(Exception):
	pass

class ChromossomeValueError(Exception):
	pass

class Chromossome(object):
	def __init__(self, alleles):
		self.alleles = list(alleles)

	def mutate(self, mutate_prob):
		return NotImplementedError()

	def cross_over(self, other):
		"""Return a list of generated chromossomes"""
		raise NotImplementedError()

	def __len__(self):
		return len(self.alleles)

class RealChromossome(Chromossome):
	def __init__(self, min, max, num_bits, value=None):
		if num_bits is None and value is None:
			raise ChromossomeArgumentError(
					"Need num_bits or value to build a Real Chromossome")

		self.min = min
		self.max = max
		self.num_bits = num_bits

		if value is None:
			self._value = random.getrandbits(self.num_bits)
		elif isinstance(value, str):
			if value.startswith('0b'):
				self._value = eval(value)
			else:
				self._value = int(value, 2)
		elif isinstance(value, list):
			self._value = int(''.join(value), 2)
		else:
			self._value = value

		Chromossome.__init__(self, self.bit_str())

	def cross_over(self, other):
		point = random.randint(0, len(self.alleles))
		if len(self) != len(other):
			raise ChromossomeArgumentError("Chromossomes size must match")

		return (RealChromossome(self.min, self.max, self.num_bits,
				self.alleles[:point] + other.alleles[point:]),
			RealChromossome(self.min, self.max, self.num_bits,
				other.alleles[:point] + self.alleles[point:]))

	def mutate(self, mutate_prob):
		for idx, allele in enumerate(self.alleles):
			if flip_coin(mutate_prob):
				self.alleles[idx] = '1' if allele == '0' else '0'

	@property
	def real(self):
		return self._value * float(self.max-self.min)/(2**self.num_bits-1) +\
				self.min

	def bit_str(self):
		self_str = bin(self._value)[2:]
		#Insert zeros to complement the binary string
		return ('0' * (self.num_bits - len(self_str))) + self_str

	def __str__(self):
		return '%s (%.6f)' % (self.bit_str(), self.real)

class Trab1ChromossomeError(Exception):
	pass

def __str__(self):
	s = ""
	if self.point is not None:
		bs = self.bit_str()
		s += "Alleles: %s %s\n" % (bs[:self.point], bs[self.point:])
	else:
		s += "Alleles: %s\n" % self.bit_str()
	s += "X: %s (%.6f)\n" % (self.bit_str()[:self.num_bits_x], self.x)
	s += "Y: %s (%.6f)\n" % (self.bit_str()[-self.num_bits_y:], self.y)
	s += "Score: %.6f\n" % self.score
	if self.point is not None:
		s += "Cross Point: %d\n" % self.point
		s += "Father:\n"
		bs = self.father.bit_str()
		s += "\t Alleles: %s %s\n" % (bs[:self.point], bs[self.point:])
		s += "\t Score: %.6f\n" % self.father.score
		s += "Mother:\n"
		bs = self.mother.bit_str()
		s += "\t Alleles: %s %s\n" % (bs[:self.point], bs[self.point:])
		s += "\t Score: %.6f\n" % self.mother.score
	return s
